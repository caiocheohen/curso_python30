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
      <button class="botao ${d.lido ? "" : "principal"}" id="btn-lido">
        ${d.lido ? "✓ Aula concluída" : "Marcar aula como lida"}
      </button>
      <button class="botao" id="btn-para-exercicios">Ir para os exercícios →</button>
    </div>`;

  $("#btn-lido").onclick = async () => {
    await api("/api/lido", { corpo: { dia: d.numero } });
    estado.dia.lido = true;
    await recarregarPainel();
    desenharDia();
    avisar("Aula marcada como lida", "ok");
  };
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

/* ---------------------------------------------------------- início ------ */

(async function iniciar() {
  try {
    await recarregarPainel();
    await abrirDia(estado.painel.proximo);
  } catch (erro) {
    $("#principal").innerHTML =
      `<div class="painel"><h2>Não consegui carregar o curso</h2>
       <p>${esc(erro.message)}</p>
       <p>Feche esta aba e abra novamente o endereço mostrado no terminal.</p></div>`;
  }
})();
