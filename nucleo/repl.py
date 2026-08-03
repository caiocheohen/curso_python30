"""Gerenciamento de sessoes de REPL Python isoladas.

Cada sessao e um processo `python3 -i` de verdade, mantido vivo entre
requisicoes HTTP. Uma thread por sessao le a saida continuamente (stdout
e stderr combinados) para uma fila, porque pipes nao suportam select()
de forma portavel no Windows -- thread bloqueante e a solucao que
funciona igual em Linux, macOS e Windows.

Cada aba do navegador tem sua propria sessao (identificada por um UUID
gerado no cliente). Sessoes sem uso por mais de TEMPO_OCIOSO segundos
sao encerradas automaticamente por uma thread de limpeza.
"""

from __future__ import annotations

import queue
import subprocess
import sys
import threading
import time
import uuid

TEMPO_OCIOSO = 30 * 60          # 30 minutos sem uso -> encerra a sessao
TIMEOUT_LEITURA = 0.05           # intervalo de poll da fila de saida
LIMITE_SAIDA = 4000              # caracteres maximos devolvidos por chamada

_sessoes: dict[str, "SessaoRepl"] = {}
_trava = threading.Lock()


class SessaoRepl:
    """Uma sessao de REPL: um processo `python3 -i` isolado."""

    def __init__(self) -> None:
        self.id = uuid.uuid4().hex
        self.fila: queue.Queue[str] = queue.Queue()
        self.ultimo_uso = time.time()
        self._trava_uso = threading.Lock()
        self.processo: subprocess.Popen | None = None
        self._thread_leitura: threading.Thread | None = None
        self._iniciar_processo()

    def _iniciar_processo(self) -> None:
        # -u: saida sem buffer, essencial para ler linha a linha em tempo real
        # -i: modo interativo, mantem o interpretador esperando por comandos
        # -q: sem a mensagem de boas-vindas do Python
        self.processo = subprocess.Popen(
            [sys.executable, "-u", "-i", "-q"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        self._thread_leitura = threading.Thread(
            target=self._ler_saida, daemon=True
        )
        self._thread_leitura.start()

    def _ler_saida(self) -> None:
        """Roda em thread separada: le a saida do processo continuamente."""
        proc = self.processo
        if proc is None or proc.stdout is None:
            return
        try:
            for linha in proc.stdout:
                self.fila.put(linha)
        except (ValueError, OSError):
            pass  # processo encerrado durante a leitura

    def enviar(self, comando: str) -> str:
        """Envia um comando ao REPL e devolve a saida produzida ate agora."""
        with self._trava_uso:
            self.ultimo_uso = time.time()
            if self.processo is None or self.processo.poll() is not None:
                self._iniciar_processo()
                # Descarta o eventual prompt residual do processo novo
                time.sleep(0.1)
                self._drenar_fila()

            try:
                self.processo.stdin.write(comando + "\n")
                self.processo.stdin.flush()
            except (BrokenPipeError, OSError):
                self._iniciar_processo()
                return "[sessão reiniciada automaticamente — processo travado]"

            # Aguarda um pouco para a saida chegar via thread de leitura
            time.sleep(0.12)
            saida = self._drenar_fila()
            return saida[-LIMITE_SAIDA:] if len(saida) > LIMITE_SAIDA else saida

    def _drenar_fila(self) -> str:
        partes = []
        try:
            while True:
                partes.append(self.fila.get_nowait())
        except queue.Empty:
            pass
        return "".join(partes)

    def reiniciar(self) -> None:
        """Mata o processo atual e sobe um novo, limpo."""
        with self._trava_uso:
            self._matar()
            self._iniciar_processo()
            self.ultimo_uso = time.time()

    def _matar(self) -> None:
        if self.processo is not None and self.processo.poll() is None:
            try:
                self.processo.kill()
                self.processo.wait(timeout=2)
            except Exception:
                pass

    def encerrar(self) -> None:
        with self._trava_uso:
            self._matar()


def obter_ou_criar(sessao_id: str) -> SessaoRepl:
    with _trava:
        sessao = _sessoes.get(sessao_id)
        if sessao is None:
            sessao = SessaoRepl()
            sessao.id = sessao_id
            _sessoes[sessao_id] = sessao
        return sessao


def enviar_comando(sessao_id: str, comando: str) -> str:
    sessao = obter_ou_criar(sessao_id)
    return sessao.enviar(comando)


def reiniciar_sessao(sessao_id: str) -> None:
    sessao = _sessoes.get(sessao_id)
    if sessao is not None:
        sessao.reiniciar()
    else:
        obter_ou_criar(sessao_id)


def encerrar_sessao(sessao_id: str) -> None:
    with _trava:
        sessao = _sessoes.pop(sessao_id, None)
    if sessao is not None:
        sessao.encerrar()


def _limpar_ociosas() -> None:
    """Roda para sempre em background: encerra sessoes sem uso ha muito tempo."""
    while True:
        time.sleep(60)
        agora = time.time()
        with _trava:
            expiradas = [
                sid for sid, s in _sessoes.items()
                if agora - s.ultimo_uso > TEMPO_OCIOSO
            ]
            for sid in expiradas:
                _sessoes.pop(sid, None).encerrar()


def iniciar_limpeza_em_background() -> None:
    threading.Thread(target=_limpar_ociosas, daemon=True).start()


def encerrar_todas() -> None:
    """Chamado ao desligar o servidor: mata todos os processos REPL."""
    with _trava:
        for sessao in _sessoes.values():
            sessao.encerrar()
        _sessoes.clear()
