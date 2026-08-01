"""Semana 2 - Dias 9 a 15: estruturas de dados, funções, módulos, arquivos e erros."""

from nucleo.modelos import Dia, Exemplo, Exercicio, Quiz

DIAS = []

# ---------------------------------------------------------------- DIA 9
DIAS.append(Dia(
    numero=9,
    titulo="Dicionários e conjuntos",
    nivel="Iniciante",
    duracao="100 min",
    objetivos=[
        "Entender quando usar dicionário em vez de lista e o que os diferencia",
        "Criar, acessar, modificar e percorrer dicionários com segurança",
        "Usar get(), setdefault(), update() e pop() corretamente",
        "Aplicar o padrão de contador e agrupador com dicionários",
        "Usar conjuntos para eliminar duplicatas e realizar operações matemáticas de conjunto",
        "Escolher a estrutura de dados certa para cada situação: lista, tupla, dict ou set",
    ],
    teoria="""
Você já conhece listas (acesso por posição numérica) e tuplas (registros
imutáveis). Hoje vamos conhecer duas estruturas novas que resolvem
problemas completamente diferentes: dicionários e conjuntos.

---------------------------------------------------------------------------
1. Por que dicionário? O problema que ele resolve
---------------------------------------------------------------------------
Imagine que você tem uma lista de alunos e quer buscar a nota de "Carlos".
Com uma lista, você precisaria percorrer elemento por elemento até achar.
Com um dicionário, você acessa diretamente pelo nome:

    # Com lista: lento e trabalhoso
    alunos = [("Ana", 9.5), ("Bruno", 7.0), ("Carlos", 8.2)]
    for nome, nota in alunos:
        if nome == "Carlos":
            print(nota)

    # Com dicionário: direto e rápido
    notas = {"Ana": 9.5, "Bruno": 7.0, "Carlos": 8.2}
    print(notas["Carlos"])    # 8.2  — acesso instantâneo

Um dicionário é um mapeamento de CHAVE para VALOR. Em vez de buscar
por posição (índice), você busca por um IDENTIFICADOR que você escolhe.

Pense como um dicionário de verdade: você não percorre da página 1 até
achar a palavra — você vai direto à letra e encontra a definição.

---------------------------------------------------------------------------
2. Criando e acessando dicionários
---------------------------------------------------------------------------
Criando um dicionário:

    # Forma literal (mais comum)
    pessoa = {
        "nome": "Ana",
        "idade": 30,
        "cidade": "Recife",
    }

    # Dicionário vazio
    vazio = {}

    # Com dict() e pares chave=valor
    config = dict(tema="escuro", fonte=14, largura=1920)

Acessando valores:

    pessoa["nome"]      # "Ana"   — acesso direto pela chave
    pessoa["cpf"]       # KeyError: 'cpf' — chave não existe!

O problema de acessar uma chave que não existe:

    # ERRADO: levanta KeyError se a chave não existir
    valor = dicionario["chave_que_pode_nao_existir"]

    # CORRETO: get() devolve None se a chave não existir
    valor = dicionario.get("chave_que_pode_nao_existir")

    # MELHOR: get() com valor padrão explícito
    valor = dicionario.get("chave_que_pode_nao_existir", 0)

Quando usar [] vs get():
    [] — quando a ausência da chave seria um BUG (você quer que o
         programa pare e informe o erro)
    get() — quando a ausência é uma situação normal e esperada

---------------------------------------------------------------------------
3. Modificando dicionários
---------------------------------------------------------------------------

    Operação                          O que faz
    -----------------------------     ----------------------------------------
    d["chave"] = valor                cria ou atualiza a chave
    d.update({"a": 1, "b": 2})        atualiza múltiplas chaves de uma vez
    d.update(outro_dict)              mescla outro_dict em d
    d.pop("chave")                    remove e DEVOLVE o valor
    d.pop("chave", padrao)            remove, ou devolve padrao se não existir
    del d["chave"]                    remove sem devolver (KeyError se não existir)
    d.setdefault("chave", valor)      cria a chave SOMENTE se ela não existir
    d.clear()                         remove todos os pares

Exemplos práticos:

    config = {"tema": "claro", "fonte": 12}

    config["lingua"] = "pt-BR"         # adiciona nova chave
    config["fonte"] = 14               # atualiza valor existente
    config.update({"tema": "escuro", "zoom": 1.5})  # atualiza vários

    removido = config.pop("zoom")      # removido = 1.5
    print(removido)                    # 1.5

    # setdefault: cria APENAS se não existir
    config.setdefault("salvar_auto", True)   # cria com True
    config.setdefault("tema", "rosa")        # NÃO altera: já existe

MESCLANDO DICIONÁRIOS (Python 3.9+):

    a = {"x": 1, "y": 2}
    b = {"y": 20, "z": 3}

    c = a | b           # novo dicionário: {"x": 1, "y": 20, "z": 3}
    a |= b              # atualiza a no lugar

    # Em versões anteriores:
    c = {**a, **b}      # desempacotamento: mesma lógica

Em caso de chave repetida, o valor do dicionário mais à DIREITA prevalece.

---------------------------------------------------------------------------
4. Percorrendo dicionários
---------------------------------------------------------------------------
Existem três formas de percorrer um dicionário, cada uma servindo a um
propósito diferente:

    pessoa = {"nome": "Ana", "idade": 30, "cidade": "Recife"}

    # 1. Percorre as CHAVES (padrão quando você itera direto)
    for chave in pessoa:
        print(chave)        # nome  idade  cidade

    # 2. Percorre os PARES chave-valor (mais comum)
    for chave, valor in pessoa.items():
        print(chave, "->", valor)

    # 3. Percorre apenas os VALORES
    for valor in pessoa.values():
        print(valor)        # Ana  30  Recife

    # Verificando se uma chave existe
    "nome" in pessoa        # True   — O(1), muito rápido
    "cpf" in pessoa         # False

    # Verificando se um valor existe (mais lento)
    "Ana" in pessoa.values()  # True   — O(n), percorre todos

IMPORTANTE: desde o Python 3.7, dicionários PRESERVAM a ordem de
inserção. Se você inseriu "nome" antes de "idade", eles aparecem nessa
ordem ao percorrer. Isso era um detalhe de implementação antes — hoje
é garantia da linguagem.

---------------------------------------------------------------------------
5. O padrão contador: contando ocorrências
---------------------------------------------------------------------------
Um dos usos mais comuns de dicionário é contar quantas vezes algo aparece:

    # Jeito manual com get()
    texto = "banana"
    contagem = {}
    for letra in texto:
        contagem[letra] = contagem.get(letra, 0) + 1
    print(contagem)    # {'b': 1, 'a': 3, 'n': 2}

    # Como funciona o get com padrão:
    # Primeira vez que "b" aparece: contagem.get("b", 0) = 0, então guarda 1
    # Segunda vez que "a" aparece: contagem.get("a", 0) = 1, então guarda 2

Esse padrão é tão comum que a biblioteca padrão tem uma versão pronta:

    from collections import Counter
    contagem = Counter("banana")
    print(contagem)                    # Counter({'a': 3, 'n': 2, 'b': 1})
    print(contagem.most_common(2))    # [('a', 3), ('n', 2)]

---------------------------------------------------------------------------
6. O padrão agrupador: agrupando por categoria
---------------------------------------------------------------------------
Outro padrão muito comum: agrupar itens por uma característica:

    # Com setdefault
    palavras = ["ana", "bia", "ary", "bob", "caio"]
    grupos = {}
    for p in palavras:
        grupos.setdefault(p[0], []).append(p)
    print(grupos)
    # {'a': ['ana', 'ary'], 'b': ['bia', 'bob'], 'c': ['caio']}

    # Como funciona:
    # setdefault("a", []) cria grupos["a"] = [] na primeira vez que "a" aparece
    # Nas vezes seguintes, só devolve a lista já existente para o append

    # Com defaultdict (mais limpo)
    from collections import defaultdict
    grupos = defaultdict(list)          # toda chave nova começa como []
    for p in palavras:
        grupos[p[0]].append(p)          # não precisa de setdefault

---------------------------------------------------------------------------
7. Conjuntos (set): quando a ordem não importa e duplicatas não existem
---------------------------------------------------------------------------
Um conjunto é uma coleção DESORDENADA de elementos ÚNICOS. Cada elemento
aparece no máximo uma vez, e não há garantia de ordem.

    # Criando conjuntos
    frutas = {"maçã", "banana", "uva"}
    numeros = {1, 2, 3, 2, 1}        # duplicatas são ignoradas automaticamente
    print(numeros)                    # {1, 2, 3}

    # ATENÇÃO: {} cria um dicionário VAZIO, não um conjunto!
    vazio_dict = {}           # dicionário
    vazio_set = set()         # conjunto vazio — use set(), não {}

    # Convertendo lista para set elimina duplicatas
    lista = [1, 2, 3, 2, 1, 4]
    unicos = set(lista)       # {1, 2, 3, 4}
    sem_dup = list(set(lista)) # de volta para lista, sem duplicatas

OPERAÇÕES MATEMÁTICAS DE CONJUNTO:

    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}

    Operacao         Simbolo    Resultado         O que significa
    ----------------  -------   ----------------  ----------------------
    a | b            uniao      {1,2,3,4,5,6}     tudo que esta em a OU b
    a & b            intersecao {3, 4}             tudo que esta em a E b
    a - b            diferenca  {1, 2}             esta em a mas NAO em b
    b - a            diferenca  {5, 6}             esta em b mas NAO em a
    a ^ b            sim. dif.  {1,2,5,6}          esta em um mas nao em ambos

Métodos de conjunto:

    s = {1, 2, 3}
    s.add(4)              # {1, 2, 3, 4}
    s.discard(2)          # {1, 3, 4} — sem erro se não existir
    s.remove(3)           # {1, 4}    — KeyError se não existir
    s.update([5, 6])      # {1, 4, 5, 6}
    3 in s                # False — O(1), muito mais rápido que em lista!

O SUPERPODER DO SET: verificação de pertencimento em O(1):

    lista_grande = list(range(1_000_000))
    set_grande = set(lista_grande)

    999_999 in lista_grande  # lento: percorre até 1 milhão de elementos
    999_999 in set_grande    # instantâneo: cálculo de hash direto

Quando usar set em vez de lista:
    - Você só precisa saber SE algo existe (não onde)
    - Você quer eliminar duplicatas
    - Você vai fazer operações de conjunto (união, interseção...)

---------------------------------------------------------------------------
8. Qual estrutura usar? Guia de decisão
---------------------------------------------------------------------------

    Estrutura    Quando usar
    ----------   -----------------------------------------------------------
    lista        ordem importa, duplicatas permitidas, acesso por posição
    tupla        registro fixo e imutável, chave de dicionário
    dicionário   busca por identificador (nome, CPF, código), mapeamento
    conjunto     pertencimento rápido, sem duplicatas, operações de conjunto

Pergunta chave: "Vou buscar por posição ou por conteúdo?"
    Por posição (índice numérico) → lista ou tupla
    Por conteúdo (chave) → dicionário ou conjunto
""",
    exemplos=[
        Exemplo(
            titulo="Padrões contador e agrupador",
            codigo='''from collections import Counter, defaultdict

# PADRAO CONTADOR: manual
texto = "mississippi"
contagem = {}
for letra in texto:
    contagem[letra] = contagem.get(letra, 0) + 1
print("Manual:", contagem)

# PADRAO CONTADOR: com Counter
c = Counter(texto)
print("Counter:", dict(c))
print("Mais comuns:", c.most_common(3))

# PADRAO AGRUPADOR: agrupando palavras por inicial
palavras = ["abacate", "banana", "amora", "blueberry", "caju", "acai"]

# Com setdefault
grupos1 = {}
for p in palavras:
    grupos1.setdefault(p[0], []).append(p)

# Com defaultdict
grupos2 = defaultdict(list)
for p in palavras:
    grupos2[p[0]].append(p)

print("\nGrupos:", dict(grupos1))
''',
            explicacao="Counter e defaultdict resolvem os dois padrões mais "
                       "comuns de dicionário sem precisar verificar se a "
                       "chave existe a cada passo. "
                       "Counter conta automaticamente; defaultdict cria a "
                       "lista vazia automaticamente na primeira vez "
                       "que uma nova chave é acessada.",
        ),
        Exemplo(
            titulo="Operações de conjunto na prática",
            codigo='''# Comparando dois cadastros de usuarios
sistema_a = {"ana", "bruno", "carla", "diego"}
sistema_b = {"bruno", "carla", "elena", "fabio"}

# Quem esta nos dois sistemas?
em_ambos = sistema_a & sistema_b
print("Em ambos:", em_ambos)        # {'bruno', 'carla'}

# Quem esta so no sistema A?
so_em_a = sistema_a - sistema_b
print("So em A:", so_em_a)          # {'ana', 'diego'}

# Quem esta em qualquer um?
em_algum = sistema_a | sistema_b
print("Em algum:", em_algum)        # todos os 6

# Quem esta em exatamente um (nao nos dois)?
exclusivos = sistema_a ^ sistema_b
print("Exclusivos:", exclusivos)    # {'ana', 'diego', 'elena', 'fabio'}

# Eliminando duplicatas de uma lista
notas = [9, 7, 9, 8, 7, 10, 8]
print("\nNotas unicas:", sorted(set(notas)))    # [7, 8, 9, 10]
''',
            explicacao="Operações de conjunto resolvem em uma linha o que "
                       "com listas exigiria dois for aninhados. "
                       "O resultado de operações entre sets não tem ordem "
                       "garantida — use sorted() se precisar de ordem. "
                       "set() para eliminar duplicatas e depois sorted() "
                       "para ordenar é um padrão muito comum.",
        ),
        Exemplo(
            titulo="Dicionário como estrutura de dados rica",
            codigo='''# Simulando um pequeno banco de dados de produtos
catalogo = {}

def adicionar_produto(codigo, nome, preco, estoque):
    catalogo[codigo] = {
        "nome": nome,
        "preco": preco,
        "estoque": estoque,
    }

adicionar_produto("A001", "Caneta Azul", 2.50, 100)
adicionar_produto("A002", "Caderno", 15.90, 30)
adicionar_produto("A003", "Borracha", 1.20, 200)

# Consultando
print(catalogo.get("A001"))   # o produto inteiro
print(catalogo.get("A999"))   # None — nao existe

# Relatorio de estoque baixo
print("\nEstoque baixo (< 50):")
for codigo, produto in catalogo.items():
    if produto["estoque"] < 50:
        print(f"  {codigo}: {produto['nome']} ({produto['estoque']} unidades)")

# Total de produtos em estoque
total = sum(p["estoque"] for p in catalogo.values())
print(f"\nTotal de itens em estoque: {total}")
''',
            explicacao="Dicionários aninhados (dicionário de dicionários) "
                       "são a forma mais natural de representar registros "
                       "estruturados em Python, antes de usar classes. "
                       "catalogo.items() percorre pares (codigo, produto), "
                       "onde produto é outro dicionário.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d09e1",
            enunciado=(
                "Escreva a funcao contar_letras(texto) que conta quantas\n"
                "vezes cada letra aparece no texto, ignorando espacos e\n"
                "sem distinguir maiusculas de minusculas.\n\n"
                "Exemplos:\n"
                "   contar_letras('aba')  -> {'a': 2, 'b': 1}\n"
                "   contar_letras('A a')  -> {'a': 2}  (espaco ignorado)\n"
                "   contar_letras('')     -> {}\n\n"
                "Estrategia:\n"
                "   1. Crie um dicionario vazio: contagem = {}\n"
                "   2. Para cada letra no texto:\n"
                "      a. Converta para minuscula: letra = letra.lower()\n"
                "      b. Se for espaco, pule com continue\n"
                "      c. contagem[letra] = contagem.get(letra, 0) + 1\n"
                "   3. Devolva contagem\n\n"
                "Como get(letra, 0) funciona:\n"
                "   Se 'a' nao estiver no dict: get devolve 0, entao guardamos 1\n"
                "   Se 'a' ja estiver: get devolve o valor atual, somamos 1"
            ),
            funcao="contar_letras",
            assinatura="def contar_letras(texto):",
            testes=[
                ("contar_letras('aba')", "{'a': 2, 'b': 1}"),
                ("contar_letras('A a')", "{'a': 2}"),
                ("contar_letras('')", "{}"),
            ],
            dica="for letra in texto: letra = letra.lower(); if letra == ' ': continue; contagem[letra] = contagem.get(letra, 0) + 1",
        ),
        Exercicio(
            id="d09e2",
            enunciado=(
                "Escreva a funcao inverter_dicionario(d) que troca chaves\n"
                "por valores e valores por chaves.\n\n"
                "Exemplos:\n"
                "   inverter_dicionario({'a': 1, 'b': 2}) -> {1: 'a', 2: 'b'}\n"
                "   inverter_dicionario({})               -> {}\n\n"
                "Estrategia:\n"
                "   1. Crie um dicionario vazio: invertido = {}\n"
                "   2. Percorra os pares com d.items():\n"
                "      for chave, valor in d.items():\n"
                "          invertido[valor] = chave\n"
                "   3. Devolva invertido\n\n"
                "Nota: isso assume que todos os valores do dicionario\n"
                "original sao unicos e hashaveis (podem ser chaves).\n"
                "Se houver valores repetidos, o ultimo prevalece."
            ),
            funcao="inverter_dicionario",
            assinatura="def inverter_dicionario(d):",
            testes=[
                ("inverter_dicionario({'a': 1, 'b': 2})", "{1: 'a', 2: 'b'}"),
                ("inverter_dicionario({})", "{}"),
            ],
            dica="invertido = {}; for chave, valor in d.items(): invertido[valor] = chave; return invertido",
        ),
        Exercicio(
            id="d09e3",
            enunciado=(
                "Escreva a funcao comuns(a, b) que devolve uma lista\n"
                "ORDENADA com os elementos que aparecem em AMBAS as listas,\n"
                "sem repeticoes.\n\n"
                "Exemplos:\n"
                "   comuns([1, 2, 3, 3], [3, 2, 9]) -> [2, 3]\n"
                "   comuns([], [1])                  -> []\n"
                "   comuns(['b', 'a'], ['a', 'b'])   -> ['a', 'b']\n\n"
                "Estrategia com conjuntos:\n"
                "   1. Converta a para set: set_a = set(a)\n"
                "      Isso elimina duplicatas E permite operacao de intersecao\n"
                "   2. Converta b para set: set_b = set(b)\n"
                "   3. Calcule a intersecao: set_a & set_b\n"
                "      Intersecao = elementos que estao nos DOIS conjuntos\n"
                "   4. Converta para lista ordenada: sorted(...)\n\n"
                "Em uma linha: return sorted(set(a) & set(b))"
            ),
            funcao="comuns",
            assinatura="def comuns(a, b):",
            testes=[
                ("comuns([1, 2, 3, 3], [3, 2, 9])", "[2, 3]"),
                ("comuns([], [1])", "[]"),
                ("comuns(['b', 'a'], ['a', 'b'])", "['a', 'b']"),
            ],
            nivel="medio",
            dica="return sorted(set(a) & set(b))",
        ),
    ],
    quiz=[
        Quiz(
            "Qual a diferenca entre dict['chave'] e dict.get('chave')?",
            ["Nao ha diferenca — os dois fazem a mesma coisa",
             "dict['chave'] levanta KeyError se a chave nao existir; get() devolve None (ou um padrao)",
             "get() e mais lento que o acesso por colchetes",
             "dict['chave'] so funciona com chaves numericas"],
            1,
            "Use [] quando a ausencia da chave seria um bug — voce quer "
            "o erro para descobrir o problema. "
            "Use get() quando a ausencia e esperada e voce quer um valor padrao. "
            "get('chave', 0) e muito util para o padrao contador.",
        ),
        Quiz(
            "Por que {} nao cria um conjunto vazio em Python?",
            ["E um bug que nunca foi corrigido",
             "Porque {} ja pertencia aos dicionarios quando conjuntos foram adicionados — use set()",
             "Porque conjuntos nao podem ser vazios",
             "{} cria um conjunto sim — isso e incorreto"],
            1,
            "Quando conjuntos foram adicionados ao Python, {} ja era a sintaxe "
            "de dicionarios. Para nao quebrar codigo existente, definiram "
            "{1, 2, 3} para conjuntos com elementos e set() para conjunto vazio. "
            "Nunca use {} sozinho esperando um conjunto.",
        ),
        Quiz(
            "Por que 'x in conjunto' e muito mais rapido que 'x in lista'?",
            ["Conjuntos sao sempre menores que listas",
             "Conjuntos usam hashing para localizar o elemento diretamente em O(1); listas percorrem elemento a elemento em O(n)",
             "O Python otimiza automaticamente a busca em listas quando sao grandes",
             "Nao ha diferenca de velocidade entre os dois"],
            1,
            "set usa uma tabela hash: calcula hash(x) para saber exatamente "
            "onde procurar, sem precisar verificar outros elementos. "
            "Com 1 milhao de elementos, set e instantaneo; "
            "lista pode verificar 1 milhao antes de concluir que nao existe.",
        ),
        Quiz(
            "O que setdefault('chave', valor_padrao) faz?",
            ["Sempre sobrescreve o valor da chave com valor_padrao",
             "Cria a chave com valor_padrao APENAS se ela nao existir ainda; se existir, nao altera nada",
             "Devolve valor_padrao sem modificar o dicionario",
             "Remove a chave se ela existir"],
            1,
            "setdefault e como 'crie se nao existir'. "
            "Se 'chave' ja tem um valor, setdefault o preserva e devolve ele. "
            "Se 'chave' nao existe, cria com valor_padrao e devolve valor_padrao. "
            "Muito util no padrao agrupador: setdefault(key, []).append(item)",
        ),
    ],
    projeto=(
        "Crie analisador_texto.py que receba um texto longo (pode ser\n"
        "hardcoded, como uma frase famosa ou paragrafo de livro) e exiba:\n\n"
        "   1. Frequencia de cada letra (ignorando espacos e pontuacao)\n"
        "   2. As 5 letras mais comuns (Counter.most_common)\n"
        "   3. Frequencia de cada palavra (case-insensitive)\n"
        "   4. As 5 palavras mais comuns\n"
        "   5. Quantas palavras UNICAS existem (use set)\n"
        "   6. Palavras que aparecem apenas uma vez\n\n"
        "Exiba os resultados como um relatorio formatado com f-strings.\n\n"
        "BONUS: compare dois textos diferentes e mostre:\n"
        "   - Palavras que aparecem em AMBOS os textos\n"
        "   - Palavras exclusivas de cada texto\n"
        "   usando operacoes de conjunto sobre os vocabularios."
    ),
    leitura=[
        "docs.python.org/pt-br/3/tutorial/datastructures.html#dictionaries",
        "docs.python.org/pt-br/3/library/collections.html — Counter e defaultdict",
        "docs.python.org/pt-br/3/tutorial/datastructures.html#sets",
    ],
))

