/* Curso de Python em 30 Dias — lógica da interface.
   Sem frameworks: DOM puro, do mesmo jeito que o curso é Python puro. */

const TOKEN = document.body.dataset.token;
const $ = (sel) => document.querySelector(sel);

const estado = {
  painel: null,
  dia: null,
  aba: "teoria",
  exercicio: 0,
  respostas: [],
  notas: { escopo: "geral", timer: null },
};

/* ----------------------------------------------------------- rede ------- */

async function api(rota, opcoes = {}) {
  const conf = Object.assign({ headers: {} }, opcoes);
  conf.headers["X-Token"] = TOKEN;
  if (conf.corpo !== undefined) {
    conf.method = "POST";
    conf.headers["Content-Type"] = "application/json";
    conf.body = JSON.stringify(conf.corpo);
    delete conf.corpo;
  }
  const resp = await fetch(rota, conf);
  const dados = await resp.json();
  if (!resp.ok) throw new Error(dados.erro || "falha na requisição");
  return dados;
}

let avisoTimer = null;
function avisar(texto, classe = "") {
  const el = $("#aviso");
  el.textContent = texto;
  el.className = "aviso " + classe;
  clearTimeout(avisoTimer);
  avisoTimer = setTimeout(() => el.classList.add("oculto"), 2600);
}

/* ------------------------------------------------------ utilidades ------ */

