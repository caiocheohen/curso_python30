"""Semana 1 - Dias 1 a 8: fundamentos da linguagem."""

from nucleo.modelos import Dia, Exemplo, Exercicio, Quiz

DIAS = []

# ---------------------------------------------------------------- DIA 1
DIAS.append(Dia(
    numero=1,
    titulo="Ambiente, interpretador e o primeiro programa",
    nivel="Iniciante",
    duracao="70 min",
    objetivos=[
        "Entender o que o interpretador Python faz e como ele roda no Linux",
        "Diferenciar REPL, script e módulo",
        "Escrever e executar o primeiro script .py, com e sem shebang",
        "Usar print(), comentários, docstrings e a função help()",
        "Ler um traceback e identificar o tipo de erro antes de entrar em pânico",
        "Aplicar as convenções de estilo (PEP 8) desde a primeira linha de código",
    ],
    teoria="""
Python é uma linguagem interpretada: você escreve texto num arquivo e o
programa `python3` lê esse texto, o transforma internamente em bytecode e
executa, tudo em um único comando. Não existe uma etapa manual de compilação
como em C ou Java — mas isso não significa que "não há compilação nenhuma".
Vale entender os bastidores, porque isso explica comportamentos que parecem
mágicos mais adiante no curso.

1. O que acontece quando você digita `python3 arquivo.py`
----------------------------------------------------------
Por trás da simplicidade, o CPython (a implementação de referência, a que
você tem instalada) faz três coisas:

    1. Lê o arquivo e o transforma em uma árvore sintática (parsing).
    2. Compila essa árvore para bytecode — instruções de baixo nível para
       uma máquina virtual, mas ainda não código de máquina real.
    3. A CPython Virtual Machine executa esse bytecode, instrução a
       instrução.

O bytecode de um módulo importado fica em cache em `__pycache__/*.pyc`, para
não recompilar toda vez. Isso é só uma otimização — o "compilar" aqui é
interno e automático; você não interage com ele diretamente, ao contrário de
`gcc arquivo.c` em C.

2. O interpretador no Linux
---------------------------
Praticamente toda distribuição Linux já vem com Python 3 pré-instalado
(geralmente usado pelo próprio sistema operacional para scripts internos —
por isso é arriscado desinstalá-lo ou trocar a versão do sistema). No
terminal:

    python3 --version      # mostra a versão instalada, ex: Python 3.12.3
    which python3          # mostra o caminho do binário, ex: /usr/bin/python3
    python3                # abre o REPL (modo interativo)

Em algumas distribuições, `python` (sem o 3) aponta para Python 2, que está
oficialmente descontinuado desde 2020 — por isso este curso e a comunidade em
geral usam sempre `python3` explicitamente. Se você tem várias versões
instaladas (comum ao usar `pyenv` ou `uv`), `python3 --version` sempre revela
qual delas está ativa na sessão atual.

3. REPL: seu laboratório de bolso
----------------------------------
REPL significa Read-Eval-Print Loop: o interpretador Lê o que você digita,
AValia (executa), imprime o resultado e recomeça o laço.

    $ python3
    Python 3.12.3 (main, ...) 
    >>> 2 + 3
    5
    >>> nome = "Ana"
    >>> nome
    'Ana'
    >>> exit()

Repare que, no REPL, o valor de uma expressão aparece automaticamente na
tela — isso só acontece ali, nunca dentro de um script (onde você precisa de
`print()` explícito). Saia com `exit()`, `quit()` ou Ctrl+D.

O REPL não substitui um editor: ele é feito para perguntas rápidas e
descartáveis ("o que `'abc'[::-1]` devolve mesmo?"), não para programas de
verdade. Ao longo do curso, o hábito mais valioso que você pode criar é abrir
um REPL ao lado sempre que tiver uma dúvida pontual, em vez de ficar
imaginando a resposta.

4. Script: o arquivo que você realmente vai escrever
-----------------------------------------------------
Um script é um arquivo de texto simples com extensão `.py`:

    nano ola.py             # ou vim, code, gedit, o editor que preferir
    python3 ola.py          # executa o arquivo do início ao fim

Você também pode torná-lo executável diretamente, sem digitar `python3` toda
vez, usando um shebang na primeira linha:

    #!/usr/bin/env python3

    chmod +x ola.py
    ./ola.py

`chmod +x` marca o arquivo como executável no sistema de arquivos Linux.
`/usr/bin/env python3` é preferível a apontar direto para `/usr/bin/python3`
porque `env` procura o `python3` que está ativo no PATH do usuário — o que
importa muito quando você estiver usando ambientes virtuais (Dia 13):
apontar direto para `/usr/bin/python3` ignoraria o ambiente virtual ativado.

5. print(): sua janela para o mundo
------------------------------------
`print` envia texto para a saída padrão (stdout) — o que aparece no
terminal. Aceita qualquer quantidade de argumentos, separados por vírgula, e
dois parâmetros nomeados que valem a pena memorizar:

    print("a", "b")               # a b        (separador padrão: espaço)
    print("a", "b", sep="-")      # a-b
    print("a", "b", "c", sep=", ")# a, b, c
    print("sem quebra", end="")   # não pula linha ao final
    print(1, 2, 3)                # 1 2 3      (print converte tudo para str)

Por padrão, cada chamada de `print` termina com uma quebra de linha (`end`
vale `"\\n"` por padrão). Trocar `end` é o truque clássico para construir uma
barra de progresso ou imprimir vários itens na mesma linha.

Um detalhe frequentemente ignorado: `print` sempre devolve `None`. Se você
escrever `x = print("oi")`, `x` vale `None` — imprimir na tela e devolver um
valor utilizável são coisas diferentes.

6. Comentários e docstrings não são a mesma coisa
--------------------------------------------------
Tudo depois de `#` até o fim da linha é ignorado pelo interpretador. Um bom
comentário explica o PORQUÊ de uma decisão, não o QUÊ — o próprio código já
diz o quê:

    # ruim: repete o obvio
    preco = preco * 0.9   # multiplica preco por 0.9

    # bom: explica a decisao de negocio
    preco = preco * 0.9   # desconto de fidelidade aprovado na reuniao de marco

Docstring é outra coisa: é uma string entre três aspas logo no início de um
módulo, função ou classe, e — diferente do comentário — ela vira parte do
programa em tempo de execução, acessível via `help(objeto)` ou
`objeto.__doc__`. Ferramentas de documentação e o próprio `help()` do REPL
leem essas strings automaticamente.

    def dobro(x):
        \"\"\"Devolve o dobro de x.\"\"\"
        return x * 2

    help(dobro)          # mostra a docstring formatada
    dobro.__doc__        # 'Devolve o dobro de x.'

7. Lendo um erro sem entrar em pânico
---------------------------------------
Todo iniciante — e todo profissional, aliás — vive cercado de tracebacks.
A diferença entre quem trava e quem resolve rápido é saber onde olhar:

    Traceback (most recent call last):
      File "programa.py", line 7, in <module>
        resultado = 10 / zero
                    ~~~^~~~~~
    ZeroDivisionError: division by zero

Leia de baixo para cima. A ÚLTIMA linha traz o tipo do erro e a mensagem —
é o resumo executivo do problema. As linhas "File ..., line N" acima dizem
ONDE o erro aconteceu, e no Python moderno (3.11+) até sublinham o trecho
exato da expressão culpada com `~~~^~~~~~`.

Os erros mais comuns na primeira semana:

    SyntaxError          -> faltou dois-pontos, parêntese, aspas ou vírgula
    IndentationError     -> misturou espaços com tabs, ou recuou errado
    NameError            -> usou um nome que não existe (ou digitou errado)
    TypeError            -> operação entre tipos incompatíveis ('a' + 3)
    ModuleNotFoundError  -> import de algo que não está instalado

Uma dica prática: quando o erro parecer incompreensível, copie só a última
linha (o tipo + a mensagem) e pesquise exatamente aquilo. É a forma mais
eficiente de aprender a resolver — e é exatamente o que profissionais fazem
o dia inteiro.

8. Estilo (PEP 8) desde a primeira linha
-------------------------------------------
PEP 8 é o guia de estilo oficial da linguagem. Segui-lo desde o início evita
reaprender hábitos depois — e torna seu código legível para qualquer outra
pessoa (inclusive você mesmo, em seis meses):

    - indentação de 4 espaços, nunca tab misturado com espaço
    - nomes de variável e função em minúsculas_com_underscore: preco_total
    - nomes de classe em PascalCase (a partir do Dia 16): ContaBancaria
    - uma instrução por linha
    - linhas com no máximo ~79-100 colunas
    - duas linhas em branco entre funções de nível superior

Editores como VS Code (com a extensão Python/Pylance) e o formatador `black`
aplicam boa parte disso automaticamente — vale configurar isso cedo em vez
de discutir estilo linha a linha depois.
""",
    exemplos=[
        Exemplo(
            titulo="Primeiro script completo",
            codigo='''#!/usr/bin/env python3
"""Programa de boas-vindas do curso."""

print("Ola, mundo!")
print("Python", "roda", "no Linux", sep=" ")
print("Fim", end=".\\n")
''',
            explicacao="Salve como ola.py e rode com: python3 ola.py. "
                       "A docstring no topo já é acessível via ola.__doc__ se "
                       "você importar este arquivo como módulo.",
        ),
        Exemplo(
            titulo="Explorando no REPL: help() e dir()",
            codigo='''>>> 2 + 3
5
>>> len("Python")
6
>>> help(print)      # documentacao embutida da propria funcao print
>>> dir(str)         # lista TUDO que uma string sabe fazer
>>> "Python".__doc__[:40]   # docstrings existem ate em tipos embutidos
''',
            explicacao="help() e dir() são suas duas melhores ferramentas de "
                       "estudo: dir() responde 'o que esse objeto sabe fazer?' "
                       "e help() responde 'como eu uso isso?'.",
        ),
        Exemplo(
            titulo="Lendo um traceback de verdade",
            codigo='''idade = "vinte"
dobro = idade * 2      # isto NAO da erro: repete a string duas vezes
print(dobro)           # vinteVinte... na verdade: vintevintevinte? nao.

soma = idade + 5       # isto SIM da TypeError
''',
            explicacao="'vinte' * 2 é permitido (repete a string), mas "
                       "'vinte' + 5 não é: Python não soma texto com número "
                       "automaticamente. O Dia 2 explica essa 'tipagem forte'.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d01e1",
            enunciado="Crie uma variável chamada `mensagem` contendo exatamente o texto: Ola, Python!",
            funcao="mensagem",
            assinatura='mensagem = ...',
            testes=[("mensagem", "'Ola, Python!'")],
            dica="Use aspas simples ou duplas; o texto deve bater caractere por caractere.",
        ),
        Exercicio(
            id="d01e2",
            enunciado=(
                "Use as variáveis nome = 'Ana' e idade = 30 para montar a variável\n"
                "`cartao` com o texto: Ana tem 30 anos"
            ),
            funcao="cartao",
            assinatura='nome = "Ana"\nidade = 30\ncartao = ...',
            testes=[("cartao", "'Ana tem 30 anos'")],
            dica="Concatene com + e converta o número com str(idade).",
        ),
        Exercicio(
            id="d01e3",
            enunciado="Calcule a variável `area` de um retângulo de base 7.5 e altura 4.",
            funcao="area",
            assinatura="base = 7.5\naltura = 4\narea = ...",
            testes=[("area", "30.0")],
            dica="Multiplicação usa o operador *.",
        ),
    ],
    quiz=[
        Quiz("Qual comando mostra a versão do Python no terminal Linux?",
             ["python3 --version", "python3 version", "print(version)", "py -v"], 0,
             "A flag --version (ou -V) é a convenção padrão em ferramentas de linha de comando no Linux."),
        Quiz("O que `print('a', 'b', sep='')` imprime?",
             ["a b", "ab", "a-b", "erro"], 1,
             "sep define o separador entre argumentos; string vazia cola tudo sem espaço."),
        Quiz("O que print() devolve quando usado como valor, ex: x = print('oi')?",
             ["A string impressa", "O número de caracteres impressos", "None", "Um erro"], 2,
             "print() serve para exibir texto; ele sempre devolve None, nunca o texto em si."),
        Quiz("Em um traceback, onde fica a informação mais importante para entender o erro?",
             ["Na primeira linha", "No meio, junto ao nome do arquivo",
              "Na última linha", "Não importa, a ordem é aleatória"], 2,
             "A última linha traz o tipo do erro (ex: TypeError) e a mensagem — o resumo do problema."),
    ],
    projeto=(
        "Crie o arquivo perfil.py que imprima um cartão de apresentação seu em 5 linhas: "
        "nome, cidade, objetivo com Python, linguagem favorita e uma frase motivacional. "
        "Adicione uma docstring de módulo explicando o que o arquivo faz, torne-o executável "
        "com chmod +x e rode com ./perfil.py."
    ),
    leitura=["docs.python.org/pt-br/3/tutorial/introduction.html", "PEP 8", "PEP 20 (O Zen do Python: import this)"],
))

