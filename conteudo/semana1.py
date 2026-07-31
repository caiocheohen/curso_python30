"""Semana 1 - Dias 1 a 8: fundamentos da linguagem."""

from nucleo.modelos import Dia, Exemplo, Exercicio, Quiz

DIAS = []

# ---------------------------------------------------------------- DIA 1
# ---------------------------------------------------------------- DIA 1
DIAS.append(Dia(
    numero=1,
    titulo="Ambiente, interpretador e o primeiro programa",
    nivel="Iniciante",
    duracao="90 min",
    objetivos=[
        "Entender o que é Python e por que ele foi criado, antes de escrever qualquer código",
        "Compreender o que um interpretador faz, passo a passo, quando executa seu programa",
        "Usar o terminal do Linux para verificar a instalação e rodar Python de duas formas diferentes",
        "Diferenciar o REPL (modo interativo) do script (arquivo .py) e saber quando usar cada um",
        "Escrever, salvar e executar o seu primeiro programa em Python",
        "Usar a função print() com todas as suas opções de formatação",
        "Entender a diferença entre comentários e docstrings, e quando cada um é apropriado",
        "Ler um traceback (mensagem de erro) sem entrar em pânico, localizando o problema rapidamente",
        "Conhecer as regras básicas de estilo (PEP 8) que todos os programadores Python seguem",
    ],
    teoria="""
Antes de escrever qualquer código, vale entender o que é Python e por que
ele existe. Python foi criado por Guido van Rossum no final dos anos 1980,
com um objetivo muito claro: ser uma linguagem que qualquer pessoa
conseguisse ler e entender, mesmo sem ser programadora. O nome veio do
grupo de humor britânico Monty Python, não da cobra — o criador queria que
a linguagem fosse divertida.

Hoje, Python é uma das linguagens mais usadas no mundo. Você a encontra em
análise de dados, inteligência artificial, automação de tarefas, criação de
sites, scripts de sistema operacional e muito mais. Uma das razões desse
sucesso é que o código Python se parece quase com texto em inglês — o que
torna o aprendizado muito mais suave do que em outras linguagens.

---------------------------------------------------------------------------
1. O que é uma linguagem de programação?
---------------------------------------------------------------------------
Um computador entende apenas instruções binárias: sequências de zeros e uns
que dizem ao processador o que fazer. Escrever programas diretamente nesse
formato seria impossível para um humano na prática.

Uma linguagem de programação é um "idioma intermediário": você escreve
instruções em algo que se parece com linguagem humana, e um programa
especial traduz isso para as instruções binárias que o computador entende.

Python é uma linguagem de ALTO NÍVEL: ela fica muito longe do hardware e
muito perto da forma como humanos pensam. Por isso seu código é mais curto,
mais legível, e mais fácil de escrever e manter do que em linguagens de
baixo nível como C ou Assembly.

---------------------------------------------------------------------------
2. Compilada versus interpretada: qual a diferença?
---------------------------------------------------------------------------
Existem dois grandes modelos de como uma linguagem transforma seu código em
instruções para o computador:

COMPILADA (ex: C, C++, Rust):
    Você escreve o código -> roda um COMPILADOR -> ele gera um arquivo
    executável (.exe no Windows, sem extensão no Linux) -> você roda
    esse arquivo.
    A tradução acontece UMA VEZ, antes de rodar. O resultado é muito
    rápido, mas você precisa recompilar a cada mudança.

INTERPRETADA (ex: Python, JavaScript, Ruby):
    Você escreve o código -> roda o INTERPRETADOR -> ele lê e executa
    o código linha por linha, na hora.
    Não existe uma etapa separada de compilação. É mais lento que
    compilado, mas muito mais prático para desenvolvimento.

Python se encaixa na categoria interpretada. Mas há um detalhe
interessante: por baixo dos panos, o Python SIM compila seu código —
só que faz isso automaticamente e de forma invisível, gerando um formato
chamado bytecode (veja a pasta __pycache__ que aparece no seu projeto
depois de rodar um arquivo). Você nunca precisa se preocupar com isso,
mas é bom saber que existe.

---------------------------------------------------------------------------
3. O interpretador CPython e o que acontece quando você roda python3
---------------------------------------------------------------------------
Quando você digita python3 arquivo.py no terminal, um programa chamado
CPython entra em ação. CPython é a implementação OFICIAL e mais usada do
Python — praticamente todo mundo que diz "estou usando Python" está, na
verdade, usando CPython.

O que o CPython faz com seu arquivo, em três etapas:

    ETAPA 1: LEITURA E ANÁLISE (Parsing)
    O CPython lê o seu arquivo .py como texto puro, igual a abrir no
    bloco de notas. Ele então analisa esse texto, verificando se a
    estrutura faz sentido (parênteses fechados? palavras-chave certas?).
    Resultado: uma árvore sintática interna que representa a estrutura
    do seu programa.

    ETAPA 2: COMPILAÇÃO PARA BYTECODE
    Essa árvore é transformada em bytecode: um conjunto de instruções
    simples para uma "máquina virtual" Python. Bytecode é mais rápido
    de executar do que reler o texto original toda vez. Fica salvo
    em arquivos .pyc na pasta __pycache__.

    ETAPA 3: EXECUÇÃO
    A Python Virtual Machine (PVM) lê e executa o bytecode, instrução
    por instrução, do início ao fim do seu programa.

Tudo isso acontece em frações de segundo, de forma completamente
automática. Você só precisa saber que existe para entender mensagens de
erro mais avançadas mais tarde.

---------------------------------------------------------------------------
4. Python no Linux: verificando a instalação
---------------------------------------------------------------------------
Praticamente toda distribuição Linux (Ubuntu, Debian, Fedora, Arch...) já
vem com Python 3 instalado por padrão — o próprio sistema operacional usa
Python para vários scripts internos.

Abra o terminal e experimente estes comandos:

    python3 --version
    Python 3.12.3

Esse comando mostra a versão instalada. Se aparecer Python 3.X.X com
qualquer número, está tudo certo para este curso.

    which python3
    /usr/bin/python3

Esse comando mostra ONDE está o programa python3 no seu computador. É o
caminho que o sistema usa quando você digita python3.

ATENÇÃO: Em alguns sistemas, o comando python (sem o 3) existe e aponta
para o Python 2, que foi oficialmente descontinuado em 2020 e não deve
ser usado para novos projetos. Sempre use python3 para garantir que está
usando a versão correta.

---------------------------------------------------------------------------
5. O REPL: seu laboratório interativo
---------------------------------------------------------------------------
REPL é uma sigla em inglês que significa:

    R - Read   (Ler o que você digitou)
    E - Eval   (Avaliar/Executar o que foi digitado)
    P - Print  (Mostrar o resultado)
    L - Loop   (Voltar ao início e esperar mais uma entrada)

Para abrir o REPL, simplesmente digita:

    python3

Você verá algo parecido com:

    Python 3.12.3 (main, ...)
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

Os três sinais de maior (>>>) indicam que o Python está esperando você
digitar algo. Experimente:

    >>> 2 + 3
    5
    >>> "Ola" + " " + "Python"
    'Ola Python'
    >>> nome = "Maria"
    >>> nome
    'Maria'
    >>> print("Meu primeiro resultado:", 2 + 2)
    Meu primeiro resultado: 4

UMA DIFERENÇA IMPORTANTE: no REPL, quando você digita uma expressão (como
2 + 3 ou nome), o resultado aparece automaticamente na tela. Isso NÃO
acontece dentro de um arquivo .py — em scripts, você precisa chamar
print() explicitamente para ver qualquer coisa na tela.

Para sair do REPL, use qualquer um destes:
    exit()   ou   quit()   ou   Ctrl+D

QUANDO USAR O REPL? Para testar ideias rápidas, explorar funções que você
não conhece, e verificar o resultado de uma expressão sem precisar criar
um arquivo inteiro. Ao longo do curso, sempre que tiver dúvida sobre como
algo funciona, abra o REPL e teste — é o hábito mais valioso de um
programador Python.

---------------------------------------------------------------------------
6. Script: criando e executando um arquivo .py
---------------------------------------------------------------------------
Um script é simplesmente um arquivo de texto com a extensão .py que
contém código Python. Ele é lido e executado do início ao fim, de cima
para baixo, linha por linha.

Para criar e rodar um script:

    1. Abra seu editor de texto (VS Code, nano, vim, gedit...)
    2. Crie um arquivo chamado ola.py
    3. Escreva o código
    4. Salve o arquivo
    5. No terminal: python3 ola.py

Exemplo de script simples:

    # Este é meu primeiro programa em Python
    print("Olá, mundo!")
    print("Estou aprendendo Python!")

Ao executar com python3 ola.py, você verá:
    Olá, mundo!
    Estou aprendendo Python!

TORNANDO UM SCRIPT EXECUTÁVEL (opcional, mas profissional):
Você pode adicionar uma linha especial chamada "shebang" no topo do
arquivo, que diz ao sistema operacional qual programa usar para rodar o
arquivo:

    #!/usr/bin/env python3
    print("Olá, mundo!")

Depois salve o arquivo e rode no terminal:

    chmod +x ola.py    # marca o arquivo como executável
    ./ola.py           # agora pode rodar sem escrever python3

O que é /usr/bin/env python3? É uma forma inteligente de dizer "use o
python3 que estiver disponível no PATH do sistema", em vez de apontar
para um caminho fixo como /usr/bin/python3 (o que causaria problemas
ao usar ambientes virtuais, assunto do Dia 13).

---------------------------------------------------------------------------
7. A função print(): sua janela para o mundo
---------------------------------------------------------------------------
print() é uma FUNÇÃO EMBUTIDA do Python — isso significa que ela já existe
e está disponível sem precisar instalar nada. Ela envia texto para a
saída padrão, ou seja, exibe algo na tela do terminal.

O que é uma função? Por enquanto, pense nela como um "comando" que realiza
uma tarefa. Você a chama pelo nome e passa informações entre parênteses.
Veremos funções em profundidade no Dia 11.

print() aceita qualquer número de valores separados por vírgula:

    print("Olá")                   # Olá
    print("Olá", "Python")         # Olá Python
    print(1, 2, 3, 4, 5)           # 1 2 3 4 5
    print("Resultado:", 10 + 5)    # Resultado: 15

Observe que print() converte tudo para texto automaticamente — por isso
print(10 + 5) funciona mesmo sendo uma conta matemática.

DOIS PARÂMETROS ESPECIAIS que modificam o comportamento:

O parâmetro sep (separador):
    Por padrão, print separa os valores com um espaço. Você pode mudar:

    print("a", "b", "c")            # a b c  (separador padrão: espaço)
    print("a", "b", "c", sep="-")   # a-b-c
    print("a", "b", "c", sep="")    # abc    (sem separador)
    print("a", "b", "c", sep=", ")  # a, b, c

O parâmetro end (fim da linha):
    Por padrão, print termina com uma quebra de linha (\n), pulando para a
    próxima linha. Você pode mudar:

    print("Linha 1")
    print("Linha 2")
    # Resultado:
    # Linha 1
    # Linha 2

    print("Sem quebra", end="")
    print(" -- continua aqui")
    # Resultado:
    # Sem quebra -- continua aqui

    print("A", end=" | ")
    print("B", end=" | ")
    print("C")
    # Resultado: A | B | C

UM DETALHE IMPORTANTE: print() SEMPRE devolve None. Isso significa que
guardar o resultado de print() numa variável não serve para nada:

    resultado = print("oi")   # isso imprime "oi"
    print(resultado)           # isso imprime None
    # print existe para MOSTRAR coisas, não para DEVOLVER valores úteis

---------------------------------------------------------------------------
8. Comentários e Docstrings: documentando seu código
---------------------------------------------------------------------------
COMENTÁRIOS:
Tudo que vem depois de # numa linha é ignorado completamente pelo
interpretador. O símbolo # "comenta" o resto da linha.

    nome = "Ana"        # isto é executado normalmente
    # isto aqui é um comentário e é ignorado
    # print("isso também não vai aparecer")

Para que servem? Para EXPLICAR o código para outras pessoas (e para você
mesmo, no futuro). Um código sem comentários pode ser impossível de
entender depois de alguns meses.

REGRA DE OURO: um bom comentário explica o PORQUÊ de uma decisão, não o
QUÊ está acontecendo — o código já diz o quê.

    # Ruim: repete o que o código já mostra
    total = preco * 1.12   # multiplica o preço por 1.12

    # Bom: explica o raciocínio
    total = preco * 1.12   # adiciona 12% de IVA, alíquota de 2024

DOCSTRINGS:
Docstring (abreviação de "documentation string") é completamente diferente
de um comentário. É uma string — texto entre aspas — colocada logo no
início de um módulo, função ou classe. Diferente do comentário, ela FAZ
PARTE do programa e pode ser acessada enquanto o programa está rodando.

    def calcular_area(base, altura):
        \"\"\"Calcula a área de um retângulo.

        Recebe a base e a altura em centímetros
        e devolve a área em centímetros quadrados.
        \"\"\"
        return base * altura

    help(calcular_area)        # mostra a docstring formatada
    calcular_area.__doc__      # acessa o texto diretamente

Por que isso importa? Ferramentas de documentação automática leem
docstrings para gerar manuais. A função help() que você usará no REPL
também as exibe. É a forma profissional de documentar código Python.

---------------------------------------------------------------------------
9. Lendo erros: o traceback não é seu inimigo
---------------------------------------------------------------------------
Todo programador, iniciante ou experiente, recebe erros o tempo todo.
Aprender a LEITURA de um traceback (o relatório de erro do Python) é
uma das habilidades mais importantes do curso.

Quando algo dá errado, o Python exibe algo assim:

    Traceback (most recent call last):
      File "programa.py", line 5, in <module>
        resultado = 10 / zero
                    ~~~^~~~~~
    ZeroDivisionError: division by zero

Como ler: SEMPRE comece PELA ÚLTIMA LINHA, que é o resumo do problema:
    ZeroDivisionError   -> o TIPO do erro (o que deu errado)
    division by zero    -> a MENSAGEM (detalhes sobre o problema)

As linhas acima mostram o CAMINHO que o programa percorreu até chegar
ao erro — útil em programas maiores para descobrir qual função chamou
qual outra. Nas linhas "File ..." há o nome do arquivo e o número da linha.

ERROS QUE VOCÊ VAI ENCONTRAR NA PRIMEIRA SEMANA:

    SyntaxError: invalid syntax
    -> O código tem um problema de escrita: faltou fechar um parêntese,
       faltou dois-pontos, aspas não fechadas, etc.
    -> SOLUÇÃO: olhe a linha indicada e compare com a sintaxe correta.

    IndentationError: unexpected indent
    -> A indentação (recuo com espaços) está errada.
    -> SOLUÇÃO: certifique-se de usar sempre 4 espaços. Nunca misture
       espaços com tabs.

    NameError: name 'x' is not defined
    -> Você usou uma variável ou função que não existe (ou digitou errado).
    -> SOLUÇÃO: verifique o nome — Python diferencia maiúsculas de
       minúsculas (idade é diferente de Idade).

    TypeError: unsupported operand type(s)
    -> Você tentou uma operação entre tipos incompatíveis.
    -> EXEMPLO: "texto" + 3 (não dá para somar texto com número diretamente).

    ModuleNotFoundError: No module named 'algo'
    -> Você tentou importar uma biblioteca que não está instalada.
    -> SOLUÇÃO: pip install nome-da-biblioteca

DICA VALIOSA: quando não entender um erro, copie exatamente a última linha
(o tipo + a mensagem) e pesquise no Google ou pergunte para uma IA. É
exatamente isso que programadores profissionais fazem o dia inteiro.

---------------------------------------------------------------------------
10. Estilo de código: PEP 8 desde o primeiro dia
---------------------------------------------------------------------------
PEP 8 é o guia oficial de estilo do Python. PEP significa "Python
Enhancement Proposal" (Proposta de Melhoria do Python) — são documentos
onde a comunidade define como a linguagem deve evoluir. A PEP 8 define
como o código Python deve ser ESCRITO para ser legível e consistente.

Por que seguir desde o início? Hábitos formados no começo são difíceis de
mudar. Código que segue o estilo padrão é mais fácil de ler para qualquer
outra pessoa (e para você mesmo depois de algumas semanas).

AS REGRAS MAIS IMPORTANTES:

Indentação: sempre 4 espaços, nunca tabs
    # Correto
    if verdadeiro:
        print("sim")   # 4 espaços

Nomes de variáveis: minúsculas com underline (snake_case)
    # Correto
    nome_completo = "João Silva"
    preco_com_desconto = 49.90

    # Errado (estilos de outras linguagens)
    nomeCompleto = "João Silva"     # camelCase, comum em Java/JavaScript
    NomeCompleto = "João Silva"     # PascalCase, para classes no Python

Linhas não muito longas: no máximo 79-100 caracteres
    # Quebre linhas longas para melhor leitura

Uma instrução por linha:
    # Correto
    a = 1
    b = 2

    # Evite (dificulta leitura e debug)
    a = 1; b = 2

Espaços ao redor de operadores:
    # Correto
    resultado = 10 + 5
    nome = "Ana"

    # Evite
    resultado=10+5
    nome="Ana"

Editores como VS Code (com a extensão Python) e o formatador automático
`black` aplicam boa parte dessas regras automaticamente. Recomendamos
configurar isso no VS Code antes de começar a escrever código — procure
nas extensões por "Python" e instale a extensão oficial da Microsoft.
""",
    exemplos=[
        Exemplo(
            titulo="Seu primeiro script completo",
            codigo='''#!/usr/bin/env python3
"""Programa de apresentação — Dia 1 do curso de Python."""

# Exibindo texto simples
print("Olá, mundo!")

# print com múltiplos valores (separados por espaço por padrão)
print("Python", "é", "incrível")

# Mudando o separador
print("2024", "07", "28", sep="/")    # 2024/07/28

# Imprimindo na mesma linha com end
print("Carregando", end="")
print(".", end="")
print(".", end="")
print(".", end=" ")
print("pronto!")
''',
            explicacao="Salve este código num arquivo ola.py e execute com "
                       "'python3 ola.py'. Cada print() gera uma saída no terminal. "
                       "Note que o shebang (#!/usr/bin/env python3) na primeira linha "
                       "permite executar o arquivo diretamente com ./ola.py depois de "
                       "usar chmod +x ola.py — mas python3 ola.py sempre funciona.",
        ),
        Exemplo(
            titulo="Explorando o REPL: help() e dir()",
            codigo='''# Cole estas linhas uma por uma no REPL (python3) para ver os resultados

# Operações matemáticas básicas
>>> 2 + 3
5
>>> 10 / 3
3.3333333333333335
>>> 10 // 3
3

# Texto
>>> len("Python")
6
>>> "Python".upper()
'PYTHON'

# Descobrindo o que uma função faz
>>> help(print)

# Descobrindo o que um objeto sabe fazer
>>> dir("qualquer texto")
''',
            explicacao="No REPL, o resultado de qualquer expressão aparece "
                       "automaticamente — você não precisa de print(). "
                       "help(objeto) mostra a documentação. "
                       "dir(objeto) lista tudo que aquele tipo de dado sabe fazer. "
                       "Esses dois comandos são seus melhores amigos ao explorar Python.",
        ),
        Exemplo(
            titulo="Comentários, docstrings e como erros aparecem",
            codigo='''#!/usr/bin/env python3
"""
Demonstração de comentários e docstrings.
Este texto acima é uma docstring de módulo.
"""

# Comentários explicam o PORQUÊ, não o QUÊ

# Calculando desconto para clientes com mais de 1 ano de cadastro
preco_original = 100.0
preco_final = preco_original * 0.85   # 15% de desconto para clientes fiéis

print("Preço original:", preco_original)
print("Preço com desconto:", preco_final)


def apresentar(nome):
    """Cumprimenta o usuário pelo nome.

    Esta é uma docstring de função.
    Acesse com: help(apresentar)
    """
    print("Olá,", nome, "— bem-vindo ao Python!")


apresentar("estudante")
''',
            explicacao="A docstring do módulo fica logo no topo, antes de qualquer código. "
                       "A docstring da função fica logo na primeira linha do corpo da função. "
                       "Tente no REPL: import este arquivo e use help() na função "
                       "para ver a docstring formatada. "
                       "O comentário explica POR QUE o desconto é 15%, não COMO "
                       "a multiplicação funciona — isso o código já mostra.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d01e1",
            enunciado=(
                "Crie uma variável chamada 'mensagem' contendo exatamente o texto:\n"
                "Ola, Python!\n\n"
                "Atenção: o texto deve ter exatamente essa escrita — com vírgula\n"
                "depois de 'Ola' e ponto de exclamação no final, sem acento.\n"
                "Use aspas simples ou duplas: ambas funcionam em Python."
            ),
            funcao="mensagem",
            assinatura='mensagem = ...',
            testes=[("mensagem", "'Ola, Python!'")],
            dica="Use aspas: mensagem = 'Ola, Python!'  ou  mensagem = \"Ola, Python!\"",
        ),
        Exercicio(
            id="d01e2",
            enunciado=(
                "Já existem duas variáveis prontas: nome = 'Ana' e idade = 30.\n"
                "Crie a variável 'cartao' juntando essas informações no formato:\n"
                "Ana tem 30 anos\n\n"
                "Dica: para juntar texto com número, você precisa converter o\n"
                "número para texto usando str(). A operação + entre strings as\n"
                "une (concatena). Então: 'Ana' + ' tem ' + str(30) + ' anos'\n"
                "produz 'Ana tem 30 anos'."
            ),
            funcao="cartao",
            assinatura='nome = "Ana"\nidade = 30\ncartao = ...',
            testes=[("cartao", "'Ana tem 30 anos'")],
            dica="str(idade) converte o número 30 para o texto '30'. Depois junte com +.",
        ),
        Exercicio(
            id="d01e3",
            enunciado=(
                "Calcule a área de um retângulo usando as variáveis já definidas:\n"
                "base = 7.5 e altura = 4\n\n"
                "Guarde o resultado na variável 'area'.\n"
                "Em Python, multiplicação usa o operador *\n"
                "Então: 7.5 * 4 = 30.0\n\n"
                "Nota: o resultado será 30.0 (com o .0) porque base é um número\n"
                "decimal (float) — Python mantém essa informação no resultado."
            ),
            funcao="area",
            assinatura="base = 7.5\naltura = 4\narea = ...",
            testes=[("area", "30.0")],
            dica="Use o operador * para multiplicar: area = base * altura",
        ),
    ],
    quiz=[
        Quiz(
            "Qual comando no terminal mostra qual versão do Python está instalada?",
            ["python3 --version", "python3 version", "print(version)", "py --check"],
            0,
            "A flag --version (ou a forma curta -V) é o padrão em ferramentas de linha "
            "de comando. Experimente no terminal agora mesmo.",
        ),
        Quiz(
            "No REPL do Python, o que acontece quando você digita '2 + 3' e pressiona Enter?",
            [
                "Nada acontece — você precisa usar print(2 + 3)",
                "O resultado 5 aparece automaticamente na tela",
                "O Python salva o resultado numa variável automática",
                "Aparece uma mensagem de erro",
            ],
            1,
            "No REPL (modo interativo), expressões são avaliadas e o resultado aparece "
            "automaticamente. Em um arquivo .py, você PRECISA de print() para ver algo.",
        ),
        Quiz(
            "Qual a diferença entre um comentário (#) e uma docstring (\"\"\"texto\"\"\")?",
            [
                "Não há diferença — ambos são ignorados pelo Python",
                "Comentários são mais rápidos de escrever",
                "Docstrings fazem parte do programa e podem ser acessadas em tempo de execução com help(); comentários são completamente ignorados",
                "Docstrings só funcionam dentro de funções",
            ],
            2,
            "help(minha_funcao) exibe a docstring em tempo de execução. "
            "Comentários são 100% ignorados pelo interpretador — não existem para o programa em si.",
        ),
        Quiz(
            "Ao ler um traceback (mensagem de erro), por onde você deve começar?",
            [
                "Pela primeira linha, que diz 'Traceback (most recent call last)'",
                "Pelo meio, onde está o nome do arquivo",
                "Pela ÚLTIMA linha, que mostra o tipo do erro e a mensagem",
                "Não importa — o traceback deve ser ignorado e o código reescrito",
            ],
            2,
            "A última linha resume tudo: o tipo do erro (ex: NameError) e o motivo "
            "(ex: name 'x' is not defined). Comece ali e só suba para as outras "
            "linhas se precisar descobrir ONDE no código o erro ocorreu.",
        ),
    ],
    projeto=(
        "Crie o arquivo perfil.py com o seguinte desafio:\n\n"
        "1. Adicione uma docstring de módulo explicando o que o arquivo faz\n"
        "2. Crie variáveis com suas informações: nome, cidade, objetivo com Python\n"
        "3. Use print() para exibir um 'cartão de apresentação' formatado, como:\n\n"
        "   ================================\n"
        "   Nome:     João Silva\n"
        "   Cidade:   São Paulo\n"
        "   Objetivo: Automatizar tarefas\n"
        "   ================================\n\n"
        "4. Adicione comentários explicando cada seção do seu código\n"
        "5. Execute com python3 perfil.py e veja o resultado\n\n"
        "BÔNUS: use sep e end no print() para criar separadores sem precisar\n"
        "digitar linhas inteiras de = manualmente."
    ),
    leitura=[
        "docs.python.org/pt-br/3/tutorial/introduction.html — tutorial oficial em português",
        "PEP 8 (peps.python.org/pep-0008) — guia de estilo oficial",
        "PEP 20 — O Zen do Python: abra o REPL e digite 'import this'",
    ],
))
# ---------------------------------------------------------------- DIA 2
DIAS.append(Dia(
    numero=2,
    titulo="Variáveis, tipos primitivos e entrada de dados",
    nivel="Iniciante",
    duracao="90 min",
    objetivos=[
        "Entender o que é uma variável e como Python a trata diferente de outras linguagens",
        "Conhecer os cinco tipos primitivos: int, float, str, bool e None",
        "Compreender tipagem dinâmica e tipagem forte — dois conceitos que andam juntos mas são diferentes",
        "Converter valores entre tipos com int(), float(), str() e bool(), sabendo quando cada um falha",
        "Usar a função type() para descobrir o tipo de qualquer valor",
        "Ler dados digitados pelo usuário com input() e entender por que sempre vira texto",
        "Reconhecer a armadilha clássica do ponto flutuante e saber como lidar com ela",
        "Escrever nomes de variáveis que seguem as convenções do Python",
    ],
    teoria="""
No Dia 1 você escreveu seu primeiro programa e aprendeu a exibir
informações com print(). Mas programas reais precisam GUARDAR informações
para trabalhar com elas: o nome do usuário, o resultado de um cálculo, uma
lista de produtos. É para isso que existem as variáveis.

---------------------------------------------------------------------------
1. O que é uma variável?
---------------------------------------------------------------------------
Uma variável é um NOME que você dá a um valor guardado na memória do
computador. Pense como uma etiqueta: você cola a etiqueta num objeto para
poder encontrá-lo depois pelo nome.

Em Python, criar uma variável é simples:

    nome = "Carlos"
    idade = 28
    altura = 1.75

Isso cria três variáveis. Depois de criadas, você pode usá-las em
qualquer lugar do programa referenciando o nome:

    print(nome)           # Carlos
    print(idade + 2)      # 30
    print(altura * 100)   # 175.0

COMO O PYTHON GUARDA VARIÁVEIS NA MEMÓRIA:
Python não guarda o valor DENTRO da variável, como uma caixinha. Em vez
disso, ele cria o objeto em algum lugar da memória e a variável é uma
REFERÊNCIA — um ponteiro — para esse objeto. Pense numa etiqueta presa
com um barbante num produto na prateleira.

Por isso, quando você faz:

    a = 10
    b = a        # b aponta para o MESMO objeto 10, não para uma cópia

...ambas as variáveis apontam para o mesmo objeto. Com números e textos
isso não causa problemas, porque eles são IMUTÁVEIS (não mudam no lugar).
Com listas e dicionários (Dias 8 e 9), esse detalhe vai causar surpresas
se você não souber.

A função id() revela o número de identificação do objeto na memória:

    a = 10
    b = a
    print(id(a))          # exemplo: 140234567891
    print(id(b))          # mesmo número — mesmo objeto!
    print(id(a) == id(b)) # True

NOMES VÁLIDOS PARA VARIÁVEIS:
Existem regras que você deve seguir ao nomear variáveis:

    PODEM conter: letras, números e underscore (_)
    NÃO PODEM: começar com número, ter espaço, ter símbolos como -, @, !
    Python diferencia MAIÚSCULAS de minúsculas:
        nome, Nome e NOME são três variáveis diferentes!

    # Correto
    nome_completo = "Ana"
    idade_em_anos = 25
    _valor_interno = 100
    resultado2 = 42

    # Errado — causam SyntaxError
    2resultado = 42        # não pode começar com número
    nome completo = "Ana"  # não pode ter espaço
    meu-nome = "Carlos"    # hífen não é permitido

CONVENÇÃO: use sempre minúsculas com underscore para variáveis (snake_case)
    preco_total = 29.90     # correto (Python)
    precoTotal = 29.90      # evite (estilo de Java/JavaScript)

---------------------------------------------------------------------------
2. Os cinco tipos primitivos fundamentais
---------------------------------------------------------------------------
Python tem cinco tipos primitivos — os "blocos de construção" mais básicos:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━




TIPO 1: int — números inteiros


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━



Números sem parte decimal. Positivos, negativos ou zero.

    quantidade = 42
    temperatura_minima = -5
    populacao_brasil = 215_000_000   # underscore facilita leitura de números grandes
    resultado = 2 ** 100             # inteiro gigante — Python não tem limite!

DIFERENCIAL DO PYTHON: diferente de C e Java, onde um int tem tamanho
fixo (geralmente 32 bits, limite de ~2 bilhões), o int do Python cresce
automaticamente conforme necessário. Nunca ocorre overflow.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━




TIPO 2: float — números com parte decimal


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━




Números com ponto decimal (use ponto, não vírgula!).

    preco = 29.90
    altura = 1.75
    temperatura = -3.5
    muito_pequeno = 1.5e-10   # notação científica: 0.00000000015

IMPORTANTE: Em Python, use ponto decimal (.), não vírgula. A vírgula tem
outro significado na linguagem (separa elementos de tuplas e listas).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━




TIPO 3: str — texto (strings)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━




Qualquer sequência de caracteres entre aspas. Pode usar aspas simples ou
duplas — o resultado é exatamente o mesmo.

    nome = "Maria"
    cidade = 'São Paulo'
    mensagem = "Ela disse: 'olá'"   # aspas simples dentro de duplas
    frase = 'Ele respondeu: "ok"'   # aspas duplas dentro de simples

Para textos com várias linhas, use três aspas:

    poema = \"\"\"
    Linha um
    Linha dois
    Linha três
    \"\"\"

Strings vazias também são válidas:

    sem_texto = ""
    tambem_vazio = ''

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━




TIPO 4: bool — valores lógicos (verdadeiro ou falso)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━




Só existem dois valores possíveis: True e False (com letra maiúscula!).

    esta_logado = True
    tem_desconto = False
    maior_de_idade = True

CURIOSIDADE: bool é um subtipo de int em Python. Por baixo dos panos,
True vale 1 e False vale 0. Isso significa que você pode fazer contas:

    True + True     # 2
    True + False    # 1
    True * 10       # 10

Isso raramente é útil no dia a dia, mas explica por que Python permite
essa operação sem erro.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━




TIPO 5: None — ausência de valor


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━




None representa "nenhum valor" ou "valor desconhecido". É diferente de
zero, de string vazia ou de False — é simplesmente a ausência de qualquer
valor.

    resultado_pendente = None
    endereco = None    # ainda não foi preenchido

None é muito usado para representar dados opcionais que ainda não foram
definidos, e como valor de retorno de funções que não devolvem nada útil
(como print() que vimos no Dia 1).

---------------------------------------------------------------------------
3. Descobrindo o tipo de uma variável com type()
---------------------------------------------------------------------------
Você pode perguntar ao Python qual o tipo de qualquer valor usando type():

    print(type(42))           # <class 'int'>
    print(type(3.14))         # <class 'float'>
    print(type("oi"))         # <class 'str'>
    print(type(True))         # <class 'bool'>
    print(type(None))         # <class 'NoneType'>

O type() é especialmente útil quando você não tem certeza do tipo de um
valor recebido — por exemplo, de uma função ou do usuário.

Outra forma é isinstance(), que verifica se um valor É de determinado tipo:

    isinstance(42, int)       # True
    isinstance("oi", str)     # True
    isinstance(42, float)     # False
    isinstance(True, int)     # True (bool é subtipo de int!)

Prefira isinstance() para verificações no código real, pois ele funciona
melhor com herança (assunto avançado do Dia 18).

---------------------------------------------------------------------------
4. Tipagem dinâmica e tipagem forte: conceitos diferentes!
---------------------------------------------------------------------------
Python tem dois comportamentos importantes relacionados a tipos, e muita
gente os confunde:

TIPAGEM DINÂMICA significa que uma variável pode mudar de tipo ao longo
do programa — você não precisa declarar o tipo com antecedência:

    x = 10          # x é int
    x = "dez"       # agora x é str — Python não reclama
    x = 3.14        # agora x é float — ainda sem problema

Compare com Java (tipagem estática), onde você escreveria:
    int x = 10;
    x = "dez";   // ERRO! x foi declarado como int e não pode mudar

TIPAGEM FORTE significa que Python NÃO converte tipos automaticamente
quando você tenta misturá-los em operações:

    "3" + 4        # TypeError: não pode somar str com int
    "3" * 4        # FUNCIONA: repete a string 4 vezes -> '3333'
    1 + True       # FUNCIONA: bool é subtipo de int (True = 1)

Compare com JavaScript (tipagem fraca), onde:
    "3" + 4  →  "34"   (JavaScript converte silenciosamente!)
    "3" - 1  →  2      (JavaScript faz mágica de conversão)

Python NUNCA faz essas conversões silenciosas. Se os tipos são
incompatíveis para a operação, você recebe um TypeError claro. Isso
parece chato no começo, mas protege você de bugs sutis e difíceis de
encontrar.

RESUMO:
    Dinâmica = variáveis podem mudar de tipo (flexibilidade de NOMES)
    Forte    = valores não se misturam sem conversão explícita (segurança de OPERAÇÕES)

---------------------------------------------------------------------------
5. Convertendo entre tipos
---------------------------------------------------------------------------
Quando você precisa converter um valor de um tipo para outro, Python
oferece funções específicas para isso:

CONVERTENDO PARA int:

    int("42")       # 42       — texto de número inteiro vira int
    int("42.5")     # ERRO!    — int() não aceita ponto decimal no texto
    int(42.9)       # 42       — TRUNCA (não arredonda!) removendo o decimal
    int(-42.9)      # -42      — trunca em direção ao zero, não para baixo
    int(True)       # 1
    int(False)      # 0

IMPORTANTE: int() com ponto decimal TRUNCA, não arredonda.
    int(9.9) é 9, não 10!
    Use round() para arredondar: round(9.9) é 10.

CONVERTENDO PARA float:

    float("3.14")   # 3.14     — texto de número decimal vira float
    float("3")      # 3.0      — inteiro no texto vira float
    float(5)        # 5.0      — int vira float
    float("abc")    # ERRO!    — texto não numérico causa ValueError

CONVERTENDO PARA str:

    str(42)         # '42'
    str(3.14)       # '3.14'
    str(True)       # 'True'
    str(None)       # 'None'
    str([1, 2, 3])  # '[1, 2, 3]' — até listas viram texto!

CONVERTENDO PARA bool:

Valores que viram False (chamados de "falsy"):
    bool(0)     # False
    bool(0.0)   # False
    bool("")    # False   <- string vazia
    bool(None)  # False

TUDO O MAIS vira True (chamados de "truthy"), incluindo:
    bool(1)         # True
    bool(-1)        # True (qualquer número não-zero)
    bool("0")       # True <- ATENÇÃO! "0" é texto não-vazio!
    bool("False")   # True <- ATENÇÃO! "False" é texto não-vazio!

A armadilha clássica: bool("False") é True! Porque "False" é uma string
com 5 caracteres, e qualquer string não-vazia é verdadeira. Se você quer
verificar se um texto representa um valor verdadeiro, faça:

    texto = "false"
    é_verdadeiro = texto.lower() == "true"   # False

---------------------------------------------------------------------------
6. A armadilha do ponto flutuante
---------------------------------------------------------------------------
Tente isso no REPL:

    >>> 0.1 + 0.2
    0.30000000000000004
    >>> 0.1 + 0.2 == 0.3
    False

Isso parece um bug, mas NÃO É! É uma limitação do padrão IEEE-754 — a
forma como todos os computadores modernos representam números decimais
em binário. O número 0.1 não tem representação exata em binário (assim
como 1/3 não tem representação exata em decimal), então o computador
guarda uma aproximação muito próxima, mas não perfeita.

Esse comportamento existe em TODAS as linguagens (C, Java, JavaScript,
Rust, Go...) que usam ponto flutuante padrão. Não é culpa do Python.

COMO LIDAR:

Para comparações, use math.isclose() em vez de ==:

    import math
    math.isclose(0.1 + 0.2, 0.3)    # True — correto!

Para dinheiro e situações que exigem precisão exata, use Decimal:

    from decimal import Decimal
    Decimal("0.1") + Decimal("0.2")          # Decimal('0.3') — exato!
    Decimal("0.1") + Decimal("0.2") == Decimal("0.3")   # True

IMPORTANTE: crie o Decimal a partir de uma STRING, não de um float:
    Decimal(0.1)    # ERRADO — herda a imprecisão do float antes de criar
    Decimal("0.1")  # CORRETO — parte do texto exato

---------------------------------------------------------------------------
7. input(): lendo dados do usuário
---------------------------------------------------------------------------
A função input() exibe uma mensagem (o "prompt") e espera o usuário
digitar algo e pressionar Enter. Ela SEMPRE devolve uma string.

    nome = input("Qual o seu nome? ")
    print("Olá,", nome)

REGRA ABSOLUTA: input() SEMPRE retorna str, não importa o que o usuário
digitou. Mesmo se o usuário digitar 42, você recebe a string "42", não
o número 42.

    numero = input("Digite um número: ")
    print(type(numero))    # <class 'str'> — sempre!

Por isso, se você precisa do valor como número, converta imediatamente:

    idade = int(input("Sua idade: "))       # converte para int
    altura = float(input("Sua altura: "))   # converte para float

MAS ATENÇÃO: se o usuário digitar texto onde se espera número, o programa
quebra com ValueError:

    idade = int(input("Sua idade: "))
    # Usuário digitou "vinte e cinco"
    # ValueError: invalid literal for int() with base 10: 'vinte e cinco'

Tratar esse tipo de erro é o assunto do Dia 15 (exceções). Por agora,
saiba que esse risco existe sempre que você usa input() com conversão.

---------------------------------------------------------------------------
8. Constantes: variáveis que não deveriam mudar
---------------------------------------------------------------------------
Python não tem uma palavra-chave para constantes (como const em
JavaScript). A convenção é usar MAIÚSCULAS_COM_UNDERSCORE para sinalizar
que aquele valor não deveria ser alterado:

    PI = 3.14159265358979
    TAXA_DESCONTO = 0.15
    LIMITE_TENTATIVAS = 3
    NOME_APP = "Meu Sistema"

Isso é apenas uma CONVENÇÃO — Python não impede a reatribuição. É um
combinado entre programadores: "se está em maiúsculas, não mexa".

---------------------------------------------------------------------------
9. Múltiplas atribuições em uma linha
---------------------------------------------------------------------------
Python permite atribuir várias variáveis de uma vez de formas elegantes:

Mesmo valor para várias variáveis:
    a = b = c = 0       # a, b e c valem 0

Valores diferentes na mesma linha:
    nome, idade = "Ana", 30
    x, y, z = 1, 2, 3

Isso é especialmente útil para TROCAR valores entre variáveis — sem
precisar de uma variável temporária auxiliar:

    a = 10
    b = 20

    # Forma clássica (outras linguagens):
    temp = a    # salva a em temp
    a = b       # a recebe o valor de b
    b = temp    # b recebe o valor original de a

    # Forma Python (muito mais elegante):
    a, b = b, a     # troca em uma linha!

Por trás dos panos, Python avalia o lado direito COMPLETAMENTE antes de
fazer qualquer atribuição, por isso a troca funciona sem variável auxiliar.
""",
    exemplos=[
        Exemplo(
            titulo="Explorando os cinco tipos primitivos",
            codigo='''# Os cinco tipos fundamentais do Python
inteiro = 42
decimal = 3.14
texto = "Python"
logico = True
ausente = None

# Verificando os tipos
print("Valor:", inteiro, "| Tipo:", type(inteiro).__name__)
print("Valor:", decimal, "| Tipo:", type(decimal).__name__)
print("Valor:", texto,   "| Tipo:", type(texto).__name__)
print("Valor:", logico,  "| Tipo:", type(logico).__name__)
print("Valor:", ausente, "| Tipo:", type(ausente).__name__)

# int do Python não tem limite!
numero_gigante = 2 ** 100
print("\n2 elevado a 100 =", numero_gigante)
print("Tipo:", type(numero_gigante).__name__)

# bool é subtipo de int
print("\nTrue + True =", True + True)    # 2
print("True * 10 =", True * 10)          # 10
print("isinstance(True, int):", isinstance(True, int))   # True
''',
            explicacao="type(x).__name__ extrai só o nome do tipo, sem o "
                       "ruído de <class '...'>. Repare que 2**100 funciona "
                       "sem erro — não há limite de tamanho para int em Python. "
                       "E True + True = 2 porque bool é um subtipo de int.",
        ),
        Exemplo(
            titulo="Conversões e a armadilha do ponto flutuante",
            codigo='''import math
from decimal import Decimal

# Conversões entre tipos
print("int('42')  =", int("42"))       # 42
print("int(9.9)   =", int(9.9))        # 9  <- TRUNCA, não arredonda!
print("round(9.9) =", round(9.9))      # 10 <- este arredonda
print("float('3') =", float("3"))      # 3.0
print("str(100)   =", str(100))        # '100'

# A armadilha do ponto flutuante
print("\n--- Ponto flutuante ---")
print("0.1 + 0.2 =", 0.1 + 0.2)              # 0.30000000000000004
print("0.1 + 0.2 == 0.3:", 0.1 + 0.2 == 0.3) # False!

# Solução 1: math.isclose para comparações
print("math.isclose:", math.isclose(0.1 + 0.2, 0.3))  # True

# Solução 2: Decimal para precisão exata (ex: dinheiro)
preco_a = Decimal("19.90")
preco_b = Decimal("5.10")
total = preco_a + preco_b
print("\nDecimal:", preco_a, "+", preco_b, "=", total)  # 25.00 exato
''',
            explicacao="int() trunca (não arredonda) — int(9.9) é 9, não 10. "
                       "Para arredondar, use round(). "
                       "O resultado 0.30000000000000004 não é bug: "
                       "é como computadores representam 0.1+0.2 em binário. "
                       "math.isclose() e Decimal são as soluções certas para cada situação.",
        ),
        Exemplo(
            titulo="input() e múltiplas atribuições",
            codigo='''# Múltiplas atribuições elegantes
nome, cidade = "Carlos", "Recife"
x, y, z = 10, 20, 30
print(nome, "mora em", cidade)
print("x =", x, "| y =", y, "| z =", z)

# Troca de valores sem variável auxiliar
a, b = 5, 8
print("\nAntes: a =", a, "b =", b)
a, b = b, a
print("Depois: a =", a, "b =", b)

# input() sempre retorna str
# (descomente para testar interativamente)
# nome_usuario = input("Seu nome: ")
# print(type(nome_usuario))    # sempre <class 'str'>
# idade = int(input("Sua idade: "))
# print("Daqui a 10 anos você terá", idade + 10)
''',
            explicacao="A troca a, b = b, a funciona porque Python avalia "
                       "o lado direito (b, a) COMPLETAMENTE antes de fazer "
                       "qualquer atribuição — então b ainda vale 8 quando "
                       "a recebe esse valor. O comentário com input() "
                       "está comentado pois o corretor não aceita entrada interativa.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d02e1",
            enunciado=(
                "Existe uma variável texto_numero = '42' — é uma STRING, não um número.\n"
                "Sua tarefa:\n"
                "1. Crie a variável 'numero' convertendo texto_numero para inteiro\n"
                "2. Crie a variável 'dobro' com o dobro desse número\n\n"
                "Use int() para converter texto para inteiro.\n"
                "O corretor vai verificar que 'numero' é int (não string) e\n"
                "que 'dobro' vale 84."
            ),
            funcao="numero",
            assinatura='texto_numero = "42"\nnumero = ...\ndobro = ...',
            testes=[("numero", "42"), ("dobro", "84"), ("type(numero) is int", "True")],
            dica="numero = int(texto_numero) converte '42' para 42. Depois dobro = numero * 2.",
        ),
        Exercicio(
            id="d02e2",
            enunciado=(
                "Existe uma variável celsius = 37.5 com uma temperatura em Celsius.\n"
                "Calcule o equivalente em Fahrenheit e guarde em 'fahrenheit'.\n\n"
                "A fórmula de conversão é:\n"
                "   Fahrenheit = Celsius × 9 ÷ 5 + 32\n\n"
                "Em Python: fahrenheit = celsius * 9 / 5 + 32\n\n"
                "Dica: verifique a ordem das operações — multiplicação e divisão\n"
                "acontecem antes da soma. Para celsius = 37.5, o resultado\n"
                "deve ser exatamente 99.5."
            ),
            funcao="fahrenheit",
            assinatura="celsius = 37.5\nfahrenheit = ...",
            testes=[("fahrenheit", "99.5")],
            dica="fahrenheit = celsius * 9 / 5 + 32",
        ),
        Exercicio(
            id="d02e3",
            enunciado=(
                "Existe a = 10 e b = 3.\n"
                "Troque os valores entre elas SEM usar uma terceira variável.\n\n"
                "Após a troca:\n"
                "   a deve valer 3\n"
                "   b deve valer 10\n\n"
                "Use o recurso de atribuição múltipla do Python:\n"
                "   a, b = b, a\n\n"
                "Isso funciona porque Python avalia o lado direito (b, a)\n"
                "completamente antes de fazer qualquer atribuição."
            ),
            funcao="a",
            assinatura="a = 10\nb = 3\n# troque aqui",
            testes=[("a", "3"), ("b", "10")],
            dica="Uma única linha resolve: a, b = b, a",
        ),
    ],
    quiz=[
        Quiz(
            "Qual será o resultado de int(7.9) em Python?",
            ["8 (arredonda para o inteiro mais próximo)",
             "7 (trunca removendo a parte decimal)",
             "7.9 (permanece float)",
             "Erro — int() não aceita float"],
            1,
            "int() TRUNCA em direção ao zero, não arredonda. int(7.9) é 7 e int(-7.9) é -7. "
            "Para arredondar, use round(): round(7.9) é 8.",
        ),
        Quiz(
            "O que input() SEMPRE retorna, independente do que o usuário digitou?",
            ["int — se o usuário digitou um número",
             "str — sempre uma string, sem exceção",
             "O tipo do que foi digitado (automático)",
             "None — se o usuário não digitou nada"],
            1,
            "input() SEMPRE retorna str. Mesmo digitando 42, você recebe '42'. "
            "Se precisar de número, converta: int(input('...')) ou float(input('...'))",
        ),
        Quiz(
            "Por que 0.1 + 0.2 == 0.3 é False em Python?",
            ["É um bug específico do Python que será corrigido",
             "Porque 0.1, 0.2 e 0.3 não têm representação exata em binário (padrão IEEE-754)",
             "Porque Python usa vírgula, não ponto, para decimais",
             "Porque é necessário importar o módulo math primeiro"],
            1,
            "Todas as linguagens com ponto flutuante (C, Java, JavaScript, Python...) "
            "têm esse comportamento. Use math.isclose() para comparações ou "
            "Decimal para precisão exata em cálculos monetários.",
        ),
        Quiz(
            "O que bool('False') retorna em Python?",
            ["False — porque 'False' representa um valor falso",
             "True — porque 'False' é uma string não-vazia, e strings não-vazias são verdadeiras",
             "Erro — não é possível converter texto para bool",
             "None"],
            1,
            "bool() avalia se o valor é 'vazio/zero' (False) ou não (True). "
            "A string 'False' tem 5 caracteres, não está vazia, então vira True. "
            "Strings que viram False: apenas a string vazia ''.",
        ),
    ],
    projeto=(
        "Crie o arquivo conversor.py que faça:\n\n"
        "1. Crie variáveis fixas (sem input por enquanto) com:\n"
        "   - Um valor em reais (ex: preco = 150.75)\n"
        "   - A cotação do dólar (ex: cotacao = 5.20)\n\n"
        "2. Calcule e exiba:\n"
        "   - O valor em dólares (preco / cotacao)\n"
        "   - O tipo de cada variável com type()\n"
        "   - O mesmo cálculo usando Decimal para comparar a precisão\n\n"
        "3. Experimente conversões que causam erro (em comentários):\n"
        "   # int('3.14')  — por que falha?\n"
        "   # int('abc')   — por que falha?\n\n"
        "BÔNUS: adicione uma versão que usa input() para ler os valores\n"
        "do usuário e converta corretamente para float antes de calcular."
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/stdtypes.html — documentação oficial dos tipos",
        "docs.python.org/pt-br/3/library/decimal.html — módulo Decimal para precisão exata",
        "docs.python.org/pt-br/3/tutorial/introduction.html#numbers — números em Python",
    ],
))
# ---------------------------------------------------------------- DIA 3
DIAS.append(Dia(
    numero=3,
    titulo="Operadores: aritméticos, comparação, lógicos e precedência",
    nivel="Iniciante",
    duracao="90 min",
    objetivos=[
        "Dominar os sete operadores aritméticos, especialmente // e % que são novidade para muitos",
        "Entender por que // arredonda para baixo (piso) e não para zero, mesmo com negativos",
        "Usar % (resto) para resolver problemas de ciclos, paridade e decomposição de números",
        "Escrever comparações encadeadas do jeito idiomático do Python",
        "Diferenciar == (compara valor) de is (compara identidade) e saber quando usar cada um",
        "Entender o que and, or e not realmente devolvem — não são apenas True ou False",
        "Reconhecer valores falsy e truthy e escrever condições mais limpas com eles",
        "Consultar a tabela de precedência sem precisar decorá-la",
    ],
    teoria="""
Nos Dias 1 e 2 você aprendeu a guardar valores em variáveis. Agora vamos
aprender a TRABALHAR com esses valores: fazer contas, comparar números e
combinar condições lógicas. Esses são os operadores — os verbos da
linguagem de programação.

---------------------------------------------------------------------------
1. Operadores aritméticos
---------------------------------------------------------------------------
Python tem sete operadores para cálculos matemáticos:

    Operador  Nome                 Exemplo       Resultado
    --------  -------------------  ----------    ---------
    +         Adição               10 + 3        13
    -         Subtração            10 - 3        7
    *         Multiplicação        10 * 3        30
    /         Divisão real         10 / 3        3.333...
    //        Divisão inteira      10 // 3       3
    %         Resto da divisão     10 % 3        1
    **        Potência             10 ** 3       1000

Os quatro primeiros (+, -, *, /) funcionam como você já conhece da
matemática. Os três últimos merecem atenção especial.

DIVISÃO REAL ( / ) SEMPRE DEVOLVE FLOAT:

    10 / 2      # 5.0  — não 5!
    9 / 3       # 3.0  — não 3!

Mesmo que o resultado seja um número redondo, / sempre devolve float.
Isso é diferente de muitas linguagens onde / entre inteiros dá inteiro.

DIVISÃO INTEIRA ( // ) — PISO, NÃO TRUNCAMENTO:

    10 // 3     # 3    (3 x 3 = 9, sobra 1)
     7 // 2     # 3    (3 x 2 = 6, sobra 1)

A grande armadilha vem com números NEGATIVOS. Em C e Java, a divisão
inteira trunca EM DIREÇÃO AO ZERO:

    -7 / 2  →  -3   (em C/Java — aproxima de zero)

Em Python, // usa a regra do PISO: sempre arredonda para o inteiro
mais próximo ABAIXO, mesmo que isso signifique se afastar do zero:

    -7 // 2     # -4  (piso de -3.5 é -4, não -3!)
     7 // -2    # -4  (idem)

Por que o piso e não o truncamento? Porque isso garante que % sempre
tenha o mesmo sinal do divisor, o que é matematicamente mais consistente
e útil para problemas de ciclos (relógio, dias da semana).

RESTO DA DIVISÃO ( % ) — O OPERADOR QUE RESOLVE MUITA COISA:

    10 % 3      # 1   (10 = 3 x 3 + 1, sobra 1)
    15 % 5      # 0   (divisão exata, sem resto)
     7 % 2      # 1   (7 é ímpar)
     8 % 2      # 0   (8 é par)

Usos clássicos de %:
    - Verificar paridade: numero % 2 == 0  significa "é par"
    - Criar ciclos: hora % 24, posicao % tamanho_da_lista
    - Decompor números em partes (centena, dezena, unidade)

POTÊNCIA ( ** ):

    2 ** 10     # 1024
    9 ** 0.5    # 3.0   (qualquer número ** 0.5 é sua raiz quadrada!)
    2 ** -1     # 0.5   (expoente negativo = fração: 1/2)

---------------------------------------------------------------------------
2. O par // e %: decompondo valores em partes
---------------------------------------------------------------------------
Juntos, // e % formam uma dupla poderosa. A relação matemática que os une:

    valor == (valor // divisor) * divisor + (valor % divisor)

Ou seja: quociente inteiro vezes divisor, mais o resto, sempre recria o
valor original. Isso é exatamente o que você fazia na divisão "com resto"
no ensino fundamental.

Exemplo prático: decompor 3725 segundos em horas, minutos e segundos:

    total = 3725

    horas   = total // 3600      # 1   (3725 ÷ 3600 = 1, com resto)
    resto   = total % 3600       # 125 (segundos que sobraram)
    minutos = resto // 60        # 2
    segundos = resto % 60        # 5

    # Verificação: 1x3600 + 2x60 + 5 = 3600 + 120 + 5 = 3725 ✓

O Python tem uma função que calcula os dois de uma vez: divmod()

    divmod(10, 3)         # (3, 1)   — devolve (quociente, resto)
    divmod(3725, 3600)    # (1, 125)

---------------------------------------------------------------------------
3. Atribuição composta: atalhos para operar e reatribuir
---------------------------------------------------------------------------
Uma operação muito comum é pegar uma variável, operar sobre ela e guardar
o resultado de volta na mesma variável. Python tem atalhos para isso:

    Forma composta    Equivalente a
    --------------    -------------
    x += 5            x = x + 5
    x -= 3            x = x - 3
    x *= 2            x = x * 2
    x /= 4            x = x / 4
    x //= 3           x = x // 3
    x %= 7            x = x % 7
    x **= 2           x = x ** 2

Exemplos práticos:

    vida = 100
    vida -= 20      # recebeu dano: vida agora é 80
    vida += 5       # curou um pouco: vida agora é 85

    preco = 50.0
    preco *= 1.10   # aumento de 10%: preco agora é 55.0

    nivel = 1
    nivel += 1      # subiu de nível: nivel agora é 2

---------------------------------------------------------------------------
4. Operadores de comparação: verificando relações
---------------------------------------------------------------------------
Comparações sempre devolvem True ou False:

    Operador  Significado        Exemplo       Resultado
    --------  -----------------  ----------    ---------
    ==        Igual a            5 == 5        True
    !=        Diferente de       5 != 3        True
    >         Maior que          5 > 3         True
    <         Menor que          3 < 5         True
    >=        Maior ou igual     5 >= 5        True
    <=        Menor ou igual     3 <= 5        True

COMPARAÇÕES ENCADEADAS (recurso exclusivo do Python!):
Em outras linguagens, verificar se um número está numa faixa exige duas
comparações ligadas por and:

    // Java/C:
    if (nota >= 0 && nota <= 10) { ... }

Em Python, você pode escrever como na matemática:

    if 0 <= nota <= 10:       # muito mais legível!
        print("nota válida")

    if 0 < x < 100:           # x está entre 1 e 99 (exclusivo)
        print("no intervalo")

O encadeamento funciona com qualquer quantidade de comparações e é
avaliado da esquerda para a direita, sem repetir o valor do meio.

---------------------------------------------------------------------------
5. == versus is: valor contra identidade
---------------------------------------------------------------------------
Esta é uma das distinções mais importantes do Python:

    == pergunta: "os dois valores são IGUAIS?"
    is pergunta: "são literalmente o MESMO objeto na memória?"

    a = [1, 2, 3]
    b = [1, 2, 3]   # lista com mesmo conteúdo, mas objeto diferente
    c = a           # c aponta para o MESMO objeto que a

    a == b    # True  — mesmo conteúdo
    a is b    # False — objetos diferentes na memória
    a == c    # True  — mesmo conteúdo
    a is c    # True  — literalmente o mesmo objeto

REGRA PRÁTICA: use is apenas com None, True e False.

    if valor is None:      # correto e idiomático
    if valor == None:      # funciona, mas evite — is None é a convenção

Por que só None, True e False? Porque Python garante que existe UM ÚNICO
objeto None no programa inteiro. Então "is None" é sempre seguro e exato.

Com outros valores, is pode dar resultados surpreendentes:

    x = 1000
    y = 1000
    x is y      # pode ser False! (dois objetos distintos)

    x = 5
    y = 5
    x is y      # pode ser True! (Python reutiliza objetos pequenos)

Isso é um detalhe interno de implementação — nunca dependa de is para
comparar números ou textos comuns.

---------------------------------------------------------------------------
6. Operadores lógicos: and, or, not
---------------------------------------------------------------------------
Os operadores lógicos combinam condições:

    not  inverte o valor lógico
    and  verdadeiro apenas se AMBOS forem verdadeiros
    or   verdadeiro se PELO MENOS UM for verdadeiro

    Tabela verdade:
    A        B        A and B    A or B    not A
    -------  -------  ---------  --------  -----
    True     True     True       True      False
    True     False    False      True      False
    False    True     False      True      True
    False    False    False      False     True

AVALIAÇÃO EM CURTO-CIRCUITO:
Python para de avaliar assim que o resultado já é conhecido:

    Com and: se o primeiro for False, o segundo NEM É AVALIADO
    Com or:  se o primeiro for True,  o segundo NEM É AVALIADO

Isso é muito útil para proteger operações perigosas:

    # Se divisor for 0, "total / divisor" nunca é avaliado — seguro!
    if divisor != 0 and total / divisor > 2:
        print("resultado alto")

    # A ordem das condições importa: coloque a "proteção" primeiro

O QUE AND E OR REALMENTE DEVOLVEM:
Aqui vem a parte que surpreende muita gente: and e or não devolvem
necessariamente True ou False — eles devolvem um dos OPERANDOS originais!

    "" or "padrão"      # 'padrão'  — primeiro era falsy, devolveu o segundo
    "ana" or "bia"      # 'ana'     — primeiro era truthy, devolveu ele mesmo
    "ana" and "bia"     # 'bia'     — primeiro era truthy, devolveu o segundo
    0 and "algo"        # 0         — primeiro era falsy, devolveu ele mesmo

A regra:
    or  devolve o PRIMEIRO valor truthy, ou o ÚLTIMO se nenhum for truthy
    and devolve o PRIMEIRO valor falsy, ou o ÚLTIMO se todos forem truthy

Isso viabiliza um padrão muito usado:

    nome = entrada or "visitante"   # usa "visitante" se entrada estiver vazia

Mas atenção à armadilha: se 0 for um valor legítimo, esse padrão
substitui o zero pelo padrão incorretamente:

    desconto = digitado or 10    # PROBLEMA: desconto legítimo de 0 vira 10!

---------------------------------------------------------------------------
7. Valores falsy e truthy
---------------------------------------------------------------------------
Em contexto lógico (dentro de if, while, and, or, not), Python avalia
qualquer valor como verdadeiro ou falso:

Valores FALSY (considerados False):
    False, None, 0, 0.0, "", [], (), {}, set()
    — resumo: qualquer coisa "vazia" ou "zero"

Valores TRUTHY (todo o resto, incluindo surpresas):
    "0"    — string com um caractere, não está vazia!
    [0]    — lista com um elemento, não está vazia!
    -1     — número não-zero
    " "    — string com espaço, não está vazia!

Por isso o código Python prefere usar a própria coleção como condição:

    if lista:            # se lista não estiver vazia (idiomático)
    if not lista:        # se lista estiver vazia (idiomático)

    # Em vez de:
    if len(lista) > 0:   # funciona, mas é redundante em Python

---------------------------------------------------------------------------
8. Precedência: qual operação acontece primeiro?
---------------------------------------------------------------------------
Quando você escreve 2 + 3 * 4, Python calcula 3*4 primeiro (12) e depois
soma 2, resultando em 14 — não 20. Isso é precedência.

Tabela da mais alta para a mais baixa:

    Prioridade  Operadores
    ----------  ---------------------------------------------------
    1 (maior)   ()                 parênteses
    2           **                 potência
    3           +x, -x             sinal unário
    4           *, /, //, %        multiplicação e divisões
    5           +, -               adição e subtração
    6           ==, !=, <, >, <=,
                >=, in, is         comparações
    7           not                negação lógica
    8           and                E lógico
    9 (menor)   or                 OU lógico

Exemplos:

    2 + 3 * 4         # 14   (multiplicação antes da adição)
    (2 + 3) * 4       # 20   (parênteses primeiro)
    2 ** 3 ** 2       # 512  (potência associa à direita: 2**(3**2) = 2**9)
    not True or False # False (not antes de or: (not True) or False)

DICA DE OURO: quando tiver dúvida sobre precedência, use parênteses.
Eles não custam nada e tornam o código muito mais claro para quem lê.

    resultado = (a + b) * (c - d)   # intenção óbvia, sem ambiguidade
""",
    exemplos=[
        Exemplo(
            titulo="// e % na prática: decompondo valores",
            codigo='''# Decompondo 3725 segundos em horas, minutos e segundos
total = 3725

horas    = total // 3600
resto    = total % 3600
minutos  = resto // 60
segundos = resto % 60

print(f"{total} segundos = {horas}h {minutos}min {segundos}s")
# 3725 segundos = 1h 2min 5s

# divmod() calcula quociente e resto de uma vez
quociente, sobra = divmod(total, 3600)
print(f"divmod(3725, 3600) = ({quociente}, {sobra})")

# % para verificar paridade
for n in [10, 7, 4, 13]:
    tipo = "par" if n % 2 == 0 else "impar"
    print(f"{n} e {tipo}")
''',
            explicacao="// dá o quociente inteiro e % dá o resto. "
                       "Juntos, eles decompõem qualquer valor em partes. "
                       "divmod(a, b) calcula os dois de uma vez. "
                       "n % 2 == 0 é a forma canônica de verificar paridade: "
                       "se o resto da divisão por 2 é zero, o número é par.",
        ),
        Exemplo(
            titulo="Comparações encadeadas e curto-circuito",
            codigo='''# Comparações encadeadas (exclusividade do Python)
nota = 7.5
print(0 <= nota <= 10)          # True

idade = 25
print(18 <= idade < 65)         # True

# Curto-circuito: a segunda parte nao e avaliada se o resultado ja e certo
divisor = 0
resultado = divisor != 0 and 100 / divisor > 10   # seguro!
print("Com divisor zero:", resultado)   # False, sem erro de divisao

# O que and e or REALMENTE devolvem
print("'' or 'padrao':", "" or "padrao")    # padrao
print("'ana' or 'bia':", "ana" or "bia")    # ana
print("'ana' and 'bia':", "ana" and "bia")  # bia
print("0 or 42:", 0 or 42)                  # 42

# Padrao com valor padrao
nome_digitado = ""
nome = nome_digitado or "visitante"
print("Nome:", nome)    # visitante
''',
            explicacao="Comparações encadeadas leem como matemática normal. "
                       "O curto-circuito evita avaliar o lado direito quando "
                       "o resultado já está determinado — essencial para "
                       "evitar erros como divisão por zero. "
                       "and e or devolvem um dos operandos, não necessariamente bool.",
        ),
        Exemplo(
            titulo="Falsy, truthy e precedência na prática",
            codigo='''# Precedencia: multiplicacao antes de adicao
print(2 + 3 * 4)        # 14, nao 20
print((2 + 3) * 4)      # 20 com parenteses

# Potencia associa a direita
print(2 ** 3 ** 2)      # 512 = 2**(3**2) = 2**9
print((2 ** 3) ** 2)    # 64  = 8**2

# Falsy e truthy na pratica
valores = [0, 1, "", "texto", [], [0], None, False, True]
for v in valores:
    rotulo = "truthy" if v else "falsy"
    print(f"{repr(v):12} -> {rotulo}")
''',
            explicacao="Os parênteses deixam explícita a intenção de quem "
                       "escreveu o código — use sempre que a precedência "
                       "não for óbvia de relance. "
                       "O loop mostra na prática quais valores Python "
                       "considera falsos: zeros, vazios e None.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d03e1",
            enunciado=(
                "Dado numero = 157, extraia os dígitos usando apenas // e %:\n"
                "   centena = 1  (o dígito das centenas)\n"
                "   dezena  = 5  (o dígito das dezenas)\n"
                "   unidade = 7  (o dígito das unidades)\n\n"
                "Dicas:\n"
                "   157 // 100 = 1   quantas centenas cabem em 157?\n"
                "   157 % 100 = 57   o que sobrou depois de tirar a centena?\n"
                "   57 // 10 = 5     dezena do que sobrou\n"
                "   157 % 10 = 7     último dígito: resto da divisão por 10"
            ),
            funcao="centena",
            assinatura="numero = 157\ncentena = ...\ndezena = ...\nunidade = ...",
            testes=[("centena", "1"), ("dezena", "5"), ("unidade", "7")],
            dica="centena = numero // 100  |  dezena = numero // 10 % 10  |  unidade = numero % 10",
        ),
        Exercicio(
            id="d03e2",
            enunciado=(
                "Dado ano = 2024, calcule 'bissexto' (True ou False).\n\n"
                "A regra completa para ano bissexto:\n"
                "   Um ano e bissexto SE:\n"
                "   (divisivel por 4 E nao divisivel por 100)\n"
                "   OU\n"
                "   (divisivel por 400)\n\n"
                "Exemplos:\n"
                "   2024: divisivel por 4 e nao por 100 -> bissexto\n"
                "   1900: divisivel por 100 mas nao por 400 -> nao bissexto\n"
                "   2000: divisivel por 400 -> bissexto\n\n"
                "Use ano % 4 == 0 para testar 'divisivel por 4'.\n"
                "Use and, or e parenteses para combinar as condicoes."
            ),
            funcao="bissexto",
            assinatura="ano = 2024\nbissexto = ...",
            testes=[("bissexto", "True"), ("type(bissexto) is bool", "True")],
            dica="bissexto = (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0)",
        ),
        Exercicio(
            id="d03e3",
            enunciado=(
                "Dado total = 3725 (segundos), calcule:\n"
                "   horas    = 1  (horas completas)\n"
                "   minutos  = 2  (minutos completos do que sobrou)\n"
                "   segundos = 5  (segundos finais)\n\n"
                "Estrategia:\n"
                "   1. horas = total // 3600\n"
                "   2. resto = total % 3600\n"
                "   3. minutos = resto // 60\n"
                "   4. segundos = resto % 60\n\n"
                "Verificacao: 1x3600 + 2x60 + 5 = 3600 + 120 + 5 = 3725"
            ),
            funcao="horas",
            assinatura="total = 3725\nhoras = ...\nminutos = ...\nsegundos = ...",
            testes=[("horas", "1"), ("minutos", "2"), ("segundos", "5")],
            dica="Calcule horas = total // 3600, depois resto = total % 3600, e decomponha o resto em minutos e segundos.",
        ),
    ],
    quiz=[
        Quiz(
            "Quanto vale -7 // 2 em Python?",
            ["-3 (trunca em direcao ao zero)",
             "-4 (arredonda para baixo, regra do piso)",
             "-3.5 (divisao real)",
             "3 (ignora o sinal)"],
            1,
            "// em Python usa a regra do PISO (floor division): sempre arredonda para o "
            "inteiro abaixo, nao em direcao ao zero. "
            "-7 / 2 = -3.5, e o piso de -3.5 e -4. "
            "Em C ou Java, -7 / 2 truncaria para -3.",
        ),
        Quiz(
            "O que a expressao '\"ana\" or \"bia\"' devolve em Python?",
            ["True",
             "False",
             "'ana' — o primeiro valor truthy encontrado",
             "'bia' — o ultimo valor da expressao"],
            2,
            "or nao devolve necessariamente True ou False: ele devolve o PRIMEIRO "
            "valor truthy que encontrar. Como 'ana' e truthy (string nao vazia), "
            "a avaliacao para ali e devolve 'ana' sem nem olhar para 'bia'.",
        ),
        Quiz(
            "Por que usar 'valor is None' em vez de 'valor == None'?",
            ["is e mais rapido de executar",
             "== None causa erro quando o valor e None",
             "is e a convencao porque None e sempre o unico objeto desse tipo no programa",
             "Nao ha diferenca pratica entre os dois"],
            2,
            "Existe apenas UM objeto None em todo o programa Python. "
            "Usar 'is None' expressa exatamente isso: e o objeto None? "
            "E a forma idiomatica recomendada pelo PEP 8.",
        ),
        Quiz(
            "O que 9 ** 0.5 calcula?",
            ["9 elevado a 5 (resultado: 59049)",
             "A raiz quadrada de 9 (resultado: 3.0)",
             "9 dividido por 0.5 (resultado: 18.0)",
             "Um erro — expoentes devem ser inteiros"],
            1,
            "x ** 0.5 e exatamente a raiz quadrada de x. "
            "9 ** 0.5 = 3.0, pois 3 x 3 = 9. "
            "Funciona com qualquer numero: 16**0.5 = 4.0, 2**0.5 ≈ 1.414.",
        ),
    ],
    projeto=(
        "Crie o arquivo calculadora_tempo.py que faça:\n\n"
        "1. Crie variaveis com duracoes em segundos de tres atividades:\n"
        "   ex: aula = 5400, treino = 3600, estudo = 7200\n\n"
        "2. Calcule o total e decomponha em horas, minutos e segundos\n\n"
        "3. Exiba um relatorio formatado:\n"
        "   Aula:   1h 30min 0s\n"
        "   Treino: 1h 0min 0s\n"
        "   Estudo: 2h 0min 0s\n"
        "   Total:  4h 30min 0s\n\n"
        "4. Verifique se o total de horas e par ou impar usando %\n\n"
        "BONUS: calcule quantos dias completos, horas, minutos e segundos\n"
        "representam 1.000.000 de segundos usando // e % em cascata."
    ),
    leitura=[
        "docs.python.org/pt-br/3/reference/expressions.html — operadores e precedencia",
        "docs.python.org/pt-br/3/library/functions.html#divmod — funcao divmod()",
        "PEP 8 — secao sobre expressoes e operadores",
    ],
))
# ---------------------------------------------------------------- DIA 4
DIAS.append(Dia(
    numero=4,
    titulo="Strings: fatiamento, métodos e f-strings",
    nivel="Iniciante",
    duracao="100 min",
    objetivos=[
        "Entender o que é uma string por dentro: uma sequência imutável de caracteres",
        "Acessar caracteres individuais com índices positivos e negativos",
        "Fatiar strings com [inicio:fim:passo] e dominar os casos mais comuns",
        "Usar os métodos de string mais importantes para limpar e transformar texto",
        "Formatar saída com f-strings, incluindo alinhamento e casas decimais",
        "Diferenciar strings comuns, cruas (raw) e multilinha, e saber quando usar cada uma",
        "Escrever suas primeiras funções usando o molde mínimo com def e return",
    ],
    teoria="""
Texto é um dos tipos de dados mais usados em programação. Quase tudo
que um programa faz envolve texto em algum ponto: ler nomes, exibir
mensagens, processar arquivos. Em Python, texto é representado pelo
tipo str (abreviação de string, que em inglês significa "sequência de
caracteres").

ATENÇÃO — NOVIDADE IMPORTANTE:
A partir de hoje, os exercícios vão pedir FUNÇÕES. A sintaxe completa
de funções (parâmetros avançados, escopo, recursão) chega no Dia 11.
Por agora, basta o molde mínimo:

    def nome_da_funcao(parametro):
        resultado = ...        # faça o cálculo aqui dentro
        return resultado       # devolva o valor para quem chamou

    def  — palavra-chave que declara a função
    nome_da_funcao  — o nome que você escolhe
    (parametro)  — o valor que a função recebe para trabalhar
    return  — encerra a função E entrega o valor calculado

Se a função terminar sem return, ela devolve None silenciosamente —
uma fonte comum de bugs para iniciantes. Sempre verifique se o return
está presente quando a função deve devolver algo.

---------------------------------------------------------------------------
1. O que é uma string por dentro
---------------------------------------------------------------------------
Uma string é uma SEQUÊNCIA ORDENADA de caracteres. Pense como um trilho
de trem: cada vagão é um caractere, e cada vagão tem um número de
posição chamado ÍNDICE, começando do zero.

    s = "Python"
    Índices:   0   1   2   3   4   5
    Caractere: P   y   t   h   o   n

    Índices negativos (contam do fim):
               -6  -5  -4  -3  -2  -1

Acessando caracteres individuais:

    s[0]    # 'P'   — primeiro caractere
    s[1]    # 'y'
    s[5]    # 'n'   — último caractere
    s[-1]   # 'n'   — último (mais fácil com índice negativo)
    s[-2]   # 'o'   — penúltimo
    s[10]   # IndexError! — índice fora do alcance

STRINGS SÃO IMUTÁVEIS:
Diferente de listas (que veremos no Dia 8), strings não podem ser
alteradas depois de criadas. Tentar mudar um caractere causa erro:

    s[0] = "J"    # TypeError: 'str' object does not support item assignment

Toda operação que parece "modificar" uma string na verdade cria uma
string NOVA. A original fica intacta. Isso tem uma consequência prática:

    nome = "  Ana  "
    nome.strip()        # cria uma nova string 'Ana', mas NÃO altera nome
    print(nome)         # ainda imprime '  Ana  ' com os espaços!

    nome = nome.strip() # agora sim: reatribui, nome passa a valer 'Ana'

Sempre reatribua (ou guarde numa nova variável) o resultado dos métodos
de string.

---------------------------------------------------------------------------
2. Fatiamento: s[inicio:fim:passo]
---------------------------------------------------------------------------
Fatiamento (slicing) extrai uma parte da string. A sintaxe é:

    string[inicio:fim:passo]

Regra mais importante: o FIM é sempre EXCLUSIVO — o caractere naquela
posição NÃO entra no resultado.

Com a string s = "Python":

    Operação       Resultado    Explicação
    ----------     ---------    ------------------------------------------
    s[0:3]         'Pyt'        posições 0, 1, 2 (para antes de 3)
    s[2:5]         'tho'        posições 2, 3, 4
    s[3:]          'hon'        da posição 3 até o fim
    s[:3]          'Pyt'        do começo até a posição 3 (exclusiva)
    s[:]           'Python'     cópia completa da string
    s[:-1]         'Pytho'      tudo menos o último caractere
    s[-3:]         'hon'        os últimos 3 caracteres
    s[::2]         'Pto'        de 2 em 2 (posições 0, 2, 4)
    s[::-1]        'nohtyP'     passo -1: percorre de trás para frente

O fatiamento com s[::-1] é o idioma clássico para inverter uma string.

UMA VANTAGEM SOBRE ÍNDICE DIRETO: fatiamento nunca gera IndexError.
Pedir uma fatia além dos limites simplesmente devolve o que existe:

    s[100:200]    # '' — string vazia, sem erro
    s[0]          # IndexError se a string estiver vazia!

---------------------------------------------------------------------------
3. Métodos essenciais de string
---------------------------------------------------------------------------
Strings têm dezenas de métodos embutidos. Os mais usados no dia a dia:

TRANSFORMANDO CAPITALIZAÇÃO:

    "python".upper()          # 'PYTHON'
    "PYTHON".lower()          # 'python'
    "python course".title()   # 'Python Course'  (cada palavra em maiúscula)
    "Python".swapcase()       # 'pYTHON'  (inverte maiúscula/minúscula)

REMOVENDO ESPAÇOS E CARACTERES DAS PONTAS:

    "  ola  ".strip()         # 'ola'    (remove dos dois lados)
    "  ola  ".lstrip()        # 'ola  '  (só da esquerda)
    "  ola  ".rstrip()        # '  ola'  (só da direita)
    "xxxolaxxx".strip("x")    # 'ola'    (remove o caractere 'x' das pontas)

SUBSTITUINDO PARTES:

    "ola mundo".replace("mundo", "Python")   # 'ola Python'
    "aabbaa".replace("a", "x")              # 'xxbbxx'  (substitui todos)
    "aabbaa".replace("a", "x", 2)          # 'xxbbaa'  (substitui só os 2 primeiros)

DIVIDINDO E JUNTANDO:

    "a,b,c".split(",")        # ['a', 'b', 'c']  — divide em lista
    "  a  b  c  ".split()    # ['a', 'b', 'c']  — sem args: divide por espaço e ignora extras
    "-".join(["a", "b", "c"]) # 'a-b-c'   — junta lista numa string

Nota: join pode parecer ao contrário. Leia como: "use '-' para juntar
os elementos da lista". O separador fica entre cada elemento.

BUSCANDO DENTRO DA STRING:

    "Python".find("th")       # 2    — índice onde começa (ou -1 se não achar)
    "Python".index("th")      # 2    — igual a find, mas levanta ValueError se não achar
    "Python".count("t")       # 1    — quantas vezes aparece
    "Python".startswith("Py") # True
    "Python".endswith("on")   # True
    "th" in "Python"          # True — operador in também funciona com strings

TESTANDO O CONTEÚDO:

    "42".isdigit()            # True  — só dígitos?
    "abc".isalpha()           # True  — só letras?
    "abc123".isalnum()        # True  — só letras e números?
    "   ".isspace()           # True  — só espaços?

ALINHANDO E PREENCHENDO:

    "42".zfill(5)             # '00042'  — preenche com zeros à esquerda
    "ola".center(9)           # '   ola   '  — centralizado em 9 posições
    "ola".ljust(9)            # 'ola      '  — alinhado à esquerda
    "ola".rjust(9)            # '      ola'  — alinhado à direita

---------------------------------------------------------------------------
4. f-strings: a forma moderna de formatar texto
---------------------------------------------------------------------------
f-strings (ou formatted string literals) são a forma recomendada de
montar strings com valores de variáveis. Prefixe a string com f e use
chaves {} para embutir qualquer expressão Python:

    nome = "Ana"
    idade = 30
    print(f"Nome: {nome}, Idade: {idade}")    # Nome: Ana, Idade: 30
    print(f"Daqui 10 anos: {idade + 10}")     # Daqui 10 anos: 40
    print(f"Maiúsculas: {nome.upper()}")       # Maiúsculas: ANA

Você pode colocar QUALQUER expressão Python dentro das chaves.

FORMATANDO NÚMEROS:

    valor = 1234.5678

    f"{valor:.2f}"        # '1234.57'   — 2 casas decimais
    f"{valor:,.2f}"       # '1,234.57'  — separador de milhar + 2 casas
    f"{valor:>12.2f}"     # '     1234.57'  — largura 12, alinhado à direita
    f"{valor:e}"          # '1.234568e+03'  — notação científica
    f"{0.856:.1%}"        # '85.6%'  — porcentagem

FORMATANDO TEXTO:

    nome = "Ana"
    f"{nome:10}"          # 'Ana       '  — alinhado à esquerda em 10 chars
    f"{nome:>10}"         # '       Ana'  — alinhado à direita
    f"{nome:^10}"         # '   Ana    '  — centralizado
    f"{nome:*^10}"        # '***Ana****'  — centralizado com * de preenchimento

RECURSO DE DEPURAÇÃO (Python 3.8+):

    x = 42
    f"{x=}"               # 'x=42'  — mostra o nome E o valor, ótimo para debug

ANTES DAS F-STRINGS existia o método .format():

    "Nome: {}, Idade: {}".format("Ana", 30)
    "Nome: {nome}".format(nome="Ana")

E o operador %:

    "Nome: %s, Idade: %d" % ("Ana", 30)

Você vai encontrar os dois em código antigo. f-strings são preferidas em
código novo por serem mais legíveis e ligeiramente mais rápidas.

---------------------------------------------------------------------------
5. Strings cruas (raw strings) e multilinha
---------------------------------------------------------------------------
RAW STRINGS (prefixo r):
Desativam completamente o processamento de escapes — cada barra
invertida é tratada literalmente.

    caminho = "C:\novo\teste"      # \n e \t viram quebra de linha e tab!
    caminho = r"C:\novo\teste"     # correto: cada \ é literal

    print("linha1\nlinha2")        # imprime em duas linhas
    print(r"linha1\nlinha2")       # imprime literalmente: linha1\nlinha2

Raw strings são essenciais em caminhos de arquivo no Windows e em
expressões regulares (Dia 26), onde \d, \w e outros têm significado
próprio que não deve ser interpretado como escape de string.

STRINGS MULTILINHA (três aspas):
Preservam quebras de linha dentro da própria string, sem precisar de \n:

    texto = \"\"\"
    Primeira linha
    Segunda linha
    Terceira linha
    \"\"\"

    sql = \"\"\"
    SELECT nome, idade
    FROM usuarios
    WHERE ativo = 1
    \"\"\"

São muito usadas em docstrings (Dia 1), templates de texto e consultas SQL.

ESCAPES COMUNS:

    Escape    Significado
    ------    -----------
    \\n        nova linha
    \\t        tabulação (tab)
    \\\\        barra invertida literal
    \\"        aspas duplas dentro de string de aspas duplas
    \\'        aspas simples dentro de string de aspas simples

---------------------------------------------------------------------------
6. Encadeamento de métodos
---------------------------------------------------------------------------
Como cada método devolve uma nova string, você pode encadear chamadas:

    "  ANA maria DA silva  ".strip().lower().title()
    # Passo 1: strip() -> "ANA maria DA silva"
    # Passo 2: lower() -> "ana maria da silva"
    # Passo 3: title() -> "Ana Maria Da Silva"

Leia da esquerda para a direita: cada método recebe o resultado do
anterior e produz uma nova string para o próximo. Isso é muito comum e
idiomático em Python — mas não exagere: mais de 3 ou 4 encadeamentos
seguidos começa a dificultar a leitura.
""",
    exemplos=[
        Exemplo(
            titulo="Indexação, fatiamento e imutabilidade",
            codigo='''s = "Python"

# Indices positivos e negativos
print(s[0], s[-1])        # P n
print(s[1:4])             # yth
print(s[::-1])            # nohtyP  (invertida)
print(s[::2])             # Pto     (de 2 em 2)

# Fatiamento nunca da IndexError
print(s[100:200])         # ''  (string vazia, sem erro)

# Strings sao imutaveis
# s[0] = "J"  -- isto causaria TypeError

# Para "alterar", cria-se uma string nova
nova = "J" + s[1:]
print(nova)               # Jython

# Erro classico: esquecer de reatribuir
nome = "  ana  "
nome.strip()              # cria nova string, mas nao altera nome!
print(repr(nome))         # '  ana  '  — ainda tem espacos

nome = nome.strip()       # agora sim
print(repr(nome))         # 'ana'
''',
            explicacao="repr() mostra a string com aspas e escapes visíveis, "
                       "útil para depurar: você vê exatamente o que está "
                       "dentro da string, incluindo espaços e quebras de linha. "
                       "O erro de esquecer de reatribuir é um dos mais comuns "
                       "com strings — lembre-se sempre.",
        ),
        Exemplo(
            titulo="Limpando e transformando texto real",
            codigo='''# Simulando dados bagunçados vindos de um formulario
entrada = "   ANA maria DA silva  "

# Encadeamento de metodos para normalizar
nome_limpo = entrada.strip().title()
print(nome_limpo)         # Ana Maria Da Silva

# Dividindo e reorganizando
partes = nome_limpo.split()
print(partes)             # ['Ana', 'Maria', 'Da', 'Silva']

sobrenome = partes[-1]
primeiro_nome = partes[0]
print(f"{sobrenome}, {primeiro_nome}")   # Silva, Ana

# Verificando o conteudo
email = "ana.silva@email.com"
print(email.count("."))           # 2
print(email.startswith("ana"))    # True
print(email.split("@"))           # ['ana.silva', 'email.com']
dominio = email.split("@")[1]
print(dominio)                    # email.com
''',
            explicacao="Esse padrão de strip() + title() para normalizar "
                       "nomes digitados por usuários é muito comum em "
                       "sistemas reais. split() sem argumentos é mais robusto "
                       "do que split(' ') pois lida com múltiplos espaços.",
        ),
        Exemplo(
            titulo="f-strings para relatórios formatados",
            codigo='''# Tabela de precos formatada com f-strings
itens = [
    ("Cafe",    24.90),
    ("Acucar",   5.50),
    ("Filtro",  12.75),
    ("Leite",    7.20),
]

print(f"{'Produto':<12} {'Preco':>8}")
print("-" * 22)

total = 0
for nome, preco in itens:
    print(f"{nome:<12} {preco:>8.2f}")
    total += preco

print("-" * 22)
print(f"{'TOTAL':<12} {total:>8.2f}")

# Debug com f"{variavel=}"
x = 42
pi = 3.14159
print(f"\n{x=}, {pi=:.2f}")    # x=42, pi=3.14
''',
            explicacao=":<12 alinha à esquerda em 12 caracteres. "
                       ":>8.2f alinha à direita em 8 caracteres com 2 casas "
                       "decimais. Essa combinação cria tabelas alinhadas "
                       "sem precisar contar espaços manualmente. "
                       "f'{var=}' é ótimo para depurar: mostra nome e valor.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d04e1",
            enunciado=(
                "Escreva a funcao gritar(texto) que:\n"
                "   1. Remove espacos do inicio e do fim do texto\n"
                "   2. Converte tudo para MAIUSCULAS\n"
                "   3. Adiciona um ponto de exclamacao no final\n\n"
                "Exemplos:\n"
                "   gritar('  ola  ')    -> 'OLA!'\n"
                "   gritar('python')     -> 'PYTHON!'\n"
                "   gritar('  ja e tarde') -> 'JA E TARDE!'\n\n"
                "Use o encadeamento de metodos: .strip() remove espacos\n"
                "das pontas, .upper() converte para maiusculas.\n"
                "Concatene '!' no final com o operador +."
            ),
            funcao="gritar",
            assinatura="def gritar(texto):",
            testes=[
                ("gritar('  ola  ')", "'OLA!'"),
                ("gritar('python')", "'PYTHON!'"),
                ("gritar('  ja e tarde')", "'JA E TARDE!'"),
            ],
            dica="return texto.strip().upper() + '!'",
        ),
        Exercicio(
            id="d04e2",
            enunciado=(
                "Escreva a funcao inverter(texto) que devolve o texto\n"
                "escrito de tras para frente.\n\n"
                "Exemplos:\n"
                "   inverter('abc')  -> 'cba'\n"
                "   inverter('')     -> ''    (string vazia continua vazia)\n"
                "   inverter('ana')  -> 'ana' (palindromo: igual ao inverso)\n\n"
                "Use fatiamento com passo negativo: texto[::-1]\n"
                "   texto[::1]   percorre do inicio ao fim\n"
                "   texto[::-1]  percorre do fim ao inicio"
            ),
            funcao="inverter",
            assinatura="def inverter(texto):",
            testes=[
                ("inverter('abc')", "'cba'"),
                ("inverter('')", "''"),
                ("inverter('ana')", "'ana'"),
            ],
            dica="return texto[::-1]",
        ),
        Exercicio(
            id="d04e3",
            enunciado=(
                "Escreva a funcao eh_palindromo(texto) que devolve True se\n"
                "o texto for um palindromo (le igual de tras para frente),\n"
                "ignorando maiusculas/minusculas e espacos.\n\n"
                "Exemplos:\n"
                "   eh_palindromo('Ame a ema')  -> True\n"
                "   eh_palindromo('Python')     -> False\n"
                "   eh_palindromo('a')          -> True\n"
                "   eh_palindromo('Anilina')    -> True\n\n"
                "Estrategia:\n"
                "   1. Converta para minusculas: .lower()\n"
                "   2. Remova os espacos: .replace(' ', '')\n"
                "   3. Compare com o reverso: texto_limpo == texto_limpo[::-1]"
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
            dica="Normalize com .lower().replace(' ', '') e compare com o reverso usando [::-1].",
        ),
    ],
    quiz=[
        Quiz(
            "O que 'Python'[1:4] devolve?",
            ["'Pyt'  — posicoes 0, 1, 2",
             "'yth'  — posicoes 1, 2, 3 (fim exclusivo)",
             "'ytho' — posicoes 1, 2, 3, 4",
             "IndexError — indice fora do alcance"],
            1,
            "Fatiamento [1:4] começa no indice 1 ('y') e para ANTES do indice 4 (exclusivo). "
            "Posicoes incluidas: 1 ('y'), 2 ('t'), 3 ('h'). Resultado: 'yth'.",
        ),
        Quiz(
            "Por que 'nome.strip()' sozinho nao altera a variavel nome?",
            ["strip() e um metodo muito lento",
             "Strings sao imutaveis — strip() cria uma string nova e a original fica intacta",
             "Faltou passar um argumento para strip()",
             "strip() so funciona dentro de funcoes"],
            1,
            "Strings sao imutaveis em Python. Todo metodo que 'transforma' uma string "
            "na verdade devolve uma STRING NOVA, sem tocar na original. "
            "Para 'alterar' nome, reatribua: nome = nome.strip()",
        ),
        Quiz(
            "Qual a diferenca entre .find() e .index() ao procurar uma substring?",
            ["Nao ha diferenca — os dois sao identicos",
             "find() devolve -1 se nao achar; index() levanta ValueError",
             "index() devolve -1 se nao achar; find() levanta ValueError",
             "find() so funciona com caracteres unicos"],
            1,
            "find() e mais tolerante: devolve -1 se nao encontrar (util para checar sem tratar erro). "
            "index() e mais estrito: levanta ValueError se nao encontrar "
            "(util quando a ausencia seria um bug).",
        ),
        Quiz(
            "Para que serve o prefixo r antes de uma string, como em r'C:\\\\Users\\\\nome'?",
            ["Torna a string somente leitura (read-only)",
             "Repete a string duas vezes",
             "Desativa o processamento de escapes: cada \\ e tratado literalmente",
             "Converte a string para bytes"],
            2,
            "Raw string (string crua): o Python nao interpreta \\n como nova linha, "
            "\\t como tab, etc. Cada caractere e exatamente o que aparece. "
            "Essencial para caminhos de arquivo no Windows e expressoes regulares.",
        ),
    ],
    projeto=(
        "Crie o arquivo analisador.py que receba uma frase (pode ser uma\n"
        "variavel fixa, sem input()) e mostre um relatorio completo:\n\n"
        "   Frase original:  '  O Python e incrivel!  '\n"
        "   Frase limpa:     'O Python e incrivel!'\n"
        "   Frase invertida: '!livercing e nohtyP O'\n"
        "   Maiusculas:      'O PYTHON E INCRIVEL!'\n"
        "   Palavras:        4\n"
        "   Caracteres:      21\n"
        "   Palavra mais longa: 'incrivel'\n\n"
        "Use f-strings para formatar cada linha com o rotulo alinhado\n"
        "a esquerda em 20 caracteres (f'{rotulo:<20} {valor}').\n\n"
        "BONUS: verifique se a frase limpa (sem pontuacao) e um palindromo."
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/string.html — mini-linguagem de formato",
        "docs.python.org/pt-br/3/library/stdtypes.html#string-methods — todos os metodos",
        "docs.python.org/pt-br/3/tutorial/introduction.html#strings — strings no tutorial oficial",
    ],
))
# ---------------------------------------------------------------- DIA 5
DIAS.append(Dia(
    numero=5,
    titulo="Condicionais: if, elif, else e match",
    nivel="Iniciante",
    duracao="90 min",
    objetivos=[
        "Escrever decisões com if, elif e else entendendo exatamente como a ordem importa",
        "Escrever condições no estilo idiomático do Python, sem traduzir de outras linguagens",
        "Usar o operador ternário para decisões simples em uma linha",
        "Evitar aninhamento excessivo com cláusulas de guarda (sair cedo)",
        "Usar match/case para casar padrões de forma mais expressiva que um if/elif longo",
        "Reconhecer as armadilhas mais comuns ao escrever condicionais",
    ],
    teoria="""
Até agora seus programas executavam linha por linha, de cima para baixo,
sem nunca desviar do caminho. Mas programas reais precisam TOMAR DECISÕES:
mostrar mensagem diferente dependendo da nota, cobrar preço diferente
dependendo do horário, agir diferente dependendo da entrada do usuário.

Para isso existem as estruturas condicionais — o mecanismo que permite ao
programa escolher qual caminho seguir.

---------------------------------------------------------------------------
1. if, elif e else: a estrutura básica de decisão
---------------------------------------------------------------------------
A estrutura completa:

    if condicao_1:
        # bloco executado se condicao_1 for verdadeira
    elif condicao_2:
        # bloco executado se condicao_1 for falsa E condicao_2 for verdadeira
    elif condicao_3:
        # bloco executado se as anteriores forem falsas E esta for verdadeira
    else:
        # bloco executado se NENHUMA condição acima for verdadeira

Pontos importantes:

DOIS-PONTOS ( : ) são obrigatórios ao final de cada if, elif e else.
Esquecer é um dos erros de sintaxe mais comuns.

INDENTAÇÃO define o bloco. Tudo com 4 espaços de recuo depois do if
faz parte daquele bloco. Quando o recuo volta ao nível anterior, o
bloco terminou.

APENAS O PRIMEIRO RAMO VERDADEIRO EXECUTA. Mesmo que uma condição
mais abaixo também seja verdadeira, ela não é avaliada:

    idade = 25
    if idade >= 18:
        print("maior de idade")    # este executa
    elif idade >= 21:
        print("nunca aparece")     # este NUNCA executa — o de cima já pegou

Isso significa que a ORDEM dos elif importa muito quando as condições
se sobrepõem. Organize sempre do caso mais específico para o mais geral,
ou vice-versa, de forma consciente.

elif e else são OPCIONAIS. Um if pode existir sozinho:

    if saldo < 0:
        print("saldo negativo!")
    # o programa continua aqui de qualquer forma

---------------------------------------------------------------------------
2. Escrevendo condições no estilo Python
---------------------------------------------------------------------------
Quem vem de outra linguagem costuma escrever Python "traduzido". Compare
as formas verbosa e idiomática:

    Forma verbosa (traduzida)          Forma idiomática (Python)
    ---------------------------------  ---------------------------------
    if len(lista) > 0:                 if lista:
    if nome != "":                     if nome:
    if valor == None:                  if valor is None:
    if ativo == True:                  if ativo:
    if ativo == False:                 if not ativo:
    if 0 <= x and x <= 10:            if 0 <= x <= 10:
    if x == "a" or x == "b":          if x in ("a", "b"):
    if x == 1 or x == 2 or x == 3:   if x in (1, 2, 3):

A coluna da direita não é só mais curta — ela expressa a intenção de
forma mais direta e é o que a comunidade Python espera ao ler seu código.

Por que "if lista:" funciona? Porque listas vazias são falsy (Dia 3):
o próprio valor da lista já diz se tem conteúdo ou não.

Por que "if x in (1, 2, 3):" é melhor que vários "or"? Porque escala
sem se tornar ilegível — se a lista de opções crescer, você só acrescenta
elementos, não repete "x ==" várias vezes.

---------------------------------------------------------------------------
3. Operador ternário: decisão em uma linha
---------------------------------------------------------------------------
Quando você precisa escolher entre dois valores simples, o operador
ternário encurta o código:

    # Forma longa
    if nota >= 6:
        situacao = "aprovado"
    else:
        situacao = "reprovado"

    # Forma ternária (equivalente)
    situacao = "aprovado" if nota >= 6 else "reprovado"

A sintaxe é: valor_se_verdadeiro if condicao else valor_se_falso

Note que a condição fica no MEIO — diferente do if comum, que a condição
fica no início. Isso confunde um pouco no começo.

QUANDO USAR: apenas quando cabe confortavelmente em uma linha e a lógica
é simples. Para mais de uma condição, use o if tradicional:

    # Evite encadear ternários — dificulta a leitura
    status = "A" if nota >= 9 else "B" if nota >= 7 else "C"

    # Prefira o if/elif — mais claro
    if nota >= 9:
        status = "A"
    elif nota >= 7:
        status = "B"
    else:
        status = "C"

---------------------------------------------------------------------------
4. Cláusula de guarda: eliminando aninhamento
---------------------------------------------------------------------------
Um problema muito comum em código de iniciante é o aninhamento excessivo
de ifs dentro de ifs, criando o que a comunidade chama de "código em flecha"
pelo formato triangular que a indentação forma:

    def processar_pedido(pedido):
        if pedido:
            if pedido["pago"]:
                if pedido["tem_estoque"]:
                    if pedido["endereco"]:
                        return "enviar"
                    else:
                        return "sem endereco"
                else:
                    return "sem estoque"
            else:
                return "nao pago"
        else:
            return "pedido vazio"

Cada nível de aninhamento exige que o leitor carregue mentalmente todas
as condições anteriores para entender o que está acontecendo. Com 4 ou
5 níveis, o código fica difícil de ler e de manter.

A solução é a CLÁUSULA DE GUARDA: inverta a lógica e saia cedo (com
return) a cada caso inválido, mantendo o código plano:

    def processar_pedido(pedido):
        if not pedido:
            return "pedido vazio"
        if not pedido["pago"]:
            return "nao pago"
        if not pedido["tem_estoque"]:
            return "sem estoque"
        if not pedido["endereco"]:
            return "sem endereco"
        return "enviar"

O código fica PLANO (sem aninhamento) e cada linha se lê isoladamente,
sem precisar carregar contexto de condições anteriores na cabeça.

Regra prática: se você estiver escrevendo mais de 2 ou 3 níveis de
aninhamento, provavelmente existe uma cláusula de guarda esperando
para deixar o código mais limpo.

---------------------------------------------------------------------------
5. match/case: casamento de padrões (Python 3.10+)
---------------------------------------------------------------------------
O match é frequentemente comparado ao switch de outras linguagens, mas
é muito mais poderoso: ele faz CASAMENTO DE PADRÕES ESTRUTURAIS, podendo
verificar a forma de listas, dicionários e objetos ao mesmo tempo.

Forma básica (substitui if/elif com muitas comparações de igualdade):

    comando = "sair"

    match comando:
        case "iniciar":
            print("iniciando...")
        case "pausar":
            print("pausando...")
        case "sair":
            print("encerrando...")
        case _:
            print("comando desconhecido")

case _: é o padrão coringa — equivale ao else, captura qualquer coisa
não capturada pelos cases anteriores. Deve vir sempre por último.

CASANDO ESTRUTURAS (o poder real do match):

    match comando.split():
        case ["sair"]:
            print("encerrando")
        case ["ir", destino]:
            print(f"indo para {destino}")
        case ["pegar", item, "em", local]:
            print(f"pegando {item} em {local}")
        case _:
            print("nao entendi")

Aqui, case ["ir", destino] não é só uma comparação: ele verifica se a
lista tem exatamente 2 elementos, se o primeiro é "ir", e se tudo bater,
atribui o segundo elemento automaticamente à variável destino. É uma
verificação de estrutura + atribuição em um único passo.

CASANDO DICIONÁRIOS:

    match evento:
        case {"tipo": "clique", "x": x, "y": y}:
            print(f"clique em ({x}, {y})")
        case {"tipo": "tecla", "valor": v}:
            print(f"tecla: {v}")

GUARDAS com if para refinar um padrão:

    match numero:
        case n if n < 0:
            print("negativo")
        case 0:
            print("zero")
        case n if n > 0:
            print("positivo")

---------------------------------------------------------------------------
6. Armadilhas comuns
---------------------------------------------------------------------------
CONFUNDIR = com ==:
    if x = 5:      # SyntaxError — Python não permite isso
    if x == 5:     # correto

Python não permite atribuição dentro de if, o que evita o bug clássico
de outras linguagens onde "if (x = 5)" compila mas faz a coisa errada.
O operador morsa (:=) é a exceção, mas é um assunto avançado.

COMPARAR FLOATS COM ==:
    if 0.1 + 0.2 == 0.3:    # False! (veja Dia 2)
    if math.isclose(0.1 + 0.2, 0.3):   # correto

ESQUECER OS DOIS-PONTOS:
    if x > 0      # SyntaxError: expected ':'
    if x > 0:     # correto

INDENTAÇÃO INCONSISTENTE:
    if x > 0:
        print("positivo")
      print("fim")    # IndentationError: unexpected indent
""",
    exemplos=[
        Exemplo(
            titulo="Classificação com if/elif/else",
            codigo='''def classificar_imc(imc):
    """Classifica o IMC segundo a tabela da OMS."""
    if imc < 18.5:
        return "Abaixo do peso"
    elif imc < 25.0:
        return "Peso normal"
    elif imc < 30.0:
        return "Sobrepeso"
    elif imc < 35.0:
        return "Obesidade grau I"
    else:
        return "Obesidade grau II ou mais"

# Testando com alguns valores
for peso, altura in [(50, 1.70), (70, 1.70), (90, 1.70), (120, 1.70)]:
    imc = peso / altura ** 2
    print(f"Peso {peso}kg, IMC {imc:.1f}: {classificar_imc(imc)}")
''',
            explicacao="A ordem dos elif é crucial: cada um já sabe que "
                       "os anteriores falharam. imc < 25 só chega aqui "
                       "se imc >= 18.5 (porque o primeiro elif já teria "
                       "capturado o caso menor). Isso evita repetir "
                       "condições como '18.5 <= imc < 25'.",
        ),
        Exemplo(
            titulo="Cláusula de guarda versus aninhamento",
            codigo='''# Versao com aninhamento (dificil de ler)
def pode_sacar_ruim(saldo, valor, conta_ativa):
    if conta_ativa:
        if valor > 0:
            if saldo >= valor:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

# Versao com clausulas de guarda (limpa e plana)
def pode_sacar(saldo, valor, conta_ativa):
    if not conta_ativa:
        return False
    if valor <= 0:
        return False
    if saldo < valor:
        return False
    return True    # passou por todas as guardas: pode sacar

print(pode_sacar(100, 50, True))    # True
print(pode_sacar(100, 50, False))   # False
print(pode_sacar(100, 0, True))     # False
print(pode_sacar(30, 50, True))     # False
''',
            explicacao="As duas funções fazem exatamente a mesma coisa. "
                       "A versão com cláusulas de guarda é mais fácil de "
                       "ler porque cada linha se justifica sozinha, sem "
                       "exigir que você rastreie os ifs anteriores. "
                       "Em código profissional, a segunda forma é sempre preferida.",
        ),
        Exemplo(
            titulo="match/case com padrões estruturais",
            codigo='''def interpretar(entrada):
    """Interpreta um comando de texto como lista de palavras."""
    match entrada.lower().split():
        case ["oi"] | ["ola"] | ["ola", "mundo"]:
            return "Ola! Como posso ajudar?"
        case ["soma", a, b]:
            return f"Resultado: {int(a) + int(b)}"
        case ["repete", *palavras]:
            return " ".join(palavras)
        case []:
            return "Voce nao digitou nada."
        case _:
            return f"Nao entendi: '{entrada}'"

print(interpretar("oi"))
print(interpretar("soma 10 20"))
print(interpretar("repete python e otimo"))
print(interpretar(""))
print(interpretar("voar alto"))
''',
            explicacao="O operador | no case permite casar vários padrões "
                       "na mesma linha. *palavras captura zero ou mais "
                       "elementos restantes numa lista. case []: "
                       "casa especificamente uma lista vazia. "
                       "Cada case é avaliado na ordem, e o primeiro que "
                       "casar executa — igual ao if/elif.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d05e1",
            enunciado=(
                "Escreva a funcao classificar(nota) que devolve a letra\n"
                "correspondente a faixa de nota:\n\n"
                "   nota >= 90  ->  'A'\n"
                "   nota >= 80  ->  'B'\n"
                "   nota >= 70  ->  'C'\n"
                "   nota >= 60  ->  'D'\n"
                "   abaixo     ->  'F'\n\n"
                "Exemplos:\n"
                "   classificar(95) -> 'A'\n"
                "   classificar(80) -> 'B'\n"
                "   classificar(70) -> 'C'\n"
                "   classificar(61) -> 'D'\n"
                "   classificar(12) -> 'F'\n\n"
                "DICA IMPORTANTE: use elif, nao if separados.\n"
                "Com if separados, nota=95 passaria por TODOS os ifs\n"
                "e devolveria 'F' no final. Com elif, para no primeiro\n"
                "que for verdadeiro.\n"
                "Teste do maior para o menor: comece com >= 90."
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
            dica="Comece com 'if nota >= 90: return A', depois elif para cada faixa abaixo.",
        ),
        Exercicio(
            id="d05e2",
            enunciado=(
                "Escreva a funcao maior_de_tres(a, b, c) que devolve o\n"
                "maior dos tres valores recebidos, SEM usar a funcao max().\n\n"
                "Exemplos:\n"
                "   maior_de_tres(1, 2, 3)   -> 3\n"
                "   maior_de_tres(9, 2, 3)   -> 9\n"
                "   maior_de_tres(-1, -5, -3) -> -1\n"
                "   maior_de_tres(5, 5, 2)   -> 5  (empate: qualquer um serve)\n\n"
                "Estrategia:\n"
                "   1. Compare a com b e guarde o maior em uma variavel\n"
                "   2. Compare esse maior com c\n"
                "   3. Devolva o maior final\n\n"
                "Dica: voce pode usar o operador ternario:\n"
                "   maior = a if a > b else b"
            ),
            funcao="maior_de_tres",
            assinatura="def maior_de_tres(a, b, c):",
            testes=[
                ("maior_de_tres(1, 2, 3)", "3"),
                ("maior_de_tres(9, 2, 3)", "9"),
                ("maior_de_tres(-1, -5, -3)", "-1"),
                ("maior_de_tres(5, 5, 2)", "5"),
            ],
            dica="Compare a com b para achar o maior entre eles, depois compare esse maior com c.",
        ),
        Exercicio(
            id="d05e3",
            enunciado=(
                "Escreva tipo_triangulo(a, b, c) que recebe tres lados e\n"
                "devolve o tipo do triangulo:\n\n"
                "   'invalido'    se os lados nao formam triangulo\n"
                "   'equilatero'  se todos os tres lados sao iguais\n"
                "   'isosceles'   se exatamente dois lados sao iguais\n"
                "   'escaleno'    se todos os lados sao diferentes\n\n"
                "REGRA DO TRIANGULO: tres lados formam um triangulo valido\n"
                "somente se CADA lado for menor que a SOMA dos outros dois:\n"
                "   a < b + c  E  b < a + c  E  c < a + b\n\n"
                "Exemplos:\n"
                "   tipo_triangulo(1, 2, 10) -> 'invalido'   (1+2 < 10)\n"
                "   tipo_triangulo(3, 3, 3)  -> 'equilatero'\n"
                "   tipo_triangulo(3, 3, 5)  -> 'isosceles'\n"
                "   tipo_triangulo(3, 4, 5)  -> 'escaleno'\n\n"
                "Use clausula de guarda: valide primeiro, classifique depois."
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
            dica="Valide com clausula de guarda primeiro. Depois: se a==b==c: equilatero. Se dois iguais: isosceles. Senao: escaleno.",
        ),
    ],
    quiz=[
        Quiz(
            "Quantos ramos de um if/elif/elif/else podem executar em uma mesma rodada?",
            ["Todos os que forem verdadeiros",
             "No maximo um — o primeiro ramo verdadeiro encontrado",
             "Sempre dois — o if e o else",
             "Depende da indentacao"],
            1,
            "A execucao para no PRIMEIRO ramo verdadeiro. Os demais nao sao "
            "nem avaliados. Por isso a ordem dos elif e tao importante.",
        ),
        Quiz(
            "Qual a forma idiomatica em Python para verificar se uma lista nao esta vazia?",
            ["if len(lista) > 0:",
             "if lista != []:",
             "if lista:",
             "if lista.size() > 0:"],
            2,
            "Listas vazias sao falsy em Python. 'if lista:' e mais curto, "
            "mais legivel e funciona com qualquer tipo de colecao "
            "(listas, tuplas, dicionarios, conjuntos) sem precisar saber qual metodo usar.",
        ),
        Quiz(
            "O que a clausula de guarda resolve?",
            ["Protege o programa contra erros de seguranca",
             "Elimina aninhamento excessivo saindo cedo com return para cada caso invalido",
             "Guarda valores em variaveis automaticamente",
             "E um recurso exclusivo do Python 3.10+"],
            1,
            "Clausula de guarda inverte a logica: em vez de aninhar os casos validos, "
            "voce rejeita os casos invalidos cedo (return) e o caminho feliz "
            "fica sempre no final, sem aninhamento.",
        ),
        Quiz(
            "O que case _: representa em um bloco match?",
            ["Faz o programa ignorar o valor",
             "E o padrao coringa: casa qualquer valor nao capturado pelos cases anteriores",
             "So funciona com strings",
             "Levanta uma excecao se nenhum case anterior casar"],
            1,
            "_ e o padrao coringa do match, equivalente ao else do if. "
            "Deve sempre vir por ultimo, pois casaria qualquer coisa e "
            "impediria os cases seguintes de serem avaliados.",
        ),
    ],
    projeto=(
        "Crie o arquivo calculadora_notas.py com uma funcao avaliar(nome, nota)\n"
        "que receba o nome do aluno e sua nota (0 a 100) e:\n\n"
        "   1. Valide a nota com clausula de guarda (nota fora de 0-100 -> erro)\n"
        "   2. Classifique em letra (A/B/C/D/F) usando if/elif\n"
        "   3. Defina a situacao usando operador ternario:\n"
        "      aprovado se nota >= 60, reprovado caso contrario\n"
        "   4. Exiba um relatorio formatado:\n\n"
        "      Aluno:     Ana Silva\n"
        "      Nota:      87.5\n"
        "      Conceito:  B\n"
        "      Situacao:  Aprovado\n\n"
        "Teste com pelo menos 5 alunos diferentes, incluindo casos\n"
        "extremos: nota 0, nota 100, nota invalida (-5 ou 105).\n\n"
        "BONUS: use match/case para personalizar a mensagem de feedback\n"
        "de acordo com o conceito (A: 'Excelente!', B: 'Muito bom!', etc.)"
    ),
    leitura=[
        "docs.python.org/pt-br/3/tutorial/controlflow.html — controle de fluxo",
        "PEP 634 — Structural Pattern Matching (match/case)",
        "PEP 636 — Tutorial de Pattern Matching em portugues",
    ],
))
# ---------------------------------------------------------------- DIA 6
DIAS.append(Dia(
    numero=6,
    titulo="Repetição com while, break e continue",
    nivel="Iniciante",
    duracao="90 min",
    objetivos=[
        "Entender para que serve o while e quando usá-lo no lugar do for",
        "Identificar as quatro partes obrigatórias de todo laço while correto",
        "Usar break para sair de um laço e continue para pular uma iteração",
        "Construir menus e validação de entrada com o padrão while True",
        "Aplicar os padrões clássicos: acumulador, contador e sentinela",
        "Diagnosticar e evitar loops infinitos antes que eles travem o programa",
        "Usar o bloco else do while, recurso exclusivo do Python",
    ],
    teoria="""
Você já sabe tomar decisões com if/elif/else. Mas e quando você precisa
fazer a MESMA coisa várias vezes? Por exemplo: somar todos os números de
1 a 100, pedir uma senha até o usuário acertar, ou processar cada linha
de um arquivo gigante.

Para isso existem os LAÇOS (loops) — estruturas que repetem um bloco de
código enquanto uma condição for verdadeira.

Python tem dois laços principais: while (este dia) e for (Dia 7).
A diferença fundamental:

    while  ->  use quando você NÃO sabe quantas repetições vai fazer
    for    ->  use quando você JÁ SABE o que vai percorrer

---------------------------------------------------------------------------
1. A anatomia do while: quatro partes obrigatórias
---------------------------------------------------------------------------
Todo while bem escrito tem exatamente quatro partes. Se faltar qualquer
uma, o laço estará incompleto ou incorreto:

    contador = 0              # 1. INICIALIZAÇÃO: cria e configura variável
    while contador < 5:       # 2. CONDIÇÃO: testada antes de cada repetição
        print(contador)       # 3. CORPO: o que o laço faz (pode ter várias linhas)
        contador += 1         # 4. ATUALIZAÇÃO: muda a variável da condição

Como funciona passo a passo:

    Passo 1: Python avalia a condição (contador < 5)
    Passo 2: Se for True, executa o corpo
    Passo 3: Executa a atualização
    Passo 4: Volta ao Passo 1
    Passo 5: Se a condição for False, pula o bloco e continua o programa

Saída do exemplo acima:
    0
    1
    2
    3
    4

PARTE 4 É A MAIS CRÍTICA: esquecer a atualização é a causa número 1 de
loops infinitos. Se contador nunca muda, contador < 5 nunca vira False,
e o programa trava para sempre. Se isso acontecer, use Ctrl+C no terminal
para interromper manualmente.

---------------------------------------------------------------------------
2. Loop infinito: como acontece e como evitar
---------------------------------------------------------------------------
Um loop infinito ocorre quando a condição do while NUNCA se torna False.
As causas mais comuns:

CAUSA 1 — Esquecer a atualização:

    # ERRADO: contador nunca muda, loop infinito!
    contador = 0
    while contador < 5:
        print(contador)
        # faltou: contador += 1

CAUSA 2 — Atualização no lugar errado:

    # ERRADO: a atualização está fora do bloco
    contador = 0
    while contador < 5:
        print(contador)
    contador += 1   # sem indentação: só executa UMA vez, depois do loop

CAUSA 3 — Condição que nunca pode ser falsa:

    # ERRADO: n começa par e aumenta de 2 em 2, nunca chega em 7
    n = 0
    while n != 7:    # perigoso! use < em vez de !=
        n += 2

    # CORRETO: use < para garantir que o loop sempre termina
    n = 0
    while n < 7:
        n += 2

DICA: sempre prefira < ou <= a != quando o passo pode "pular" o valor
exato de parada.

---------------------------------------------------------------------------
3. break: saindo do laço antes da hora
---------------------------------------------------------------------------
break interrompe o laço IMEDIATAMENTE, independente da condição. A
execução continua na primeira linha APÓS o bloco while:

    numero = 1
    while numero <= 10:
        if numero == 5:
            break            # sai do loop quando numero chega em 5
        print(numero)
        numero += 1
    print("loop encerrado")

    # Saída: 1  2  3  4  loop encerrado

break só afeta o laço mais INTERNO. Se você tiver um while dentro de
outro while, o break sai apenas do while mais próximo.

O PADRÃO while True + break:
Uma combinação muito usada em Python para situações onde a condição de
parada só pode ser verificada DENTRO do loop:

    while True:                          # loop "infinito" controlado por dentro
        entrada = input("Senha: ")
        if entrada == "python123":
            print("Acesso liberado!")
            break                        # sai quando acertar
        print("Senha incorreta, tente novamente.")

Este padrão é especialmente útil para menus e validação de entrada, onde
você precisa rodar pelo menos uma vez antes de saber se deve continuar.

---------------------------------------------------------------------------
4. continue: pulando uma iteração
---------------------------------------------------------------------------
continue pula o RESTANTE do corpo do laço na iteração atual e volta
direto para a avaliação da condição:

    numero = 0
    while numero < 10:
        numero += 1
        if numero % 2 == 0:
            continue         # pula o print para números pares
        print(numero)        # só executa para ímpares

    # Saída: 1  3  5  7  9

continue é útil para evitar aninhamento excessivo. Compare:

    # Com aninhamento (menos claro)
    while condicao:
        if item_valido:
            processar(item)

    # Com continue (mais claro)
    while condicao:
        if not item_valido:
            continue
        processar(item)    # código principal sem aninhamento

---------------------------------------------------------------------------
5. Padrões clássicos de laço
---------------------------------------------------------------------------
Existem três padrões que aparecem repetidamente em problemas com while.
Reconhecê-los ajuda a escrever o código mais rápido:

PADRÃO 1 — ACUMULADOR: acumula um valor progressivamente

    # Soma de 1 a 100
    soma = 0          # inicializa o acumulador com identidade da operação
    i = 1
    while i <= 100:
        soma += i     # acumula
        i += 1
    print(soma)       # 5050

    # Para multiplicação, o acumulador começa em 1 (não em 0!)
    produto = 1
    while ...:
        produto *= valor

PADRÃO 2 — CONTADOR: conta quantas vezes algo acontece

    pares = 0
    i = 1
    while i <= 20:
        if i % 2 == 0:
            pares += 1    # incrementa o contador
        i += 1
    print(pares)          # 10

PADRÃO 3 — SENTINELA: repete até receber um valor especial de parada

    total = 0
    while True:
        entrada = input("Valor (0 para sair): ")
        valor = float(entrada)
        if valor == 0:
            break          # 0 é o sentinela: sinaliza "parei"
        total += valor
    print("Total:", total)

---------------------------------------------------------------------------
6. Decompondo com while: reduzindo um número
---------------------------------------------------------------------------
O while é perfeito para problemas onde você processa um número
repetidamente até esgotá-lo. Por exemplo, contar os dígitos de um número:

    n = 12345
    digitos = 0
    while n > 0:
        n //= 10       # remove o último dígito (12345 -> 1234 -> ... -> 0)
        digitos += 1
    print(digitos)     # 5

Caso especial: se n começa em 0, o loop não executa e o resultado seria 0,
mas 0 tem 1 dígito. Trate com cláusula de guarda antes do loop:

    if n == 0:
        return 1

---------------------------------------------------------------------------
7. O bloco else do while: recurso exclusivo do Python
---------------------------------------------------------------------------
Python permite um bloco else depois de um while. Ele executa quando o
laço termina NORMALMENTE — ou seja, quando a condição ficou False
por conta própria, sem um break ter interrompido:

    n = 91
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            print(f"{n} nao e primo (divisivel por {divisor})")
            break
        divisor += 1
    else:
        print(f"{n} e primo!")    # so executa se o break nao ocorreu

A forma mais fácil de ler: pense no else como "senão nenhum break
ocorreu". É o complemento lógico do break, útil em buscas onde você
quer executar algo apenas quando a busca inteira falhou.

---------------------------------------------------------------------------
8. Boas práticas com while
---------------------------------------------------------------------------
    - Sempre garanta que a variável da condição MUDA dentro do loop
    - Prefira < ou <= a != quando possível
    - Use while True + break para menus e validação
    - Use continue para evitar aninhamento (cláusula de guarda no loop)
    - Teste casos extremos: e se o loop não rodar nenhuma vez?
    - No corretor deste curso, um loop que não termina em 12 segundos
      é detectado como loop infinito e interrompido automaticamente
""",
    exemplos=[
        Exemplo(
            titulo="Os três padrões clássicos em ação",
            codigo='''# PADRAO 1: Acumulador — calcula a soma dos quadrados
soma = 0
i = 1
while i <= 5:
    soma += i ** 2    # 1 + 4 + 9 + 16 + 25
    i += 1
print("Soma dos quadrados de 1 a 5:", soma)   # 55

# PADRAO 2: Contador — conta quantos numeros sao pares
pares = 0
i = 1
while i <= 20:
    if i % 2 == 0:
        pares += 1
    i += 1
print("Pares de 1 a 20:", pares)    # 10

# PADRAO 3: Sentinela — Sequencia de Fibonacci ate 100
a, b = 0, 1
print("Fibonacci ate 100:", end=" ")
while a <= 100:
    print(a, end=" ")
    a, b = b, a + b
print()    # quebra de linha no final
''',
            explicacao="No acumulador, a variável soma começa em 0 "
                       "(elemento neutro da adição). "
                       "No contador, pares só incrementa quando a condição "
                       "é satisfeita. "
                       "No Fibonacci, a troca 'a, b = b, a + b' é simultânea: "
                       "Python avalia o lado direito completamente antes "
                       "de fazer qualquer atribuição.",
        ),
        Exemplo(
            titulo="while True + break para validação de entrada",
            codigo='''# Simula validacao de entrada sem usar input() de verdade
# (input() nao funciona no corretor automatico)
entradas = ["abc", "-5", "0", "150", "42"]  # simula o que o usuario digitaria
indice = 0

while True:
    entrada = entradas[indice]    # simula input()
    indice += 1
    print(f"Tentativa: '{entrada}'")

    if not entrada.isdigit():
        print("  -> Erro: nao e um numero inteiro positivo")
        continue

    numero = int(entrada)
    if numero <= 0:
        print("  -> Erro: precisa ser maior que zero")
        continue

    if numero > 100:
        print("  -> Erro: precisa ser no maximo 100")
        continue

    print(f"  -> Aceito! numero = {numero}")
    break

print(f"Numero valido recebido: {numero}")
''',
            explicacao="O padrão while True + continue + break é perfeito "
                       "para validação: cada continue rejeita uma condição "
                       "inválida, e o break só executa quando todas as "
                       "validações passaram. O código principal (break) "
                       "fica sempre no final, sem aninhamento.",
        ),
        Exemplo(
            titulo="else do while: verificando primo",
            codigo='''def verificar_primo(n):
    """Verifica se n e primo usando while com else."""
    if n < 2:
        return f"{n} nao e primo (menor que 2)"

    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return f"{n} nao e primo (divisivel por {divisor})"
        divisor += 1
    else:
        # So chega aqui se o while terminou SEM break
        return f"{n} e primo!"

for numero in [1, 2, 7, 15, 97, 100]:
    print(verificar_primo(numero))
''',
            explicacao="O else do while executa apenas se o loop terminou "
                       "naturalmente (condição virou False), nunca se um "
                       "break interrompeu. Aqui: se nenhum divisor foi "
                       "encontrado até sqrt(n), o número é primo. "
                       "Verificar apenas até sqrt(n) é uma otimização "
                       "clássica: se n tem um divisor maior que sqrt(n), "
                       "o par correspondente seria menor que sqrt(n).",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d06e1",
            enunciado=(
                "Escreva a funcao soma_ate(n) que calcula a soma de todos\n"
                "os inteiros de 1 ate n usando while.\n\n"
                "Exemplos:\n"
                "   soma_ate(5)   -> 15   (1+2+3+4+5)\n"
                "   soma_ate(1)   -> 1\n"
                "   soma_ate(0)   -> 0    (sem numeros para somar)\n"
                "   soma_ate(100) -> 5050\n\n"
                "Estrategia (padrao acumulador):\n"
                "   1. Crie uma variavel 'total' comecarando em 0\n"
                "   2. Crie uma variavel 'i' comecando em 1\n"
                "   3. while i <= n: adicione i ao total e incremente i\n"
                "   4. Devolva total\n\n"
                "Caso especial: se n <= 0, o while nao executa nenhuma vez\n"
                "e total permanece 0 — exatamente o resultado esperado."
            ),
            funcao="soma_ate",
            assinatura="def soma_ate(n):",
            testes=[
                ("soma_ate(5)", "15"),
                ("soma_ate(1)", "1"),
                ("soma_ate(0)", "0"),
                ("soma_ate(100)", "5050"),
            ],
            dica="Padrao acumulador: total = 0; i = 1; while i <= n: total += i; i += 1",
        ),
        Exercicio(
            id="d06e2",
            enunciado=(
                "Escreva a funcao contar_digitos(n) que devolve quantos\n"
                "digitos tem um numero inteiro nao negativo.\n"
                "NAO use str() — resolva so com operacoes matematicas.\n\n"
                "Exemplos:\n"
                "   contar_digitos(0)       -> 1   (zero tem 1 digito)\n"
                "   contar_digitos(7)       -> 1\n"
                "   contar_digitos(12345)   -> 5\n"
                "   contar_digitos(1000000) -> 7\n\n"
                "Estrategia:\n"
                "   1. Trate o caso especial: se n == 0, devolva 1\n"
                "   2. Comece com contador = 0\n"
                "   3. while n > 0: divida n por 10 com //= e incremente contador\n"
                "      12345 // 10 = 1234  (removeu o ultimo digito)\n"
                "      1234  // 10 = 123\n"
                "      123   // 10 = 12\n"
                "      12    // 10 = 1\n"
                "      1     // 10 = 0     (loop para aqui)\n"
                "   4. Contador vai chegar em 5 para 12345"
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
            dica="if n == 0: return 1. Depois: while n > 0: n //= 10; contador += 1",
        ),
        Exercicio(
            id="d06e3",
            enunciado=(
                "A Conjectura de Collatz diz que, partindo de qualquer inteiro\n"
                "positivo n, se voce aplicar as regras abaixo repetidamente,\n"
                "sempre chegara em 1:\n\n"
                "   Se n for PAR:   n = n / 2\n"
                "   Se n for IMPAR: n = n * 3 + 1\n\n"
                "Escreva passos_collatz(n) que conta quantos passos sao\n"
                "necessarios para n chegar em 1.\n\n"
                "Exemplos:\n"
                "   passos_collatz(1)  -> 0   (ja comecou em 1)\n"
                "   passos_collatz(2)  -> 1   (2 -> 1)\n"
                "   passos_collatz(6)  -> 8   (6->3->10->5->16->8->4->2->1)\n"
                "   passos_collatz(27) -> 111\n\n"
                "Estrategia:\n"
                "   contador = 0\n"
                "   while n != 1:\n"
                "       se n for par: n = n // 2\n"
                "       senao:        n = n * 3 + 1\n"
                "       contador += 1\n"
                "   return contador"
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
            dica="while n != 1: aplique a regra (par: n//=2, impar: n=n*3+1) e incremente o contador.",
        ),
    ],
    quiz=[
        Quiz(
            "Qual das quatro partes do while e a mais critica para evitar loop infinito?",
            ["A inicializacao da variavel",
             "A condicao de parada",
             "A atualizacao da variavel dentro do loop",
             "O corpo do loop"],
            2,
            "Sem a atualizacao, a variavel da condicao nunca muda, "
            "a condicao nunca vira False e o loop nunca termina. "
            "Inicializacao, condicao e corpo podem estar corretos "
            "e o loop ainda travar se faltar a atualizacao.",
        ),
        Quiz(
            "Qual a diferenca entre break e continue?",
            ["break pula uma iteracao; continue encerra o loop",
             "break encerra o loop completamente; continue pula para a proxima iteracao",
             "Sao sinonimos — fazem a mesma coisa",
             "break so funciona com while; continue so funciona com for"],
            1,
            "break = sai do loop (execucao vai para apos o while). "
            "continue = pula o restante do corpo desta iteracao e volta "
            "para a verificacao da condicao, comecando a proxima volta.",
        ),
        Quiz(
            "Quando o bloco else de um while executa?",
            ["Sempre, apos o loop terminar",
             "Quando o loop nao executa nenhuma vez",
             "Apenas quando a condicao era False desde o inicio",
             "Quando o loop termina naturalmente, sem break ter interrompido"],
            3,
            "else do while executa se e somente se a condicao ficou False "
            "por conta propria. Se um break interrompeu o loop, "
            "o else e pulado. Pense: 'nao houve break = else executa'.",
        ),
        Quiz(
            "Por que 'while n != 7' pode ser perigoso se n aumenta de 2 em 2?",
            ["!= e mais lento que <",
             "Se n comecar par, nunca chegara exatamente em 7 e o loop nunca termina",
             "while so aceita comparacoes com <",
             "n aumentar de 2 em 2 e invalido em Python"],
            1,
            "Se n comecar em 0 e aumentar de 2 em 2 (0, 2, 4, 6, 8...), "
            "nunca passara pelo valor 7 exato. != 7 nunca sera False. "
            "Use n < 7 ou n <= 6 para garantir que o loop sempre termina.",
        ),
    ],
    projeto=(
        "Crie jogo_adivinha.py com o seguinte desafio:\n\n"
        "1. Sorteie um numero secreto entre 1 e 100:\n"
        "      import random\n"
        "      secreto = random.randint(1, 100)\n\n"
        "2. Use while True para o loop principal do jogo\n\n"
        "3. Leia um palpite com input() e trate erros:\n"
        "   - Se nao for numero: print erro e continue\n"
        "   - Se for < 1 ou > 100: print erro e continue\n\n"
        "4. Dê dicas: 'muito baixo', 'muito alto' ou 'acertou!'\n\n"
        "5. Ao acertar, mostre quantas tentativas foram necessarias\n"
        "   e use else do while para uma mensagem especial se acertar\n"
        "   com menos de 7 tentativas\n\n"
        "BONUS: implemente um modo automatico que testa o jogo com\n"
        "uma estrategia de busca binaria (sempre chuta o meio do intervalo)\n"
        "e mostra em quantos passos ela resolve — compare com o maximo\n"
        "teorico de 7 tentativas para 100 numeros."
    ),
    leitura=[
        "docs.python.org/pt-br/3/tutorial/controlflow.html — controle de fluxo",
        "docs.python.org/pt-br/3/reference/compound_stmts.html#the-while-statement",
    ],
))
# ---------------------------------------------------------------- DIA 7
DIAS.append(Dia(
    numero=7,
    titulo="for, range, enumerate e zip",
    nivel="Iniciante",
    duracao="90 min",
    objetivos=[
        "Entender o for como um 'para cada' e por que ele é diferente do for de C ou Java",
        "Usar range com um, dois e três argumentos, e entender por que ele é preguiçoso",
        "Obter índice e valor ao mesmo tempo com enumerate, sem gerenciar contador manualmente",
        "Percorrer duas listas em paralelo com zip e entender o que acontece com tamanhos diferentes",
        "Usar break e continue dentro do for da mesma forma que no while",
        "Conhecer as funções que já iteram por você: sum, max, min, any, all, sorted",
        "Evitar o erro clássico de modificar uma lista enquanto a percorre",
    ],
    teoria="""
No Dia 6 você aprendeu o while, que repete enquanto uma condição for
verdadeira. Hoje vamos conhecer o for, que é o laço mais usado em Python
no dia a dia — e que funciona de forma completamente diferente.

---------------------------------------------------------------------------
1. O for é um "para cada", não um contador
---------------------------------------------------------------------------
Se você já programou em C, Java ou JavaScript, provavelmente conhece o
for assim:

    // Java/C
    for (int i = 0; i < 5; i++) {
        System.out.println(i);
    }

O for do Python funciona de outra forma: em vez de gerenciar um contador
manualmente, ele PERCORRE DIRETAMENTE os elementos de uma sequência,
entregando um de cada vez:

    for elemento in sequencia:
        # use o elemento aqui

Exemplos com diferentes tipos de sequência:

    for letra in "Python":
        print(letra)           # P  y  t  h  o  n  (um por linha)

    for numero in [10, 20, 30]:
        print(numero)          # 10  20  30

    for fruta in ("maçã", "banana", "uva"):
        print(fruta)           # maçã  banana  uva

Esse estilo é chamado de "for-each" em outras linguagens. A filosofia é:
diga O QUE você quer percorrer, não COMO percorrer. Python cuida dos
detalhes internos.

Usar a variável de loop com um nome descritivo torna o código muito mais
legível:

    for produto in lista_produtos:    # claro: o que é cada elemento
    for i in lista_produtos:          # confuso: i sugere índice, não produto

---------------------------------------------------------------------------
2. range(): gerando sequências de números
---------------------------------------------------------------------------
Quando você precisa repetir algo um número específico de vezes, ou
percorrer uma sequência de números, use range():

    Forma              Gera                           Exemplo
    ---------------    ----------------------------   -------------------
    range(n)           0, 1, 2, ..., n-1              range(5) -> 0,1,2,3,4
    range(a, b)        a, a+1, ..., b-1               range(2,6) -> 2,3,4,5
    range(a, b, p)     a, a+p, a+2p, ... ate b        range(0,10,2) -> 0,2,4,6,8
    range(a, b, -1)    a, a-1, ..., b+1               range(5,0,-1) -> 5,4,3,2,1

Exemplos práticos:

    # Repetir 3 vezes (quando o índice não importa)
    for _ in range(3):
        print("olá")            # _ é convencão para "variável que não uso"

    # Números de 1 a 10
    for i in range(1, 11):
        print(i)

    # Números pares de 0 a 18
    for par in range(0, 20, 2):
        print(par)

    # Contagem regressiva
    for i in range(10, 0, -1):
        print(i)
    print("Fogo!")

RANGE É PREGUIÇOSO (lazy):
range() NÃO cria uma lista com todos os números na memória. Ele sabe
apenas onde começa, onde termina e o passo. Os números são gerados um
por um, conforme necessário. Por isso range(1_000_000) não ocupa memória
de 1 milhão de inteiros — ocupa quase nada.

    import sys
    print(sys.getsizeof(range(1_000_000)))   # ~48 bytes, independente do tamanho!
    print(sys.getsizeof(list(range(1_000_000))))  # ~8 MB

Se você precisar de uma lista de verdade, converta explicitamente:

    lista = list(range(5))    # [0, 1, 2, 3, 4]

---------------------------------------------------------------------------
3. enumerate(): índice e valor juntos
---------------------------------------------------------------------------
Uma situação muito comum: você está percorrendo uma lista mas também
precisa saber a posição (índice) de cada elemento.

A forma ingênua (estilo C, evite em Python):

    frutas = ["maçã", "banana", "uva"]
    i = 0
    for fruta in frutas:
        print(i, fruta)
        i += 1

A forma Pythônica com enumerate():

    for i, fruta in enumerate(frutas):
        print(i, fruta)

Saída de ambas:
    0 maçã
    1 banana
    2 uva

enumerate() devolve pares (índice, valor). O desempacotamento direto
no for (i, fruta) extrai os dois de uma vez — muito mais elegante e
menos propenso a erros.

COMEÇANDO DO 1 EM VEZ DO 0:
enumerate() aceita um parâmetro start para controlar de onde a contagem
começa:

    for numero, fruta in enumerate(frutas, start=1):
        print(f"{numero}. {fruta}")

    # 1. maçã
    # 2. banana
    # 3. uva

Isso é especialmente útil para listas exibidas ao usuário, que espera
numeração começando em 1, não em 0.

---------------------------------------------------------------------------
4. zip(): percorrendo duas listas em paralelo
---------------------------------------------------------------------------
zip() combina duas (ou mais) sequências, produzindo pares com um elemento
de cada:

    nomes = ["Ana", "Bruno", "Carla"]
    notas = [9.5, 7.0, 8.5]

    for nome, nota in zip(nomes, notas):
        print(f"{nome}: {nota}")

    # Ana: 9.5
    # Bruno: 7.0
    # Carla: 8.5

Sem zip(), você precisaria de range(len(...)) e indexação manual — mais
verboso e mais sujeito a erro de índice.

O QUE ACONTECE COM TAMANHOS DIFERENTES:
zip() para quando a sequência MAIS CURTA se esgota. Os elementos extras
da sequência mais longa são silenciosamente ignorados:

    nomes = ["Ana", "Bruno", "Carla", "Daniel"]
    notas = [9.5, 7.0]    # só duas notas

    for nome, nota in zip(nomes, notas):
        print(nome, nota)

    # Ana: 9.5
    # Bruno: 7.0
    # Carla e Daniel: ignorados sem aviso!

Se as listas deveriam ter o mesmo tamanho e isso é obrigatório, use
zip(a, b, strict=True) (Python 3.10+) para receber um erro explícito
se os tamanhos diferirem.

MONTANDO UM DICIONÁRIO COM ZIP:
zip() combinado com dict() é uma forma elegante de criar dicionários
a partir de duas listas paralelas:

    chaves = ["nome", "idade", "cidade"]
    valores = ["Ana", 30, "Recife"]
    pessoa = dict(zip(chaves, valores))
    # {'nome': 'Ana', 'idade': 30, 'cidade': 'Recife'}

---------------------------------------------------------------------------
5. Desempacotamento no for
---------------------------------------------------------------------------
Quando os elementos da sequência já são tuplas ou listas, o for pode
desempacotá-los diretamente:

    pontos = [(1, 2), (3, 4), (5, 6)]

    # Sem desempacotamento (menos claro)
    for ponto in pontos:
        print(ponto[0], ponto[1])

    # Com desempacotamento (mais claro)
    for x, y in pontos:
        print(x, y)

Com o operador estrela (*) você pode capturar "o resto":

    primeiro, *meio, ultimo = [1, 2, 3, 4, 5]
    # primeiro = 1, meio = [2, 3, 4], ultimo = 5

---------------------------------------------------------------------------
6. break e continue funcionam igualmente no for
---------------------------------------------------------------------------
break e continue (aprendidos no Dia 6) funcionam da mesma forma no for:

    # Busca: para no primeiro par encontrado
    numeros = [3, 7, 4, 9, 2, 8]
    for n in numeros:
        if n % 2 == 0:
            print(f"Primeiro par: {n}")
            break            # sai do for

    # Pula os negativos, processa só os positivos
    valores = [1, -3, 5, -2, 8]
    for v in valores:
        if v < 0:
            continue         # pula para o próximo
        print(v)             # 1  5  8

O for também tem o bloco else (igual ao while): executa se o loop
terminou sem break:

    for n in numeros:
        if n > 100:
            print("encontrou maior que 100")
            break
    else:
        print("nenhum maior que 100 encontrado")

---------------------------------------------------------------------------
7. Funções que iteram por você
---------------------------------------------------------------------------
Antes de escrever um for para calcular algo, verifique se já existe uma
função embutida que faz isso:

    Função          O que faz                        Exemplo
    ------------    --------------------------------  ----------------------
    sum(seq)        soma todos os elementos           sum([1,2,3]) -> 6
    max(seq)        devolve o maior                   max([3,1,4]) -> 4
    min(seq)        devolve o menor                   min([3,1,4]) -> 1
    len(seq)        conta os elementos                len([1,2,3]) -> 3
    sorted(seq)     devolve lista ordenada            sorted([3,1,2]) -> [1,2,3]
    reversed(seq)   percorre ao contrário             list(reversed([1,2,3])) -> [3,2,1]
    any(seq)        True se algum for truthy          any([0,0,1]) -> True
    all(seq)        True se todos forem truthy        all([1,2,3]) -> True

any() e all() têm curto-circuito — param assim que o resultado é certo:

    # any: para no primeiro True
    any(n > 10 for n in numeros)

    # all: para no primeiro False
    all(n > 0 for n in numeros)

---------------------------------------------------------------------------
8. NUNCA modifique uma lista enquanto a percorre
---------------------------------------------------------------------------
Este é um erro clássico e sutil que pode pular elementos sem aviso:

    numeros = [1, 2, 3, 4, 5, 6]

    # ERRADO: modifica a lista enquanto percorre
    for n in numeros:
        if n % 2 == 0:
            numeros.remove(n)    # comportamento imprevisível!
    print(numeros)    # [1, 3, 5] — parece certo, mas é sorte!
                      # com outros dados, pode pular elementos

O que acontece: quando você remove um elemento, todos os seguintes
"deslizam" uma posição para trás. O for avança normalmente, mas agora
aponta para o elemento errado — pulando um.

A forma correta é iterar sobre uma CÓPIA:

    # CORRETO: percorre a cópia, modifica o original
    for n in numeros[:]:          # numeros[:] cria uma cópia
        if n % 2 == 0:
            numeros.remove(n)
    print(numeros)    # [1, 3, 5] — sempre correto

Ou melhor ainda: construa uma nova lista com os elementos que quer manter:

    # MAIS PYTHONICO: filtragem direta
    numeros = [n for n in numeros if n % 2 != 0]
    print(numeros)    # [1, 3, 5]

(Compreensões de lista são o tema do Dia 10 — por ora, apenas
reconheça que essa forma existe e é preferida.)
""",
    exemplos=[
        Exemplo(
            titulo="range() em todas as suas formas",
            codigo='''# range com um argumento: 0 ate n-1
print("range(5):", list(range(5)))        # [0, 1, 2, 3, 4]

# range com dois argumentos: inicio ate fim-1
print("range(2,8):", list(range(2, 8)))   # [2, 3, 4, 5, 6, 7]

# range com tres argumentos: inicio, fim, passo
print("pares:", list(range(0, 11, 2)))    # [0, 2, 4, 6, 8, 10]
print("impares:", list(range(1, 11, 2)))  # [1, 3, 5, 7, 9]
print("regressiva:", list(range(5, 0, -1))) # [5, 4, 3, 2, 1]

# Uso pratico: tabuada do 7
print("\nTabuada do 7:")
for i in range(1, 11):
    print(f"7 x {i:2} = {7*i:2}")

# _ quando o indice nao importa
print("\nContagem regressiva:")
for _ in range(3, 0, -1):
    print(_)
print("Vai!")
''',
            explicacao="list(range(...)) materializa a sequência para exibição, "
                       "mas em loops você nunca precisa de list() — o for "
                       "consome range diretamente, sem criar lista na memória. "
                       "O _ é convenção para 'variável que não vou usar'.",
        ),
        Exemplo(
            titulo="enumerate e zip no mundo real",
            codigo='''alunos = ["Ana", "Bruno", "Carla", "Diego"]
notas = [9.5, 6.0, 8.2, 7.8]

# Boletim com enumerate + zip juntos
print(f"{'Pos':<4} {'Nome':<10} {'Nota':>6} {'Situacao'}")
print("-" * 34)

for pos, (nome, nota) in enumerate(
        sorted(zip(alunos, notas), key=lambda p: -p[1]),
        start=1):
    situacao = "Aprovado" if nota >= 6 else "Reprovado"
    print(f"{pos:<4} {nome:<10} {nota:>6.1f} {situacao}")

print("-" * 34)
print(f"Media da turma: {sum(notas)/len(notas):.2f}")
print(f"Todos aprovados: {all(n >= 6 for n in notas)}")
''',
            explicacao="zip une as duas listas em pares. sorted ordena "
                       "pelo segundo elemento do par (nota) em ordem "
                       "decrescente (o - inverte). enumerate numera os "
                       "resultados já ordenados. O desempacotamento "
                       "(pos, (nome, nota)) extrai os três valores de vez.",
        ),
        Exemplo(
            titulo="Buscas com for + break + else",
            codigo='''def buscar(lista, alvo):
    """Busca linear: encontra o indice de alvo ou -1 se nao existir."""
    for i, elemento in enumerate(lista):
        if elemento == alvo:
            return i    # achou: retorna o indice
    return -1           # nao achou

numeros = [15, 3, 42, 8, 7, 19]
print(buscar(numeros, 42))   # 2
print(buscar(numeros, 99))   # -1

# Usando for + else para verificar se existe primo na lista
def tem_primo(numeros):
    for n in numeros:
        if n < 2:
            continue
        for d in range(2, int(n**0.5) + 1):
            if n % d == 0:
                break
        else:
            return True    # o for interno terminou sem break = n e primo
    return False

print(tem_primo([4, 6, 8, 7]))   # True  (7 e primo)
print(tem_primo([4, 6, 8, 9]))   # False
''',
            explicacao="O else do for interno dispara apenas se nenhum "
                       "divisor foi encontrado (ou seja, n é primo). "
                       "O break do for interno só afeta o for interno — "
                       "o for externo continua normalmente. "
                       "Esse padrão de for aninhado com else é clássico "
                       "para verificação de primalidade.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d07e1",
            enunciado=(
                "Escreva a funcao tabuada(n) que devolve uma LISTA com\n"
                "os dez primeiros multiplos de n: n*1, n*2, ..., n*10.\n\n"
                "Exemplos:\n"
                "   tabuada(3) -> [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]\n"
                "   tabuada(0) -> [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]\n"
                "   len(tabuada(7)) -> 10  (sempre 10 elementos)\n\n"
                "Estrategia:\n"
                "   1. Crie uma lista vazia: resultado = []\n"
                "   2. for i in range(1, 11):  (de 1 a 10 inclusive)\n"
                "   3. resultado.append(n * i)\n"
                "   4. return resultado\n\n"
                "Lembre: range(1, 11) gera 1, 2, 3, ..., 10\n"
                "(o 11 e exclusivo — nao entra na sequencia)"
            ),
            funcao="tabuada",
            assinatura="def tabuada(n):",
            testes=[
                ("tabuada(3)", "[3, 6, 9, 12, 15, 18, 21, 24, 27, 30]"),
                ("tabuada(0)", "[0]*10"),
                ("len(tabuada(7))", "10"),
            ],
            dica="resultado = []; for i in range(1, 11): resultado.append(n * i); return resultado",
        ),
        Exercicio(
            id="d07e2",
            enunciado=(
                "Escreva a funcao indices_de(lista, alvo) que devolve uma\n"
                "LISTA com todas as posicoes em que 'alvo' aparece em 'lista'.\n"
                "Se 'alvo' nao aparecer, devolve uma lista vazia.\n\n"
                "Exemplos:\n"
                "   indices_de([1, 2, 1, 3, 1], 1) -> [0, 2, 4]\n"
                "   indices_de(['a', 'b'], 'z')     -> []\n"
                "   indices_de([5], 5)              -> [0]\n\n"
                "Estrategia: use enumerate() para obter indice e valor\n"
                "ao mesmo tempo, sem precisar de um contador manual:\n\n"
                "   for indice, valor in enumerate(lista):\n"
                "       if valor == alvo:\n"
                "           posicoes.append(indice)"
            ),
            funcao="indices_de",
            assinatura="def indices_de(lista, alvo):",
            testes=[
                ("indices_de([1, 2, 1, 3, 1], 1)", "[0, 2, 4]"),
                ("indices_de(['a', 'b'], 'z')", "[]"),
                ("indices_de([5], 5)", "[0]"),
            ],
            dica="posicoes = []; for i, v in enumerate(lista): if v == alvo: posicoes.append(i); return posicoes",
        ),
        Exercicio(
            id="d07e3",
            enunciado=(
                "Escreva a funcao produto_escalar(a, b) que calcula o\n"
                "produto escalar de dois vetores representados como listas.\n\n"
                "O produto escalar e a soma dos produtos de cada par:\n"
                "   [1,2,3] . [4,5,6] = 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32\n\n"
                "Exemplos:\n"
                "   produto_escalar([1, 2, 3], [4, 5, 6]) -> 32\n"
                "   produto_escalar([], [])                -> 0\n"
                "   produto_escalar([2], [10])             -> 20\n\n"
                "Estrategia: use zip(a, b) para percorrer os pares\n"
                "correspondentes das duas listas ao mesmo tempo:\n\n"
                "   for x, y in zip(a, b):\n"
                "       total += x * y\n\n"
                "zip(a, b) produz: (1,4), (2,5), (3,6) para os exemplos acima"
            ),
            funcao="produto_escalar",
            assinatura="def produto_escalar(a, b):",
            testes=[
                ("produto_escalar([1, 2, 3], [4, 5, 6])", "32"),
                ("produto_escalar([], [])", "0"),
                ("produto_escalar([2], [10])", "20"),
            ],
            nivel="medio",
            dica="total = 0; for x, y in zip(a, b): total += x * y; return total",
        ),
    ],
    quiz=[
        Quiz(
            "O que range(5, 0, -1) produz?",
            ["[5, 4, 3, 2, 1, 0]  — de 5 ate 0 inclusive",
             "[5, 4, 3, 2, 1]     — de 5 ate 1 (0 e exclusivo)",
             "[0, 1, 2, 3, 4]     — range nao aceita passo negativo",
             "[]                  — range vazio"],
            1,
            "O segundo argumento e SEMPRE exclusivo, mesmo com passo negativo. "
            "range(5, 0, -1) vai de 5 descendo ate 1, parando antes de chegar em 0. "
            "Para incluir o 0: range(5, -1, -1).",
        ),
        Quiz(
            "Qual a vantagem de enumerate() sobre gerenciar um indice manualmente?",
            ["enumerate() e mais rapido de executar",
             "Elimina a necessidade de criar e incrementar uma variavel contadora separada, reduzindo o risco de erro",
             "enumerate() so funciona com listas, nao com tuplas",
             "Nao ha vantagem real — sao equivalentes em todos os aspectos"],
            1,
            "Sem enumerate: i = 0; for x in lista: usar i; i += 1. "
            "Com enumerate: for i, x in enumerate(lista): usar i e x. "
            "Menos codigo, menos chance de esquecer de incrementar i ou "
            "inicializá-lo com o valor errado.",
        ),
        Quiz(
            "O que acontece se as listas passadas para zip() tiverem tamanhos diferentes?",
            ["Levanta IndexError apontando o elemento faltante",
             "Preenche os espacos vazios com None",
             "Para silenciosamente quando a lista mais curta se esgota",
             "Sempre usa o tamanho da lista mais longa"],
            2,
            "zip() para na lista mais curta, ignorando os elementos extras "
            "da mais longa sem qualquer aviso. Para detectar isso como erro, "
            "use zip(a, b, strict=True) no Python 3.10+.",
        ),
        Quiz(
            "Por que modificar uma lista enquanto a percorre com for pode pular elementos?",
            ["O for nao permite modificacoes — sempre levanta um erro",
             "Ao remover um elemento, os seguintes deslocam para traz e o for avanca normalmente, pulando um",
             "O Python reordena a lista automaticamente durante o loop",
             "So ocorre com listas numericas, nao com listas de texto"],
            1,
            "Imagine a lista [1, 2, 3, 4]. O for aponta para posicao 0 (valor 1). "
            "Voce remove 1. A lista vira [2, 3, 4]. O for avanca para posicao 1 (valor 3). "
            "O 2 foi pulado! Solucao: percorra uma copia (lista[:]) ou crie uma lista nova.",
        ),
    ],
    projeto=(
        "Crie analise_turma.py com dados de uma turma ficticia:\n\n"
        "   alunos = ['Ana', 'Bruno', 'Carla', 'Diego', 'Elena']\n"
        "   notas =  [9.5, 6.0, 4.5, 8.2, 7.8]\n\n"
        "Usando for, enumerate, zip e as funcoes embutidas, exiba:\n\n"
        "   1. Lista numerada de alunos com nota (enumerate, start=1)\n"
        "   2. Situacao de cada aluno: Aprovado (>= 6) ou Reprovado\n"
        "   3. Media da turma (sum / len)\n"
        "   4. Maior e menor nota com o nome do aluno correspondente\n"
        "   5. Quantos foram aprovados (use sum() com condicao)\n"
        "   6. Se TODOS foram aprovados (all())\n"
        "   7. Se ALGUM tirou 10 (any())\n"
        "   8. Ranking do melhor para o pior (sorted com zip)\n\n"
        "BONUS: repita a analise para uma segunda turma e compare\n"
        "as medias das duas usando uma terceira lista de alunos e notas."
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/functions.html — funcoes embutidas (sum, any, all...)",
        "docs.python.org/pt-br/3/library/stdtypes.html#range — tipo range",
        "docs.python.org/pt-br/3/tutorial/controlflow.html#for-statements",
    ],
))
# ---------------------------------------------------------------- DIA 8
DIAS.append(Dia(
    numero=8,
    titulo="Listas e tuplas",
    nivel="Iniciante",
    duracao="100 min",
    objetivos=[
        "Criar e manipular listas com os métodos que modificam no lugar e os que consultam",
        "Entender a diferença entre alias, cópia rasa e cópia profunda, e quando cada uma importa",
        "Ordenar listas com sort() e sorted() usando chaves personalizadas",
        "Evitar a armadilha clássica do atributo de lista compartilhado entre objetos",
        "Saber quando usar tupla em vez de lista, e quais são as vantagens de cada uma",
        "Entender o custo de desempenho das operações mais comuns de lista",
    ],
    teoria="""
Nos dias anteriores você usou listas em vários exemplos. Hoje vamos
entendê-las a fundo: como funcionam por dentro, quais operações existem,
quando elas custam tempo e quando custam memória, e qual a diferença para
as tuplas.

---------------------------------------------------------------------------
1. Criando e acessando listas
---------------------------------------------------------------------------
Uma lista é uma sequência MUTÁVEL e ORDENADA de elementos. Mutável
significa que você pode modificá-la depois de criada — adicionar, remover
e alterar elementos. Ordenada significa que a posição de cada elemento é
preservada e importa.

    # Criando listas
    numeros = [1, 2, 3, 4, 5]
    nomes = ["Ana", "Bruno", "Carla"]
    mista = [1, "dois", 3.0, True, None]  # Python aceita tipos mistos
    vazia = []
    aninhada = [[1, 2], [3, 4], [5, 6]]  # lista de listas (matriz)

Acesso por índice funciona igual a strings (Dia 4):

    numeros[0]      # 1    — primeiro elemento
    numeros[-1]     # 5    — último elemento
    numeros[1:3]    # [2, 3] — fatiamento (fim exclusivo)
    numeros[::2]    # [1, 3, 5] — de dois em dois

Diferente de strings, listas permitem ATRIBUIÇÃO por índice:

    numeros[0] = 10      # agora: [10, 2, 3, 4, 5]
    numeros[1:3] = [20]  # substitui dois por um: [10, 20, 4, 5]

---------------------------------------------------------------------------
2. Métodos que MODIFICAM a lista no lugar
---------------------------------------------------------------------------
Esses métodos alteram a lista original e DEVOLVEM None. O erro mais
clássico de iniciante é tentar guardar o resultado:

    lista = lista.append(4)   # ARMADILHA: lista agora vale None!

Nunca reatribua ao chamar esses métodos. Use-os como comandos, não
como expressões:

    Método                         O que faz
    --------------------------     ----------------------------------------
    lista.append(x)                adiciona x ao FINAL
    lista.extend(outra)            adiciona TODOS os elementos de outra ao final
    lista.insert(i, x)             insere x na posição i, empurra os demais
    lista.remove(x)                remove a PRIMEIRA ocorrência de x
    lista.pop()                    remove e DEVOLVE o último elemento
    lista.pop(i)                   remove e DEVOLVE o elemento na posição i
    lista.sort()                   ordena a lista no lugar
    lista.reverse()                inverte a lista no lugar
    lista.clear()                  remove todos os elementos

Exemplos:

    frutas = ["maçã", "banana"]
    frutas.append("uva")           # ["maçã", "banana", "uva"]
    frutas.insert(1, "laranja")    # ["maçã", "laranja", "banana", "uva"]
    frutas.remove("banana")        # ["maçã", "laranja", "uva"]
    retirada = frutas.pop()        # retirada = "uva", lista = ["maçã", "laranja"]
    frutas.extend(["kiwi", "pera"]) # ["maçã", "laranja", "kiwi", "pera"]

DIFERENÇA ENTRE append E extend:

    lista = [1, 2, 3]
    lista.append([4, 5])    # [1, 2, 3, [4, 5]]  — adiciona a lista como UM elemento
    lista.extend([4, 5])    # [1, 2, 3, 4, 5]    — adiciona CADA elemento

---------------------------------------------------------------------------
3. Métodos de CONSULTA (não alteram a lista)
---------------------------------------------------------------------------
    Método / Operação       O que faz
    -------------------     ------------------------------------------
    lista.index(x)          índice da primeira ocorrência de x (ValueError se não achar)
    lista.count(x)          quantas vezes x aparece
    len(lista)              quantidade de elementos
    x in lista              True se x está na lista (O(n) — percorre tudo)
    min(lista)              menor elemento
    max(lista)              maior elemento
    sum(lista)              soma (só para números)

---------------------------------------------------------------------------
4. Ordenação: sort() versus sorted()
---------------------------------------------------------------------------
Python tem dois jeitos de ordenar, com uma diferença fundamental:

    sort()     — ordena a PRÓPRIA lista no lugar, devolve None
    sorted()   — devolve uma NOVA lista ordenada, original intacta

    numeros = [3, 1, 4, 1, 5, 9]

    nova = sorted(numeros)     # nova = [1, 1, 3, 4, 5, 9], numeros intacto
    numeros.sort()             # numeros vira [1, 1, 3, 4, 5, 9], devolve None

Quando usar cada um:
    sorted() — quando você precisa preservar a lista original
    sort()   — quando pode modificar a lista e quer economizar memória

ORDENAÇÃO PERSONALIZADA com o parâmetro key:

    palavras = ["banana", "kiwi", "maçã", "abacaxi"]

    # Por tamanho
    sorted(palavras, key=len)
    # ["kiwi", "maçã", "banana", "abacaxi"]

    # Ignorando maiúsculas/minúsculas
    nomes = ["carlos", "Ana", "bruno", "Diana"]
    sorted(nomes, key=str.lower)
    # ["Ana", "bruno", "carlos", "Diana"]

    # Por um campo de uma lista de dicionários (preview do Dia 9)
    pessoas = [{"nome": "Carlos", "idade": 30}, {"nome": "Ana", "idade": 25}]
    sorted(pessoas, key=lambda p: p["idade"])
    # ordem: Ana (25), Carlos (30)

    # Ordem inversa
    sorted(numeros, reverse=True)    # do maior para o menor

ORDENAÇÃO É ESTÁVEL: elementos que empatam no critério de ordenação
mantêm a ordem relativa original. Isso permite ordenar por vários
critérios em etapas:

    # Primeiro por sobrenome, depois por nome (para empates)
    sorted(pessoas, key=lambda p: (p["sobrenome"], p["nome"]))

---------------------------------------------------------------------------
5. Cópia: alias, rasa e profunda
---------------------------------------------------------------------------
Este é o ponto que mais causa confusão e bugs em iniciantes. Existem
três formas diferentes de "copiar" uma lista:

ALIAS (não é cópia — os dois nomes apontam para o mesmo objeto):

    a = [1, 2, 3]
    b = a           # b e a são o MESMO objeto na memória

    b.append(4)
    print(a)        # [1, 2, 3, 4] — a também mudou!
    print(a is b)   # True — mesmo objeto

CÓPIA RASA (shallow copy — novo objeto, mas elementos compartilhados):

    a = [1, 2, 3]
    b = a[:]        # ou list(a), ou a.copy()

    b.append(4)
    print(a)        # [1, 2, 3] — a não mudou
    print(a is b)   # False — objetos diferentes

A cópia rasa cria um novo objeto lista, mas se a lista contiver OBJETOS
MUTÁVEIS (como outras listas), esses objetos internos ainda são
compartilhados:

    a = [[1, 2], [3, 4]]
    b = a[:]          # cópia rasa

    b[0].append(99)   # modifica o objeto interno compartilhado
    print(a)          # [[1, 2, 99], [3, 4]] — a também foi afetada!

CÓPIA PROFUNDA (deep copy — copia tudo, inclusive objetos internos):

    import copy
    a = [[1, 2], [3, 4]]
    b = copy.deepcopy(a)

    b[0].append(99)
    print(a)          # [[1, 2], [3, 4]] — a não foi afetada

REGRA PRÁTICA:
    - Listas simples (só números e strings): a[:] resolve
    - Listas de listas (matrizes): use copy.deepcopy()

---------------------------------------------------------------------------
6. A armadilha da lista compartilhada
---------------------------------------------------------------------------
Uma consequência direta do modelo de referências do Python é um bug
que pega muita gente de surpresa:

    # ERRADO: cria uma lista só e repete a REFERÊNCIA a ela
    matriz_errada = [[0] * 3] * 3
    matriz_errada[0][0] = 1
    print(matriz_errada)
    # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]  — todas as linhas mudaram!

Por quê? Porque [0] * 3 cria UMA lista, e o * 3 externo cria uma lista
com TRÊS REFERÊNCIAS à mesma lista interna. Mudar qualquer linha muda
todas, pois todas são o mesmo objeto.

    # CORRETO: compreensão cria uma lista NOVA para cada linha
    matriz_certa = [[0] * 3 for _ in range(3)]
    matriz_certa[0][0] = 1
    print(matriz_certa)
    # [[1, 0, 0], [0, 0, 0], [0, 0, 0]]  — só a linha 0 mudou

(Compreensões de lista são formalmente apresentadas no Dia 10.)

---------------------------------------------------------------------------
7. Tuplas: sequências imutáveis
---------------------------------------------------------------------------
Uma tupla é como uma lista, mas IMUTÁVEL: depois de criada, não pode
ser modificada.

    ponto = (3, 4)
    rgb = (255, 128, 0)
    unitaria = (7,)     # ATENÇÃO: a vírgula faz isso ser tupla!
    vazia = ()

    ponto[0]            # 3 — leitura funciona
    ponto[0] = 10       # TypeError — escrita não funciona

A VÍRGULA FAZ A TUPLA, não os parênteses:
    (7)    →  int 7     (apenas parênteses em volta de uma expressão)
    (7,)   →  tupla (7,)  (a vírgula sinaliza: isso é uma tupla)
    7, 8   →  tupla (7, 8)  (sem parênteses, a vírgula ainda cria tupla)

Desempacotamento funciona como listas:

    x, y = ponto         # x = 3, y = 4
    a, *resto = (1, 2, 3, 4)  # a = 1, resto = [2, 3, 4]

POR QUE USAR TUPLA EM VEZ DE LISTA?

    Razão                          Exemplo de uso
    ----------------------------   ------------------------------------
    Imutabilidade: dados fixos     coordenadas, cores RGB, datas
    Pode ser chave de dicionário   {(0, 0): "origem"} — listas não podem
    Desempenho: ligeiramente menor Milhões de pequenos registros
    Semântica: "registro fixo"     (nome, cpf, nascimento) de uma pessoa

A escolha prática:
    - Vai mudar depois? Use lista
    - É um registro fixo de campos relacionados? Use tupla
    - Precisa usar como chave de dicionário? Use tupla

---------------------------------------------------------------------------
8. Custo das operações (prévia do Dia 29)
---------------------------------------------------------------------------
Nem todas as operações de lista custam o mesmo tempo. Conhecer o custo
evita escrever código que parece funcionar com 10 itens mas trava com
1 milhão:

    Operação                  Custo    Motivo
    ----------------------    ------   ----------------------------------------
    lista[i]                  O(1)     acesso direto por endereço de memória
    lista.append(x)           O(1)     adiciona no final, sem mover nada
    lista.pop()               O(1)     remove do final, sem mover nada
    lista.insert(0, x)        O(n)     empurra TODOS os elementos uma posição
    lista.pop(0)              O(n)     desloca TODOS os elementos uma posição
    x in lista                O(n)     no pior caso, percorre a lista inteira
    lista.sort()              O(n log n) o melhor possível para ordenação

Para inserção/remoção frequente no INÍCIO, use collections.deque (Dia 29).
Para verificar pertencimento frequente, use set (Dia 9 — custo O(1)).
""",
    exemplos=[
        Exemplo(
            titulo="Métodos de lista e a armadilha do append",
            codigo='''frutas = ["maça", "banana", "uva"]

# Metodos que modificam no lugar (devolvem None)
frutas.append("kiwi")
print("Apos append:", frutas)

frutas.insert(1, "laranja")
print("Apos insert(1, 'laranja'):", frutas)

retirada = frutas.pop()
print("Retirada:", retirada)
print("Apos pop:", frutas)

frutas.sort()
print("Apos sort:", frutas)

# A armadilha classica
lista = [1, 2, 3]
resultado = lista.append(4)   # append devolve None!
print("\nresultado de append:", resultado)    # None
print("mas a lista foi modificada:", lista)  # [1, 2, 3, 4]

# Diferenca entre append e extend
a = [1, 2]
b = [1, 2]
a.append([3, 4])    # adiciona a lista como UM elemento
b.extend([3, 4])    # adiciona CADA elemento
print("\nappend:", a)    # [1, 2, [3, 4]]
print("extend:", b)    # [1, 2, 3, 4]
''',
            explicacao="append() e extend() parecem parecidos mas fazem "
                       "coisas diferentes: append adiciona um único elemento "
                       "(que pode ser uma lista), extend desempacota e "
                       "adiciona cada elemento separadamente. "
                       "Nunca faça 'lista = lista.append(x)' — "
                       "lista viraria None.",
        ),
        Exemplo(
            titulo="Cópia rasa versus profunda na prática",
            codigo='''import copy

# Com tipos simples: copia rasa resolve
original = [1, 2, 3]
copia = original[:]
copia.append(4)
print("Original:", original)    # [1, 2, 3] — nao afetado
print("Copia:", copia)          # [1, 2, 3, 4]

# Com listas aninhadas: copia rasa NAO e suficiente
matriz_a = [[1, 2], [3, 4]]
matriz_b = matriz_a[:]          # copia rasa

matriz_b[0].append(99)          # modifica o objeto interno compartilhado
print("\nmatriz_a:", matriz_a)   # [[1, 2, 99], [3, 4]] — afetado!
print("matriz_b:", matriz_b)    # [[1, 2, 99], [3, 4]]

# Copia profunda: independe do nivel de aninhamento
matriz_c = [[1, 2], [3, 4]]
matriz_d = copy.deepcopy(matriz_c)

matriz_d[0].append(99)
print("\nmatriz_c:", matriz_c)   # [[1, 2], [3, 4]] — intacto!
print("matriz_d:", matriz_d)    # [[1, 2, 99], [3, 4]]
''',
            explicacao="Com listas simples (de números ou strings), a[:] "
                       "é suficiente porque os elementos são imutáveis e "
                       "não importa se são compartilhados. "
                       "Com listas de listas (matrizes), você precisa de "
                       "deepcopy para garantir independência total.",
        ),
        Exemplo(
            titulo="Ordenação com chaves personalizadas",
            codigo='''# Ordenando por comprimento
palavras = ["banana", "kiwi", "abacaxi", "uva", "maca"]
print(sorted(palavras, key=len))
# ['uva', 'kiwi', 'maca', 'banana', 'abacaxi']

# Ordenando dicionários por campo
alunos = [
    {"nome": "Carlos", "nota": 7.5},
    {"nome": "Ana",    "nota": 9.2},
    {"nome": "Bruno",  "nota": 6.8},
]

por_nota = sorted(alunos, key=lambda a: a["nota"], reverse=True)
for pos, aluno in enumerate(por_nota, start=1):
    print(f"{pos}. {aluno['nome']}: {aluno['nota']}")

# Ordenacao por multiplos criterios: tupla como chave
dados = [("Ana", "Silva"), ("Bruno", "Silva"), ("Ana", "Costa")]
print(sorted(dados))  # ordena por primeiro nome, depois sobrenome
# [('Ana', 'Costa'), ('Ana', 'Silva'), ('Bruno', 'Silva')]
''',
            explicacao="key= recebe uma FUNÇÃO que é aplicada a cada "
                       "elemento antes de comparar. len, str.lower e "
                       "lambda são as formas mais comuns. "
                       "Tupla como chave ordena pelo primeiro elemento "
                       "e usa o segundo para desempatar — exatamente "
                       "como comparação normal de tuplas funciona.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d08e1",
            enunciado=(
                "Escreva a funcao media(numeros) que calcula a media\n"
                "aritmetica de uma lista de numeros.\n\n"
                "Exemplos:\n"
                "   media([1, 2, 3, 4]) -> 2.5\n"
                "   media([])           -> 0.0   (lista vazia: retorna 0.0)\n"
                "   media([10])         -> 10.0\n\n"
                "Estrategia:\n"
                "   1. Clausula de guarda: se a lista estiver vazia, devolva 0.0\n"
                "      (sem essa verificacao, sum([]) / 0 causaria ZeroDivisionError)\n"
                "   2. Calcule: sum(numeros) / len(numeros)\n"
                "   3. Devolva o resultado\n\n"
                "Observacao: a divisao / em Python sempre devolve float,\n"
                "por isso media([10]) devolve 10.0 (nao o inteiro 10)."
            ),
            funcao="media",
            assinatura="def media(numeros):",
            testes=[
                ("media([1, 2, 3, 4])", "2.5"),
                ("media([])", "0.0"),
                ("media([10])", "10.0"),
            ],
            dica="if not numeros: return 0.0  — depois return sum(numeros) / len(numeros)",
        ),
        Exercicio(
            id="d08e2",
            enunciado=(
                "Escreva a funcao segundo_maior(numeros) que devolve o\n"
                "SEGUNDO MAIOR valor DISTINTO da lista.\n"
                "Se nao existir segundo maior, devolva None.\n\n"
                "Exemplos:\n"
                "   segundo_maior([3, 1, 4, 4, 5]) -> 4  (5 e o maior, 4 e o segundo)\n"
                "   segundo_maior([7, 7, 7])        -> None  (so um valor distinto)\n"
                "   segundo_maior([2, 9])            -> 2\n"
                "   segundo_maior([])               -> None\n\n"
                "Estrategia:\n"
                "   1. Elimine duplicatas convertendo para set e de volta para lista\n"
                "      unicos = sorted(set(numeros))\n"
                "   2. Se len(unicos) < 2: nao ha segundo maior, devolva None\n"
                "   3. O penultimo elemento da lista ordenada e o segundo maior:\n"
                "      unicos[-2]\n\n"
                "Por que set? set remove automaticamente os elementos repetidos.\n"
                "sorted(set([3,1,4,4,5])) -> [1, 3, 4, 5]  (sem o 4 duplicado)"
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
            dica="unicos = sorted(set(numeros)); if len(unicos) < 2: return None; return unicos[-2]",
        ),
        Exercicio(
            id="d08e3",
            enunciado=(
                "Escreva a funcao achatar(matriz) que transforma uma lista\n"
                "de listas em uma unica lista plana.\n\n"
                "Exemplos:\n"
                "   achatar([[1, 2], [3], [4, 5]]) -> [1, 2, 3, 4, 5]\n"
                "   achatar([])                    -> []\n"
                "   achatar([[], [1]])             -> [1]\n\n"
                "Estrategia usando extend:\n"
                "   resultado = []\n"
                "   for sublista in matriz:\n"
                "       resultado.extend(sublista)  <- adiciona cada elemento\n"
                "   return resultado\n\n"
                "Por que extend e nao append?\n"
                "   append([[1,2]]) -> [[1, 2]]  (adiciona a lista inteira)\n"
                "   extend([[1,2]]) -> [1, 2]    (adiciona cada elemento)"
            ),
            funcao="achatar",
            assinatura="def achatar(matriz):",
            testes=[
                ("achatar([[1, 2], [3], [4, 5]])", "[1, 2, 3, 4, 5]"),
                ("achatar([])", "[]"),
                ("achatar([[], [1]])", "[1]"),
            ],
            nivel="medio",
            dica="resultado = []; for sublista in matriz: resultado.extend(sublista); return resultado",
        ),
    ],
    quiz=[
        Quiz(
            "O que lista.append(x) devolve?",
            ["A lista modificada com o novo elemento",
             "O elemento x que foi adicionado",
             "None — append modifica a lista no lugar e nao devolve nada util",
             "O indice onde x foi inserido"],
            2,
            "Todos os metodos que modificam a lista no lugar (append, extend, "
            "insert, remove, sort, reverse) devolvem None. "
            "Nunca faca 'lista = lista.append(x)' — lista viraria None!",
        ),
        Quiz(
            "Por que [[0]*3]*3 e perigoso ao criar uma matriz?",
            ["E mais lento que outras formas",
             "Cria tres referencias ao mesmo objeto lista interna — mudar uma linha muda todas",
             "Causa IndexError ao tentar modificar",
             "Nao e perigoso — funciona identicamente a uma compreensao de lista"],
            1,
            "[0]*3 cria UMA lista. O *3 externo cria tres REFERENCIAS a essa mesma lista. "
            "matriz[0][0] = 1 muda o unico objeto compartilhado, "
            "por isso todas as 'linhas' mostram a mudança. "
            "Use [[0]*3 for _ in range(3)] para listas independentes.",
        ),
        Quiz(
            "Qual a diferenca entre sort() e sorted()?",
            ["sorted() e mais rapido que sort()",
             "sort() so funciona com numeros; sorted() com qualquer tipo",
             "sort() modifica a lista original e devolve None; sorted() devolve uma nova lista sem alterar a original",
             "Nao ha diferenca — produzem o mesmo resultado da mesma forma"],
            2,
            "sort() e um metodo de lista: altera a propria lista e devolve None. "
            "sorted() e uma funcao embutida: aceita qualquer iteravel, "
            "preserva o original intacto e devolve uma lista nova ja ordenada.",
        ),
        Quiz(
            "Quando uma tupla deve ser preferida a uma lista?",
            ["Nunca — listas fazem tudo que tuplas fazem e mais",
             "Quando os dados sao fixos e nao devem mudar, ou quando precisam ser usados como chave de dicionario",
             "Apenas quando os elementos sao todos do mesmo tipo",
             "Quando a lista tem mais de 100 elementos"],
            1,
            "Tuplas sao imutateis: comunicam 'estes dados nao devem mudar' "
            "e por isso podem ser chaves de dicionario (listas nao podem). "
            "Use lista quando os dados podem crescer ou mudar; "
            "use tupla para registros fixos como coordenadas, cores RGB ou retornos multiplos.",
        ),
    ],
    projeto=(
        "Crie gestao_estoque.py com uma lista de produtos como tuplas:\n\n"
        "   produtos = [\n"
        "       ('Caneta', 2.50, 100),  # (nome, preco, quantidade)\n"
        "       ('Caderno', 15.90, 30),\n"
        "       ('Regua', 3.75, 50),\n"
        "       ('Borracha', 1.20, 80),\n"
        "       ('Lapis', 0.90, 200),\n"
        "   ]\n\n"
        "Usando listas e os metodos aprendidos, calcule e exiba:\n\n"
        "   1. Relatorio completo ordenado por preco (menor para maior)\n"
        "   2. Relatorio ordenado por valor total em estoque (preco * qtd)\n"
        "   3. Produto mais caro e mais barato\n"
        "   4. Valor total do estoque\n"
        "   5. Produtos com estoque abaixo de 40 unidades (alerta)\n"
        "   6. Media de preco dos produtos\n\n"
        "BONUS: permita adicionar e remover produtos dinamicamente com\n"
        "uma lista mutavel de listas (nao tuplas), e reimprima o relatorio\n"
        "apos cada operacao."
    ),
    leitura=[
        "docs.python.org/pt-br/3/tutorial/datastructures.html — listas e tuplas",
        "docs.python.org/pt-br/3/library/copy.html — modulo copy (deepcopy)",
        "wiki.python.org/moin/TimeComplexity — custo das operacoes de lista",
    ],
))