function esc(texto) {
  return String(texto).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

const PALAVRAS = ["False", "None", "True", "and", "as", "assert", "async", "await",
  "break", "class", "continue", "def", "del", "elif", "else", "except", "finally",
  "for", "from", "global", "if", "import", "in", "is", "lambda", "match", "case",
  "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with", "yield"];

const EMBUTIDOS = ["abs", "all", "any", "bool", "bytes", "callable", "chr", "classmethod",
  "dict", "dir", "divmod", "enumerate", "filter", "float", "format", "frozenset",
  "getattr", "hasattr", "hash", "id", "input", "int", "isinstance", "issubclass",
  "iter", "len", "list", "map", "max", "min", "next", "object", "open", "ord", "pow",
  "print", "property", "range", "repr", "reversed", "round", "set", "setattr",
  "sorted", "staticmethod", "str", "sum", "super", "tuple", "type", "vars", "zip"];

const RE_REALCE = new RegExp([
  "(#[^\\n]*)",
  "([rbfuRBFU]{0,2}(?:\"\"\"[\\s\\S]*?\"\"\"|'''[\\s\\S]*?'''|\"(?:\\\\.|[^\"\\\\\\n])*\"|'(?:\\\\.|[^'\\\\\\n])*'))",
  "(@[A-Za-z_][\\w.]*)",
  "\\b(" + PALAVRAS.join("|") + ")\\b",
  "\\b(self|cls)\\b",
  "\\b(" + EMBUTIDOS.join("|") + ")\\b",
  "\\b(\\d+\\.?\\d*)\\b",
  "\\b([A-Za-z_]\\w*)(?=\\s*\\()",
].join("|"), "g");

function realce(codigo) {
  return esc(codigo).replace(RE_REALCE, (bruto, com, str, dec, kw, eu, bi, num, fun) => {
    if (com) return `<span class="tk-com">${com}</span>`;
    if (str) return `<span class="tk-str">${str}</span>`;
    if (dec) return `<span class="tk-dec">${dec}</span>`;
    if (kw) return `<span class="tk-kw">${kw}</span>`;
    if (eu) return `<span class="tk-bi">${eu}</span>`;
    if (bi) return `<span class="tk-bi">${bi}</span>`;
    if (num) return `<span class="tk-num">${num}</span>`;
    if (fun) return `<span class="tk-fun">${fun}</span>`;
    return bruto;
  });
}

function blocoCodigo(codigo) {
  return `<pre class="codigo"><code>${realce(codigo)}</code></pre>`;
}

/** Converte `crase` em <code> e escapa o resto. */
function prosa(texto) {
  return esc(texto).replace(/`([^`\n]+)`/g, (m, p) => `<code>${p}</code>`);
}

/* -------------------------------------------------------- lateral ------- */

function desenharLateral() {
  const lateral = $("#lateral");
  lateral.innerHTML = "";
  let nivelAtual = null;

  estado.painel.dias.forEach((d) => {
    if (d.nivel !== nivelAtual) {
      nivelAtual = d.nivel;
      const h = document.createElement("div");
      h.className = "grupo-nivel";
      h.textContent = d.nivel;
      lateral.appendChild(h);
    }
    const b = document.createElement("button");
    const completo = d.lido && d.exercicios_ok === d.exercicios;
    b.className = "item-dia" + (completo ? " feito" : "") +
                  (estado.dia && estado.dia.numero === d.numero ? " ativo" : "");
    b.innerHTML = `<span class="num">${completo ? "✓" : d.numero}</span>
                   <span class="nome">${esc(d.titulo)}</span>
                   <span class="selo">${d.exercicios_ok}/${d.exercicios}</span>`;
    b.onclick = () => abrirDia(d.numero);
    lateral.appendChild(b);
  });
}

function atualizarMedidores() {
  const p = estado.painel;
  const pctAulas = Math.round((p.dias_lidos / p.total_dias) * 100);
  const pctEx = Math.round((p.exercicios_ok / p.total_exercicios) * 100);
  $("#barra-aulas").style.width = pctAulas + "%";
  $("#barra-ex").style.width = pctEx + "%";
  $("#txt-aulas").textContent = `${p.dias_lidos}/${p.total_dias}`;
  $("#txt-ex").textContent = `${p.exercicios_ok}/${p.total_exercicios}`;
  $("#sequencia").textContent = `🔥 ${p.sequencia}`;
}

async function recarregarPainel() {
  estado.painel = await api("/api/painel");
  atualizarMedidores();
  desenharLateral();
  atualizarBotaoCertificado();
}

/* ------------------------------------------------ certificado ---------- */

function atualizarBotaoCertificado() {
  const p = estado.painel;
  const btn = $("#btn-certificado");
  if (!btn) return;

  const pctEx = Math.round((p.exercicios_ok / p.total_exercicios) * 100);
  const exOk = p.exercicios_ok === p.total_exercicios;

  if (exOk) {
    btn.className = "btn-certificado btn-cert-ok";
    btn.innerHTML = "Emitir Certificado";
    btn.title = "Todos os exercicios concluidos! Clique para emitir.";
    btn.onclick = abrirModalCertificado;
  } else {
    btn.className = "btn-certificado btn-cert-bloqueado";
    btn.innerHTML = "Certificado  <span class=\"cert-pct\">" + pctEx + "%</span>";
    btn.title = p.exercicios_ok + "/" + p.total_exercicios + " exercicios. Conclua todos para liberar.";
    btn.onclick = () => {
      const overlay = document.createElement("div");
      overlay.id = "modal-cert-overlay";
      overlay.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,0.55);display:flex;align-items:center;justify-content:center;z-index:9999;";
      overlay.innerHTML =
        "<div style=\"background:var(--fundo,#1e1e2e);color:var(--texto,#cdd6f4);border:1px solid #45475a;border-radius:10px;padding:2rem;width:min(360px,90vw);font-family:sans-serif;position:relative;\">" +
          "<button onclick=\"this.closest('#modal-cert-overlay').remove()\" style=\"position:absolute;top:1rem;right:1rem;background:none;border:none;color:#6c7086;font-size:1.4rem;cursor:pointer;\">&times;</button>" +
          "<h2 style=\"font-size:1rem;margin-bottom:1rem;\">Certificado ainda bloqueado</h2>" +
          "<div style=\"background:#313244;border-radius:8px;padding:1rem;font-size:0.82rem;line-height:1.8;\">" +
            "<div style=\"display:flex;justify-content:space-between;margin-bottom:0.4rem;\">" +
              "<span style=\"color:#a6adc8;\">Exercicios</span>" +
              "<span style=\"color:#fab387;font-weight:600;\">" + p.exercicios_ok + "/" + p.total_exercicios + "</span>" +
            "</div>" +
            "<div style=\"background:#1e1e2e;border-radius:4px;height:6px;margin-bottom:1rem;overflow:hidden;\">" +
              "<div style=\"height:100%;width:" + pctEx + "%;background:#fab387;border-radius:4px;\"></div>" +
            "</div>" +
            "<p style=\"color:#6c7086;font-size:0.78rem;text-align:center;\">Conclua todos os exercicios e tenha media >= 75% nos quizzes para liberar o certificado.</p>" +
          "</div>" +
        "</div>";
      overlay.onclick = (e) => { if (e.target === overlay) overlay.remove(); };
      document.body.appendChild(overlay);
    };
  }
}

function abrirModalCertificado() {
  const overlay = document.createElement("div");
  overlay.id = "modal-cert-overlay";
  overlay.style.cssText = `
    position:fixed;inset:0;background:rgba(0,0,0,0.55);
    display:flex;align-items:center;justify-content:center;z-index:9999;`;

  overlay.innerHTML = `
    <div id="modal-cert" style="
      background:var(--fundo,#1e1e2e);color:var(--texto,#cdd6f4);
      border:1px solid #45475a;border-radius:10px;padding:2rem;
      width:min(420px,90vw);font-family:sans-serif;position:relative;">
      <button id="modal-fechar" style="
        position:absolute;top:1rem;right:1rem;background:none;border:none;
        color:#6c7086;font-size:1.4rem;cursor:pointer;line-height:1;">&times;</button>
      <h2 style="font-size:1.1rem;margin-bottom:0.4rem;">
        Emitir Certificado
      </h2>
      <p style="font-size:0.8rem;color:#6c7086;margin-bottom:1.5rem;">
        Verificando sua elegibilidade...
      </p>
      <div id="modal-corpo">
        <div id="msg-elegibilidade" style="margin-bottom:1.2rem;"></div>
      </div>
    </div>`;

  document.body.appendChild(overlay);

  overlay.querySelector("#modal-fechar").onclick = () => overlay.remove();
  overlay.onclick = (e) => { if (e.target === overlay) overlay.remove(); };

  // Verifica elegibilidade primeiro
  api("/api/elegibilidade", { corpo: {} }).then((r) => {
    const corpo = overlay.querySelector("#modal-corpo");
    const msgEl = overlay.querySelector("#msg-elegibilidade");

    if (!r.elegivel) {
      // Mostra o que falta
      let html = `<div style="background:#313244;border-radius:6px;padding:1rem;margin-bottom:1rem;">
        <p style="font-size:0.85rem;font-weight:600;color:#f38ba8;margin-bottom:0.6rem;">
          Ainda nao e possivel emitir o certificado:
        </p>
        <ul style="font-size:0.8rem;color:#cba6f7;padding-left:1.2rem;line-height:1.9;">`;
      r.pendencias.forEach((p) => { html += `<li>${esc(p)}</li>`; });
      html += `</ul></div>`;

      if (r.exercicios_faltando && r.exercicios_faltando.length) {
        html += `<p style="font-size:0.75rem;color:#6c7086;margin-bottom:0.4rem;">
          Exercicios pendentes (${r.exercicios_faltando.length}):
        </p>
        <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:1rem;">`;
        r.exercicios_faltando.forEach((id) => {
          html += `<span style="font-size:0.7rem;background:#1e1e2e;border:1px solid #45475a;
            border-radius:4px;padding:2px 6px;font-family:monospace;color:#fab387;">${esc(id)}</span>`;
        });
        html += `</div>`;
      }

      html += `<p style="font-size:0.75rem;color:#a6adc8;text-align:center;">
        Media atual dos quizzes: <strong style="color:#a6e3a1;">${r.media_quiz}%</strong>
        &nbsp;(minimo: 75%)
      </p>`;

      msgEl.innerHTML = html;
      corpo.querySelector("#modal-fechar") && null;

      // Troca o texto do subtitulo
      overlay.querySelector("p").textContent = "Veja o que ainda precisa ser concluido:";
      return;
    }

    // Elegivel: mostra formulario
    overlay.querySelector("p").textContent =
      "Preencha seus dados para gerar o certificado.";
    msgEl.innerHTML = `
      <div style="background:#313244;border-radius:6px;padding:1rem;margin-bottom:1rem;">
        <p style="font-size:0.8rem;color:#a6e3a1;margin-bottom:0.8rem;">
          Parabens! Todos os requisitos foram cumpridos.
          Media dos quizzes: <strong>${r.media_quiz}%</strong>
        </p>
        <label style="display:block;margin-bottom:0.8rem;">
          <span style="font-size:0.8rem;color:#cdd6f4;display:block;margin-bottom:0.3rem;">
            Nome completo
          </span>
          <input id="cert-nome" type="text" placeholder="Ex: Maria da Silva Oliveira"
            style="width:100%;padding:0.5rem 0.7rem;background:#1e1e2e;
            border:1px solid #45475a;border-radius:6px;color:#cdd6f4;
            font-size:0.85rem;outline:none;">
        </label>
        <label style="display:block;margin-bottom:1rem;">
          <span style="font-size:0.8rem;color:#cdd6f4;display:block;margin-bottom:0.3rem;">
            CPF (somente numeros ou com pontos/traco)
          </span>
          <input id="cert-cpf" type="text" placeholder="Ex: 123.456.789-00"
            style="width:100%;padding:0.5rem 0.7rem;background:#1e1e2e;
            border:1px solid #45475a;border-radius:6px;color:#cdd6f4;
            font-size:0.85rem;outline:none;">
        </label>
        <button id="btn-gerar-cert" style="
          width:100%;padding:0.6rem;background:#cba6f7;color:#1e1e2e;
          border:none;border-radius:6px;font-size:0.9rem;font-weight:600;
          cursor:pointer;">
          Gerar Certificado
        </button>
        <p id="cert-erro" style="color:#f38ba8;font-size:0.75rem;margin-top:0.5rem;display:none;"></p>
      </div>`;

    const btnGerar = overlay.querySelector("#btn-gerar-cert");
    btnGerar.onclick = async () => {
      const nome = overlay.querySelector("#cert-nome").value.trim();
      const cpf = overlay.querySelector("#cert-cpf").value.trim();
      const erroEl = overlay.querySelector("#cert-erro");
      erroEl.style.display = "none";

      if (!nome || nome.split(" ").filter(Boolean).length < 2) {
        erroEl.textContent = "Informe o nome completo (nome e sobrenome).";
        erroEl.style.display = "block";
        return;
      }
      if (!cpf || cpf.replace(/\D/g, "").length !== 11) {
        erroEl.textContent = "CPF invalido. Informe os 11 digitos.";
        erroEl.style.display = "block";
        return;
      }

      btnGerar.textContent = "Gerando...";
      btnGerar.disabled = true;
      try {
        const resp = await api("/api/certificado", { corpo: { nome, cpf } });
        if (resp.erro) throw new Error(resp.erro);
        const w = window.open("", "_blank");
        w.document.open();
        w.document.write(resp.html);
        w.document.close();
        overlay.remove();
      } catch (err) {
        erroEl.textContent = err.message || "Erro ao gerar certificado.";
        erroEl.style.display = "block";
        btnGerar.textContent = "Gerar Certificado";
        btnGerar.disabled = false;
      }
    };
  }).catch(() => {
    overlay.querySelector("#msg-elegibilidade").textContent =
      "Erro ao verificar elegibilidade. Tente novamente.";
  });
}

