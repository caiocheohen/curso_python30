"""Semana 2 - Dias 9 a 15: estruturas de dados, funções, módulos, arquivos e erros."""

from nucleo.modelos import Dia, Exemplo, Exercicio, Quiz

DIAS = []

# ---------------------------------------------------------------- DIA 9
DIAS.append(Dia(
    numero=9,
    titulo="Dicionários e conjuntos",
    nivel="Iniciante",
    duracao="80 min",
    objetivos=[
        "Criar, acessar e percorrer dicionários com segurança",
        "Usar get, setdefault, update e desempacotamento com **",
        "Aplicar conjuntos para deduplicação e operações matemáticas",
        "Escolher a estrutura certa para cada problema",
    ],
    teoria="""
1. Dicionário: mapeamento chave -> valor
----------------------------------------
    aluno = {"nome": "Ana", "nota": 9.5, "aprovado": True}
    aluno["nome"]          -> 'Ana'
    aluno["curso"]         -> KeyError
    aluno.get("curso")     -> None            (não levanta erro)
    aluno.get("curso", "-") -> '-'            (valor padrão)

Chaves precisam ser HASHÁVEIS (imutáveis): str, int, float, bool, tuple.
Listas e dicionários não podem ser chave. Desde o Python 3.7 a ordem de
inserção é preservada.

2. Modificação
--------------
    aluno["nota"] = 10                 # cria ou atualiza
    aluno.update({"nota": 8, "cpf": 1})
    aluno.pop("cpf")                   # remove e devolve
    aluno.pop("nada", None)            # sem erro
    del aluno["nota"]
    aluno.setdefault("faltas", 0)      # só cria se não existir

3. Percorrendo
--------------
    for chave in aluno: ...              # itera as CHAVES
    for chave, valor in aluno.items(): ...
    for valor in aluno.values(): ...
    "nome" in aluno                     # testa a chave (rápido, O(1))

4. Padrão contador
------------------
    contagem = {}
    for palavra in texto.split():
        contagem[palavra] = contagem.get(palavra, 0) + 1

Versão pronta da biblioteca padrão:
    from collections import Counter
    Counter(texto.split()).most_common(3)

E para agrupar:
    from collections import defaultdict
    grupos = defaultdict(list)
    grupos[chave].append(item)

5. Mesclagem
------------
    a = {"x": 1}; b = {"y": 2}
    juntos = {**a, **b}        # qualquer versão 3.5+
    juntos = a | b             # 3.9+
    a |= b                     # atualiza a no lugar

6. Conjunto (set): coleção sem ordem e sem repetição
----------------------------------------------------
    s = {1, 2, 3}
    vazio = set()              # {} é dicionário vazio!
    set([1, 1, 2])             -> {1, 2}

Operações:
    a | b   união
    a & b   interseção
    a - b   diferença
    a ^ b   diferença simétrica
    a <= b  subconjunto

Métodos: .add(), .discard() (não erra), .remove() (erra), .update()

`x in conjunto` é O(1), contra O(n) em lista — trocar lista por set em buscas
repetidas é a otimização mais barata que existe.

frozenset é a versão imutável, que pode ser chave de dicionário.

7. Qual estrutura usar?
-----------------------
    lista   ordem importa, permite repetição, acesso por posição
    tupla   registro fixo, imutável, pode ser chave
    dict    busca por identificador, dados associados
    set     pertencimento, unicidade, operações de conjunto
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
            explicacao="setdefault cria a lista na primeira vez e reaproveita depois.",
        ),
        Exemplo(
            titulo="Conjuntos para comparar cadastros",
            codigo='''antigos = {"ana", "bia", "caio"}
novos = {"bia", "caio", "davi"}
print("sairam:", antigos - novos)      # {'ana'}
print("entraram:", novos - antigos)    # {'davi'}
print("ficaram:", antigos & novos)     # {'bia', 'caio'}
''',
            explicacao="Três linhas resolvem o que exigiria laços aninhados com listas.",
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
             "Listas são mutáveis, logo não hasháveis."),
        Quiz("O que cria um conjunto vazio?",
             ["{}", "set()", "[]", "()"], 1,
             "{} cria um dicionário vazio."),
    ],
    projeto=(
        "Faça agenda.py: dicionário nome -> telefone, com menu para adicionar, buscar, "
        "remover e listar em ordem alfabética, salvando tudo em memória."
    ),
    leitura=["docs.python.org/pt-br/3/library/collections.html"],
))

# ---------------------------------------------------------------- DIA 10
DIAS.append(Dia(
    numero=10,
    titulo="Compreensões de lista, dicionário e conjunto",
    nivel="Iniciante",
    duracao="70 min",
    objetivos=[
        "Traduzir laços em compreensões",
        "Filtrar e transformar em uma única expressão",
        "Usar compreensões aninhadas com cuidado",
        "Diferenciar compreensão de expressão geradora",
    ],
    teoria="""
1. A forma geral
----------------
    [ EXPRESSÃO for ITEM in ITERÁVEL if CONDIÇÃO ]

Equivale a:

    resultado = []
    for ITEM in ITERÁVEL:
        if CONDIÇÃO:
            resultado.append(EXPRESSÃO)

Exemplos:
    [x * x for x in range(6)]                 -> [0, 1, 4, 9, 16, 25]
    [x for x in range(20) if x % 3 == 0]      -> [0, 3, 6, 9, 12, 15, 18]
    [p.upper() for p in palavras if len(p) > 3]

2. if/else na EXPRESSÃO
-----------------------
Quando você quer transformar (não filtrar), o ternário vai ANTES do for:

    ["par" if x % 2 == 0 else "impar" for x in range(4)]
Filtrar -> `if` no fim. Escolher valor -> ternário no começo.

3. Dicionário e conjunto
------------------------
    {p: len(p) for p in palavras}
    {p.lower() for p in palavras}                  # set, sem repetição
    {v: k for k, v in dicionario.items()}          # inverter

4. Aninhamento
--------------
Leia na mesma ordem em que escreveria os laços:

    [ (i, j) for i in range(3) for j in range(2) ]
    # for i ... : for j ... : append((i, j))

Achatar matriz:
    [x for linha in matriz for x in linha]

Construir matriz (repare nos colchetes internos):
    [[0] * 3 for _ in range(3)]

Transpor:
    [[linha[c] for linha in m] for c in range(len(m[0]))]

5. Expressão geradora
---------------------
Trocando [] por (), nada é construído na memória: os valores saem sob demanda.

    sum(x * x for x in range(1_000_000))    # não cria a lista
    any(p.startswith("a") for p in palavras)
    max((len(p) for p in palavras), default=0)

Regra prática: se você só vai CONSUMIR o resultado uma vez, use gerador.

6. Quando NÃO usar compreensão
------------------------------
- quando precisa de efeito colateral (print, gravar arquivo): use for normal;
- quando o resultado passa de ~2 linhas ou tem 3+ níveis de aninhamento;
- quando o `if` fica com múltiplas condições longas.

Legibilidade > concisão. Uma compreensão que precisa ser decifrada é pior que
um laço explícito.
""",
    exemplos=[
        Exemplo(
            titulo="Limpeza de dados em uma linha",
            codigo='''bruto = [" ana ", "", "  BIA", "carla ", "   "]
nomes = [n.strip().title() for n in bruto if n.strip()]
print(nomes)     # ['Ana', 'Bia', 'Carla']
''',
            explicacao="Filtra vazios e normaliza ao mesmo tempo.",
        ),
        Exemplo(
            titulo="Compreensão de dicionário com filtro",
            codigo='''estoque = {"caneta": 0, "papel": 12, "cola": 3}
disponiveis = {p: q for p, q in estoque.items() if q > 0}
print(disponiveis)      # {'papel': 12, 'cola': 3}
''',
            explicacao="Mesma sintaxe, chaves em vez de colchetes.",
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
             "Parênteses criam expressão geradora, avaliada sob demanda."),
        Quiz("Onde vai o if quando você quer FILTRAR elementos?",
             ["Antes do for", "Depois do for", "Dentro da expressão", "Não é possível"], 1,
             "Filtro vai no final; ternário (if/else) vai no começo."),
    ],
    projeto=(
        "Refaça o analisador de texto do Dia 4 usando apenas compreensões: "
        "palavras únicas, frequência, palavras com mais de 5 letras e tamanho médio."
    ),
    leitura=["docs.python.org/pt-br/3/tutorial/datastructures.html#list-comprehensions"],
))

# ---------------------------------------------------------------- DIA 11
DIAS.append(Dia(
    numero=11,
    titulo="Funções: parâmetros, escopo e boas práticas",
    nivel="Intermediário",
    duracao="90 min",
    objetivos=[
        "Dominar parâmetros posicionais, nomeados e padrão",
        "Usar *args e **kwargs",
        "Entender escopo LEGB, global e nonlocal",
        "Escrever docstrings úteis",
    ],
    teoria="""
1. Definição e retorno
----------------------
    def area_retangulo(base, altura):
        \"\"\"Devolve a área de um retângulo.\"\"\"
        return base * altura

- `return` encerra a função imediatamente.
- Sem return (ou com return sozinho), devolve None.
- É possível devolver vários valores — na verdade uma tupla:
      def divmod2(a, b):
          return a // b, a % b
      q, r = divmod2(7, 2)

2. Argumentos
-------------
    def cadastrar(nome, idade=18, ativo=True): ...

    cadastrar("Ana")                       # posicional
    cadastrar("Ana", 30)
    cadastrar(idade=30, nome="Ana")        # nomeados, ordem livre
Parâmetros com valor padrão vêm sempre DEPOIS dos obrigatórios.

3. A armadilha do padrão mutável
--------------------------------
    def add(item, lista=[]):      # ERRADO
        lista.append(item)
        return lista
    add(1); add(2)                # [1, 2] — a lista é criada UMA vez!

Correto:
    def add(item, lista=None):
        if lista is None:
            lista = []
        lista.append(item)
        return lista

4. *args e **kwargs
-------------------
    def somar(*numeros):              # tupla com os posicionais extras
        return sum(numeros)

    def config(**opcoes):             # dicionário com os nomeados extras
        return opcoes

    somar(1, 2, 3)                    # 6
    config(cor="azul", tamanho=10)    # {'cor': 'azul', 'tamanho': 10}

Na CHAMADA, * e ** desempacotam:
    valores = [1, 2, 3]; somar(*valores)
    dados = {"nome": "Ana"}; cadastrar(**dados)

Restrições de assinatura:
    def f(a, b, /, c, *, d):   # a,b só posicionais; d só nomeado
        ...

5. Escopo LEGB
--------------
Python procura um nome nesta ordem: Local -> Enclosing -> Global -> Builtins.

    x = "global"
    def externa():
        x = "enclosing"
        def interna():
            print(x)      # enclosing
        interna()

Atribuir dentro da função cria uma variável LOCAL, a menos que você declare:
    global x       # altera a variável de módulo
    nonlocal x     # altera a da função externa (closures)

Use global o mínimo possível: funções que dependem de estado externo são
difíceis de testar.

6. Passagem de argumentos
-------------------------
Python passa REFERÊNCIAS a objetos. Reatribuir dentro da função não afeta o
chamador; MUTAR o objeto afeta:

    def f(lista, numero):
        lista.append(1)   # visível fora
        numero += 1       # invisível fora (int é imutável)

7. Docstring
------------
    def calcular_juros(principal, taxa, meses):
        \"\"\"Calcula juros compostos.

        Args:
            principal: valor inicial em reais.
            taxa: taxa mensal em decimal (0.01 = 1%).
            meses: número de períodos.

        Returns:
            O montante final arredondado em 2 casas.
        \"\"\"

Uma função bem escrita: faz UMA coisa, tem nome verbal, poucos parâmetros
(idealmente até 4) e não imprime nada — quem decide como exibir é quem chama.
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
            explicacao="largura e alinhar são keyword-only por virem depois de *linhas.",
        ),
        Exemplo(
            titulo="Escopo em ação",
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
            explicacao="nonlocal permite que a função interna altere o estado da externa.",
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
             ["É mais lento", "O padrão é criado uma única vez e persiste entre chamadas",
              "Não é permitido", "Só funciona com números"], 1,
             "Use None como sentinela e crie a lista dentro."),
        Quiz("O que **kwargs recebe?",
             ["Uma lista", "Uma tupla dos extras posicionais",
              "Um dicionário dos argumentos nomeados extras", "Uma string"], 2,
             "* junta posicionais em tupla; ** junta nomeados em dicionário."),
    ],
    projeto=(
        "Crie calculadora.py com funções puras (somar, subtrair, multiplicar, dividir "
        "com tratamento de zero, potencia) e um menu que as chama por um dicionário de despacho."
    ),
    leitura=["PEP 257 - Docstring Conventions"],
))

