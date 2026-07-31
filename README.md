# Curso de Python em 30 Dias

**Um curso completo de Python que roda como programa.** Você lê a teoria, escreve o código e recebe a correção sem sair da mesma tela — no navegador ou no terminal.

Material 100% em português, do `print("olá")` até asyncio e empacotamento. Sem dependências: se você tem Python, você tem o curso.

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![Sem dependências](https://img.shields.io/badge/depend%C3%AAncias-nenhuma-brightgreen)
![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-lightgrey)
![Linux](https://img.shields.io/badge/testado%20em-Linux-orange)

<!-- Tire um print da aba de exercícios, salve como docs/tela.png e apague os marcadores de comentário desta linha:
![Interface do curso](docs/tela.png)
-->

## Por que existe

Aprender Python sozinho costuma virar um vaivém entre o vídeo, o editor, o terminal e a aba do Stack Overflow. Some-se a isso o material bom estar quase todo em inglês, e a desistência acontece por volta da terceira semana — não por falta de capacidade, mas por atrito.

Este projeto tira o atrito do caminho: um programa só, que ensina, propõe o exercício, roda o seu código e diz o que faltou.

```
▶ Testar solução

  ✗ tabuada(3)   devolveu [3], esperado [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
  ✗ tabuada(0)   devolveu [0], esperado [0]*10

  1 de 3 testes passaram
  💡 Dica: multiplique n por cada valor de range(1, 11).
```

## Começando

```bash
git clone https://github.com/SEU_USUARIO/curso-python-30-dias.git
cd curso-python-30-dias
python3 curso_web.py
```

O navegador abre sozinho. É isso — não há `pip install`, venv nem configuração.

Prefere terminal? `python3 curso.py`. Quer atalhos no PATH (`curso` e `curso-gui`)? `bash instalar.sh`.

**Requisitos:** Linux com Python 3.10 ou superior (`python3 --version`). Deve funcionar em macOS; ainda não foi testado lá.

## O que tem dentro

- **30 dias de teoria escrita**, não tópicos soltos: cada dia explica o *porquê*, com as armadilhas comuns e o jeito idiomático de fazer.
- **90 exercícios com correção automática**, em três níveis por dia.
- **60 questões de quiz** com explicação de cada resposta.
- **30 projetos diários** sem correção — o espaço para errar sozinho.
- **Editor embutido** na interface gráfica: realce de sintaxe, numeração de linhas, indentação automática, `Ctrl+Enter` para testar.
- **Progresso persistente**: dias lidos, exercícios resolvidos, notas dos quizzes, sequência de dias seguidos e revisão espaçada dos assuntos em que você foi pior.

## Duas interfaces, um curso só

| | Gráfica | Terminal |
|---|---|---|
| Abrir com | `python3 curso_web.py` | `python3 curso.py` |
| Onde roda | navegador | terminal |
| Editor | embutido | você usa o seu (nano, vim, VS Code) |
| Boa para | estudar | revisar rápido, ver progresso |

As duas compartilham o mesmo motor e o mesmo arquivo de progresso. Dá para estudar no navegador de dia e conferir o avanço pelo terminal de noite, sem perder nada.

### Interface gráfica

```bash
python3 curso_web.py                  # http://127.0.0.1:8765
python3 curso_web.py --porta 9000     # outra porta
python3 curso_web.py --sem-navegador  # não abre o navegador sozinho
```

O servidor escuta apenas em `127.0.0.1` e exige um token que aparece no terminal — ninguém na rede alcança. Por isso abra o endereço completo, com o `?t=...`. Para encerrar, `Ctrl+C`.

### Linha de comando

```bash
python3 curso.py hoje             # próximo dia não concluído
python3 curso.py dia 7            # um dia específico
python3 curso.py ex d07e2         # abre um exercício
python3 curso.py testar d07e2     # corrige sem abrir a aula
python3 curso.py quiz 7           # quiz do dia
python3 curso.py progresso        # painel de progresso
python3 curso.py buscar zip       # procura no material inteiro
python3 curso.py ementa           # lista os 30 dias
```

## O programa

**Iniciante (1–10)** — ambiente e primeiro script · variáveis e tipos · operadores · strings e f-strings · condicionais e `match` · `while` · `for`, `range`, `enumerate`, `zip` · listas e tuplas · dicionários e conjuntos · compreensões

**Intermediário (11–17)** — funções e escopo · alta ordem, lambda e recursão · módulos, venv e pip · arquivos, JSON e CSV · exceções · POO I · POO II

**Avançado (18–30)** — herança e dunders · dataclasses, Enum, ABC · iteradores e geradores · decoradores · context managers · type hints · testes e TDD · Python no Linux · regex · concorrência e GIL · asyncio · desempenho · empacotamento

<details>
<summary>Ver os 30 dias um a um</summary>

| Dia | Assunto | Dia | Assunto |
|---|---|---|---|
| 1 | Ambiente e primeiro programa | 16 | POO I: classes e estado |
| 2 | Variáveis e tipos | 17 | POO II: propriedades e métodos de classe |
| 3 | Operadores | 18 | POO III: herança e dunders |
| 4 | Strings e f-strings | 19 | dataclasses, Enum, ABC |
| 5 | Condicionais e `match` | 20 | Iteradores, geradores, itertools |
| 6 | `while`, `break`, `continue` | 21 | Decoradores e functools |
| 7 | `for`, `range`, `enumerate`, `zip` | 22 | Context managers |
| 8 | Listas e tuplas | 23 | Type hints |
| 9 | Dicionários e conjuntos | 24 | Testes: unittest, pytest, TDD |
| 10 | Compreensões | 25 | Python no Linux |
| 11 | Funções e escopo | 26 | Expressões regulares |
| 12 | Alta ordem, lambda, recursão | 27 | Concorrência e o GIL |
| 13 | Módulos, venv e pip | 28 | asyncio |
| 14 | Arquivos, JSON e CSV | 29 | Desempenho e profiling |
| 15 | Erros e exceções | 30 | Projeto final e empacotamento |

</details>

### Como aproveitar (60–120 min por dia)

1. Leia a **teoria** e os **exemplos** — o programa conduz.
2. Responda o **quiz**: ele revela o que você achou que entendeu.
3. Resolva os **3 exercícios** até os testes passarem.
4. Faça o **projeto do dia** por conta própria.

Constância vence intensidade: uma hora por dia rende mais que sete horas no sábado. Se um dia parecer pesado, faça só a teoria e um exercício — voltar amanhã vale mais que parar.

## Como a correção funciona

Cada exercício declara seus testes como pares de expressão e resultado esperado, ao lado do enunciado:

```python
Exercicio(
    id="d07e1",
    enunciado="Escreva tabuada(n) que devolve a lista com n*1, n*2, ..., n*10.",
    assinatura="def tabuada(n):",
    testes=[
        ("tabuada(3)", "[3, 6, 9, 12, 15, 18, 21, 24, 27, 30]"),
        ("tabuada(0)", "[0]*10"),
    ],
    dica="Multiplique n por cada valor de range(1, 11).",
)
```

Um executor genérico carrega o arquivo que você escreveu e avalia essas expressões dentro dele — **em um subprocesso isolado, com timeout de 12 segundos**. Isso não é preciosismo: seu código pode ter um laço infinito, chamar `sys.exit()` ou imprimir coisas no meio da correção, e no mesmo processo qualquer um dos três derrubaria o curso. Isolado, o laço infinito vira uma mensagem educada e o que você imprime com `print()` é capturado e mostrado à parte.

A comparação tem alguns cuidados: `float` compara com tolerância, `bool` compara com `is` (senão `1 == True` passaria batido), e a sintaxe `"!raise ValueError"` no esperado testa se a exceção certa foi levantada.

## Estrutura do código

```
curso.py         interface de terminal
curso_web.py     interface gráfica (servidor HTTP local, só stdlib)
web/             index.html, app.css, app.js
nucleo/
├── modelos.py   Dia, Exercicio, Quiz, Exemplo (dataclasses)
├── ui.py        cores ANSI, caixas, realce de código
├── progresso.py persistência em JSON
├── avaliador.py criação e correção dos exercícios
└── _runner.py   executor isolado (subprocesso + timeout)
conteudo/
└── semana1-4.py os 30 dias
```

O motor não sabe nada sobre interface, e as interfaces não sabem corrigir exercício nenhum — foi isso que permitiu acrescentar a versão gráfica sem tocar na lógica.

O próprio código é material de estudo: a partir do dia 13 você consegue lê-lo inteiro, e ele usa dataclasses, subprocess, pathlib, JSON, context managers e type hints.

## Seus arquivos

```
~/curso_python30/
├── progresso.json          seu progresso
└── exercicios/
    └── dia01/d01e1.py      os arquivos que você edita
```

| Variável | Efeito |
|---|---|
| `CURSO_DIR` | muda a pasta dos seus arquivos |
| `CURSO_SEM_COR=1` | desliga as cores no terminal |

## Contribuindo

Correções de erro no material são muito bem-vindas — abra uma issue dizendo o dia e o trecho. Para exercícios novos, mantenha o formato de `testes` acima e confira que a correção funciona antes de abrir o PR.

## Licença

MIT. Use, modifique e ensine com ele à vontade.

---

<sub>Projeto desenvolvido com auxílio de IA (Claude), revisado e testado antes da publicação.</sub>