/* ------------------------------------------------------------ dia ------- */

let pedidoAtual = 0;

async function abrirDia(numero, aba = "teoria") {
  await descarregarEditor();
  const meuPedido = ++pedidoAtual;
  const dia = await api("/api/dia?n=" + numero);
  if (meuPedido !== pedidoAtual) return;   // o aluno já clicou em outro dia
  estado.dia = dia;
  estado.aba = aba;
  estado.exercicio = 0;
  estado.respostas = new Array(estado.dia.quiz.length).fill(null);
  desenharLateral();
  desenharDia();
  $("#principal").scrollTop = 0;
  atualizarIndicadorNotas();
  // Se o painel de notas estiver aberto e no escopo "dia", recarrega o conteúdo
  const painelNotas = $("#painel-notas");
  if (painelNotas && !painelNotas.classList.contains("oculto") && estado.notas.escopo === "dia") {
    carregarNota();
  }
}

function desenharDia() {
  const d = estado.dia;
  const abas = [
    ["teoria", "Teoria", d.lido ? "✓" : ""],
    ["exemplos", `Exemplos (${d.exemplos.length})`, ""],
    ["exercicios", `Exercícios (${d.exercicios.filter((e) => e.resolvido).length}/${d.exercicios.length})`,
      d.exercicios.every((e) => e.resolvido) ? "✓" : ""],
    ["quiz", "Quiz", d.nota_quiz ? "✓" : ""],
    ["projeto", "Projeto", ""],
  ];

  $("#principal").innerHTML = `
    <div class="cabecalho-dia">
      <div class="trilha">Dia ${d.numero} de 30</div>
      <h2>${esc(d.titulo)}</h2>
      <div class="etiquetas">
        <span class="etiqueta ${d.nivel.toLowerCase().replace(/[áâã]/g, "a")}">${esc(d.nivel)}</span>
        <span class="etiqueta">⏱ ${esc(d.duracao)}</span>
        <span class="etiqueta">${d.exercicios.length} exercícios</span>
      </div>
    </div>
    <div class="abas">
      ${abas.map(([id, rotulo, pino]) => `
        <button class="aba ${estado.aba === id ? "ativa" : ""}" data-aba="${id}">
          ${rotulo}${pino ? `<span class="pino">${pino}</span>` : ""}
        </button>`).join("")}
    </div>
    <div class="painel" id="painel-aba"></div>`;

  document.querySelectorAll(".aba").forEach((b) => {
    b.onclick = async () => {
      await descarregarEditor();
      estado.aba = b.dataset.aba;
      desenharDia();
    };
  });

  ({
    teoria: painelTeoria,
    exemplos: painelExemplos,
    exercicios: painelExercicios,
    quiz: painelQuiz,
    projeto: painelProjeto,
  })[estado.aba]();
}

