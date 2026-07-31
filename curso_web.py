#!/usr/bin/env python3
"""Interface gráfica do Curso de Python em 30 Dias.

Sobe um servidor HTTP local (só 127.0.0.1) e abre o navegador. Usa apenas a
biblioteca padrão: nada de Flask, Django ou npm. O motor é o mesmo da versão
de terminal — `conteudo`, `nucleo.avaliador` e `nucleo.progresso` —, então o
progresso é compartilhado entre as duas interfaces.

    python3 curso_web.py
    python3 curso_web.py --porta 9000 --sem-navegador
"""

from __future__ import annotations

import argparse
import json
import re
import secrets
import sys
import threading
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

import conteudo                                  # noqa: E402
from nucleo import avaliador, progresso          # noqa: E402

WEB = RAIZ / "web"
TOKEN = secrets.token_urlsafe(16)

TIPOS = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
}


# --------------------------------------------------------------------------
# Conversão do conteúdo para JSON
# --------------------------------------------------------------------------

def blocos_teoria(texto: str) -> list[dict]:
    """Quebra a teoria em blocos (titulo | codigo | texto) para o navegador.

    Convenções do material: título é uma linha seguida de outra só com '---';
    bloco de código é indentado com 4 espaços; o resto é prosa.
    """
    linhas = texto.split("\n")
    blocos: list[dict] = []
    prosa: list[str] = []
    codigo: list[str] = []

    def fechar_prosa() -> None:
        if prosa:
            inteiro = "\n".join(prosa).strip("\n")
            for paragrafo in re.split(r"\n\s*\n", inteiro):
                if paragrafo.strip():
                    blocos.append({"tipo": "texto", "conteudo": paragrafo.strip()})
            prosa.clear()

    def fechar_codigo() -> None:
        if codigo:
            blocos.append({"tipo": "codigo",
                           "conteudo": "\n".join(codigo).strip("\n")})
            codigo.clear()

    i = 0
    while i < len(linhas):
        linha = linhas[i]
        seguinte = linhas[i + 1] if i + 1 < len(linhas) else ""
        sublinhado = seguinte.strip()

        if linha.strip() and sublinhado and set(sublinhado) == {"-"} and len(sublinhado) >= 3:
            fechar_codigo()
            fechar_prosa()
            blocos.append({"tipo": "titulo", "conteudo": linha.strip()})
            i += 2
            continue

        if linha.startswith("    "):
            fechar_prosa()
            codigo.append(linha[4:])
            i += 1
            continue

        if not linha.strip() and codigo:
            # linha em branco: só continua o bloco de código se o próximo
            # trecho não-vazio também estiver indentado
            j = i + 1
            while j < len(linhas) and not linhas[j].strip():
                j += 1
            if j < len(linhas) and linhas[j].startswith("    "):
                codigo.append("")
                i += 1
                continue
            fechar_codigo()
            i += 1
            continue

        fechar_codigo()
        prosa.append(linha)
        i += 1

    fechar_codigo()
    fechar_prosa()
    return blocos


def _resumo_dia(dia, dados: dict) -> dict:
    ids = [e.id for e in dia.exercicios]
    feitos = [i for i in ids if i in dados.get("exercicios_ok", [])]
    nota = dados.get("quiz", {}).get(str(dia.numero))
    return {
        "numero": dia.numero,
        "titulo": dia.titulo,
        "nivel": dia.nivel,
        "duracao": dia.duracao,
        "lido": dia.numero in dados.get("dias_lidos", []),
        "exercicios": len(ids),
        "exercicios_ok": len(feitos),
        "quiz": nota,
    }


def _exercicio_json(ex, dados: dict) -> dict:
    caminho = avaliador.preparar(ex)
    return {
        "id": ex.id,
        "enunciado": ex.enunciado,
        "nivel": ex.nivel,
        "dica": ex.dica,
        "assinatura": ex.assinatura,
        "testes": [{"expr": e, "esperado": r} for e, r in ex.testes],
        "codigo": caminho.read_text(encoding="utf-8"),
        "arquivo": str(caminho),
        "resolvido": ex.id in dados.get("exercicios_ok", []),
    }


def dia_json(numero: int) -> dict | None:
    dia = conteudo.por_numero(numero)
    if dia is None:
        return None
    dados = progresso.carregar()
    return {
        "numero": dia.numero,
        "titulo": dia.titulo,
        "nivel": dia.nivel,
        "duracao": dia.duracao,
        "objetivos": dia.objetivos,
        "teoria": blocos_teoria(dia.teoria),
        "exemplos": [{"titulo": x.titulo, "codigo": x.codigo,
                      "explicacao": x.explicacao} for x in dia.exemplos],
        "exercicios": [_exercicio_json(e, dados) for e in dia.exercicios],
        "quiz": [{"pergunta": q.pergunta, "alternativas": q.alternativas}
                 for q in dia.quiz],
        "projeto": dia.projeto,
        "leitura": dia.leitura,
        "lido": dia.numero in dados.get("dias_lidos", []),
        "nota_quiz": dados.get("quiz", {}).get(str(dia.numero)),
    }


