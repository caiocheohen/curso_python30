"""Semana 2 - Dias 9 a 15: estruturas de dados, funções, módulos, arquivos e erros."""

from nucleo.modelos import Dia, Exemplo, Exercicio, Quiz

DIAS = []

# ---------------------------------------------------------------- DIA 9
DIAS.append(Dia(
    numero=9,
    titulo="Dicionários e conjuntos",
    nivel="Iniciante",
    duracao="90 min",
    objetivos=[
        "Criar, acessar e percorrer dicionários com segurança, sem KeyError inesperado",
        "Usar get, setdefault, update, pop e o desempacotamento com **",
        "Aplicar conjuntos para deduplicação e para as quatro operações matemáticas de conjunto",
        "Escolher a estrutura de dados certa (lista, tupla, dict ou set) para cada problema",
        "Reconhecer por que Counter e defaultdict resolvem padrões que você reescreveria toda hora",
    ],
    teoria="""
1. Dicionário: mapeamento chave -> valor
--------------------------------------------
Um dicionário é a estrutura que você usa quando precisa buscar um valor por
um IDENTIFICADOR, em vez de por posição — o oposto de uma lista, que é
organizada por índice numérico:

    aluno = {"nome": "Ana", "nota": 9.5, "aprovado": True}
    aluno["nome"]          -> 'Ana'
    aluno["curso"]         -> KeyError: 'curso'
    aluno.get("curso")     -> None            (não levanta erro; devolve None por padrão)
    aluno.get("curso", "-") -> '-'            (você escolhe o valor padrão)

A diferença entre `aluno["curso"]` e `aluno.get("curso")` é uma decisão de
design que você toma toda vez: use colchetes quando a ausência da chave é um
BUG (você quer que o programa pare e avise); use `.get()` quando a ausência
é uma situação normal e esperada, que seu código já sabe tratar.

Chaves precisam ser HASHÁVEIS — na prática, isso significa imutáveis: `str`,
`int`, `float`, `bool` e `tuple` servem; `list`, `dict` e `set` não servem,
porque são mutáveis e não têm um hash estável ao longo do tempo (voltamos a
esse conceito no Dia 18, com `__hash__`). Desde o Python 3.7, a ordem de
inserção das chaves é preservada e faz parte da especificação da linguagem
— antes disso, a ordem era um detalhe de implementação não garantido.

2. Modificando um dicionário
---------------------------------
    aluno["nota"] = 10                 # cria a chave se não existir, ou atualiza se existir
    aluno.update({"nota": 8, "cpf": 1})  # atualiza várias chaves de uma vez
    aluno.pop("cpf")                   # remove a chave e DEVOLVE o valor removido
    aluno.pop("nada", None)            # sem KeyError: devolve None se a chave não existir
    del aluno["nota"]                  # remove sem devolver nada (KeyError se não existir)
    aluno.setdefault("faltas", 0)      # só cria a chave "faltas" se ela ainda não existir

`setdefault` é sutil na primeira leitura: ele devolve o valor da chave se ela
já existe, ou cria a chave com o valor informado E devolve esse valor — numa
única chamada. Isso o torna a base do "padrão de agrupamento" que vemos na
seção 4.

3. Percorrendo um dicionário
---------------------------------
    for chave in aluno: ...              # itera as CHAVES (comportamento padrão)
    for chave, valor in aluno.items(): ...   # itera pares (chave, valor)
    for valor in aluno.values(): ...         # itera só os valores
    "nome" in aluno                          # testa se a CHAVE existe — O(1), muito rápido

Um erro comum de quem vem de outras linguagens é escrever
`for item in aluno:` esperando os VALORES — em Python, iterar um dicionário
diretamente sempre percorre as chaves. Se você quer os dois, `.items()` é
explícito e evita essa confusão.

4. O padrão contador (e por que Counter existe)
-----------------------------------------------------
Um dos usos mais comuns de dicionário é contar ocorrências:

    contagem = {}
    for palavra in texto.split():
        contagem[palavra] = contagem.get(palavra, 0) + 1

Esse padrão aparece com tanta frequência que a biblioteca padrão já o
resolve pronto:

    from collections import Counter
    Counter(texto.split()).most_common(3)     # as 3 palavras mais frequentes

E para AGRUPAR itens por uma característica (em vez de só contar):

    from collections import defaultdict
    grupos = defaultdict(list)                 # toda chave nova já começa como []
    for palavra in palavras:
        grupos[palavra[0]].append(palavra)

`defaultdict(list)` elimina a necessidade de `.setdefault()` ou de checar
"a chave já existe?" manualmente: qualquer chave nunca vista antes já vem
com uma lista vazia pronta para usar. A regra prática é: se você está prestes
a escrever um `if chave not in dicionario:`, provavelmente existe uma
ferramenta de `collections` que já resolve isso de forma mais direta.

5. Mesclando dois dicionários
----------------------------------
    a = {"x": 1}; b = {"y": 2}
    juntos = {**a, **b}        # funciona desde Python 3.5
    juntos = a | b             # operador de união, Python 3.9+
    a |= b                     # mescla b DENTRO de a, no lugar

Em caso de chave repetida entre `a` e `b`, o valor de `b` (o operando da
direita) sempre prevalece — pense nisso como "b sobrescreve a".

6. Conjunto (set): coleção sem ordem e sem repetição
---------------------------------------------------------
    s = {1, 2, 3}
    vazio = set()              # {} sozinho cria um DICIONÁRIO vazio, não um set!
    set([1, 1, 2])             -> {1, 2}     (duplicatas somem automaticamente)

A pegadinha de `{}` ser dicionário (não conjunto) é histórica: quando os
conjuntos foram adicionados à linguagem, a sintaxe `{}` já pertencia aos
dicionários havia anos, então não havia como reaproveitá-la sem quebrar
código existente.

As quatro operações matemáticas de conjunto, direto na sintaxe:

    a | b   união                (elementos que estão em a OU em b)
    a & b   interseção           (elementos que estão em a E em b)
    a - b   diferença            (elementos que estão em a, mas NÃO em b)
    a ^ b   diferença simétrica  (elementos que estão em só um dos dois, não nos dois)
    a <= b  subconjunto           (todo elemento de a também está em b?)

Métodos úteis: `.add(x)` adiciona um elemento; `.discard(x)` remove sem
erro se não existir; `.remove(x)` remove mas levanta `KeyError` se não
existir; `.update(outro_iteravel)` adiciona vários de uma vez.

O detalhe de desempenho mais importante do dia: `x in conjunto` custa tempo
CONSTANTE (O(1)), enquanto `x in lista` custa tempo PROPORCIONAL ao tamanho
da lista (O(n)), porque precisa checar item por item. Trocar uma lista por
um conjunto quando você só precisa checar pertencimento repetidamente é uma
das otimizações mais simples e mais impactantes que existem — sem mudar
nada na lógica do programa, só na estrutura de dados escolhida.

`frozenset` é a versão IMUTÁVEL de um conjunto — por ser imutável, ela pode,
diferente do `set` comum, ser usada como chave de dicionário ou elemento de
outro conjunto.

7. Qual estrutura usar? Um guia de decisão rápido
--------------------------------------------------------
    lista (list)   a ordem importa, permite elementos repetidos, acesso por posição numérica
    tupla (tuple)   registro de tamanho fixo, imutável, pode virar chave de dicionário
    dicionário (dict)   busca por um identificador (chave), cada chave associada a um dado
    conjunto (set)  interessa só "pertence ou não", sem duplicatas, com operações de conjunto

Uma pergunta prática para decidir: "eu vou buscar isso pelo conteúdo (então
quero set/dict, que são rápidos) ou pela posição em que foi inserido (então
quero list/tuple)?"
""",
    exemplos=[
        Exemplo(
            titulo="Agrupando com setdefault",
            codigo='''palavras = ["ana", "bia", "ary", "bob", "caio"]
grupos = {}
for p in palavras:
    grupos.setdefault(p[0], []).append(p)
print(grupos)   # {'a': ['ana', 'ary'], 'b': ['bia', 'bob'], 'c': ['caio']}
''',
            explicacao="setdefault cria a lista vazia na primeira vez que "
                       "aquela letra aparece, e nas vezes seguintes apenas "
                       "devolve a lista já existente para o append.",
        ),
        Exemplo(
            titulo="Conjuntos para comparar dois cadastros",
            codigo='''antigos = {"ana", "bia", "caio"}
novos = {"bia", "caio", "davi"}
print("sairam:", antigos - novos)      # {'ana'}
print("entraram:", novos - antigos)    # {'davi'}
print("ficaram:", antigos & novos)     # {'bia', 'caio'}
''',
            explicacao="Três linhas resolvem o que exigiria dois laços "
                       "aninhados e listas auxiliares se feito com listas.",
        ),
        Exemplo(
            titulo="Counter e defaultdict na prática",
            codigo='''from collections import Counter, defaultdict

texto = "o rato roeu a roupa do rei de roma"
mais_comuns = Counter(texto.split()).most_common(2)
print(mais_comuns)          # [('o', 1), ('rato', 1)] (empate, ordem de insercao)

por_tamanho = defaultdict(list)
for palavra in texto.split():
    por_tamanho[len(palavra)].append(palavra)
print(dict(por_tamanho))
''',
            explicacao="Counter conta automaticamente; defaultdict elimina "
                       "a necessidade de checar 'a chave já existe?'.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d09e1",
            enunciado=(
                "Escreva contar_letras(texto): devolve um dicionário com a frequência de\n"
                "cada letra, ignorando espaços e diferenças de maiúsculas."
            ),
            funcao="contar_letras",
            assinatura="def contar_letras(texto):",
            testes=[
                ("contar_letras('aba')", "{'a': 2, 'b': 1}"),
                ("contar_letras('A a')", "{'a': 2}"),
                ("contar_letras('')", "{}"),
            ],
            dica="Converta para minúsculas, pule espaços e use .get(letra, 0) + 1.",
        ),
        Exercicio(
            id="d09e2",
            enunciado="Escreva inverter_dicionario(d) trocando chaves por valores.",
            funcao="inverter_dicionario",
            assinatura="def inverter_dicionario(d):",
            testes=[
                ("inverter_dicionario({'a': 1, 'b': 2})", "{1: 'a', 2: 'b'}"),
                ("inverter_dicionario({})", "{}"),
            ],
            dica="Percorra .items() e monte um novo dicionário.",
        ),
        Exercicio(
            id="d09e3",
            enunciado=(
                "Escreva comuns(a, b) devolvendo a lista ORDENADA dos elementos que\n"
                "aparecem nas duas listas, sem repetição."
            ),
            funcao="comuns",
            assinatura="def comuns(a, b):",
            testes=[
                ("comuns([1, 2, 3, 3], [3, 2, 9])", "[2, 3]"),
                ("comuns([], [1])", "[]"),
                ("comuns(['b', 'a'], ['a', 'b'])", "['a', 'b']"),
            ],
            nivel="medio",
            dica="sorted(set(a) & set(b))",
        ),
    ],
    quiz=[
        Quiz("Qual destes NÃO pode ser chave de dicionário?",
             ["'texto'", "(1, 2)", "[1, 2]", "3.14"], 2,
             "Listas são mutáveis, logo não hasháveis — não podem virar chave."),
        Quiz("O que cria um conjunto vazio?",
             ["{}", "set()", "[]", "()"], 1,
             "{} sozinho cria um dicionário vazio, por razões históricas da linguagem."),
        Quiz("Por que trocar uma lista por um set melhora a performance de 'x in colecao'?",
             ["Não melhora nada", "set usa hashing e faz a checagem em tempo constante O(1), lista percorre item a item O(n)",
              "set ordena os elementos automaticamente", "Listas não suportam o operador in"], 1,
             "A busca por pertencimento em um set é, na prática, independente do tamanho da coleção."),
        Quiz("O que defaultdict(list) resolve que um dict comum não resolve sozinho?",
             ["Ordena as chaves automaticamente", "Evita checar manualmente se a chave já existe antes do primeiro append",
              "Impede chaves duplicadas", "Torna o dicionário imutável"], 1,
             "Toda chave nova já nasce com uma lista vazia, dispensando o setdefault ou o if de checagem."),
    ],
    projeto=(
        "Faça agenda.py: dicionário nome -> telefone, com menu para adicionar, buscar, "
        "remover e listar em ordem alfabética, salvando tudo em memória. Use Counter para "
        "mostrar quantos contatos existem por DDD."
    ),
    leitura=["docs.python.org/pt-br/3/library/collections.html", "docs.python.org/pt-br/3/tutorial/datastructures.html#sets"],
))