/* --------------------------------------------------------- teoria ------- */

function painelTeoria() {
  const d = estado.dia;
  const corpo = d.teoria.map((b) => {
    if (b.tipo === "titulo") return `<h3>${esc(b.conteudo)}</h3>`;
    if (b.tipo === "codigo") return blocoCodigo(b.conteudo);
    return `<p>${prosa(b.conteudo)}</p>`;
  }).join("");

  $("#painel-aba").innerHTML = `
    <div class="objetivos">
      <h3>Ao final deste dia você será capaz de</h3>
      <ul>${d.objetivos.map((o) => `<li>${prosa(o)}</li>`).join("")}</ul>
    </div>
    <div class="teoria">${corpo}</div>
    <div class="rodape-dia">
      ${d.lido
        ? `<span class="aula-lida-label">✓ Aula concluída</span>
           <button class="botao botao-desmarcar" id="btn-desmarcar">Desmarcar</button>`
        : `<button class="botao principal" id="btn-lido">Marcar aula como lida</button>`}
      <button class="botao" id="btn-para-exercicios">Ir para os exercícios →</button>
    </div>`;

  if (d.lido) {
    $("#btn-desmarcar").onclick = async () => {
      await api("/api/desmarcar_lido", { corpo: { dia: d.numero } });
      estado.dia.lido = false;
      await recarregarPainel();
      desenharDia();
      avisar("Aula desmarcada", "");
    };
  } else {
    $("#btn-lido").onclick = async () => {
      await api("/api/lido", { corpo: { dia: d.numero } });
      estado.dia.lido = true;
      await recarregarPainel();
      desenharDia();
      avisar("Aula marcada como lida", "ok");
    };
  }
  $("#btn-para-exercicios").onclick = () => { estado.aba = "exercicios"; desenharDia(); };
}