# ---------------------------------------------------------------- DIA 2
DIAS.append(Dia(
    numero=2,
    titulo="Variáveis, tipos primitivos e entrada de dados",
    nivel="Iniciante",
    duracao="80 min",
    objetivos=[
        "Entender variável como rótulo, não como caixa de memória",
        "Dominar int, float, str, bool e None e como o interpretador os distingue",
        "Explicar o que significa tipagem dinâmica e forte, com exemplos práticos",
        "Converter tipos com int(), float(), str(), bool() e saber quando cada conversão falha",
        "Ler dados do usuário com input() e validar o tipo antes de usar",
        "Reconhecer as armadilhas de ponto flutuante e saber quando usar Decimal",
    ],
    teoria="""
1. Variável é um rótulo, não uma caixa
--------------------------------------
Em linguagens como C, uma variável é uma caixa de memória com tamanho fixo:
declarar `int x` reserva 4 bytes, e atribuir muda o conteúdo daquela caixa.
Python funciona de outro jeito. `x = 10` não copia o valor 10 para dentro de
uma gaveta chamada x. Em vez disso, Python cria o objeto inteiro 10 em algum
lugar da memória e faz o nome `x` apontar para ele — como uma etiqueta presa
com um barbante, não como uma caixa.

Essa diferença explica um comportamento que costuma surpreender:

    a = [1, 2]
    b = a          # b aponta para a MESMA lista que a, não para uma cópia
    b.append(3)
    print(a)       # [1, 2, 3]  <- surpresa clássica para quem vem de outras linguagens

`id(objeto)` mostra o endereço de memória (na prática, um número que
identifica o objeto); `id(a) == id(b)` aqui seria True. Números e strings são
imutáveis, então esse efeito de "dois nomes, um objeto só" nunca causa
problema visível com eles — mas com listas, dicionários e objetos de classes
próprias (a partir do Dia 16), é a primeira coisa a suspeitar quando algo
"muda sozinho".

2. Os tipos primitivos
----------------------
    int    inteiro de precisão ILIMITADA:  10, -3, 10_000_000, 2**200
    float  ponto flutuante (64 bits, IEEE-754): 3.14, 2.0, 1e-5
    str    texto Unicode:                   'oi', "oi", '''várias linhas'''
    bool   True / False (é, tecnicamente, um SUBTIPO de int!)
    None   ausência de valor (o único valor do tipo NoneType)

Um detalhe que diferencia Python de C/Java/Go: `int` não estoura. Enquanto
em C um `int` de 32 bits vira lixo (overflow) ao ultrapassar ~2 bilhões,
Python expande a representação automaticamente:

    2 ** 100     # 1267650600228229401496703205376 — sem erro, sem overflow

Isso tem um custo: inteiros muito grandes ficam mais lentos para operar do
que inteiros pequenos, mas na prática você raramente sente essa diferença.

`type(x)` revela o tipo exato de um objeto; `isinstance(x, int)` testa se x
pertence a um tipo (ou a uma de suas subclasses) — prefira `isinstance` para
validações, porque ele lida melhor com herança (assunto do Dia 18).

3. Tipagem dinâmica e forte — dois conceitos que se confundem
----------------------------------------------------------------
DINÂMICA significa que o mesmo NOME pode apontar para objetos de tipos
diferentes ao longo do tempo — não há necessidade de declarar `int x` antes:

    x = 10          # x aponta para um int
    x = "dez"       # agora x aponta para uma str; nada impede isso

FORTE significa que Python NÃO converte tipos incompatíveis silenciosamente
para você tentar operar entre eles — ao contrário de JavaScript, por
exemplo, onde `"3" + 4` vira `"34"` sem avisar nada:

    "3" + 4        # TypeError: can only concatenate str (not "int") to str
    "3" * 4        # '3333'    (isto SIM é permitido: repetição, não soma)
    3 + True       # 4         (bool é literalmente um int por baixo: True == 1)
    3 + False      # 3         (False == 0)

Note a diferença entre "dinâmica" (o nome muda de tipo) e "forte" (os
valores não se misturam sem conversão explícita). Muita gente confunde os
dois termos, mas eles respondem perguntas diferentes: dinâmica é sobre
NOMES; forte é sobre OPERAÇÕES entre VALORES.

4. Conversões explícitas: onde cada uma falha
-----------------------------------------------
    int("42")      -> 42
    int("42.5")    -> ValueError: invalid literal for int() (int não parseia decimais em texto!)
    int(42.9)      -> 42        (TRUNCA na direção do zero, não arredonda)
    int(-42.9)     -> -42       (trunca para -42, não para -43)
    round(42.9)    -> 43        (este sim arredonda para o inteiro mais próximo)
    float("3.14")  -> 3.14
    float("abc")   -> ValueError
    str(3.14)      -> '3.14'
    bool(0), bool(""), bool([]), bool(None), bool(0.0)  -> False (todos)
    bool(qualquer OUTRA coisa, inclusive "0" e "False" como strings!)  -> True

O último ponto é uma pegadinha clássica: `bool("False")` é `True`, porque a
string `"False"` não é vazia — ela é um texto com 5 caracteres, e qualquer
string não vazia é "verdadeira". Para interpretar texto como valor lógico de
verdade, é preciso lógica própria: `texto.lower() == "true"`, por exemplo.

5. Cuidado com float: o problema não é do Python
---------------------------------------------------
    0.1 + 0.2 == 0.3     # False!

Isso NÃO é um bug do Python — é como o padrão IEEE-754 (usado por
praticamente toda linguagem: C, Java, JavaScript, Rust) representa números
decimais em binário. Frações como 0.1 não têm representação binária finita,
então o computador guarda uma aproximação extremamente próxima, mas não
exata. Para comparar floats com segurança:

    import math
    math.isclose(0.1 + 0.2, 0.3)     # True

Para dinheiro — onde centavos de diferença são inaceitáveis — a prática
profissional é usar `decimal.Decimal`, que representa números em base 10
exatamente:

    from decimal import Decimal
    Decimal("0.1") + Decimal("0.2") == Decimal("0.3")   # True

Repare que se cria o Decimal a partir de uma STRING, não de um float — criar
com `Decimal(0.1)` herdaria a imprecisão do float original antes mesmo de
chegar ao Decimal.

6. input(): sempre string, sem exceção
------------------------------------------
`input()` mostra um prompt opcional e SEMPRE devolve uma string, mesmo que o
usuário digite só números:

    idade_texto = input("Idade: ")    # digitando 25, idade_texto é '25', não 25
    idade = int(input("Idade: "))     # converta na hora, direto na mesma linha

Se o usuário digitar algo que não é um número válido (`"vinte e cinco"`),
`int(...)` levanta `ValueError` — e o programa quebra ali, a menos que você
trate isso. O Dia 15 (exceções) ensina a lidar com essa situação de forma
elegante com `try/except`; por enquanto, é importante só saber que essa
falha existe e é comum em programas que leem entrada de usuários reais.

7. Constantes e as regras de nomes válidos
-----------------------------------------------
Python não tem uma palavra-chave para "constante de verdade" (como `const`
em JavaScript). A convenção universal é usar MAIÚSCULAS_COM_UNDERSCORE para
sinalizar "este valor não deveria mudar":

    TAXA_JUROS = 0.05
    MAX_TENTATIVAS = 3

Isso é só convenção — nada impede tecnicamente de reatribuir
`TAXA_JUROS = 1`. É o mesmo princípio de "combinado não sai caro" que rege
boa parte do estilo Python.

Nomes de variável não podem começar com número, não podem conter espaços ou
símbolos como `-`, e não podem ser uma das 35 palavras reservadas da
linguagem (`class`, `for`, `lambda`, `import`...). Para ver a lista completa:

    import keyword
    keyword.kwlist
""",
    exemplos=[
        Exemplo(
            titulo="Inspecionando tipos e identidade",
            codigo='''valores = [10, 3.14, "texto", True, None]
for v in valores:
    print(repr(v), "->", type(v).__name__)

a = [1, 2]
b = a
c = a[:]
print(a is b)       # True: mesmo objeto
print(a is c)       # False: c e uma copia
''',
            explicacao="type(v).__name__ dá o nome limpo do tipo. `is` compara "
                       "identidade (mesmo objeto), não valor — reserve-o para "
                       "None, True e False.",
        ),
        Exemplo(
            titulo="Calculadora de IMC com entrada do usuário",
            codigo='''peso = float(input("Peso em kg: "))
altura = float(input("Altura em m: "))
imc = peso / altura ** 2
print("Seu IMC e", round(imc, 2))
''',
            explicacao="Note a conversão com float() logo na leitura — sem "
                       "isso, 'peso / altura ** 2' tentaria dividir strings, "
                       "o que gera TypeError.",
        ),
        Exemplo(
            titulo="Quando 0.1 + 0.2 não é 0.3",
            codigo='''import math
from decimal import Decimal

print(0.1 + 0.2)                       # 0.30000000000000004
print(0.1 + 0.2 == 0.3)                # False
print(math.isclose(0.1 + 0.2, 0.3))    # True

preco_a = Decimal("19.90")
preco_b = Decimal("5.10")
print(preco_a + preco_b == Decimal("25.00"))   # True, exato
''',
            explicacao="Para exibir ou comparar valores monetários com "
                       "confiança, prefira Decimal criado a partir de string.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d02e1",
            enunciado=(
                "A partir de texto_numero = '42', crie `numero` como inteiro e\n"
                "`dobro` com o dobro desse valor."
            ),
            funcao="numero",
            assinatura='texto_numero = "42"\nnumero = ...\ndobro = ...',
            testes=[("numero", "42"), ("dobro", "84"), ("type(numero) is int", "True")],
            dica="int() converte texto em inteiro.",
        ),
        Exercicio(
            id="d02e2",
            enunciado="Converta celsius = 37.5 para `fahrenheit` (F = C * 9/5 + 32).",
            funcao="fahrenheit",
            assinatura="celsius = 37.5\nfahrenheit = ...",
            testes=[("fahrenheit", "99.5")],
            dica="Cuidado com a precedência: multiplique antes de somar 32.",
        ),
        Exercicio(
            id="d02e3",
            enunciado=(
                "Comece com a = 10 e b = 3 e troque os valores entre eles\n"
                "SEM usar uma terceira variável."
            ),
            funcao="a",
            assinatura="a = 10\nb = 3\n# troque aqui",
            testes=[("a", "3"), ("b", "10")],
            dica="Python permite atribuição múltipla: a, b = b, a",
        ),
    ],
    quiz=[
        Quiz("Qual o resultado de int('7') + int(7.9)?",
             ["14", "14.9", "15", "TypeError"], 0,
             "int(7.9) trunca para 7 (não arredonda), então 7 + 7 = 14."),
        Quiz("O que input() sempre devolve, independente do que o usuário digitar?",
             ["int", "str", "o tipo digitado", "None"], 1,
             "input() devolve sempre string; converter para int/float é responsabilidade do programa."),
        Quiz("Por que 0.1 + 0.2 == 0.3 é False em Python?",
             ["É um bug específico do Python",
              "Frações decimais não têm representação binária finita (padrão IEEE-754)",
              "Porque 0.1 e 0.2 são strings", "Porque falta importar math"], 1,
             "É uma limitação do padrão de ponto flutuante binário, comum a quase toda linguagem."),
        Quiz("O que 3 + True vale em Python?",
             ["Erro de tipo", "3", "4", "True"], 2,
             "bool é subtipo de int: True vale 1 e False vale 0 em contas aritméticas."),
    ],
    projeto=(
        "Faça conversor.py: pergunte um valor em reais e a cotação do dólar, "
        "e mostre o valor convertido com 2 casas decimais, além do tipo de cada variável usada. "
        "Depois, refaça o cálculo do valor final usando Decimal e compare o resultado com o float."
    ),
    leitura=["docs.python.org/pt-br/3/library/stdtypes.html", "docs.python.org/pt-br/3/library/decimal.html"],
))

