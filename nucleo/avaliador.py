"""Criacao e correcao automatica dos exercicios."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from . import progresso, ui
from .modelos import Exercicio

RAIZ = Path(__file__).resolve().parent.parent
TIMEOUT = 12  # segundos por exercicio


def caminho_exercicio(ex: Exercicio) -> Path:
    pasta = progresso.diretorio_base() / "exercicios" / f"dia{ex.dia:02d}"
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta / f"{ex.id}.py"


def modelo(ex: Exercicio) -> str:
    linhas = [
        f'"""Exercicio {ex.id} - Dia {ex.dia}',
        "",
    ]
    for l in ex.enunciado.strip().split("\n"):
        linhas.append(l.strip())
    linhas += ['"""', "", ""]
    if ex.assinatura.lstrip().startswith("def "):
        linhas += [
            ex.assinatura,
            '    """Escreva sua solucao aqui."""',
            "    # TODO: implemente e apague a linha abaixo",
            "    raise NotImplementedError",
        ]
    else:
        linhas += ["# TODO: complete o codigo abaixo", ex.assinatura]
    linhas += [
        "",
        "",
        'if __name__ == "__main__":',
        f"    # Teste rapido manual (opcional):",
        f"    print({ex.testes[0][0]})",
        "",
    ]
    return "\n".join(linhas)


def preparar(ex: Exercicio, sobrescrever: bool = False) -> Path:
    """Garante que o arquivo do exercicio exista e devolve o caminho."""
    caminho = caminho_exercicio(ex)
    if sobrescrever or not caminho.exists():
        caminho.write_text(modelo(ex), encoding="utf-8")
    return caminho


def executar(ex: Exercicio) -> dict:
    """Roda os testes do exercicio em subprocesso isolado."""
    caminho = preparar(ex)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                     encoding="utf-8") as f:
        json.dump(ex.testes, f)
        arq_testes = f.name
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "nucleo._runner", str(caminho), arq_testes],
            cwd=str(RAIZ), capture_output=True, text=True, timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return {"timeout": True, "testes": [], "erro_carga": None, "saida_aluno": ""}
    finally:
        Path(arq_testes).unlink(missing_ok=True)

    if proc.returncode != 0 or not proc.stdout.strip():
        return {"timeout": False, "testes": [], "saida_aluno": "",
                "erro_carga": proc.stderr or "Falha inesperada ao executar."}
    try:
        return json.loads(proc.stdout.strip().splitlines()[-1])
    except json.JSONDecodeError:
        return {"timeout": False, "testes": [], "saida_aluno": "",
                "erro_carga": proc.stdout}


def corrigir(ex: Exercicio, dados: dict) -> bool:
    """Roda, mostra o relatorio e registra o progresso. Devolve True se passou."""
    caminho = preparar(ex)
    ui.secao(f"Corrigindo {ex.id}")
    ui.info(f"arquivo: {caminho}")
    r = executar(ex)

    if r.get("timeout"):
        ui.erro(f"Tempo esgotado ({TIMEOUT}s). Provavel laco infinito.")
        return False

    if r.get("erro_carga"):
        ui.erro("O arquivo nao pode ser executado:")
        print(ui.C.VERMELHO + "    " +
              r["erro_carga"].strip().replace("\n", "\n    ") + ui.C.RESET)
        return False

    if r.get("saida_aluno", "").strip():
        ui.info("Voce imprimiu isto durante a execucao:")
        ui.saida(r["saida_aluno"])

    passou_tudo = True
    for t in r["testes"]:
        if t["passou"]:
            ui.ok(f"{t['expr']}  ->  {t['obtido']}")
        else:
            passou_tudo = False
            if t["erro"]:
                ui.erro(f"{t['expr']}  levantou  {t['erro']}")
            else:
                ui.erro(f"{t['expr']}  ->  {t['obtido']}   "
                        f"(esperado: {t['esperado']})")

    print()
    if passou_tudo and r["testes"]:
        ui.ok("Todos os testes passaram. Exercicio concluido!")
        progresso.marcar_exercicio(dados, ex.id)
    else:
        ui.aviso("Ainda nao. Ajuste o codigo e rode de novo.")
        if ex.dica:
            ui.info("Dica: " + ex.dica)
    return passou_tudo