# ---------------------------------------------------------------- DIA 10
DIAS.append(Dia(
    numero=10,
    titulo="Compreensões de lista, dicionário e conjunto",
    nivel="Iniciante",
    duracao="90 min",
    objetivos=[
        "Traduzir um laço for explícito para uma compreensão de lista, e vice-versa",
        "Filtrar e transformar dados em uma única expressão legível",
        "Entender a diferença entre o if de filtro e o if/else ternário dentro de compreensões",
        "Escrever compreensões de dicionário e de conjunto",
        "Usar compreensões aninhadas com consciência do momento em que deixam de ser legíveis",
        "Diferenciar compreensão de lista (ávida) de expressão geradora (preguiçosa)",
        "Reconhecer quando um for tradicional é mais claro do que uma compreensão",
    ],
    teoria="""
Nos Dias 7, 8 e 9 você escreveu muitos laços com o mesmo padrão:
criar uma lista vazia, percorrer algo com for e ir adicionando elementos
com append. Esse padrão é tão comum que Python tem uma sintaxe especial
para ele, mais compacta e expressiva: as compreensões.

---------------------------------------------------------------------------
1. O problema que as compreensões resolvem
---------------------------------------------------------------------------
Compare os dois códigos abaixo — eles fazem exatamente a mesma coisa:

    # Forma tradicional com for (4 linhas)
    quadrados = []
    for x in range(10):
        quadrados.append(x ** 2)

    # Forma com compreensão de lista (1 linha)
    quadrados = [x ** 2 for x in range(10)]

A compreensão não é apenas mais curta. Ela é mais clara porque lê quase
como inglês: "a lista dos x ao quadrado, para cada x em range(10)".
O padrão de 4 linhas tem "ruído" — a criação da lista vazia e o append
existem por obrigação da sintaxe, não por lógica do problema.

---------------------------------------------------------------------------
2. A estrutura completa de uma compreensão de lista
---------------------------------------------------------------------------
A forma geral é:

    [EXPRESSÃO for ITEM in ITERÁVEL if CONDIÇÃO]

Onde:
    EXPRESSÃO  — o que colocar na lista para cada item (pode usar o item)
    for ITEM in ITERÁVEL — percorre cada elemento do iterável
    if CONDIÇÃO — (opcional) filtra: só inclui se a condição for True

Exemplos progressivos:

    # Só a expressão e o for (sem filtro)
    [x for x in range(5)]          # [0, 1, 2, 3, 4]
    [x * 2 for x in range(5)]      # [0, 2, 4, 6, 8]
    [x ** 2 for x in range(5)]     # [0, 1, 4, 9, 16]

    # Com filtro (if no final)
    [x for x in range(10) if x % 2 == 0]     # [0, 2, 4, 6, 8]
    [x ** 2 for x in range(10) if x % 2 == 0] # [0, 4, 16, 36, 64]

    # Com strings
    frutas = ["maçã", "banana", "kiwi", "uva"]
    [f.upper() for f in frutas]                # ['MAÇÃ', 'BANANA', 'KIWI', 'UVA']
    [f for f in frutas if len(f) > 4]          # ['maçã', 'banana']

---------------------------------------------------------------------------
3. if de filtro versus if/else ternário: posições diferentes, papéis diferentes
---------------------------------------------------------------------------
Esta é a parte que mais confunde quem está aprendendo compreensões.
Existem dois usos diferentes do if, e cada um fica em um lugar diferente:

USO 1 — Filtro (if no FINAL): REMOVE elementos que não satisfazem a condição

    [x for x in range(10) if x % 2 == 0]
    # Resultado: [0, 2, 4, 6, 8]
    # Elementos ímpares foram REMOVIDOS da lista

    Posição: DEPOIS do for
    Efeito: a lista resultante tem MENOS elementos que o iterável original
    O if não tem else aqui — ou inclui ou descarta

USO 2 — Ternário (if/else no INÍCIO): TRANSFORMA cada elemento

    ["par" if x % 2 == 0 else "impar" for x in range(5)]
    # Resultado: ['par', 'impar', 'par', 'impar', 'par']
    # TODOS os elementos estão presentes, mas transformados

    Posição: ANTES do for, entre a expressão e o for
    Efeito: a lista resultante tem o MESMO número de elementos
    O if SEMPRE tem else aqui — todo elemento gera um valor

Comparação lado a lado:

    lista = [1, 2, 3, 4, 5, 6]

    # Filtro: só os pares (lista menor)
    [x for x in lista if x % 2 == 0]
    # [2, 4, 6]

    # Ternário: rotula cada um (lista igual)
    [x if x % 2 == 0 else -x for x in lista]
    # [x negativo para ímpares: -1, 2, -3, 4, -5, 6]

Regra para não confundir:
    if no FINAL  →  filtra (elimina elementos)
    if no INÍCIO →  ternário (transforma todos)

---------------------------------------------------------------------------
4. Compreensão de dicionário
---------------------------------------------------------------------------
A mesma ideia, mas com chave: valor em vez de só valor, e chaves {} em
vez de colchetes []:

    {CHAVE: VALOR for ITEM in ITERÁVEL if CONDIÇÃO}

Exemplos:

    # Palavra -> comprimento
    palavras = ["maçã", "banana", "kiwi"]
    {p: len(p) for p in palavras}
    # {'maçã': 4, 'banana': 6, 'kiwi': 4}

    # Número -> quadrado (só pares)
    {x: x**2 for x in range(10) if x % 2 == 0}
    # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

    # Invertendo um dicionário (chaves viram valores e vice-versa)
    original = {"a": 1, "b": 2, "c": 3}
    {v: k for k, v in original.items()}
    # {1: 'a', 2: 'b', 3: 'c'}

    # Filtrando itens do estoque com valor acima de 10
    estoque = {"caneta": 2.50, "caderno": 15.90, "régua": 8.75}
    {item: preco for item, preco in estoque.items() if preco > 10}
    # {'caderno': 15.90}

---------------------------------------------------------------------------
5. Compreensão de conjunto
---------------------------------------------------------------------------
Igual à de lista, mas com {} e sem duplicatas:

    {EXPRESSÃO for ITEM in ITERÁVEL if CONDIÇÃO}

    # Letras únicas de uma palavra (sem repetição, sem ordem garantida)
    {"banana"}                    # não é compreensão, é um conjunto literal
    {letra for letra in "banana"} # {'b', 'a', 'n'} — cada letra uma vez

    # Comprimentos únicos das palavras
    palavras = ["maçã", "kiwi", "banana", "uva", "pera"]
    {len(p) for p in palavras}
    # {3, 4, 6} — sem duplicatas, sem ordem garantida

    # Iniciais únicas
    nomes = ["Ana", "Bruno", "Alice", "Carlos", "Bia"]
    {nome[0] for nome in nomes}
    # {'A', 'B', 'C'}

---------------------------------------------------------------------------
6. Compreensões aninhadas: for dentro de for
---------------------------------------------------------------------------
Você pode ter mais de um for em uma compreensão. A ordem é a mesma
que você escreveria com laços aninhados tradicionais:

    # For aninhado tradicional
    pares = []
    for i in range(3):
        for j in range(3):
            pares.append((i, j))

    # Equivalente com compreensão
    pares = [(i, j) for i in range(3) for j in range(3)]
    # [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

ACHATANDO UMA MATRIZ (lista de listas em lista simples):

    matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    # Forma tradicional
    plana = []
    for linha in matriz:
        for elemento in linha:
            plana.append(elemento)

    # Com compreensão
    plana = [elemento for linha in matriz for elemento in linha]
    # [1, 2, 3, 4, 5, 6, 7, 8, 9]

TRANSPONDO UMA MATRIZ (linhas viram colunas):

    # [[1,2,3],     ->    [[1,4],
    #  [4,5,6]]            [2,5],
    #                      [3,6]]

    transposta = [[linha[c] for linha in matriz] for c in range(len(matriz[0]))]

    Leitura da compreensão externa para a interna:
    "Para cada coluna c em range(número de colunas):
        cria uma lista com o elemento da coluna c de cada linha"

LIMITES DE LEGIBILIDADE:
Compreensões aninhadas ficam difíceis de ler rapidamente. Uma boa
heurística: se você precisar reler mais de uma vez para entender, use
o for tradicional.

    # Legível: achatar
    [x for linha in matriz for x in linha]

    # No limite: transpor (ainda ok com comentário)
    [[linha[c] for linha in m] for c in range(len(m[0]))]

    # Não use: três níveis de aninhamento
    [x for a in b for c in a for x in c]  # difícil de ler

---------------------------------------------------------------------------
7. Expressão geradora: a compreensão preguiçosa
---------------------------------------------------------------------------
Trocando os colchetes por parênteses, você cria uma EXPRESSÃO GERADORA
em vez de uma lista. A diferença fundamental: a lista calcula e guarda
TODOS os valores imediatamente; o gerador calcula um por vez, sob demanda.

    # Lista: calcula tudo agora, guarda na memória
    lista = [x ** 2 for x in range(1_000_000)]    # 8 MB na memória

    # Gerador: calcula sob demanda, ocupa quase nada
    gerador = (x ** 2 for x in range(1_000_000))  # ~100 bytes

    # Ambos produzem o mesmo resultado quando consumidos
    sum(lista)      # funciona
    sum(gerador)    # funciona, e usa bem menos memória

Quando usar gerador em vez de lista:
    - Você só vai percorrer uma vez
    - Está passando direto para uma função como sum(), any(), all()
    - O iterável é muito grande e não quer guardar tudo na memória

    # Forma compacta ao passar para funções (parênteses fundidos)
    sum(x ** 2 for x in range(10))    # não precisa de colchetes extras

LIMITAÇÃO: geradores se esgotam. Depois de percorrido uma vez, não
produzem mais nada. Se precisar percorrer mais de uma vez, use lista.

    g = (x for x in range(3))
    list(g)    # [0, 1, 2]
    list(g)    # []  — já foi consumido!

---------------------------------------------------------------------------
8. Quando NÃO usar compreensão
---------------------------------------------------------------------------
Compreensões são ótimas para CONSTRUIR coleções. Evite usá-las para:

EFEITOS COLATERAIS (imprimir, gravar, enviar):

    # ERRADO: compreensão só para efeito colateral
    [print(x) for x in lista]   # funciona, mas é má prática

    # CORRETO: use for quando o objetivo é o efeito, não a lista
    for x in lista:
        print(x)

LÓGICA COMPLEXA (mais de 2-3 condições):

    # Quando a compreensão fica difícil de ler, use for
    # [x for x in dados if condicao1 and condicao2 and condicao3]
    resultado = []
    for x in dados:
        if condicao1 and condicao2 and condicao3:
            resultado.append(x)

A regra final é sempre legibilidade: uma compreensão que você precisa
reler várias vezes para entender é pior do que um for de 4 linhas claro.
""",
    exemplos=[
        Exemplo(
            titulo="Limpando dados reais com compreensão",
            codigo='''# Simulando dados bagunçados vindos de um formulario
entradas = ["  Ana ", "", "BRUNO", "  ", "carla", None, "DIEGO  "]

# Forma tradicional (6 linhas)
nomes_trad = []
for e in entradas:
    if e and e.strip():
        nomes_trad.append(e.strip().title())

# Com compreensao (1 linha)
nomes = [e.strip().title() for e in entradas if e and e.strip()]

print(nomes)   # ['Ana', 'Bruno', 'Carla', 'Diego']

# Filtrando e transformando numeros
valores = [1, -3, 5, -2, 0, 8, -1, 4]

positivos = [v for v in valores if v > 0]      # [1, 5, 8, 4]
absolutos = [abs(v) for v in valores]           # [1, 3, 5, 2, 0, 8, 1, 4]
rotulados = ["pos" if v > 0 else "neg" if v < 0 else "zero"
             for v in valores]
print(rotulados)   # ['pos', 'neg', 'pos', 'neg', 'zero', 'pos', 'neg', 'pos']
''',
            explicacao="O filtro 'if e and e.strip()' verifica duas coisas: "
                       "e not None/vazio (primeiro 'e') E a string "
                       "não é só espaços (segundo 'e.strip()'). "
                       "O ternário encadeado 'pos/neg/zero' funciona mas "
                       "está no limite da legibilidade — para mais condições "
                       "use if/elif tradicional.",
        ),
        Exemplo(
            titulo="Compreensões de dicionário e conjunto",
            codigo='''# Compreensao de dicionario: inventario de letras
palavra = "abracadabra"
freq = {letra: palavra.count(letra) for letra in set(palavra)}
print(freq)    # {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}

# Filtrando dicionario: so quem passou
notas = {"Ana": 9.5, "Bruno": 4.5, "Carla": 7.0, "Diego": 5.9}
aprovados = {nome: nota for nome, nota in notas.items() if nota >= 6.0}
print(aprovados)   # {'Ana': 9.5, 'Carla': 7.0}

# Normalizando chaves de um dicionario
dados_brutos = {"Nome": "Ana", "IDADE": 30, "Cidade": "Recife"}
normalizado = {k.lower(): v for k, v in dados_brutos.items()}
print(normalizado)  # {'nome': 'Ana', 'idade': 30, 'cidade': 'Recife'}

# Compreensao de conjunto: iniciais unicas
nomes = ["Ana", "Bruno", "Alice", "Carlos", "Beatriz", "Andre"]
iniciais = {nome[0] for nome in nomes}
print(sorted(iniciais))    # ['A', 'B', 'C']
''',
            explicacao="A compreensão de frequência usa set(palavra) para "
                       "percorrer cada letra única uma vez — mais eficiente "
                       "do que usar Counter, e mostra como compreensão e "
                       "conjunto se complementam. "
                       "Normalizar chaves de dicionário é um caso de uso "
                       "muito comum ao receber dados de APIs externas.",
        ),
        Exemplo(
            titulo="Gerador versus lista: quando a memória importa",
            codigo='''import sys

# Compreensao de lista: tudo na memoria de uma vez
lista = [x ** 2 for x in range(100_000)]
print(f"Lista:   {sys.getsizeof(lista):>10,} bytes")

# Expressao geradora: quase nada na memoria
gerador = (x ** 2 for x in range(100_000))
print(f"Gerador: {sys.getsizeof(gerador):>10,} bytes")

# Ambos produzem o mesmo resultado
soma_lista = sum(lista)
soma_gerador = sum(x ** 2 for x in range(100_000))
print(f"Resultados iguais: {soma_lista == soma_gerador}")

# Gerador se esgota!
g = (x for x in range(3))
print(list(g))    # [0, 1, 2]
print(list(g))    # []  — ja foi consumido

# Quando usar cada um:
# Lista   -> precisa usar mais de uma vez, acessar por indice, saber o len
# Gerador -> so percorre uma vez, passa direto para sum/any/all/max
''',
            explicacao="A diferença de memória é dramática: a lista com "
                       "100 mil elementos ocupa centenas de KB; o gerador "
                       "ocupa menos de 200 bytes independente do tamanho. "
                       "O truque 'sum(x**2 for x in range(n))' usa o "
                       "gerador diretamente sem criar lista intermediária.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d10e1",
            enunciado=(
                "Escreva a funcao quadrados_pares(n) que devolve, usando\n"
                "compreensao de lista, os quadrados dos numeros PARES\n"
                "de 0 ate n-1.\n\n"
                "Exemplos:\n"
                "   quadrados_pares(7) -> [0, 4, 16, 36]\n"
                "      (pares de 0 a 6: 0,2,4,6 -> quadrados: 0,4,16,36)\n"
                "   quadrados_pares(1) -> [0]\n"
                "      (so o 0 cabe em range(1), e 0 e par)\n"
                "   quadrados_pares(0) -> []\n"
                "      (range(0) e vazio, nenhum elemento)\n\n"
                "Estrutura da compreensao:\n"
                "   [x*x for x in range(n) if x % 2 == 0]\n\n"
                "Leitura: 'a lista de x ao quadrado, para cada x em\n"
                "range(n), somente se x for par (resto da divisao por 2 = 0)'"
            ),
            funcao="quadrados_pares",
            assinatura="def quadrados_pares(n):",
            testes=[
                ("quadrados_pares(7)", "[0, 4, 16, 36]"),
                ("quadrados_pares(1)", "[0]"),
                ("quadrados_pares(0)", "[]"),
            ],
            dica="return [x*x for x in range(n) if x % 2 == 0]",
        ),
        Exercicio(
            id="d10e2",
            enunciado=(
                "Escreva agrupar_por_tamanho(palavras) que devolve um\n"
                "dicionario onde cada chave e um tamanho (int) e o valor\n"
                "e a lista de palavras daquele tamanho, na ordem de entrada.\n\n"
                "Exemplos:\n"
                "   agrupar_por_tamanho(['oi', 'ana', 'ai'])\n"
                "   -> {2: ['oi', 'ai'], 3: ['ana']}\n\n"
                "   agrupar_por_tamanho([]) -> {}\n\n"
                "Estrategia com for e setdefault (mais legivel aqui):\n"
                "   grupos = {}\n"
                "   for p in palavras:\n"
                "       grupos.setdefault(len(p), []).append(p)\n"
                "   return grupos\n\n"
                "Por que setdefault(len(p), [])?\n"
                "   - Na primeira palavra de 2 letras: cria grupos[2] = []\n"
                "   - Nas seguintes: apenas devolve a lista ja existente\n"
                "   - .append(p) adiciona a palavra a essa lista"
            ),
            funcao="agrupar_por_tamanho",
            assinatura="def agrupar_por_tamanho(palavras):",
            testes=[
                ("agrupar_por_tamanho(['oi', 'ana', 'ai'])",
                 "{2: ['oi', 'ai'], 3: ['ana']}"),
                ("agrupar_por_tamanho([])", "{}"),
            ],
            nivel="medio",
            dica="grupos = {}; for p in palavras: grupos.setdefault(len(p), []).append(p); return grupos",
        ),
        Exercicio(
            id="d10e3",
            enunciado=(
                "Escreva transposta(matriz) que devolve a transposta\n"
                "de uma matriz (listas de listas): linhas viram colunas.\n\n"
                "Exemplos:\n"
                "   transposta([[1,2,3],[4,5,6]])\n"
                "   -> [[1,4],[2,5],[3,6]]\n\n"
                "   Visualizando:\n"
                "   [[1, 2, 3],       [[1, 4],\n"
                "    [4, 5, 6]]  ->    [2, 5],\n"
                "                      [3, 6]]\n\n"
                "   transposta([[1]])  -> [[1]]\n"
                "   transposta([])     -> []\n\n"
                "Estrategia:\n"
                "   1. Trate o caso vazio: if not matriz: return []\n"
                "   2. Use compreensao aninhada:\n"
                "      [[linha[c] for linha in matriz]\n"
                "       for c in range(len(matriz[0]))]\n\n"
                "   Leitura: 'para cada coluna c, cria uma lista com\n"
                "   o elemento da coluna c de cada linha'"
            ),
            funcao="transposta",
            assinatura="def transposta(matriz):",
            testes=[
                ("transposta([[1, 2, 3], [4, 5, 6]])", "[[1, 4], [2, 5], [3, 6]]"),
                ("transposta([[1]])", "[[1]]"),
                ("transposta([])", "[]"),
            ],
            nivel="dificil",
            dica="if not matriz: return []. Depois: [[linha[c] for linha in matriz] for c in range(len(matriz[0]))]",
        ),
    ],
    quiz=[
        Quiz(
            "Qual a diferenca entre [x for x in lista if x > 0] e [x if x > 0 else 0 for x in lista]?",
            ["Nao ha diferenca — os dois produzem o mesmo resultado",
             "O primeiro FILTRA (lista menor, so positivos); o segundo TRANSFORMA (lista igual, negativos viram 0)",
             "O primeiro e mais rapido que o segundo",
             "O segundo e invalido — if/else nao funciona dentro de compreensao"],
            1,
            "if no FINAL filtra: elementos que nao satisfazem sao REMOVIDOS da lista. "
            "if/else no INICIO e ternario: TODOS os elementos ficam, "
            "mas podem ser transformados. "
            "Resultado: filtro gera lista menor; ternario mantem o mesmo tamanho.",
        ),
        Quiz(
            "Quando uma expressao geradora (x for x in y) e preferivel a uma compreensao [x for x in y]?",
            ["Nunca — a lista e sempre mais util",
             "Quando os valores serao percorridos apenas uma vez e a lista seria muito grande para guardar na memoria",
             "Quando voce precisa acessar elementos por indice",
             "Quando o iteravel tem menos de 100 elementos"],
            1,
            "Gerador e preguicoso: calcula um item por vez, ocupa poucos bytes. "
            "Lista e avida: calcula e guarda tudo imediatamente. "
            "Use gerador quando passa direto para sum(), any(), all(), max() "
            "e nao precisa percorrer mais de uma vez.",
        ),
        Quiz(
            "O que {x for x in [1, 2, 2, 3, 1]} produz?",
            ["{1, 2, 2, 3, 1} — preserva duplicatas",
             "[1, 2, 3] — lista sem duplicatas",
             "{1, 2, 3} — conjunto sem duplicatas e sem ordem garantida",
             "Um erro — compreensao de conjunto nao existe"],
            2,
            "Compreensao com {} cria um SET, que nao admite duplicatas. "
            "Os valores 2 e 1 duplicados sao automaticamente descartados. "
            "A ordem nao e garantida em conjuntos, mas o conteudo sera {1, 2, 3}.",
        ),
        Quiz(
            "Por que usar [print(x) for x in lista] e considerado ma pratica?",
            ["print() nao funciona dentro de compreensoes",
             "Compreensoes existem para CONSTRUIR colecoes; usa-las so para efeitos colaterais cria uma lista de None desnecessaria",
             "E mais lento que um for tradicional",
             "Compreensoes nao aceitam funcoes como expressao"],
            1,
            "print() devolve None. A compreensao cria [None, None, None...] "
            "sem nenhuma utilidade, gastando memoria a toa. "
            "Para efeitos colaterais (imprimir, gravar, enviar), use for. "
            "Para construir colecoes, use compreensao.",
        ),
    ],
    projeto=(
        "Crie pipeline_dados.py que processe uma lista de registros de vendas:\n\n"
        "   vendas = [\n"
        "       {'produto': 'Caneta', 'valor': 2.50, 'qtd': 10, 'regiao': 'Norte'},\n"
        "       {'produto': 'Caderno', 'valor': 15.90, 'qtd': 3, 'regiao': 'Sul'},\n"
        "       {'produto': 'Borracha', 'valor': 1.20, 'qtd': 25, 'regiao': 'Norte'},\n"
        "       {'produto': 'Caneta', 'valor': 2.50, 'qtd': 5, 'regiao': 'Sul'},\n"
        "       {'produto': 'Regua', 'valor': 3.75, 'qtd': 8, 'regiao': 'Norte'},\n"
        "   ]\n\n"
        "Usando apenas compreensoes (sem for tradicional onde possivel):\n\n"
        "   1. Lista de totais por venda (valor * qtd)\n"
        "   2. Dicionario produto -> total faturado\n"
        "   3. Vendas da regiao Norte com total > 20\n"
        "   4. Conjunto de regioes distintas\n"
        "   5. Conjunto de produtos distintos\n"
        "   6. Total geral usando expressao geradora com sum()\n\n"
        "BONUS: use compreensao aninhada para criar uma tabela de\n"
        "produto x regiao com o total faturado em cada combinacao."
    ),
    leitura=[
        "docs.python.org/pt-br/3/tutorial/datastructures.html#list-comprehensions",
        "PEP 289 — Generator Expressions",
        "PEP 274 — Dict Comprehensions",
    ],
))