function painelExemplos() {
  $("#painel-aba").innerHTML = estado.dia.exemplos.map((x) => `
    <div class="exemplo">
      <h4>${esc(x.titulo)}</h4>
      ${blocoCodigo(x.codigo)}
      ${x.explicacao ? `<p class="prosa">${prosa(x.explicacao)}</p>` : ""}
    </div>`).join("");
}

function painelProjeto() {
  const d = estado.dia;
  $("#painel-aba").innerHTML = `
    <h3>Projeto do dia</h3>
    <div class="projeto-texto">${prosa(d.projeto)}</div>
    <p class="prosa" style="color:var(--texto-apagado);font-size:13.5px;margin-top:14px">
      Este projeto não tem correção automática — é seu espaço para errar sozinho.
      Crie um arquivo em <code>${esc(estado.painel.pasta)}</code> e mande ver.
    </p>
    ${d.leitura.length ? `<div class="leitura"><h3>Para se aprofundar</h3>
      <ul>${d.leitura.map((l) => `<li>${prosa(l)}</li>`).join("")}</ul></div>` : ""}`;
}

/* ----------------------------------------------------- exercícios ------- */

function painelExercicios() {
  const exs = estado.dia.exercicios;
  const ex = exs[estado.exercicio];

  $("#painel-aba").innerHTML = `
    <div class="pilulas">
      ${exs.map((e, i) => `
        <button class="pilula ${i === estado.exercicio ? "ativa" : ""} ${e.resolvido ? "feita" : ""}"
                data-i="${i}">${e.resolvido ? "✓ " : ""}${e.id} · ${e.nivel}</button>`).join("")}
    </div>

    <div class="enunciado">${prosa(ex.enunciado)}</div>

    <div class="testes-lista">
      ${ex.testes.map((t) => `<div class="linha"><span>${esc(t.expr)}</span>
        <span class="seta">→</span><span class="esperado">${esc(t.esperado)}</span></div>`).join("")}
    </div>

    <div class="editor-caixa">
      <div class="editor-topo">
        <span>${esc(ex.arquivo)}</span>
        <span style="margin-left:auto" id="estado-salvo">salvo</span>
      </div>
      <div class="editor-area">
        <div class="numeros" id="numeros"></div>
        <pre id="realce" aria-hidden="true"><code></code></pre>
        <textarea id="editor" spellcheck="false" autocapitalize="off"
                  autocorrect="off" wrap="off"></textarea>
      </div>
    </div>

    <div class="ferramentas">
      <button class="botao principal" id="btn-testar">▶ Testar solução</button>
      <span class="atalho">Ctrl+Enter</span>
      <button class="botao" id="btn-dica">💡 Dica</button>
      <button class="botao" id="btn-recriar">↺ Recomeçar do zero</button>
      <span class="atalho" style="margin-left:auto">Ctrl+S salva</span>
    </div>

    <div class="saida" id="saida"></div>`;

  document.querySelectorAll(".pilula").forEach((b) => {
    b.onclick = async () => {
      await descarregarEditor();
      estado.exercicio = Number(b.dataset.i);
      painelExercicios();
    };
  });

  prepararEditor(ex.codigo);
  $("#btn-testar").onclick = testar;
  $("#btn-recriar").onclick = recriar;
  $("#btn-dica").onclick = () => {
    if ($("#dica-atual")) { $("#dica-atual").remove(); return; }
    const div = document.createElement("div");
    div.className = "dica-caixa";
    div.id = "dica-atual";
    div.innerHTML = "💡 " + prosa(ex.dica || "Sem dica para este exercício.");
    $("#saida").before(div);
  };
}

let salvarTimer = null;

/** Grava o que estiver pendente antes de o editor sumir da tela. */
async function descarregarEditor() {
  clearTimeout(salvarTimer);
  salvarTimer = null;
  if ($("#editor") && estado.aba === "exercicios") await salvar();
}