def painel_json() -> dict:
    dados = progresso.carregar()
    quizzes = dados.get("quiz", {})
    acertos = sum(q["acertos"] for q in quizzes.values())
    total_q = sum(q["total"] for q in quizzes.values())
    return {
        "dias": [_resumo_dia(d, dados) for d in conteudo.DIAS],
        "total_dias": conteudo.TOTAL_DIAS,
        "total_exercicios": conteudo.TOTAL_EXERCICIOS,
        "dias_lidos": len(dados.get("dias_lidos", [])),
        "exercicios_ok": len(dados.get("exercicios_ok", [])),
        "quiz_acertos": acertos,
        "quiz_total": total_q,
        "sequencia": progresso.sequencia(dados),
        "sessoes": len(dados.get("sessoes", [])),
        "proximo": progresso.proximo_dia(dados, conteudo.TOTAL_DIAS),
        "pasta": str(progresso.diretorio_base()),
    }


# --------------------------------------------------------------------------
# Ações
# --------------------------------------------------------------------------

def acao_salvar(corpo: dict) -> dict:
    ex = conteudo.exercicio_por_id(corpo.get("id", ""))
    if ex is None:
        return {"erro": "exercício não encontrado"}
    caminho = avaliador.caminho_exercicio(ex)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(corpo.get("codigo", ""), encoding="utf-8")
    return {"ok": True, "arquivo": str(caminho)}


def acao_testar(corpo: dict) -> dict:
    ex = conteudo.exercicio_por_id(corpo.get("id", ""))
    if ex is None:
        return {"erro": "exercício não encontrado"}
    acao_salvar(corpo)
    r = avaliador.executar(ex)
    passou = (not r.get("timeout") and not r.get("erro_carga")
              and bool(r["testes"]) and all(t["passou"] for t in r["testes"]))
    if passou:
        dados = progresso.carregar()
        progresso.marcar_exercicio(dados, ex.id)
        progresso.salvar(dados)
    return {
        "passou": passou,
        "timeout": bool(r.get("timeout")),
        "erro_carga": r.get("erro_carga"),
        "saida_aluno": r.get("saida_aluno", ""),
        "testes": r.get("testes", []),
        "dica": ex.dica,
    }


def acao_recriar(corpo: dict) -> dict:
    ex = conteudo.exercicio_por_id(corpo.get("id", ""))
    if ex is None:
        return {"erro": "exercício não encontrado"}
    caminho = avaliador.preparar(ex, sobrescrever=True)
    return {"ok": True, "codigo": caminho.read_text(encoding="utf-8")}


def acao_quiz(corpo: dict) -> dict:
    dia = conteudo.por_numero(int(corpo.get("dia", 0)))
    if dia is None:
        return {"erro": "dia não encontrado"}
    respostas = corpo.get("respostas", [])
    correcao, acertos = [], 0
    for i, q in enumerate(dia.quiz):
        marcada = respostas[i] if i < len(respostas) else None
        certo = marcada == q.correta
        acertos += int(certo)
        correcao.append({"certo": certo, "correta": q.correta,
                         "explicacao": q.explicacao})
    dados = progresso.carregar()
    progresso.registrar_quiz(dados, dia.numero, acertos, len(dia.quiz))
    progresso.salvar(dados)
    return {"acertos": acertos, "total": len(dia.quiz), "correcao": correcao}


def acao_lido(corpo: dict) -> dict:
    dados = progresso.carregar()
    progresso.marcar_dia_lido(dados, int(corpo.get("dia", 0)))
    progresso.salvar(dados)
    return {"ok": True}


def acao_buscar(termo: str) -> dict:
    achados = conteudo.buscar(termo) if termo.strip() else []
    return {"resultados": [{"numero": d.numero, "titulo": d.titulo,
                            "trecho": t} for d, t in achados]}