# ---------------------------------------------------------------- DIA 11
DIAS.append(Dia(
    numero=11,
    titulo="Funções: parâmetros, escopo e boas práticas",
    nivel="Intermediário",
    duracao="110 min",
    objetivos=[
        "Entender o que é uma função e por que ela é a unidade fundamental de organização do código",
        "Dominar os quatro tipos de parâmetro: posicional, com padrão, *args e **kwargs",
        "Entender a regra LEGB de escopo e prever onde Python vai procurar cada nome",
        "Reconhecer e evitar a armadilha do argumento padrão mutável",
        "Diferenciar reatribuir um parâmetro de mutar o objeto que ele aponta",
        "Escrever docstrings úteis e funções com responsabilidade única",
    ],
    teoria="""
Desde o Dia 4 você já usa a sintaxe básica de funções para os exercícios.
Hoje vamos entender funções a fundo: como os parâmetros realmente funcionam,
onde o Python procura cada variável, e como escrever funções que sejam
fáceis de usar, testar e manter.

---------------------------------------------------------------------------
1. Por que funções existem?
---------------------------------------------------------------------------
Funções resolvem três problemas fundamentais em programação:

PROBLEMA 1 — REPETIÇÃO: sem funções, você copia e cola o mesmo código
várias vezes. Quando precisar corrigir um bug ou mudar o comportamento,
precisa encontrar e alterar todas as cópias.

PROBLEMA 2 — COMPLEXIDADE: um programa de 500 linhas em sequência é
impossível de entender. Funções permitem dar NOMES a pedaços de lógica,
tornando o código legível como uma lista de instruções em português.

PROBLEMA 3 — TESTABILIDADE: é muito mais fácil testar uma função isolada
do que testar um programa inteiro de uma vez.

A regra mais importante sobre funções:
UMA FUNÇÃO DEVE FAZER UMA COISA SÓ.

Se você precisar usar "e" para descrever o que uma função faz, ela
provavelmente está fazendo coisas demais:

    def calcular_e_imprimir(nota):  # faz duas coisas
        ...

    def calcular_media(notas):      # faz uma coisa
        ...
    def formatar_relatorio(media):  # faz uma coisa
        ...

---------------------------------------------------------------------------
2. Anatomia completa de uma função
---------------------------------------------------------------------------
    def calcular_desconto(preco, percentual=10, minimo=0.0):
        \"\"\"Calcula o preco com desconto aplicado.

        Args:
            preco: valor original em reais (deve ser positivo)
            percentual: percentual de desconto (0 a 100), padrao 10
            minimo: preco minimo apos desconto, padrao 0.0

        Returns:
            O preco final com desconto, nunca abaixo do minimo.
        \"\"\"
        if preco < 0:
            raise ValueError("preco nao pode ser negativo")
        desconto = preco * percentual / 100
        return max(preco - desconto, minimo)

Partes importantes:

    def        palavra-chave que define a função
    nome       verbo que descreve o que a função faz
    parâmetros dados que a função precisa para trabalhar
    docstring  documentação acessível via help()
    corpo      a lógica da função (indentado 4 espaços)
    return     o valor que a função entrega para quem a chamou

SOBRE O RETURN:
    - return encerra a função IMEDIATAMENTE
    - uma função sem return (ou com return sozinho) devolve None
    - você pode ter vários returns em caminhos diferentes
    - devolver múltiplos valores cria uma TUPLA automaticamente:

    def dividir(a, b):
        return a // b, a % b    # na verdade devolve a tupla (quociente, resto)

    q, r = dividir(10, 3)       # desempacotamento: q=3, r=1

---------------------------------------------------------------------------
3. Os quatro tipos de parâmetro
---------------------------------------------------------------------------

TIPO 1 — POSICIONAL: obrigatório, passado na ordem
    def somar(a, b):
        return a + b

    somar(3, 4)      # a=3, b=4
    somar(4, 3)      # a=4, b=3  (ordem importa!)

TIPO 2 — COM VALOR PADRÃO: opcional, usa o padrão se não for passado

    def saudar(nome, saudacao="Olá"):
        return f"{saudacao}, {nome}!"

    saudar("Ana")             # "Olá, Ana!"
    saudar("Ana", "Oi")       # "Oi, Ana!"
    saudar(nome="Ana")        # argumento nomeado — ordem não importa
    saudar(saudacao="Ei", nome="Bruno")  # nomeados podem vir em qualquer ordem

    REGRA DE SINTAXE: parâmetros com padrão devem vir DEPOIS
    dos obrigatórios:

    def f(a, b=1):    # correto
    def f(a=1, b):    # SyntaxError!

TIPO 3 — *args: captura argumentos posicionais extras como tupla

    def somar_tudo(*numeros):
        return sum(numeros)    # numeros é uma TUPLA

    somar_tudo(1, 2, 3)      # numeros = (1, 2, 3)
    somar_tudo(5)            # numeros = (5,)
    somar_tudo()             # numeros = ()

TIPO 4 — **kwargs: captura argumentos nomeados extras como dicionário

    def mostrar_info(**dados):
        for chave, valor in dados.items():
            print(f"{chave}: {valor}")

    mostrar_info(nome="Ana", idade=30, cidade="Recife")
    # dados = {'nome': 'Ana', 'idade': 30, 'cidade': 'Recife'}

COMBINANDO OS QUATRO (ordem obrigatória):

    def funcao(pos1, pos2, padrao=1, *args, **kwargs):
        pass

    Ordem: posicionais -> com padrão -> *args -> **kwargs

DESEMPACOTANDO NA CHAMADA (o inverso de *args/**kwargs):

    numeros = [1, 2, 3]
    somar_tudo(*numeros)     # equivale a somar_tudo(1, 2, 3)

    dados = {"nome": "Ana", "idade": 30}
    mostrar_info(**dados)    # equivale a mostrar_info(nome="Ana", idade=30)

---------------------------------------------------------------------------
4. A armadilha do argumento padrão mutável
---------------------------------------------------------------------------
Este é um dos bugs mais famosos do Python. Entender por que ele acontece
é fundamental para nunca cometê-lo:

    # ERRADO — parece inocente, mas é uma armadilha!
    def adicionar(item, lista=[]):
        lista.append(item)
        return lista

    print(adicionar("a"))    # ['a']
    print(adicionar("b"))    # ['a', 'b']  <- SURPRESA! devia ser ['b']
    print(adicionar("c"))    # ['a', 'b', 'c']  <- acumula entre chamadas!

POR QUÊ ACONTECE?
O valor padrão `[]` é criado UMA ÚNICA VEZ, quando a linha `def` é
executada (quando o arquivo é carregado), não a cada vez que a função
é chamada. Como listas são mutáveis, todas as chamadas sem argumento
compartilham a mesma lista, que vai acumulando.

Você pode verificar isso:

    print(adicionar.__defaults__)  # (['a', 'b', 'c'],) — a lista "padrão" acumulada

A SOLUÇÃO: use None como sentinela e crie o objeto mutável dentro da
função, a cada chamada:

    # CORRETO
    def adicionar(item, lista=None):
        if lista is None:
            lista = []       # nova lista a cada chamada sem argumento
        lista.append(item)
        return lista

    print(adicionar("a"))    # ['a']
    print(adicionar("b"))    # ['b']   <- correto!

REGRA: nunca use lista, dicionário ou conjunto como valor padrão.
Use None e crie o objeto dentro da função.

---------------------------------------------------------------------------
5. Como Python passa argumentos: reatribuir vs mutar
---------------------------------------------------------------------------
Python passa REFERÊNCIAS a objetos — nem cópia nem ponteiro no sentido
de C. Entender isso explica comportamentos que parecem inconsistentes:

    def tentar_mudar(numero, lista):
        numero = 999         # REATRIBUI: cria variável local, original intacto
        lista.append(999)    # MUTA o objeto: visível fora da função!

    n = 10
    l = [1, 2, 3]
    tentar_mudar(n, l)
    print(n)    # 10    — não mudou
    print(l)    # [1, 2, 3, 999]  — mudou!

Por quê?

    REATRIBUIR (numero = 999):
    Dentro da função, numero passa a apontar para 999.
    A variável n lá fora ainda aponta para 10. São coisas separadas.

    MUTAR (lista.append(999)):
    lista e l apontam para o MESMO objeto na memória.
    .append() modifica o objeto no lugar — quem quer que aponte para ele
    vê a mudança, incluindo o código que chamou a função.

RESUMO PRÁTICO:

    Tipos imutáveis (int, float, str, tuple):
    → A função nunca pode afetar o original.
    → Reatribuir dentro da função não tem efeito fora.

    Tipos mutáveis (list, dict, set, objetos):
    → A função PODE afetar o original se usar métodos de mutação.
    → Se você não quer afetar o original, passe uma cópia: lista[:]

---------------------------------------------------------------------------
6. Escopo LEGB: onde Python procura cada nome
---------------------------------------------------------------------------
Quando o Python encontra um nome (variável, função, classe) no código,
ele busca em quatro lugares em ordem, parando no primeiro onde encontrar:

    L — Local:     dentro da função atual
    E — Enclosing: funções que envolvem esta (funções aninhadas)
    G — Global:    no nível do módulo (o arquivo .py)
    B — Builtin:   funções embutidas (print, len, range...)

    x = "global"            # escopo G

    def externa():
        x = "enclosing"     # escopo E para a função interna

        def interna():
            # Python procura x em L (não tem), depois E: encontra "enclosing"
            print(x)        # "enclosing"

        interna()

    externa()
    print(x)    # "global" — a função não alterou o x externo

MODIFICANDO O ESCOPO EXTERNO:
Por padrão, atribuir a uma variável dentro de uma função cria uma
variável LOCAL, mesmo que exista uma de mesmo nome fora:

    contador = 0

    def incrementar():
        contador = 1      # cria variável LOCAL chamada contador
    # não altera o contador global!

    incrementar()
    print(contador)    # 0 — não mudou!

Para modificar a variável do escopo externo, use global ou nonlocal:

    contador = 0

    def incrementar():
        global contador    # agora se refere ao contador do módulo
        contador += 1

    incrementar()
    print(contador)    # 1 — agora mudou

    # nonlocal: para funções aninhadas, modifica o escopo da função externa

CUIDADO COM global: funções que dependem de estado global são difíceis
de testar e entender. Prefira receber e retornar valores em vez de
modificar variáveis globais.

---------------------------------------------------------------------------
7. Docstrings: documentação que fica junto com o código
---------------------------------------------------------------------------
Docstring é a string logo após o def. Ela fica disponível via help()
e ferramentas de documentação:

    def calcular_imc(peso, altura):
        \"\"\"Calcula o Indice de Massa Corporal.

        Args:
            peso: peso em quilogramas (deve ser positivo)
            altura: altura em metros (deve ser positivo)

        Returns:
            O IMC como float, arredondado em 2 casas decimais.

        Raises:
            ValueError: se peso ou altura forem menores ou iguais a zero.
        \"\"\"
        if peso <= 0 or altura <= 0:
            raise ValueError("peso e altura devem ser positivos")
        return round(peso / altura ** 2, 2)

Não existe um formato obrigatório, mas os mais usados são Google Style
(Args/Returns/Raises como acima) e NumPy Style (seções com ---).
O importante é escolher um e ser consistente.

---------------------------------------------------------------------------
8. Boas práticas resumidas
---------------------------------------------------------------------------
    Uma função, uma responsabilidade
    Nome verbal que descreve a ação: calcular_media(), nao media_calculo()
    Parametros com nomes descritivos: nao f(x, y, z)
    Docstring sempre que a funcao for usada em mais de um lugar
    Nunca use lista/dict como valor padrao — use None
    Prefira retornar valores a imprimir dentro da funcao
    Maximo de 3-4 parametros; se precisar de mais, agrupe em dict ou objeto
    Evite efeitos colaterais surpreendentes (mutar argumentos sem avisar)
""",
    exemplos=[
        Exemplo(
            titulo="Os quatro tipos de parâmetro em ação",
            codigo='''def relatorio(titulo, *linhas, separador="-", largura=40):
    """Gera um relatorio formatado.

    titulo e posicional obrigatorio.
    *linhas captura qualquer numero de linhas de conteudo.
    separador e largura sao keyword-only (vem apos *linhas).
    """
    print(titulo.center(largura, "="))
    print(separador * largura)
    for linha in linhas:
        print(linha)
    print(separador * largura)
    return len(linhas)

# Chamadas possiveis:
relatorio("Vendas")
relatorio("Vendas", "Ana: R$120", "Bruno: R$90")
relatorio("Vendas", "Ana: R$120", separador="*", largura=30)

# Desempacotando na chamada:
itens = ["Item A", "Item B", "Item C"]
relatorio("Estoque", *itens)    # equivale a relatorio("Estoque", "Item A", "Item B", "Item C")
''',
            explicacao="separador e largura são keyword-only: como vêm depois "
                       "de *linhas na assinatura, só podem ser passados por nome, "
                       "nunca por posição. Isso evita ambiguidade: se fossem "
                       "posicionais, como distinguir uma linha de conteúdo de um "
                       "separador? O * em *itens na chamada desempacota a lista.",
        ),
        Exemplo(
            titulo="A armadilha do padrão mutável, ao vivo",
            codigo='''# VERSAO COM BUG: lista padrao acumula entre chamadas
def adicionar_bug(item, lista=[]):
    lista.append(item)
    return lista

print(adicionar_bug("a"))    # ['a']
print(adicionar_bug("b"))    # ['a', 'b']  — bug!
print(adicionar_bug("c"))    # ['a', 'b', 'c']  — acumulou tudo!
print(adicionar_bug.__defaults__)  # veja a lista "padrao" acumulada

print()

# VERSAO CORRETA: None como sentinela
def adicionar_certo(item, lista=None):
    if lista is None:
        lista = []    # nova lista a cada chamada
    lista.append(item)
    return lista

print(adicionar_certo("a"))    # ['a']
print(adicionar_certo("b"))    # ['b']  — correto!

# Passando uma lista existente ainda funciona:
minha_lista = [10, 20]
adicionar_certo(30, minha_lista)
print(minha_lista)    # [10, 20, 30]
''',
            explicacao="__defaults__ guarda os valores padrão atuais — "
                       "você pode ver a lista acumulando entre chamadas. "
                       "Na versão correta, cada chamada sem argumento cria "
                       "uma lista nova independente. "
                       "Mas passar uma lista existente continua funcionando "
                       "— a função ainda a modifica no lugar (o que pode ser "
                       "o comportamento desejado).",
        ),
        Exemplo(
            titulo="Escopo LEGB: rastreando onde cada nome é encontrado",
            codigo='''x = "global"

def externa():
    x = "enclosing"

    def interna():
        # L: nao tem x local
        # E: encontra "enclosing" aqui
        print("interna ve:", x)

    interna()
    print("externa ve:", x)

externa()
print("modulo ve:", x)

# global e nonlocal em acao
contador = 0

def incrementar():
    global contador
    contador += 1

incrementar()
incrementar()
print("contador:", contador)    # 2

# Funcao que nao precisa de global (forma preferida)
def incrementar_limpo(c):
    return c + 1    # recebe e retorna, sem tocar no global

n = 0
n = incrementar_limpo(n)
n = incrementar_limpo(n)
print("n:", n)    # 2  — mesmo resultado, sem efeito colateral
''',
            explicacao="A versão com global funciona, mas a versão 'limpa' "
                       "é muito preferida: receber o valor como parâmetro "
                       "e retornar o novo valor torna a função testável "
                       "isoladamente — você pode chamar incrementar_limpo(5) "
                       "e prever o resultado sem saber nada do estado global.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d11e1",
            enunciado=(
                "Escreva a funcao saudacao(nome, saudacao='Ola') que devolve\n"
                "uma saudacao no formato: '<saudacao>, <nome>!'\n\n"
                "Exemplos:\n"
                "   saudacao('Ana')              -> 'Ola, Ana!'\n"
                "   saudacao('Bruno', 'Bom dia') -> 'Bom dia, Bruno!'\n"
                "   saudacao(saudacao='Oi', nome='Cris') -> 'Oi, Cris!'\n\n"
                "Observe o terceiro exemplo: como saudacao tem um valor\n"
                "padrao, pode ser passado POR NOME em qualquer posicao.\n"
                "Argumentos nomeados ignoram a ordem da definicao.\n\n"
                "Use uma f-string para montar o resultado:\n"
                "   f'{saudacao}, {nome}!'"
            ),
            funcao="saudacao",
            assinatura="def saudacao(nome, saudacao='Ola'):",
            testes=[
                ("saudacao('Ana')", "'Ola, Ana!'"),
                ("saudacao('Bruno', 'Bom dia')", "'Bom dia, Bruno!'"),
                ("saudacao(saudacao='Oi', nome='Cris')", "'Oi, Cris!'"),
            ],
            dica="return f'{saudacao}, {nome}!'",
        ),
        Exercicio(
            id="d11e2",
            enunciado=(
                "Escreva a funcao estatisticas(*numeros) que recebe qualquer\n"
                "quantidade de numeros e devolve a tupla (minimo, maximo, media).\n"
                "Se nao receber nenhum numero, devolve (None, None, None).\n\n"
                "Exemplos:\n"
                "   estatisticas(3, 1, 5)  -> (1, 5, 3.0)\n"
                "   estatisticas()         -> (None, None, None)\n"
                "   estatisticas(4)        -> (4, 4, 4.0)\n\n"
                "*numeros captura todos os argumentos posicionais como TUPLA.\n"
                "Uma tupla vazia () e falsy em Python, entao:\n"
                "   if not numeros:   <- isso verifica se a tupla esta vazia\n\n"
                "Estrategia:\n"
                "   1. if not numeros: return (None, None, None)\n"
                "   2. return min(numeros), max(numeros), sum(numeros)/len(numeros)\n\n"
                "Lembre: devolver multiplos valores separados por virgula\n"
                "automaticamente cria uma tupla."
            ),
            funcao="estatisticas",
            assinatura="def estatisticas(*numeros):",
            testes=[
                ("estatisticas(3, 1, 5)", "(1, 5, 3.0)"),
                ("estatisticas()", "(None, None, None)"),
                ("estatisticas(4)", "(4, 4, 4.0)"),
            ],
            nivel="medio",
            dica="if not numeros: return (None, None, None). Depois: return min(numeros), max(numeros), sum(numeros)/len(numeros)",
        ),
        Exercicio(
            id="d11e3",
            enunciado=(
                "Escreva a funcao montar_url(base, **params) que monta uma\n"
                "URL com parametros de query string.\n\n"
                "Exemplos:\n"
                "   montar_url('/api', b=2, a=1)  -> '/api?a=1&b=2'\n"
                "   montar_url('/api')             -> '/api'\n"
                "   montar_url('/x', z='oi')       -> '/x?z=oi'\n\n"
                "Regras:\n"
                "   - Se nao houver params: devolva apenas a base\n"
                "   - Os parametros devem aparecer em ordem ALFABETICA\n"
                "     (por isso '/api?a=1&b=2' e nao '/api?b=2&a=1')\n"
                "   - Formato: base + '?' + 'chave=valor' separados por '&'\n\n"
                "**params captura os argumentos nomeados como DICIONARIO.\n\n"
                "Estrategia:\n"
                "   1. if not params: return base\n"
                "   2. Ordene os parametros: sorted(params.items())\n"
                "      sorted sobre items() ordena por chave alfabeticamente\n"
                "   3. Monte cada par: f'{k}={v}'\n"
                "   4. Una com '&': '&'.join(...)\n"
                "   5. Retorne base + '?' + resultado"
            ),
            funcao="montar_url",
            assinatura="def montar_url(base, **params):",
            testes=[
                ("montar_url('/api', b=2, a=1)", "'/api?a=1&b=2'"),
                ("montar_url('/api')", "'/api'"),
                ("montar_url('/x', z='oi')", "'/x?z=oi'"),
            ],
            nivel="dificil",
            dica="if not params: return base. Depois: '&'.join(f'{k}={v}' for k, v in sorted(params.items()))",
        ),
    ],
    quiz=[
        Quiz(
            "Por que usar lista como valor padrao em uma funcao e perigoso?",
            ["Listas nao podem ser valores padrao em Python",
             "O valor padrao e criado uma unica vez quando a funcao e definida, entao todas as chamadas sem argumento compartilham a mesma lista",
             "A lista padrao e copiada a cada chamada, causando lentidao",
             "Funciona normalmente — nao ha problema algum"],
            1,
            "def f(lista=[]): a lista [] e criada QUANDO o def e executado, "
            "nao a cada chamada. Todas as chamadas sem argumento pegam "
            "a MESMA lista, que vai acumulando. Solucao: def f(lista=None) "
            "e criar a lista dentro da funcao.",
        ),
        Quiz(
            "Dentro de uma funcao, o que acontece ao atribuir a uma variavel de mesmo nome que uma global?",
            ["A variavel global e modificada automaticamente",
             "Causa um SyntaxError",
             "Cria uma variavel LOCAL nova — a global nao e afetada, a menos que voce declare 'global nome'",
             "A variavel local e ignorada e a global e usada"],
            2,
            "Python cria uma variavel LOCAL sempre que voce atribui a um nome "
            "dentro de uma funcao. A variavel global com mesmo nome fica intacta. "
            "Para modificar a global, declare 'global nome' antes de usar.",
        ),
        Quiz(
            "O que *args faz na definicao de uma funcao?",
            ["Torna todos os parametros opcionais",
             "Captura argumentos posicionais extras em uma TUPLA",
             "Captura argumentos nomeados extras em um dicionario",
             "Desempacota uma lista na chamada da funcao"],
            1,
            "*args captura zero ou mais argumentos posicionais extras como uma TUPLA. "
            "**kwargs captura argumentos nomeados como DICIONARIO. "
            "Na CHAMADA, *lista desempacota a lista em argumentos separados — "
            "operacao inversa.",
        ),
        Quiz(
            "Qual a diferenca entre reatribuir um parametro e mutar o objeto que ele aponta?",
            ["Nao ha diferenca — ambos afetam o chamador",
             "Nenhum dos dois afeta o chamador",
             "Reatribuir nao afeta o chamador; mutar (ex: .append) afeta, pois o objeto e compartilhado",
             "Depende do tipo do parametro: int sempre afeta, str nunca afeta"],
            2,
            "Python passa referencias. Reatribuir (param = novo_valor) faz o parametro "
            "local apontar para outra coisa — o chamador nao ve. "
            "Mutar (lista.append(x)) modifica o objeto em si, que chamador e funcao "
            "compartilham — o chamador ve a mudanca.",
        ),
    ],
    projeto=(
        "Crie calculadora_financeira.py com as seguintes funcoes:\n\n"
        "   1. juros_simples(principal, taxa, tempo)\n"
        "      -> montante = principal * (1 + taxa * tempo)\n\n"
        "   2. juros_compostos(principal, taxa, tempo)\n"
        "      -> montante = principal * (1 + taxa) ** tempo\n\n"
        "   3. parcelamento(valor, parcelas, taxa_mensal=0.0)\n"
        "      -> (valor_parcela, total, juros_pagos)\n\n"
        "   4. relatorio(*investimentos, taxa=0.05, anos=10)\n"
        "      Recebe varios valores de investimento e exibe uma tabela\n"
        "      comparando juros simples vs compostos para cada um\n\n"
        "Requisitos:\n"
        "   - Docstring em todas as funcoes (Args e Returns)\n"
        "   - Clausulas de guarda para valores invalidos (negativo, zero)\n"
        "   - Nenhuma funcao usa print() — apenas retornam valores\n"
        "   - Uma funcao principal() que chama todas e exibe os resultados\n\n"
        "BONUS: adicione um parametro *args para aceitar multiplas taxas\n"
        "e comparar o rendimento do mesmo principal com taxas diferentes."
    ),
    leitura=[
        "docs.python.org/pt-br/3/tutorial/controlflow.html#defining-functions",
        "PEP 257 — Docstring Conventions",
        "docs.python.org/pt-br/3/faq/programming.html — armadilha do argumento mutavel",
    ],
))

