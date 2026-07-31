"""Reúne o conteúdo das quatro semanas em uma única lista de 30 dias."""

from . import semana1, semana2, semana3, semana4

DIAS = semana1.DIAS + semana2.DIAS + semana3.DIAS + semana4.DIAS
DIAS.sort(key=lambda d: d.numero)

TOTAL_DIAS = len(DIAS)
TODOS_EXERCICIOS = [e for d in DIAS for e in d.exercicios]
TOTAL_EXERCICIOS = len(TODOS_EXERCICIOS)


def por_numero(numero: int):
    for d in DIAS:
        if d.numero == numero:
            return d
    return None


def exercicio_por_id(ex_id: str):
    for e in TODOS_EXERCICIOS:
        if e.id == ex_id.lower():
            return e
    return None


def buscar(termo: str):
    """Busca simples por título, objetivos e teoria. Devolve lista de (Dia, trecho)."""
    termo = termo.lower().strip()
    achados = []
    for d in DIAS:
        alvo = " ".join([d.titulo, " ".join(d.objetivos), d.teoria]).lower()
        if termo in alvo:
            pos = alvo.find(termo)
            trecho = alvo[max(0, pos - 60):pos + 80].replace("\n", " ")
            achados.append((d, "..." + trecho.strip() + "..."))
    return achados
