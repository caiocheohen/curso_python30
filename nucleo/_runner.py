"""Executor isolado de exercicios.

Uso interno: chamado como subprocesso pelo avaliador.

    python3 -m nucleo._runner <arquivo.py> <testes.json>

Imprime no stdout um JSON com o resultado de cada teste. Tudo que o aluno
imprimir e capturado e devolvido no campo "saida_aluno" para nao corromper
o protocolo.
"""

import io
import json
import runpy
import sys
import traceback
from contextlib import redirect_stdout


def _iguais(obtido, esperado) -> bool:
    """Compara resultado do aluno com o gabarito, com tolerancia para float."""
    if isinstance(esperado, bool) or isinstance(obtido, bool):
        return obtido is esperado
    if isinstance(esperado, float) and isinstance(obtido, (int, float)):
        return abs(obtido - esperado) < 1e-9
    if isinstance(esperado, (list, tuple)) and isinstance(obtido, (list, tuple)):
        return type(obtido) is type(esperado) and len(obtido) == len(esperado) and all(
            _iguais(a, b) for a, b in zip(obtido, esperado)
        )
    return obtido == esperado


def principal() -> int:
    arquivo, arquivo_testes = sys.argv[1], sys.argv[2]
    testes = json.loads(open(arquivo_testes, encoding="utf-8").read())

    buffer = io.StringIO()
    resultado = {"erro_carga": None, "saida_aluno": "", "testes": []}

    try:
        with redirect_stdout(buffer):
            ns = runpy.run_path(arquivo, run_name="__exercicio__")
    except BaseException:
        resultado["erro_carga"] = traceback.format_exc(limit=3)
        resultado["saida_aluno"] = buffer.getvalue()
        print(json.dumps(resultado))
        return 0

    for expr, esperado_src in testes:
        item = {"expr": expr, "esperado": esperado_src, "obtido": None,
                "passou": False, "erro": None}
        # Sintaxe especial: "!raise NomeDaExcecao" espera que a expressao falhe.
        if esperado_src.startswith("!raise "):
            alvo = esperado_src.split(None, 1)[1].strip()
            try:
                with redirect_stdout(buffer):
                    obtido = eval(expr, ns)      # noqa: S307
                item["obtido"] = repr(obtido)
                item["erro"] = f"nao levantou {alvo}"
            except BaseException as exc:
                nomes = [c.__name__ for c in type(exc).__mro__]
                item["obtido"] = type(exc).__name__
                item["passou"] = alvo in nomes
                if not item["passou"]:
                    item["erro"] = f"levantou {type(exc).__name__} em vez de {alvo}"
            resultado["testes"].append(item)
            continue

        try:
            with redirect_stdout(buffer):
                obtido = eval(expr, ns)      # noqa: S307 - ambiente de estudo
                esperado = eval(esperado_src, ns)
            item["obtido"] = repr(obtido)
            item["passou"] = _iguais(obtido, esperado)
        except BaseException:
            item["erro"] = traceback.format_exc(limit=2).strip().split("\n")[-1]
        resultado["testes"].append(item)

    resultado["saida_aluno"] = buffer.getvalue()
    print(json.dumps(resultado))
    return 0


if __name__ == "__main__":
    sys.exit(principal())