# ---------------------------------------------------------------- DIA 10
DIAS.append(Dia(
    numero=10,
    titulo="Compreensões de lista, dicionário e conjunto",
    nivel="Iniciante",
    duracao="80 min",
    objetivos=[
        "Traduzir um laço for explícito para uma compreensão, e vice-versa",
        "Filtrar e transformar dados em uma única expressão legível",
        "Usar compreensões aninhadas com consciência de quando param de ser legíveis",
        "Diferenciar compreensão (ávida) de expressão geradora (preguiçosa) e saber quando usar cada uma",
        "Reconhecer quando um laço for tradicional é a escolha melhor, não a compreensão",
    ],
    teoria="""
1. A forma geral, e por que ela existe
------------------------------------------
    [ EXPRESSÃO for ITEM in ITERÁVEL if CONDIÇÃO ]

Uma compreensão de lista não é um recurso "extra" — ela é literalmente a
tradução direta do padrão mais comum de laço em Python: criar uma lista
vazia, percorrer algo, e ir acrescentando itens.

    resultado = []
    for ITEM in ITERÁVEL:
        if CONDIÇÃO:
            resultado.append(EXPRESSÃO)

Sempre que você perceber que está escrevendo esse padrão de 4 linhas, é
provável que uma compreensão de 1 linha expresse a mesma ideia com menos
ruído visual — não por concisão em si, mas porque a estrutura de 4 linhas
tem partes fixas (criar a lista, o for, o append) que só existem por causa
da sintaxe, não por causa da lógica do problema.

    [x * x for x in range(6)]                 -> [0, 1, 4, 9, 16, 25]
    [x for x in range(20) if x % 3 == 0]      -> [0, 3, 6, 9, 12, 15, 18]
    [p.upper() for p in palavras if len(p) > 3]

2. if/else DENTRO da expressão: uma sintaxe diferente do filtro
--------------------------------------------------------------------
Um erro comum de iniciante é confundir "filtrar" com "escolher um valor
alternativo". São coisas diferentes, e cada uma tem sua posição própria na
compreensão:

    ["par" if x % 2 == 0 else "impar" for x in range(4)]

Aqui não estamos removendo elementos — TODOS os números de `range(4)`
aparecem no resultado, só que transformados em uma das duas strings. Esse é
o ternário (Dia 5), que sempre vem ANTES do `for` quando usado dentro de uma
compreensão. Já o `if` de filtro (que remove elementos, sem alternativa)
sempre vem DEPOIS do `for`, no final da expressão. A regra prática: filtrar
elimina; ternário escolhe um valor para cada elemento, sem eliminar nenhum.

3. Compreensão de dicionário e de conjunto
------------------------------------------------
A mesma sintaxe geral se aplica trocando os colchetes por chaves, com uma
distinção adicional para dicionário (precisa de `chave: valor`):

    {p: len(p) for p in palavras}                   # dicionário: palavra -> tamanho
    {p.lower() for p in palavras}                    # conjunto: sem repetição, sem ordem
    {v: k for k, v in dicionario.items()}           # inverte um dicionário existente

4. Aninhamento: leia na mesma ordem em que escreveria os laços
---------------------------------------------------------------------
Uma compreensão pode ter mais de um `for`, e a leitura deve seguir a mesma
ordem que você usaria escrevendo os laços aninhados manualmente, da
esquerda para a direita:

    [ (i, j) for i in range(3) for j in range(2) ]
    # equivale a: for i in range(3): for j in range(2): resultado.append((i, j))

Duas aplicações muito comuns desse padrão:

    achatar = [x for linha in matriz for x in linha]                # achatar uma matriz em uma lista única
    matriz_nova = [[0] * 3 for _ in range(3)]                        # construir matriz (repare: colchetes internos!)
    transposta = [[linha[c] for linha in m] for c in range(len(m[0]))]  # transpor linhas e colunas

Note que `[[0] * 3 for _ in range(3)]` NÃO sofre da armadilha de
`[[0] * 3] * 3` que vimos no Dia 8: aqui, a compreensão executa `[0] * 3`
uma vez PARA CADA iteração de `_`, criando três listas de fato
independentes — é exatamente por isso que compreensões são a forma correta
de construir matrizes, não a multiplicação de lista.

5. Expressão geradora: trocando [] por ()
------------------------------------------------
Ao trocar os colchetes por parênteses, você não cria mais uma lista — cria
uma expressão geradora, que produz os valores SOB DEMANDA (preguiçosamente),
sem nunca materializar a coleção inteira na memória de uma vez:

    sum(x * x for x in range(1_000_000))    # nunca cria a lista de 1 milhão de itens na memória
    any(p.startswith("a") for p in palavras)
    max((len(p) for p in palavras), default=0)

Essa diferença de memória é o motivo pelo qual, ao passar uma expressão
geradora como ÚNICO argumento de uma função, os parênteses de fora da
função e os da expressão podem ser fundidos: `sum(x*x for x in range(10))`
funciona sem parênteses duplicados.

Regra prática para escolher: se você só vai CONSUMIR o resultado uma única
vez (somar, checar existência, percorrer uma vez), use o gerador — ele
economiza memória e costuma ser mais rápido para começar a produzir
resultados. Se você precisa acessar por índice, percorrer mais de uma vez,
ou saber o tamanho com `len()`, materialize uma lista de verdade.

6. Quando NÃO usar compreensão
------------------------------------
- quando o corpo precisa de um EFEITO COLATERAL, como `print` ou gravar em
  arquivo — compreensões existem para CONSTRUIR uma coleção, não para
  executar ações; usar uma compreensão só para disparar efeitos é
  considerado um mau uso da ferramenta;
- quando o resultado passa de ~2 linhas de leitura ou tem 3 ou mais níveis
  de aninhamento — nesse ponto, a economia de digitação já não compensa a
  perda de clareza;
- quando a condição `if` cresce com múltiplas cláusulas longas, dificultando
  saber, de relance, o que está sendo filtrado.

A régua final é sempre: legibilidade vence concisão. Uma compreensão que
exige ser lida duas ou três vezes para ser entendida é pior, na prática, do
que um laço `for` explícito de quatro linhas que qualquer pessoa lê uma vez
e entende.
""",
    exemplos=[
        Exemplo(
            titulo="Limpeza de dados em uma linha",
            codigo='''bruto = [" ana ", "", "  BIA", "carla ", "   "]
nomes = [n.strip().title() for n in bruto if n.strip()]
print(nomes)     # ['Ana', 'Bia', 'Carla']
''',
            explicacao="Filtra strings vazias (após strip) e normaliza a "
                       "capitalização ao mesmo tempo, em uma única passada.",
        ),
        Exemplo(
            titulo="Compreensão de dicionário com filtro",
            codigo='''estoque = {"caneta": 0, "papel": 12, "cola": 3}
disponiveis = {p: q for p, q in estoque.items() if q > 0}
print(disponiveis)      # {'papel': 12, 'cola': 3}
''',
            explicacao="Mesma sintaxe da compreensão de lista, só trocando "
                       "colchetes por chaves e usando par chave: valor.",
        ),
        Exemplo(
            titulo="Lista versus gerador: quando a diferença de memória importa",
            codigo='''import sys

lista = [x for x in range(100_000)]
gerador = (x for x in range(100_000))

print(sys.getsizeof(lista))     # milhares de bytes: todos os valores existem na memoria
print(sys.getsizeof(gerador))   # pouco mais de cem bytes: nada foi calculado ainda

print(sum(gerador))              # so agora os valores sao produzidos, um a um, e somados
''',
            explicacao="O gerador não guarda os 100 mil números — ele guarda "
                       "apenas 'como calcular o próximo', o que economiza "
                       "memória enquanto o resultado for consumido uma vez só.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d10e1",
            enunciado=(
                "Escreva quadrados_pares(n) devolvendo, com compreensão, a lista dos\n"
                "quadrados dos números pares de 0 até n-1."
            ),
            funcao="quadrados_pares",
            assinatura="def quadrados_pares(n):",
            testes=[
                ("quadrados_pares(7)", "[0, 4, 16, 36]"),
                ("quadrados_pares(1)", "[0]"),
                ("quadrados_pares(0)", "[]"),
            ],
            dica="[x*x for x in range(n) if x % 2 == 0]",
        ),
        Exercicio(
            id="d10e2",
            enunciado=(
                "Escreva agrupar_por_tamanho(palavras) devolvendo um dicionário\n"
                "tamanho -> lista de palavras daquele tamanho (na ordem de entrada)."
            ),
            funcao="agrupar_por_tamanho",
            assinatura="def agrupar_por_tamanho(palavras):",
            testes=[
                ("agrupar_por_tamanho(['oi', 'ana', 'ai'])",
                 "{2: ['oi', 'ai'], 3: ['ana']}"),
                ("agrupar_por_tamanho([])", "{}"),
            ],
            nivel="medio",
            dica="Pode usar setdefault num for comum, ou compreensão de dicionário com set de tamanhos.",
        ),
        Exercicio(
            id="d10e3",
            enunciado=(
                "Escreva transposta(matriz) que devolve a matriz transposta\n"
                "(linhas viram colunas). Matriz vazia devolve []."
            ),
            funcao="transposta",
            assinatura="def transposta(matriz):",
            testes=[
                ("transposta([[1, 2, 3], [4, 5, 6]])", "[[1, 4], [2, 5], [3, 6]]"),
                ("transposta([[1]])", "[[1]]"),
                ("transposta([])", "[]"),
            ],
            nivel="dificil",
            dica="[[l[c] for l in matriz] for c in range(len(matriz[0]))] — trate o caso vazio antes.",
        ),
    ],
    quiz=[
        Quiz("Qual a diferença entre [x for x in y] e (x for x in y)?",
             ["Nenhuma", "A segunda é um gerador preguiçoso", "A segunda é uma tupla",
              "A segunda é mais lenta"], 1,
             "Parênteses criam expressão geradora, avaliada sob demanda e sem materializar tudo na memória."),
        Quiz("Onde vai o if quando você quer FILTRAR elementos (eliminá-los)?",
             ["Antes do for", "Depois do for", "Dentro da expressão", "Não é possível"], 1,
             "Filtro vai no final; o ternário if/else (que escolhe um valor, sem eliminar) vai no começo."),
        Quiz("Por que [[0]*3 for _ in range(3)] é seguro, ao contrário de [[0]*3]*3?",
             ["Não há diferença real entre os dois", "A compreensão executa [0]*3 uma vez por iteração, criando listas independentes",
              "A compreensão usa menos memória sempre", "range(3) impede repetição de valores"], 1,
             "Na compreensão, cada volta do for cria uma lista nova; na multiplicação externa, as três 'linhas' são o mesmo objeto."),
        Quiz("Quando um laço for tradicional é preferível a uma compreensão?",
             ["Nunca, compreensão é sempre melhor", "Quando o corpo precisa de efeito colateral (print, gravar arquivo) ou tem lógica complexa",
              "Apenas quando os dados são números", "Quando o iterável tem menos de 10 elementos"], 1,
             "Compreensões existem para construir coleções; efeitos colaterais e lógica complexa pedem um for explícito."),
    ],
    projeto=(
        "Refaça o analisador de texto do Dia 4 usando apenas compreensões: "
        "palavras únicas, frequência, palavras com mais de 5 letras e tamanho médio. "
        "Compare o resultado de usar uma lista versus um gerador para calcular a soma dos tamanhos."
    ),
    leitura=["docs.python.org/pt-br/3/tutorial/datastructures.html#list-comprehensions", "PEP 289 - Generator Expressions"],
))