function prepararEditor(codigo) {
  const editor = $("#editor");
  const pre = $("#realce").firstElementChild;
  const numeros = $("#numeros");

  function pintar() {
    let texto = editor.value;
    if (texto.endsWith("\n")) texto += " ";
    pre.innerHTML = realce(texto);
    const linhas = editor.value.split("\n").length;
    numeros.innerHTML = Array.from({ length: linhas }, (_, i) => i + 1).join("<br>");
  }

  function sincronizar() {
    pre.parentElement.scrollTop = editor.scrollTop;
    pre.parentElement.scrollLeft = editor.scrollLeft;
    numeros.scrollTop = editor.scrollTop;
  }

  editor.value = codigo;
  pintar();

  editor.addEventListener("input", () => {
    pintar();
    $("#estado-salvo").textContent = "editando…";
    clearTimeout(salvarTimer);
    salvarTimer = setTimeout(salvar, 1200);
  });
  editor.addEventListener("scroll", sincronizar);

  editor.addEventListener("keydown", (ev) => {
    const ini = editor.selectionStart;
    const fim = editor.selectionEnd;

    if (ev.key === "Tab") {
      ev.preventDefault();
      if (ev.shiftKey) {
        const inicioLinha = editor.value.lastIndexOf("\n", ini - 1) + 1;
        if (editor.value.slice(inicioLinha, inicioLinha + 4) === "    ") {
          editor.value = editor.value.slice(0, inicioLinha) +
                         editor.value.slice(inicioLinha + 4);
          editor.selectionStart = editor.selectionEnd = Math.max(inicioLinha, ini - 4);
        }
      } else {
        editor.value = editor.value.slice(0, ini) + "    " + editor.value.slice(fim);
        editor.selectionStart = editor.selectionEnd = ini + 4;
      }
      editor.dispatchEvent(new Event("input"));
      return;
    }

    if (ev.key === "Enter") {
      const inicioLinha = editor.value.lastIndexOf("\n", ini - 1) + 1;
      const linha = editor.value.slice(inicioLinha, ini);
      const recuo = (linha.match(/^[ \t]*/) || [""])[0];
      const extra = linha.trimEnd().endsWith(":") ? "    " : "";
      ev.preventDefault();
      const insercao = "\n" + recuo + extra;
      editor.value = editor.value.slice(0, ini) + insercao + editor.value.slice(fim);
      editor.selectionStart = editor.selectionEnd = ini + insercao.length;
      editor.dispatchEvent(new Event("input"));
      return;
    }

    if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") { ev.preventDefault(); testar(); }
    if ((ev.ctrlKey || ev.metaKey) && ev.key.toLowerCase() === "s") { ev.preventDefault(); salvar(); }
  });

  editor.focus();
}

function exercicioAtual() {
  return estado.dia.exercicios[estado.exercicio];
}

async function salvar() {
  const campo = $("#editor");
  if (!campo || estado.aba !== "exercicios") return;   // o aluno já trocou de aba
  const ex = exercicioAtual();
  const codigo = campo.value;
  ex.codigo = codigo;
  await api("/api/salvar", { corpo: { id: ex.id, codigo } });
  const marca = $("#estado-salvo");
  if (marca) marca.textContent = "salvo";
}

async function recriar() {
  const ex = exercicioAtual();
  if (!confirm("Isso apaga o que você escreveu neste exercício. Continuar?")) return;
  clearTimeout(salvarTimer);            // não deixa o autosave ressuscitar o código antigo
  const r = await api("/api/recriar", { corpo: { id: ex.id } });
  ex.codigo = r.codigo;
  painelExercicios();
  avisar("Arquivo recriado", "ok");
}

async function testar() {
  const ex = exercicioAtual();
  const botao = $("#btn-testar");
  const saida = $("#saida");
  botao.disabled = true;
  botao.textContent = "⏳ Rodando…";
  saida.innerHTML = "";

  try {
    const r = await api("/api/testar", { corpo: { id: ex.id, codigo: $("#editor").value } });
    $("#estado-salvo").textContent = "salvo";
    saida.innerHTML = relatorio(r);
    if (r.passou) {
      ex.resolvido = true;
      await recarregarPainel();
      avisar("Exercício concluído! 🎉", "ok");
      painelExercicios();
      $("#saida").innerHTML = relatorio(r);
    }
  } catch (erro) {
    saida.innerHTML = `<div class="bloco-saida falha">${esc(erro.message)}</div>`;
  } finally {
    if ($("#btn-testar")) {
      $("#btn-testar").disabled = false;
      $("#btn-testar").textContent = "▶ Testar solução";
    }
  }
}

function relatorio(r) {
  if (r.timeout) {
    return `<div class="bloco-saida falha">
      <p class="res-titulo falha">Tempo esgotado (12 s)</p>
      <div class="detalhe">Provavelmente há um laço que nunca termina.
      Confira a condição do <code>while</code> e se a variável de controle muda.</div></div>`;
  }
  if (r.erro_carga) {
    return `<div class="bloco-saida falha">
      <p class="res-titulo falha">O arquivo nem chegou a rodar</p>
      <pre class="traceback">${esc(r.erro_carga.trim())}</pre></div>`;
  }

  const linhas = r.testes.map((t) => {
    if (t.passou) {
      return `<div class="res-linha"><span class="marca-ok">✓</span>
        <span>${esc(t.expr)} <span class="detalhe">→</span> ${esc(t.esperado)}</span></div>`;
    }
    const motivo = t.erro
      ? `levantou <b>${esc(t.erro)}</b>`
      : `devolveu <b>${esc(t.obtido)}</b>, esperado <b>${esc(t.esperado)}</b>`;
    return `<div class="res-linha"><span class="marca-x">✗</span>
      <span>${esc(t.expr)} <span class="detalhe">${motivo}</span></span></div>`;
  }).join("");

  const ok = r.passou;
  const total = r.testes.length;
  const acertos = r.testes.filter((t) => t.passou).length;

  return `<div class="bloco-saida ${ok ? "ok" : "falha"}">
    <p class="res-titulo ${ok ? "ok" : "falha"}">
      ${ok ? "✓ Todos os testes passaram. Exercício concluído!"
           : `${acertos} de ${total} testes passaram`}</p>
    ${linhas}
    ${r.saida_aluno ? `<div class="stdout-aluno"><b>Sua saída (print):</b>\n${esc(r.saida_aluno)}</div>` : ""}
    ${!ok && r.dica ? `<div class="dica-caixa">💡 ${prosa(r.dica)}</div>` : ""}
  </div>`;
}