# ---------------------------------------------------------------- DIA 12
DIAS.append(Dia(
    numero=12,
    titulo="Funções de alta ordem, lambda e recursão",
    nivel="Intermediário",
    duracao="90 min",
    objetivos=[
        "Passar funções como argumento e devolvê-las",
        "Usar lambda com sorted, map e filter",
        "Escrever funções recursivas com caso base correto",
        "Entender closures",
    ],
    teoria="""
1. Funções são objetos de primeira classe
-----------------------------------------
Podem ser atribuídas, passadas e devolvidas:

    def dobrar(x): return x * 2
    f = dobrar          # sem parênteses: referência à função
    f(5)                # 10
    print(dobrar.__name__, dobrar.__doc__)

Função de alta ordem = recebe e/ou devolve função.

2. lambda
---------
Função anônima de UMA expressão:

    quadrado = lambda x: x ** 2          # evite atribuir: use def
    sorted(pessoas, key=lambda p: p["idade"])

Use lambda apenas como argumento curto e descartável. Se precisa de nome,
condicional complexa ou mais de uma linha, use def.

3. map, filter, sorted, reduce
------------------------------
    list(map(str.upper, ["a", "b"]))            -> ['A', 'B']
    list(filter(lambda x: x > 0, [-1, 2]))      -> [2]
    sorted(dados, key=len, reverse=True)
    from functools import reduce
    reduce(lambda a, b: a * b, [1, 2, 3, 4])    -> 24

Em Python idiomático, compreensões costumam ser preferidas a map/filter:
    [x.upper() for x in nomes]      # em vez de map
    [x for x in nums if x > 0]      # em vez de filter
map/filter brilham quando a função já existe e é passada por nome.

Auxiliares úteis:
    from operator import itemgetter, attrgetter
    sorted(registros, key=itemgetter("nota"))

4. Closure
----------
Função interna que "lembra" o ambiente onde foi criada:

    def multiplicador(fator):
        def aplicar(x):
            return x * fator     # fator vem do escopo externo
        return aplicar

    triplo = multiplicador(3)
    triplo(10)      # 30

Closures são a base dos decoradores (Dia 21).

5. Recursão
-----------
Toda recursão precisa de:
  (a) caso base — quando parar;
  (b) passo que se aproxima do caso base.

    def fatorial(n):
        if n <= 1:            # caso base
            return 1
        return n * fatorial(n - 1)

    def soma_lista(lista):
        if not lista:
            return 0
        return lista[0] + soma_lista(lista[1:])

Limite padrão de profundidade: 1000 chamadas
(`sys.setrecursionlimit` ajusta, mas raramente é a solução certa).
Python NÃO otimiza chamada de cauda: para percorrer coleções grandes, use
iteração. Recursão brilha em estruturas naturalmente recursivas: árvores,
JSON aninhado, sistemas de arquivos, backtracking.

6. Divisão e conquista
----------------------
    def busca_binaria(lista, alvo, inicio=0, fim=None):
        if fim is None:
            fim = len(lista) - 1
        if inicio > fim:
            return -1
        meio = (inicio + fim) // 2
        if lista[meio] == alvo:
            return meio
        if lista[meio] < alvo:
            return busca_binaria(lista, alvo, meio + 1, fim)
        return busca_binaria(lista, alvo, inicio, meio - 1)
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
            explicacao="Sinal negativo inverte apenas o critério numérico.",
        ),
        Exemplo(
            titulo="Recursão em estrutura aninhada",
            codigo='''def somar_tudo(dados):
    total = 0
    for item in dados:
        if isinstance(item, list):
            total += somar_tudo(item)     # desce um nivel
        else:
            total += item
    return total

print(somar_tudo([1, [2, [3, [4]], 5]]))   # 15
''',
            explicacao="A recursão acompanha a forma dos dados.",
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
             "Sem caso base (ou sem se aproximar dele) a pilha estoura."),
        Quiz("Qual é o uso mais apropriado de lambda?",
             ["Substituir todas as funções", "Como argumento curto de sorted/map/filter",
              "Para escrever classes", "Para laços"], 1,
             "lambda é para expressões curtas e descartáveis."),
    ],
    projeto=(
        "Crie pipeline.py: uma lista de funções de transformação de texto (minúsculas, "
        "remover acentos, trocar espaço por hífen) aplicadas em sequência por uma função aplicar_todas()."
    ),
    leitura=["docs.python.org/pt-br/3/howto/functional.html"],
))

# ---------------------------------------------------------------- DIA 13
DIAS.append(Dia(
    numero=13,
    titulo="Módulos, pacotes, venv e pip no Linux",
    nivel="Intermediário",
    duracao="80 min",
    objetivos=[
        "Organizar código em módulos e pacotes",
        "Entender import, from-import e __name__",
        "Criar e usar ambientes virtuais",
        "Conhecer módulos essenciais da biblioteca padrão",
    ],
    teoria="""
1. Módulo é um arquivo .py
--------------------------
    # matematica.py
    PI = 3.14159
    def area_circulo(r):
        return PI * r ** 2

    # main.py
    import matematica
    matematica.area_circulo(2)

    from matematica import area_circulo, PI
    import matematica as mat
    from matematica import *          # EVITE: polui o namespace

2. O bloco __main__
-------------------
Quando um arquivo é executado diretamente, `__name__ == "__main__"`. Quando é
importado, `__name__` vira o nome do módulo. Por isso:

    def principal():
        ...

    if __name__ == "__main__":
        principal()

Isso permite que o arquivo seja usado tanto como script quanto como biblioteca
— sem executar nada indesejado no import.

3. Pacote é uma pasta com módulos
---------------------------------
    meu_projeto/
        __init__.py          (pode ser vazio; marca o pacote)
        modelos.py
        utils/
            __init__.py
            texto.py

    from meu_projeto.utils.texto import limpar

Imports relativos, dentro do pacote:
    from . import modelos
    from ..utils.texto import limpar
Só funcionam dentro de pacotes importados, não em scripts soltos.

4. Onde o Python procura módulos
--------------------------------
    import sys; print(sys.path)
Ordem: diretório do script, PYTHONPATH, bibliotecas do sistema/venv.
Nunca dê a um arquivo seu o nome de um módulo padrão (random.py, json.py,
email.py): ele sombreia o original e gera erros bizarros.

5. Ambiente virtual (essencial no Linux)
----------------------------------------
    python3 -m venv .venv           # cria a pasta .venv
    source .venv/bin/activate       # ativa (bash/zsh)
    pip install requests
    pip freeze > requirements.txt
    pip install -r requirements.txt
    deactivate

Por que usar? Para não misturar dependências de projetos diferentes nem
poluir o Python do sistema (em muitas distros, `pip install` global é
bloqueado por padrão — PEP 668). Adicione `.venv/` ao .gitignore.

6. Biblioteca padrão que vale conhecer hoje
-------------------------------------------
    math          sqrt, ceil, floor, pi, isclose, factorial
    random        random, randint, choice, sample, shuffle, seed
    datetime      date, datetime, timedelta
    pathlib       Path — manipulação moderna de caminhos
    os / sys      ambiente, variáveis, argumentos
    json / csv    formatos de dados
    collections   Counter, defaultdict, deque, namedtuple
    itertools     combinações, produtos, agrupamentos
    statistics    mean, median, stdev

Regra de ouro: antes de escrever algo do zero, procure na biblioteca padrão.

7. pathlib em 30 segundos
-------------------------
    from pathlib import Path
    p = Path("/home/usuario/dados/relatorio.csv")
    p.name      # 'relatorio.csv'
    p.stem      # 'relatorio'
    p.suffix    # '.csv'
    p.parent    # PosixPath('/home/usuario/dados')
    p.exists(), p.is_file(), p.is_dir()
    (Path.home() / "projetos" / "x.txt")     # o operador / monta caminhos
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
            explicacao="Rodar direto testa; importar só traz as funções.",
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
            explicacao="timedelta faz aritmética de datas sem dor de cabeça.",
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
             ["Definir a função principal", "Executar código só quando o arquivo roda diretamente",
              "Criar um módulo", "Importar bibliotecas"], 1,
             "Evita executar código de script durante o import."),
        Quiz("Qual comando cria um ambiente virtual?",
             ["pip venv", "python3 -m venv .venv", "virtualenv --pip", "python3 install venv"], 1,
             "O módulo venv já vem com o Python 3."),
    ],
    projeto=(
        "Transforme suas funções dos dias anteriores num pacote utilitarios/ com módulos "
        "texto.py, numeros.py e datas.py, e um main.py que importa e demonstra cada um."
    ),
    leitura=["docs.python.org/pt-br/3/tutorial/modules.html", "PEP 668"],
))