# ---------------------------------------------------------------- DIA 11
DIAS.append(Dia(
    numero=11,
    titulo="Funções: parâmetros, escopo e boas práticas",
    nivel="Intermediário",
    duracao="100 min",
    objetivos=[
        "Dominar parâmetros posicionais, nomeados e com valor padrão, na ordem certa",
        "Usar *args e **kwargs para assinaturas flexíveis, e desempacotar na chamada",
        "Entender a regra de escopo LEGB e quando global/nonlocal são realmente necessários",
        "Explicar por que argumentos padrão mutáveis são uma armadilha e como evitá-la",
        "Diferenciar reatribuir de mutar um argumento, e prever o efeito em quem chamou a função",
        "Escrever docstrings úteis seguindo uma convenção reconhecível",
    ],
    teoria="""
1. Definição e retorno
---------------------------
    def area_retangulo(base, altura):
        \"\"\"Devolve a área de um retângulo.\"\"\"
        return base * altura

Alguns fatos sobre `return` que costumam surpreender:

- `return` encerra a execução da função IMEDIATAMENTE, não importa quantas
  linhas ainda existam depois dele no corpo da função;
- uma função sem `return` explícito (ou com um `return` sozinho, sem valor)
  devolve `None` — é o comportamento padrão, não um erro;
- é possível devolver vários valores separados por vírgula — o que Python
  faz por baixo dos panos é empacotar tudo em uma TUPLA, e o desempacotamento
  na hora de receber o resultado é o que dá a ilusão de "múltiplos retornos":

      def divmod2(a, b):
          return a // b, a % b       # na verdade devolve a tupla (a // b, a % b)
      q, r = divmod2(7, 2)           # desempacotamento na atribuição

2. Argumentos: posicionais, nomeados e com valor padrão
--------------------------------------------------------------
    def cadastrar(nome, idade=18, ativo=True): ...

    cadastrar("Ana")                       # posicional: nome="Ana", o resto usa o padrão
    cadastrar("Ana", 30)                   # posicional: nome="Ana", idade=30
    cadastrar(idade=30, nome="Ana")        # nomeado: a ORDEM deixa de importar

Uma regra rígida da linguagem: parâmetros com valor padrão sempre vêm
DEPOIS dos parâmetros obrigatórios na definição da função — o interpretador
recusa (`SyntaxError`) uma assinatura como `def f(a=1, b):`, porque seria
ambíguo saber onde termina o "padrão" e começa o "obrigatório" na chamada.

3. A armadilha do argumento padrão mutável
------------------------------------------------
Esta é, sem exagero, uma das pegadinhas mais citadas de toda a linguagem
Python, e vale entender a fundo por que ela acontece:

    def add(item, lista=[]):      # ERRADO — parece inofensivo, mas não é
        lista.append(item)
        return lista

    add(1)      # [1]
    add(2)      # [1, 2]  <- devia ser [2], mas a lista "vazia" é sempre A MESMA!

O motivo: o valor padrão `[]` é criado UMA ÚNICA VEZ, no momento em que a
função é DEFINIDA (quando o `def` é executado), não a cada vez que ela é
CHAMADA. Como listas são mutáveis, todas as chamadas que não passam um
valor explícito para `lista` compartilham exatamente o mesmo objeto lista,
que vai acumulando itens de chamada em chamada — um efeito colateral
completamente inesperado para quem não conhece essa regra.

A correção padrão é usar `None` como "sentinela" (um valor que sinaliza
"nada foi passado") e criar o objeto mutável de verdade DENTRO do corpo da
função, a cada chamada:

    def add(item, lista=None):
        if lista is None:
            lista = []          # uma lista NOVA a cada chamada sem argumento
        lista.append(item)
        return lista

Essa regra vale para qualquer valor padrão mutável — listas, dicionários,
conjuntos, ou instâncias de classes próprias (Dia 16) que você mesmo
escreveu.

4. *args e **kwargs: assinaturas flexíveis
-------------------------------------------------
    def somar(*numeros):              # numeros vira uma TUPLA com os posicionais extras
        return sum(numeros)

    def config(**opcoes):             # opcoes vira um DICIONÁRIO com os nomeados extras
        return opcoes

    somar(1, 2, 3)                    # 6           -- numeros = (1, 2, 3)
    config(cor="azul", tamanho=10)    # {'cor': 'azul', 'tamanho': 10}

`*args` e `**kwargs` são só os NOMES convencionais — o que importa é o `*`
e o `**` antes do nome do parâmetro; você poderia chamá-los de qualquer
coisa, mas seguir a convenção ajuda quem lê seu código a reconhecer o
padrão de longe.

Na CHAMADA de uma função (não na definição), `*` e `**` fazem o oposto:
DESEMPACOTAM uma coleção existente em argumentos separados:

    valores = [1, 2, 3]; somar(*valores)              # equivale a somar(1, 2, 3)
    dados = {"nome": "Ana"}; cadastrar(**dados)       # equivale a cadastrar(nome="Ana")

Python também permite restringir explicitamente a forma como os argumentos
podem ser passados, usando marcadores especiais na assinatura:

    def f(a, b, /, c, *, d):
        ...

Aqui, `a` e `b` só podem ser passados POSICIONALMENTE (o `/` marca o fim
dos parâmetros só-posicionais); `d` só pode ser passado por NOME (o `*`
sozinho marca o início dos parâmetros só-nomeados); `c` aceita as duas
formas. Isso aparece bastante em bibliotecas profissionais para deixar a
assinatura de uma função mais clara e evitar que quem a chama dependa de
detalhes de implementação (como o nome exato de um parâmetro interno).

5. Escopo LEGB: onde Python procura um nome
--------------------------------------------------
Quando o interpretador encontra um nome de variável, ele procura nesta
ordem exata, parando na primeira ocorrência: Local -> Enclosing (função que
envolve, se houver) -> Global (módulo) -> Builtins (embutidos da
linguagem, como `len` ou `print`).

    x = "global"
    def externa():
        x = "enclosing"
        def interna():
            print(x)      # Python procura: local de interna? não tem x.
                           # enclosing (externa)? tem! usa "enclosing".
        interna()

Um ponto que confunde muita gente: ATRIBUIR um valor a um nome DENTRO de
uma função cria automaticamente uma variável LOCAL para essa função — mesmo
que exista uma variável de mesmo nome em um escopo mais externo. Se você
realmente quer alterar a variável do escopo de fora (não criar uma local
nova), precisa declarar isso explicitamente:

    global x       # dentro de uma função: refere-se à variável do MÓDULO
    nonlocal x     # dentro de uma função aninhada: refere-se à da função EXTERNA (closures)

A prática recomendada é usar `global` o mínimo possível: funções que
dependem de estado externo mutável são mais difíceis de testar isoladamente
e de raciocinar sobre, porque seu comportamento passa a depender de "o que
mais já rodou antes", não só dos argumentos recebidos.

6. Como Python realmente passa argumentos
------------------------------------------------
Python passa REFERÊNCIAS aos objetos — não é nem "por valor" (uma cópia
completa, como em C) nem exatamente "por referência" (no sentido de
apontador que outras linguagens usam), mas algo entre os dois, às vezes
chamado de "passagem por atribuição de objeto". A regra prática que resolve
99% das dúvidas: REATRIBUIR um parâmetro dentro da função não afeta quem
chamou; MUTAR o objeto (alterar seu conteúdo no lugar) afeta, sim, porque
o objeto é compartilhado:

    def f(lista, numero):
        lista.append(1)   # MUTA o objeto: visível fora da função, no chamador
        numero += 1        # REATRIBUI numero para um int NOVO: invisível fora,
                            # porque int é imutável e numero passou a apontar
                            # para um objeto diferente, só dentro da função

7. Docstring: documentação que vive junto com o código
--------------------------------------------------------------
    def calcular_juros(principal, taxa, meses):
        \"\"\"Calcula juros compostos.

        Args:
            principal: valor inicial em reais.
            taxa: taxa mensal em decimal (0.01 = 1%).
            meses: número de períodos.

        Returns:
            O montante final arredondado em 2 casas.
        \"\"\"

Esse formato (Args / Returns) é uma convenção popular (inspirada no estilo
do Google), não uma exigência da linguagem — o importante é escolher UM
padrão e usá-lo consistentemente, porque ferramentas de documentação e o
próprio `help()` sabem exibi-lo de forma legível.

Uma função bem escrita, segundo o consenso da comunidade, tem estas
características: faz UMA coisa (se o nome da função precisa de "e" para
descrevê-la, como `validar_e_salvar`, é sinal de que ela faz duas coisas);
tem um nome verbal, que descreve a ação; tem poucos parâmetros (a partir de
uns 4-5, considere agrupá-los em um objeto ou dicionário); e, sempre que
possível, NÃO imprime nada diretamente — quem decide COMO exibir um
resultado deve ser quem CHAMA a função, não a função em si. Isso mantém a
função reutilizável tanto num script de terminal quanto numa interface
gráfica (como a que este próprio curso usa).
""",
    exemplos=[
        Exemplo(
            titulo="Assinatura flexível com *args e **kwargs",
            codigo='''def relatorio(titulo, *linhas, largura=40, alinhar="<"):
    print(titulo.center(largura, "="))
    for l in linhas:
        print(f"{l:{alinhar}{largura}}")
    return len(linhas)

relatorio("VENDAS", "Ana: 120", "Bruno: 90", largura=24)
''',
            explicacao="largura e alinhar são keyword-only por virem depois "
                       "de *linhas na assinatura — não podem ser passados "
                       "posicionalmente, só por nome.",
        ),
        Exemplo(
            titulo="Escopo em ação: global e nonlocal",
            codigo='''contador = 0

def incrementar():
    global contador
    contador += 1

def acumulador():
    total = 0
    def somar(x):
        nonlocal total
        total += x
        return total
    return somar

incrementar(); incrementar()
soma = acumulador()
print(contador, soma(5), soma(3))     # 2 5 8
''',
            explicacao="global altera a variável do módulo; nonlocal altera "
                       "a variável da função que engloba (o 'total' de "
                       "acumulador), permitindo que somar acumule estado.",
        ),
        Exemplo(
            titulo="A armadilha do argumento padrão mutável, ao vivo",
            codigo='''def errado(item, historico=[]):
    historico.append(item)
    return historico

def certo(item, historico=None):
    if historico is None:
        historico = []
    historico.append(item)
    return historico

print(errado(1))   # [1]
print(errado(2))   # [1, 2]  -- a MESMA lista de antes, acumulando!

print(certo(1))     # [1]
print(certo(2))     # [2]     -- lista nova a cada chamada, como esperado
''',
            explicacao="errado() reaproveita a mesma lista criada uma única "
                       "vez na definição; certo() cria uma lista nova a cada "
                       "chamada em que o argumento não é passado.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d11e1",
            enunciado=(
                "Escreva saudacao(nome, saudacao='Ola') devolvendo 'Ola, Ana!'\n"
                "no formato: <saudacao>, <nome>!"
            ),
            funcao="saudacao",
            assinatura="def saudacao(nome, saudacao='Ola'):",
            testes=[
                ("saudacao('Ana')", "'Ola, Ana!'"),
                ("saudacao('Bruno', 'Bom dia')", "'Bom dia, Bruno!'"),
                ("saudacao(saudacao='Oi', nome='Cris')", "'Oi, Cris!'"),
            ],
            dica="Use f-string com os dois parâmetros.",
        ),
        Exercicio(
            id="d11e2",
            enunciado=(
                "Escreva estatisticas(*numeros) devolvendo a tupla (menor, maior, media).\n"
                "Sem argumentos, devolva (None, None, None)."
            ),
            funcao="estatisticas",
            assinatura="def estatisticas(*numeros):",
            testes=[
                ("estatisticas(3, 1, 5)", "(1, 5, 3.0)"),
                ("estatisticas()", "(None, None, None)"),
                ("estatisticas(4)", "(4, 4, 4.0)"),
            ],
            nivel="medio",
            dica="min(), max() e sum()/len() — mas trate a tupla vazia primeiro.",
        ),
        Exercicio(
            id="d11e3",
            enunciado=(
                "Escreva montar_url(base, **params) que devolve base + '?' + pares\n"
                "chave=valor separados por & e ORDENADOS por chave.\n"
                "Sem parâmetros, devolve apenas a base."
            ),
            funcao="montar_url",
            assinatura="def montar_url(base, **params):",
            testes=[
                ("montar_url('/api', b=2, a=1)", "'/api?a=1&b=2'"),
                ("montar_url('/api')", "'/api'"),
                ("montar_url('/x', z='oi')", "'/x?z=oi'"),
            ],
            nivel="dificil",
            dica="sorted(params.items()) e '&'.join(f'{k}={v}' ...).",
        ),
    ],
    quiz=[
        Quiz("Por que `def f(x, lista=[])` é perigoso?",
             ["É mais lento", "O padrão é criado uma única vez (na definição) e persiste entre chamadas",
              "Não é permitido", "Só funciona com números"], 1,
             "Use None como sentinela e crie a lista de verdade dentro do corpo da função."),
        Quiz("O que **kwargs recebe dentro de uma função?",
             ["Uma lista", "Uma tupla dos extras posicionais",
              "Um dicionário dos argumentos nomeados extras", "Uma string"], 2,
             "* junta os posicionais extras em tupla; ** junta os nomeados extras em dicionário."),
        Quiz("O que acontece se você fizer 'numero += 1' dentro de uma função, sem declarar global?",
             ["Altera o valor no chamador também", "Cria uma variável local nova; o valor externo não muda",
              "Levanta um erro imediatamente", "Depende do tipo do número"], 1,
             "Atribuir a um nome dentro de uma função cria uma variável local, a menos que global/nonlocal seja declarado."),
        Quiz("O que o marcador / na assinatura def f(a, b, /, c) indica?",
             ["Que a e b são opcionais", "Que a e b só podem ser passados por posição, nunca por nome",
              "Que a função aceita divisão", "Que c é obrigatório e os outros não"], 1,
             "O / marca o fim dos parâmetros exclusivamente posicionais."),
    ],
    projeto=(
        "Crie calculadora.py com funções puras (somar, subtrair, multiplicar, dividir "
        "com tratamento de zero, potencia) e um menu que as chama por um dicionário de despacho "
        "(nome da operação -> função), evitando um bloco if/elif gigante."
    ),
    leitura=["PEP 257 - Docstring Conventions", "PEP 570 - Positional-Only Parameters"],
))
# ---------------------------------------------------------------- DIA 12
DIAS.append(Dia(
    numero=12,
    titulo="Funções de alta ordem, lambda e recursão",
    nivel="Intermediário",
    duracao="100 min",
    objetivos=[
        "Explicar o que significa 'função é objeto de primeira classe' e por que isso importa",
        "Usar lambda com sorted, map e filter, sabendo quando NÃO usar lambda",
        "Escrever closures e entender por que elas 'lembram' o ambiente onde nasceram",
        "Escrever funções recursivas com caso base correto e evitar RecursionError",
        "Comparar recursão com iteração e saber quando cada uma é a ferramenta certa",
    ],
    teoria="""
1. Funções são objetos de primeira classe
------------------------------------------------
Em Python, uma função não é um conceito especial e separado dos outros
valores da linguagem — ela é um OBJETO como qualquer outro, que pode ser
atribuído a uma variável, guardado em uma lista, passado como argumento e
devolvido por outra função:

    def dobrar(x): return x * 2
    f = dobrar          # SEM parênteses: isto copia a REFERÊNCIA à função, não a executa
    f(5)                # 10 — agora f e dobrar apontam para o mesmo objeto função
    print(dobrar.__name__, dobrar.__doc__)   # funções também têm atributos, como qualquer objeto

Uma FUNÇÃO DE ALTA ORDEM é qualquer função que recebe outra função como
argumento e/ou devolve uma função como resultado. `sorted(lista, key=...)`,
`map()` e `filter()` são exemplos de alta ordem já embutidos na linguagem;
os decoradores do Dia 21 são o exemplo mais elaborado desse conceito.

2. lambda: função anônima de uma única expressão
--------------------------------------------------------
    quadrado = lambda x: x ** 2          # evite atribuir lambda a um nome: prefira def
    sorted(pessoas, key=lambda p: p["idade"])

`lambda` cria uma função sem nome, limitada a UMA expressão (sem
`if`/`for`/atribuições de várias linhas dentro dela). O uso idiomático é
como argumento CURTO e DESCARTÁVEL de outra função — normalmente dentro de
`sorted`, `map`, `filter` ou `key=`. Se a lógica precisa de um nome próprio
(porque será reutilizada), de uma condicional mais elaborada, ou de mais de
uma linha, a comunidade recomenda fortemente usar `def` em vez de lambda —
inclusive o guia de estilo oficial (PEP 8) desaconselha atribuir um lambda a
um nome, justamente porque `def` já faz isso melhor e com mensagens de erro
mais claras em tracebacks.

3. map, filter, sorted e reduce
------------------------------------
    list(map(str.upper, ["a", "b"]))            -> ['A', 'B']
    list(filter(lambda x: x > 0, [-1, 2]))      -> [2]
    sorted(dados, key=len, reverse=True)
    from functools import reduce
    reduce(lambda a, b: a * b, [1, 2, 3, 4])    -> 24    (multiplica tudo, acumulando)

Em Python idiomático moderno, compreensões (Dia 10) costumam ser
PREFERIDAS a `map`/`filter` quando a transformação é simples:

    [x.upper() for x in nomes]      # geralmente preferido a map(str.upper, nomes)
    [x for x in nums if x > 0]      # geralmente preferido a filter(lambda x: x > 0, nums)

Onde `map`/`filter` continuam brilhando é quando a função já EXISTE e tem
nome (como `str.upper` no primeiro exemplo) — nesse caso, passar a função
diretamente por nome é mais direto do que embrulhá-la numa compreensão.

Dois auxiliares da biblioteca padrão que evitam escrever lambdas repetitivas
para acessar campos:

    from operator import itemgetter, attrgetter
    sorted(registros, key=itemgetter("nota"))          # em vez de lambda r: r["nota"]
    sorted(objetos, key=attrgetter("idade"))            # em vez de lambda o: o.idade

4. Closure: uma função que carrega seu ambiente de origem
------------------------------------------------------------------
Uma closure é uma função interna que "lembra" as variáveis do escopo onde
foi criada, mesmo depois que esse escopo já terminou de executar:

    def multiplicador(fator):
        def aplicar(x):
            return x * fator     # fator vem do escopo de multiplicador, "capturado"
        return aplicar

    triplo = multiplicador(3)     # a função externa já terminou de rodar...
    triplo(10)                     # ...mas aplicar ainda lembra que fator = 3.  Resultado: 30

O que torna isso possível é que Python mantém uma referência ao ambiente
(chamado de "célula" internamente) enquanto alguma função ainda pode
precisar dele — o coletor de lixo da linguagem não descarta esse ambiente
enquanto `aplicar` (a closure) continuar existindo em algum lugar do
programa. Closures são a base conceitual dos decoradores (Dia 21), que
usam exatamente esse mecanismo para "envolver" outra função com
comportamento extra.

5. Recursão: uma função que chama a si mesma
------------------------------------------------
Toda função recursiva precisa de duas partes, sem exceção:

  (a) CASO BASE — a condição mais simples, que a função sabe resolver
      diretamente, sem chamar a si mesma;
  (b) PASSO RECURSIVO — a chamada da própria função com uma entrada MENOR
      ou mais próxima do caso base, garantindo que a recursão eventualmente
      termine.

    def fatorial(n):
        if n <= 1:            # caso base
            return 1
        return n * fatorial(n - 1)      # passo recursivo: aproxima-se de n <= 1

    def soma_lista(lista):
        if not lista:                    # caso base: lista vazia
            return 0
        return lista[0] + soma_lista(lista[1:])   # passo recursivo

Se o caso base estiver ausente, ou se o passo recursivo nunca se aproximar
dele (por exemplo, chamar `fatorial(n)` em vez de `fatorial(n - 1)` por
engano), o resultado é uma cadeia infinita de chamadas que eventualmente
levanta `RecursionError` — o Python tem um limite padrão de cerca de 1000
chamadas empilhadas (`sys.setrecursionlimit()` pode aumentar esse número,
mas raramente é a solução certa: geralmente é sinal de que a recursão
deveria virar iteração).

Um detalhe técnico importante: diferente de linguagens como Scheme ou
certas versões de JavaScript, Python NÃO faz otimização de chamada de
cauda (tail-call optimization) — mesmo uma recursão "bem comportada", onde
a chamada recursiva é a última coisa que a função faz, ainda consome uma
posição na pilha de chamadas a cada nível. Por isso, para percorrer
coleções grandes (milhares ou milhões de itens), a iteração (`for`, `while`)
é geralmente a escolha mais segura e eficiente em Python.

Onde a recursão realmente brilha é em estruturas que são NATURALMENTE
recursivas: árvores genealógicas, JSON aninhado (objetos dentro de objetos,
sem limite fixo de profundidade), sistemas de arquivos com subpastas, e
algoritmos de backtracking (tentar, se não der certo, desfazer e tentar
outro caminho) — problemas onde escrever a versão iterativa exigiria uma
pilha manual explícita, tornando o código mais confuso, não mais simples.

6. Um exemplo mais elaborado: divisão e conquista
------------------------------------------------------------
A busca binária é o exemplo clássico de um algoritmo "dividir para
conquistar", expresso naturalmente como recursão: a cada chamada, o
problema (encontrar um valor em uma faixa da lista) fica pela metade do
tamanho:

    def busca_binaria(lista, alvo, inicio=0, fim=None):
        if fim is None:
            fim = len(lista) - 1
        if inicio > fim:
            return -1                         # caso base: faixa vazia, não encontrado
        meio = (inicio + fim) // 2
        if lista[meio] == alvo:
            return meio                        # caso base: encontrou
        if lista[meio] < alvo:
            return busca_binaria(lista, alvo, meio + 1, fim)   # metade direita
        return busca_binaria(lista, alvo, inicio, meio - 1)     # metade esquerda

Note os DOIS casos base (faixa vazia e valor encontrado) e como cada
chamada recursiva reduz a faixa de busca pela metade — é isso que garante
que o algoritmo termine rapidamente mesmo em listas muito grandes (essa
noção de "quão rápido" é formalizada no Dia 29).
""",
    exemplos=[
        Exemplo(
            titulo="Ordenação com chaves compostas",
            codigo='''funcionarios = [
    {"nome": "Ana", "setor": "TI", "salario": 8000},
    {"nome": "Bruno", "setor": "RH", "salario": 6000},
    {"nome": "Cris", "setor": "TI", "salario": 9000},
]
por_setor_salario = sorted(funcionarios,
                           key=lambda f: (f["setor"], -f["salario"]))
for f in por_setor_salario:
    print(f["setor"], f["nome"], f["salario"])
''',
            explicacao="A tupla (setor, -salario) ordena primeiro por setor "
                       "(alfabético) e, dentro do mesmo setor, por salário "
                       "decrescente — o sinal negativo inverte só esse critério.",
        ),
        Exemplo(
            titulo="Recursão em estrutura aninhada",
            codigo='''def somar_tudo(dados):
    total = 0
    for item in dados:
        if isinstance(item, list):
            total += somar_tudo(item)     # desce um nivel de aninhamento
        else:
            total += item
    return total

print(somar_tudo([1, [2, [3, [4]], 5]]))   # 15
''',
            explicacao="A recursão acompanha a forma dos próprios dados: "
                       "cada lista aninhada dispara uma nova chamada, até "
                       "chegar aos números (o caso base implícito).",
        ),
        Exemplo(
            titulo="Closures criando funções personalizadas em série",
            codigo='''def criar_validador(minimo, maximo):
    def validar(valor):
        return minimo <= valor <= maximo
    return validar

nota_valida = criar_validador(0, 10)
idade_valida = criar_validador(0, 120)

print(nota_valida(8), nota_valida(15))     # True False
print(idade_valida(8), idade_valida(15))   # True True
''',
            explicacao="Cada chamada de criar_validador gera uma closure "
                       "independente, com seu próprio 'minimo' e 'maximo' "
                       "capturados — as duas funções não interferem entre si.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d12e1",
            enunciado=(
                "Escreva ordenar_por_sobrenome(nomes): recebe nomes completos como\n"
                "'Ana Silva' e devolve a lista ordenada pelo ÚLTIMO nome."
            ),
            funcao="ordenar_por_sobrenome",
            assinatura="def ordenar_por_sobrenome(nomes):",
            testes=[
                ("ordenar_por_sobrenome(['Ana Silva', 'Bo Alves', 'Cris Melo'])",
                 "['Bo Alves', 'Cris Melo', 'Ana Silva']"),
                ("ordenar_por_sobrenome([])", "[]"),
            ],
            dica="sorted(nomes, key=lambda n: n.split()[-1])",
        ),
        Exercicio(
            id="d12e2",
            enunciado="Escreva fatorial(n) de forma RECURSIVA (fatorial(0) == 1).",
            funcao="fatorial",
            assinatura="def fatorial(n):",
            testes=[
                ("fatorial(0)", "1"),
                ("fatorial(1)", "1"),
                ("fatorial(5)", "120"),
                ("fatorial(10)", "3628800"),
            ],
            dica="Caso base n <= 1 devolve 1; senão n * fatorial(n-1).",
        ),
        Exercicio(
            id="d12e3",
            enunciado=(
                "Escreva compor(f, g) que devolve uma NOVA função h tal que\n"
                "h(x) == f(g(x))."
            ),
            funcao="compor",
            assinatura="def compor(f, g):",
            testes=[
                ("compor(lambda x: x + 1, lambda x: x * 2)(5)", "11"),
                ("compor(str, len)('abcd')", "'4'"),
                ("callable(compor(len, str))", "True"),
            ],
            nivel="dificil",
            dica="Defina uma função interna e devolva-a SEM parênteses.",
        ),
    ],
    quiz=[
        Quiz("O que falta em uma recursão que causa RecursionError?",
             ["return", "caso base alcançável", "lambda", "global"], 1,
             "Sem caso base (ou sem se aproximar dele a cada chamada) a pilha de chamadas estoura."),
        Quiz("Qual é o uso mais apropriado de lambda?",
             ["Substituir todas as funções do programa", "Como argumento curto e descartável de sorted/map/filter",
              "Para escrever classes", "Para escrever laços"], 1,
             "lambda é para expressões curtas de uso único; para lógica reutilizável ou complexa, use def."),
        Quiz("Por que Python não otimiza chamadas de cauda (tail-call), diferente de outras linguagens?",
             ["É uma limitação técnica sem solução prevista, e por isso recursão profunda em Python geralmente deve virar iteração",
              "Python sempre otimiza automaticamente", "Só funciona em funções sem parâmetros",
              "Isso só afeta funções recursivas com mais de um parâmetro"], 0,
             "É uma decisão de design da linguagem: cada chamada recursiva, mesmo 'bem comportada', ocupa espaço na pilha."),
        Quiz("O que uma closure consegue fazer que uma função comum não consegue?",
             ["Rodar mais rápido sempre", "'Lembrar' e reutilizar variáveis do escopo onde foi criada, mesmo depois desse escopo terminar",
              "Aceitar infinitos argumentos", "Substituir uma classe inteira"], 1,
             "É essa capacidade de capturar o ambiente de criação que torna closures a base dos decoradores no Dia 21."),
    ],
    projeto=(
        "Crie pipeline.py: uma lista de funções de transformação de texto (minúsculas, "
        "remover acentos, trocar espaço por hífen) aplicadas em sequência por uma função "
        "aplicar_todas() que usa reduce ou um for simples. Depois, reescreva usando compor() "
        "do exercício de hoje para encadear apenas duas transformações."
    ),
    leitura=["docs.python.org/pt-br/3/howto/functional.html", "docs.python.org/pt-br/3/library/operator.html"],
))
# ---------------------------------------------------------------- DIA 13
DIAS.append(Dia(
    numero=13,
    titulo="Módulos, pacotes, venv e pip no Linux",
    nivel="Intermediário",
    duracao="90 min",
    objetivos=[
        "Organizar código em módulos e pacotes, entendendo o papel do __init__.py",
        "Explicar import, from-import e o papel de __name__ == '__main__'",
        "Criar, ativar e usar ambientes virtuais no Linux, e entender por que isso importa",
        "Saber onde o Python procura módulos e evitar o erro de sombrear a biblioteca padrão",
        "Reconhecer os módulos essenciais da biblioteca padrão antes de reinventá-los",
        "Usar pathlib como forma moderna de manipular caminhos de arquivo",
    ],
    teoria="""
1. Módulo é apenas um arquivo .py
--------------------------------------
A ideia de "módulo" em Python é mais simples do que parece: qualquer
arquivo `.py` já é, por si só, um módulo importável por outro arquivo:

    # matematica.py
    PI = 3.14159
    def area_circulo(r):
        return PI * r ** 2

    # main.py
    import matematica
    matematica.area_circulo(2)

    from matematica import area_circulo, PI      # importa nomes específicos
    import matematica as mat                      # apelido, comum para nomes longos
    from matematica import *                       # EVITE: importa tudo, "polui" o namespace

O motivo para evitar `from modulo import *` não é apenas estilo: ao importar
tudo de um módulo sem prefixo, fica impossível saber, só olhando o código,
de onde um nome específico veio — e se dois módulos importados dessa forma
tiverem um nome em comum, um sobrescreve o outro silenciosamente, sem
nenhum aviso.

2. O bloco __main__: o mesmo arquivo, dois papéis
--------------------------------------------------------
Python dá a cada módulo uma variável especial chamada `__name__`. Quando um
arquivo é executado DIRETAMENTE (`python3 arquivo.py`), essa variável vale
a string `"__main__"`. Quando o MESMO arquivo é importado por outro (`import
arquivo`), `__name__` vale o nome do módulo (`"arquivo"`), não
`"__main__"`. Isso permite escrever um arquivo que funciona nos dois papéis
sem conflito:

    def principal():
        ...

    if __name__ == "__main__":
        principal()

Se alguém importar esse arquivo só para usar suas funções, o bloco dentro
do `if` NÃO executa — só executa quando o arquivo é rodado como o programa
principal. Sem essa proteção, importar um módulo poderia disparar efeitos
colaterais indesejados (imprimir coisas na tela, abrir arquivos, pedir
entrada do usuário) só por ele ter sido carregado.

3. Pacote é uma pasta que agrupa módulos
-------------------------------------------------
    meu_projeto/
        __init__.py          (pode estar vazio; sua presença marca a pasta como pacote)
        modelos.py
        utils/
            __init__.py
            texto.py

    from meu_projeto.utils.texto import limpar

O arquivo `__init__.py` é o que sinaliza ao Python "esta pasta é um pacote
importável, não apenas uma pasta qualquer" — ele pode estar completamente
vazio, ou conter código de inicialização do pacote (imports que você quer
disponíveis direto no nível do pacote, por exemplo).

Dentro de um pacote, imports RELATIVOS usam pontos para indicar "a partir
daqui":

    from . import modelos               # um módulo no mesmo pacote
    from ..utils.texto import limpar    # subindo um nível e entrando em outro subpacote

Imports relativos só funcionam dentro de um pacote que foi ele mesmo
importado como pacote — eles não funcionam em um script solto executado
diretamente, o que costuma confundir iniciantes ao tentar rodar um arquivo
de dentro de um pacote isoladamente.

4. Onde o Python procura os módulos
------------------------------------------
    import sys
    print(sys.path)

`sys.path` é a lista de lugares, em ordem, onde o Python procura um módulo
ao encontrar um `import`: primeiro o diretório do próprio script que está
rodando, depois a variável de ambiente `PYTHONPATH` (se definida), e por
fim as bibliotecas instaladas (do sistema ou do ambiente virtual ativo).

Um erro clássico de iniciante: nomear um arquivo próprio igual a um módulo
da biblioteca padrão — `random.py`, `json.py`, `email.py`, `test.py`. Como
o diretório do script vem PRIMEIRO na busca, seu arquivo "sombreia" (esconde)
o módulo original, e qualquer `import random` dentro do seu próprio projeto
vai carregar o SEU arquivo em vez da biblioteca padrão — produzindo erros
confusos e difíceis de diagnosticar, porque tudo parece "quebrado" sem
motivo aparente.

5. Ambiente virtual: essencial para qualquer projeto Python sério no Linux
--------------------------------------------------------------------------------
    python3 -m venv .venv           # cria a pasta .venv com uma cópia isolada do interpretador
    source .venv/bin/activate       # ativa o ambiente (bash/zsh) — o prompt muda para indicar isso
    pip install requests            # instala uma biblioteca só DENTRO deste ambiente
    pip freeze > requirements.txt   # grava a lista exata de dependências instaladas
    pip install -r requirements.txt # reinstala essa mesma lista em outra máquina
    deactivate                       # sai do ambiente virtual

Por que isso importa tanto? Sem um ambiente virtual, todo `pip install`
afeta o Python do sistema operacional inteiro — e projetos diferentes quase
sempre precisam de versões diferentes das mesmas bibliotecas, o que gera
conflitos. Em muitas distribuições Linux modernas, o `pip install` fora de
um ambiente virtual é inclusive BLOQUEADO por padrão (uma política chamada
PEP 668, criada exatamente para evitar que usuários quebrem acidentalmente
ferramentas do próprio sistema operacional, que também dependem de Python).
A prática recomendada é: todo projeto Python tem seu próprio `.venv/`, que
NUNCA é versionado no git (por isso ele entra no `.gitignore`).

6. Biblioteca padrão que vale a pena conhecer desde já
-----------------------------------------------------------------
    math          sqrt, ceil, floor, pi, isclose, factorial
    random        random, randint, choice, sample, shuffle, seed
    datetime      date, datetime, timedelta
    pathlib       Path — manipulação moderna e orientada a objetos de caminhos
    os / sys      informações do ambiente, variáveis, argumentos de linha de comando
    json / csv    formatos de dados amplamente usados para troca de informação
    collections   Counter, defaultdict, deque, namedtuple (vistos nos Dias 9 e 29)
    itertools     combinações, produtos cartesianos, agrupamentos eficientes
    statistics    mean, median, stdev — estatística básica sem precisar de bibliotecas externas

A regra de ouro de qualquer programador Python experiente: antes de
escrever uma função para resolver algo do zero, vale a pena checar se a
biblioteca padrão já não resolve isso — a documentação oficial em
docs.python.org é organizada exatamente para essa consulta rápida.

7. pathlib em poucos minutos
---------------------------------
`pathlib.Path` é a forma moderna e recomendada de trabalhar com caminhos de
arquivo em Python, substituindo o estilo antigo baseado em strings e
`os.path`:

    from pathlib import Path
    p = Path("/home/usuario/dados/relatorio.csv")
    p.name      # 'relatorio.csv'                (nome completo do arquivo)
    p.stem      # 'relatorio'                     (nome sem a extensão)
    p.suffix    # '.csv'                          (só a extensão)
    p.parent    # PosixPath('/home/usuario/dados')  (a pasta que contém o arquivo)
    p.exists(), p.is_file(), p.is_dir()             (testes sobre o sistema de arquivos real)
    (Path.home() / "projetos" / "x.txt")            # o operador / MONTA caminhos, de forma legível

O uso do operador `/` para juntar partes de um caminho (em vez de
concatenar strings manualmente com `+` ou `os.path.join`) é o que mais
chama atenção de quem vem de outras linguagens — e funciona corretamente em
qualquer sistema operacional, já que `Path` sabe qual separador usar
internamente (`/` no Linux/macOS, `\\` no Windows), sem que você precise se
preocupar com isso.
""",
    exemplos=[
        Exemplo(
            titulo="Módulo reutilizável com bloco main",
            codigo='''# conversores.py
def c_para_f(c):
    return c * 9 / 5 + 32

def f_para_c(f):
    return (f - 32) * 5 / 9

if __name__ == "__main__":
    for c in (0, 25, 100):
        print(c, "C =", c_para_f(c), "F")
''',
            explicacao="Rodar este arquivo diretamente executa o laço de "
                       "teste; importá-lo de outro arquivo só traz as duas "
                       "funções, sem disparar nenhuma impressão na tela.",
        ),
        Exemplo(
            titulo="Datas com datetime",
            codigo='''from datetime import date, timedelta

hoje = date(2026, 7, 28)
prazo = hoje + timedelta(days=45)
print(prazo.isoformat())               # 2026-09-11
print((prazo - hoje).days, "dias")     # 45 dias
print(hoje.strftime("%d/%m/%Y"))       # 28/07/2026
''',
            explicacao="timedelta faz aritmética de datas sem dor de "
                       "cabeça — Python já sabe lidar com meses de tamanhos "
                       "diferentes e anos bissextos por trás dos panos.",
        ),
        Exemplo(
            titulo="Um sombreamento de módulo, para nunca fazer isso",
            codigo='''# Suponha um arquivo chamado random.py na mesma pasta do seu projeto,
# contendo por exemplo: def sorteio(): return 4

# Em outro arquivo do MESMO projeto:
import random
print(random.randint(1, 10))   # ERRO: AttributeError, pois o "random"
                                # carregado foi o SEU arquivo, nao a
                                # biblioteca padrao — ela nao tem sorteio()
                                # nem foi encontrada, porque seu arquivo
                                # veio primeiro na busca de sys.path
''',
            explicacao="Nunca nomeie um arquivo seu igual a um módulo da "
                       "biblioteca padrão (random, json, os, string, "
                       "email, test...) — o Python encontra o seu primeiro.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d13e1",
            enunciado=(
                "Importe o módulo math e escreva area_circulo(r) devolvendo a área\n"
                "arredondada com 4 casas decimais."
            ),
            funcao="area_circulo",
            assinatura="import math\n\n\ndef area_circulo(r):",
            testes=[
                ("area_circulo(1)", "3.1416"),
                ("area_circulo(2)", "12.5664"),
                ("area_circulo(0)", "0.0"),
            ],
            dica="round(math.pi * r ** 2, 4)",
        ),
        Exercicio(
            id="d13e2",
            enunciado=(
                "Escreva dias_entre(d1, d2): recebe duas datas no formato 'AAAA-MM-DD'\n"
                "e devolve o número de dias entre elas (sempre positivo)."
            ),
            funcao="dias_entre",
            assinatura="from datetime import date\n\n\ndef dias_entre(d1, d2):",
            testes=[
                ("dias_entre('2024-01-01', '2024-01-31')", "30"),
                ("dias_entre('2024-03-01', '2024-02-01')", "29"),
                ("dias_entre('2026-07-28', '2026-07-28')", "0"),
            ],
            nivel="medio",
            dica="date.fromisoformat() converte; abs((a - b).days) dá o valor.",
        ),
        Exercicio(
            id="d13e3",
            enunciado=(
                "Use pathlib para escrever info_caminho(caminho) devolvendo a tupla\n"
                "(nome_do_arquivo, nome_sem_extensao, extensao)."
            ),
            funcao="info_caminho",
            assinatura="from pathlib import Path\n\n\ndef info_caminho(caminho):",
            testes=[
                ("info_caminho('/home/ana/dados/relatorio.csv')",
                 "('relatorio.csv', 'relatorio', '.csv')"),
                ("info_caminho('script.py')", "('script.py', 'script', '.py')"),
                ("info_caminho('/tmp/README')", "('README', 'README', '')"),
            ],
            dica="Path(caminho).name, .stem e .suffix.",
        ),
    ],
    quiz=[
        Quiz("Para que serve `if __name__ == '__main__':`?",
             ["Definir a função principal", "Executar código só quando o arquivo roda diretamente, não quando é importado",
              "Criar um módulo", "Importar bibliotecas"], 1,
             "Evita que efeitos colaterais de script (prints, execução de rotina) disparem durante um import."),
        Quiz("Qual comando cria um ambiente virtual no Linux?",
             ["pip venv", "python3 -m venv .venv", "virtualenv --pip", "python3 install venv"], 1,
             "O módulo venv já vem embutido no Python 3, sem instalação adicional."),
        Quiz("O que acontece se você criar um arquivo chamado random.py no seu projeto?",
             ["Nada, os nomes coexistem sem problema", "Ele sombreia o módulo random da biblioteca padrão, causando erros confusos ao importar random",
              "O Python renomeia automaticamente", "Isso só é um problema no Windows"], 1,
             "O diretório do script vem primeiro na busca de módulos (sys.path), então seu arquivo é encontrado antes do original."),
        Quiz("Por que usar ambientes virtuais (venv) em vez de instalar tudo globalmente com pip?",
             ["É apenas uma preferência estética", "Evita conflitos de versão entre projetos diferentes e não afeta o Python do sistema operacional",
              "Torna o código mais rápido", "É a única forma de usar bibliotecas externas"], 1,
             "Cada projeto pode ter suas próprias versões de dependências, isoladas das de outros projetos e do sistema."),
    ],
    projeto=(
        "Transforme suas funções dos dias anteriores num pacote utilitarios/ com módulos "
        "texto.py, numeros.py e datas.py (cada um com seu próprio bloco __main__ de teste), "
        "e um main.py que importa e demonstra cada um. Crie um .venv para o projeto, mesmo "
        "sem dependências externas ainda, só para praticar o fluxo."
    ),
    leitura=["docs.python.org/pt-br/3/tutorial/modules.html", "PEP 668"],
))

