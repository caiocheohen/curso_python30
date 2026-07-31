#!/usr/bin/env bash
# Instalador opcional: cria o atalho "curso" em ~/.local/bin
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESTINO="$HOME/.local/bin"
ATALHO="$DESTINO/curso"

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
    print("AVISO: recomendado Python 3.10+. Alguns exercicios (match, |, "
          "TaskGroup) podem nao funcionar nesta versao.")
EOF

mkdir -p "$DESTINO"
cat > "$ATALHO" <<EOF
#!/usr/bin/env bash
exec python3 "$RAIZ/curso.py" "\$@"
EOF
cat > "$DESTINO/curso-gui" <<EOF
#!/usr/bin/env bash
exec python3 "$RAIZ/curso_web.py" "\$@"
EOF
chmod +x "$ATALHO" "$DESTINO/curso-gui" "$RAIZ/curso.py" "$RAIZ/curso_web.py"

echo ">> Atalhos criados:"
echo "   $ATALHO           (terminal)"
echo "   $DESTINO/curso-gui       (navegador)"
if ! echo "$PATH" | tr ':' '\n' | grep -qx "$DESTINO"; then
    echo ">> Adicione ao seu ~/.bashrc (ou ~/.zshrc):"
    echo '   export PATH="$HOME/.local/bin:$PATH"'
fi

echo
echo "Pronto! Comece com:"
echo "   curso-gui        interface gráfica no navegador"
echo "   curso            interface de terminal"