# ---------------------------------------------------------------- DIA 14
DIAS.append(Dia(
    numero=14,
    titulo="Arquivos, JSON e CSV",
    nivel="Intermediário",
    duracao="90 min",
    objetivos=[
        "Ler e escrever arquivos com with",
        "Escolher o modo correto de abertura e o encoding",
        "Serializar dados com json",
        "Processar tabelas com csv",
    ],
    teoria="""
1. Sempre use `with`
--------------------
    with open("dados.txt", "r", encoding="utf-8") as f:
        conteudo = f.read()
    # arquivo fechado automaticamente, mesmo se der erro

Modos:
    "r"   leitura (padrão) — erro se não existe
    "w"   escrita — CRIA ou APAGA o conteúdo existente
    "a"   append — escreve no final
    "x"   criação exclusiva — erro se já existe
    "r+"  leitura e escrita
    "rb"/"wb"  binário (imagens, zip) — sem encoding

Em Linux, sempre passe encoding="utf-8" explicitamente: o padrão depende do
locale da máquina e isso já quebrou muito código em produção.

2. Formas de ler
----------------
    f.read()             tudo em uma string
    f.readline()         uma linha
    f.readlines()        lista de linhas
    for linha in f:      MELHOR: streaming, não carrega tudo na memória

    for linha in f:
        linha = linha.rstrip("\\n")

3. Escrita
----------
    with open("saida.txt", "w", encoding="utf-8") as f:
        f.write("primeira linha\\n")       # write NÃO adiciona \\n
        f.writelines(["a\\n", "b\\n"])
        print("via print", file=f)         # print aceita file=

4. pathlib para tarefas simples
-------------------------------
    from pathlib import Path
    p = Path("nota.txt")
    p.write_text("conteudo", encoding="utf-8")
    texto = p.read_text(encoding="utf-8")
    p.unlink(missing_ok=True)              # apaga
    for arquivo in Path(".").glob("*.py"): ...
    for arquivo in Path(".").rglob("*.py"): ...   # recursivo

5. JSON
-------
    import json
    json.dumps(obj, ensure_ascii=False, indent=2)   # objeto -> string
    json.loads(texto)                               # string -> objeto
    json.dump(obj, arquivo)                         # direto no arquivo
    json.load(arquivo)

Mapeamento: dict<->object, list<->array, str, int/float, True/False<->true/false,
None<->null. Tuplas viram listas. datetime NÃO é serializável (use isoformat()
ou o parâmetro default=).

    json.dumps({"nome": "João"}, ensure_ascii=False)   # mantém acentos

6. CSV
------
    import csv
    with open("dados.csv", newline="", encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            print(linha["nome"], linha["nota"])     # valores são strings!

    with open("saida.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["nome", "nota"])
        w.writeheader()
        w.writerows(registros)

`newline=""` evita linhas em branco extras — é exigência do módulo csv.
Para separador diferente: csv.reader(f, delimiter=";").

7. Escrita segura
-----------------
Grave em arquivo temporário e renomeie ao final. `Path.replace()` é atômico no
mesmo sistema de arquivos, então você nunca fica com um arquivo pela metade
se o programa cair no meio da escrita.
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
            explicacao="Para arquivos pequenos, pathlib elimina o boilerplate.",
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
            explicacao="indent deixa legível; ensure_ascii=False preserva acentos.",
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
             ["Erro", "O conteúdo é apagado", "Escreve no final", "Abre só leitura"], 1,
             "'w' trunca o arquivo; para preservar, use 'a'."),
        Quiz("Por que usar `with open(...)`?",
             ["É mais rápido", "Fecha o arquivo automaticamente, mesmo com erro",
              "Permite JSON", "É obrigatório"], 1,
             "with garante a liberação do recurso."),
    ],
    projeto=(
        "Crie notas_csv.py: leia um CSV de alunos e notas, calcule a média de cada aluno, "
        "grave um novo CSV com a situação (aprovado/reprovado) e um resumo em JSON."
    ),
    leitura=["docs.python.org/pt-br/3/library/json.html", "docs.python.org/pt-br/3/library/csv.html"],
))

# ---------------------------------------------------------------- DIA 15
DIAS.append(Dia(
    numero=15,
    titulo="Erros e exceções",
    nivel="Intermediário",
    duracao="80 min",
    objetivos=[
        "Tratar erros com try/except/else/finally",
        "Capturar exceções específicas e usar a instância",
        "Criar exceções personalizadas",
        "Aplicar EAFP e falhar de forma explícita",
    ],
    teoria="""
1. Estrutura completa
---------------------
    try:
        valor = int(texto)
    except ValueError as e:
        print("conversao falhou:", e)
        valor = 0
    except (TypeError, KeyError):
        valor = -1
    else:
        print("deu certo, nenhum erro")     # só se NÃO houve exceção
    finally:
        print("sempre executa")             # limpeza, mesmo com return/raise

2. Hierarquia (resumo)
----------------------
    BaseException
     +- SystemExit, KeyboardInterrupt, GeneratorExit
     +- Exception
         +- ArithmeticError -> ZeroDivisionError
         +- LookupError     -> IndexError, KeyError
         +- OSError         -> FileNotFoundError, PermissionError
         +- ValueError, TypeError, AttributeError, NameError
         +- RuntimeError    -> RecursionError
         +- StopIteration

Capture sempre o MAIS ESPECÍFICO possível. `except Exception:` só na fronteira
do programa (para logar e sair com dignidade). NUNCA use `except:` puro — ele
engole até Ctrl+C.

Anti-padrão clássico:
    try:
        fazer_tudo()
    except Exception:
        pass                # o bug desaparece e você nunca descobre

3. Levantando erros
-------------------
    raise ValueError("idade nao pode ser negativa")
    raise                                    # re-levanta a exceção atual

Encadeamento (preserva a causa original no traceback):
    try:
        ...
    except KeyError as e:
        raise ConfiguracaoInvalida("falta a chave") from e

4. Exceções personalizadas
--------------------------
    class ErroDeNegocio(Exception):
        \"\"\"Base para os erros da aplicação.\"\"\"

    class SaldoInsuficiente(ErroDeNegocio):
        def __init__(self, saldo, valor):
            super().__init__(f"saldo {saldo} < saque {valor}")
            self.saldo = saldo
            self.valor = valor

Uma base própria permite que quem usa seu código escreva
`except ErroDeNegocio:` e pegue toda a família de uma vez.

5. EAFP x LBYL
--------------
Python prefere EAFP ("é mais fácil pedir perdão que permissão"):

    try:                            # EAFP
        return dados["chave"]
    except KeyError:
        return padrao

    if "chave" in dados:            # LBYL
        return dados["chave"]

EAFP evita condições de corrida (o arquivo pode sumir entre o teste e o uso) e
costuma ser mais rápido no caminho feliz.

6. assert não é validação
-------------------------
`assert` some quando o Python roda com -O. Use para checagem interna de
invariantes durante o desenvolvimento, nunca para validar entrada de usuário.

7. Boas práticas
----------------
- valide cedo, falhe alto: erro silencioso vira bug caro;
- mensagens de erro devem dizer o que fazer, não só o que houve;
- use `finally` ou context managers (Dia 22) para liberar recursos;
- registre com o módulo `logging` (Dia 25), não com print.
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
            explicacao="Cada falha tem tratamento próprio; nada é engolido em silêncio.",
        ),
        Exemplo(
            titulo="Exceção própria com dados",
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
            explicacao="Carregar dados na exceção facilita o tratamento de quem captura.",
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
             "else roda apenas no caminho sem erros."),
        Quiz("Por que `except:` puro é ruim?",
             ["É lento", "Captura até KeyboardInterrupt e SystemExit, escondendo problemas",
              "Não é válido", "Só funciona em funções"], 1,
             "Ele engole tudo, inclusive sinais de saída do programa."),
    ],
    projeto=(
        "Refaça a calculadora do Dia 11 tornando-a à prova de falhas: entradas não numéricas, "
        "divisão por zero e Ctrl+C tratados, com mensagens claras e uma exceção própria OperacaoInvalida."
    ),
    leitura=["docs.python.org/pt-br/3/tutorial/errors.html"],
))