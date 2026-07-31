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
        "Entender o que significa 'função é um objeto de primeira classe' em Python",
        "Passar funções como argumentos e devolvê-las como resultado",
        "Usar lambda para criar funções anônimas curtas onde elas fazem sentido",
        "Reconhecer quando lambda prejudica a legibilidade e usar def no lugar",
        "Entender closures e como uma função pode 'lembrar' o ambiente onde nasceu",
        "Escrever funções recursivas com caso base e passo recursivo corretos",
        "Diagnosticar RecursionError e saber quando recursão vira iteração",
    ],
    teoria="""
No Dia 11 você dominou os parâmetros e o escopo de funções. Hoje vamos
explorar um nível acima: funções que recebem outras funções, funções
que geram outras funções, e funções que chamam a si mesmas.

Esses conceitos parecem abstratos no começo, mas você já usou dois deles
sem perceber: sorted(lista, key=len) passa a função len como argumento,
e map(str, numeros) passa str como argumento.

---------------------------------------------------------------------------
1. Funções são objetos de primeira classe
---------------------------------------------------------------------------
Em Python, funções são objetos como qualquer outro: podem ser atribuídas
a variáveis, guardadas em listas, passadas como argumentos e devolvidas
como resultado de outras funções.

"Primeira classe" significa que funções têm os mesmos direitos que
inteiros, strings e listas — elas não são cidadãs de segunda categoria.

    def dobrar(x):
        return x * 2

    # Atribuindo a uma variável (note: SEM parênteses — não estamos chamando)
    operacao = dobrar
    print(operacao(5))     # 10 — operacao e dobrar apontam para o mesmo objeto

    # Guardando em uma lista
    operacoes = [dobrar, abs, str]
    for op in operacoes:
        print(op(-3))      # -6   3   '-3'

    # Passando como argumento
    def aplicar(funcao, valor):
        return funcao(valor)

    aplicar(dobrar, 10)    # 20
    aplicar(abs, -7)       # 7

    # Verificando que é um objeto
    print(type(dobrar))           # <class 'function'>
    print(dobrar.__name__)        # 'dobrar'
    print(dobrar.__doc__)         # a docstring da função

A distinção crucial entre dobrar (sem parênteses) e dobrar() (com
parênteses):

    dobrar     — a função em si, como objeto, sem executar nada
    dobrar()   — chama a função e produz o resultado

Esquecer os parênteses quando você quer chamar (ou colocá-los quando
não quer) é um erro muito comum no começo.

---------------------------------------------------------------------------
2. Funções de alta ordem: recebendo e devolvendo funções
---------------------------------------------------------------------------
Uma função de ALTA ORDEM é qualquer função que:
    (a) recebe uma ou mais funções como argumento, OU
    (b) devolve uma função como resultado

Você já conhece vários exemplos da biblioteca padrão:

    sorted(lista, key=len)          # recebe a função len como argumento
    map(str, [1, 2, 3])             # recebe str como argumento
    filter(lambda x: x > 0, lista)  # recebe uma função como argumento

Escrevendo suas próprias:

    def aplicar_a_todos(funcao, lista):
        """Aplica funcao a cada elemento e devolve nova lista."""
        return [funcao(x) for x in lista]

    aplicar_a_todos(abs, [-1, -2, 3])        # [1, 2, 3]
    aplicar_a_todos(str.upper, ["a", "b"])   # ['A', 'B']

    def criar_multiplicador(fator):
        """Devolve uma funcao que multiplica por fator."""
        def multiplicar(x):
            return x * fator          # fator vem do escopo externo
        return multiplicar             # devolve a função, SEM chamá-la

    dobro = criar_multiplicador(2)
    triplo = criar_multiplicador(3)

    dobro(5)     # 10
    triplo(5)    # 15

---------------------------------------------------------------------------
3. Closures: funções que lembram o ambiente onde nasceram
---------------------------------------------------------------------------
No exemplo acima, criar_multiplicador(2) cria e devolve a função
multiplicar. Mas essa função usa a variável fator, que pertence ao
escopo de criar_multiplicador — uma função que já terminou de executar.

Como multiplicar ainda consegue acessar fator?

    # Verificando o que a closure guarda
    dobro = criar_multiplicador(2)
    print(dobro.__closure__)          # (<cell at 0x...>,)
    print(dobro.__closure__[0].cell_contents)  # 2

Python mantém as variáveis do escopo externo vivas enquanto alguma
função interna ainda puder precisar delas. Isso se chama CLOSURE —
a função "fecha sobre" (closes over) as variáveis do ambiente onde foi
criada.

Closures são poderosas para criar funções especializadas sem repetição:

    def criar_validador(minimo, maximo):
        def validar(valor):
            return minimo <= valor <= maximo
        return validar

    nota_valida = criar_validador(0, 10)
    idade_valida = criar_validador(0, 120)
    percentual_valido = criar_validador(0, 100)

    nota_valida(8)         # True
    nota_valida(15)        # False
    idade_valida(25)       # True

Cada chamada de criar_validador produz uma closure independente com
seus próprios valores de minimo e maximo capturados.

---------------------------------------------------------------------------
4. lambda: funções anônimas de uma linha
---------------------------------------------------------------------------
lambda cria uma função sem nome, em uma única expressão:

    lambda parametros: expressão

Exemplos:

    lambda x: x * 2           # equivale a def f(x): return x * 2
    lambda x, y: x + y        # dois parâmetros
    lambda: 42                 # sem parâmetros, sempre devolve 42

lambda é útil como argumento de curta duração para funções de alta ordem:

    nomes = ["ana", "carlos", "bia", "daniela"]

    # Ordenar por comprimento
    sorted(nomes, key=lambda n: len(n))    # ['ana', 'bia', 'carlos', 'daniela']

    # Ordenar por última letra
    sorted(nomes, key=lambda n: n[-1])     # ['daniela', 'bia', 'ana', 'carlos']

    # Filtrar comprimentos pares
    list(filter(lambda n: len(n) % 2 == 0, nomes))   # ['ana', 'carlos']

LIMITAÇÕES DO LAMBDA:
    - Apenas UMA expressão (não pode ter if/elif/else multilinha, for, etc.)
    - Não pode ter statements (atribuições, return explícito, try/except)
    - Não pode ter docstring

QUANDO NÃO USAR LAMBDA:

    # RUIM: lambda com nome (use def!)
    dobrar = lambda x: x * 2   # PEP 8 desaconselha isso explicitamente

    # BOM: def tem nome, docstring e mensagens de erro mais claras
    def dobrar(x):
        return x * 2

    # RUIM: lambda complexo e difícil de ler
    sorted(dados, key=lambda d: (d["idade"], -d["salario"], d["nome"].lower()))

    # BOM: extraia em uma função com nome descritivo
    def chave_ordenacao(d):
        return (d["idade"], -d["salario"], d["nome"].lower())

    sorted(dados, key=chave_ordenacao)

A regra prática: lambda é para argumentos curtos e descartáveis, onde
você não vai reutilizar a função e o nome não acrescentaria clareza.
Para qualquer coisa mais complexa, def é mais claro.

---------------------------------------------------------------------------
5. map() e filter(): funções de alta ordem clássicas
---------------------------------------------------------------------------

    map(funcao, iteravel)
    Aplica funcao a cada elemento e devolve um iterador (preguiçoso):

    list(map(str, [1, 2, 3]))            # ['1', '2', '3']
    list(map(abs, [-1, 2, -3]))          # [1, 2, 3]
    list(map(str.upper, ["a", "b"]))     # ['A', 'B']

    filter(funcao, iteravel)
    Mantém apenas os elementos onde funcao(elemento) for verdadeiro:

    list(filter(lambda x: x > 0, [-1, 2, -3, 4]))  # [2, 4]
    list(filter(None, [0, 1, "", "ok", None]))       # [1, 'ok']  (remove falsy)

Em Python moderno, compreensões de lista costumam ser preferidas por
serem mais legíveis:

    [str(x) for x in [1, 2, 3]]               # substitui map
    [x for x in lista if x > 0]               # substitui filter

Mas map() e filter() brilham quando a função já existe e tem nome:

    list(map(str.upper, palavras))             # mais direto que compreensão
    list(filter(str.isdigit, caracteres))      # mais expressivo

---------------------------------------------------------------------------
6. Recursão: uma função que chama a si mesma
---------------------------------------------------------------------------
Uma função RECURSIVA resolve um problema chamando a si mesma com uma
entrada menor, até chegar a um caso simples que ela sabe resolver
diretamente.

Toda função recursiva precisa de:

    CASO BASE: a condição mais simples, que a função resolve sem se chamar.
               Sem isso, a recursão nunca termina.

    PASSO RECURSIVO: a chamada da própria função com uma entrada MENOR,
                     aproximando-se do caso base a cada chamada.

Exemplo clássico: fatorial

    def fatorial(n):
        # Caso base: fatorial de 0 e 1 é 1 (sem chamar recursão)
        if n <= 1:
            return 1
        # Passo recursivo: n! = n * (n-1)!
        return n * fatorial(n - 1)

    fatorial(5)
    = 5 * fatorial(4)
    = 5 * 4 * fatorial(3)
    = 5 * 4 * 3 * fatorial(2)
    = 5 * 4 * 3 * 2 * fatorial(1)
    = 5 * 4 * 3 * 2 * 1
    = 120

Visualizando como uma pilha de chamadas:

    fatorial(5)     <- chamada original, aguardando resultado de fatorial(4)
      fatorial(4)   <- aguardando fatorial(3)
        fatorial(3) <- aguardando fatorial(2)
          fatorial(2) <- aguardando fatorial(1)
            fatorial(1) <- caso base! devolve 1
          fatorial(2) recebe 1, devolve 2
        fatorial(3) recebe 2, devolve 6
      fatorial(4) recebe 6, devolve 24
    fatorial(5) recebe 24, devolve 120

---------------------------------------------------------------------------
7. RecursionError: o limite de Python
---------------------------------------------------------------------------
Python tem um limite de quantas chamadas recursivas podem estar ativas
ao mesmo tempo (padrão: ~1000). Se ultrapassar:

    RecursionError: maximum recursion depth exceeded

As causas mais comuns:

    CAUSA 1 — Sem caso base:
    def contar(n):
        print(n)
        contar(n + 1)    # nunca para!

    CAUSA 2 — Caso base nunca alcançado:
    def fatorial(n):
        if n == 0: return 1
        return n * fatorial(n - 2)   # -2 pula o zero se n for ímpar!

    CAUSA 3 — Entrada muito grande:
    fatorial(10000)   # recursão com 10000 níveis estoura o limite

Você pode verificar e alterar o limite:

    import sys
    sys.getrecursionlimit()    # tipicamente 1000
    sys.setrecursionlimit(5000)  # aumenta — mas geralmente o correto é
                                  # reescrever como iteração

QUANDO USAR RECURSÃO vs ITERAÇÃO:

    Use recursão quando:
    - O problema é naturalmente recursivo (árvores, estruturas aninhadas)
    - A versão recursiva é muito mais clara que a iterativa
    - A profundidade é limitada (< algumas centenas de níveis)

    Use iteração (while/for) quando:
    - A profundidade pode ser grande
    - O problema se resolve bem com acumulador
    - Desempenho é crítico (chamadas de função têm custo)

    fatorial(10000) crasha com recursão — use um while.
    Percorrer uma árvore JSON aninhada — recursão é mais natural.

---------------------------------------------------------------------------
8. Recursão em estruturas aninhadas
---------------------------------------------------------------------------
O lugar onde recursão realmente brilha é em estruturas cujo nível de
aninhamento é desconhecido em tempo de escrita — como JSON aninhado,
árvores de diretórios, ou expressões matemáticas:

    def somar_aninhado(dados):
        \"\"\"Soma todos os numeros numa lista que pode ter listas dentro.\"\"\"
        total = 0
        for item in dados:
            if isinstance(item, list):
                total += somar_aninhado(item)  # desce um nível
            else:
                total += item
        return total

    somar_aninhado([1, [2, [3, [4]], 5]])   # 15

Com iteração, você precisaria de uma pilha manual — a recursão deixa
o código muito mais expressivo aqui.
""",
    exemplos=[
        Exemplo(
            titulo="Closures criando funções especializadas",
            codigo='''def criar_formatador(prefixo, sufixo=""):
    """Devolve uma funcao que formata texto com prefixo e sufixo."""
    def formatar(texto):
        return f"{prefixo}{texto}{sufixo}"
    return formatar     # devolve a funcao, SEM chamar

# Cada chamada cria uma closure independente
negrito = criar_formatador("**", "**")
italico = criar_formatador("_", "_")
titulo = criar_formatador("# ")
alerta = criar_formatador("[ALERTA] ")

print(negrito("Python"))     # **Python**
print(italico("Python"))     # _Python_
print(titulo("Python"))      # # Python
print(alerta("Erro grave"))  # [ALERTA] Erro grave

# Closures em lista: fabrica de multiplicadores
multiplicadores = [criar_formatador(f"{i}x: ") for i in range(1, 4)]
for fmt in multiplicadores:
    print(fmt("resultado"))
''',
            explicacao="Cada chamada de criar_formatador cria uma closure "
                       "independente com seu próprio prefixo e sufixo "
                       "capturados. As funções formatar compartilham o "
                       "mesmo código mas carregam contextos diferentes. "
                       "Isso é muito mais elegante do que criar uma classe "
                       "ou passar prefixo/sufixo em cada chamada.",
        ),
        Exemplo(
            titulo="lambda onde faz sentido, def onde não faz",
            codigo='''# Lambda apropriado: argumento curto e descartavel
dados = [
    {"nome": "Carlos", "idade": 30, "salario": 5000},
    {"nome": "Ana",    "idade": 25, "salario": 7000},
    {"nome": "Bruno",  "idade": 30, "salario": 4500},
]

# Por idade, depois por salario decrescente (empates)
por_idade_salario = sorted(dados, key=lambda d: (d["idade"], -d["salario"]))
for p in por_idade_salario:
    print(p["nome"], p["idade"], p["salario"])

print()

# Lambda inapropriado: complexo demais, extraia em funcao
# RUIM:
# resultado = sorted(dados, key=lambda d: d["nome"].split()[-1].lower() if " " in d["nome"] else d["nome"].lower())

# BOM: extraia a logica com um nome descritivo
def chave_sobrenome(d):
    """Extrai o sobrenome para ordenacao, lidando com nome simples."""
    partes = d["nome"].split()
    return partes[-1].lower()

por_sobrenome = sorted(dados, key=chave_sobrenome)
for p in por_sobrenome:
    print(p["nome"])
''',
            explicacao="Lambda com critério duplo (idade, -salario) ainda "
                       "é legível — a tupla como chave é um padrão idiomático. "
                       "Mas uma lambda com lógica condicional e múltiplas "
                       "operações de string deve virar def: tem nome descritivo, "
                       "pode ter docstring e gera mensagens de erro mais claras.",
        ),
        Exemplo(
            titulo="Recursão: visualizando a pilha de chamadas",
            codigo='''def fatorial(n, nivel=0):
    """Fatorial com visualizacao da pilha de chamadas."""
    recuo = "  " * nivel
    print(f"{recuo}fatorial({n}) chamado")

    if n <= 1:
        print(f"{recuo}-> caso base: devolvendo 1")
        return 1

    resultado = n * fatorial(n - 1, nivel + 1)
    print(f"{recuo}-> fatorial({n}) = {n} * {resultado // n} = {resultado}")
    return resultado

print(f"Resultado: {fatorial(5)}")
print()

# Recursao em estrutura aninhada
def somar_aninhado(dados):
    """Soma todos os numeros numa lista que pode ter listas dentro."""
    total = 0
    for item in dados:
        if isinstance(item, list):
            total += somar_aninhado(item)    # recursao para sublista
        else:
            total += item
    return total

print(somar_aninhado([1, [2, [3, [4]], 5]]))   # 15
print(somar_aninhado([10, [20, 30], [40]]))    # 100
''',
            explicacao="O parâmetro nivel mostra visualmente como a pilha "
                       "de chamadas se aprofunda e depois se resolve de "
                       "volta — cada chamada aguarda o resultado da próxima "
                       "antes de completar a multiplicação. "
                       "somar_aninhado mostra onde recursão brilha: "
                       "profundidade desconhecida não exige mudança no código.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d12e1",
            enunciado=(
                "Escreva a funcao ordenar_por_sobrenome(nomes) que recebe\n"
                "uma lista de nomes completos (ex: 'Ana Silva') e devolve\n"
                "a lista ordenada pelo ULTIMO nome (sobrenome).\n\n"
                "Exemplos:\n"
                "   ordenar_por_sobrenome(['Ana Silva', 'Bo Alves', 'Cris Melo'])\n"
                "   -> ['Bo Alves', 'Cris Melo', 'Ana Silva']\n"
                "      (Alves < Melo < Silva em ordem alfabetica)\n\n"
                "   ordenar_por_sobrenome([]) -> []\n\n"
                "Estrategia:\n"
                "   Use sorted() com key= recebendo uma lambda que:\n"
                "   1. Divide o nome em partes: n.split()\n"
                "      'Ana Silva' -> ['Ana', 'Silva']\n"
                "   2. Pega o ultimo elemento: [-1]\n"
                "      ['Ana', 'Silva'][-1] -> 'Silva'\n\n"
                "   sorted(nomes, key=lambda n: n.split()[-1])"
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
                "Escreva a funcao fatorial(n) de forma RECURSIVA.\n"
                "fatorial(0) = 1 e fatorial(1) = 1 (casos base).\n\n"
                "Exemplos:\n"
                "   fatorial(0)  -> 1\n"
                "   fatorial(1)  -> 1\n"
                "   fatorial(5)  -> 120  (5*4*3*2*1)\n"
                "   fatorial(10) -> 3628800\n\n"
                "A recursao funciona assim:\n"
                "   fatorial(5)\n"
                "   = 5 * fatorial(4)\n"
                "   = 5 * 4 * fatorial(3)\n"
                "   = 5 * 4 * 3 * fatorial(2)\n"
                "   = 5 * 4 * 3 * 2 * fatorial(1)\n"
                "   = 5 * 4 * 3 * 2 * 1\n"
                "   = 120\n\n"
                "Estrutura:\n"
                "   1. if n <= 1: return 1     <- caso base\n"
                "   2. return n * fatorial(n - 1)  <- passo recursivo\n\n"
                "O PASSO RECURSIVO DEVE REDUZIR n a cada chamada,\n"
                "garantindo que o caso base sera alcancado."
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
                "Escreva a funcao compor(f, g) que devolve uma NOVA FUNCAO\n"
                "h tal que h(x) == f(g(x)) — composicao matematica.\n\n"
                "Exemplos:\n"
                "   compor(lambda x: x+1, lambda x: x*2)(5)\n"
                "   -> 11   (primeiro: 5*2=10, depois: 10+1=11)\n\n"
                "   compor(str, len)('abcd')\n"
                "   -> '4'  (primeiro: len('abcd')=4, depois: str(4)='4')\n\n"
                "   callable(compor(len, str)) -> True\n"
                "   (compor deve devolver algo chamavel)\n\n"
                "Estrategia (closure):\n"
                "   def compor(f, g):\n"
                "       def h(x):          <- funcao interna que captura f e g\n"
                "           return f(g(x)) <- aplica g primeiro, f depois\n"
                "       return h            <- devolve h SEM chamar (sem parenteses)\n\n"
                "Lembre: 'return h' devolve a funcao como objeto.\n"
                "'return h(x)' chamaria a funcao — errado aqui!"
            ),
            funcao="compor",
            assinatura="def compor(f, g):",
            testes=[
                ("compor(lambda x: x + 1, lambda x: x * 2)(5)", "11"),
                ("compor(str, len)('abcd')", "'4'"),
                ("callable(compor(len, str))", "True"),
            ],
            nivel="dificil",
            dica="Defina uma funcao interna h(x) que retorna f(g(x)) e devolva h sem parenteses.",
        ),
    ],
    quiz=[
        Quiz(
            "Qual a diferenca entre escrever 'dobrar' e 'dobrar()' em Python?",
            ["Nao ha diferenca — os dois chamam a funcao",
             "'dobrar' e o objeto funcao (sem executar); 'dobrar()' CHAMA a funcao e produz o resultado",
             "'dobrar' imprime a funcao; 'dobrar()' executa silenciosamente",
             "'dobrar' so funciona dentro de outras funcoes"],
            1,
            "Sem parenteses: voce esta referenciando o OBJETO funcao, "
            "que pode ser passado como argumento, guardado em variavel, etc. "
            "Com parenteses: voce esta CHAMANDO a funcao e recebendo o resultado. "
            "sorted(lista, key=len) passa o objeto len sem chama-lo.",
        ),
        Quiz(
            "O que e uma closure em Python?",
            ["Um bloco de codigo que nao pode ser modificado",
             "Uma funcao que 'lembra' e acessa variaveis do escopo onde foi criada, mesmo apos esse escopo terminar",
             "Uma funcao sem parametros",
             "Um tipo especial de lambda"],
            1,
            "Quando criar_multiplicador(2) termina, seu escopo local desaparece — "
            "exceto pelas variaveis que a funcao interna ainda usa (como fator=2). "
            "Python mantem essas variaveis vivas enquanto a closure existir. "
            "Voce pode inspecionar com funcao.__closure__.",
        ),
        Quiz(
            "Por que toda funcao recursiva precisa de um caso base?",
            ["E so uma convencao, nao e obrigatorio",
             "Sem caso base a funcao nao pode receber argumentos",
             "Sem caso base a funcao chama a si mesma infinitamente ate RecursionError",
             "Python exige caso base na sintaxe — da SyntaxError sem ele"],
            2,
            "O caso base e a condicao de parada da recursao. "
            "Sem ele, a funcao continua chamando a si mesma, criando "
            "uma pilha cada vez maior de chamadas abertas, ate "
            "o limite ser atingido (~1000 por padrao) e RecursionError ser levantado.",
        ),
        Quiz(
            "Quando lambda deve ser preferido a def?",
            ["Sempre — lambda e mais moderno e rapido",
             "Como argumento curto e descartavel onde a expressao e simples e o nome nao acrescentaria clareza",
             "Quando a funcao precisa de mais de dois parametros",
             "Quando voce precisa de docstring na funcao"],
            1,
            "lambda brilha como key=lambda x: x[-1] em sorted() — "
            "curto, descartavel, a expressao diz tudo. "
            "Mas 'dobrar = lambda x: x*2' viola o PEP 8 (use def). "
            "Lambda complexo e dificil de depurar: mensagens de erro "
            "dizem 'lambda' no lugar do nome da funcao.",
        ),
    ],
    projeto=(
        "Crie pipeline_funcional.py implementando um mini-framework\n"
        "de transformacao de dados:\n\n"
        "   1. compor(f, g): composicao de duas funcoes (exercicio d12e3)\n\n"
        "   2. pipeline(*funcoes): recebe N funcoes e devolve uma funcao\n"
        "      que aplica todas em sequencia:\n"
        "      pipeline(f, g, h)(x) == h(g(f(x)))\n\n"
        "   3. aplicar_se(condicao, transformacao): devolve uma funcao\n"
        "      que aplica transformacao apenas se condicao(x) for True\n\n"
        "   4. Use essas funcoes para processar uma lista de textos:\n"
        "      - Remover espacos nas pontas\n"
        "      - Converter para title case\n"
        "      - Substituir espacos por hifens\n"
        "      - Mas so converter se o texto tiver mais de 3 caracteres\n\n"
        "   5. Implemente fibonacci(n) de forma recursiva e demonstre\n"
        "      o RecursionError com valores grandes (>= 1000),\n"
        "      depois implemente a versao iterativa para comparar\n\n"
        "BONUS: use @functools.lru_cache na fibonacci recursiva e\n"
        "compare o desempenho com a versao sem cache para fib(35)."
    ),
    leitura=[
        "docs.python.org/pt-br/3/howto/functional.html — programacao funcional em Python",
        "docs.python.org/pt-br/3/library/functools.html — functools (lru_cache, reduce)",
        "docs.python.org/pt-br/3/faq/programming.html#how-do-i-make-a-higher-order-function",
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
    duracao="100 min",
    objetivos=[
        "Abrir, ler e escrever arquivos de texto com with open() de forma segura",
        "Entender os modos de abertura e quando usar cada um",
        "Ler arquivos grandes linha por linha sem carregar tudo na memória",
        "Serializar e desserializar dados com o módulo json",
        "Entender o que é serializável em JSON e o que não é",
        "Ler e escrever arquivos CSV com DictReader e DictWriter",
        "Usar pathlib para operações simples de leitura e escrita",
    ],
    teoria="""
Programas que encerram e perdem tudo que foi calculado são de pouca
utilidade prática. Para persistir dados entre execuções — salvar
configurações, resultados, registros — você precisa escrever em arquivos.
Hoje vamos dominar as três formas mais comuns de arquivo em Python:
texto simples, JSON e CSV.

---------------------------------------------------------------------------
1. Abrindo arquivos: sempre use with
---------------------------------------------------------------------------
A forma correta de abrir um arquivo em Python é com o bloco with:

    with open("arquivo.txt", "r", encoding="utf-8") as f:
        conteudo = f.read()
    # arquivo já foi fechado aqui, mesmo se houve erro dentro do bloco

Por que with e não open()/close() manual?

    # Jeito manual (frágil):
    f = open("arquivo.txt", "r")
    conteudo = f.read()    # se uma exceção ocorrer aqui...
    f.close()              # ...esta linha nunca executa! arquivo fica aberto

    # Com with (seguro):
    with open("arquivo.txt", "r") as f:
        conteudo = f.read()    # exceção aqui? with fecha o arquivo mesmo assim

O with é um "gerenciador de contexto" que garante a limpeza dos recursos
(fechar o arquivo) independente de ter ocorrido erro ou não. Aprenderemos
como criar os nossos no Dia 22.

OS MODOS DE ABERTURA:

    Modo    Significado          Arquivo não existe    Conteúdo existente
    ------  -------------------  --------------------  ------------------
    'r'     leitura (padrão)     FileNotFoundError     preservado
    'w'     escrita              cria o arquivo        APAGADO (cuidado!)
    'a'     append (adicionar)   cria o arquivo        preservado, escreve no fim
    'x'     criação exclusiva    cria o arquivo        FileExistsError (seguro!)
    'r+'    leitura e escrita    FileNotFoundError     preservado
    'rb'    leitura binária      FileNotFoundError     preservado
    'wb'    escrita binária      cria o arquivo        APAGADO

SEMPRE ESPECIFIQUE O ENCODING:

    # Ruim: usa o encoding padrão do sistema (varia entre máquinas!)
    with open("dados.txt", "r") as f:
        ...

    # Bom: comportamento consistente em qualquer sistema
    with open("dados.txt", "r", encoding="utf-8") as f:
        ...

Texto com acentos pode quebrar se o encoding não for especificado,
porque o padrão varia entre Linux (UTF-8), Windows (cp1252) e outros.
Sempre use encoding="utf-8" para máxima compatibilidade.

---------------------------------------------------------------------------
2. Lendo arquivos: as três formas
---------------------------------------------------------------------------

FORMA 1 — read(): lê o arquivo inteiro de uma vez

    with open("arquivo.txt", encoding="utf-8") as f:
        conteudo = f.read()       # string com todo o conteúdo
    print(conteudo)

    Quando usar: arquivos pequenos (configurações, templates)
    Quando evitar: arquivos grandes — carrega tudo na RAM

FORMA 2 — readlines(): lê todas as linhas em uma lista

    with open("arquivo.txt", encoding="utf-8") as f:
        linhas = f.readlines()    # lista de strings, cada uma com \n
    print(linhas[0])              # 'Primeira linha\n'

    Detalhe: cada linha ainda contém o \n no final.
    Use linha.rstrip() ou linha.strip() para remover.

FORMA 3 — iteração direta (melhor para arquivos grandes)

    with open("arquivo.txt", encoding="utf-8") as f:
        for linha in f:           # lê uma linha por vez, sob demanda
            linha = linha.rstrip("\n")
            print(linha)

    Quando usar: sempre que o arquivo puder ser grande
    Por quê: só uma linha ocupa memória por vez — arquivo de 10 GB
    funciona igual a arquivo de 1 KB em termos de consumo de RAM

---------------------------------------------------------------------------
3. Escrevendo arquivos
---------------------------------------------------------------------------

    # write(): escreve uma string (não adiciona \n automaticamente!)
    with open("saida.txt", "w", encoding="utf-8") as f:
        f.write("Primeira linha\n")
        f.write("Segunda linha\n")

    # writelines(): escreve uma lista de strings (também sem \n automático)
    linhas = ["linha 1\n", "linha 2\n", "linha 3\n"]
    with open("saida.txt", "w", encoding="utf-8") as f:
        f.writelines(linhas)

    # print() também aceita arquivo como destino:
    with open("saida.txt", "w", encoding="utf-8") as f:
        print("Olá, arquivo!", file=f)    # print adiciona \n automaticamente

    # append: adiciona ao final sem apagar o que já existe
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write("Nova entrada de log\n")

CUIDADO COM 'w': ele APAGA o arquivo existente antes de escrever.
Se quiser acrescentar, use 'a'. Se quiser garantir que não vai sobrescrever
um arquivo existente, use 'x' (levanta FileExistsError se já existir).

---------------------------------------------------------------------------
4. pathlib para arquivos simples
---------------------------------------------------------------------------
Para arquivos pequenos, pathlib oferece atalhos muito convenientes:

    from pathlib import Path

    # Leitura completa em uma linha
    conteudo = Path("arquivo.txt").read_text(encoding="utf-8")

    # Escrita completa em uma linha (equivale a open com 'w')
    Path("saida.txt").write_text("conteúdo aqui", encoding="utf-8")

    # Leitura de bytes (arquivos binários)
    dados = Path("imagem.png").read_bytes()

Para arquivos grandes ou quando precisa de controle de linha por linha,
use open() com with. Para ler/escrever arquivos pequenos de uma vez,
pathlib é mais conciso.

---------------------------------------------------------------------------
5. JSON: o formato universal de dados estruturados
---------------------------------------------------------------------------
JSON (JavaScript Object Notation) é um formato de texto para representar
dados estruturados. É o formato mais usado para trocar dados entre sistemas:
APIs web, configurações, resultados de análise.

O mapeamento entre Python e JSON:

    Python              JSON
    ---------------     ---------------
    dict                object { }
    list, tuple         array [ ]
    str                 string " "
    int, float          number
    True                true
    False               false
    None                null

As quatro funções essenciais do módulo json:

    import json

    # Python -> string JSON
    json.dumps(obj)
    json.dumps(obj, indent=2)           # formatado, mais legível
    json.dumps(obj, ensure_ascii=False) # preserva acentos (não escapa para \uXXXX)

    # string JSON -> Python
    json.loads(texto)

    # Python -> arquivo JSON
    with open("dados.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

    # arquivo JSON -> Python
    with open("dados.json", encoding="utf-8") as f:
        obj = json.load(f)

O QUE NÃO É SERIALIZÁVEL EM JSON:

    json.dumps(datetime.date.today())   # TypeError!
    json.dumps(set())                   # TypeError!
    json.dumps(Path("/tmp"))            # TypeError!

    Solução: converta antes de serializar
    json.dumps(str(datetime.date.today()))   # '2026-07-28'
    json.dumps(list(meu_set))               # [...]

TUPLAS VIRAM LISTAS: json.dumps((1, 2, 3)) produz "[1, 2, 3]" — ao
deserializar, você recebe uma lista, não uma tupla de volta.

ensure_ascii=False: por padrão, json.dumps escapa caracteres não-ASCII:
"São Paulo" vira "S\u00e3o Paulo". Com ensure_ascii=False, os acentos
ficam como estão — muito mais legível no arquivo final.

---------------------------------------------------------------------------
6. CSV: tabelas como texto
---------------------------------------------------------------------------
CSV (Comma-Separated Values) é o formato mais simples para tabelas:
cada linha é um registro, cada campo separado por vírgula (ou outro
delimitador).

    nome,idade,cidade
    Ana,30,Recife
    Bruno,25,São Paulo
    Carla,35,Belo Horizonte

O módulo csv lida com casos complicados automaticamente: campos com
vírgulas dentro de aspas, campos com quebras de linha, etc.

LENDO COM DictReader (recomendado):

    import csv

    with open("dados.csv", encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            # linha é um dicionário com as chaves do cabeçalho
            print(linha["nome"], linha["idade"])

    # Por que newline=""?
    # csv precisa controlar as quebras de linha internamente
    # sem isso, pode dobrar os \r\n no Windows

IMPORTANTE: todos os valores lidos são STRINGS. Se precisar de número:
    int(linha["idade"]) ou float(linha["preco"])

ESCREVENDO COM DictWriter:

    import csv

    dados = [
        {"nome": "Ana", "nota": 9.5},
        {"nome": "Bruno", "nota": 7.0},
    ]

    with open("notas.csv", "w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=["nome", "nota"])
        escritor.writeheader()   # escreve a linha de cabeçalho
        escritor.writerows(dados)

LENDO PARA UMA LISTA DE DICIONÁRIOS de uma vez:

    with open("dados.csv", encoding="utf-8", newline="") as f:
        registros = list(csv.DictReader(f))
    # registros é uma lista de dicts — arquivo já fechado

DELIMITADOR DIFERENTE (ponto e vírgula, comum em CSV brasileiro):

    csv.DictReader(f, delimiter=";")
    csv.DictWriter(f, fieldnames=..., delimiter=";")

---------------------------------------------------------------------------
7. Usando io.StringIO para testar sem arquivos reais
---------------------------------------------------------------------------
io.StringIO cria um "arquivo em memória" — um objeto que se comporta
como arquivo, mas existe só na RAM. Muito útil para testes:

    import io
    import csv

    texto_csv = "nome,nota\nana,9\nbia,7"
    buffer = io.StringIO(texto_csv)    # "arquivo" em memória

    leitor = csv.DictReader(buffer)
    for linha in leitor:
        print(linha)    # {'nome': 'ana', 'nota': '9'}

Isso evita criar arquivos temporários só para testar código que processa
CSV — o mesmo padrão é usado nos exercícios deste dia.

---------------------------------------------------------------------------
8. Boas práticas ao trabalhar com arquivos
---------------------------------------------------------------------------
    Use sempre with — nunca open/close manual
    Sempre especifique encoding="utf-8"
    Use newline="" ao abrir arquivos CSV
    Prefira iteração linha por linha para arquivos grandes
    Trate FileNotFoundError quando o arquivo pode não existir
    Para JSON com acentos: ensure_ascii=False
    Lembre: valores de CSV são sempre strings — converta se necessário
    Para arquivos críticos, escreva em temporário e renomeie (atômico)
""",
    exemplos=[
        Exemplo(
            titulo="Lendo e escrevendo arquivos de texto",
            codigo='''from pathlib import Path

# Criando um arquivo de exemplo
Path("/tmp/notas.txt").write_text(
    "# Arquivo de notas de estudo\n"
    "Python e uma linguagem incrivel\n"
    "\n"
    "# Topicos aprendidos:\n"
    "- variaveis e tipos\n"
    "- funcoes e modulos\n"
    "- arquivos e JSON\n",
    encoding="utf-8"
)

# Lendo linha por linha (eficiente para qualquer tamanho)
print("=== Linhas uteis (sem comentarios e vazias): ===")
with open("/tmp/notas.txt", encoding="utf-8") as f:
    for linha in f:
        linha = linha.strip()
        if linha and not linha.startswith("#"):
            print(" ", linha)

# Adicionando ao final (modo append)
with open("/tmp/notas.txt", "a", encoding="utf-8") as f:
    f.write("- arquivos CSV\n")

# Lendo tudo de uma vez para verificar
conteudo = Path("/tmp/notas.txt").read_text(encoding="utf-8")
print(f"\nTotal de linhas: {len(conteudo.splitlines())}")
''',
            explicacao="A iteração direta 'for linha in f' é a forma mais "
                       "eficiente: apenas uma linha fica na memória por vez. "
                       "Para filtrar, use condições dentro do loop. "
                       "Modo 'a' (append) adiciona ao final sem apagar — "
                       "ideal para logs onde cada execução acrescenta.",
        ),
        Exemplo(
            titulo="JSON: ida e volta com dados complexos",
            codigo='''import json
from pathlib import Path
from datetime import date

# Dados com tipos variados
config = {
    "app": "MeuSistema",
    "versao": "1.0.0",
    "debug": False,
    "max_usuarios": 1000,
    "taxa_desconto": 0.15,
    "funcionalidades": ["login", "relatorio", "exportar"],
    "banco": {
        "host": "localhost",
        "porta": 5432,
    },
    "criado_em": str(date.today()),   # date nao e serializavel, converta!
}

# Serializando para string (visualizacao)
texto = json.dumps(config, indent=2, ensure_ascii=False)
print(texto[:200], "...")

# Salvando em arquivo
arquivo = Path("/tmp/config.json")
with open(arquivo, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# Carregando de volta
with open(arquivo, encoding="utf-8") as f:
    carregado = json.load(f)

print(f"\nApp: {carregado['app']}")
print(f"Funcionalidades: {carregado['funcionalidades']}")
print(f"Tipos recuperados: debug={type(carregado['debug']).__name__}, "
      f"max={type(carregado['max_usuarios']).__name__}")
''',
            explicacao="indent=2 torna o JSON legível por humanos. "
                       "ensure_ascii=False preserva acentos como estão "
                       "em vez de escapar para \\uXXXX. "
                       "date não é serializável diretamente — convertemos "
                       "para string antes. Ao carregar, o JSON preserva os "
                       "tipos: bool, int e float voltam como Python nativo.",
        ),
        Exemplo(
            titulo="CSV: lendo e escrevendo tabelas",
            codigo='''import csv
import io
from pathlib import Path

# Criando um CSV de exemplo
dados = [
    {"nome": "Ana", "nota": 9.5, "aprovado": True},
    {"nome": "Bruno", "nota": 5.0, "aprovado": False},
    {"nome": "Carla", "nota": 7.8, "aprovado": True},
]

arquivo = Path("/tmp/turma.csv")
with open(arquivo, "w", encoding="utf-8", newline="") as f:
    escritor = csv.DictWriter(f, fieldnames=["nome", "nota", "aprovado"])
    escritor.writeheader()
    escritor.writerows(dados)

print("CSV criado:")
print(arquivo.read_text(encoding="utf-8"))

# Lendo de volta
print("Lendo o CSV:")
with open(arquivo, encoding="utf-8", newline="") as f:
    for linha in csv.DictReader(f):
        # TODOS os valores sao strings! converta o que precisar
        nome = linha["nome"]
        nota = float(linha["nota"])          # converte para float
        aprovado = linha["aprovado"] == "True"  # converte para bool
        print(f"  {nome}: {nota:.1f} ({'Aprovado' if aprovado else 'Reprovado'})")
''',
            explicacao="DictWriter.writeheader() escreve a linha de cabeçalho. "
                       "writerows() escreve todos os registros de uma vez. "
                       "Na leitura, TUDO vira string: nota '9.5' não é o "
                       "float 9.5, e 'True' não é o bool True. "
                       "Sempre converta os tipos ao ler CSV.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d14e1",
            enunciado=(
                "Escreva a funcao ida_e_volta(dados) que:\n"
                "   1. Converte o dicionario para JSON e salva em um\n"
                "      arquivo temporario em /tmp\n"
                "   2. Le o arquivo de volta\n"
                "   3. Devolve o objeto Python recuperado\n\n"
                "Exemplos:\n"
                "   ida_e_volta({'a': 1, 'b': [2, 3]}) -> {'a': 1, 'b': [2, 3]}\n"
                "   ida_e_volta({}) -> {}\n\n"
                "Estrategia:\n"
                "   1. Escolha um caminho temporario:\n"
                "      arquivo = Path('/tmp') / 'temp_ida_volta.json'\n"
                "   2. Escreva o JSON:\n"
                "      with open(arquivo, 'w', encoding='utf-8') as f:\n"
                "          json.dump(dados, f)\n"
                "   3. Leia de volta:\n"
                "      with open(arquivo, encoding='utf-8') as f:\n"
                "          return json.load(f)\n\n"
                "O modulo json e pathlib ja estao importados na assinatura."
            ),
            funcao="ida_e_volta",
            assinatura="import json\nimport tempfile\nfrom pathlib import Path\n\n\ndef ida_e_volta(dados):",
            testes=[
                ("ida_e_volta({'a': 1, 'b': [2, 3]})", "{'a': 1, 'b': [2, 3]}"),
                ("ida_e_volta({})", "{}"),
            ],
            nivel="medio",
            dica="arquivo = Path('/tmp/temp_ida_volta.json'); json.dump(...); depois json.load(...)",
        ),
        Exercicio(
            id="d14e2",
            enunciado=(
                "Escreva a funcao linhas_uteis(texto) que recebe um texto\n"
                "com multiplas linhas e devolve uma lista com apenas as\n"
                "linhas que tenham conteudo real:\n"
                "   - Remove espacos das pontas de cada linha\n"
                "   - Descarta linhas vazias (apos o strip)\n"
                "   - Descarta linhas que comecam com # (comentarios)\n\n"
                "Exemplos:\n"
                "   linhas_uteis('a\\n\\n # com\\n b ')\n"
                "   -> ['a', 'b']\n"
                "   (espaco antes do # conta: ' # com' comeca com espaco, nao #\n"
                "    mas apos strip() vira '# com', que comeca com #)\n\n"
                "   linhas_uteis('') -> []\n"
                "   linhas_uteis('#tudo comentado') -> []\n\n"
                "Estrategia:\n"
                "   1. texto.splitlines() divide em lista de linhas\n"
                "   2. Para cada linha: linha = linha.strip()\n"
                "   3. Descarte se vazia (not linha) ou comentario (startswith('#'))\n"
                "   4. Inclua o restante na lista resultado"
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
                "Escreva csv_para_dicts(texto_csv) que converte um texto\n"
                "no formato CSV (com cabecalho) em uma lista de dicionarios.\n\n"
                "Exemplos:\n"
                "   csv_para_dicts('nome,nota\\nana,9\\nbia,7')\n"
                "   -> [{'nome': 'ana', 'nota': '9'}, {'nome': 'bia', 'nota': '7'}]\n\n"
                "   csv_para_dicts('a,b')\n"
                "   -> []  (so tem cabecalho, sem dados)\n\n"
                "O truque: io.StringIO transforma uma STRING em um objeto\n"
                "que se comporta como arquivo, sem criar arquivo real no disco.\n\n"
                "Estrategia:\n"
                "   1. buffer = io.StringIO(texto_csv)\n"
                "      (cria um 'arquivo em memoria' a partir da string)\n"
                "   2. leitor = csv.DictReader(buffer)\n"
                "      (DictReader usa o 1o linha como cabecalho das chaves)\n"
                "   3. return list(leitor)\n"
                "      (materializa todos os registros em uma lista)\n\n"
                "csv e io ja estao importados na assinatura."
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
            "Por que usar 'with open(...)' em vez de open() e close() separados?",
            ["with open e mais rapido que open manual",
             "with garante que o arquivo sera fechado mesmo se ocorrer uma excecao dentro do bloco",
             "open() sem with nao consegue ler arquivos grandes",
             "E apenas uma questao de estilo — os dois funcionam igualmente"],
            1,
            "Se uma excecao ocorrer entre open() e close() manual, o close() "
            "nunca executa e o arquivo fica aberto, ocupando recursos do sistema. "
            "with garante a limpeza independente do que acontecer — "
            "mesmo com return, break ou excecao no meio do bloco.",
        ),
        Quiz(
            "O que acontece com o conteudo existente ao abrir um arquivo no modo 'w'?",
            ["O conteudo e preservado e a escrita e adicionada ao final",
             "O arquivo e bloqueado para escrita por outros programas",
             "O conteudo e completamente APAGADO antes de qualquer escrita",
             "Python levanta FileExistsError se o arquivo ja existir"],
            2,
            "'w' trunca (apaga) o arquivo ao abri-lo, mesmo antes de escrever qualquer coisa. "
            "Para adicionar ao final sem apagar: use 'a' (append). "
            "Para criar apenas se nao existir: use 'x' (exclusivo).",
        ),
        Quiz(
            "Qual o tipo de todos os valores lidos por csv.DictReader?",
            ["O tipo original: int para numeros, str para texto",
             "str (string) — CSV e texto puro, sem informacao de tipo",
             "dict para cada linha",
             "Depende do cabecalho do arquivo"],
            1,
            "CSV e um formato de texto puro — nao tem como saber se '9' e um "
            "inteiro ou um texto de um digito. DictReader sempre devolve strings. "
            "Voce e responsavel por converter: int(linha['idade']), float(linha['preco']).",
        ),
        Quiz(
            "Por que json.dumps({'nome': 'Sao Paulo'}, ensure_ascii=True) e ruim?",
            ["ensure_ascii=True e o padrao e nao afeta acentos",
             "Com ensure_ascii=True, caracteres nao-ASCII como acentos sao escapados para \\uXXXX, tornando o arquivo ilegivel",
             "ensure_ascii=True faz json.dumps falhar com ValueError",
             "Nao ha diferenca — o resultado e identico"],
            1,
            "Com ensure_ascii=True (padrao), 'Sao Paulo' fica como 'S\\u00e3o Paulo'. "
            "Com ensure_ascii=False, fica como 'Sao Paulo' — muito mais legivel. "
            "Use sempre ensure_ascii=False para arquivos que humanos vao ler.",
        ),
    ],
    projeto=(
        "Crie sistema_notas.py que gerencie notas de alunos em CSV e JSON:\n\n"
        "   ESTRUTURA DE DADOS:\n"
        "   Um CSV com colunas: nome, nota1, nota2, nota3\n\n"
        "   FUNCOES A IMPLEMENTAR:\n\n"
        "   1. carregar_csv(caminho) -> lista de dicts\n"
        "      Le o CSV e converte as notas para float\n\n"
        "   2. calcular_medias(alunos) -> lista de dicts com media\n"
        "      Adiciona 'media' e 'situacao' (Aprovado/Reprovado) a cada dict\n\n"
        "   3. salvar_relatorio_json(alunos, caminho)\n"
        "      Salva o relatorio completo em JSON com indent=2\n\n"
        "   4. salvar_aprovados_csv(alunos, caminho)\n"
        "      Salva apenas os aprovados em um novo CSV\n\n"
        "   5. resumo(alunos) -> dict\n"
        "      Retorna: total, aprovados, reprovados, media_turma, melhor_aluno\n\n"
        "   EXECUCAO:\n"
        "   Crie um CSV de exemplo com 5 alunos, processe e salve\n"
        "   o relatorio JSON e o CSV de aprovados.\n\n"
        "BONUS: use try/except ao carregar o CSV para tratar\n"
        "FileNotFoundError (arquivo nao existe) e\n"
        "ValueError (nota nao e numero valido)."
    ),
    leitura=[
        "docs.python.org/pt-br/3/tutorial/inputoutput.html — arquivos",
        "docs.python.org/pt-br/3/library/json.html — modulo json",
        "docs.python.org/pt-br/3/library/csv.html — modulo csv",
    ],
))
# ---------------------------------------------------------------- DIA 15
DIAS.append(Dia(
    numero=15,
    titulo="Erros e exceções",
    nivel="Intermediário",
    duracao="100 min",
    objetivos=[
        "Entender a diferença entre erros de sintaxe e exceções de tempo de execução",
        "Usar try/except/else/finally e entender o papel exato de cada bloco",
        "Capturar exceções específicas em vez de genéricas, e saber por que isso importa",
        "Levantar exceções com raise para sinalizar problemas no próprio código",
        "Criar exceções personalizadas que comunicam erros do seu domínio",
        "Diferenciar o estilo EAFP (pythônico) do estilo LBYL (de outras linguagens)",
        "Reconhecer os anti-padrões mais comuns no tratamento de exceções",
    ],
    teoria="""
Até agora, quando algo dava errado no seu código, o programa parava e
mostrava um traceback. Isso é útil durante o desenvolvimento, mas um
programa real precisa lidar com erros de forma elegante: tentar de novo,
usar um valor padrão, registrar o problema e continuar.

---------------------------------------------------------------------------
1. Dois tipos de erro: sintaxe versus exceção
---------------------------------------------------------------------------
Python tem dois tipos de erro fundamentalmente diferentes:

ERRO DE SINTAXE (SyntaxError):
Acontece ANTES do programa rodar. O Python analisa o arquivo e detecta
código que viola as regras gramaticais da linguagem:

    if x > 0      # SyntaxError: faltou o dois-pontos
    def f(        # SyntaxError: parêntese não fechado
    x === 5       # SyntaxError: === não existe em Python

O programa não inicia de forma alguma quando há SyntaxError.

EXCEÇÃO (Exception):
Acontece DURANTE a execução, quando uma operação que parecia válida
encontra um problema em tempo de execução:

    10 / 0           # ZeroDivisionError: divisão por zero
    int("abc")       # ValueError: valor inválido para a conversão
    lista[100]       # IndexError: índice fora do alcance
    nome_inexistente # NameError: nome não foi definido

O programa estava rodando normalmente e então algo deu errado. Exceções
podem — e devem — ser capturadas e tratadas pelo seu código.

---------------------------------------------------------------------------
2. try/except/else/finally: a estrutura completa
---------------------------------------------------------------------------
    try:
        # código que PODE gerar uma exceção
        resultado = int(input("Digite um número: "))
    except ValueError:
        # executado SE ocorrer um ValueError
        print("Isso não é um número válido!")
        resultado = 0
    except ZeroDivisionError:
        # executado SE ocorrer ZeroDivisionError
        print("Não pode dividir por zero!")
    else:
        # executado SOMENTE SE nenhuma exceção ocorreu no try
        print(f"Número lido com sucesso: {resultado}")
    finally:
        # executado SEMPRE — com ou sem exceção, com ou sem return
        print("Processamento concluído.")

O papel de cada bloco:

    try       — o código "arriscado" que pode falhar
    except    — o que fazer quando falha (pode ter vários, para tipos diferentes)
    else      — o que fazer quando DEU CERTO (sem exceção)
    finally   — limpeza que deve ocorrer independente do resultado

else É SUBUTILIZADO MAS MUITO ÚTIL:
Separa "o código que pode falhar" do "código que roda após o sucesso":

    # Sem else: o print pode mascarar erros
    try:
        dados = carregar_arquivo("config.json")
        print("Arquivo carregado!")    # e se print falhar?
    except FileNotFoundError:
        print("Arquivo não encontrado")

    # Com else: fica claro o que é crítico e o que vem depois
    try:
        dados = carregar_arquivo("config.json")
    except FileNotFoundError:
        print("Arquivo não encontrado")
    else:
        print("Arquivo carregado!")    # só roda se não houve exceção

finally GARANTE EXECUÇÃO:
finally executa mesmo com return, break ou uma nova exceção:

    def ler_arquivo(caminho):
        f = open(caminho)
        try:
            return f.read()       # return não impede o finally
        finally:
            f.close()             # SEMPRE executa, mesmo com o return acima
            print("arquivo fechado")

(Na prática, use with open() — mas o exemplo mostra o poder do finally)

---------------------------------------------------------------------------
3. Capturando exceções específicas
---------------------------------------------------------------------------
NUNCA capture exceções mais amplas do que o necessário:

    # PÉSSIMO: captura tudo, engole erros silenciosamente
    try:
        resultado = calcular(x)
    except:
        pass    # o programa falhou, mas você nunca vai saber por quê!

    # RUIM: Exception captura quase tudo, ainda muito amplo
    try:
        resultado = calcular(x)
    except Exception:
        pass    # ainda esconde o problema real

    # BOM: captura apenas o que você sabe tratar
    try:
        resultado = calcular(x)
    except ZeroDivisionError:
        resultado = 0    # sei exatamente por que falhou e o que fazer

CAPTURANDO MÚLTIPLOS TIPOS:

    # Opção 1: um except para cada tipo (tratamentos diferentes)
    try:
        valor = int(texto)
    except ValueError:
        print("Texto inválido para conversão")
    except TypeError:
        print("O argumento não é texto")

    # Opção 2: tupla para o mesmo tratamento
    try:
        valor = int(texto)
    except (ValueError, TypeError):
        valor = 0    # ambos recebem o mesmo tratamento

ACESSANDO OS DETALHES DA EXCEÇÃO:

    try:
        int("abc")
    except ValueError as e:
        print(f"Erro: {e}")             # invalid literal for int() with base 10: 'abc'
        print(f"Tipo: {type(e).__name__}")  # ValueError
        print(e.args)                   # ('invalid literal...',)

---------------------------------------------------------------------------
4. A hierarquia de exceções
---------------------------------------------------------------------------
Exceções em Python formam uma hierarquia de herança. Conhecer os
principais ramos ajuda a capturar no nível certo:

    BaseException
    ├── SystemExit          (sys.exit() — NÃO capture, a não ser que saiba o que faz)
    ├── KeyboardInterrupt   (Ctrl+C — NÃO capture na maioria dos casos)
    └── Exception           (a base de praticamente tudo que você vai capturar)
        ├── ArithmeticError
        │   └── ZeroDivisionError
        ├── LookupError
        │   ├── IndexError
        │   └── KeyError
        ├── OSError
        │   ├── FileNotFoundError
        │   └── PermissionError
        ├── ValueError
        ├── TypeError
        ├── AttributeError
        ├── NameError
        └── RuntimeError
            └── RecursionError

Por que isso importa? Se você captura ArithmeticError, captura todos
os seus filhos: ZeroDivisionError, OverflowError, etc. Capture sempre
o nível mais específico que faz sentido para o seu caso.

SOBRE except Exception: é aceitável apenas na "fronteira" do programa —
o ponto mais alto onde você quer registrar erros inesperados antes de
encerrar graciosamente. Nunca no meio da lógica de negócio.

---------------------------------------------------------------------------
5. Levantando exceções com raise
---------------------------------------------------------------------------
Você não é apenas receptor de exceções — pode levantá-las para comunicar
problemas ao código que chamou a sua função:

    def dividir(a, b):
        if b == 0:
            raise ValueError("O divisor não pode ser zero")
        return a / b

    def definir_idade(idade):
        if not isinstance(idade, int):
            raise TypeError(f"Idade deve ser int, recebi {type(idade).__name__}")
        if idade < 0 or idade > 150:
            raise ValueError(f"Idade {idade} está fora do intervalo válido (0-150)")
        self.idade = idade

RE-LEVANTANDO A EXCEÇÃO ATUAL:
Dentro de um except, raise sozinho re-levanta a exceção capturada:

    try:
        processar()
    except ValueError as e:
        registrar_erro(e)    # registra o erro
        raise               # re-levanta a mesma exceção para cima

ENCADEAMENTO DE EXCEÇÕES:
Preserve a causa original ao converter um tipo de exceção em outro:

    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as e:
        raise ValueError("Configuração inválida") from e
        # O traceback vai mostrar que ValueError foi CAUSADO por JSONDecodeError

Sem o "from e", a causa original seria perdida — quem depura não
saberia que o verdadeiro problema era JSON malformado.

---------------------------------------------------------------------------
6. Exceções personalizadas: comunicando erros do seu domínio
---------------------------------------------------------------------------
Criar suas próprias exceções permite comunicar erros específicos do
problema que você está resolvendo, em vez de reutilizar exceções
genéricas que podem não fazer sentido no contexto:

    # Hierarquia de exceções do seu sistema
    class ErroDeNegocio(Exception):
        """Classe base para todos os erros de negócio do sistema."""
        pass

    class SaldoInsuficiente(ErroDeNegocio):
        def __init__(self, saldo_atual, valor_solicitado):
            self.saldo_atual = saldo_atual
            self.valor_solicitado = valor_solicitado
            self.faltam = valor_solicitado - saldo_atual
            mensagem = (
                f"Saldo insuficiente: tem R$ {saldo_atual:.2f}, "
                f"precisa de R$ {valor_solicitado:.2f} "
                f"(faltam R$ {self.faltam:.2f})"
            )
            super().__init__(mensagem)

    class LimiteExcedido(ErroDeNegocio):
        pass

Usando a hierarquia:

    try:
        conta.sacar(1000)
    except SaldoInsuficiente as e:
        print(e)                        # mensagem formatada
        print(f"Faltam: R$ {e.faltam:.2f}")  # dados estruturados
    except ErroDeNegocio:
        print("Erro de negócio genérico")   # captura qualquer filho

A vantagem: quem captura SaldoInsuficiente tem acesso a saldo_atual,
valor_solicitado e faltam como atributos — não precisa fazer parsing
da mensagem de erro para extrair os valores.

---------------------------------------------------------------------------
7. EAFP versus LBYL: dois estilos de programação defensiva
---------------------------------------------------------------------------
Existem duas filosofias para lidar com situações que podem dar errado:

LBYL — "Look Before You Leap" (Olhe antes de pular):
Verificar se está tudo certo ANTES de tentar a operação:

    # Estilo LBYL
    if "chave" in dicionario:
        valor = dicionario["chave"]
    else:
        valor = padrao

    if os.path.exists(caminho):
        with open(caminho) as f:
            conteudo = f.read()

EAFP — "Easier to Ask Forgiveness than Permission" (É mais fácil pedir
perdão do que permissão):
Tentar a operação e tratar o erro se ocorrer:

    # Estilo EAFP
    try:
        valor = dicionario["chave"]
    except KeyError:
        valor = padrao

    try:
        with open(caminho) as f:
            conteudo = f.read()
    except FileNotFoundError:
        conteudo = ""

EAFP É O ESTILO PYTHÔNICO. Por quê?

    RAZÃO 1 — Condições de corrida: no LBYL, entre o if os.path.exists()
    e o open(), outro processo pode excluir o arquivo. A janela de tempo
    é pequena mas real. EAFP não tem esse problema.

    RAZÃO 2 — Performance: verificar antes paga o custo da verificação
    SEMPRE. EAFP paga o custo do except apenas quando há falha (que
    esperamos ser raro).

    RAZÃO 3 — Clareza: EAFP separa o caminho feliz (try) do caminho
    de erro (except) de forma clara.

QUANDO LBYL AINDA FAZ SENTIDO:
Quando a verificação é barata, óbvia e a falha seria crítica:

    if not isinstance(x, (int, float)):
        raise TypeError("x deve ser número")
    # agora podemos usar x com segurança

---------------------------------------------------------------------------
8. Anti-padrões a evitar
---------------------------------------------------------------------------

ANTI-PADRÃO 1 — except vazio ou genérico demais:

    try:
        algo()
    except:          # captura TUDO, incluindo KeyboardInterrupt
        pass         # engole o erro silenciosamente — debugging nightmare

ANTI-PADRÃO 2 — except Exception: pass:
Similar ao anterior — esconde erros reais que você precisaria saber.

ANTI-PADRÃO 3 — Usar exceção para controle de fluxo normal:

    # MAU USO: exceção como goto
    try:
        for item in lista:
            if item == alvo:
                raise StopIteration("Encontrou!")
    except StopIteration:
        pass    # use break no lugar!

ANTI-PADRÃO 4 — Capturar e re-levantar sem adicionar informação:

    try:
        processar()
    except ValueError as e:
        raise ValueError(str(e))    # inútil — só adiciona ruído ao traceback

ANTI-PADRÃO 5 — Esconder a causa original:

    try:
        resultado = json.loads(texto)
    except json.JSONDecodeError:
        raise ValueError("Dados inválidos")  # perdeu a causa original!
        # Use: raise ValueError("Dados inválidos") from e
""",
    exemplos=[
        Exemplo(
            titulo="try/except/else/finally em ação",
            codigo='''def ler_numero(texto):
    """Converte texto para inteiro com tratamento completo."""
    try:
        numero = int(texto.strip())
    except ValueError:
        print(f"  -> '{texto}' nao e um numero valido")
        return None
    except AttributeError:
        print(f"  -> Esperava texto, recebi {type(texto).__name__}")
        return None
    else:
        # So executa se nenhuma excecao ocorreu
        print(f"  -> Convertido com sucesso: {numero}")
        return numero
    finally:
        # Sempre executa — util para logging, limpeza, etc.
        print(f"  -> Tentativa finalizada para: {repr(texto)}")

# Testando com casos variados
for entrada in ["42", " 7 ", "abc", None, "3.14", "-10"]:
    print(f"\nProcessando {repr(entrada)}:")
    resultado = ler_numero(entrada)
    print(f"  Resultado: {resultado}")
''',
            explicacao="else executa apenas quando o try completou sem erros "
                       "— é o lugar certo para código que depende do sucesso "
                       "do try mas não precisa de tratamento de erro. "
                       "finally sempre executa, mesmo com return dentro do try "
                       "— ideal para logging e limpeza de recursos.",
        ),
        Exemplo(
            titulo="Exceção personalizada com dados estruturados",
            codigo='''class ErroDeNegocio(Exception):
    """Base para erros de negocio do sistema bancario."""
    pass

class SaldoInsuficiente(ErroDeNegocio):
    def __init__(self, saldo, valor):
        self.saldo = saldo
        self.valor = valor
        self.faltam = valor - saldo
        super().__init__(
            f"Saldo R${saldo:.2f} insuficiente para saque de R${valor:.2f} "
            f"(faltam R${self.faltam:.2f})"
        )

class ValorInvalido(ErroDeNegocio):
    pass

def sacar(saldo, valor):
    if valor <= 0:
        raise ValorInvalido(f"Valor de saque deve ser positivo, recebi {valor}")
    if valor > saldo:
        raise SaldoInsuficiente(saldo, valor)
    return saldo - valor

# Testando
for saldo, valor in [(100, 30), (100, 150), (100, 0), (50, 50)]:
    try:
        novo_saldo = sacar(saldo, valor)
        print(f"Saque R${valor:.2f}: OK. Novo saldo: R${novo_saldo:.2f}")
    except SaldoInsuficiente as e:
        print(f"NEGADO: {e}")
        print(f"  Deposite pelo menos R${e.faltam:.2f} para continuar")
    except ErroDeNegocio as e:
        print(f"ERRO DE NEGOCIO: {e}")
''',
            explicacao="A hierarquia ErroDeNegocio -> SaldoInsuficiente permite "
                       "capturar especificamente (except SaldoInsuficiente) "
                       "ou genericamente (except ErroDeNegocio). "
                       "Carregar dados na exceção (saldo, valor, faltam) "
                       "evita fazer parsing da mensagem de texto para "
                       "extrair valores — muito mais robusto.",
        ),
        Exemplo(
            titulo="EAFP versus LBYL: comparando os estilos",
            codigo='''# Cenario: acessar uma chave em dicionario que pode nao existir

dados = {"nome": "Ana", "idade": 30}

# Estilo LBYL (comum em C, Java)
if "email" in dados:
    email = dados["email"]
else:
    email = "nao informado"
print("LBYL:", email)

# Estilo EAFP (pythônico)
try:
    email = dados["email"]
except KeyError:
    email = "nao informado"
print("EAFP:", email)

# Para dicionario, .get() e ainda mais simples
email = dados.get("email", "nao informado")
print("get():", email)

# Cenario onde EAFP e claramente superior: multiplas condicoes
import os

# LBYL: multiplas verificacoes (e ainda pode falhar entre elas!)
caminho = "/tmp/arquivo_inexistente.txt"
if os.path.exists(caminho) and os.access(caminho, os.R_OK):
    with open(caminho) as f:
        conteudo = f.read()
else:
    conteudo = ""

# EAFP: tenta direto, trata se falhar
try:
    with open(caminho) as f:
        conteudo = f.read()
except (FileNotFoundError, PermissionError):
    conteudo = ""

print("Conteudo:", repr(conteudo))
''',
            explicacao="Para dicionários, .get() é a forma mais idiomática "
                       "quando há um valor padrão simples. "
                       "Para arquivos, EAFP é claramente melhor: o LBYL "
                       "faz duas chamadas ao sistema operacional (exists + access) "
                       "e ainda pode falhar entre elas se outro processo "
                       "alterar o arquivo nesse intervalo.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d15e1",
            enunciado=(
                "Escreva a funcao divisao_segura(a, b) que divide a por b\n"
                "e devolve o resultado. Se b for zero, devolve None em vez\n"
                "de deixar o programa travar com ZeroDivisionError.\n\n"
                "Exemplos:\n"
                "   divisao_segura(10, 2)  -> 5.0\n"
                "   divisao_segura(1, 0)   -> None\n"
                "   divisao_segura(-9, 3)  -> -3.0\n\n"
                "Use try/except, NAO use if b == 0.\n"
                "O objetivo e praticar o estilo EAFP:\n"
                "   try:\n"
                "       return a / b      <- tente a divisao\n"
                "   except ZeroDivisionError:\n"
                "       return None       <- trate se der errado\n\n"
                "Nota: a divisao / sempre devolve float em Python,\n"
                "por isso 10/2 retorna 5.0 (nao o inteiro 5)."
            ),
            funcao="divisao_segura",
            assinatura="def divisao_segura(a, b):",
            testes=[
                ("divisao_segura(10, 2)", "5.0"),
                ("divisao_segura(1, 0)", "None"),
                ("divisao_segura(-9, 3)", "-3.0"),
            ],
            dica="try: return a / b  except ZeroDivisionError: return None",
        ),
        Exercicio(
            id="d15e2",
            enunciado=(
                "Escreva a funcao para_int(texto, padrao=0) que tenta\n"
                "converter texto para inteiro e devolve padrao se falhar.\n\n"
                "Exemplos:\n"
                "   para_int('42')      -> 42\n"
                "   para_int('abc')     -> 0   (padrao)\n"
                "   para_int(None, -1)  -> -1  (None causa TypeError)\n"
                "   para_int('  7  ')   -> 7   (int() ja ignora espacos)\n\n"
                "Dois tipos de erro podem ocorrer:\n"
                "   ValueError: quando o texto nao representa um inteiro\n"
                "               ex: int('abc'), int('3.14')\n"
                "   TypeError:  quando o argumento nao e texto\n"
                "               ex: int(None), int([1, 2])\n\n"
                "Capture os dois com uma tupla:\n"
                "   except (ValueError, TypeError):\n"
                "       return padrao\n\n"
                "Curiosidade: int('  7  ') funciona! int() ignora\n"
                "espacos nas pontas de strings numericas."
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
            dica="try: return int(texto)  except (ValueError, TypeError): return padrao",
        ),
        Exercicio(
            id="d15e3",
            enunciado=(
                "Crie a excecao SaldoInsuficiente e a funcao sacar(saldo, valor)\n"
                "que devem funcionar assim:\n\n"
                "   sacar(100, 30)  -> 70       (novo saldo)\n"
                "   sacar(100, 500) -> levanta SaldoInsuficiente\n"
                "   sacar(100, 0)   -> levanta ValueError\n"
                "   sacar(100, 100) -> 0         (saque total)\n\n"
                "Regras de validacao (nessa ordem!):\n"
                "   1. Se valor <= 0:\n"
                "      raise ValueError('Valor de saque deve ser positivo')\n"
                "   2. Se valor > saldo:\n"
                "      raise SaldoInsuficiente('Saldo insuficiente')\n"
                "   3. Devolva saldo - valor\n\n"
                "A classe SaldoInsuficiente ja esta na assinatura:\n"
                "   class SaldoInsuficiente(Exception):\n"
                "       pass\n\n"
                "Herdar de Exception e o suficiente para criar uma\n"
                "excecao personalizada basica. O 'pass' indica que\n"
                "nao ha atributos ou metodos adicionais."
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
            dica="Valide valor <= 0 primeiro (ValueError), depois valor > saldo (SaldoInsuficiente), por fim return saldo - valor.",
        ),
    ],
    quiz=[
        Quiz(
            "Quando o bloco 'else' de um try/except executa?",
            ["Sempre, apos o try terminar",
             "Somente se uma excecao foi capturada pelo except",
             "Somente se o try completou SEM nenhuma excecao",
             "Apenas quando o finally nao esta presente"],
            2,
            "else no try/except e o oposto do except: "
            "executa quando TUDO DEU CERTO no try. "
            "E util para separar 'codigo que pode falhar' (try) "
            "de 'codigo que depende do sucesso' (else), "
            "sem misturar tudo no bloco try.",
        ),
        Quiz(
            "Por que 'except: pass' e considerado um dos piores habitos em Python?",
            ["pass e uma palavra reservada que nao pode ser usada em except",
             "Captura TODAS as excecoes, incluindo KeyboardInterrupt (Ctrl+C), e suprime silenciosamente — bugs desaparecem sem deixar rastro",
             "e mais lento que except Exception: pass",
             "Funciona apenas com Python 2, nao com Python 3"],
            1,
            "except: sem tipo captura BaseException, que inclui SystemExit e "
            "KeyboardInterrupt. O programa nao consegue mais ser interrompido "
            "com Ctrl+C! Alem disso, qualquer erro real desaparece silenciosamente. "
            "Sempre especifique o tipo: except ValueError, except FileNotFoundError, etc.",
        ),
        Quiz(
            "Qual a diferenca entre 'raise' sozinho e 'raise ExcecaoNova()'?",
            ["Nao ha diferenca — os dois levantam a mesma excecao",
             "'raise' sozinho re-levanta a excecao ATUAL capturada pelo except; 'raise ExcecaoNova()' levanta uma nova excecao diferente",
             "'raise' sozinho encerra o programa; 'raise Excecao()' continua a execucao",
             "'raise' sozinho so funciona fora de um bloco except"],
            1,
            "'raise' sozinho dentro de um except preserva o traceback original "
            "e re-levanta exatamente a excecao que foi capturada — util para "
            "logar o erro e ainda propaga-lo. "
            "'raise NovaExcecao() from e' levanta uma nova mas preserva a causa.",
        ),
        Quiz(
            "Por que o estilo EAFP e preferido ao LBYL em Python?",
            ["EAFP e mais rapido em todos os casos",
             "LBYL nao e valido em Python — causa SyntaxError",
             "EAFP evita condicoes de corrida, tem melhor performance no caminho feliz e torna o codigo mais claro",
             "E apenas uma preferencia pessoal sem justificativa tecnica"],
            2,
            "LBYL faz a verificacao SEMPRE, mesmo quando o caso de erro e raro. "
            "EAFP paga custo apenas quando ha excecao. "
            "Alem disso, entre 'if existe' e 'usar', outro processo pode alterar "
            "o estado (condicao de corrida) — EAFP nao tem essa janela vulneravel.",
        ),
    ],
    projeto=(
        "Crie validador_dados.py com um sistema robusto de validacao:\n\n"
        "EXCECOES PERSONALIZADAS:\n"
        "   class ErroDeValidacao(Exception): pass\n"
        "   class CampoObrigatorio(ErroDeValidacao): pass\n"
        "   class ValorForaDeFaixa(ErroDeValidacao): pass\n"
        "   class FormatoInvalido(ErroDeValidacao): pass\n\n"
        "FUNCOES:\n\n"
        "   1. validar_nome(nome):\n"
        "      - Levanta CampoObrigatorio se vazio\n"
        "      - Levanta FormatoInvalido se tiver numeros\n"
        "      - Devolve nome.strip().title()\n\n"
        "   2. validar_idade(valor):\n"
        "      - Converte para int (levanta FormatoInvalido se falhar)\n"
        "      - Levanta ValorForaDeFaixa se < 0 ou > 150\n"
        "      - Devolve o int\n\n"
        "   3. validar_email(email):\n"
        "      - Levanta CampoObrigatorio se vazio\n"
        "      - Levanta FormatoInvalido se nao contem '@'\n"
        "      - Devolve email.lower()\n\n"
        "   4. validar_cadastro(dados_dict):\n"
        "      Chama as tres funcoes anteriores com try/except\n"
        "      Coleta TODOS os erros (nao para no primeiro)\n"
        "      Devolve (dados_validos, lista_de_erros)\n\n"
        "BONUS: adicione logging com o modulo logging para registrar\n"
        "cada tentativa de validacao em um arquivo de log."
    ),
    leitura=[
        "docs.python.org/pt-br/3/tutorial/errors.html — erros e excecoes",
        "docs.python.org/pt-br/3/library/exceptions.html — hierarquia completa",
        "PEP 3151 — racionalizacao da hierarquia de excecoes de OS",
    ],
))