/* ------------------------------------------------------------ quiz ------ */

function painelQuiz() {
  const d = estado.dia;
  if (!d.quiz.length) {
    $("#painel-aba").innerHTML = "<p>Este dia não tem quiz.</p>";
    return;
  }
  $("#painel-aba").innerHTML = `
    ${d.quiz.map((q, i) => `
      <div class="questao" data-q="${i}">
        <h4>${i + 1}. ${prosa(q.pergunta)}</h4>
        ${q.alternativas.map((alt, j) => `
          <label class="alternativa" data-alt="${j}">
            <input type="radio" name="q${i}" value="${j}">
            <span><code>${esc(alt)}</code></span>
          </label>`).join("")}
        <div class="explicacao oculto"></div>
      </div>`).join("")}
    <button class="botao principal" id="btn-corrigir">Corrigir quiz</button>
    <div id="nota"></div>`;

  document.querySelectorAll(".questao input").forEach((inp) => {
    inp.onchange = (ev) => {
      const q = Number(ev.target.closest(".questao").dataset.q);
      estado.respostas[q] = Number(ev.target.value);
    };
  });

  $("#btn-corrigir").onclick = async () => {
    const r = await api("/api/quiz", { corpo: { dia: d.numero, respostas: estado.respostas } });
    r.correcao.forEach((c, i) => {
      const questao = document.querySelector(`.questao[data-q="${i}"]`);
      questao.querySelectorAll(".alternativa").forEach((label) => {
        const j = Number(label.dataset.alt);
        if (j === c.correta) label.classList.add("certa");
        else if (j === estado.respostas[i]) label.classList.add("errada");
      });
      const exp = questao.querySelector(".explicacao");
      exp.textContent = c.explicacao;
      exp.classList.remove("oculto");
    });
    const pct = Math.round((r.acertos / r.total) * 100);
    $("#nota").innerHTML = `<p class="nota-quiz">Resultado: <b>${r.acertos}/${r.total}</b> (${pct}%) —
      ${pct === 100 ? "conteúdo dominado 🎯" : pct >= 50 ? "quase lá, revise os erros acima."
        : "vale reler a teoria antes dos exercícios."}</p>`;
    estado.dia.nota_quiz = { acertos: r.acertos, total: r.total };
    await recarregarPainel();
  };
}

/* ----------------------------------------------------------- busca ------ */

let buscaTimer = null;
$("#busca").addEventListener("input", (ev) => {
  clearTimeout(buscaTimer);
  const termo = ev.target.value.trim();
  const caixa = $("#resultados-busca");
  if (termo.length < 2) { caixa.classList.add("oculto"); return; }
  buscaTimer = setTimeout(async () => {
    const r = await api("/api/buscar?q=" + encodeURIComponent(termo));
    caixa.classList.remove("oculto");
    if (!r.resultados.length) {
      caixa.innerHTML = `<div class="vazio">Nada encontrado para “${esc(termo)}”.</div>`;
      return;
    }
    caixa.innerHTML = r.resultados.map((x) => `
      <button data-n="${x.numero}">
        <b>Dia ${x.numero} — ${esc(x.titulo)}</b>
        <div class="trecho">${esc(x.trecho)}</div>
      </button>`).join("");
    caixa.querySelectorAll("button").forEach((b) => {
      b.onclick = () => {
        caixa.classList.add("oculto");
        $("#busca").value = "";
        abrirDia(Number(b.dataset.n));
      };
    });
  }, 250);
});

document.addEventListener("click", (ev) => {
  if (!ev.target.closest(".busca")) $("#resultados-busca").classList.add("oculto");
});

/* -------------------------------------------------------- anotações ----- */