# ---------------------------------------------------------------- DIA 3
DIAS.append(Dia(
    numero=3,
    titulo="Operadores: aritméticos, comparação, lógicos e precedência",
    nivel="Iniciante",
    duracao="70 min",
    objetivos=[
        "Usar //, %, ** e entender por que divisão inteira arredonda para baixo (piso), não para zero",
        "Encadear comparações do jeito idiomático do Python",
        "Diferenciar == (valor) de is (identidade) com precisão",
        "Aplicar and/or/not e explicar o que cada um realmente devolve",
        "Reconhecer valores falsy e escrever condições mais legíveis com eles",
        "Consultar a tabela de precedência sem depender de memorização",
    ],
    teoria="""
1. Operadores aritméticos
--------------------------
    +   -   *          soma, subtração, multiplicação
    /                  divisão REAL, SEMPRE devolve float: 6 / 3 -> 2.0 (não 2!)
    //                 divisão inteira (piso): 7 // 2 -> 3 ; -7 // 2 -> -4
    %                  resto da divisão: 7 % 2 -> 1 ; usado para paridade e ciclos
    **                 potência: 2 ** 10 -> 1024 ; 9 ** 0.5 -> 3.0 (raiz quadrada!)

O comportamento de `//` com números negativos surpreende quem vem de C ou
Java: nessas linguagens, a divisão inteira trunca em direção ao zero
(-7 / 2 dá -3). Em Python, `//` é uma divisão de PISO (floor division):
sempre arredonda para o inteiro mais próximo ABAIXO, mesmo com negativos.
Por isso `-7 // 2` é `-4`, não `-3`. Essa escolha de design faz `%` sempre
ter o mesmo sinal do divisor, o que é útil para problemas cíclicos (relógio,
dias da semana).

O par (`//`, `%`) é a base para decompor números em partes:

    total_segundos = 3725
    horas = total_segundos // 3600          # 1
    resto = total_segundos % 3600           # 125
    minutos = resto // 60                   # 2
    segundos = resto % 60                   # 5

`divmod(a, b)` devolve os dois de uma vez, como uma tupla: `divmod(7, 2)` dá
`(3, 1)` — quociente e resto num só cálculo, útil quando você precisa dos
dois valores e quer evitar computar a divisão duas vezes.

2. Atribuição composta
------------------------
Toda operação binária tem uma forma "composta" que lê e reatribui a mesma
variável numa única expressão:

    x += 1     x -= 2     x *= 3     x /= 2     x //= 2     x %= 5     x **= 2

`x += 1` não é apenas um atalho visual: para tipos mutáveis (como listas),
`+=` pode se comportar de forma diferente de `x = x + ...` — assunto que
aprofundamos no Dia 8 ao falar de `.extend()` versus concatenação.

3. Comparação: valor versus identidade
----------------------------------------
    ==  !=  <  <=  >  >=

Podem ser encadeadas de forma natural, um recurso que a maioria das
linguagens não tem:

    if 0 <= nota <= 10:      # equivale a: 0 <= nota AND nota <= 10

Isso é puro açúcar sintático que deixa o código mais próximo da notação
matemática — e evita o erro clássico de escrever `if 0 <= nota <= 10` em
Java/C, onde isso simplesmente não compila (lá seria obrigatório escrever
os dois lados por extenso).

A distinção mais importante do dia: `==` compara VALOR (o conteúdo dos
objetos é igual?); `is` compara IDENTIDADE (é literalmente o MESMO objeto em
memória?).

    a = [1, 2, 3]
    b = [1, 2, 3]
    a == b    # True  — mesmo conteúdo
    a is b    # False — objetos diferentes na memória, por acaso com o mesmo conteúdo

    c = a
    a is c    # True  — c e a são o mesmo objeto (veja o Dia 2, "rótulo, não caixa")

A convenção da comunidade é usar `is` apenas com `None`, `True` e `False`:

    if valor is None:        # correto e idiomático
    if valor == None:        # funciona, mas soa estranho e pode falhar com
                              # classes que sobrescrevem __eq__ de forma incomum

Por que `is None` funciona sempre com segurança? Porque existe exatamente UM
objeto `None` em todo o programa Python — não importa quantas vezes você
escreva `None`, é sempre o mesmo objeto na memória.

4. Lógicos e avaliação em curto-circuito
---------------------------------------------
    and  or  not

Python avalia da esquerda para a direita e PARA assim que o resultado já é
conhecido — é a chamada avaliação em curto-circuito (short-circuit
evaluation). Isso não é só uma otimização de performance: é uma ferramenta
de proteção de código muito usada:

    if divisor != 0 and total / divisor > 2:
        ...

Se `divisor != 0` for `False`, Python nunca chega a avaliar
`total / divisor`, evitando a `ZeroDivisionError`. Essa ordem importa — se
você escrever as condições ao contrário, o curto-circuito não te protege.

Um ponto sutil e muito usado no código Python real: `and`/`or` NÃO devolvem
um booleano — eles devolvem um dos DOIS OPERANDOS originais.

    "" or "padrao"      -> 'padrao'   (o primeiro era falsy, devolve o segundo)
    "ana" and "bia"     -> 'bia'      (o primeiro era truthy, avalia e devolve o segundo)
    0 or []             -> []         (0 é falsy, [] também, mas [] é o que "sobra")
    "ana" or "bia"      -> 'ana'      (o primeiro já é truthy, para ali e devolve ele)

Isso viabiliza o idioma `valor = entrada or "padrao"` para fornecer um valor
default quando `entrada` é falsy — mas cuidado: se `0` for um valor
LEGÍTIMO (por exemplo, "o usuário digitou zero de propósito"), esse idioma
vai substituí-lo pelo padrão incorretamente, porque `0` também é falsy.

5. Valores "falsy": o que conta como falso em um if
--------------------------------------------------------
São considerados falsos em contexto booleano: `False`, `None`, `0`, `0.0`,
`""` (string vazia), `[]`, `()`, `{}`, `set()` e `range(0)` — ou seja,
QUALQUER coleção ou valor "vazio" ou "zero". Todo o resto é considerado
verdadeiro (truthy), inclusive `"0"` (string com um caractere) e `[0]`
(lista com um elemento, mesmo que esse elemento seja zero).

Por isso o código idiomático em Python prefere:

    if lista:                  # em vez de: if len(lista) > 0:
    if not lista:              # em vez de: if len(lista) == 0:
    if nome:                   # em vez de: if nome != "":

Essa preferência não é só estilo: ela também funciona automaticamente com
QUALQUER tipo de coleção (lista, tupla, dicionário, conjunto), sem precisar
saber qual método de "tamanho" cada uma usa.

6. Tabela de precedência (do mais forte para o mais fraco)
-------------------------------------------------------------
    **                        potência (associa à direita: 2**3**2 = 2**(3**2) = 512)
    unário  -x  +x  ~x        sinal e complemento de bits
    *  /  //  %                multiplicação e divisões
    +  -                       soma e subtração
    <<  >>                     deslocamento de bits
    &                          E bit a bit
    ^                          OU exclusivo bit a bit
    |                          OU bit a bit
    comparações, in, is        ==, <, in, is etc.
    not                        negação lógica
    and                        E lógico
    or                         OU lógico

Na dúvida, use parênteses — legibilidade vence economia de caracteres, e
ninguém, nem quem escreveu a linguagem, memoriza essa tabela inteira no
dia a dia; ela existe para consulta, não para decoreba.

7. Operadores bit a bit (visão geral)
-----------------------------------------
Menos usados no dia a dia de quem está começando, mas presentes em código de
sistemas, criptografia e otimizações de baixo nível:

    5 & 3   -> 1     (AND:  0101 & 0011 = 0001)
    5 | 3   -> 7     (OR:   0101 | 0011 = 0111)
    5 ^ 3   -> 6     (XOR:  0101 ^ 0011 = 0110)
    5 << 1  -> 10    (desloca a esquerda = multiplica por 2)
    5 >> 1  -> 2     (desloca a direita = divide por 2, descartando o resto)

`bin(5)` mostra a representação binária de um inteiro (`'0b101'`), útil para
visualizar essas operações enquanto você aprende.
""",
    exemplos=[
        Exemplo(
            titulo="Decompondo um valor monetário em notas",
            codigo='''valor = 287
for nota in (100, 50, 20, 10, 5, 2, 1):
    quantidade, valor = divmod(valor, nota)
    if quantidade:
        print(f"{quantidade} nota(s) de {nota}")
''',
            explicacao="divmod devolve quociente e resto ao mesmo tempo, "
                       "reaproveitando `valor` como o resto que ainda falta distribuir.",
        ),
        Exemplo(
            titulo="Curto-circuito como valor padrão (e sua armadilha)",
            codigo='''nome_digitado = ""
nome = nome_digitado or "visitante"
print("Ola,", nome)          # Ola, visitante

desconto_digitado = 0        # usuario digitou 0 de proposito
desconto = desconto_digitado or 10
print(desconto)              # 10 -- ERRADO, o 0 legitimo foi substituido!
''',
            explicacao="Idiomático, mas perigoso quando 0 (ou '' ou []) é um "
                       "valor válido, não uma ausência de valor. Nesse caso, "
                       "prefira: desconto = desconto_digitado if desconto_digitado is not None else 10",
        ),
        Exemplo(
            titulo="is versus == na prática",
            codigo='''a = [1, 2]
b = [1, 2]
c = a

print(a == b, a is b)   # True False
print(a == c, a is c)   # True True

x = None
print(x is None)        # True -- forma idiomatica e segura
print(x == None)        # tambem True aqui, mas is e a convencao
''',
            explicacao="== pergunta 'tem o mesmo conteúdo?'; is pergunta "
                       "'é o mesmo objeto na memória?'. São perguntas diferentes.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d03e1",
            enunciado=(
                "Dado numero = 157, extraia `centena` (1), `dezena` (5) e `unidade` (7)\n"
                "usando apenas // e %."
            ),
            funcao="centena",
            assinatura="numero = 157\ncentena = ...\ndezena = ...\nunidade = ...",
            testes=[("centena", "1"), ("dezena", "5"), ("unidade", "7")],
            dica="dezena = numero // 10 % 10",
        ),
        Exercicio(
            id="d03e2",
            enunciado=(
                "Com ano = 2024, calcule `bissexto` (True/False).\n"
                "Regra: divisível por 4 e não por 100, OU divisível por 400."
            ),
            funcao="bissexto",
            assinatura="ano = 2024\nbissexto = ...",
            testes=[("bissexto", "True"), ("type(bissexto) is bool", "True")],
            dica="Use parênteses para agrupar a primeira condição antes do or.",
        ),
        Exercicio(
            id="d03e3",
            enunciado=(
                "Converta total = 3725 segundos em `horas`, `minutos` e `segundos`\n"
                "(resultado esperado: 1, 2 e 5)."
            ),
            funcao="horas",
            assinatura="total = 3725\nhoras = ...\nminutos = ...\nsegundos = ...",
            testes=[("horas", "1"), ("minutos", "2"), ("segundos", "5")],
            dica="1 hora = 3600 s. Trabalhe com o resto após tirar as horas.",
        ),
    ],
    quiz=[
        Quiz("Quanto vale -7 // 2 em Python?",
             ["-3", "-4", "-3.5", "3"], 1,
             "// arredonda sempre para baixo (piso, floor division), então -3.5 vira -4, não -3."),
        Quiz("O que devolve 0 or 'x'?",
             ["True", "0", "'x'", "False"], 2,
             "or devolve o primeiro operando verdadeiro (ou o último, se nenhum for), não um bool."),
        Quiz("Por que 'if valor is None' é preferível a 'if valor == None'?",
             ["is é mais rápido de digitar", "is é a convenção porque None é sempre o mesmo objeto único",
              "== não funciona com None", "Não há diferença nenhuma"], 1,
             "Existe apenas um objeto None em todo o programa, então is é semanticamente exato e idiomático."),
        Quiz("Qual destes valores é considerado falsy em um if?",
             ["'0' (string com um caractere)", "[0] (lista com um elemento)", "0.0", "' ' (espaço)"], 2,
             "0.0 é o número zero em ponto flutuante — falsy. Os outros três são coleções ou strings não vazias, logo truthy."),
    ],
    projeto=(
        "Escreva caixa.py: dado um valor de compra e o valor pago, calcule o troco "
        "e imprima quantas notas de 100, 50, 20, 10, 5, 2 e moedas de 1 devolver. "
        "Valide com is que o valor pago não é None antes de calcular."
    ),
    leitura=["docs.python.org/pt-br/3/reference/expressions.html", "docs.python.org/pt-br/3/reference/datamodel.html#object.__eq__"],
))