# ---------------------------------------------------------------- DIA 12
DIAS.append(Dia(
    numero=12,
    titulo="Funções de alta ordem, lambda e recursão",
    nivel="Intermediário",
    duracao="110 min",
    objetivos=[
        "Entender que funções são objetos de primeira classe: podem ser atribuídas, passadas e retornadas",
        "Usar map(), filter() e sorted() com funções como argumentos",
        "Escrever closures e entender o que é captura de variável do escopo externo",
        "Criar lambdas para expressões simples e saber quando elas são inadequadas",
        "Escrever funções recursivas com caso base e caso recursivo bem definidos",
        "Visualizar a pilha de chamadas e entender o que causa RecursionError",
        "Compor funções para criar transformações em cadeia",
    ],
    teoria="""
No Dia 11 você aprendeu como funções recebem e retornam valores. Hoje
vamos um passo além: funções que recebem OUTRAS FUNÇÕES como argumento,
funções que RETORNAM funções, e funções que se chamam a si mesmas.

Esses conceitos formam a base da programação funcional — um estilo de
programar que Python suporta naturalmente ao lado do estilo orientado
a objetos.

---------------------------------------------------------------------------
1. Funções são objetos de primeira classe
---------------------------------------------------------------------------
Em Python, uma função é um objeto como qualquer outro. Você pode:

    def dobrar(x):
        return x * 2

    # Atribuir a uma variável
    operacao = dobrar        # sem parênteses! não chama a função, aponta para ela
    print(operacao(5))       # 10

    # Guardar em uma lista
    operacoes = [dobrar, abs, str]
    for op in operacoes:
        print(op(-3))        # -6, 3, '-3'

    # Passar como argumento
    numeros = [3, -1, 4, -1, 5]
    print(sorted(numeros, key=dobrar))   # ordena pelo dobro

    # Verificar o tipo
    print(type(dobrar))     # <class 'function'>
    print(callable(dobrar)) # True — pode ser chamada com ()

A distinção crucial:
    dobrar      referência ao objeto função (não executa)
    dobrar(5)   chama a função e devolve o resultado (10)

---------------------------------------------------------------------------
2. Funções de alta ordem: recebendo funções
---------------------------------------------------------------------------
Uma função de ALTA ORDEM (ou higher-order function) é qualquer função
que receba outra função como argumento OU que retorne uma função.

Você já usa funções de alta ordem sem saber: sorted(key=...) e
max(key=...) recebem funções como argumentos.

AS TRÊS CLÁSSICAS: map, filter, reduce

map(funcao, iteravel): aplica a função a cada elemento

    numeros = [1, 2, 3, 4, 5]
    dobrados = list(map(lambda x: x * 2, numeros))
    # [2, 4, 6, 8, 10]

    # Equivalente com compreensão (preferida em Python):
    dobrados = [x * 2 for x in numeros]

filter(funcao, iteravel): mantém só os que retornam True

    pares = list(filter(lambda x: x % 2 == 0, numeros))
    # [2, 4]

    # Equivalente com compreensão:
    pares = [x for x in numeros if x % 2 == 0]

reduce: acumula (precisa importar de functools)

    from functools import reduce
    produto = reduce(lambda acc, x: acc * x, numeros)
    # 1 * 2 * 3 * 4 * 5 = 120

    # Equivalente explícito:
    produto = 1
    for x in numeros:
        produto *= x

QUANDO USAR map/filter vs compreensões:
Em Python moderno, compreensões são geralmente preferidas por serem mais
legíveis. map e filter brilham quando a função já existe (não precisa de
lambda) ou quando você constrói pipelines com várias transformações:

    # map com função existente (mais limpo que compreensão)
    textos = ["  ana  ", " BRUNO ", "carla"]
    limpos = list(map(str.strip, textos))   # sem lambda, sem compreensão

ESCREVENDO SUAS PRÓPRIAS FUNÇÕES DE ALTA ORDEM:

    def aplicar_a_todos(funcao, lista):
        return [funcao(x) for x in lista]

    def aplicar_se(predicado, funcao, lista):
        return [funcao(x) if predicado(x) else x for x in lista]

    resultado = aplicar_se(
        lambda x: x < 0,      # predicado: é negativo?
        lambda x: -x,         # transformação: inverte o sinal
        [1, -2, 3, -4, 5]
    )
    # [1, 2, 3, 4, 5]

---------------------------------------------------------------------------
3. Funções que retornam funções: closures
---------------------------------------------------------------------------
Uma closure é uma função que "captura" variáveis do escopo onde foi
criada. Ela carrega esses valores consigo, mesmo depois que a função
externa terminou de executar.

    def criar_multiplicador(fator):
        def multiplicar(x):
            return x * fator    # fator vem do escopo externo
        return multiplicar      # retorna a função, sem chamar

    dobrar = criar_multiplicador(2)
    triplicar = criar_multiplicador(3)

    print(dobrar(5))      # 10
    print(triplicar(5))   # 15

    # dobrar e triplicar são closures: cada uma "lembrou" seu fator

Como funciona:
    1. criar_multiplicador(2) é chamada: fator = 2
    2. Dentro, multiplicar é criada, mas ainda não executada
    3. A função multiplicar é retornada — ela "leva" o fator consigo
    4. Mesmo depois de criar_multiplicador terminar, o fator persiste
       dentro de dobrar (você pode verificar com dobrar.__closure__)

Verificando a closure:

    print(dobrar.__closure__)              # (<cell at 0x...>,)
    print(dobrar.__closure__[0].cell_contents)  # 2

ARMADILHA CLÁSSICA DE CLOSURE EM LOOP:

    # ERRADO: todas as funções capturam a mesma variável i
    funcoes = []
    for i in range(3):
        funcoes.append(lambda x: x * i)    # captura i, não o valor atual!

    print(funcoes[0](10))   # 20, não 0 — i já é 2 quando executado
    print(funcoes[1](10))   # 20
    print(funcoes[2](10))   # 20

    # CORRETO: "congela" o valor atual com argumento padrão
    funcoes = []
    for i in range(3):
        funcoes.append(lambda x, i=i: x * i)   # i=i captura o valor AGORA

    print(funcoes[0](10))   # 0   — correto
    print(funcoes[1](10))   # 10  — correto
    print(funcoes[2](10))   # 20  — correto

---------------------------------------------------------------------------
4. lambda: funções anônimas de uma expressão
---------------------------------------------------------------------------
lambda cria uma função sem nome, com uma única expressão como corpo:

    lambda parametros: expressao

    # Equivalências:
    lambda x: x * 2
    # é equivalente a:
    def anonima(x):
        return x * 2

Usos adequados (como argumento para funções de alta ordem):

    sorted(nomes, key=lambda n: n.split()[-1])   # ordena por sobrenome
    max(produtos, key=lambda p: p["preco"])       # produto mais caro
    filter(lambda x: x > 0, numeros)             # só positivos

REGRAS DO lambda:

    Pode:
    - Ter zero ou mais parâmetros: lambda: 42  /  lambda x, y: x + y
    - Conter uma única expressão (calculada e retornada)
    - Usar *args e **kwargs: lambda *args: sum(args)

    Não pode:
    - Ter múltiplas instruções
    - Usar return, if/elif/else como instruções, for, while
    - Ter docstring
    - Ter corpo com efeitos colaterais complexos

QUANDO NÃO USAR lambda:

    # ERRADO: lambda desnecessário quando a função já existe
    sorted(numeros, key=lambda x: abs(x))   # redundante
    sorted(numeros, key=abs)                # direto e claro

    # ERRADO: atribuir lambda a variável com nome
    dobrar = lambda x: x * 2   # faz o mesmo que def, mas sem docstring
    # Se você vai nomear, use def!

    # CERTO: argumento temporário e descartável
    sorted(pessoas, key=lambda p: (p["sobrenome"], p["nome"]))

---------------------------------------------------------------------------
5. Recursão: funções que chamam a si mesmas
---------------------------------------------------------------------------
Uma função recursiva é aquela que chama a si mesma. Para funcionar
corretamente, toda recursão precisa de DUAS partes obrigatórias:

    CASO BASE:     a condição que faz a recursão parar
    CASO RECURSIVO: onde a função chama a si mesma, se aproximando do caso base

Sem o caso base, a função chama a si mesma infinitamente até estourar
a pilha de chamadas (RecursionError).

EXEMPLO CLÁSSICO: fatorial

    def fatorial(n):
        # Caso base: ponto de parada
        if n <= 1:
            return 1
        # Caso recursivo: chama a si mesmo com n-1 (se aproxima do caso base)
        return n * fatorial(n - 1)

    fatorial(5)
    # = 5 * fatorial(4)
    # = 5 * 4 * fatorial(3)
    # = 5 * 4 * 3 * fatorial(2)
    # = 5 * 4 * 3 * 2 * fatorial(1)
    # = 5 * 4 * 3 * 2 * 1       <- caso base, começa a retornar
    # = 120

VISUALIZANDO A PILHA DE CHAMADAS:
Cada chamada de função empilha um "frame" (quadro) na pilha de execução.
Na recursão, esses frames se acumulam:

    PILHA (de baixo para cima):
    | fatorial(1) = 1           | <- topo: caso base, retorna 1
    | fatorial(2) = 2 * ?       |
    | fatorial(3) = 3 * ?       |
    | fatorial(4) = 4 * ?       |
    | fatorial(5) = 5 * ?       | <- fundo: chamada original
    ---------------------------------
    | código principal           |

Quando fatorial(1) retorna, o frame é removido e o valor 1 vai para
fatorial(2), que calcula 2*1=2, retorna, e assim por diante.

AS TRÊS CAUSAS DE RecursionError:

    CAUSA 1: Sem caso base
    def infinita(n):
        return infinita(n - 1)   # nunca para

    CAUSA 2: Caso base inalcançável
    def bugada(n):
        if n == 0: return 0
        return bugada(n + 1)   # aumenta n, nunca chega em 0

    CAUSA 3: Limite da pilha (mesmo com recursão correta)
    fatorial(10000)   # RecursionError: pilha com limite de ~1000 frames

O limite padrão do Python é ~1000 chamadas recursivas. Pode ser
ajustado com sys.setrecursionlimit(), mas raramente é a solução certa.
Se a recursão for muito profunda, prefira a versão iterativa (com while).

RECURSÃO vs ITERAÇÃO:
Recursão e iteração são equivalentes em poder: tudo que um pode fazer,
o outro também pode. A escolha é de clareza e contexto:

    Use recursão quando:
    - O problema tem estrutura naturalmente recursiva (árvores, grafos)
    - O código recursivo é significativamente mais claro
    - A profundidade é pequena e conhecida

    Prefira iteração quando:
    - A recursão pode ir fundo demais (risco de RecursionError)
    - Desempenho é crítico (cada chamada de função tem custo)
    - O problema é naturalmente iterativo (percorrer lista)

---------------------------------------------------------------------------
6. Composição de funções
---------------------------------------------------------------------------
Compor funções significa criar uma nova função que aplica duas (ou mais)
funções em sequência, onde a saída de uma é a entrada da próxima:

    # Sem composição (manual)
    def processar(texto):
        sem_espacos = texto.strip()
        minusculo = sem_espacos.lower()
        return minusculo

    # Com composição explícita
    def compor(f, g):
        def composta(x):
            return f(g(x))     # aplica g primeiro, depois f
        return composta

    limpar = compor(str.lower, str.strip)
    print(limpar("  ANA  "))    # "ana"

    # Compondo várias funções
    def pipeline(*funcoes):
        from functools import reduce
        return reduce(compor, funcoes)

    processar = pipeline(str.strip, str.lower, str.title)
    print(processar("  ana maria  "))   # "Ana Maria"

Composição é um conceito poderoso em programação funcional: você constrói
comportamentos complexos combinando funções simples, cada uma fazendo
uma coisa só.
""",
    exemplos=[
        Exemplo(
            titulo="Funções de alta ordem na prática",
            codigo='''# sorted com key: ordena pelo ultimo caractere
palavras = ["banana", "kiwi", "abacaxi", "uva"]
por_ultima = sorted(palavras, key=lambda p: p[-1])
print("Por ultima letra:", por_ultima)

# max/min com key: produto mais caro / mais barato
produtos = [
    {"nome": "Caneta", "preco": 2.50},
    {"nome": "Caderno", "preco": 15.90},
    {"nome": "Regua", "preco": 3.75},
]
mais_caro = max(produtos, key=lambda p: p["preco"])
mais_barato = min(produtos, key=lambda p: p["preco"])
print(f"Mais caro: {mais_caro['nome']} (R${mais_caro['preco']:.2f})")
print(f"Mais barato: {mais_barato['nome']} (R${mais_barato['preco']:.2f})")

# map com funcao existente (sem lambda)
textos = ["  ana  ", " BRUNO ", " carla "]
limpos = list(map(str.strip, textos))
maiusculos = list(map(str.upper, limpos))
print("Limpos:", limpos)
print("Maiusculos:", maiusculos)

# Funcao que aceita funcao como argumento
def aplicar_desconto(produtos, calcular):
    return [{**p, "preco": round(calcular(p["preco"]), 2)} for p in produtos]

com_desc = aplicar_desconto(produtos, lambda p: p * 0.9)
for prod in com_desc:
    print(f"{prod['nome']}: R${prod['preco']:.2f}")
''',
            explicacao="lambda p: p[-1] acessa o último caractere de cada string. "
                       "map(str.strip, textos) usa o método strip como função — "
                       "str.strip é a versão 'desligada' do método, que recebe a "
                       "string como primeiro argumento. "
                       "{**p, 'preco': ...} cria um dicionário novo baseado em p "
                       "com o campo preco substituído — preview do Dia 16.",
        ),
        Exemplo(
            titulo="Closures: fábricas de funções",
            codigo='''# Fabrica de validadores
def criar_validador(minimo, maximo):
    def validar(valor):
        return minimo <= valor <= maximo
    return validar    # retorna a funcao, nao o resultado!

validar_nota = criar_validador(0, 10)
validar_idade = criar_validador(0, 150)
validar_percentual = criar_validador(0, 100)

print(validar_nota(7.5))    # True
print(validar_nota(11))     # False
print(validar_idade(25))    # True
print(validar_percentual(105))  # False

# Verificando o que a closure capturou
print(validar_nota.__closure__[0].cell_contents)   # 0  (minimo)
print(validar_nota.__closure__[1].cell_contents)   # 10 (maximo)

# Fabrica de formatadores
def criar_formatador(prefixo, sufixo=""):
    def formatar(valor):
        return f"{prefixo}{valor}{sufixo}"
    return formatar

em_reais = criar_formatador("R$ ", " BRL")
porcentagem = criar_formatador("", "%")

print(em_reais(29.90))      # R$ 29.9 BRL
print(porcentagem(85))      # 85%
''',
            explicacao="Cada chamada a criar_validador cria uma nova closure "
                       "independente com seus próprios minimo e maximo. "
                       "__closure__ expõe as variáveis capturadas — útil para "
                       "depuração. O padrão 'fábrica de funções' é muito usado "
                       "para criar variações de comportamento sem repetir código.",
        ),
        Exemplo(
            titulo="Recursão: visualizando a pilha",
            codigo='''import sys

def fatorial(n, nivel=0):
    """Fatorial com visualizacao da pilha de chamadas."""
    recuo = "  " * nivel
    print(f"{recuo}-> fatorial({n})")

    if n <= 1:
        print(f"{recuo}<- retorna 1 (caso base)")
        return 1

    resultado = n * fatorial(n - 1, nivel + 1)
    print(f"{recuo}<- retorna {n} * ... = {resultado}")
    return resultado

print(fatorial(4))

print("\nLimite atual da pilha:", sys.getrecursionlimit())

# Recursao para achatar lista (problema naturalmente recursivo)
def achatar_recursivo(lista):
    resultado = []
    for item in lista:
        if isinstance(item, list):
            resultado.extend(achatar_recursivo(item))  # recursao!
        else:
            resultado.append(item)
    return resultado

aninhado = [1, [2, [3, [4]], 5], 6]
print(achatar_recursivo(aninhado))  # [1, 2, 3, 4, 5, 6]
''',
            explicacao="O parâmetro nivel é um artifício para visualizar a "
                       "profundidade da pilha — não faz parte do algoritmo. "
                       "A versão recursiva de achatar é mais elegante do que "
                       "a iterativa porque o problema tem estrutura naturalmente "
                       "recursiva: uma lista pode conter listas que contêm listas.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d12e1",
            enunciado=(
                "Escreva ordenar_por_sobrenome(nomes) que recebe uma lista\n"
                "de nomes completos e devolve a lista ordenada pelo SOBRENOME\n"
                "(ultimo nome de cada string).\n\n"
                "Exemplos:\n"
                "   ordenar_por_sobrenome(['Ana Silva', 'Bo Alves', 'Cris Melo'])\n"
                "   -> ['Bo Alves', 'Cris Melo', 'Ana Silva']\n"
                "   (Alves < Melo < Silva em ordem alfabetica)\n\n"
                "   ordenar_por_sobrenome([]) -> []\n\n"
                "Estrategia:\n"
                "   1. Use sorted() com o parametro key\n"
                "   2. A key deve extrair o ULTIMO elemento apos split():\n"
                "      lambda n: n.split()[-1]\n"
                "   3. n.split() divide o nome em lista de palavras\n"
                "   4. [-1] pega o ultimo elemento (o sobrenome)\n\n"
                "Por que lambda aqui e adequado: e uma expressao simples\n"
                "usada uma so vez como argumento de sorted()."
            ),
            funcao="ordenar_por_sobrenome",
            assinatura="def ordenar_por_sobrenome(nomes):",
            testes=[
                ("ordenar_por_sobrenome(['Ana Silva', 'Bo Alves', 'Cris Melo'])",
                 "['Bo Alves', 'Cris Melo', 'Ana Silva']"),
                ("ordenar_por_sobrenome([])", "[]"),
            ],
            dica="return sorted(nomes, key=lambda n: n.split()[-1])",
        ),
        Exercicio(
            id="d12e2",
            enunciado=(
                "Escreva a funcao fatorial(n) que calcula n! de forma\n"
                "RECURSIVA (sem usar loops).\n\n"
                "Definicao matematica:\n"
                "   0! = 1  (por definicao)\n"
                "   1! = 1\n"
                "   n! = n * (n-1)!  para n > 1\n\n"
                "Exemplos:\n"
                "   fatorial(0)  -> 1\n"
                "   fatorial(1)  -> 1\n"
                "   fatorial(5)  -> 120  (5*4*3*2*1)\n"
                "   fatorial(10) -> 3628800\n\n"
                "Estrutura da recursao:\n"
                "   def fatorial(n):\n"
                "       if n <= 1:              <- CASO BASE: para a recursao\n"
                "           return 1\n"
                "       return n * fatorial(n-1) <- CASO RECURSIVO: se aproxima do base\n\n"
                "Rastreie fatorial(4) mentalmente:\n"
                "   4 * fatorial(3)\n"
                "   4 * 3 * fatorial(2)\n"
                "   4 * 3 * 2 * fatorial(1)\n"
                "   4 * 3 * 2 * 1 = 24"
            ),
            funcao="fatorial",
            assinatura="def fatorial(n):",
            testes=[
                ("fatorial(0)", "1"),
                ("fatorial(1)", "1"),
                ("fatorial(5)", "120"),
                ("fatorial(10)", "3628800"),
            ],
            dica="if n <= 1: return 1. Senao: return n * fatorial(n - 1)",
        ),
        Exercicio(
            id="d12e3",
            enunciado=(
                "Escreva a funcao compor(f, g) que recebe duas funcoes e\n"
                "devolve uma NOVA FUNCAO que aplica g primeiro e depois f.\n\n"
                "Em matematica: compor(f, g)(x) = f(g(x))\n\n"
                "Exemplos:\n"
                "   compor(lambda x: x + 1, lambda x: x * 2)(5)\n"
                "   -> 11   (primeiro: 5*2=10, depois: 10+1=11)\n\n"
                "   compor(str, len)('abcd')\n"
                "   -> '4'  (primeiro: len('abcd')=4, depois: str(4)='4')\n\n"
                "   callable(compor(len, str))\n"
                "   -> True  (o resultado e uma funcao, nao um valor)\n\n"
                "Estrategia (closure):\n"
                "   def compor(f, g):\n"
                "       def composta(x):\n"
                "           return f(g(x))   <- g executa primeiro, f depois\n"
                "       return composta      <- retorna a FUNCAO, sem chamar!\n\n"
                "ATENCAO: return composta  (sem parenteses)\n"
                "         return composta() (com parenteses) chamaria a funcao agora!"
            ),
            funcao="compor",
            assinatura="def compor(f, g):",
            testes=[
                ("compor(lambda x: x + 1, lambda x: x * 2)(5)", "11"),
                ("compor(str, len)('abcd')", "'4'"),
                ("callable(compor(len, str))", "True"),
            ],
            nivel="dificil",
            dica="def composta(x): return f(g(x)). Depois: return composta  (sem parenteses!)",
        ),
    ],
    quiz=[
        Quiz(
            "Qual a diferenca entre 'dobrar' e 'dobrar(5)' ao referenciar uma funcao?",
            ["Nao ha diferenca — os dois executam a funcao",
             "'dobrar' e a referencia ao objeto funcao; 'dobrar(5)' chama a funcao e devolve o resultado",
             "'dobrar' causa um NameError pois funcao precisa de argumentos",
             "'dobrar' e valido apenas dentro de outras funcoes"],
            1,
            "Funcoes sao objetos. 'dobrar' sem parenteses e apenas uma referencia "
            "— voce pode atribuir a uma variavel, guardar em lista, passar como argumento. "
            "'dobrar(5)' executa a funcao com argumento 5 e devolve o resultado.",
        ),
        Quiz(
            "O que uma closure 'captura' do escopo externo?",
            ["Uma copia do valor no momento da criacao",
             "Uma referencia a variavel do escopo externo, nao apenas o valor",
             "Apenas variaveis globais, nao locais",
             "Nada — closures nao tem acesso ao escopo externo"],
            1,
            "Closure captura a VARIAVEL (referencia), nao o valor no momento. "
            "Por isso a armadilha do loop: se a variavel muda depois da closure "
            "ser criada, a closure ve o valor atual, nao o antigo. "
            "Para 'congelar' o valor, use argumento padrao: lambda x, i=i: ...",
        ),
        Quiz(
            "Quando usar def em vez de lambda?",
            ["Nunca — lambda e sempre mais compacto e equivalente",
             "Quando a funcao precisa de nome, docstring, multiplas instrucoes, ou sera usada em mais de um lugar",
             "Apenas quando a funcao recebe mais de um parametro",
             "Apenas dentro de classes"],
            1,
            "Lambda e adequado para expressoes simples e temporarias como argumento de key= ou filter(). "
            "Se voce vai atribuir a uma variavel (dobrar = lambda x: x*2), use def — "
            "voce ganha docstring, nome descritivo no traceback e melhor legibilidade.",
        ),
        Quiz(
            "O que acontece se uma funcao recursiva nao tem caso base?",
            ["Ela devolve None automaticamente apos 1000 chamadas",
             "Ela entra em loop infinito e o programa trava para sempre",
             "Python detecta e levanta RecursionError apos esgotar o limite da pilha de chamadas",
             "A funcao funciona normalmente ate terminar o trabalho"],
            2,
            "Python tem um limite de profundidade da pilha (~1000 por padrao). "
            "Sem caso base, a funcao se chama indefinidamente ate estourar esse limite. "
            "Python entao levanta RecursionError: maximum recursion depth exceeded. "
            "Nunca um loop infinito no sentido de travar — sempre o RecursionError.",
        ),
    ],
    projeto=(
        "Crie pipeline_funcional.py com um conjunto de funcoes utilitarias\n"
        "para processamento de dados no estilo funcional:\n\n"
        "   1. criar_filtro(predicado) -> funcao que filtra uma lista\n"
        "      uso: filtrar_pares = criar_filtro(lambda x: x % 2 == 0)\n"
        "           filtrar_pares([1,2,3,4,5]) -> [2, 4]\n\n"
        "   2. criar_transformador(funcao) -> funcao que transforma uma lista\n"
        "      uso: dobrar_todos = criar_transformador(lambda x: x * 2)\n"
        "           dobrar_todos([1, 2, 3]) -> [2, 4, 6]\n\n"
        "   3. pipeline(*funcoes) -> funcao que aplica funcoes em sequencia\n"
        "      uso: processar = pipeline(filtrar_pares, dobrar_todos)\n"
        "           processar([1,2,3,4,5]) -> [4, 8]\n\n"
        "   4. memoizar(funcao) -> versao com cache da funcao\n"
        "      (guarda resultados ja calculados em um dicionario)\n\n"
        "Demonstre com:\n"
        "   - fib(n) recursivo memoizado para n=35 (compare com sem cache)\n"
        "   - pipeline de limpeza de texto: strip -> lower -> title\n"
        "   - pipeline numerico: filtrar positivos -> dobrar -> ordenar\n\n"
        "BONUS: implemente compor(*funcoes) que compoe N funcoes\n"
        "em vez de apenas duas, usando reduce() de functools."
    ),
    leitura=[
        "docs.python.org/pt-br/3/howto/functional.html — programacao funcional em Python",
        "docs.python.org/pt-br/3/library/functools.html — reduce, lru_cache e outros",
        "docs.python.org/pt-br/3/reference/expressions.html#lambda",
    ],
))

