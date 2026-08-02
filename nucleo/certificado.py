"""Geracao de certificado de conclusao do curso.

Verifica elegibilidade (todos os exercicios + media quiz >= 75%),
gera codigo unico e produz HTML completo para impressao em PDF.
"""

from __future__ import annotations

import hashlib
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

_MESES = [
    "Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]


# ---------------------------------------------------------------------------
# Elegibilidade
# ---------------------------------------------------------------------------

def verificar_elegibilidade(dados: dict) -> dict:
    """Verifica se o aluno pode emitir o certificado.

    Criterios:
        - Todos os 90 exercicios concluidos (3 por dia x 30 dias)
        - Media dos quizzes >= 75% (considerando apenas dias com quiz feito)

    Returns:
        dict com chaves:
            elegivel (bool)
            exercicios_faltando (list[str])   IDs dos exercicios nao feitos
            dias_sem_quiz (list[int])          dias cujo quiz nao foi feito
            media_quiz (float)                 media em % (0-100)
    """
    # Todos os IDs esperados: d01e1 .. d30e3
    todos_ids: list[str] = []
    for d in range(1, 31):
        for e in range(1, 4):
            todos_ids.append(f"d{d:02d}e{e}")

    feitos = set(dados.get("exercicios_ok", []))
    faltando = [ex for ex in todos_ids if ex not in feitos]

    quiz = dados.get("quiz", {})
    dias_sem_quiz = [d for d in range(1, 31) if str(d) not in quiz]

    notas = []
    for d in range(1, 31):
        q = quiz.get(str(d))
        if q and q["total"] > 0:
            notas.append(q["acertos"] / q["total"])

    media = round(sum(notas) / len(notas) * 100, 1) if notas else 0.0
    elegivel = (not faltando) and (not dias_sem_quiz) and (media >= 75.0)

    return {
        "elegivel": elegivel,
        "exercicios_faltando": faltando,
        "dias_sem_quiz": dias_sem_quiz,
        "media_quiz": media,
    }


# ---------------------------------------------------------------------------
# Codigo unico
# ---------------------------------------------------------------------------

def gerar_codigo(nome: str, cpf: str) -> str:
    """Gera codigo unico de validacao: PY30-AAAA-XXXXXXXX."""
    hoje = date.today().isoformat()
    semente = f"{nome.strip().upper()}:{cpf}:{hoje}:PYTHON30DIAS"
    h = hashlib.sha256(semente.encode("utf-8")).hexdigest()[:8].upper()
    return f"PY30-{hoje[:4]}-{h}"


# ---------------------------------------------------------------------------
# Assinatura protegida
# ---------------------------------------------------------------------------

def _html_assinatura() -> str:
    """Retorna assinatura cursiva como SVG embutido (sem arquivo externo)."""
    return '''
    <div class="sig-wrapper">
      <svg width="180" height="52" viewBox="0 0 180 52"
           xmlns="http://www.w3.org/2000/svg"
           style="display:block;margin:0 auto;user-select:none;pointer-events:none;">
        <text x="90" y="36"
              font-family="&apos;Brush Script MT&apos;, &apos;Segoe Script&apos;,
                           &apos;Dancing Script&apos;, &apos;Pacifico&apos;, cursive"
              font-size="30"
              fill="#2C1810"
              text-anchor="middle"
              font-style="italic">Caio Cheohen</text>
      </svg>
    </div>'''


# ---------------------------------------------------------------------------
# HTML do certificado
# ---------------------------------------------------------------------------

def gerar_html(nome: str, cpf: str, dados: dict) -> str:
    """Gera o HTML completo do certificado (frente + verso).

    Args:
        nome:   nome completo do aluno
        cpf:    CPF formatado (xxx.xxx.xxx-xx)
        dados:  dicionario de progresso (nucleo.progresso.carregar())

    Returns:
        String HTML pronta para abrir no navegador e imprimir como PDF.
    """
    import conteudo as _c  # importacao local para evitar ciclo

    codigo = gerar_codigo(nome, cpf)
    sig_html = _html_assinatura()

    hoje = date.today()
    data_fmt = f"{hoje.day} de {_MESES[hoje.month - 1]} de {hoje.year}"

    quiz = dados.get("quiz", {})
    notas = []
    for d in range(1, 31):
        q = quiz.get(str(d))
        if q and q["total"] > 0:
            notas.append(q["acertos"] / q["total"])
    media = round(sum(notas) / len(notas) * 100, 1) if notas else 0.0

    # Conteudo programatico para o verso (semanas agrupadas)
    semanas = {1: [], 2: [], 3: [], 4: []}
    for dia in _c.DIAS:
        semana = ((dia.numero - 1) // 7) + 1
        semanas[min(semana, 4)].append(dia)

    verso_html = _html_verso(semanas)
    frente_html = _html_frente(
        nome=nome,
        cpf=cpf,
        codigo=codigo,
        data_fmt=data_fmt,
        media=media,
        sig_html=sig_html,
    )

    return _montar_documento(frente_html, verso_html)


# ---------------------------------------------------------------------------
# Partes do HTML
# ---------------------------------------------------------------------------

def _html_frente(nome, cpf, codigo, data_fmt, media, sig_html) -> str:
    return f"""
    <div class="pagina frente">
      <div class="borda-ext"></div>
      <div class="borda-int"></div>
      <div class="canto c-tl"></div>
      <div class="canto c-tr"></div>
      <div class="canto c-bl"></div>
      <div class="canto c-br"></div>

      <header class="cert-header">
        <div class="emissor">Caio Cheohen &bull; MEI Educacional</div>
        <h1 class="cert-titulo">Certificado de Conclusao</h1>
        <div class="cert-subtitulo">Python do Zero ao Avancado em 30 Dias</div>
        <div class="divisor"></div>
      </header>

      <main class="cert-corpo">
        <p class="certifica-texto">Certificamos que</p>
        <p class="aluno-nome">{_esc(nome)}</p>
        <p class="aluno-cpf">CPF: {_esc(cpf)}</p>
        <p class="cert-descricao">
          concluiu com aproveitamento o curso
          <strong>Python do Zero ao Avancado em 30 Dias</strong>,
          abrangendo fundamentos da linguagem, estruturas de dados,
          orientacao a objetos, testes automatizados, concorrencia,
          programacao assincrona, expressoes regulares e boas praticas
          de desenvolvimento de software.
        </p>
      </main>

      <div class="cert-meta">
        <div class="meta-item">
          <div class="meta-label">Carga Horaria</div>
          <div class="meta-valor">45 horas</div>
        </div>
        <div class="meta-sep"></div>
        <div class="meta-item">
          <div class="meta-label">Aproveitamento</div>
          <div class="meta-valor">{media:.0f}% nos quizzes</div>
        </div>
        <div class="meta-sep"></div>
        <div class="meta-item">
          <div class="meta-label">Data de Conclusao</div>
          <div class="meta-valor">{data_fmt}</div>
        </div>
      </div>

      <footer class="cert-footer">
        <div class="assinatura-bloco">
          {sig_html}
          <div class="ass-linha"></div>
          <div class="ass-nome">Caio Cheohen</div>
          <div class="ass-cargo">Professor Responsavel</div>
          <div class="ass-cnpj">CNPJ 63.635.799/0001-02</div>
          <div class="ass-local">Macae &mdash; RJ</div>
        </div>
      </footer>
    </div>"""


def _html_verso(semanas: dict) -> str:
    semana_titulos = {
        1: "Semana 1 &mdash; Fundamentos",
        2: "Semana 2 &mdash; Colecoes, Funcoes e Arquivos",
        3: "Semana 3 &mdash; POO, Iteradores e Padroes Avancados",
        4: "Semana 4 &mdash; Testes, Sistemas e Projeto Final",
    }

    blocos = ""
    for num_semana, dias in semanas.items():
        itens = "\n".join(
            f'<li><span class="dia-num">Dia {d.numero:02d}</span>'
            f'<span class="dia-titulo">{_esc(d.titulo)}</span></li>'
            for d in dias
        )
        blocos += f"""
        <div class="semana-bloco">
          <h3 class="semana-titulo">{semana_titulos[num_semana]}</h3>
          <ul class="dias-lista">{itens}</ul>
        </div>"""

    return f"""
    <div class="pagina verso">
      <div class="borda-ext"></div>
      <div class="borda-int"></div>

      <header class="verso-header">
        <h2>Conteudo Programatico</h2>
        <p class="verso-sub">Python do Zero ao Avancado em 30 Dias &mdash; 45 horas</p>
      </header>

      <div class="semanas-grid">
        {blocos}
      </div>

      <footer class="verso-footer">
        Caio Cheohen &bull; Professor &bull; CNPJ 63.635.799/0001-02
        &bull; Macae &mdash; RJ
      </footer>
    </div>"""


def _montar_documento(frente: str, verso: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Certificado &mdash; Python 30 Dias</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  background: #e8e4dc;
  font-family: 'Inter', sans-serif;
  color: #1a1a1a;
}}

.pagina {{
  width: 297mm;
  min-height: 210mm;
  background: #fdfaf5;
  margin: 8mm auto;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20mm 22mm;
  overflow: hidden;
  page-break-after: always;
}}

/* --- bordas decorativas --- */
.borda-ext {{
  position: absolute; inset: 8mm;
  border: 1.5px solid #8B6914;
  pointer-events: none;
}}
.borda-int {{
  position: absolute; inset: 10.5mm;
  border: 0.5px solid #C9A84C;
  pointer-events: none;
}}
.canto {{
  position: absolute;
  width: 10mm; height: 10mm;
  border-color: #8B6914; border-style: solid;
}}
.c-tl {{ top: 12mm; left: 12mm; border-width: 1.5px 0 0 1.5px; }}
.c-tr {{ top: 12mm; right: 12mm; border-width: 1.5px 1.5px 0 0; }}
.c-bl {{ bottom: 12mm; left: 12mm; border-width: 0 0 1.5px 1.5px; }}
.c-br {{ bottom: 12mm; right: 12mm; border-width: 0 1.5px 1.5px 0; }}

/* --- frente: cabecalho --- */
.cert-header {{ text-align: center; margin-bottom: 5mm; }}
.emissor {{
  font-size: 7pt; letter-spacing: 3px; color: #8B6914;
  text-transform: uppercase; margin-bottom: 2mm;
}}
.cert-titulo {{
  font-family: 'Playfair Display', serif;
  font-size: 26pt; font-weight: 400; color: #2C1810;
  line-height: 1.1;
}}
.cert-subtitulo {{
  font-size: 7.5pt; letter-spacing: 2px; color: #8B6914;
  text-transform: uppercase; margin-top: 2mm;
}}
.divisor {{
  width: 40mm; height: 0.5px;
  background: linear-gradient(90deg, transparent, #8B6914, transparent);
  margin: 4mm auto;
}}

/* --- frente: corpo --- */
.cert-corpo {{ text-align: center; margin-bottom: 4mm; }}
.certifica-texto {{
  font-size: 8pt; color: #666; letter-spacing: 1px;
  text-transform: uppercase; margin-bottom: 2mm;
}}
.aluno-nome {{
  font-family: 'Playfair Display', serif;
  font-size: 22pt; font-weight: 700; color: #1a1a1a;
  margin: 1mm 0;
}}
.aluno-cpf {{
  font-size: 7.5pt; color: #888; letter-spacing: 1px;
  margin-bottom: 4mm;
}}
.cert-descricao {{
  font-size: 8.5pt; color: #555; line-height: 1.7;
  max-width: 180mm; margin: 0 auto;
}}

/* --- frente: meta --- */
.cert-meta {{
  display: flex; align-items: center; gap: 5mm;
  margin: 5mm 0; padding: 4mm 8mm;
  border-top: 0.5px solid #C9A84C;
  border-bottom: 0.5px solid #C9A84C;
}}
.meta-item {{ text-align: center; flex: 1; }}
.meta-label {{
  font-size: 6.5pt; letter-spacing: 1.5px; color: #8B6914;
  text-transform: uppercase; margin-bottom: 1mm;
}}
.meta-valor {{ font-size: 9pt; font-weight: 600; color: #2C1810; }}
.meta-sep {{ width: 0.5px; height: 8mm; background: #C9A84C; }}

/* --- frente: rodape --- */
.cert-footer {{
  display: flex; justify-content: center;
  align-items: flex-end; width: 100%; margin-top: 4mm;
}}
.assinatura-bloco {{ text-align: center; min-width: 55mm; }}

.sig-wrapper {{
  margin: 0 auto 1mm;
  user-select: none;
  pointer-events: none;
}}

.ass-linha {{
  width: 55mm; height: 0.5px; background: #8B6914; margin: 0 auto 1.5mm;
}}
.ass-nome {{ font-size: 8pt; font-weight: 600; color: #2C1810; }}
.ass-cargo {{ font-size: 7pt; color: #666; margin-top: 0.5mm; }}
.ass-cnpj {{ font-size: 6pt; color: #999; margin-top: 0.5mm; }}
.ass-local {{ font-size: 6pt; color: #999; }}



/* --- verso --- */
.verso {{
  padding: 15mm 20mm;
  justify-content: flex-start;
}}
.verso-header {{
  text-align: center; margin-bottom: 8mm; width: 100%;
  border-bottom: 0.5px solid #C9A84C; padding-bottom: 4mm;
}}
.verso-header h2 {{
  font-family: 'Playfair Display', serif;
  font-size: 18pt; font-weight: 400; color: #2C1810;
}}
.verso-sub {{
  font-size: 7pt; color: #8B6914; letter-spacing: 1.5px;
  text-transform: uppercase; margin-top: 2mm;
}}

.semanas-grid {{
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 6mm; width: 100%;
}}
.semana-bloco {{
  border: 0.5px solid #e8e0cc;
  padding: 4mm; background: rgba(139,105,20,0.02);
}}
.semana-titulo {{
  font-size: 8pt; font-weight: 600; color: #8B6914;
  text-transform: uppercase; letter-spacing: 1px;
  margin-bottom: 3mm; padding-bottom: 1.5mm;
  border-bottom: 0.5px solid #e8e0cc;
}}
.dias-lista {{
  list-style: none; display: flex; flex-direction: column; gap: 1.5mm;
}}
.dias-lista li {{
  display: flex; gap: 2mm; align-items: baseline; font-size: 7.5pt;
}}
.dia-num {{
  color: #8B6914; font-weight: 600; min-width: 10mm; font-size: 7pt;
}}
.dia-titulo {{ color: #444; }}

.verso-footer {{
  margin-top: auto; padding-top: 4mm;
  border-top: 0.5px solid #e8e0cc;
  width: 100%; text-align: center;
  font-size: 6.5pt; color: #aaa;
  letter-spacing: 1px;
}}

/* --- impressao --- */
@media print {{
  body {{ background: white; }}
  .pagina {{ margin: 0; width: 100%; min-height: 0; }}
}}
</style>
</head>
<body>
{frente}
{verso}
<script>
// Bloqueia inspecao de elemento e click-direito na pagina toda
document.addEventListener('contextmenu', e => e.preventDefault());
document.addEventListener('keydown', e => {{
  if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && ['I','J','C'].includes(e.key))) {{
    e.preventDefault();
  }}
}});
// Instrucao de impressao
if (!window.matchMedia('print').matches) {{
  const msg = document.createElement('div');
  msg.style.cssText = 'text-align:center;padding:6mm;font-family:sans-serif;font-size:9pt;color:#666;';
  msg.innerHTML = 'Para salvar como PDF: <strong>Ctrl+P</strong> &rarr; Destino: <strong>Salvar como PDF</strong> &rarr; Layout: <strong>Paisagem</strong>';
  document.body.insertBefore(msg, document.body.firstChild);
}}
</script>
</body>
</html>"""


def _esc(texto: str) -> str:
    return (texto
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))
