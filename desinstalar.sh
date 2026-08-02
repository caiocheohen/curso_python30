#!/usr/bin/env bash
# Desinstalador do Curso de Python em 30 Dias
# Remove atalhos, icone, entrada no menu e atalho no desktop.
# O progresso do aluno (~/curso_python30/) e mantido por padrao.
set -euo pipefail

DESTINO="$HOME/.local/bin"
ICONE_DST="$HOME/.local/share/icons/curso-python30.png"
DESKTOP_FILE="$HOME/.local/share/applications/curso-python30.desktop"

# --------------------------------------------------------- confirmacao
echo ""
echo "========================================"
echo " Desinstalador — Curso Python 30 Dias"
echo "========================================"
echo ""
echo "Isso vai remover:"
echo "  - Atalhos de terminal (curso-python, curso-python-terminal)"
echo "  - Icone do desktop e do menu do sistema"
echo "  - Entrada no menu de aplicativos"
echo ""
echo "NAO sera removido:"
echo "  - Os arquivos do curso (esta pasta)"
echo "  - Seu progresso salvo em ~/curso_python30/"
echo ""
read -r -p "Continuar? [s/N] " CONFIRMA
case "$CONFIRMA" in
    [sS][iI][mM]|[sS]) ;;
    *)
        echo "Desinstalacao cancelada."
        exit 0
        ;;
esac

echo ""
REMOVIDOS=0

# --------------------------------------------------------- atalhos terminal
for ATALHO in "curso-python" "curso-python-terminal" "curso" "curso-gui"; do
    CAMINHO="$DESTINO/$ATALHO"
    if [ -f "$CAMINHO" ]; then
        rm -f "$CAMINHO"
        echo ">> Removido: $CAMINHO"
        REMOVIDOS=$((REMOVIDOS + 1))
    fi
done

# --------------------------------------------------------- icone
if [ -f "$ICONE_DST" ]; then
    rm -f "$ICONE_DST"
    echo ">> Removido: $ICONE_DST"
    REMOVIDOS=$((REMOVIDOS + 1))
fi

# --------------------------------------------------------- entrada no menu
if [ -f "$DESKTOP_FILE" ]; then
    rm -f "$DESKTOP_FILE"
    echo ">> Removido: $DESKTOP_FILE"
    REMOVIDOS=$((REMOVIDOS + 1))
fi

# Atualiza cache de aplicativos (silencioso se nao disponivel)
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
fi

# --------------------------------------------------------- atalho no desktop
for DESKTOP_DIR in \
    "$HOME/Desktop" \
    "$HOME/Ambiente de trabalho" \
    "$HOME/Escritorio"
do
    LINK="$DESKTOP_DIR/Curso Python 30 Dias.desktop"
    if [ -f "$LINK" ]; then
        rm -f "$LINK"
        echo ">> Removido: $LINK"
        REMOVIDOS=$((REMOVIDOS + 1))
    fi
done

# --------------------------------------------------------- resultado
echo ""
if [ "$REMOVIDOS" -eq 0 ]; then
    echo "Nada encontrado para remover."
    echo "(O curso pode nao ter sido instalado com instalar.sh)"
else
    echo "========================================"
    echo " $REMOVIDOS item(s) removido(s). Tudo limpo!"
    echo "========================================"
    echo ""
    echo "Seu progresso continua salvo em ~/curso_python30/"
    echo "Para reinstalar, execute: bash instalar.sh"
fi
echo ""