# ---------------------------------------------------------------- DIA 14
DIAS.append(Dia(
    numero=14,
    titulo="Arquivos, JSON e CSV",
    nivel="Intermediário",
    duracao="100 min",
    objetivos=[
        "Ler e escrever arquivos com with, entendendo por que isso é sempre preferível",
        "Escolher o modo de abertura correto e sempre especificar o encoding no Linux",
        "Ler arquivos grandes por streaming, sem carregar tudo na memória de uma vez",
        "Serializar e desserializar dados com json, sabendo o que não é serializável",
        "Processar tabelas com o módulo csv, incluindo DictReader e DictWriter",
        "Escrever em arquivo de forma seguraatômica, sem risco de corromper dados a meio caminho",
    ],
    teoria="""
1. Sempre use `with` para abrir arquivos
------------------------------------------------
    with open("dados.txt", "r", encoding="utf-8") as f:
        conteudo = f.read()
    # o arquivo já está fechado aqui, mesmo que ocorra um erro dentro do bloco

O bloco `with` (um "gerenciador de contexto", explicado a fundo no Dia 22)
garante que o arquivo seja fechado automaticamente ao sair do bloco — seja
pelo caminho normal, seja porque uma exceção interrompeu a execução no
meio. Sem `with`, seria necessário chamar `f.close()` manualmente, e
esquecer isso (ou esquecer de fechá-lo quando um erro interrompe o código
antes do close) pode deixar arquivos "presos", consumindo recursos do
sistema operacional até o programa terminar.

Os modos de abertura mais comuns:

    "r"   leitura (é o padrão se você omitir) — levanta erro se o arquivo não existir
    "w"   escrita — CRIA o arquivo se não existir, ou APAGA todo o conteúdo existente
    "a"   append (adicionar) — escreve sempre no final, sem apagar o que já havia
    "x"   criação exclusiva — levanta erro se o arquivo já existir (evita sobrescrever sem querer)
    "r+"  leitura e escrita simultâneas
    "rb" / "wb"  modo binário (para imagens, arquivos zip, executáveis) — sem parâmetro de encoding

No Linux (e em qualquer sistema, na verdade), é uma boa prática sempre
passar `encoding="utf-8"` explicitamente ao abrir arquivos de texto. Sem
isso, Python usa o encoding padrão do LOCALE da máquina — que pode variar
entre sistemas, containers e servidores, e já foi causa de bugs difíceis de
reproduzir em produção ("funciona na minha máquina, mas quebra no
servidor" é, frequentemente, um problema de encoding).

2. Formas de ler um arquivo, e por que a maioria delas é uma armadilha
------------------------------------------------------------------------------
    f.read()             lê TUDO de uma vez, devolvendo uma única string
    f.readline()         lê uma única linha por vez
    f.readlines()        lê TUDO de uma vez, mas já devolve uma lista de linhas
    for linha in f:      MELHOR: percorre linha por linha, sem carregar o arquivo inteiro na memória

Para arquivos pequenos (configurações, textos curtos), `.read()` é
perfeitamente aceitável. Mas para arquivos GRANDES — logs de um sistema em
produção, exportações de banco de dados com milhões de linhas — usar
`.read()` ou `.readlines()` tenta carregar o conteúdo inteiro na memória
RAM de uma vez, o que pode travar ou derrubar o programa. `for linha in f:`
processa em STREAMING: uma linha entra na memória, é processada, e é
descartada antes da próxima linha ser lida — o consumo de memória fica
praticamente constante, não importa o tamanho do arquivo.

    for linha in f:
        linha = linha.rstrip("\\n")     # cada linha lida já vem com a quebra de linha no final

3. Escrevendo em um arquivo
--------------------------------
    with open("saida.txt", "w", encoding="utf-8") as f:
        f.write("primeira linha\\n")       # write() NÃO adiciona quebra de linha sozinho!
        f.writelines(["a\\n", "b\\n"])      # escreve uma lista de strings, sem separador automático
        print("via print", file=f)         # print() também sabe escrever direto num arquivo

Um erro comum: esperar que `f.write("texto")` pule para a próxima linha
automaticamente, como `print` faz por padrão. `write()` escreve EXATAMENTE
o que você passar, sem adicionar nada — se você quer uma quebra de linha,
precisa incluir `"\\n"` você mesmo.

4. pathlib para tarefas simples de arquivo
----------------------------------------------
Para operações rápidas (ler ou escrever o conteúdo inteiro de um arquivo
pequeno), `pathlib.Path` (Dia 13) oferece atalhos que dispensam o `with`
explícito, já cuidando de abrir e fechar o arquivo internamente:

    from pathlib import Path
    p = Path("nota.txt")
    p.write_text("conteudo", encoding="utf-8")
    texto = p.read_text(encoding="utf-8")
    p.unlink(missing_ok=True)              # apaga o arquivo; não erra se ele não existir
    for arquivo in Path(".").glob("*.py"): ...       # lista arquivos .py na pasta atual
    for arquivo in Path(".").rglob("*.py"): ...      # o mesmo, mas RECURSIVO em subpastas

5. JSON: o formato universal de troca de dados estruturados
------------------------------------------------------------------
    import json
    json.dumps(obj, ensure_ascii=False, indent=2)   # converte um objeto Python para uma STRING JSON
    json.loads(texto)                               # converte uma STRING JSON de volta para um objeto Python
    json.dump(obj, arquivo)                         # como dumps, mas escreve DIRETO em um arquivo
    json.load(arquivo)                               # como loads, mas lê DIRETO de um arquivo

O mapeamento de tipos entre Python e JSON segue uma tabela previsível: `dict`
vira objeto JSON, `list` vira array JSON, `str`/`int`/`float` mantêm
correspondência direta, `True`/`False`/`None` viram `true`/`false`/`null`
(em minúsculas, seguindo a convenção JSON, diferente do Python). Uma
armadilha comum: TUPLAS viram LISTAS ao serem serializadas — o JSON não tem
o conceito de tupla, então essa distinção se perde na conversão. Outra:
objetos `datetime` NÃO são serializáveis diretamente — é preciso convertê-
los para string antes (com `.isoformat()`) ou fornecer uma função customizada
através do parâmetro `default=` de `json.dumps`.

    json.dumps({"nome": "João"}, ensure_ascii=False)   # 'ensure_ascii=False' preserva acentos como estão,
                                                         # em vez de escapá-los como sequências \\uXXXX

6. CSV: o formato universal de tabelas
---------------------------------------------
    import csv
    with open("dados.csv", newline="", encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            print(linha["nome"], linha["nota"])     # atenção: os valores lidos são sempre STRINGS!

    with open("saida.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["nome", "nota"])
        w.writeheader()
        w.writerows(registros)

`csv.DictReader` lê cada linha do arquivo como um dicionário, usando a
PRIMEIRA linha do CSV como os nomes das chaves — muito mais legível do que
acessar colunas por índice numérico. Um detalhe fácil de esquecer: todo
valor lido de um CSV vem como STRING, mesmo que pareça um número — se você
precisar de `9` como inteiro em vez de `'9'` como texto, a conversão
(`int()`, `float()`) é sua responsabilidade.

O parâmetro `newline=""` ao abrir o arquivo é uma exigência específica do
módulo `csv` para evitar linhas em branco extras no Windows (mas é uma boa
prática incluir sempre, mesmo em Linux, por portabilidade). Para arquivos
com separador diferente de vírgula (comum em CSVs exportados de planilhas
em português, que usam ponto e vírgula): `csv.reader(f, delimiter=";")`.

7. Escrita segura: evitando arquivos corrompidos pela metade
--------------------------------------------------------------------
Se o programa for interrompido (queda de energia, `kill -9`, um erro não
tratado) exatamente no meio de uma escrita, o arquivo final pode ficar
truncado — com metade do conteúdo antigo e metade do novo, ou pior, vazio.
A técnica profissional para evitar isso é escrever em um arquivo TEMPORÁRIO
primeiro e só então RENOMEAR para o nome final:

    from pathlib import Path
    temporario = Path("dados.json.tmp")
    temporario.write_text(novo_conteudo, encoding="utf-8")
    temporario.replace("dados.json")     # operação atômica no mesmo sistema de arquivos

`Path.replace()` é ATÔMICA quando origem e destino estão no mesmo sistema
de arquivos — ou seja, do ponto de vista de qualquer programa observando de
fora, o arquivo `dados.json` muda instantaneamente do conteúdo antigo para
o novo, sem nunca existir um estado "pela metade" visível para outros
processos.
""",
    exemplos=[
        Exemplo(
            titulo="Ler, filtrar e gravar",
            codigo='''from pathlib import Path

entrada = Path("/tmp/log.txt")
entrada.write_text("INFO ok\\nERRO falhou\\nINFO fim\\n", encoding="utf-8")

erros = [l for l in entrada.read_text(encoding="utf-8").splitlines()
         if l.startswith("ERRO")]
Path("/tmp/erros.txt").write_text("\\n".join(erros), encoding="utf-8")
print(erros)
''',
            explicacao="Para arquivos pequenos, pathlib elimina o "
                       "boilerplate de abrir/fechar manualmente com with.",
        ),
        Exemplo(
            titulo="JSON de ida e volta",
            codigo='''import json

config = {"tema": "escuro", "fontes": [12, 14], "auto_salvar": True}
texto = json.dumps(config, ensure_ascii=False, indent=2)
print(texto)
recuperado = json.loads(texto)
print(recuperado["fontes"][1])      # 14
''',
            explicacao="indent deixa a saída legível para humanos; "
                       "ensure_ascii=False preserva acentos em vez de "
                       "escapá-los como \\uXXXX.",
        ),
        Exemplo(
            titulo="Streaming versus carregar tudo de uma vez",
            codigo='''from pathlib import Path

arquivo = Path("/tmp/numeros.txt")
arquivo.write_text("\\n".join(str(i) for i in range(100000)), encoding="utf-8")

# Carrega tudo de uma vez (aceitavel para arquivos pequenos):
total_read = sum(int(l) for l in arquivo.read_text(encoding="utf-8").splitlines())

# Streaming linha a linha (preferivel para arquivos grandes):
total_stream = 0
with open(arquivo, encoding="utf-8") as f:
    for linha in f:
        total_stream += int(linha)

print(total_read == total_stream, total_stream)
''',
            explicacao="Os dois chegam ao mesmo resultado, mas o segundo "
                       "nunca guarda o arquivo inteiro na memória — só uma "
                       "linha de cada vez.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d14e1",
            enunciado=(
                "Escreva ida_e_volta(dados): grava o dicionário em um arquivo JSON\n"
                "temporário, lê de volta e devolve o objeto lido."
            ),
            funcao="ida_e_volta",
            assinatura="import json\nimport tempfile\nfrom pathlib import Path\n\n\ndef ida_e_volta(dados):",
            testes=[
                ("ida_e_volta({'a': 1, 'b': [2, 3]})", "{'a': 1, 'b': [2, 3]}"),
                ("ida_e_volta({})", "{}"),
            ],
            nivel="medio",
            dica="Use tempfile.gettempdir() ou Path('/tmp') para o arquivo.",
        ),
        Exercicio(
            id="d14e2",
            enunciado=(
                "Escreva linhas_uteis(texto): devolve a lista de linhas sem espaços nas\n"
                "pontas, descartando linhas vazias e as que começam com #."
            ),
            funcao="linhas_uteis",
            assinatura="def linhas_uteis(texto):",
            testes=[
                ("linhas_uteis('a\\n\\n # com\\n b ')", "['a', 'b']"),
                ("linhas_uteis('')", "[]"),
                ("linhas_uteis('#tudo comentado')", "[]"),
            ],
            dica="splitlines() + strip() + filtros.",
        ),
        Exercicio(
            id="d14e3",
            enunciado=(
                "Escreva csv_para_dicts(texto_csv) que converte um CSV (com cabeçalho,\n"
                "separado por vírgula) em uma lista de dicionários."
            ),
            funcao="csv_para_dicts",
            assinatura="import csv\nimport io\n\n\ndef csv_para_dicts(texto_csv):",
            testes=[
                ("csv_para_dicts('nome,nota\\nana,9\\nbia,7')",
                 "[{'nome': 'ana', 'nota': '9'}, {'nome': 'bia', 'nota': '7'}]"),
                ("csv_para_dicts('a,b')", "[]"),
            ],
            nivel="dificil",
            dica="io.StringIO(texto) transforma a string em um arquivo em memória para o DictReader.",
        ),
    ],
    quiz=[
        Quiz("O que acontece ao abrir um arquivo existente no modo 'w'?",
             ["Erro", "O conteúdo existente é apagado (truncado)", "Escreve no final, preservando o conteúdo", "Abre só para leitura"], 1,
             "'w' trunca o arquivo inteiro; para preservar o conteúdo existente e adicionar ao final, use 'a'."),
        Quiz("Por que usar `with open(...)` em vez de open()/close() manual?",
             ["É mais rápido de executar", "Garante o fechamento do arquivo automaticamente, mesmo se ocorrer um erro no meio",
              "Só with permite ler JSON", "with é obrigatório na sintaxe do Python"], 1,
             "with é um gerenciador de contexto que fecha o recurso de forma confiável, mesmo diante de exceções."),
        Quiz("Por que 'for linha in arquivo:' é preferível a arquivo.read() para arquivos muito grandes?",
             ["Não há diferença real de comportamento", "Processa uma linha por vez (streaming), sem carregar o arquivo inteiro na memória",
              "É a única forma de ler arquivos de texto", "read() não funciona com encoding utf-8"], 1,
             "read() e readlines() carregam tudo de uma vez; o for direto no arquivo consome memória praticamente constante."),
        Quiz("Por que valores lidos de um CSV com DictReader vêm sempre como string?",
             ["É um bug do módulo csv", "O formato CSV é puro texto; não existe tipo número dentro do próprio arquivo",
              "Porque o arquivo não foi aberto com encoding correto", "Só acontece se o CSV tiver cabeçalho"], 1,
             "CSV é um formato inteiramente textual; a conversão para int/float é sempre responsabilidade de quem lê."),
    ],
    projeto=(
        "Crie notas_csv.py: leia um CSV de alunos e notas, calcule a média de cada aluno, "
        "grave um novo CSV com a situação (aprovado/reprovado) e um resumo em JSON. Implemente "
        "a escrita segura (arquivo temporário + replace) para o resumo em JSON."
    ),
    leitura=["docs.python.org/pt-br/3/library/json.html", "docs.python.org/pt-br/3/library/csv.html"],
))