# ---------------------------------------------------------------- DIA 4
DIAS.append(Dia(
    numero=4,
    titulo="Strings: fatiamento, métodos e f-strings",
    nivel="Iniciante",
    duracao="90 min",
    objetivos=[
        "Indexar e fatiar strings com [i] e [inicio:fim:passo] com confiança",
        "Explicar por que strings são imutáveis e o que isso implica na prática",
        "Usar os métodos mais frequentes de str para limpar e transformar texto",
        "Formatar saída com f-strings, incluindo a mini-linguagem de formatação",
        "Diferenciar strings comuns, cruas (raw) e multilinha",
        "Escrever suas primeiras funções usando o molde mínimo com def/return",
    ],
    teoria="""
ATENÇÃO: a partir de hoje os exercícios pedem FUNÇÕES. A sintaxe completa de
funções (parâmetros com valor padrão, *args, **kwargs, escopo) chega no Dia
11; por ora basta o molde mínimo, que já é suficiente para resolver os
exercícios dos próximos dias:

    def nome_da_funcao(parametro):
        resultado = ...        # faça o cálculo aqui dentro
        return resultado       # devolva o valor para quem chamou

`def` declara a função; o bloco indentado abaixo é o corpo. `return`
encerra a execução da função IMEDIATAMENTE e entrega o valor a quem a
chamou. Se a função terminar sem um `return` explícito, ela devolve `None`
silenciosamente — uma fonte comum de bugs sutis para iniciantes.

1. String é uma sequência imutável de caracteres
------------------------------------------------------
    s = "Python"
    s[0]     -> 'P'                     (índices começam em 0)
    s[-1]    -> 'n'                     (índices negativos contam do fim)
    s[0] = "J"                          -> TypeError: 'str' object does not support item assignment

Diferente de listas (Dia 8), strings NÃO podem ser alteradas depois de
criadas. Toda operação que parece "modificar" uma string (como `.upper()`
ou `.replace()`) na verdade cria e devolve uma string NOVA, deixando a
original intacta. Isso tem uma vantagem prática: strings podem ser usadas
como chave de dicionário (Dia 9) e compartilhadas com segurança entre partes
diferentes de um programa, sem risco de uma parte alterar o que a outra vê.

2. Fatiamento: s[inicio:fim:passo]
----------------------------------------
A regra mais importante do fatiamento: o `fim` é sempre EXCLUSIVO — o
caractere naquela posição NÃO entra no resultado. Omitir uma das três partes
significa "do começo" (início) ou "até o fim" (fim) ou "de um em um" (passo):

    s[0:3]    -> 'Pyt'      (posições 0, 1, 2 — para antes de 3)
    s[2:]     -> 'thon'     (da posição 2 até o fim)
    s[:3]     -> 'Pyt'      (do começo até a posição 3, exclusiva)
    s[:-1]    -> 'Pytho'    (tudo menos o último caractere)
    s[::2]    -> 'Pto'      (de 2 em 2, começando do 0)
    s[::-1]   -> 'nohtyP'   (passo -1: percorre de trás para frente — o idioma clássico para inverter)

Uma vantagem do fatiamento sobre indexação direta: ele NUNCA levanta erro de
índice fora do alcance. `s[100:200]` numa string curta simplesmente devolve
`''` (string vazia), enquanto `s[100]` levantaria `IndexError`.

3. Métodos essenciais de string
---------------------------------
    .upper() .lower() .title() .capitalize() .swapcase()
    .strip() .lstrip() .rstrip()          remove espaços (ou outros caracteres) das pontas
    .replace(velho, novo, [n])            substitui ocorrências (todas, ou só as n primeiras)
    .split(sep)      -> lista             "a,b,c".split(",")  -> ['a', 'b', 'c']
    .split()         -> lista             "  a  b ".split()   -> ['a', 'b']  (sem args: separa por qualquer espaço em branco, ignorando extras)
    sep.join(lista)  -> str               ",".join(['a','b']) -> 'a,b'
    .find(sub)       -> índice ou -1      (não gera erro se não achar)
    .index(sub)      -> índice ou ValueError  (gera erro se não achar)
    .count(sub)                            conta ocorrências não sobrepostas
    .startswith() .endswith()              testa prefixo/sufixo
    .isdigit() .isalpha() .isalnum() .isspace()   testes de composição de caracteres
    .zfill(n) .center(n) .ljust(n) .rjust(n)      preenchimento e alinhamento

Um erro clássico de quem está começando: esquecer que os métodos de string
DEVOLVEM uma string nova em vez de alterar a original:

    nome = "  Ana  "
    nome.strip()           # cria uma nova string 'Ana', mas NÃO altera nome
    print(nome)             # ainda imprime '  Ana  ' com os espaços!
    nome = nome.strip()    # agora sim: reatribuído, nome vale 'Ana'

4. f-strings: a forma moderna de formatar (Python 3.6+)
-----------------------------------------------------------
f-strings (formatted string literals) permitem embutir expressões Python
diretamente dentro do texto, prefixando a string com `f`:

    nome, saldo = "Ana", 1234.5678
    f"{nome} tem R$ {saldo:.2f}"          -> 'Ana tem R$ 1234.57'
    f"{saldo:>12,.2f}"                    -> '    1,234.57'    (largura 12, separador de milhar, 2 casas)
    f"{nome:*^11}"                        -> '****Ana****'     (centralizado, preenchido com *)
    f"{2**10=}"                           -> '2**10=1024'      (recurso de depuração: mostra a expressão E o valor)

A mini-linguagem de formato dentro das chaves segue este padrão:

    {valor:[preenchimento][alinhamento][sinal][largura][,][.precisão][tipo]}

Alinhamento: `<` esquerda (padrão para texto), `>` direita (padrão para
números), `^` centralizado. Tipos comuns: `d` (inteiro), `f` (float com casas
fixas), `e` (notação científica), `%` (porcentagem), `b` (binário), `x`
(hexadecimal).

Antes das f-strings, o Python usava `.format()` e o operador `%`. Você ainda
vai encontrar esses dois estilos em código legado, mas f-strings são hoje o
padrão recomendado por serem mais legíveis e ligeiramente mais rápidas.

5. Escapes e strings cruas (raw strings)
--------------------------------------------
    \\n nova linha   \\t tabulação   \\\\ barra invertida literal   \\" aspas dentro de aspas duplas

Strings cruas, prefixadas com `r`, desativam completamente o processamento
de escapes — cada barra invertida é tratada literalmente. Isso é
indispensável para caminhos do Windows e, principalmente, para expressões
regulares (Dia 26), onde `\\d`, `\\w` etc. têm significado próprio que não
deve ser confundido com escapes de string:

    r"C:\\novo\\pasta"    # cada \\ é literal, não vira quebra de linha nem nada
    r"\\d{2}/\\d{2}"      # típico em regex: sem o r, teríamos que escrever \\\\d

6. Strings multilinha
-------------------------
Três aspas (simples ou duplas) preservam quebras de linha dentro da própria
string, sem precisar de `\\n` explícito. São muito usadas em docstrings
(Dia 1) e em textos ou templates mais longos:

    aviso = \"\"\"
    Este programa apaga arquivos.
    Use com cuidado.
    \"\"\"
""",
    exemplos=[
        Exemplo(
            titulo="Limpando e formatando entrada bagunçada",
            codigo='''bruto = "   ANA maria DA silva  "
nome = bruto.strip().title()
print(f"[{nome}]")                     # [Ana Maria Da Silva]
partes = nome.split()
print(f"{partes[-1]}, {' '.join(partes[:-1])}")
''',
            explicacao="Encadeamento de métodos (strip().title()) é comum e "
                       "legível: cada método devolve uma nova string, sobre "
                       "a qual o próximo método já pode ser chamado.",
        ),
        Exemplo(
            titulo="Relatório alinhado com f-strings",
            codigo='''itens = [("Café", 24.9), ("Açúcar", 5.5), ("Filtro", 12.75)]
print(f"{'Produto':<12}{'Preço':>10}")
print("-" * 22)
for nome, preco in itens:
    print(f"{nome:<12}{preco:>10.2f}")
''',
            explicacao="Alinhamento com < e > cria tabelas legíveis no "
                       "terminal, sem precisar contar espaços manualmente.",
        ),
        Exemplo(
            titulo="Strings cruas para caminhos e padrões",
            codigo='''caminho_errado = "C:\\novo\\teste"    # \\n e \\t viram escapes indesejados!
caminho_certo = r"C:\\novo\\teste"     # cada \\ e tratado literalmente

print(repr(caminho_errado))
print(repr(caminho_certo))
''',
            explicacao="repr() mostra a string com os caracteres especiais "
                       "visíveis, revelando a diferença entre as duas versões.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d04e1",
            enunciado=(
                "Escreva gritar(texto) que remove espaços das pontas, deixa tudo\n"
                "em MAIÚSCULAS e acrescenta um ponto de exclamação no final."
            ),
            funcao="gritar",
            assinatura="def gritar(texto):",
            testes=[
                ("gritar('  ola  ')", "'OLA!'"),
                ("gritar('python')", "'PYTHON!'"),
                ("gritar('  ja e tarde')", "'JA E TARDE!'"),
            ],
            dica="Encadeie .strip() e .upper() e concatene '!'.",
        ),
        Exercicio(
            id="d04e2",
            enunciado="Escreva inverter(texto) que devolve o texto de trás para frente.",
            funcao="inverter",
            assinatura="def inverter(texto):",
            testes=[
                ("inverter('abc')", "'cba'"),
                ("inverter('')", "''"),
                ("inverter('ana')", "'ana'"),
            ],
            dica="Fatiamento com passo -1.",
        ),
        Exercicio(
            id="d04e3",
            enunciado=(
                "Escreva eh_palindromo(texto) que ignora maiúsculas/minúsculas e\n"
                "espaços e diz se o texto é um palíndromo."
            ),
            funcao="eh_palindromo",
            assinatura="def eh_palindromo(texto):",
            testes=[
                ("eh_palindromo('Ame a ema')", "True"),
                ("eh_palindromo('Python')", "False"),
                ("eh_palindromo('a')", "True"),
                ("eh_palindromo('Anilina')", "True"),
            ],
            nivel="medio",
            dica="Normalize com .lower().replace(' ', '') e compare com o reverso.",
        ),
    ],
    quiz=[
        Quiz("O que devolve 'Python'[1:4]?",
             ["'Pyt'", "'yth'", "'ytho'", "'tho'"], 1,
             "Começa no índice 1 ('y') e para ANTES do índice 4 (exclusivo), resultando em 'yth'."),
        Quiz("Por que nome.strip() sozinho não altera a variável nome?",
             ["Porque strip é lento", "Porque str é imutável e o método devolve uma nova string",
              "Porque falta o parêntese", "Porque strip só funciona em listas"], 1,
             "Strings são imutáveis: todo método que 'transforma' uma string devolve uma nova, e é preciso reatribuir o resultado."),
        Quiz("Qual a diferença entre .find() e .index() ao procurar uma substring ausente?",
             ["Não há diferença", "find() devolve -1, index() levanta ValueError",
              "find() levanta erro, index() devolve -1", "Ambos sempre devolvem None"], 1,
             "find() é mais tolerante (devolve -1); index() é mais estrito e levanta exceção se não encontrar."),
        Quiz("Para que serve o prefixo r antes de uma string, como em r'C:\\\\novo'?",
             ["Torna a string maiúscula", "Repete a string", "Desativa o processamento de escapes (\\n, \\t etc.)", "Converte para bytes"], 2,
             "String crua (raw): cada caractere é tratado literalmente, essencial para caminhos e regex."),
    ],
    projeto=(
        "Crie analisador.py: leia uma frase e mostre número de caracteres, de palavras, "
        "a frase invertida, em maiúsculas, e a palavra mais longa. Use f-strings para "
        "formatar toda a saída de forma alinhada."
    ),
    leitura=["docs.python.org/pt-br/3/library/string.html#format-specification-mini-language", "docs.python.org/pt-br/3/library/stdtypes.html#string-methods"],
))
# ---------------------------------------------------------------- DIA 5
DIAS.append(Dia(
    numero=5,
    titulo="Condicionais: if, elif, else e match",
    nivel="Iniciante",
    duracao="80 min",
    objetivos=[
        "Escrever decisões com if/elif/else e entender a ordem de avaliação",
        "Escrever condições no estilo idiomático do Python, não traduzido de outra linguagem",
        "Usar o operador ternário sem sacrificar legibilidade",
        "Evitar aninhamento excessivo com cláusulas de guarda",
        "Usar match/case (Python 3.10+) para casamento de padrões estruturais",
        "Reconhecer as armadilhas mais comuns ao comparar valores em condições",
    ],
    teoria="""
1. Estrutura básica
-----------------------
    if condicao:
        # bloco executado se condicao for verdadeira
    elif outra_condicao:
        # bloco executado se a primeira falhou E esta for verdadeira
    else:
        # bloco executado se NENHUMA condição acima foi verdadeira

O bloco é definido pela INDENTAÇÃO (4 espaços é a convenção — veja o Dia 1),
não por chaves como em C/Java/JavaScript. Os dois-pontos ao final da linha
de condição são obrigatórios. É crucial entender que apenas o PRIMEIRO ramo
verdadeiro executa — mesmo que uma condição mais abaixo também seria
verdadeira, ela nunca é sequer avaliada:

    idade = 25
    if idade >= 18:
        print("maior de idade")
    elif idade >= 21:
        print("nunca aparece, mesmo sendo tecnicamente verdadeiro")

Isso significa que a ORDEM dos `elif` importa muito quando as condições se
sobrepõem — organize sempre do caso mais específico para o mais genérico, ou
vice-versa, de forma consciente.

2. Escrevendo condições no estilo Python (não traduzidas de outra linguagem)
--------------------------------------------------------------------------------
Quem vem de outra linguagem costuma escrever Python "sotacado". Compare:

    if len(lista) > 0:              ->    if lista:
    if nome != "":                  ->    if nome:
    if valor == None:               ->    if valor is None:
    if idade >= 0 and idade <= 10:  ->    if 0 <= idade <= 10:
    if letra == "a" or letra == "e" or letra == "i" or letra == "o" or letra == "u":
                                    ->    if letra in "aeiou":
    if tipo == "a" or tipo == "b":  ->    if tipo in ("a", "b"):

A coluna da direita não é só "mais curta" — ela expressa a intenção de forma
mais direta e é o que a comunidade Python espera ao ler seu código.

3. Operador ternário: útil, mas com limite
------------------------------------------------
    status = "aprovado" if nota >= 6 else "reprovado"

A sintaxe é `valor_se_verdadeiro if condicao else valor_se_falso` — repare
que a condição fica no MEIO, ao contrário do `if` comum, o que confunde
muita gente na primeira vez. Use o ternário apenas quando ele cabe
confortavelmente em uma linha e expressa uma escolha simples entre dois
valores; para lógica com mais de uma condição, um `if/elif/else` tradicional
é mais legível — encadear vários ternários (`a if x else b if y else c`)
é tecnicamente válido, mas quase sempre um sinal de que está na hora de
reescrever como um `if` de várias linhas.

4. Cláusulas de guarda: eliminando aninhamento
----------------------------------------------------
Um padrão comum entre iniciantes é aninhar `if`s dentro de `if`s, criando o
que a comunidade chama de "flecha" (arrow code), pelo formato triangular que
a indentação forma:

    def processar(pedido):
        if pedido:
            if pedido["pago"]:
                if pedido["estoque"]:
                    return "enviar"
        return "aguardar"

O código funciona, mas cada nível de indentação exige que o leitor carregue
mentalmente todas as condições anteriores. A alternativa profissional é
inverter a lógica e sair cedo — uma cláusula de guarda por vez, sempre no
início da função:

    def processar(pedido):
        if not pedido:
            return "aguardar"
        if not pedido["pago"]:
            return "aguardar"
        if not pedido["estoque"]:
            return "aguardar"
        return "enviar"

O código fica PLANO (sem aninhamento) e cada linha só precisa ser lida uma
vez, isoladamente — sem carregar contexto de condições anteriores na
cabeça. Esse padrão aparece o tempo todo em código profissional e vai
reaparecer com força no Dia 15, quando tratamos erros com exceções.

5. match/case (Python 3.10+): não é um "switch" simples
--------------------------------------------------------------
Quem já programou em C, Java ou JavaScript pode olhar para `match/case` e
pensar "ah, é um switch". Não é bem isso: `match` faz CASAMENTO DE PADRÕES
ESTRUTURAIS — ele pode desconstruir listas, tuplas, dicionários e até
objetos de classes próprias (Dia 16), não só comparar um valor simples:

    match comando.split():
        case ["sair"]:
            return "encerrando"
        case ["somar", a, b]:
            return int(a) + int(b)
        case ["ler", nome, *resto]:
            return f"lendo {nome} ({len(resto)} extras)"
        case _:
            return "comando desconhecido"

Repare que `case ["somar", a, b]` não é apenas uma comparação: ele verifica
se a lista tem exatamente 3 elementos, se o primeiro é a string `"somar"` e,
se tudo isso bater, atribui automaticamente o segundo e o terceiro elemento
às variáveis `a` e `b`. É simultaneamente um teste E uma atribuição.

`case _:` é o padrão coringa (equivalente ao `default` de um switch), e
Python exige que ele venha por último, já que os padrões são testados na
ordem em que aparecem, de cima para baixo — igual ao `elif`.

`match` também casa dicionários por CHAVES presentes, sem exigir que o
dicionário tenha exatamente essas chaves e nenhuma outra:

    match evento:
        case {"tipo": "pix", "valor": v}:
            print(f"pix de R$ {v}")

E aceita guardas adicionais com `if`, refinando um padrão que já bateu
estruturalmente:

    case {"tipo": "tecla", "valor": v} if v.isdigit():
        return f"digito {v}"

6. Armadilhas comuns
------------------------
- `=` (atribuição) vs `==` (comparação): escrever `if x = 5:` por engano é
  comum em outras linguagens, mas em Python isso é um SyntaxError imediato
  — a linguagem simplesmente não permite atribuição dentro de um `if` sem
  sintaxe especial, o que evita uma classe inteira de bugs silenciosos.

- O operador morsa `:=` (walrus operator, Python 3.8+) permite atribuir uma
  variável DENTRO de uma expressão, algo que antes exigiria duas linhas:

      if (n := len(dados)) > 100:
          print(f"{n} itens, grande demais para processar de uma vez")

  Sem o operador morsa, seria necessário escrever `n = len(dados)` numa
  linha e só depois `if n > 100:` na seguinte — o `:=` economiza essa
  repetição quando o valor intermediário só importa dentro da condição.

- Comparar floats com `==` é arriscado, como vimos no Dia 2 — prefira
  `math.isclose(a, b)` quando a precisão de ponto flutuante estiver em jogo.
""",
    exemplos=[
        Exemplo(
            titulo="Faixas de valor com elif",
            codigo='''def faixa_etaria(idade):
    if idade < 0:
        return "invalida"
    elif idade < 12:
        return "crianca"
    elif idade < 18:
        return "adolescente"
    elif idade < 60:
        return "adulto"
    return "idoso"

print(faixa_etaria(15))     # adolescente
''',
            explicacao="A ordem importa: cada elif já assume implicitamente "
                       "que todos os anteriores falharam — por isso 'idade < 18' "
                       "não precisa repetir 'idade >= 12'.",
        ),
        Exemplo(
            titulo="match com padrões estruturais e guarda",
            codigo='''def responder(evento):
    match evento:
        case {"tipo": "clique", "x": x, "y": y}:
            return f"clique em ({x}, {y})"
        case {"tipo": "tecla", "valor": v} if v.isdigit():
            return f"digito {v}"
        case {"tipo": "tecla"}:
            return "tecla nao numerica"
        case _:
            return "evento ignorado"

print(responder({"tipo": "clique", "x": 3, "y": 9}))
''',
            explicacao="Note a guarda `if v.isdigit()` refinando o padrão: o "
                       "dicionário precisa bater com o padrão E satisfazer a "
                       "condição extra para cair nesse case.",
        ),
        Exemplo(
            titulo="Cláusula de guarda vs. aninhamento (mesmo resultado, legibilidade diferente)",
            codigo='''def pode_dirigir_ruim(idade, tem_cnh):
    if idade >= 18:
        if tem_cnh:
            return True
        else:
            return False
    else:
        return False

def pode_dirigir_bom(idade, tem_cnh):
    if idade < 18:
        return False
    if not tem_cnh:
        return False
    return True

print(pode_dirigir_ruim(20, True), pode_dirigir_bom(20, True))
''',
            explicacao="As duas funções fazem exatamente a mesma coisa, mas "
                       "a segunda é plana e cada linha se explica sozinha, "
                       "sem exigir que você acompanhe o aninhamento.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d05e1",
            enunciado=(
                "Escreva classificar(nota) que devolve 'A' para nota >= 90,\n"
                "'B' >= 80, 'C' >= 70, 'D' >= 60 e 'F' abaixo disso."
            ),
            funcao="classificar",
            assinatura="def classificar(nota):",
            testes=[
                ("classificar(95)", "'A'"),
                ("classificar(80)", "'B'"),
                ("classificar(70)", "'C'"),
                ("classificar(61)", "'D'"),
                ("classificar(12)", "'F'"),
            ],
            dica="Teste do maior para o menor usando elif.",
        ),
        Exercicio(
            id="d05e2",
            enunciado="Escreva maior_de_tres(a, b, c) devolvendo o maior valor (sem usar max).",
            funcao="maior_de_tres",
            assinatura="def maior_de_tres(a, b, c):",
            testes=[
                ("maior_de_tres(1, 2, 3)", "3"),
                ("maior_de_tres(9, 2, 3)", "9"),
                ("maior_de_tres(-1, -5, -3)", "-1"),
                ("maior_de_tres(5, 5, 2)", "5"),
            ],
            dica="Compare a com b, depois o vencedor com c.",
        ),
        Exercicio(
            id="d05e3",
            enunciado=(
                "Escreva tipo_triangulo(a, b, c) que devolve 'invalido' se os lados não\n"
                "formam triângulo (cada lado deve ser menor que a soma dos outros dois),\n"
                "senão 'equilatero', 'isosceles' ou 'escaleno'."
            ),
            funcao="tipo_triangulo",
            assinatura="def tipo_triangulo(a, b, c):",
            testes=[
                ("tipo_triangulo(1, 2, 10)", "'invalido'"),
                ("tipo_triangulo(3, 3, 3)", "'equilatero'"),
                ("tipo_triangulo(3, 3, 5)", "'isosceles'"),
                ("tipo_triangulo(3, 4, 5)", "'escaleno'"),
            ],
            nivel="medio",
            dica="Valide primeiro (cláusula de guarda), depois conte lados iguais.",
        ),
    ],
    quiz=[
        Quiz("Quantos ramos de um if/elif/elif/else executam, no máximo?",
             ["todos os verdadeiros", "no máximo um", "sempre dois", "depende da indentação"], 1,
             "A execução para no primeiro ramo verdadeiro; os demais nem são avaliados."),
        Quiz("O que faz `case _:` em um match?",
             ["Ignora o valor", "Casa com qualquer coisa (default)", "Causa erro", "Compara com underscore"], 1,
             "_ é o padrão coringa, equivalente ao default de um switch, e deve vir por último."),
        Quiz("Por que a cláusula de guarda (sair cedo com return) é preferida a aninhar ifs?",
             ["É mais rápida de executar", "Deixa o código plano, sem exigir que o leitor acumule condições anteriores",
              "É a única forma de retornar um valor", "Funciona apenas com match"], 1,
             "É uma questão de legibilidade: cada linha se explica isoladamente, sem depender de contexto acumulado."),
        Quiz("O que o operador morsa (:=) permite fazer?",
             ["Comparar dois valores", "Atribuir uma variável dentro de uma expressão, como dentro de um if",
              "Criar uma tupla", "Repetir uma string"], 1,
             "Ele evita escrever a atribuição numa linha separada quando o valor só importa dentro da condição."),
    ],
    projeto=(
        "Faça imc.py: leia peso e altura, calcule o IMC e classifique em abaixo do peso, "
        "normal, sobrepeso ou obesidade, validando entradas negativas com cláusulas de guarda."
    ),
    leitura=["PEP 636 - Structural Pattern Matching Tutorial", "PEP 572 - Assignment Expressions (o operador morsa)"],
))