# --------------------------------------------------------------------------
# Servidor
# --------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    server_version = "CursoPython30"
    # HTTP/1.0: uma conexão por requisição. Keep-alive do 1.1 travava pedidos
    # em sequência e não traz ganho nenhum num servidor local de um usuário só.
    protocol_version = "HTTP/1.0"

    def log_message(self, formato, *args):     # silencia o log padrão
        pass

    # -- utilidades ---------------------------------------------------------
    def _host_local(self) -> bool:
        host = (self.headers.get("Host") or "").split(":")[0]
        return host in ("127.0.0.1", "localhost", "[::1]", "::1")

    def _autorizado(self) -> bool:
        if self.headers.get("X-Token") == TOKEN:
            return True
        query = parse_qs(urlparse(self.path).query)
        return query.get("t", [""])[0] == TOKEN

    def _enviar(self, corpo: bytes, tipo: str, status=HTTPStatus.OK) -> None:
        self.send_response(status)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(corpo)

    def _json(self, dados, status=HTTPStatus.OK) -> None:
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self._enviar(corpo, "application/json; charset=utf-8", status)

    def _erro(self, status, mensagem: str) -> None:
        self._json({"erro": mensagem}, status)

    def _ler_corpo(self) -> dict:
        tamanho = int(self.headers.get("Content-Length") or 0)
        if tamanho <= 0 or tamanho > 5_000_000:
            return {}
        try:
            return json.loads(self.rfile.read(tamanho).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}

    def _estatico(self, caminho: str) -> None:
        nome = caminho.lstrip("/") or "index.html"
        arquivo = (WEB / nome).resolve()
        if not str(arquivo).startswith(str(WEB.resolve())) or not arquivo.is_file():
            self._erro(HTTPStatus.NOT_FOUND, "arquivo não encontrado")
            return
        tipo = TIPOS.get(arquivo.suffix, "application/octet-stream")
        self._enviar(arquivo.read_bytes(), tipo)

    # -- rotas --------------------------------------------------------------
    def do_GET(self):                                    # noqa: N802
        if not self._host_local():
            self._erro(HTTPStatus.FORBIDDEN, "apenas acesso local")
            return
        url = urlparse(self.path)
        rota, query = url.path, parse_qs(url.query)

        if rota == "/":
            if not self._autorizado():
                self._enviar(b"Abra o endereco mostrado no terminal (com ?t=...).",
                             "text/plain; charset=utf-8", HTTPStatus.FORBIDDEN)
                return
            html = (WEB / "index.html").read_text(encoding="utf-8")
            html = html.replace("{{TOKEN}}", TOKEN)
            self._enviar(html.encode("utf-8"), TIPOS[".html"])
            return

        if not rota.startswith("/api/"):
            self._estatico(rota)
            return

        if not self._autorizado():
            self._erro(HTTPStatus.FORBIDDEN, "token inválido")
            return

        if rota == "/api/painel":
            self._json(painel_json())
        elif rota == "/api/dia":
            try:
                numero = int(query.get("n", ["0"])[0])
            except ValueError:
                self._erro(HTTPStatus.BAD_REQUEST, "número inválido")
                return
            dados = dia_json(numero)
            if dados is None:
                self._erro(HTTPStatus.NOT_FOUND, "dia não encontrado")
            else:
                self._json(dados)
        elif rota == "/api/buscar":
            self._json(acao_buscar(query.get("q", [""])[0]))
        else:
            self._erro(HTTPStatus.NOT_FOUND, "rota desconhecida")

    def do_POST(self):                                   # noqa: N802
        if not self._host_local():
            self._erro(HTTPStatus.FORBIDDEN, "apenas acesso local")
            return
        if not self._autorizado():
            self._erro(HTTPStatus.FORBIDDEN, "token inválido")
            return
        rota = urlparse(self.path).path
        corpo = self._ler_corpo()
        acoes = {
            "/api/salvar": acao_salvar,
            "/api/testar": acao_testar,
            "/api/recriar": acao_recriar,
            "/api/quiz": acao_quiz,
            "/api/lido": acao_lido,
        }
        if rota not in acoes:
            self._erro(HTTPStatus.NOT_FOUND, "rota desconhecida")
            return
        try:
            self._json(acoes[rota](corpo))
        except Exception as exc:                          # noqa: BLE001
            self._erro(HTTPStatus.INTERNAL_SERVER_ERROR, f"{type(exc).__name__}: {exc}")


def escolher_porta(inicial: int) -> int:
    import socket
    for porta in range(inicial, inicial + 40):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("127.0.0.1", porta))
                return porta
            except OSError:
                continue
    raise SystemExit("Nenhuma porta livre entre "
                     f"{inicial} e {inicial + 40}. Use --porta.")


def principal(argv=None) -> int:
    p = argparse.ArgumentParser(description="Interface gráfica do curso.")
    p.add_argument("--porta", type=int, default=8765)
    p.add_argument("--sem-navegador", action="store_true",
                   help="não abre o navegador automaticamente")
    args = p.parse_args(argv)

    if not (WEB / "index.html").is_file():
        raise SystemExit(f"Pasta 'web/' não encontrada em {RAIZ}.")

    # salvar() já registra a data de hoje na lista de sessões
    progresso.salvar(progresso.carregar())

    porta = escolher_porta(args.porta)
    endereco = f"http://127.0.0.1:{porta}/?t={TOKEN}"
    servidor = ThreadingHTTPServer(("127.0.0.1", porta), Handler)
    servidor.daemon_threads = True

    print("\n  Curso de Python em 30 Dias — interface gráfica")
    print("  " + "-" * 52)
    print(f"  Abra no navegador:  {endereco}")
    print(f"  Seus arquivos:      {progresso.diretorio_base()}")
    print("  Encerrar:           Ctrl+C\n")

    if not args.sem_navegador:
        threading.Timer(0.8, lambda: webbrowser.open(endereco)).start()

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n  Servidor encerrado. Até a próxima sessão.\n")
    finally:
        servidor.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(principal())