# ---------------------------------------------------------------- DIA 15
DIAS.append(Dia(
    numero=15,
    titulo="Erros e exceções",
    nivel="Intermediário",
    duracao="90 min",
    objetivos=[
        "Tratar erros com try/except/else/finally, entendendo o papel exato de cada bloco",
        "Capturar exceções específicas em vez de genéricas, e usar a instância da exceção",
        "Criar exceções personalizadas que carregam dados úteis para quem as captura",
        "Aplicar o estilo EAFP e entender por que a comunidade Python o prefere a LBYL",
        "Diferenciar assert de uma validação de verdade, e saber quando usar cada um",
        "Adotar boas práticas de tratamento de erro: falhar cedo, falhar alto, nunca em silêncio",
    ],
    teoria="""
1. Estrutura completa: try/except/else/finally
--------------------------------------------------------
    try:
        valor = int(texto)
    except ValueError as e:
        print("conversao falhou:", e)
        valor = 0
    except (TypeError, KeyError):
        valor = -1
    else:
        print("deu certo, nenhum erro ocorreu")     # só executa se NÃO houve exceção
    finally:
        print("sempre executa")                     # limpeza, mesmo com return ou raise dentro do try

Cada bloco tem um papel bem definido, que vale a pena decorar por
significado, não só por posição:

- `try`: o código que PODE falhar;
- `except`: o que fazer quando falha (pode haver vários, para tipos
  diferentes de erro, testados na ordem em que aparecem);
- `else`: código que só roda quando NADA deu errado — útil para separar
  "o que pode falhar" (dentro do try) de "o que fazer depois que deu certo"
  (no else), deixando ambos mais claros isoladamente;
- `finally`: código que roda SEMPRE, independente de ter havido erro ou não,
  e mesmo que um `return` tenha sido executado dentro do try ou do except —
  é o lugar certo para liberar recursos (fechar arquivos, conexões de rede).

2. Hierarquia de exceções (resumo do essencial)
----------------------------------------------------
    BaseException
     +- SystemExit, KeyboardInterrupt, GeneratorExit
     +- Exception
         +- ArithmeticError -> ZeroDivisionError
         +- LookupError     -> IndexError, KeyError
         +- OSError         -> FileNotFoundError, PermissionError
         +- ValueError, TypeError, AttributeError, NameError
         +- RuntimeError    -> RecursionError
         +- StopIteration

Toda exceção do dia a dia herda de `Exception`, que por sua vez herda de
`BaseException` — mas note que `SystemExit` e `KeyboardInterrupt` (disparado
por Ctrl+C) ficam FORA de `Exception`, diretamente sob `BaseException`. Isso
é deliberado: um `except Exception:` genérico não captura essas duas, o que
significa que Ctrl+C ainda consegue interromper seu programa mesmo que ele
tenha um bloco `except Exception` "pegando tudo".

A regra de ouro é capturar sempre o tipo MAIS ESPECÍFICO possível para cada
situação. `except Exception:` só se justifica na FRONTEIRA do programa —
por exemplo, para registrar o erro em log e encerrar com uma mensagem
decente ao usuário, não silenciosamente. E `except:` sozinho, sem
especificar nenhum tipo, é considerado um erro grave de estilo: ele captura
literalmente TUDO, inclusive `KeyboardInterrupt` e `SystemExit`, tornando
impossível até mesmo interromper o programa com Ctrl+C enquanto ele estiver
dentro desse bloco.

O anti-padrão mais citado da linguagem, que vale memorizar para NUNCA
escrever:

    try:
        fazer_tudo()
    except Exception:
        pass                # o erro desaparece silenciosamente — e o bug nunca é descoberto

Esse padrão (apelidado às vezes de "exceção engolida" ou, em inglês,
"the bare except that swallows everything") é responsável por incontáveis
horas de depuração em código profissional, porque o sintoma do bug aparece
muito longe (ou muito depois) da causa real, que foi silenciada aqui.

3. Levantando exceções deliberadamente
--------------------------------------------
    raise ValueError("idade nao pode ser negativa")
    raise                                    # dentro de um except: relevanta a MESMA exceção capturada

Uma técnica importante para preservar contexto ao converter um erro em
outro é o encadeamento com `from`, que mantém visível no traceback QUAL foi
a causa original, em vez de esconder essa informação:

    try:
        configuracao = obter_config()
    except KeyError as e:
        raise ConfiguracaoInvalida("falta a chave obrigatória") from e

Sem o `from e`, quem depurar o problema veria apenas a nova exceção
`ConfiguracaoInvalida`, sem saber que ela foi causada por um `KeyError`
específico — o `from` preserva essa cadeia de causalidade no próprio
traceback impresso.

4. Exceções personalizadas: comunicando erros do SEU domínio
------------------------------------------------------------------
    class ErroDeNegocio(Exception):
        \"\"\"Classe base para todos os erros específicos desta aplicação.\"\"\"

    class SaldoInsuficiente(ErroDeNegocio):
        def __init__(self, saldo, valor):
            super().__init__(f"saldo {saldo} < saque {valor}")
            self.saldo = saldo
            self.valor = valor

Criar uma classe BASE própria (`ErroDeNegocio` aqui) para toda a família de
erros do seu programa permite que quem usa seu código capture a família
inteira de uma vez, com um único `except ErroDeNegocio:`, sem precisar
listar cada subtipo específico — e ainda assim capturar um subtipo
específico quando precisar de um tratamento diferenciado para ele.

5. EAFP contra LBYL: duas filosofias de programação defensiva
--------------------------------------------------------------------
A comunidade Python tem uma preferência clara e batizada por um acrônimo
memorável: EAFP, de "Easier to Ask Forgiveness than Permission" ("é mais
fácil pedir perdão do que permissão"):

    try:                            # estilo EAFP: tenta e trata o erro se ocorrer
        return dados["chave"]
    except KeyError:
        return padrao

    if "chave" in dados:            # estilo LBYL ("Look Before You Leap"): checa antes de agir
        return dados["chave"]
    else:
        return padrao

Por que EAFP é preferido? Duas razões práticas: primeiro, ele evita
CONDIÇÕES DE CORRIDA (race conditions) — por exemplo, checar
`arquivo.exists()` e, um instante depois, tentar abrir o arquivo, corre o
risco de o arquivo ter sido apagado bem NESSE intervalo entre a checagem e
a ação, por outro processo do sistema; o `try/except` direto elimina essa
janela de tempo vulnerável. Segundo, EAFP costuma ser mais rápido no
"caminho feliz" (quando tudo dá certo), porque não paga o custo de checar a
condição toda vez antes de agir — a checagem só acontece (via exceção) nos
casos raros em que algo realmente deu errado.

6. assert não substitui validação de entrada
--------------------------------------------------
`assert condicao, "mensagem"` levanta `AssertionError` se a condição for
falsa — mas existe um detalhe crítico que torna `assert` inadequado para
validar dados de usuário ou entrada externa: quando o Python roda com a
flag de otimização `-O`, TODAS as instruções `assert` do programa são
simplesmente REMOVIDAS, como se nunca tivessem existido. Por isso, `assert`
deve ser usado apenas para checagens INTERNAS de desenvolvimento (verificar
uma invariante que, se falhar, indica um BUG no seu próprio código, não um
erro do usuário) — nunca para validar CPF, senha, faixa de idade ou
qualquer coisa que possa legitimamente vir errada de fora do programa.

7. Boas práticas consolidadas
-----------------------------------
- valide cedo e falhe de forma clara e alta: um erro silencioso hoje é um
  bug muito mais caro (e difícil de rastrear) amanhã;
- mensagens de erro devem orientar sobre O QUE FAZER a seguir, não apenas
  descrever o que deu errado — "arquivo de configuração não encontrado em
  /etc/app/config.json; copie o modelo de config.example.json" é mais útil
  do que apenas "FileNotFoundError";
- use `finally`, ou melhor ainda, gerenciadores de contexto (`with`, tema do
  Dia 22) para garantir a liberação de recursos, mesmo diante de erro;
- registre erros com o módulo `logging` (Dia 25) em código de produção, não
  com `print()` — logging permite níveis de severidade, redirecionamento
  para arquivos e muito mais controle sobre o que é registrado e onde.
""",
    exemplos=[
        Exemplo(
            titulo="Leitura robusta de configuração",
            codigo='''import json

def carregar_config(caminho, padrao=None):
    padrao = padrao or {"tema": "claro"}
    try:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return padrao
    except json.JSONDecodeError as e:
        raise ValueError(f"config invalida em {caminho}: {e}") from e

print(carregar_config("/tmp/nao_existe.json"))
''',
            explicacao="Cada tipo de falha tem um tratamento próprio e "
                       "explícito; nada é engolido em silêncio, e o segundo "
                       "except preserva a causa original com 'from e'.",
        ),
        Exemplo(
            titulo="Exceção própria carregando dados úteis",
            codigo='''class SaldoInsuficiente(Exception):
    def __init__(self, saldo, valor):
        super().__init__(f"Saldo {saldo:.2f} insuficiente para {valor:.2f}")
        self.faltam = valor - saldo

try:
    raise SaldoInsuficiente(50, 120)
except SaldoInsuficiente as e:
    print(e)               # Saldo 50.00 insuficiente para 120.00
    print(e.faltam)        # 70
''',
            explicacao="Carregar dados extras na própria exceção (como "
                       "e.faltam) facilita muito o tratamento de quem a "
                       "captura, sem precisar reprocessar a mensagem de texto.",
        ),
        Exemplo(
            titulo="EAFP evitando uma condição de corrida",
            codigo='''from pathlib import Path

def ler_com_seguranca(caminho):
    # LBYL (arriscado): o arquivo pode sumir ENTRE o exists() e o read_text()
    # if Path(caminho).exists():
    #     return Path(caminho).read_text(encoding="utf-8")

    # EAFP (preferido): tenta direto, trata a falha se ela realmente ocorrer
    try:
        return Path(caminho).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None

print(ler_com_seguranca("/tmp/talvez_exista.txt"))
''',
            explicacao="Na versão comentada (LBYL), outro processo poderia "
                       "apagar o arquivo bem no intervalo entre a checagem e "
                       "a leitura — o EAFP fecha essa janela de risco.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d15e1",
            enunciado=(
                "Escreva divisao_segura(a, b) devolvendo o resultado da divisão\n"
                "ou None se o divisor for zero (use try/except, não if)."
            ),
            funcao="divisao_segura",
            assinatura="def divisao_segura(a, b):",
            testes=[
                ("divisao_segura(10, 2)", "5.0"),
                ("divisao_segura(1, 0)", "None"),
                ("divisao_segura(-9, 3)", "-3.0"),
            ],
            dica="except ZeroDivisionError: return None",
        ),
        Exercicio(
            id="d15e2",
            enunciado=(
                "Escreva para_int(texto, padrao=0): converte para inteiro e devolve\n"
                "`padrao` se a conversão falhar (por valor inválido ou tipo errado)."
            ),
            funcao="para_int",
            assinatura="def para_int(texto, padrao=0):",
            testes=[
                ("para_int('42')", "42"),
                ("para_int('abc')", "0"),
                ("para_int(None, -1)", "-1"),
                ("para_int('  7  ')", "7"),
            ],
            nivel="medio",
            dica="Capture (ValueError, TypeError) em um único except.",
        ),
        Exercicio(
            id="d15e3",
            enunciado=(
                "Crie a exceção SaldoInsuficiente(Exception) e a função\n"
                "sacar(saldo, valor) que devolve o novo saldo, mas levanta\n"
                "SaldoInsuficiente se valor > saldo e ValueError se valor <= 0."
            ),
            funcao="sacar",
            assinatura="class SaldoInsuficiente(Exception):\n    pass\n\n\ndef sacar(saldo, valor):",
            testes=[
                ("sacar(100, 30)", "70"),
                ("sacar(100, 500)", "!raise SaldoInsuficiente"),
                ("sacar(100, 0)", "!raise ValueError"),
                ("sacar(100, 100)", "0"),
            ],
            nivel="dificil",
            dica="Valide primeiro o valor (ValueError), depois o saldo, e por fim retorne.",
        ),
    ],
    quiz=[
        Quiz("Quando o bloco `else` de um try executa?",
             ["Sempre", "Quando ocorre exceção", "Quando NÃO ocorre exceção", "No lugar de finally"], 2,
             "else roda apenas no caminho em que nenhum erro aconteceu dentro do try."),
        Quiz("Por que `except:` puro (sem especificar o tipo) é considerado ruim?",
             ["É mais lento de executar", "Captura até KeyboardInterrupt e SystemExit, escondendo até o Ctrl+C",
              "Não é sintaxe válida em Python", "Só funciona dentro de funções"], 1,
             "Ele engole absolutamente tudo, incluindo sinais que deveriam poder interromper o programa."),
        Quiz("Por que o estilo EAFP é geralmente preferido a LBYL em Python?",
             ["Porque LBYL não é suportado pela linguagem", "Porque evita condições de corrida e costuma ser mais rápido no caminho sem erros",
              "Porque EAFP nunca levanta exceções", "Não há preferência real, é só estilo pessoal"], 1,
             "Checar e agir em dois passos separados (LBYL) deixa uma janela de tempo onde o estado pode mudar entre a checagem e a ação."),
        Quiz("Por que assert não deve ser usado para validar entrada de usuário?",
             ["assert é mais lento que if", "Instruções assert são REMOVIDAS quando o Python roda com a flag -O",
              "assert só funciona com números", "assert sempre levanta ValueError, nunca AssertionError"], 1,
             "Se o programa rodar otimizado (-O), todo assert desaparece silenciosamente — inadequado para validação que precisa sempre ocorrer."),
    ],
    projeto=(
        "Refaça a calculadora do Dia 11 tornando-a à prova de falhas: entradas não numéricas, "
        "divisão por zero e Ctrl+C tratados, com mensagens claras e uma exceção própria "
        "OperacaoInvalida que herda de uma classe base ErroDeCalculadora."
    ),
    leitura=["docs.python.org/pt-br/3/tutorial/errors.html", "docs.python.org/pt-br/3/library/exceptions.html#exception-hierarchy"],
))