# ---------------------------------------------------------------- DIA 6
DIAS.append(Dia(
    numero=6,
    titulo="Repetição com while, break e continue",
    nivel="Iniciante",
    duracao="80 min",
    objetivos=[
        "Escrever laços while corretos, entendendo cada uma das suas quatro partes",
        "Usar break, continue e o bloco else exclusivo do while do Python",
        "Construir menus e rotinas de validação de entrada com while True",
        "Reconhecer e aplicar os padrões acumulador, contador e sentinela",
        "Diagnosticar e evitar loops infinitos antes que eles travem o programa",
    ],
    teoria="""
1. Anatomia completa do while
---------------------------------
Todo `while` bem formado tem quatro partes, mesmo que elas não estejam
sempre visualmente próximas umas das outras:

    contador = 0                 # 1. inicialização (antes do laço)
    while contador < 5:          # 2. condição (testada a cada volta)
        print(contador)          # 3. corpo (o que o laço realmente faz)
        contador += 1            # 4. atualização (o que muda a cada volta)

A parte 4 é a que mais gera bugs: esquecer de atualizar a variável que a
condição testa produz um LOOP INFINITO — o programa nunca sai dali, porque a
condição nunca deixa de ser verdadeira. Se isso acontecer no terminal,
Ctrl+C interrompe a execução manualmente.

Diferente do `for` (Dia 7), o `while` não sabe automaticamente quando parar
— ele só sabe repetir enquanto uma condição continuar verdadeira. Por isso
ele é a ferramenta certa quando você NÃO sabe de antemão quantas vezes vai
repetir (esperar uma entrada válida do usuário, por exemplo), enquanto o
`for` é melhor quando você já sabe o que vai percorrer.

2. break e continue
-----------------------
`break` sai IMEDIATAMENTE do laço mais interno, sem terminar a iteração
atual. `continue` pula o restante do corpo e volta direto para o teste da
condição, começando a próxima iteração.

    while True:                       # laço "infinito" controlado por dentro
        comando = input("> ")
        if comando == "sair":
            break                     # sai do laço aqui
        if not comando:
            continue                  # ignora linha vazia e volta ao input
        print("executando", comando)

O padrão `while True: ... break` parece contraditório à primeira vista
("infinito" que na verdade não é), mas é extremamente idiomático em Python
para menus e validação de entrada — ele costuma ser mais claro que
duplicar a lógica de leitura antes e dentro do laço, uma alternativa comum
em outras linguagens.

3. O bloco else do laço: um recurso exclusivo do Python
-------------------------------------------------------------
Poucas linguagens têm isso, e por isso costuma confundir quem já programou
em outro lugar: o `while` (e também o `for`) pode ter um bloco `else`, que
executa quando o laço termina NATURALMENTE — ou seja, quando a condição
ficou falsa por conta própria, sem que um `break` tenha interrompido antes:

    n, divisor = 91, 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            print("composto")
            break
        divisor += 1
    else:
        print("primo")

A forma mais fácil de entender é ler `else` aqui como "senão, nenhum break
aconteceu" — ele é o par lógico do `break`, não do `if`. Esse padrão é
comum em buscas: "procure por algo; se achar, break; se terminar a busca
inteira sem achar nada, faça X no else".

4. Padrões clássicos de laço
---------------------------------
Acumulador (soma valores progressivamente):

    soma = 0
    while ...:
        soma += valor

Contador (conta quantas vezes algo acontece):

    quantidade = 0
    while ...:
        if condicao:
            quantidade += 1

Sentinela (repete até o usuário digitar um valor especial que sinaliza
"parar", geralmente uma string vazia):

    while (linha := input("valor (vazio p/ sair): ")):
        processar(linha)

Aqui o operador morsa (Dia 5) permite atribuir e testar `linha` na mesma
expressão — sem ele, seria preciso duplicar o `input()` antes do laço.

Redução de número dígito a dígito (muito comum em exercícios matemáticos):

    n, digitos = 12345, 0
    while n > 0:
        n //= 10
        digitos += 1

5. Como evitar (e diagnosticar) um loop infinito
------------------------------------------------------
- garanta que ALGUMA variável usada na condição realmente muda dentro do
  corpo do laço — é a causa mais comum de loop infinito;
- prefira `<` a `!=` quando o passo do incremento puder "pular" o valor
  exato de parada (por exemplo, `contador += 2` nunca vai bater
  exatamente em um número ímpar se `contador` começa par: `!=` nunca seria
  satisfeito, mas `<` sempre é, eventualmente);
- em laços que dependem de entrada do usuário, garanta sempre uma saída
  clara (um `break` alcançável ou uma condição sentinela);
- no ambiente deste curso, o corretor automático interrompe qualquer
  exercício após 12 segundos e avisa que provavelmente há um loop infinito
  — é exatamente esse tipo de erro que ele foi desenhado para capturar.
""",
    exemplos=[
        Exemplo(
            titulo="Validação de entrada com while True",
            codigo='''while True:
    texto = input("Digite um numero positivo: ")
    if texto.isdigit() and int(texto) > 0:
        numero = int(texto)
        break
    print("Entrada invalida, tente de novo.")
print("Voce digitou", numero)
''',
            explicacao="Só sai do laço quando a entrada é realmente válida — "
                       "o padrão 'while True + break' garante isso sem "
                       "duplicar a leitura antes do laço.",
        ),
        Exemplo(
            titulo="Sequência de Fibonacci com while",
            codigo='''a, b = 0, 1
while a < 100:
    print(a, end=" ")
    a, b = b, a + b
print()
''',
            explicacao="Atribuição múltipla (a, b = b, a + b) evita precisar "
                       "de uma variável temporária para guardar o valor "
                       "antigo de a enquanto calcula o novo b.",
        ),
        Exemplo(
            titulo="else do while: buscando um número primo",
            codigo='''def eh_primo(n):
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False   # achou um divisor: nao e primo
        divisor += 1
    else:
        return True        # o laco terminou sem break: e primo

for numero in (7, 8, 97):
    print(numero, eh_primo(numero))
''',
            explicacao="Aqui o else nem chega a ser necessário na prática "
                       "(o return já sai da função), mas ilustra a leitura: "
                       "'se o laço não foi interrompido, retorne True'.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d06e1",
            enunciado="Escreva soma_ate(n) que soma todos os inteiros de 1 até n usando while (0 se n < 1).",
            funcao="soma_ate",
            assinatura="def soma_ate(n):",
            testes=[
                ("soma_ate(5)", "15"),
                ("soma_ate(1)", "1"),
                ("soma_ate(0)", "0"),
                ("soma_ate(100)", "5050"),
            ],
            dica="Acumulador + contador que cresce até n.",
        ),
        Exercicio(
            id="d06e2",
            enunciado=(
                "Escreva contar_digitos(n) que devolve quantos dígitos tem um inteiro\n"
                "não negativo. contar_digitos(0) deve valer 1. Não use str()."
            ),
            funcao="contar_digitos",
            assinatura="def contar_digitos(n):",
            testes=[
                ("contar_digitos(0)", "1"),
                ("contar_digitos(7)", "1"),
                ("contar_digitos(12345)", "5"),
                ("contar_digitos(1000000)", "7"),
            ],
            nivel="medio",
            dica="Divida por 10 repetidamente com //= e conte as divisões.",
        ),
        Exercicio(
            id="d06e3",
            enunciado=(
                "Conjectura de Collatz: se n é par, divida por 2; se ímpar, faça 3n+1.\n"
                "Escreva passos_collatz(n) devolvendo quantos passos até chegar a 1."
            ),
            funcao="passos_collatz",
            assinatura="def passos_collatz(n):",
            testes=[
                ("passos_collatz(1)", "0"),
                ("passos_collatz(2)", "1"),
                ("passos_collatz(6)", "8"),
                ("passos_collatz(27)", "111"),
            ],
            nivel="dificil",
            dica="while n != 1: aplique a regra e incremente o contador.",
        ),
    ],
    quiz=[
        Quiz("Quando o bloco else de um while executa?",
             ["Sempre", "Quando o laço termina sem break", "Quando há break", "Nunca"], 1,
             "else só roda se a condição ficou falsa naturalmente, sem interrupção por break."),
        Quiz("O que causa um loop infinito com mais frequência?",
             ["Usar break", "Esquecer de atualizar a variável da condição",
              "Usar continue", "Indentar com 4 espaços"], 1,
             "Sem atualização, a condição do while nunca deixa de ser verdadeira."),
        Quiz("Por que 'while contador != 10' pode ser mais arriscado que 'while contador < 10'?",
             ["Não há diferença nenhuma", "!= é mais lento de calcular",
              "Se o passo do contador pular o valor 10, != nunca é satisfeito e o laço não para",
              "< não funciona com inteiros"], 2,
             "Um passo de 2, por exemplo, pode nunca bater exatamente em 10 se o contador começa ímpar."),
        Quiz("O que o padrão 'while True: ... break' costuma representar?",
             ["Um erro de lógica sempre", "Um menu ou validação de entrada, saindo quando a condição de parada é atingida",
              "Um laço que nunca deveria terminar de fato", "Uma forma antiga de escrever for"], 1,
             "É idiomático em Python para repetir até uma condição interna (não testável antes) ser satisfeita."),
    ],
    projeto=(
        "Crie jogo_adivinha.py: o programa sorteia um número de 1 a 100 (random.randint) "
        "e o jogador tenta adivinhar, recebendo dicas 'maior'/'menor' até acertar. Conte as tentativas "
        "e use o bloco else do while para exibir uma mensagem final apenas quando o jogador acertar."
    ),
    leitura=["docs.python.org/pt-br/3/tutorial/controlflow.html"],
))