function inicializarAnotacoes() {
  const btn = document.createElement("button");
  btn.id = "btn-notas-flutuante";
  btn.className = "btn-notas-flutuante";
  btn.title = "Minhas anotações";
  btn.innerHTML = "📝";
  document.body.appendChild(btn);

  const painel = document.createElement("div");
  painel.id = "painel-notas";
  painel.className = "painel-notas oculto";
  painel.innerHTML = `
    <div class="notas-cabecalho" id="notas-arraste">
      <div class="notas-abas">
        <button class="notas-aba ativa" data-escopo="geral">Geral</button>
        <button class="notas-aba" data-escopo="dia">Este dia</button>
      </div>
      <button class="notas-fechar" id="notas-fechar" title="Fechar">✕</button>
    </div>
    <textarea id="notas-texto" class="notas-texto"
      placeholder="Escreva aqui suas anotações..."></textarea>
    <div class="notas-rodape">
      <span id="notas-status" class="notas-status"></span>
    </div>
    <div class="notas-redimensionar" id="notas-resize"></div>`;
  document.body.appendChild(painel);

  btn.onclick = () => {
    const oculto = painel.classList.toggle("oculto");
    if (!oculto) carregarNota();
  };
  $("#notas-fechar").onclick = () => painel.classList.add("oculto");

  painel.querySelectorAll(".notas-aba").forEach((aba) => {
    aba.onclick = () => {
      painel.querySelectorAll(".notas-aba").forEach((a) => a.classList.remove("ativa"));
      aba.classList.add("ativa");
      estado.notas.escopo = aba.dataset.escopo;
      carregarNota();
    };
  });

  const textarea = $("#notas-texto");
  textarea.addEventListener("input", () => {
    const statusEl = $("#notas-status");
    statusEl.textContent = "digitando…";
    statusEl.className = "notas-status";
    clearTimeout(estado.notas.timer);
    estado.notas.timer = setTimeout(() => salvarNotaAtual(textarea.value), 700);
  });

  tornarArrastavel(painel, $("#notas-arraste"));
  tornarRedimensionavel(painel, $("#notas-resize"));
}

function chaveNotaAtual() {
  if (estado.notas.escopo === "geral") return "geral";
  return String(estado.dia ? estado.dia.numero : "geral");
}

function carregarNota() {
  const chave = chaveNotaAtual();
  const notas = (estado.painel && estado.painel.notas) || {};
  const textarea = $("#notas-texto");
  textarea.value = notas[chave] || "";
  const statusEl = $("#notas-status");
  statusEl.textContent = "";

  // Ajusta o rótulo da aba "Este dia" com o número do dia atual
  const abaDia = $('.notas-aba[data-escopo="dia"]');
  if (abaDia && estado.dia) abaDia.textContent = `Dia ${estado.dia.numero}`;

  atualizarIndicadorNotas();
}

async function salvarNotaAtual(texto) {
  const chave = chaveNotaAtual();
  const statusEl = $("#notas-status");
  try {
    await api("/api/nota", { corpo: { chave, texto } });
    if (!estado.painel.notas) estado.painel.notas = {};
    if (texto.trim()) estado.painel.notas[chave] = texto;
    else delete estado.painel.notas[chave];
    statusEl.textContent = "salvo ✓";
    atualizarIndicadorNotas();
  } catch {
    statusEl.textContent = "erro ao salvar";
  }
}

function atualizarIndicadorNotas() {
  const btn = $("#btn-notas-flutuante");
  if (!btn) return;
  const notas = (estado.painel && estado.painel.notas) || {};
  const chaveDia = String(estado.dia ? estado.dia.numero : "");
  const temAlgo = !!notas["geral"] || !!notas[chaveDia];
  btn.classList.toggle("tem-nota", temAlgo);
}

function tornarArrastavel(painel, alca) {
  let ativo = false, offX = 0, offY = 0;
  alca.addEventListener("mousedown", (e) => {
    if (e.target.closest("button")) return;
    ativo = true;
    const r = painel.getBoundingClientRect();
    offX = e.clientX - r.left;
    offY = e.clientY - r.top;
    painel.style.right = "auto";
    painel.style.bottom = "auto";
  });
  document.addEventListener("mousemove", (e) => {
    if (!ativo) return;
    painel.style.left = `${e.clientX - offX}px`;
    painel.style.top = `${e.clientY - offY}px`;
  });
  document.addEventListener("mouseup", () => { ativo = false; });
}

function tornarRedimensionavel(painel, alca) {
  let ativo = false, w0 = 0, h0 = 0, x0 = 0, y0 = 0;
  alca.addEventListener("mousedown", (e) => {
    ativo = true;
    const r = painel.getBoundingClientRect();
    w0 = r.width; h0 = r.height; x0 = e.clientX; y0 = e.clientY;
    e.preventDefault();
  });
  document.addEventListener("mousemove", (e) => {
    if (!ativo) return;
    painel.style.width = `${Math.max(260, w0 + (e.clientX - x0))}px`;
    painel.style.height = `${Math.max(200, h0 + (e.clientY - y0))}px`;
  });
  document.addEventListener("mouseup", () => { ativo = false; });
}

/* ---------------------------------------------------------- início ------ */

(async function iniciar() {
  try {
    inicializarAnotacoes();
    await recarregarPainel();
    await abrirDia(estado.painel.proximo);
  } catch (erro) {
    $("#principal").innerHTML =
      `<div class="painel"><h2>Não consegui carregar o curso</h2>
       <p>${esc(erro.message)}</p>
       <p>Feche esta aba e abra novamente o endereço mostrado no terminal.</p></div>`;
  }
})();
