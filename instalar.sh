#!/usr/bin/env bash
# Instalador do Curso de Python em 30 Dias
# Cria atalhos no terminal, icone no desktop e entrada no menu do sistema.
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESTINO="$HOME/.local/bin"
ICONE_SRC="$RAIZ/assets/icon.png"
ICONE_DST="$HOME/.local/share/icons/curso-python30.png"
DESKTOP_FILE="$HOME/.local/share/applications/curso-python30.desktop"
DESKTOP_LINK="$HOME/Desktop/Curso Python 30 Dias.desktop"

# --------------------------------------------------------- python
echo ">> Verificando o Python..."
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERRO: python3 nao encontrado."
    echo "  Debian/Ubuntu: sudo apt install python3"
    echo "  Fedora:        sudo dnf install python3"
    echo "  Arch:          sudo pacman -S python"
    exit 1
fi

VERSAO=$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')
echo "   Python $VERSAO encontrado."
python3 - <<'EOF'
import sys
if sys.version_info < (3, 10):
    print("AVISO: recomendado Python 3.10+. Alguns exercicios (match, |, TaskGroup) podem nao funcionar.")
EOF

# --------------------------------------------------------- atalhos terminal
mkdir -p "$DESTINO"

cat > "$DESTINO/curso-python" <<EOF
#!/usr/bin/env bash
exec python3 "$RAIZ/curso_web.py" "\$@"
EOF

cat > "$DESTINO/curso-python-terminal" <<EOF
#!/usr/bin/env bash
exec python3 "$RAIZ/curso.py" "\$@"
EOF

chmod +x "$DESTINO/curso-python" \
         "$DESTINO/curso-python-terminal" \
         "$RAIZ/curso.py" \
         "$RAIZ/curso_web.py"

echo ">> Atalhos de terminal criados:"
echo "   curso-python           (abre no navegador)"
echo "   curso-python-terminal  (interface de terminal)"

# --------------------------------------------------------- icone
mkdir -p "$(dirname "$ICONE_DST")"
if [ -f "$ICONE_SRC" ]; then
    cp "$ICONE_SRC" "$ICONE_DST"
    echo ">> Icone instalado em $ICONE_DST"
else
    echo "AVISO: icone nao encontrado em $ICONE_SRC — desktop sem icone."
fi

# --------------------------------------------------------- entrada .desktop
mkdir -p "$(dirname "$DESKTOP_FILE")"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Curso Python 30 Dias
GenericName=Curso de Python
Comment=Python do Zero ao Avancado em 30 Dias
Exec=python3 $RAIZ/curso_web.py
Icon=$ICONE_DST
Terminal=false
Categories=Education;Development;
Keywords=python;curso;programacao;
StartupNotify=true
EOF

echo ">> Entrada no menu do sistema criada."

# --------------------------------------------------------- atalho no desktop
if [ -d "$HOME/Desktop" ]; then
    DESKTOP_DIR="$HOME/Desktop"
elif [ -d "$HOME/Ambiente de trabalho" ]; then
    DESKTOP_DIR="$HOME/Ambiente de trabalho"
elif [ -d "$HOME/Escritorio" ]; then
    DESKTOP_DIR="$HOME/Escritorio"
else
    DESKTOP_DIR=""
fi

if [ -n "$DESKTOP_DIR" ]; then
    cp "$DESKTOP_FILE" "$DESKTOP_DIR/Curso Python 30 Dias.desktop"
    chmod +x "$DESKTOP_DIR/Curso Python 30 Dias.desktop"

    # Marca como confiavel no GNOME (evita o aviso "arquivo nao confiavel")
    if command -v gio >/dev/null 2>&1; then
        gio set "$DESKTOP_DIR/Curso Python 30 Dias.desktop" \
            metadata::trusted true 2>/dev/null || true
    fi

    echo ">> Icone criado no desktop: $DESKTOP_DIR/Curso Python 30 Dias.desktop"
else
    echo ">> Desktop nao encontrado — use o menu do sistema para abrir o curso."
fi

# --------------------------------------------------------- PATH
if ! echo "$PATH" | tr ':' '\n' | grep -qx "$DESTINO"; then
    echo ""
    echo ">> Adicione ao seu ~/.bashrc (ou ~/.zshrc) para usar no terminal:"
    echo '   export PATH="$HOME/.local/bin:$PATH"'
fi

# --------------------------------------------------------- fim
echo ""
echo "========================================"
echo " Instalacao concluida!"
echo "========================================"
echo ""
echo "  Clique duplo no icone do desktop, ou:"
echo "  curso-python           -- abre no navegador"
echo "  curso-python-terminal  -- interface de terminal"
echo ""