# ---------------------------------------------------------------- DIA 7
DIAS.append(Dia(
    numero=7,
    titulo="for, range, enumerate e zip",
    nivel="Iniciante",
    duracao="80 min",
    objetivos=[
        "Iterar sobre qualquer sequência com for, entendendo que é um 'for-each'",
        "Usar range com início, fim e passo, e saber por que ele é preguiçoso",
        "Aplicar enumerate e zip em vez de manipular índices manualmente",
        "Escrever laços aninhados com consciência do custo de cada um",
        "Usar funções que consomem iteráveis (sum, any, all, sorted) em vez de reinventá-las",
        "Evitar o erro clássico de modificar uma lista enquanto a percorre",
    ],
    teoria="""
1. for percorre elementos, não índices
---------------------------------------------
    for letra in "abc":
        print(letra)

    for item in [10, 20, 30]:
        print(item)

Diferente de C ou Java, onde o `for` clássico manipula um contador
numérico (`for (int i = 0; i < n; i++)`), o `for` do Python é o que se
chama de "for-each": ele entrega diretamente cada ELEMENTO da sequência, um
de cada vez, sem que você precise gerenciar um índice manualmente. Se você
realmente precisar do índice junto com o valor, a ferramenta certa é
`enumerate` (seção 3) — escrever `for i in range(len(lista)):` e depois
indexar com `lista[i]` é considerado um antipadrão em Python, quase sempre
substituível por algo mais direto.

2. range(inicio, fim, passo): uma sequência preguiçosa
--------------------------------------------------------------
    range(5)          -> 0 1 2 3 4        (um argumento: vai de 0 até fim-1)
    range(2, 6)       -> 2 3 4 5          (dois argumentos: início e fim)
    range(0, 10, 3)   -> 0 3 6 9          (três argumentos: início, fim, passo)
    range(5, 0, -1)   -> 5 4 3 2 1        (passo negativo: conta regressivamente)

Um detalhe importante de desempenho: `range` é PREGUIÇOSO (lazy) — ele não
cria uma lista inteira na memória de uma vez. `range(1_000_000)` ocupa uma
quantidade de memória praticamente constante, porque ele só calcula "qual é
o próximo número" sob demanda, à medida que o laço avança. Se você
realmente precisar de uma lista concreta de números (por exemplo, para
imprimir ou fatiar), materialize explicitamente com `list(range(5))`.

3. enumerate: índice e valor, sem gerenciamento manual
-----------------------------------------------------------
    for i, nome in enumerate(["ana", "bia"], start=1):
        print(i, nome)          # 1 ana / 2 bia

`enumerate` devolve pares (índice, valor) um de cada vez, e aceita um
parâmetro `start` para começar a contagem de um número diferente de 0 — útil
para exibir listas numeradas a partir de 1, como fazem interfaces
voltadas para usuários finais.

4. zip: percorrendo várias sequências em paralelo
-------------------------------------------------------
`zip` combina duas ou mais sequências, produzindo tuplas com um elemento de
cada, e PARA assim que a mais curta delas se esgota:

    nomes = ["ana", "bia", "cris"]
    notas = [9, 7]
    for nome, nota in zip(nomes, notas):
        print(nome, nota)       # ana 9 / bia 7   (cris fica de fora, sem erro)

Esse comportamento de "parar na mais curta" é conveniente na maioria dos
casos, mas pode esconder um bug real se as listas deveriam ter o mesmo
tamanho e não têm. Para isso, `zip(a, b, strict=True)` (a partir do Python
3.10) levanta `ValueError` explicitamente se os tamanhos diferirem — vale a
pena usar `strict=True` sempre que o alinhamento entre as sequências for uma
garantia que seu programa precisa manter.

Uma aplicação clássica de `zip`: `dict(zip(chaves, valores))` é a forma mais
direta de montar um dicionário (Dia 9) a partir de duas listas paralelas.

5. Desempacotamento dentro do for
----------------------------------------
Quando os elementos da sequência já são tuplas ou listas, o `for` pode
desempacotá-los diretamente nas variáveis do cabeçalho:

    pares = [(1, "um"), (2, "dois")]
    for numero, palavra in pares:
        print(numero, palavra)

Com o operador estrela, é possível capturar "o resto" dos elementos numa
lista à parte:

    primeiro, *resto = [1, 2, 3, 4]     # primeiro vale 1, resto vale [2, 3, 4]

6. Laços aninhados: cuidado com o custo
------------------------------------------------
    for i in range(1, 4):
        for j in range(1, 4):
            print(f"{i}x{j}={i*j}", end="  ")
        print()

Cada volta do laço externo dispara TODAS as voltas do laço interno. Se o
laço externo tem N elementos e o interno também tem N, o total de
operações é N ao quadrado (N²) — para N pequeno (dezenas) isso é
imperceptível, mas para N grande (milhões) o programa fica visivelmente
lento. Essa noção de "custo" é retomada com mais rigor no Dia 29
(desempenho e complexidade).

7. Funções que já sabem consumir um iterável inteiro
------------------------------------------------------------
Antes de escrever seu próprio laço para somar, contar ou verificar algo,
vale conferir se a biblioteca padrão já resolve isso:

    sum(), max(), min(), len(), sorted(), reversed(), any(), all()

    any(n > 10 for n in numeros)     # existe algum elemento maior que 10?
    all(n > 0 for n in numeros)      # TODOS os elementos são positivos?

`any` devolve `True` assim que encontra o primeiro elemento que satisfaz a
condição (curto-circuito, igual ao `and`/`or` do Dia 3); `all` devolve
`False` assim que encontra o primeiro que NÃO satisfaz. Usar essas funções
em vez de escrever um laço manual com uma variável booleana auxiliar deixa
o código mais curto e menos sujeito a erro de lógica.

8. Nunca modifique a lista que você está percorrendo
------------------------------------------------------------
    for item in lista:
        lista.remove(item)     # comportamento imprevisível e provavelmente errado

Ao remover elementos durante a iteração, os índices internos que o `for`
usa para saber "qual é o próximo" ficam dessincronizados com o conteúdo real
da lista — o resultado costuma ser pular elementos silenciosamente, sem
nenhum erro que avise que algo deu errado. A forma segura é iterar sobre uma
CÓPIA (`lista[:]` ou `list(lista)`) enquanto modifica a original, ou então
construir uma lista nova do zero com os elementos que você quer manter.
""",
    exemplos=[
        Exemplo(
            titulo="Tabela de multiplicação formatada",
            codigo='''for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i*j:4d}", end="")
    print()
''',
            explicacao="{:4d} reserva 4 colunas para cada número, alinhando "
                       "a tabela mesmo quando os valores têm quantidades "
                       "diferentes de dígitos.",
        ),
        Exemplo(
            titulo="Boletim com zip e enumerate",
            codigo='''alunos = ["Ana", "Bruno", "Carla"]
notas = [8.5, 6.0, 9.2]
for pos, (aluno, nota) in enumerate(sorted(zip(alunos, notas),
                                           key=lambda p: -p[1]), start=1):
    print(f"{pos}o {aluno:<8} {nota:.1f}")
''',
            explicacao="zip une as duas listas paralelas em pares; sorted "
                       "ordena esses pares por nota decrescente (o sinal de "
                       "menos inverte a ordem); enumerate numera o resultado.",
        ),
        Exemplo(
            titulo="Removendo com segurança durante a iteração",
            codigo='''numeros = [1, 2, 3, 4, 5, 6]

# ERRADO: modificar a lista original enquanto a percorre pula elementos
# for n in numeros:
#     if n % 2 == 0:
#         numeros.remove(n)

# CORRETO: iterar sobre uma copia, remover da original
for n in numeros[:]:
    if n % 2 == 0:
        numeros.remove(n)
print(numeros)     # [1, 3, 5]
''',
            explicacao="numeros[:] cria uma cópia rasa para percorrer, "
                       "enquanto .remove() age sobre a lista original sem "
                       "atrapalhar a iteração em andamento.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d07e1",
            enunciado="Escreva tabuada(n) que devolve a lista com n*1, n*2, ..., n*10.",
            funcao="tabuada",
            assinatura="def tabuada(n):",
            testes=[
                ("tabuada(3)", "[3, 6, 9, 12, 15, 18, 21, 24, 27, 30]"),
                ("tabuada(0)", "[0]*10"),
                ("len(tabuada(7))", "10"),
            ],
            dica="Use for com range(1, 11) e .append().",
        ),
        Exercicio(
            id="d07e2",
            enunciado=(
                "Escreva indices_de(lista, alvo) devolvendo a lista de posições em que\n"
                "alvo aparece (lista vazia se não aparecer)."
            ),
            funcao="indices_de",
            assinatura="def indices_de(lista, alvo):",
            testes=[
                ("indices_de([1, 2, 1, 3, 1], 1)", "[0, 2, 4]"),
                ("indices_de(['a', 'b'], 'z')", "[]"),
                ("indices_de([5], 5)", "[0]"),
            ],
            dica="enumerate dá índice e valor ao mesmo tempo.",
        ),
        Exercicio(
            id="d07e3",
            enunciado=(
                "Escreva produto_escalar(a, b): soma dos produtos elemento a elemento\n"
                "de duas listas de mesmo tamanho. Lista vazia devolve 0."
            ),
            funcao="produto_escalar",
            assinatura="def produto_escalar(a, b):",
            testes=[
                ("produto_escalar([1, 2, 3], [4, 5, 6])", "32"),
                ("produto_escalar([], [])", "0"),
                ("produto_escalar([2], [10])", "20"),
            ],
            nivel="medio",
            dica="zip(a, b) percorre os pares; acumule x*y.",
        ),
    ],
    quiz=[
        Quiz("O que produz list(range(5, 0, -1))?",
             ["[5,4,3,2,1]", "[5,4,3,2,1,0]", "[0,1,2,3,4]", "[]"], 0,
             "Passo -1 desce até 1, pois 0 é exclusivo (o fim nunca é incluído)."),
        Quiz("Qual a forma idiomática de obter índice e valor ao mesmo tempo?",
             ["range(len(x))", "enumerate(x)", "zip(x)", "x.index()"], 1,
             "enumerate é mais legível e menos suscetível a erro do que gerenciar um índice manual."),
        Quiz("O que acontece quando as listas passadas a zip() têm tamanhos diferentes?",
             ["Levanta erro sempre", "Preenche com None os espaços que faltam",
              "Para na sequência mais curta, silenciosamente (a menos que use strict=True)",
              "Trava o programa"], 2,
             "zip() para na mais curta por padrão; strict=True (3.10+) torna isso um erro explícito quando necessário."),
        Quiz("Por que 'for item in lista: lista.remove(item)' é perigoso?",
             ["É apenas mais lento, mas correto", "Modificar a lista durante a iteração dessincroniza os índices internos e pode pular elementos",
              "remove() não existe em listas", "for não aceita remove dentro do corpo"], 1,
             "A solução segura é iterar sobre uma cópia (lista[:]) enquanto modifica a lista original."),
    ],
    projeto=(
        "Escreva notas.py: dada uma lista de alunos e uma de notas, imprima um boletim "
        "alinhado com média geral, maior nota, menor nota e quantidade de aprovados (>= 6), "
        "usando any/all para checar rapidamente casos como 'todos aprovados' ou 'alguém zerou'."
    ),
    leitura=["docs.python.org/pt-br/3/library/functions.html", "docs.python.org/pt-br/3/library/stdtypes.html#range"],
))

