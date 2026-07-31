"""Interface de terminal: cores ANSI, caixas, realce simples de codigo.

Funciona em qualquer terminal Linux. Se a saida nao for um terminal
(por exemplo, `python3 curso.py | less`), as cores sao desativadas.
"""

import os
import re
import shutil
import sys

_TTY = sys.stdout.isatty() and os.environ.get("TERM") not in (None, "dumb")
_SEM_COR = os.environ.get("CURSO_SEM_COR") == "1"
ATIVO = _TTY and not _SEM_COR


def _c(codigo: str) -> str:
    return codigo if ATIVO else ""


class C:
    RESET = _c("\033[0m")
    NEGRITO = _c("\033[1m")
    FRACO = _c("\033[2m")
    ITALICO = _c("\033[3m")
    VERMELHO = _c("\033[31m")
    VERDE = _c("\033[32m")
    AMARELO = _c("\033[33m")
    AZUL = _c("\033[34m")
    MAGENTA = _c("\033[35m")
    CIANO = _c("\033[36m")
    CINZA = _c("\033[90m")
    FUNDO_AZUL = _c("\033[44m")


LARGURA = min(shutil.get_terminal_size((80, 24)).columns, 88)


def limpar() -> None:
    if ATIVO:
        os.system("clear")


def linha(ch: str = "-") -> None:
    print(C.CINZA + ch * LARGURA + C.RESET)


def titulo(texto: str) -> None:
    print()
    print(C.NEGRITO + C.CIANO + "=" * LARGURA + C.RESET)
    print(C.NEGRITO + C.CIANO + texto.center(LARGURA) + C.RESET)
    print(C.NEGRITO + C.CIANO + "=" * LARGURA + C.RESET)


def secao(texto: str) -> None:
    print()
    print(C.NEGRITO + C.AMARELO + ">> " + texto + C.RESET)
    linha()


def ok(texto: str) -> None:
    print(C.VERDE + "  [OK] " + texto + C.RESET)


def erro(texto: str) -> None:
    print(C.VERMELHO + "  [X]  " + texto + C.RESET)


def aviso(texto: str) -> None:
    print(C.AMARELO + "  [!]  " + texto + C.RESET)


def info(texto: str) -> None:
    print(C.CIANO + "  [i]  " + texto + C.RESET)


PALAVRAS_CHAVE = {
    "False", "None", "True", "and", "as", "assert", "async", "await", "break",
    "class", "continue", "def", "del", "elif", "else", "except", "finally",
    "for", "from", "global", "if", "import", "in", "is", "lambda", "match",
    "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with",
    "yield", "case", "self",
}


def _realce(linha_txt: str) -> str:
    if not ATIVO:
        return linha_txt
    # comentarios
    if "#" in linha_txt:
        antes, _, depois = linha_txt.partition("#")
        return _realce(antes) + C.CINZA + "#" + depois + C.RESET
    # strings
    def _str(m):
        return C.VERDE + m.group(0) + C.RESET
    linha_txt = re.sub(r"('[^']*'|\"[^\"]*\")", _str, linha_txt)

    def _kw(m):
        p = m.group(0)
        if p in PALAVRAS_CHAVE:
            return C.MAGENTA + p + C.RESET
        return p
    return re.sub(r"\b[A-Za-z_]\w*\b", _kw, linha_txt)


def codigo(fonte: str, numerar: bool = True) -> None:
    """Imprime um bloco de codigo com fundo destacado."""
    print()
    linhas = fonte.strip("\n").split("\n")
    largura_num = len(str(len(linhas)))
    for i, l in enumerate(linhas, 1):
        prefixo = f"{C.CINZA}{str(i).rjust(largura_num)} | {C.RESET}" if numerar else "    "
        print("  " + prefixo + _realce(l))
    print()


def saida(texto: str) -> None:
    """Mostra a saida esperada de um codigo."""
    print(C.CINZA + "  saida:" + C.RESET)
    for l in texto.strip("\n").split("\n"):
        print(C.CINZA + "    | " + C.RESET + l)
    print()


def paragrafo(texto: str) -> None:
    """Imprime texto corrido com quebra de linha respeitando a largura."""
    import textwrap
    for bloco in texto.split("\n"):
        if not bloco.strip():
            print()
        elif bloco.startswith("    ") or bloco.startswith("\t"):
            print(_realce(bloco))
        else:
            for l in textwrap.wrap(bloco, width=LARGURA - 2):
                print("  " + l)


def barra(atual: int, total: int, largura: int = 30) -> str:
    frac = 0 if total == 0 else atual / total
    cheio = int(frac * largura)
    return (C.VERDE + "#" * cheio + C.CINZA + "." * (largura - cheio) + C.RESET
            + f" {atual}/{total} ({frac*100:4.0f}%)")


def pausar(msg: str = "Pressione ENTER para continuar...") -> None:
    try:
        input(C.CINZA + "\n  " + msg + C.RESET)
    except (EOFError, KeyboardInterrupt):
        print()
        raise SystemExit(0)


def perguntar(msg: str, padrao: str = "") -> str:
    try:
        r = input(C.NEGRITO + "  " + msg + C.RESET).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        raise SystemExit(0)
    return r or padrao


def menu(opcoes: list, cabecalho: str = "") -> str:
    """Mostra um menu numerado e devolve a chave escolhida."""
    if cabecalho:
        secao(cabecalho)
    for chave, rotulo in opcoes:
        print(f"   {C.NEGRITO}{C.AMARELO}{chave}{C.RESET}) {rotulo}")
    print()
    return perguntar("Escolha: ").lower()