# ---------------------------------------------------------------- DIA 13
DIAS.append(Dia(
    numero=13,
    titulo="Módulos, pacotes, venv e pip no Linux",
    nivel="Intermediário",
    duracao="100 min",
    objetivos=[
        "Entender o que é um módulo e como o Python o encontra quando você importa",
        "Usar as diferentes formas de import e saber quando cada uma é adequada",
        "Compreender o papel do bloco if __name__ == '__main__' e por que ele importa",
        "Organizar código em pacotes com __init__.py",
        "Criar e ativar ambientes virtuais no Linux para isolar dependências",
        "Instalar, listar e remover bibliotecas com pip",
        "Usar pathlib para manipular caminhos de arquivo de forma moderna",
        "Conhecer os módulos mais úteis da biblioteca padrão",
    ],
    teoria="""
Até agora todo o seu código ficou em um único arquivo. Programas reais
têm centenas ou milhares de arquivos organizados em módulos e pacotes.
Hoje você aprende a estruturar código em partes reutilizáveis e a usar
bibliotecas de terceiros.

---------------------------------------------------------------------------
1. O que é um módulo?
---------------------------------------------------------------------------
Um módulo é simplesmente um ARQUIVO .py. Qualquer arquivo Python que
você cria já é automaticamente um módulo — não há nada especial a fazer.

Quando você escreve import math, o Python:

    1. Procura um arquivo chamado math.py (ou um pacote math/) em
       vários lugares, nessa ordem:
       a. O diretório do script atual
       b. Variável de ambiente PYTHONPATH (se definida)
       c. As pastas de instalação do Python (onde a stdlib fica)
       d. Pacotes instalados com pip (site-packages)

    2. Executa o arquivo encontrado uma única vez e guarda o resultado
       em sys.modules como cache — importar o mesmo módulo várias
       vezes não re-executa o arquivo

    3. Cria um objeto módulo no seu espaço de nomes

Você pode ver onde Python procura:

    import sys
    for caminho in sys.path:
        print(caminho)

---------------------------------------------------------------------------
2. As formas de importar e quando usar cada uma
---------------------------------------------------------------------------

FORMA 1 — import módulo: traz o módulo com seu prefixo (mais seguro)

    import math
    import os
    import datetime

    math.pi           # 3.141592...
    math.sqrt(16)     # 4.0
    os.getcwd()       # diretório atual

    # Alias: útil para nomes longos
    import datetime as dt
    dt.date.today()

FORMA 2 — from módulo import nome: traz nomes específicos sem prefixo

    from math import pi, sqrt, ceil
    from datetime import date, timedelta

    pi              # 3.141592... (sem o math. na frente)
    sqrt(16)        # 4.0
    date.today()    # objeto date de hoje

    # Quando usar: quando você usa muito uma função e o prefixo
    # ficaria repetitivo. Ex: pi aparece 20 vezes no código.

FORMA 3 — from módulo import *: traz TUDO (quase sempre evite)

    from math import *    # importa pi, e, sqrt, sin, cos, log, ...

    # Por que evitar:
    # - Polui o namespace: você não sabe mais de onde veio cada nome
    # - Pode sobrescrever nomes existentes sem avisar
    # - Dificulta leitura: de onde veio essa função sqrt?
    # - A única exceção aceita: __init__.py de pacotes para expor API

QUAL USAR? Uma boa heurística:
    - Módulos da stdlib conhecidos (math, os, sys): use import módulo
    - Funções muito usadas do módulo: use from módulo import função
    - Nunca use import * em código de produção

---------------------------------------------------------------------------
3. O bloco if __name__ == '__main__': por que ele existe
---------------------------------------------------------------------------
Todo módulo Python tem uma variável especial chamada __name__:

    Quando o arquivo é EXECUTADO diretamente (python3 arquivo.py):
        __name__ vale "__main__"

    Quando o arquivo é IMPORTADO por outro módulo:
        __name__ vale o nome do arquivo (sem o .py)

Por que isso importa? Imagine um arquivo calculos.py:

    # calculos.py (sem o bloco __main__)
    def media(valores):
        return sum(valores) / len(valores)

    # Este código roda SEMPRE — tanto ao executar quanto ao importar!
    print("Testando:")
    print(media([1, 2, 3]))

Quando outro arquivo faz import calculos, ele verá "Testando:" e o
resultado impresso na tela — efeito colateral indesejado!

A solução é o bloco __main__:

    # calculos.py (com o bloco __main__)
    def media(valores):
        return sum(valores) / len(valores)

    if __name__ == "__main__":
        # Este bloco só executa quando rodamos: python3 calculos.py
        # Quando importado, este bloco é PULADO
        print("Testando:")
        print(media([1, 2, 3]))

Regra prática: qualquer código que não seja definição de função/classe
deve estar dentro do if __name__ == "__main__".

---------------------------------------------------------------------------
4. Pacotes: organizando módulos em pastas
---------------------------------------------------------------------------
Um PACOTE é uma pasta que contém módulos. Para que o Python reconheça
uma pasta como pacote, ela precisa ter um arquivo __init__.py (pode ser
vazio):

    meu_projeto/
        __init__.py          <- marca como pacote
        calculos.py
        textos.py
        util/
            __init__.py      <- subpacote
            formatacao.py
            validacao.py

Importando de um pacote:

    import meu_projeto.calculos
    meu_projeto.calculos.media([1, 2, 3])

    from meu_projeto.calculos import media
    media([1, 2, 3])

    from meu_projeto.util.formatacao import formatar_moeda
    formatar_moeda(1234.56)

O __init__.py pode expor uma API pública do pacote:

    # meu_projeto/__init__.py
    from .calculos import media, soma
    from .textos import limpar, normalizar

    # Agora quem importa o pacote tem acesso direto:
    from meu_projeto import media   # sem precisar de meu_projeto.calculos.media

O ponto (.) em from .calculos import representa o pacote atual
(importação relativa) — usado dentro do próprio pacote para referenciar
módulos irmãos sem escrever o caminho completo.

---------------------------------------------------------------------------
5. Ambientes virtuais: isolando dependências no Linux
---------------------------------------------------------------------------
PROBLEMA: você tem dois projetos. O projeto A precisa de requests versão
2.28 e o projeto B precisa de requests versão 2.31. Como instalar os dois?

SOLUÇÃO: ambientes virtuais. Cada projeto tem sua própria cópia isolada
do Python e das bibliotecas instaladas.

CRIANDO E USANDO UM AMBIENTE VIRTUAL:

    # 1. Criar o ambiente (cria a pasta .venv no diretório atual)
    python3 -m venv .venv

    # 2. Ativar o ambiente
    source .venv/bin/activate

    # O prompt muda para mostrar que o ambiente está ativo:
    # (.venv) usuario@maquina:~/projeto$

    # 3. Instalar bibliotecas (vão para .venv, não para o sistema)
    pip install requests
    pip install pandas numpy

    # 4. Ver o que está instalado
    pip list
    pip freeze            # formato requirements.txt

    # 5. Salvar as dependências
    pip freeze > requirements.txt

    # 6. Restaurar em outro computador
    pip install -r requirements.txt

    # 7. Desativar o ambiente
    deactivate

POR QUE .venv E NÃO OUTRO NOME?
É a convenção mais aceita. O ponto no início faz a pasta ficar oculta
no Linux, e a maioria dos .gitignore de Python já inclui .venv/.

NUNCA versione o .venv no git! Adicione ao .gitignore:

    .venv/
    __pycache__/
    *.pyc

Em vez de .venv, versione o requirements.txt — quem clonar o repositório
cria o próprio ambiente e instala a partir do arquivo.

---------------------------------------------------------------------------
6. pip: gerenciando bibliotecas
---------------------------------------------------------------------------

    Comando                              O que faz
    ---------------------------------    ----------------------------------------
    pip install nome                     instala a versão mais recente
    pip install nome==2.28.0             instala uma versão específica
    pip install nome>=2.0,<3.0           instala dentro de uma faixa
    pip install -r requirements.txt      instala tudo do arquivo
    pip uninstall nome                   remove a biblioteca
    pip list                             lista o que está instalado
    pip show nome                        detalhes sobre uma biblioteca
    pip search nome                      busca no PyPI (às vezes desativado)
    pip install --upgrade nome           atualiza para a versão mais recente

PyPI (Python Package Index) em pypi.org é o repositório público de
bibliotecas Python — qualquer pessoa pode publicar lá.

---------------------------------------------------------------------------
7. A biblioteca padrão: o que já vem pronto
---------------------------------------------------------------------------
Python tem uma extensa biblioteca padrão ("batteries included"). Antes
de instalar qualquer coisa, verifique se já existe:

    Módulo          Para que serve
    ----------      -------------------------------------------------
    math            funções matemáticas: sqrt, pi, ceil, floor, log
    random          números aleatórios: random, randint, choice, shuffle
    datetime        datas e horas: date, datetime, timedelta
    pathlib         caminhos de arquivo (moderno, use isso)
    os              interação com SO: listdir, environ, getcwd
    sys             interpretador: argv, path, exit
    json            serializar/deserializar JSON
    csv             ler e escrever arquivos CSV
    re              expressões regulares
    collections     Counter, defaultdict, deque, namedtuple
    itertools       ferramentas para iteração
    functools       lru_cache, partial, reduce
    string          constantes de caracteres
    time            medir tempo: time(), sleep(), perf_counter()
    statistics      media, mediana, desvio padrão
    hashlib         MD5, SHA256 e outros hashes

---------------------------------------------------------------------------
8. pathlib: caminhos de arquivo do jeito moderno
---------------------------------------------------------------------------
O módulo pathlib oferece uma forma orientada a objetos de trabalhar
com caminhos, muito mais legível que os.path antigo:

    from pathlib import Path

    # Criando caminhos
    p = Path("/home/ana/projetos/relatorio.csv")
    p2 = Path.home() / "projetos" / "relatorio.csv"   # mesmo resultado!

    # O operador / une partes de caminho de forma segura
    # (não é divisão — é sobrecarga do operador)

    # Informações sobre o caminho
    p.name          # 'relatorio.csv'    — nome completo com extensão
    p.stem          # 'relatorio'        — nome sem extensão
    p.suffix        # '.csv'             — só a extensão
    p.parent        # Path('/home/ana/projetos')
    p.parts         # ('/', 'home', 'ana', 'projetos', 'relatorio.csv')

    # Verificando o que existe no disco
    p.exists()      # True/False — o caminho existe?
    p.is_file()     # True/False — é um arquivo?
    p.is_dir()      # True/False — é um diretório?

    # Lendo e escrevendo (para arquivos pequenos)
    texto = p.read_text(encoding="utf-8")
    p.write_text("novo conteudo", encoding="utf-8")

    # Listando conteúdo de diretório
    for arquivo in Path(".").iterdir():
        print(arquivo.name)

    # Buscando arquivos recursivamente
    for py in Path(".").rglob("*.py"):
        print(py)

    # Criando e removendo
    Path("nova_pasta").mkdir(parents=True, exist_ok=True)
    Path("arquivo.txt").unlink(missing_ok=True)   # remove sem erro se não existir

    # Renomeando/movendo
    Path("antigo.txt").rename("novo.txt")
""",
    exemplos=[
        Exemplo(
            titulo="Módulo reutilizável com bloco __main__",
            codigo='''# Simula o que estaria em um arquivo temperatura.py

def celsius_para_fahrenheit(c):
    """Converte Celsius para Fahrenheit."""
    return c * 9 / 5 + 32

def fahrenheit_para_celsius(f):
    """Converte Fahrenheit para Celsius."""
    return (f - 32) * 5 / 9

def celsius_para_kelvin(c):
    """Converte Celsius para Kelvin."""
    return c + 273.15

# Este bloco so executa ao rodar diretamente: python3 temperatura.py
# Ao importar (import temperatura), este bloco e PULADO
if __name__ == "__main__":
    for temp_c in [0, 25, 100, -40]:
        temp_f = celsius_para_fahrenheit(temp_c)
        temp_k = celsius_para_kelvin(temp_c)
        print(f"{temp_c:6.1f} C = {temp_f:6.1f} F = {temp_k:6.2f} K")
''',
            explicacao="Se outra parte do programa fizer 'import temperatura', "
                       "as três funções ficam disponíveis mas o bloco de teste "
                       "NÃO executa — não há print indesejado na tela. "
                       "Ao rodar 'python3 temperatura.py' diretamente, "
                       "o bloco if __name__ == '__main__' executa normalmente.",
        ),
        Exemplo(
            titulo="datetime: trabalhando com datas",
            codigo='''from datetime import date, datetime, timedelta

# Data de hoje
hoje = date.today()
print(f"Hoje: {hoje}")                    # 2026-07-28

# Criando datas específicas
nascimento = date(1990, 5, 15)
print(f"Nascimento: {nascimento}")

# Aritmética de datas
idade_dias = (hoje - nascimento).days
print(f"Idade em dias: {idade_dias}")

anos = idade_dias // 365
print(f"Idade aproximada: {anos} anos")

# Adicionando dias
prazo = hoje + timedelta(days=30)
print(f"Prazo em 30 dias: {prazo}")

# Formatando para exibição
print(hoje.strftime("%d/%m/%Y"))          # 28/07/2026
print(hoje.strftime("%A, %d de %B"))      # Monday, 28 de July

# Comparando datas
vencimento = date(2026, 12, 31)
if hoje < vencimento:
    faltam = (vencimento - hoje).days
    print(f"Vence em {faltam} dias")
''',
            explicacao="timedelta representa uma duração (diferença entre datas). "
                       "Subtrair duas datas produz um timedelta — use .days "
                       "para obter o número inteiro de dias. "
                       "Adicionar timedelta a uma data produz uma nova data. "
                       "strftime formata a data como string usando códigos: "
                       "%d=dia, %m=mês, %Y=ano com 4 dígitos.",
        ),
        Exemplo(
            titulo="pathlib: manipulando caminhos de forma moderna",
            codigo='''from pathlib import Path
import sys

# Caminho do script atual
script = Path(__file__) if "__file__" in dir() else Path("exemplo.py")
print("Script:", script.name)

# Construindo caminhos com /
home = Path.home()
projetos = home / "projetos"
arquivo = projetos / "dados" / "relatorio.csv"

print("Home:", home)
print("Arquivo:", arquivo)
print("Nome:", arquivo.name)
print("Stem:", arquivo.stem)
print("Sufixo:", arquivo.suffix)
print("Pai:", arquivo.parent)

# Trabalhando com o diretório atual
atual = Path(".")
print("\nArquivos .py no diretório atual:")
for py in sorted(atual.glob("*.py")):
    tamanho = py.stat().st_size if py.exists() else 0
    print(f"  {py.name} ({tamanho} bytes)")

# Criando um arquivo temporário para demonstração
temp = Path("/tmp/demo_pathlib.txt")
temp.write_text("Conteúdo de demonstração\nLinha 2\n", encoding="utf-8")
print(f"\nArquivo criado: {temp}")
print(f"Conteúdo:\n{temp.read_text(encoding='utf-8')}")
temp.unlink()    # remove o arquivo
print("Arquivo removido.")
''',
            explicacao="Path.home() devolve o diretório home do usuário. "
                       "O operador / entre Paths constrói caminhos de forma "
                       "segura e portável — funciona em Linux, Mac e Windows "
                       "sem precisar se preocupar com / vs \\. "
                       "glob('*.py') lista arquivos por padrão; "
                       "rglob('*.py') faz o mesmo recursivamente.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d13e1",
            enunciado=(
                "Escreva a funcao area_circulo(r) que calcula a area\n"
                "de um circulo de raio r, usando math.pi.\n"
                "O resultado deve ser arredondado para 4 casas decimais.\n\n"
                "Exemplos:\n"
                "   area_circulo(1) -> 3.1416\n"
                "   area_circulo(2) -> 12.5664\n"
                "   area_circulo(0) -> 0.0\n\n"
                "Formula: area = pi * r^2\n\n"
                "O import math ja esta na assinatura — use math.pi\n"
                "para obter o valor de pi com maxima precisao.\n"
                "round(valor, 4) arredonda para 4 casas decimais."
            ),
            funcao="area_circulo",
            assinatura="import math\n\n\ndef area_circulo(r):",
            testes=[
                ("area_circulo(1)", "3.1416"),
                ("area_circulo(2)", "12.5664"),
                ("area_circulo(0)", "0.0"),
            ],
            dica="return round(math.pi * r ** 2, 4)",
        ),
        Exercicio(
            id="d13e2",
            enunciado=(
                "Escreva a funcao dias_entre(d1, d2) que recebe duas datas\n"
                "no formato 'AAAA-MM-DD' e devolve o numero de dias entre\n"
                "elas (sempre positivo, independente da ordem).\n\n"
                "Exemplos:\n"
                "   dias_entre('2024-01-01', '2024-01-31') -> 30\n"
                "   dias_entre('2024-03-01', '2024-02-01') -> 29\n"
                "      (ordem invertida — resultado ainda e positivo)\n"
                "   dias_entre('2026-07-28', '2026-07-28') -> 0\n\n"
                "Estrategia:\n"
                "   1. Converta as strings para objetos date:\n"
                "      date.fromisoformat('2024-01-01') -> date(2024, 1, 1)\n"
                "   2. Subtraia as datas:\n"
                "      data2 - data1 produz um objeto timedelta\n"
                "   3. Use .days para obter o numero de dias:\n"
                "      timedelta.days pode ser negativo\n"
                "   4. Use abs() para garantir o resultado positivo"
            ),
            funcao="dias_entre",
            assinatura="from datetime import date\n\n\ndef dias_entre(d1, d2):",
            testes=[
                ("dias_entre('2024-01-01', '2024-01-31')", "30"),
                ("dias_entre('2024-03-01', '2024-02-01')", "29"),
                ("dias_entre('2026-07-28', '2026-07-28')", "0"),
            ],
            nivel="medio",
            dica="a = date.fromisoformat(d1); b = date.fromisoformat(d2); return abs((a - b).days)",
        ),
        Exercicio(
            id="d13e3",
            enunciado=(
                "Escreva a funcao info_caminho(caminho) que recebe uma\n"
                "string de caminho de arquivo e devolve a tupla:\n"
                "   (nome_completo, nome_sem_extensao, extensao)\n\n"
                "Exemplos:\n"
                "   info_caminho('/home/ana/dados/relatorio.csv')\n"
                "   -> ('relatorio.csv', 'relatorio', '.csv')\n\n"
                "   info_caminho('script.py')\n"
                "   -> ('script.py', 'script', '.py')\n\n"
                "   info_caminho('/tmp/README')\n"
                "   -> ('README', 'README', '')  <- sem extensao: sufixo vazio\n\n"
                "Estrategia com pathlib:\n"
                "   p = Path(caminho)\n"
                "   p.name    -> nome completo com extensao ('relatorio.csv')\n"
                "   p.stem    -> nome sem extensao ('relatorio')\n"
                "   p.suffix  -> so a extensao ('.csv') ou '' se nao tiver\n\n"
                "Devolva os tres como uma tupla: (p.name, p.stem, p.suffix)"
            ),
            funcao="info_caminho",
            assinatura="from pathlib import Path\n\n\ndef info_caminho(caminho):",
            testes=[
                ("info_caminho('/home/ana/dados/relatorio.csv')",
                 "('relatorio.csv', 'relatorio', '.csv')"),
                ("info_caminho('script.py')", "('script.py', 'script', '.py')"),
                ("info_caminho('/tmp/README')", "('README', 'README', '')"),
            ],
            dica="p = Path(caminho); return (p.name, p.stem, p.suffix)",
        ),
    ],
    quiz=[
        Quiz(
            "O que acontece quando voce importa o mesmo modulo duas vezes em sequencia?",
            ["O arquivo e executado duas vezes, dobrando o tempo de carga",
             "O Python usa o cache em sys.modules e nao re-executa o arquivo",
             "Causa um ImportError de importacao duplicada",
             "A segunda importacao sobrescreve a primeira"],
            1,
            "Na primeira importacao, Python executa o arquivo e guarda o resultado "
            "em sys.modules. Nas importacoes seguintes, encontra o modulo no cache "
            "e o reutiliza sem executar o arquivo novamente. "
            "Isso e importante: codigo no nivel de modulo roda apenas uma vez.",
        ),
        Quiz(
            "Por que adicionar '.venv/' ao .gitignore e essencial?",
            ["Para economizar espaco em disco no repositorio",
             "Ambientes virtuais contem binarios especificos da maquina e nao devem ser compartilhados — use requirements.txt para reproducibilidade",
             "O git nao consegue versionar pastas que comecam com ponto",
             "E apenas uma convencao opcional sem consequencia pratica"],
            1,
            "O .venv contem executaveis compilados para o SO especifico. "
            "Em outro computador (ou SO diferente), esses binarios nao funcionam. "
            "O correto e versionar requirements.txt e cada desenvolvedor criar "
            "seu proprio .venv com 'pip install -r requirements.txt'.",
        ),
        Quiz(
            "Qual e a diferenca entre Path.name, Path.stem e Path.suffix para o caminho '/dados/relatorio.csv'?",
            ["Os tres retornam a mesma coisa: 'relatorio.csv'",
             "name='relatorio.csv' (nome completo), stem='relatorio' (sem extensao), suffix='.csv' (so extensao)",
             "name='/dados/relatorio.csv' (caminho completo), stem='relatorio', suffix='.csv'",
             "stem e suffix nao existem em pathlib — apenas name"],
            1,
            "name e o arquivo com extensao, stem e sem extensao, suffix e so a extensao "
            "(incluindo o ponto). Para '/dados/rel.tar.gz': name='rel.tar.gz', "
            "stem='rel.tar', suffix='.gz'. suffixes devolve ['.tar', '.gz'].",
        ),
        Quiz(
            "Quando o bloco 'if __name__ == \"__main__\":' NAO executa?",
            ["Quando o arquivo e vazio",
             "Quando o arquivo e IMPORTADO por outro modulo (nao executado diretamente)",
             "Quando o arquivo tem erros de sintaxe",
             "Nunca — esse bloco sempre executa independente de como o arquivo e usado"],
            1,
            "Ao executar 'python3 arquivo.py', __name__ vale '__main__' e o bloco executa. "
            "Ao fazer 'import arquivo' em outro script, __name__ vale 'arquivo' "
            "(o nome do modulo) e o bloco e pulado. "
            "Isso permite o mesmo arquivo ser script E modulo reutilizavel.",
        ),
    ],
    projeto=(
        "Organize o codigo dos dias anteriores em um pacote:\n\n"
        "   meu_curso/\n"
        "       __init__.py\n"
        "       matematica.py    (area_circulo, fatorial, media, segundo_maior)\n"
        "       textos.py        (gritar, inverter, eh_palindromo, slug)\n"
        "       datas.py         (dias_entre, eh_bissexto)\n"
        "       main.py          (demonstra cada modulo)\n\n"
        "Requisitos:\n"
        "   1. Cada modulo tem if __name__ == '__main__' com testes proprios\n"
        "   2. main.py importa de cada modulo e demonstra as funcoes\n"
        "   3. __init__.py expoe as funcoes mais importantes do pacote\n"
        "   4. Crie um .venv para o projeto:\n"
        "      python3 -m venv .venv\n"
        "      source .venv/bin/activate\n"
        "      pip install pytest\n"
        "      pip freeze > requirements.txt\n\n"
        "BONUS: escreva um arquivo tests/test_matematica.py usando pytest\n"
        "e rode com 'pytest tests/' para ver os testes passando."
    ),
    leitura=[
        "docs.python.org/pt-br/3/tutorial/modules.html — modulos e pacotes",
        "docs.python.org/pt-br/3/library/pathlib.html — pathlib",
        "pip.pypa.io — documentacao do pip",
    ],
))
# ---------------------------------------------------------------- DIA 14
DIAS.append(Dia(
    numero=14,
    titulo="Arquivos, JSON e CSV",
    nivel="Intermediário",
    duracao="110 min",
    objetivos=[
        "Abrir, ler e escrever arquivos de texto com segurança usando o gerenciador with",
        "Entender os modos de abertura e escolher o certo para cada situação",
        "Serializar e desserializar dados com json.dumps() e json.loads()",
        "Ler e escrever arquivos CSV com csv.reader e csv.DictReader",
        "Usar io.StringIO para testar código de arquivo sem criar arquivos reais",
        "Navegar e manipular caminhos de arquivo com pathlib de forma moderna",
    ],
    teoria="""
Até agora, tudo que seus programas calculam desaparece quando o programa
encerra. Para guardar dados entre execuções — salvar configurações, exportar
resultados, ler entradas — você precisa trabalhar com ARQUIVOS.

Python tem ferramentas excelentes para isso: desde a leitura simples de
texto até formatos estruturados como JSON e CSV que são usados em quase
todos os sistemas modernos.

---------------------------------------------------------------------------
1. Abrindo e fechando arquivos: open() e o gerenciador with
---------------------------------------------------------------------------
A forma básica de abrir um arquivo em Python é com a função open():

    arquivo = open("dados.txt", "r")    # abre para leitura
    conteudo = arquivo.read()           # lê o conteúdo
    arquivo.close()                     # fecha — OBRIGATÓRIO

O problema: se ocorrer um erro entre open() e close(), o arquivo nunca é
fechado. Arquivo não fechado pode corromper dados, travar o sistema de
arquivos ou impedir que outros programas acessem o arquivo.

A SOLUÇÃO: o gerenciador de contexto with garante que o arquivo é sempre
fechado, mesmo que ocorra um erro:

    with open("dados.txt", "r") as arquivo:
        conteudo = arquivo.read()
    # arquivo é fechado automaticamente aqui, com ou sem erro

Pense no with como: "abra isso, dê o nome 'arquivo', execute o bloco
e GARANTA o fechamento ao final, aconteça o que acontecer".

NUNCA use open/close manual quando puder usar with. É mais seguro,
mais legível e é o padrão universal do Python moderno.

---------------------------------------------------------------------------
2. Modos de abertura
---------------------------------------------------------------------------
O segundo argumento de open() define o modo:

    Modo    Significado                              Se o arquivo não existe
    ------  ---------------------------------------  -----------------------
    'r'     leitura (padrão)                         FileNotFoundError
    'w'     escrita (apaga tudo que existia!)        cria o arquivo
    'a'     append (acrescenta ao final)             cria o arquivo
    'x'     criação exclusiva (falha se já existe)   cria o arquivo
    'r+'    leitura e escrita (sem apagar)           FileNotFoundError

Combinações com 'b' para modo binário (imagens, PDFs, etc.):

    'rb'    leitura binária
    'wb'    escrita binária

ATENÇÃO COM 'w': abre o arquivo e apaga TODO o conteúdo existente
IMEDIATAMENTE, antes mesmo de você escrever qualquer coisa. Se você
quiser preservar o conteúdo e adicionar ao final, use 'a'.

ENCODING: sempre especifique o encoding ao trabalhar com texto, para
evitar problemas entre sistemas operacionais diferentes:

    with open("dados.txt", "r", encoding="utf-8") as f:
        conteudo = f.read()

UTF-8 é o encoding mais universal — use-o por padrão.

---------------------------------------------------------------------------
3. Formas de ler um arquivo
---------------------------------------------------------------------------
Existem três formas, cada uma com seu caso de uso:

FORMA 1 — read(): lê o arquivo inteiro de uma vez como uma string

    with open("dados.txt", "r", encoding="utf-8") as f:
        conteudo = f.read()    # string com todo o conteúdo

    Quando usar: arquivos pequenos que cabem na memória.
    Cuidado: um arquivo de 2 GB carregado com read() vai usar 2 GB de RAM.

FORMA 2 — readlines(): lê todas as linhas como lista de strings

    with open("dados.txt", "r", encoding="utf-8") as f:
        linhas = f.readlines()    # ['linha1\n', 'linha2\n', ...]

    Cada linha inclui o '\n' no final. Use .strip() para remover:
        linhas = [l.strip() for l in f.readlines()]

FORMA 3 — iteração direta (preferida para arquivos grandes):

    with open("dados.txt", "r", encoding="utf-8") as f:
        for linha in f:              # lê uma linha por vez
            linha = linha.strip()    # remove \n e espaços
            processar(linha)

    Quando usar: arquivos grandes — lê uma linha por vez sem carregar
    tudo na memória.

---------------------------------------------------------------------------
4. Escrevendo em arquivos
---------------------------------------------------------------------------

    # Criando ou sobrescrevendo
    with open("saida.txt", "w", encoding="utf-8") as f:
        f.write("Linha 1\n")         # escreve texto (sem \n automático!)
        f.write("Linha 2\n")

    # Acrescentando ao final de um arquivo existente
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write("Nova entrada\n")

    # print() pode escrever diretamente em arquivo
    with open("saida.txt", "w", encoding="utf-8") as f:
        print("Linha 1", file=f)     # print adiciona \n automaticamente
        print("Linha 2", file=f)

    # Escrevendo múltiplas linhas de uma vez
    linhas = ["ana\n", "bruno\n", "carla\n"]
    with open("nomes.txt", "w", encoding="utf-8") as f:
        f.writelines(linhas)    # writelines NÃO adiciona \n automaticamente

DIFERENÇA entre write e print(file=...):
    write() não adiciona '\n' — você controla tudo
    print(file=f) adiciona '\n' automaticamente (comportamento padrão do print)

---------------------------------------------------------------------------
5. Pathlib: navegando o sistema de arquivos de forma moderna
---------------------------------------------------------------------------
pathlib é a forma moderna de trabalhar com caminhos de arquivo em Python.
Em vez de strings, usa objetos Path que entendem o sistema operacional:

    from pathlib import Path

    # Criando caminhos
    p = Path("dados")                   # caminho relativo
    p = Path("/home/usuario/dados")     # absoluto no Linux
    p = Path.home()                     # diretório home do usuário
    p = Path.cwd()                      # diretório atual

    # Navegando
    p = Path("projeto") / "dados" / "vendas.csv"  # / junta caminhos!
    print(p)          # projeto/dados/vendas.csv

    # Informações sobre o caminho
    p.name            # 'vendas.csv'
    p.stem            # 'vendas'      (sem extensão)
    p.suffix          # '.csv'
    p.parent          # Path('projeto/dados')
    p.exists()        # True/False
    p.is_file()       # True/False
    p.is_dir()        # True/False

    # Listando arquivos
    for arquivo in Path(".").iterdir():
        print(arquivo)

    for csv in Path("dados").glob("*.csv"):    # só arquivos .csv
        print(csv)

    # Lendo e escrevendo com pathlib diretamente
    p = Path("dados.txt")
    texto = p.read_text(encoding="utf-8")       # lê tudo de uma vez
    p.write_text("novo conteúdo", encoding="utf-8")  # escreve

    # Criando diretórios
    Path("novo_dir").mkdir(exist_ok=True)               # um nível
    Path("a/b/c").mkdir(parents=True, exist_ok=True)   # vários níveis

---------------------------------------------------------------------------
6. JSON: trocando dados estruturados
---------------------------------------------------------------------------
JSON (JavaScript Object Notation) é o formato mais usado para trocar dados
estruturados entre sistemas — APIs web, arquivos de configuração, bancos
de dados de documentos. É texto legível por humanos e máquinas.

CORRESPONDÊNCIA Python ↔ JSON:

    Python              JSON
    ----------------    ----------------
    dict                object {}
    list, tuple         array []
    str                 string ""
    int, float          number
    True / False        true / false
    None                null

AS QUATRO FUNÇÕES PRINCIPAIS:

    import json

    # Objeto Python -> string JSON (serialização)
    dados = {"nome": "Ana", "idade": 30, "ativo": True}
    texto = json.dumps(dados)
    # '{"nome": "Ana", "idade": 30, "ativo": true}'

    # String JSON -> objeto Python (desserialização)
    de_volta = json.loads(texto)
    # {'nome': 'Ana', 'idade': 30, 'ativo': True}

    # Objeto Python -> arquivo JSON
    with open("dados.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    # Arquivo JSON -> objeto Python
    with open("dados.json", "r", encoding="utf-8") as f:
        dados = json.load(f)

PARÂMETROS IMPORTANTES de dumps/dump:

    indent=2             formata o JSON com indentação (mais legível)
    ensure_ascii=False   permite caracteres acentuados no JSON
    sort_keys=True       ordena as chaves alfabeticamente

ATENÇÃO: JSON não suporta todos os tipos Python. Tentar serializar
um set, datetime ou objeto customizado sem tratamento causa TypeError:

    json.dumps({1, 2, 3})          # TypeError: Object of type set is not JSON serializable
    json.dumps(set([1, 2, 3]))     # TypeError

    # Solução: converta antes
    json.dumps(list({1, 2, 3}))    # '[1, 2, 3]'

---------------------------------------------------------------------------
7. CSV: dados tabulares
---------------------------------------------------------------------------
CSV (Comma-Separated Values) é o formato universal para dados tabulares —
planilhas, exportações de banco de dados, relatórios. Cada linha é um
registro, cada campo separado por vírgula (ou outro delimitador).

    # Exemplo de arquivo CSV:
    nome,nota,cidade
    Ana,9.5,Recife
    Bruno,7.0,São Paulo
    Carla,8.2,Belo Horizonte

LENDO COM csv.reader (devolve listas):

    import csv

    with open("alunos.csv", "r", encoding="utf-8") as f:
        leitor = csv.reader(f)
        cabecalho = next(leitor)    # lê a primeira linha (cabeçalho)
        for linha in leitor:
            print(linha)            # ['Ana', '9.5', 'Recife']

LENDO COM csv.DictReader (devolve dicionários — preferido):

    with open("alunos.csv", "r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            print(linha)
            # {'nome': 'Ana', 'nota': '9.5', 'cidade': 'Recife'}

    DictReader usa a primeira linha automaticamente como cabeçalho
    e cada linha vira um dicionário. Muito mais legível do que índices.

ATENÇÃO: CSV devolve TUDO como string. Se nota é "9.5", você precisa
converter: float(linha["nota"]) para obter o número.

ESCREVENDO COM csv.writer:

    with open("saida.csv", "w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(["nome", "nota"])     # cabeçalho
        escritor.writerow(["Ana", 9.5])
        escritor.writerows([["Bruno", 7.0], ["Carla", 8.2]])  # várias

ESCREVENDO COM csv.DictWriter:

    campos = ["nome", "nota", "cidade"]
    with open("saida.csv", "w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()     # escreve o cabeçalho automaticamente
        escritor.writerow({"nome": "Ana", "nota": 9.5, "cidade": "Recife"})

POR QUE newline=""? No Windows, sem newline="", cada linha ganha uma
linha em branco extra. É uma peculiaridade do módulo csv — sempre use.

---------------------------------------------------------------------------
8. io.StringIO: arquivo em memória para testes
---------------------------------------------------------------------------
io.StringIO cria um objeto que se comporta EXATAMENTE como um arquivo,
mas existe só na memória — nenhum arquivo real é criado no disco.

É extremamente útil para:
    - Testar código que lê/escreve arquivos sem criar arquivos reais
    - Passar "arquivos" como strings para funções que esperam arquivo
    - Processamento intermediário sem tocar o disco

    import io

    # Simula um arquivo de texto em memória
    texto = "linha1\nlinha2\nlinha3"
    f_virtual = io.StringIO(texto)

    for linha in f_virtual:
        print(linha.strip())    # linha1, linha2, linha3

    # Com csv: processa string como se fosse arquivo
    import csv
    dados_csv = "nome,nota\nAna,9.5\nBruno,7.0"
    leitor = csv.DictReader(io.StringIO(dados_csv))
    for linha in leitor:
        print(linha)
""",
    exemplos=[
        Exemplo(
            titulo="Lendo e processando arquivos de texto",
            codigo='''from pathlib import Path
import tempfile

# Cria um arquivo temporario para o exemplo
tmp = Path(tempfile.gettempdir()) / "exemplo.txt"
tmp.write_text(
    "# Comentario\\n"
    "  Ana Silva   \\n"
    "\\n"
    "  # Outro comentario\\n"
    "Bruno Costa\\n"
    "Carla Melo\\n",
    encoding="utf-8"
)

# Le e processa: ignora comentarios e linhas vazias
nomes = []
with open(tmp, "r", encoding="utf-8") as f:
    for linha in f:
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue          # pula vazias e comentarios
        nomes.append(linha)

print("Nomes encontrados:", nomes)

# Mesmo resultado com pathlib diretamente
conteudo = tmp.read_text(encoding="utf-8")
nomes2 = [
    l.strip() for l in conteudo.splitlines()
    if l.strip() and not l.strip().startswith("#")
]
print("Via pathlib:", nomes2)

# Informacoes sobre o arquivo
print(f"Tamanho: {tmp.stat().st_size} bytes")
print(f"Nome: {tmp.name}")
print(f"Extensao: {tmp.suffix}")
''',
            explicacao="O padrão de pular linhas vazias e comentários com "
                       "continue é muito comum ao processar arquivos de "
                       "configuração. "
                       "pathlib.read_text() + splitlines() é uma alternativa "
                       "concisa para arquivos pequenos. "
                       "tempfile.gettempdir() devolve um diretório temporário "
                       "que funciona em qualquer sistema operacional.",
        ),
        Exemplo(
            titulo="JSON: salvando e restaurando dados complexos",
            codigo='''import json
from pathlib import Path
import tempfile

# Dados complexos com varios tipos Python
dados = {
    "turma": "Python 2024",
    "alunos": [
        {"nome": "Ana", "nota": 9.5, "aprovado": True},
        {"nome": "Bruno", "nota": 5.8, "aprovado": False},
    ],
    "media": 7.65,
    "tags": ["iniciante", "presencial"],
    "config": None,
}

# Serializando para string (inspecao)
texto = json.dumps(dados, ensure_ascii=False, indent=2)
print(texto[:200])     # primeiras 200 letras

# Salvando em arquivo
arquivo = Path(tempfile.gettempdir()) / "turma.json"
with open(arquivo, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

# Carregando de volta
with open(arquivo, "r", encoding="utf-8") as f:
    recuperado = json.load(f)

# Verificando que e identico
print("Dados identicos:", dados == recuperado)
print("Tipo de 'alunos':", type(recuperado["alunos"]))
print("Aprovado de Ana:", recuperado["alunos"][0]["aprovado"])
''',
            explicacao="ensure_ascii=False é essencial para preservar "
                       "acentos e caracteres especiais — sem ele, 'Ana' "
                       "viraria 'Ana' mas 'José' viraria '\\u004a\\u006f...' "
                       "indent=2 torna o arquivo legível para humanos. "
                       "Após json.load, os tipos Python são restaurados: "
                       "True volta como bool, None como None, etc.",
        ),
        Exemplo(
            titulo="CSV com DictReader e io.StringIO",
            codigo='''import csv
import io

# Dados CSV como string (simula leitura de arquivo)
dados_csv = """nome,nota,cidade
Ana Silva,9.5,Recife
Bruno Costa,7.0,Sao Paulo
Carla Melo,8.2,Belo Horizonte
Diego Alves,4.5,Fortaleza"""

# Lendo com DictReader via StringIO (sem arquivo real)
leitor = csv.DictReader(io.StringIO(dados_csv))
alunos = list(leitor)

# Convertendo nota de str para float
for a in alunos:
    a["nota"] = float(a["nota"])

# Processando
aprovados = [a for a in alunos if a["nota"] >= 6.0]
print(f"Total: {len(alunos)} | Aprovados: {len(aprovados)}")

# Ordenando por nota
por_nota = sorted(alunos, key=lambda a: a["nota"], reverse=True)
print("\\nRanking:")
for pos, a in enumerate(por_nota, 1):
    status = "OK" if a["nota"] >= 6 else "Reprov"
    print(f"  {pos}. {a['nome']:<15} {a['nota']:.1f} [{status}]")

# Escrevendo resultado de volta como CSV
saida = io.StringIO()
campos = ["nome", "nota", "cidade"]
escritor = csv.DictWriter(saida, fieldnames=campos)
escritor.writeheader()
escritor.writerows(por_nota)
print("\\nCSV gerado:")
print(saida.getvalue())
''',
            explicacao="io.StringIO é perfeito para os exercícios e testes: "
                       "você passa uma string e o módulo csv a lê como "
                       "se fosse um arquivo. "
                       "DictReader é sempre preferido a reader simples "
                       "porque você acessa campos por nome, não por índice, "
                       "tornando o código autoexplicativo. "
                       "Sempre converta os campos numéricos: CSV não tem tipos.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d14e1",
            enunciado=(
                "Escreva a funcao ida_e_volta(dados) que:\n"
                "   1. Salva o dicionario 'dados' em um arquivo JSON temporario\n"
                "   2. Le o arquivo de volta\n"
                "   3. Devolve os dados recuperados\n\n"
                "Exemplos:\n"
                "   ida_e_volta({'a': 1, 'b': [2, 3]}) -> {'a': 1, 'b': [2, 3]}\n"
                "   ida_e_volta({})                    -> {}\n\n"
                "Os imports ja estao disponiveis: json, tempfile, Path.\n\n"
                "Estrategia:\n"
                "   1. Crie um caminho temporario:\n"
                "      arquivo = Path(tempfile.gettempdir()) / 'temp.json'\n"
                "   2. Salve com json.dump() dentro de with open(..., 'w'):\n"
                "   3. Leia com json.load() dentro de with open(..., 'r'):\n"
                "   4. Devolva o resultado do load\n\n"
                "O teste verifica que os dados saem identicos ao que entraram:\n"
                "tipos, valores e estrutura devem ser preservados pelo JSON."
            ),
            funcao="ida_e_volta",
            assinatura="import json\nimport tempfile\nfrom pathlib import Path\n\n\ndef ida_e_volta(dados):",
            testes=[
                ("ida_e_volta({'a': 1, 'b': [2, 3]})", "{'a': 1, 'b': [2, 3]}"),
                ("ida_e_volta({})", "{}"),
            ],
            nivel="medio",
            dica="arquivo = Path(tempfile.gettempdir()) / 'tmp.json'. Salve com json.dump e leia com json.load.",
        ),
        Exercicio(
            id="d14e2",
            enunciado=(
                "Escreva linhas_uteis(texto) que recebe uma string com\n"
                "multiplas linhas e devolve uma lista apenas com as linhas\n"
                "que nao sao vazias e nao sao comentarios (comecam com #),\n"
                "com os espacos das pontas removidos.\n\n"
                "Exemplos:\n"
                "   linhas_uteis('a\\n\\n# com\\n b ') -> ['a', 'b']\n"
                "   linhas_uteis('')                 -> []\n"
                "   linhas_uteis('#tudo comentado') -> []\n\n"
                "Estrategia:\n"
                "   1. texto.splitlines() divide a string em lista de linhas\n"
                "      (melhor que split('\\n') pois lida com diferentes\n"
                "      formatos de quebra de linha: \\r\\n, \\n, \\r)\n"
                "   2. Para cada linha: aplique .strip() para remover espacos\n"
                "   3. Filtre as linhas vazias (falsy apos strip)\n"
                "   4. Filtre as que comecam com '#'\n\n"
                "Uma compreensao resolve tudo em uma linha."
            ),
            funcao="linhas_uteis",
            assinatura="def linhas_uteis(texto):",
            testes=[
                ("linhas_uteis('a\\n\\n # com\\n b ')", "['a', 'b']"),
                ("linhas_uteis('')", "[]"),
                ("linhas_uteis('#tudo comentado')", "[]"),
            ],
            dica="[l.strip() for l in texto.splitlines() if l.strip() and not l.strip().startswith('#')]",
        ),
        Exercicio(
            id="d14e3",
            enunciado=(
                "Escreva csv_para_dicts(texto_csv) que recebe uma string\n"
                "com conteudo CSV e devolve uma lista de dicionarios,\n"
                "usando a primeira linha como cabecalho.\n"
                "Se o CSV so tiver o cabecalho (sem dados), devolve [].\n\n"
                "Exemplos:\n"
                "   csv_para_dicts('nome,nota\\nana,9\\nbia,7')\n"
                "   -> [{'nome': 'ana', 'nota': '9'}, {'nome': 'bia', 'nota': '7'}]\n\n"
                "   csv_para_dicts('a,b') -> []  (so cabecalho, sem dados)\n\n"
                "Os imports ja estao disponiveis: csv e io.\n\n"
                "Estrategia:\n"
                "   1. io.StringIO(texto_csv) transforma a string em\n"
                "      um objeto que se comporta como um arquivo\n"
                "   2. csv.DictReader(io.StringIO(texto_csv)) le o\n"
                "      CSV usando a primeira linha como chaves\n"
                "   3. list(...) materializa todos os dicionarios\n"
                "   4. Devolva a lista\n\n"
                "Nota: todos os valores no dicionario sao strings.\n"
                "O teste nao pede conversao de tipos — so a estrutura."
            ),
            funcao="csv_para_dicts",
            assinatura="import csv\nimport io\n\n\ndef csv_para_dicts(texto_csv):",
            testes=[
                ("csv_para_dicts('nome,nota\\nana,9\\nbia,7')",
                 "[{'nome': 'ana', 'nota': '9'}, {'nome': 'bia', 'nota': '7'}]"),
                ("csv_para_dicts('a,b')", "[]"),
            ],
            nivel="dificil",
            dica="return list(csv.DictReader(io.StringIO(texto_csv)))",
        ),
    ],
    quiz=[
        Quiz(
            "Por que usar 'with open(...)' em vez de 'open()' e 'close()' manual?",
            ["with e mais rapido que open/close",
             "with garante que o arquivo e sempre fechado mesmo se ocorrer um erro no bloco",
             "open() sem with causa FileNotFoundError",
             "close() foi removido no Python 3"],
            1,
            "Se uma excecao ocorrer entre open() e close(), o close() nunca e executado. "
            "O arquivo fica 'preso' (aberto sem necessidade), podendo corromper dados "
            "ou impedir outros programas de acessar o arquivo. "
            "with usa o protocolo de contexto para garantir o fechamento em qualquer situacao.",
        ),
        Quiz(
            "Qual a diferenca entre json.dumps() e json.dump()?",
            ["dumps e mais rapido que dump",
             "dumps serializa para STRING; dump serializa diretamente para ARQUIVO",
             "dump suporta mais tipos Python que dumps",
             "Nao ha diferenca — sao aliases"],
            1,
            "dumps = 'dump to string': devolve uma string JSON. "
            "dump = 'dump to file': escreve diretamente em um objeto arquivo. "
            "A mesma logica vale para loads (le de string) e load (le de arquivo).",
        ),
        Quiz(
            "Por que csv.DictReader e preferido a csv.reader simples?",
            ["DictReader e mais rapido",
             "DictReader usa a primeira linha como cabecalho e acessa campos por nome, tornando o codigo mais legivel e resistente a mudancas de ordem das colunas",
             "reader simples nao funciona com arquivos grandes",
             "DictReader converte os valores automaticamente para os tipos corretos"],
            1,
            "Com reader: linha[2] para acessar a cidade — se a coluna muda de posicao, quebra. "
            "Com DictReader: linha['cidade'] — funciona independente da ordem das colunas. "
            "Desvantagem: DictReader nao converte tipos — tudo chega como string.",
        ),
        Quiz(
            "O que io.StringIO faz e por que e util em testes?",
            ["Lê arquivos de forma mais rapida que open()",
             "Cria um objeto que se comporta como arquivo mas existe so na memoria, sem criar arquivo real no disco",
             "Converte strings para bytes automaticamente",
             "E uma alternativa ao pathlib para navegar diretorios"],
            1,
            "StringIO implementa a mesma interface de um arquivo (read, write, seek...) "
            "mas armazena os dados em memoria RAM. "
            "Em testes, isso permite verificar codigo que le/escreve arquivos "
            "sem depender do sistema de arquivos — mais rapido, sem efeitos colaterais, "
            "sem limpeza necessaria depois.",
        ),
    ],
    projeto=(
        "Crie gerenciador_contatos.py que mantenha uma lista de contatos\n"
        "persistida em JSON. O programa deve:\n\n"
        "   ESTRUTURA DE CADA CONTATO:\n"
        "   {'nome': str, 'email': str, 'telefone': str}\n\n"
        "   FUNCOES (todas sem print — so retornam):\n"
        "   1. carregar(arquivo) -> lista de contatos ([] se nao existir)\n"
        "   2. salvar(arquivo, contatos) -> None\n"
        "   3. adicionar(contatos, nome, email, telefone) -> lista atualizada\n"
        "   4. buscar(contatos, termo) -> lista com matches (nome ou email)\n"
        "   5. remover(contatos, nome) -> lista sem o contato\n"
        "   6. exportar_csv(contatos, arquivo_csv) -> None\n\n"
        "   SCRIPT PRINCIPAL:\n"
        "   - Carrega contatos de 'contatos.json'\n"
        "   - Adiciona 3 contatos novos\n"
        "   - Busca por um termo e exibe resultados\n"
        "   - Salva de volta em JSON\n"
        "   - Exporta para 'contatos.csv'\n\n"
        "BONUS: adicione validacao de email (deve conter @ e .)\n"
        "e importe contatos de um CSV existente com DictReader."
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/pathlib.html — pathlib moderno",
        "docs.python.org/pt-br/3/library/json.html — modulo json",
        "docs.python.org/pt-br/3/library/csv.html — modulo csv",
    ],
))

