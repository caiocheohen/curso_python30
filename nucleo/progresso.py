"""Persistencia do progresso do aluno (JSON em ~/curso_python30/)."""

import json
import os
from datetime import date, datetime
from pathlib import Path


def diretorio_base() -> Path:
    """Diretorio de trabalho do aluno. Configuravel via CURSO_DIR."""
    base = os.environ.get("CURSO_DIR")
    p = Path(base).expanduser() if base else Path.home() / "curso_python30"
    p.mkdir(parents=True, exist_ok=True)
    (p / "exercicios").mkdir(exist_ok=True)
    return p


ARQUIVO = diretorio_base() / "progresso.json"

_MODELO = {
    "criado_em": "",
    "nome": "",
    "dias_lidos": [],          # [1, 2, ...]
    "exercicios_ok": [],       # ["d01e1", ...]
    "quiz": {},                # {"1": {"acertos": 2, "total": 2}}
    "sessoes": [],             # ["2026-07-28", ...]
    "minutos": 0,
    "notas": {},               # {"3": "revisar fatiamento"}
}


def carregar() -> dict:
    if ARQUIVO.exists():
        try:
            dados = json.loads(ARQUIVO.read_text(encoding="utf-8"))
            for k, v in _MODELO.items():
                dados.setdefault(k, v if not isinstance(v, (list, dict)) else type(v)())
            return dados
        except (json.JSONDecodeError, OSError):
            pass
    novo = json.loads(json.dumps(_MODELO))
    novo["criado_em"] = datetime.now().isoformat(timespec="seconds")
    return novo


def salvar(dados: dict) -> None:
    hoje = date.today().isoformat()
    if hoje not in dados["sessoes"]:
        dados["sessoes"].append(hoje)
    tmp = ARQUIVO.with_suffix(".tmp")
    tmp.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(ARQUIVO)


def marcar_dia_lido(dados: dict, dia: int) -> None:
    if dia not in dados["dias_lidos"]:
        dados["dias_lidos"].append(dia)
        dados["dias_lidos"].sort()
    salvar(dados)


def marcar_exercicio(dados: dict, ex_id: str) -> None:
    if ex_id not in dados["exercicios_ok"]:
        dados["exercicios_ok"].append(ex_id)
        dados["exercicios_ok"].sort()
    salvar(dados)


def registrar_quiz(dados: dict, dia: int, acertos: int, total: int) -> None:
    ant = dados["quiz"].get(str(dia), {"acertos": 0, "total": 0})
    if acertos >= ant["acertos"]:
        dados["quiz"][str(dia)] = {"acertos": acertos, "total": total}
    salvar(dados)


def sequencia(dados: dict) -> int:
    """Dias consecutivos de estudo (streak)."""
    if not dados["sessoes"]:
        return 0
    datas = sorted({date.fromisoformat(s) for s in dados["sessoes"]}, reverse=True)
    hoje = date.today()
    if (hoje - datas[0]).days > 1:
        return 0
    streak = 1
    for a, b in zip(datas, datas[1:]):
        if (a - b).days == 1:
            streak += 1
        else:
            break
    return streak


def salvar_nota(dados: dict, chave: str, texto: str) -> None:
    """Salva uma anotação. chave = 'geral' ou o numero do dia como string."""
    if texto.strip():
        dados["notas"][chave] = texto
    else:
        dados["notas"].pop(chave, None)
    salvar(dados)


def proximo_dia(dados: dict, total: int = 30) -> int:
    for d in range(1, total + 1):
        if d not in dados["dias_lidos"]:
            return d
    return total