# ---------------------------------------------------------------- DIA 8
DIAS.append(Dia(
    numero=8,
    titulo="Listas e tuplas",
    nivel="Iniciante",
    duracao="90 min",
    objetivos=[
        "Dominar os métodos de list que modificam no lugar versus os que consultam",
        "Entender mutabilidade, alias, cópia rasa e cópia profunda com precisão",
        "Ordenar com sort/sorted usando chave personalizada e múltiplos critérios",
        "Saber quando escolher tupla em vez de lista, e por quê",
        "Ter uma primeira noção do custo (Big O) das operações mais comuns de lista",
    ],
    teoria="""
1. Lista: sequência mutável e heterogênea
--------------------------------------------
    numeros = [3, 1, 4]
    misto = [1, "dois", 3.0, [4]]     # listas podem misturar tipos, inclusive outras listas

Métodos que MODIFICAM a lista NO LUGAR (e por isso devolvem `None`, não a
lista modificada — um erro clássico é esquecer disso):

    .append(x)          adiciona um único elemento ao fim
    .extend(iteravel)   concatena todos os elementos de outro iterável ao fim
    .insert(i, x)       insere x na posição i, empurrando os demais
    .remove(x)          remove a PRIMEIRA ocorrência de x (ValueError se x não existe)
    .pop([i])           remove E DEVOLVE o elemento (índice padrão: o último)
    .sort(key=, reverse=)   ordena a própria lista
    .reverse()           inverte a própria lista
    .clear()             esvazia a lista

Métodos de CONSULTA, que não alteram nada:

    .index(x)  .count(x)  len(lista)  x in lista

O erro mais clássico de quem está começando com listas:

    lista = lista.append(4)   # ARMADILHA: lista agora vale None!

Como `.append()` modifica a lista original e devolve `None`, reatribuir o
resultado a `lista` destrói a lista inteira, substituindo-a por `None`. A
forma correta é apenas chamar `lista.append(4)` sem reatribuir nada.

2. Fatiamento também funciona em listas
-------------------------------------------
Tudo o que vimos sobre fatiamento de strings (Dia 4) se aplica a listas,
com um poder extra: fatias de lista podem ser ATRIBUÍDAS, substituindo um
trecho inteiro de uma vez:

    l = [1, 2, 3, 4, 5]
    l[1:3]          # [2, 3]         (sublista, nova lista)
    l[::-1]         # [5, 4, 3, 2, 1]  (invertida)
    l[1:3] = [9]    # substitui l[1] e l[2] por um único elemento: l vira [1, 9, 4, 5]
    del l[0]        # remove pelo índice: l vira [9, 4, 5]

Note que `l[1:3] = [9]` MUDA O TAMANHO da lista, porque estamos
substituindo dois elementos por apenas um — isso é uma diferença marcante
em relação a arrays de tamanho fixo em outras linguagens.

3. Cópia: o ponto que mais gera bug em quem está aprendendo
-------------------------------------------------------------------
Retomando o conceito de "rótulo, não caixa" do Dia 2, existem quatro formas
distintas de "copiar" uma lista, cada uma com um significado diferente:

    b = a                                # ALIAS: b e a são o MESMO objeto
    b = a[:]                             # cópia RASA (shallow): novo contêiner externo
    b = list(a)                          # também cópia rasa, forma alternativa
    import copy; b = copy.deepcopy(a)    # cópia PROFUNDA (deep): duplica tudo, recursivamente

A cópia rasa duplica apenas o CONTÊINER mais externo — se a lista contém
outras listas (ou dicionários, ou objetos) dentro dela, esses elementos
internos continuam sendo COMPARTILHADOS entre o original e a cópia. Isso
produz uma armadilha muito conhecida:

    matriz = [[0] * 3] * 3      # ARMADILHA: as três "linhas" são o MESMO objeto lista!
    matriz[0][0] = 1            # muda as três linhas ao mesmo tempo, não só a primeira!
    print(matriz)                # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]

O motivo: `[[0] * 3] * 3` primeiro cria UMA lista `[0, 0, 0]`, e depois a
multiplicação externa `* 3` cria uma lista com TRÊS REFERÊNCIAS a essa mesma
lista interna — não três listas independentes. A forma correta de criar uma
matriz onde cada linha é de fato independente é usar uma compreensão de
lista (introduzida formalmente no Dia 10):

    correto = [[0] * 3 for _ in range(3)]    # cada iteração cria uma lista NOVA

4. Ordenação: sort() versus sorted()
-----------------------------------------
    ordenada = sorted(lista)          # devolve uma NOVA lista ordenada; a original não muda
    lista.sort()                      # ordena a PRÓPRIA lista no lugar; devolve None

`sorted()` funciona com qualquer iterável (inclusive tuplas e dicionários) e
sempre devolve uma lista nova; `.sort()` só existe em listas e as modifica
diretamente. Ambos aceitam os mesmos parâmetros nomeados:

    sorted(pessoas, key=lambda p: p["idade"], reverse=True)   # do mais velho ao mais novo
    sorted(palavras, key=len)                                   # da mais curta para a mais longa
    sorted(palavras, key=str.lower)                             # ordem alfabética ignorando maiúsculas

A ordenação em Python é ESTÁVEL: elementos que empatam no critério de
ordenação preservam sua ordem relativa original. Essa garantia permite
ordenar por VÁRIOS critérios em etapas, ou de uma vez usando uma tupla como
chave, do critério mais importante para o menos importante:

    sorted(pessoas, key=lambda p: (p["sobrenome"], p["nome"]))

Aqui Python ordena primeiro por sobrenome; entre pessoas com o mesmo
sobrenome, desempata pelo nome — exatamente como comparar tuplas
funcionaria numa comparação direta (`("Silva", "Ana") < ("Silva", "Bruno")`).

5. Tupla: sequência imutável
--------------------------------
    ponto = (3, 4)
    unitaria = (7,)        # a VÍRGULA é o que faz isso ser uma tupla, não os parênteses!
    vazia = ()

Um erro sutil e comum: `(7)` sozinho NÃO é uma tupla — é apenas o número 7
entre parênteses (os parênteses aqui só agrupam, como em uma expressão
matemática). É a vírgula depois do 7 que sinaliza "isto é uma tupla de um
elemento só".

Por que escolher tupla em vez de lista?
- é imutável, portanto segura para passar adiante sem risco de outra parte
  do código alterá-la sem você saber;
- por ser imutável (e, por consequência, "hashável"), pode ser usada como
  CHAVE de dicionário (Dia 9) — listas não podem;
- expressa a intenção de "registro de tamanho fixo" (uma coordenada, um
  RGB, uma linha vinda de banco de dados) de forma mais clara que uma lista,
  que sugere "coleção que pode crescer ou encolher";
- é levemente mais leve e rápida de criar que uma lista equivalente.

Desempacotamento de tupla funciona igual ao que já vimos:

    x, y = ponto
    primeiro, *meio, ultimo = [1, 2, 3, 4]    # funciona também com listas

6. Pilha e fila: a mesma lista, dois usos diferentes
------------------------------------------------------------
Uma PILHA (LIFO — last in, first out, como uma pilha de pratos) é eficiente
de implementar com uma lista comum, usando sempre as operações do FINAL:

    pilha = []
    pilha.append(1); pilha.append(2)
    pilha.pop()          # remove e devolve 2 (o último que entrou)

Uma FILA (FIFO — first in, first out, como uma fila de banco) é LENTA se
implementada com lista comum, porque `pop(0)` (remover do início) precisa
deslocar todos os elementos restantes uma posição para trás — um custo que
cresce com o tamanho da lista. Para filas de verdade, a biblioteca padrão
oferece `collections.deque`, otimizada para inserir e remover dos dois
lados em tempo constante (aprofundamos isso no Dia 29).

7. Custo das operações mais comuns (prévia do Dia 29)
--------------------------------------------------------------
Entender o custo aproximado de cada operação evita escrever código que
"funciona no teste com 10 itens" mas fica lento com 100 mil:

    acesso por índice (lista[i])     O(1)  — tempo constante, não importa o tamanho
    append (lista.append(x))         O(1) amortizado — quase sempre instantâneo
    insert(0, x) / pop(0)             O(n) — precisa deslocar todo o resto da lista
    x in lista                        O(n) — no pior caso, percorre a lista inteira
    sort() / sorted()                 O(n log n) — o custo do melhor algoritmo de ordenação por comparação

Essa notação "O(...)" (Big O) descreve como o tempo de execução cresce
conforme o tamanho `n` da entrada aumenta — não é ainda o momento de
dominar essa notação, apenas de perceber que operações "no início" da lista
(`insert(0, ...)`, `pop(0)`) são mais custosas do que operações "no fim".
""",
    exemplos=[
        Exemplo(
            titulo="Ordenação por múltiplos critérios",
            codigo='''pessoas = [
    {"nome": "Ana", "idade": 30},
    {"nome": "Bruno", "idade": 25},
    {"nome": "Carla", "idade": 30},
]
por_idade_e_nome = sorted(pessoas, key=lambda p: (-p["idade"], p["nome"]))
for p in por_idade_e_nome:
    print(p["idade"], p["nome"])
''',
            explicacao="Tupla como chave: idade decrescente (o sinal de "
                       "menos inverte) e, entre empates de idade, nome "
                       "crescente.",
        ),
        Exemplo(
            titulo="Alias, cópia rasa e a armadilha da matriz",
            codigo='''original = [1, 2, 3]
alias = original
copia = original[:]
alias.append(4)
print(original)   # [1, 2, 3, 4]  -- alias e original sao o MESMO objeto
print(copia)      # [1, 2, 3]     -- copia e independente

errado = [[0] * 3] * 3
errado[0][0] = 1
print(errado)      # [[1, 0, 0], [1, 0, 0], [1, 0, 0]] -- as 3 linhas mudaram!

certo = [[0] * 3 for _ in range(3)]
certo[0][0] = 1
print(certo)       # [[1, 0, 0], [0, 0, 0], [0, 0, 0]] -- so a linha 0 mudou
''',
            explicacao="alias compartilha o mesmo objeto que original; a "
                       "fatia [:] cria um objeto novo; e a compreensão de "
                       "lista evita a armadilha de linhas compartilhadas.",
        ),
        Exemplo(
            titulo="Pilha com lista: verificando parênteses balanceados",
            codigo='''def parenteses_balanceados(texto):
    pilha = []
    pares = {")": "(", "]": "[", "}": "{"}
    for caractere in texto:
        if caractere in "([{":
            pilha.append(caractere)
        elif caractere in ")]}":
            if not pilha or pilha.pop() != pares[caractere]:
                return False
    return not pilha    # deve terminar vazia

print(parenteses_balanceados("(a[b]{c})"))   # True
print(parenteses_balanceados("(a[b)"))       # False
''',
            explicacao="Uso clássico de pilha (LIFO): cada abertura empilha, "
                       "cada fechamento deve corresponder ao último aberto.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d08e1",
            enunciado="Escreva media(numeros) devolvendo a média aritmética como float (0.0 se a lista for vazia).",
            funcao="media",
            assinatura="def media(numeros):",
            testes=[
                ("media([1, 2, 3, 4])", "2.5"),
                ("media([])", "0.0"),
                ("media([10])", "10.0"),
            ],
            dica="Trate a lista vazia antes de dividir (cláusula de guarda).",
        ),
        Exercicio(
            id="d08e2",
            enunciado=(
                "Escreva segundo_maior(numeros) devolvendo o segundo MAIOR valor distinto.\n"
                "Se não existir, devolva None."
            ),
            funcao="segundo_maior",
            assinatura="def segundo_maior(numeros):",
            testes=[
                ("segundo_maior([3, 1, 4, 4, 5])", "4"),
                ("segundo_maior([7, 7, 7])", "None"),
                ("segundo_maior([2, 9])", "2"),
                ("segundo_maior([])", "None"),
            ],
            nivel="medio",
            dica="Elimine duplicatas com set(), ordene e pegue o penúltimo.",
        ),
        Exercicio(
            id="d08e3",
            enunciado="Escreva achatar(matriz) que transforma uma lista de listas em uma lista única.",
            funcao="achatar",
            assinatura="def achatar(matriz):",
            testes=[
                ("achatar([[1, 2], [3], [4, 5]])", "[1, 2, 3, 4, 5]"),
                ("achatar([])", "[]"),
                ("achatar([[], [1]])", "[1]"),
            ],
            nivel="medio",
            dica="Laço externo pelas linhas + .extend() ou laço interno com append.",
        ),
    ],
    quiz=[
        Quiz("O que lista.append(4) devolve?",
             ["A lista modificada", "None", "O valor 4", "Uma cópia"], 1,
             "Métodos que mudam a lista no lugar devolvem None; nunca reatribua 'lista = lista.append(x)'."),
        Quiz("Por que [[0]*3]*3 é perigoso ao tentar criar uma matriz?",
             ["É lento", "Cria 3 referências para a mesma lista interna, então mudar uma 'linha' muda todas",
              "Não compila", "Cria strings em vez de números"], 1,
             "A multiplicação de lista replica a REFERÊNCIA ao objeto interno, não o conteúdo independente."),
        Quiz("Qual a diferença essencial entre sorted(lista) e lista.sort()?",
             ["Não há diferença", "sorted() devolve uma nova lista e não altera a original; sort() altera a própria lista e devolve None",
              "sort() é mais rápido sempre", "sorted() só funciona com números"], 1,
             "sorted() funciona com qualquer iterável e preserva o original; sort() existe só em listas e as modifica no lugar."),
        Quiz("Por que uma tupla pode ser usada como chave de dicionário, mas uma lista não?",
             ["Tuplas são menores em memória", "Tuplas são imutáveis (hasháveis); listas são mutáveis e não têm hash estável",
              "É apenas uma limitação arbitrária sem motivo técnico", "Listas nunca podem conter números"], 1,
             "Chaves de dicionário precisam de um hash que nunca muda; um objeto mutável como lista não garante isso."),
    ],
    projeto=(
        "Crie lista_compras.py com menu (adicionar, remover, listar ordenado, total, sair) "
        "usando uma lista de tuplas (produto, quantidade, preço). Ordene a listagem por preço "
        "total do item (quantidade * preço) usando sorted com key."
    ),
    leitura=["docs.python.org/pt-br/3/tutorial/datastructures.html", "docs.python.org/pt-br/3/library/collections.html#collections.deque"],
))