# ---------------------------------------------------------------- DIA 15
DIAS.append(Dia(
    numero=15,
    titulo="Erros e exceções",
    nivel="Intermediário",
    duracao="110 min",
    objetivos=[
        "Entender a diferença entre SyntaxError (antes de rodar) e exceções em tempo de execução",
        "Usar try/except/else/finally e entender o papel de cada cláusula",
        "Capturar exceções específicas em vez de usar except genérico",
        "Lançar exceções com raise e encadear com raise ... from",
        "Criar exceções personalizadas para comunicar erros do domínio do problema",
        "Reconhecer os cinco anti-padrões mais comuns no tratamento de exceções",
        "Escolher entre EAFP (peça perdão) e LBYL (peça permissão) consciente e corretamente",
    ],
    teoria="""
Todo programa encontra situações inesperadas: o arquivo não existe, o
usuário digitou texto onde se esperava número, a conexão de rede caiu.
Em Python, essas situações são representadas por EXCEÇÕES — objetos que
carregam informações sobre o que deu errado e onde.

Aprender a lidar com exceções corretamente é o que separa um programa
frágil (que trava na primeira dificuldade) de um programa robusto (que
lida com problemas de forma elegante).

---------------------------------------------------------------------------
1. SyntaxError versus exceções em tempo de execução
---------------------------------------------------------------------------
Existem dois momentos em que erros podem ocorrer em Python:

ANTES DE RODAR — SyntaxError:
O interpretador lê o arquivo, analisa a estrutura e encontra código
malformado. O programa não inicia de forma alguma.

    if x > 0      # SyntaxError: expected ':'
        print(x)  # IndentationError: expected an indented block

DURANTE A EXECUÇÃO — exceções:
O código está sintaticamente correto, mas algo dá errado enquanto roda.

    10 / 0         # ZeroDivisionError
    int("abc")     # ValueError
    lista[100]     # IndexError
    nome + 3       # TypeError (onde nome é str)
    dicionario["chave_inexistente"]  # KeyError

A distinção importa: SyntaxError é sempre um bug para corrigir.
Exceções em tempo de execução podem ser situações legítimas que o
programa deve tratar (usuário digitou dado inválido) OU bugs (você
tentou acessar um índice que não existe).

---------------------------------------------------------------------------
2. try/except/else/finally: a estrutura completa
---------------------------------------------------------------------------
    try:
        # Código que PODE gerar uma exceção
        resultado = operacao_arriscada()

    except TipoDeErro:
        # Executa SE a exceção ocorreu
        tratar_o_erro()

    else:
        # Executa SE o try terminou SEM exceção
        usar_resultado(resultado)

    finally:
        # Executa SEMPRE — com ou sem exceção
        liberar_recursos()

O PAPEL DE CADA CLÁUSULA:

    try      — delimita o código que pode falhar
    except   — o que fazer quando falha
    else     — o que fazer quando não falha (separado do try para clareza)
    finally  — limpeza que deve ocorrer em qualquer caso

Por que ter else se você pode colocar o código depois do try/except?
A diferença é sutil mas importante:

    # SEM else — código após try/except pode mascarar erros
    try:
        resultado = operacao()
    except ValueError:
        tratar()
    usar_resultado(resultado)   # se usar_resultado levantar ValueError,
                                # cai no except acima — comportamento inesperado!

    # COM else — só entra no else se operacao() não gerou exceção
    try:
        resultado = operacao()
    except ValueError:
        tratar()
    else:
        usar_resultado(resultado)  # except acima não cobre este código

finally SEMPRE executa, mesmo que haja return dentro do try ou except:

    def testar():
        try:
            return "try"
        finally:
            print("finally executou!")  # sempre imprime

    testar()   # imprime "finally executou!" e depois retorna "try"

O uso mais comum de finally é garantir que recursos sejam liberados
(fechar arquivos, encerrar conexões) mesmo quando ocorrem erros.
Mas com with (Dia 14), a maioria dos casos de finally é desnecessária.

---------------------------------------------------------------------------
3. Capturando exceções específicas
---------------------------------------------------------------------------
A regra mais importante: sempre capture a exceção MAIS ESPECÍFICA possível.

    # RUIM: captura qualquer coisa, esconde bugs
    try:
        resultado = calcular(dados)
    except:                          # nunca faça isso
        print("deu erro")

    # AINDA RUIM: Exception é ampla demais
    try:
        resultado = calcular(dados)
    except Exception as e:
        print(e)

    # BOM: exceção específica
    try:
        resultado = int(entrada)
    except ValueError:
        print("entrada não é um número inteiro")

Por que capturar genérico é ruim?
    - Esconde bugs reais (NameError, AttributeError, seu próprio código bugado)
    - Torna difícil entender o que pode dar errado
    - Pode capturar KeyboardInterrupt (Ctrl+C), impedindo o usuário de sair

CAPTURANDO MÚLTIPLOS TIPOS:

    # Varios tipos na mesma linha (tupla)
    try:
        valor = int(dados[chave])
    except (KeyError, ValueError) as e:
        print(f"Dado inválido: {e}")

    # Tratamentos diferentes para cada tipo
    try:
        valor = int(dados[chave])
    except KeyError:
        print("chave não encontrada")
    except ValueError:
        print("valor não é um número")

ACESSANDO A EXCEÇÃO COM as:

    try:
        resultado = 10 / divisor
    except ZeroDivisionError as erro:
        print(f"Erro: {erro}")          # Erro: division by zero
        print(type(erro).__name__)      # ZeroDivisionError

---------------------------------------------------------------------------
4. A hierarquia de exceções
---------------------------------------------------------------------------
As exceções formam uma hierarquia de herança. Capturar uma exceção mais
alta também captura todas as abaixo dela:

    BaseException
    ├── SystemExit          (sys.exit())
    ├── KeyboardInterrupt   (Ctrl+C)
    └── Exception           (todas as exceções "normais")
        ├── ArithmeticError
        │   ├── ZeroDivisionError
        │   └── OverflowError
        ├── LookupError
        │   ├── IndexError
        │   └── KeyError
        ├── ValueError
        ├── TypeError
        ├── AttributeError
        ├── NameError
        ├── IOError / OSError
        │   └── FileNotFoundError
        └── RuntimeError
            └── RecursionError

Regra prática: capture o nível mais baixo (mais específico) que resolve
o seu problema. Nunca capture BaseException (inclui SystemExit e
KeyboardInterrupt, o que impede o usuário de sair com Ctrl+C).

---------------------------------------------------------------------------
5. raise: lançando exceções
---------------------------------------------------------------------------
Você pode lançar exceções intencionalmente com raise — para sinalizar
que algo inválido foi fornecido à sua função:

    def calcular_raiz(n):
        if n < 0:
            raise ValueError(f"raiz de número negativo não é real: {n}")
        return n ** 0.5

    # Relançando a mesma exceção (preserva o traceback original)
    try:
        resultado = operacao()
    except ValueError as e:
        registrar_log(e)
        raise    # raise sozinho relança a exceção atual

ENCADEAMENTO DE EXCEÇÕES com raise ... from:

    def carregar_config(arquivo):
        try:
            with open(arquivo) as f:
                return json.load(f)
        except FileNotFoundError as e:
            raise RuntimeError(f"Config '{arquivo}' não encontrada") from e

    # O traceback mostrará AMBAS as exceções:
    # FileNotFoundError (causa original)
    # RuntimeError (exceção de alto nível)

Por que encadear? O chamador recebe uma exceção com significado no nível
de abstração correto ("Config não encontrada") enquanto o traceback ainda
preserva a causa técnica original (FileNotFoundError).

Para suprimir a causa original explicitamente:

    raise RuntimeError("erro") from None   # esconde a causa original

---------------------------------------------------------------------------
6. Criando exceções personalizadas
---------------------------------------------------------------------------
Criar suas próprias exceções torna o código mais expressivo e permite
que o chamador trate erros específicos do seu domínio:

    # Exceção simples (só o nome já basta na maioria dos casos)
    class SaldoInsuficiente(Exception):
        pass

    # Exceção com dados extras
    class SaldoInsuficiente(Exception):
        def __init__(self, saldo, valor):
            self.saldo = saldo
            self.valor = valor
            super().__init__(
                f"Saldo {saldo:.2f} insuficiente para saque de {valor:.2f}"
            )

    # Hierarquia de exceções do domínio
    class ErroBancario(Exception):
        pass

    class SaldoInsuficiente(ErroBancario):
        pass

    class ContaBloqueada(ErroBancario):
        pass

    # Quem usa pode capturar o geral ou o específico:
    try:
        sacar(conta, 1000)
    except SaldoInsuficiente as e:
        print(f"Saldo insuficiente: R${e.saldo:.2f}")
    except ErroBancario as e:
        print(f"Erro bancário: {e}")

CONVENÇÃO DE NOMES: sempre termine com "Error" para exceções que sinalizam
erros, ou com "Exception" para situações excepcionais não necessariamente
ruins. Exemplos: ValueError, FileNotFoundError, SaldoInsuficienteError.

---------------------------------------------------------------------------
7. EAFP versus LBYL
---------------------------------------------------------------------------
Existem duas filosofias para lidar com possíveis erros:

LBYL — Look Before You Leap (olhe antes de pular):
Verifique SE a condição é válida ANTES de tentar a operação.

    # LBYL
    if "chave" in dicionario:
        valor = dicionario["chave"]
    else:
        valor = None

    if os.path.exists(arquivo):
        with open(arquivo) as f:
            dados = f.read()

EAFP — Easier to Ask Forgiveness than Permission (mais fácil pedir perdão):
Tente a operação e trate a exceção SE ela ocorrer.

    # EAFP
    try:
        valor = dicionario["chave"]
    except KeyError:
        valor = None

    try:
        with open(arquivo) as f:
            dados = f.read()
    except FileNotFoundError:
        dados = None

PYTHON FAVORECE EAFP: é mais pythônico, evita a condição de corrida
(o arquivo pode ser apagado entre o if e o open) e frequentemente
resulta em código mais simples.

QUANDO USAR CADA UM:

    Prefira EAFP quando:
    - A operação vai falhar raramente (verificar é mais caro)
    - Há risco de condição de corrida entre verificar e agir
    - A lógica fica mais simples com try/except

    Prefira LBYL quando:
    - O erro seria frequente e try/except ficaria caro
    - A validação expressa claramente as pré-condições

---------------------------------------------------------------------------
8. Os cinco anti-padrões de exceção
---------------------------------------------------------------------------

ANTI-PADRÃO 1 — Capturar tudo silenciosamente:
    try:
        operacao()
    except:
        pass    # engole o erro sem registro — o pior de todos

ANTI-PADRÃO 2 — Usar exceções para controle de fluxo normal:
    # Exceção não deveria ser o caminho feliz
    try:
        return lista[0]
    except IndexError:
        return None
    # Melhor: return lista[0] if lista else None

ANTI-PADRÃO 3 — Capturar demais e depois verificar:
    try:
        resultado = calcular()
    except Exception as e:
        if isinstance(e, ValueError):
            tratar_valor()
        elif isinstance(e, TypeError):
            tratar_tipo()
    # Melhor: dois excepts separados

ANTI-PADRÃO 4 — Perder o traceback original:
    try:
        operacao()
    except Exception as e:
        raise RuntimeError("falhou")    # perde a causa original!
    # Melhor: raise RuntimeError("falhou") from e

ANTI-PADRÃO 5 — Usar bare except em vez de except Exception:
    try:
        operacao()
    except:              # captura KeyboardInterrupt e SystemExit!
        tratar()
    # Melhor: except Exception:
""",
    exemplos=[
        Exemplo(
            titulo="try/except/else/finally em ação",
            codigo='''import json

def carregar_json(texto):
    """Carrega JSON com tratamento completo de erros."""
    try:
        dados = json.loads(texto)          # pode levantar JSONDecodeError
    except json.JSONDecodeError as e:
        print(f"JSON inválido na posicao {e.pos}: {e.msg}")
        return None
    else:
        # So executa se try foi bem-sucedido
        print(f"JSON carregado: {len(dados)} chaves" if isinstance(dados, dict)
              else f"JSON carregado: {len(dados)} itens")
        return dados
    finally:
        # Sempre executa — util para logging, limpeza
        print("tentativa de parse concluida")

print("Teste 1:")
r1 = carregar_json('{"nome": "Ana", "idade": 30}')
print("Resultado:", r1)

print("\\nTeste 2:")
r2 = carregar_json("{invalido}")
print("Resultado:", r2)
''',
            explicacao="else executa apenas quando try não lança exceção — "
                       "é o lugar certo para 'o que fazer com o resultado'. "
                       "finally executa sempre, útil para logging de auditoria. "
                       "Capturar json.JSONDecodeError é mais específico do que "
                       "ValueError, mesmo que JSONDecodeError seja subclasse de ValueError.",
        ),
        Exemplo(
            titulo="Exceções personalizadas e encadeamento",
            codigo='''class ErroValidacao(Exception):
    """Erro base para validacoes do dominio."""
    pass

class ValorNegativo(ErroValidacao):
    def __init__(self, campo, valor):
        self.campo = campo
        self.valor = valor
        super().__init__(f"Campo '{campo}' nao pode ser negativo: {valor}")

class ValorMuitoAlto(ErroValidacao):
    def __init__(self, campo, valor, maximo):
        super().__init__(f"Campo '{campo}' ({valor}) excede o maximo ({maximo})")

def processar_pedido(quantidade, preco_unitario):
    """Processa pedido com validacao rica."""
    if quantidade < 0:
        raise ValorNegativo("quantidade", quantidade)
    if preco_unitario < 0:
        raise ValorNegativo("preco_unitario", preco_unitario)
    if quantidade > 1000:
        raise ValorMuitoAlto("quantidade", quantidade, 1000)
    return quantidade * preco_unitario

# Testando
casos = [(5, 10.0), (-1, 10.0), (5, -2.0), (2000, 1.0)]
for qtd, preco in casos:
    try:
        total = processar_pedido(qtd, preco)
        print(f"Pedido OK: qtd={qtd}, preco={preco} -> total={total}")
    except ValorNegativo as e:
        print(f"Valor negativo: {e}")
    except ValorMuitoAlto as e:
        print(f"Limite excedido: {e}")
    except ErroValidacao as e:    # captura qualquer outro erro do dominio
        print(f"Erro de validacao: {e}")
''',
            explicacao="A hierarquia ErroValidacao -> ValorNegativo / ValorMuitoAlto "
                       "permite que o chamador escolha o nível de detalhe: "
                       "capturar ErroValidacao pega qualquer erro do domínio; "
                       "capturar ValorNegativo é mais específico. "
                       "super().__init__(...) passa a mensagem para Exception, "
                       "que a armazena e exibe no traceback.",
        ),
        Exemplo(
            titulo="EAFP na prática: leitura de configuração",
            codigo='''import json
from pathlib import Path

def carregar_config(caminho, padrao=None):
    """Carrega config JSON com EAFP — trata excecoes naturalmente."""
    if padrao is None:
        padrao = {}
    try:
        texto = Path(caminho).read_text(encoding="utf-8")
        config = json.loads(texto)
        return config
    except FileNotFoundError:
        print(f"Config '{caminho}' nao encontrada — usando padrao")
        return padrao
    except json.JSONDecodeError as e:
        print(f"Config '{caminho}' corrompida: {e.msg}")
        return padrao
    except PermissionError:
        print(f"Sem permissao para ler '{caminho}'")
        return padrao

# LBYL equivalente (mais verboso e com condicao de corrida):
def carregar_config_lbyl(caminho, padrao=None):
    if padrao is None:
        padrao = {}
    p = Path(caminho)
    if not p.exists():        # arquivo pode ser apagado entre este if...
        return padrao
    if not p.is_file():
        return padrao
    try:                      # ...e este open() — condicao de corrida!
        texto = p.read_text(encoding="utf-8")
        return json.loads(texto)
    except:
        return padrao

# Testando ambas
config1 = carregar_config("config.json", {"tema": "claro"})
print("Config:", config1)
''',
            explicacao="A versão EAFP é mais curta e mais segura: não há "
                       "janela de tempo entre verificar se existe e abrir. "
                       "Em sistemas com vários processos, o arquivo pode "
                       "ser apagado entre p.exists() e p.read_text() — "
                       "a versão LBYL falharia igualmente, mas de forma "
                       "inesperada. A versão EAFP trata exatamente o erro "
                       "que ocorre.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d15e1",
            enunciado=(
                "Escreva divisao_segura(a, b) que divide a por b e devolve\n"
                "o resultado como float. Se b for zero, devolve None em\n"
                "vez de levantar ZeroDivisionError.\n\n"
                "Exemplos:\n"
                "   divisao_segura(10, 2)  -> 5.0\n"
                "   divisao_segura(1, 0)   -> None\n"
                "   divisao_segura(-9, 3)  -> -3.0\n\n"
                "Estrategia:\n"
                "   try:\n"
                "       return a / b\n"
                "   except ZeroDivisionError:\n"
                "       return None\n\n"
                "Por que 5.0 e nao 5? O operador / sempre devolve float:\n"
                "   10 / 2 = 5.0  (nao 5)\n"
                "   Use / (nao //) para divisao real."
            ),
            funcao="divisao_segura",
            assinatura="def divisao_segura(a, b):",
            testes=[
                ("divisao_segura(10, 2)", "5.0"),
                ("divisao_segura(1, 0)", "None"),
                ("divisao_segura(-9, 3)", "-3.0"),
            ],
            dica="try: return a / b. except ZeroDivisionError: return None",
        ),
        Exercicio(
            id="d15e2",
            enunciado=(
                "Escreva para_int(texto, padrao=0) que tenta converter\n"
                "'texto' para inteiro. Se nao conseguir por qualquer motivo\n"
                "(texto invalido, None, etc.), devolve 'padrao'.\n\n"
                "Exemplos:\n"
                "   para_int('42')     -> 42\n"
                "   para_int('abc')    -> 0   (ValueError: nao e numero)\n"
                "   para_int(None, -1) -> -1  (TypeError: None nao tem strip)\n"
                "   para_int('  7  ')  -> 7   (int() ignora espacos)\n\n"
                "Dois tipos de erro podem ocorrer:\n"
                "   ValueError: int('abc') — texto nao representa numero\n"
                "   TypeError:  int(None)  — tipo incompativel\n\n"
                "Capture os dois em um unico except:\n"
                "   except (ValueError, TypeError):\n"
                "       return padrao\n\n"
                "Nota: int('  7  ') funciona! int() ignora espacos nas\n"
                "pontas automaticamente — nao precisa de strip()."
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
            dica="try: return int(texto). except (ValueError, TypeError): return padrao",
        ),
        Exercicio(
            id="d15e3",
            enunciado=(
                "A classe SaldoInsuficiente ja esta definida na assinatura.\n"
                "Escreva sacar(saldo, valor) que:\n"
                "   - Levanta ValueError se valor <= 0\n"
                "   - Levanta SaldoInsuficiente se valor > saldo\n"
                "   - Devolve o novo saldo (saldo - valor) se tudo ok\n\n"
                "Exemplos:\n"
                "   sacar(100, 30)  -> 70       (saque ok)\n"
                "   sacar(100, 500) -> levanta SaldoInsuficiente\n"
                "   sacar(100, 0)   -> levanta ValueError\n"
                "   sacar(100, 100) -> 0         (zera o saldo)\n\n"
                "Use clausulas de guarda (raise early):\n"
                "   1. if valor <= 0: raise ValueError(...)\n"
                "   2. if valor > saldo: raise SaldoInsuficiente(...)\n"
                "   3. return saldo - valor\n\n"
                "O teste usa '!raise NomeDaExcecao' para verificar\n"
                "que a excecao foi levantada — faz parte do corretor."
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
            dica="Valide com raise primeiro (valor <= 0 -> ValueError, valor > saldo -> SaldoInsuficiente), depois return saldo - valor.",
        ),
    ],
    quiz=[
        Quiz(
            "Qual a diferenca entre o bloco else e o bloco finally em um try?",
            ["else e finally fazem a mesma coisa",
             "else executa apenas se o try NAO levantou excecao; finally executa SEMPRE, com ou sem excecao",
             "finally executa apenas se ocorreu excecao; else executa sempre",
             "else so funciona com excecoes personalizadas"],
            1,
            "else = 'o que fazer com o resultado quando tudo correu bem'. "
            "finally = 'limpeza que deve ocorrer aconteca o que acontecer'. "
            "Com with (Dia 14), a maioria dos usos de finally para fechar "
            "recursos e desnecessaria — with ja garante o fechamento.",
        ),
        Quiz(
            "Por que 'except:' (sem tipo) e considerado um anti-padrao grave?",
            ["E mais lento que except Exception",
             "Captura ate KeyboardInterrupt e SystemExit, impedindo o usuario de sair com Ctrl+C e engolindo todos os bugs",
             "Nao funciona com excecoes personalizadas",
             "Foi removido no Python 3.10"],
            1,
            "Bare except captura TUDO, incluindo KeyboardInterrupt (Ctrl+C) "
            "e SystemExit (sys.exit()). O usuario nao consegue encerrar o programa. "
            "Alem disso, qualquer bug no codigo (NameError, AttributeError) "
            "seria silenciado. Use sempre except Exception: no minimo, "
            "ou melhor ainda, o tipo especifico esperado.",
        ),
        Quiz(
            "O que 'raise RuntimeError(\"falhou\") from e' faz de diferente de 'raise RuntimeError(\"falhou\")'?",
            ["Nao ha diferenca — from e e opcional e ignorado",
             "Encadeia a excecao: o traceback mostra AMBAS (a original 'e' como causa e a nova RuntimeError)",
             "Suprime a excecao original e mostra so a RuntimeError",
             "from e so funciona com excecoes da biblioteca padrao"],
            1,
            "from e preserva a causa original no traceback com a mensagem "
            "'The above exception was the direct cause of the following exception'. "
            "Isso e crucial para depuracao: voce ve tanto o erro de alto nivel "
            "(RuntimeError: falhou) quanto a causa tecnica original. "
            "'raise ... from None' faz o oposto: suprime a causa original.",
        ),
        Quiz(
            "Qual filosofia Python prefere: EAFP ou LBYL?",
            ["LBYL — sempre verifique antes para evitar erros",
             "EAFP — tente a operacao e trate a excecao se ocorrer",
             "Nenhuma — Python nao tem preferencia",
             "Depende da versao do Python"],
            1,
            "Python favorece EAFP por ser mais pythonico, evitar condicoes de corrida "
            "(arquivo pode ser apagado entre verificar e abrir) e frequentemente "
            "resultar em codigo mais simples. "
            "LBYL faz sentido quando a verificacao e muito mais barata que tentar "
            "e falhar, ou quando a falha seria cara de reverter.",
        ),
    ],
    projeto=(
        "Crie validador_dados.py com um sistema robusto de validacao:\n\n"
        "   EXCECOES PERSONALIZADAS:\n"
        "   class ErroDados(Exception): pass\n"
        "   class CampoObrigatorio(ErroDados): pass\n"
        "   class TipoInvalido(ErroDados): pass\n"
        "   class ValorForaDoIntervalo(ErroDados): pass\n\n"
        "   FUNCOES:\n"
        "   1. validar_idade(valor) -> int\n"
        "      - Converte para int (TypeError/ValueError -> TipoInvalido)\n"
        "      - Verifica 0 <= idade <= 150 (-> ValorForaDoIntervalo)\n\n"
        "   2. validar_email(valor) -> str\n"
        "      - Verifica que nao e None/vazio (-> CampoObrigatorio)\n"
        "      - Verifica que contem @ e . (-> TipoInvalido)\n\n"
        "   3. validar_pessoa(dados: dict) -> dict\n"
        "      - Valida chaves 'nome', 'idade', 'email'\n"
        "      - Devolve o dicionario com tipos corretos\n"
        "      - Encadeia excecoes: raise ErroDados(...) from e\n\n"
        "   DEMONSTRACAO:\n"
        "   Teste com casos validos e invalidos, capturando cada tipo\n"
        "   de excecao separadamente e exibindo mensagens claras.\n\n"
        "BONUS: use try/except/else/finally em todas as funcoes de\n"
        "validacao e registre cada tentativa num arquivo de log."
    ),
    leitura=[
        "docs.python.org/pt-br/3/tutorial/errors.html — erros e excecoes",
        "docs.python.org/pt-br/3/library/exceptions.html — hierarquia de excecoes",
        "PEP 3134 — Exception Chaining (raise ... from)",
    ],
))