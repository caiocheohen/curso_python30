"""Semana 3 - Dias 16 a 23: orientação a objetos e recursos avançados da linguagem."""

from nucleo.modelos import Dia, Exemplo, Exercicio, Quiz

DIAS = []

# ---------------------------------------------------------------- DIA 16
DIAS.append(Dia(
    numero=16,
    titulo="POO I: classes, objetos e estado",
    nivel="Intermediário",
    duracao="110 min",
    objetivos=[
        "Entender o que é orientação a objetos e qual problema ela resolve em relação a funções puras",
        "Criar classes com __init__, atributos de instância e métodos",
        "Compreender o papel de self: o que é, por que existe e como funciona mecanicamente",
        "Diferenciar atributo de instância de atributo de classe e prever as armadilhas de cada um",
        "Implementar __str__ e __repr__ e saber qual é chamado em cada situação",
        "Inspecionar objetos com dir(), vars() e isinstance()",
    ],
    teoria="""
Nos Dias 11 e 12 você aprendeu a organizar código em funções. Funções
são ótimas para AÇÕES — transformar uma entrada numa saída. Mas quando
você precisa representar uma ENTIDADE com estado que persiste e muda ao
longo do tempo, funções começam a ficar desajeitadas.

---------------------------------------------------------------------------
1. O problema que POO resolve
---------------------------------------------------------------------------
Imagine que você quer representar uma conta bancária. Com funções:

    # Com funções: estado espalhado em variáveis soltas
    saldo = 1000.0
    titular = "Ana"
    historico = []

    def depositar(valor):
        global saldo, historico
        saldo += valor
        historico.append(f"+{valor}")

    def sacar(valor):
        global saldo, historico
        if valor > saldo:
            raise ValueError("saldo insuficiente")
        saldo -= valor
        historico.append(f"-{valor}")

O problema: e se você precisar de DUAS contas ao mesmo tempo? As variáveis
globais `saldo`, `titular` e `historico` são únicas — não há como ter
duas contas independentes sem duplicar todo o código.

Com uma classe, cada conta é um objeto independente com seu próprio estado:

    class ContaBancaria:
        def __init__(self, titular, saldo_inicial=0.0):
            self.titular = titular
            self.saldo = saldo_inicial
            self.historico = []

        def depositar(self, valor):
            self.saldo += valor
            self.historico.append(f"+{valor}")

        def sacar(self, valor):
            if valor > self.saldo:
                raise ValueError("saldo insuficiente")
            self.saldo -= valor
            self.historico.append(f"-{valor}")

    conta1 = ContaBancaria("Ana", 1000.0)
    conta2 = ContaBancaria("Bruno", 500.0)
    # conta1 e conta2 são independentes — cada uma tem seu próprio estado

Esse é o núcleo da orientação a objetos: AGRUPAR dados (atributos) e
comportamentos (métodos) que pertencem à mesma entidade.

---------------------------------------------------------------------------
2. Classe versus objeto: o molde e a peça
---------------------------------------------------------------------------
Uma CLASSE é o molde — define a estrutura e o comportamento.
Um OBJETO (ou instância) é uma peça produzida a partir do molde.

    class Cachorro:           # <-- o molde
        def __init__(self, nome, raca):
            self.nome = nome
            self.raca = raca

        def latir(self):
            return f"{self.nome} diz: Au au!"

    rex   = Cachorro("Rex", "Pastor Alemão")   # <-- peça 1
    bolinha = Cachorro("Bolinha", "Poodle")    # <-- peça 2

    print(rex.latir())      # Rex diz: Au au!
    print(bolinha.latir())  # Bolinha diz: Au au!

Cada objeto tem seus próprios atributos (nome, raca), mas compartilha
os métodos definidos na classe. Modificar o nome de rex não afeta bolinha.

---------------------------------------------------------------------------
3. __init__: o construtor
---------------------------------------------------------------------------
__init__ é chamado automaticamente quando você cria um objeto com
NomeDaClasse(...). É onde você inicializa os atributos do objeto.

    class Pessoa:
        def __init__(self, nome, idade):
            self.nome = nome     # cria o atributo nome neste objeto
            self.idade = idade   # cria o atributo idade neste objeto

    # Criar um objeto chama __init__ automaticamente
    p = Pessoa("Ana", 30)
    # Equivale a: Pessoa.__init__(p, "Ana", 30)

__init__ não retorna nada (nunca use return com valor em __init__).
Se você tentar return valor em __init__, recebe um TypeError.

---------------------------------------------------------------------------
4. self: o mecanismo por trás dos métodos
---------------------------------------------------------------------------
self é o parâmetro que recebe a REFERÊNCIA ao objeto que está sendo usado.
Quando você chama p.metodo(), Python automaticamente passa p como primeiro
argumento — o self.

MECANICAMENTE, essas duas formas são equivalentes:

    p.saudar()              # forma de instância (o que você escreve)
    Pessoa.saudar(p)        # forma de classe (o que Python faz internamente)

Por isso self é sempre o PRIMEIRO parâmetro de todo método de instância.
Você pode chamar de qualquer nome (tecnicamente), mas self é a convenção
universal — nunca use outro nome.

SELF NÃO É AUTOMÁTICO DENTRO DO MÉTODO:
Dentro de um método, para acessar qualquer atributo ou outro método
da mesma instância, você precisa escrever self. explicitamente:

    class Circulo:
        def __init__(self, raio):
            self.raio = raio

        def area(self):
            import math
            return math.pi * self.raio ** 2   # precisa de self.raio!

        def area_dobrada(self):
            return self.area() * 2             # precisa de self.area()!

Esquecer self. é um dos erros mais comuns em POO:

    class Bugado:
        def __init__(self, valor):
            self.valor = valor

        def dobrar(self):
            return valor * 2    # NameError: name 'valor' is not defined
                                # deveria ser self.valor * 2

---------------------------------------------------------------------------
5. Atributo de instância versus atributo de classe
---------------------------------------------------------------------------
Existem dois tipos de atributos, e confundi-los é uma fonte comum de bugs:

ATRIBUTO DE INSTÂNCIA: pertence a UM objeto específico
    - Criado dentro de __init__ com self.nome = valor
    - Cada objeto tem o seu próprio, independente dos demais
    - Modificar um não afeta os outros

ATRIBUTO DE CLASSE: pertence à CLASSE inteira, compartilhado por todos
    - Criado no corpo da classe, fora de qualquer método
    - Todos os objetos veem o mesmo valor
    - Útil para constantes e contadores compartilhados

    class Produto:
        categoria = "Geral"           # atributo de CLASSE
        total_criados = 0             # atributo de CLASSE (contador)

        def __init__(self, nome, preco):
            self.nome = nome          # atributo de INSTÂNCIA
            self.preco = preco        # atributo de INSTÂNCIA
            Produto.total_criados += 1

    p1 = Produto("Caneta", 2.50)
    p2 = Produto("Caderno", 15.90)

    print(p1.categoria)          # "Geral"  (vem da classe)
    print(Produto.categoria)     # "Geral"  (acesso direto à classe)
    print(Produto.total_criados) # 2        (dois produtos criados)

A ARMADILHA CLÁSSICA: atributo de classe mutável

    class Turma:
        alunos = []          # PERIGO: lista compartilhada por TODAS as turmas!

        def adicionar(self, nome):
            self.alunos.append(nome)   # muta a lista da CLASSE

    t1 = Turma()
    t2 = Turma()
    t1.adicionar("Ana")
    print(t2.alunos)     # ['Ana'] — t2 também foi afetada!

    # CORRETO: criar a lista no __init__
    class Turma:
        def __init__(self):
            self.alunos = []    # lista PRÓPRIA de cada instância

        def adicionar(self, nome):
            self.alunos.append(nome)

A REGRA: nunca use listas, dicionários ou conjuntos como atributos de
classe. Use sempre __init__ para criar objetos mutáveis.

---------------------------------------------------------------------------
6. Métodos: funções que pertencem à classe
---------------------------------------------------------------------------
Métodos são simplesmente funções definidas dentro de uma classe. A única
diferença é que sempre recebem self como primeiro parâmetro:

    class Temperatura:
        def __init__(self, celsius):
            self.celsius = celsius

        def em_fahrenheit(self):
            return self.celsius * 9 / 5 + 32

        def em_kelvin(self):
            return self.celsius + 273.15

        def aquecer(self, graus):
            self.celsius += graus     # modifica o estado do objeto
            return self               # retornar self permite encadeamento

    t = Temperatura(25)
    print(t.em_fahrenheit())   # 77.0
    t.aquecer(10).aquecer(5)   # encadeamento: 25 + 10 + 5 = 40
    print(t.celsius)           # 40

MÉTODOS PODEM RETORNAR self para permitir encadeamento de chamadas —
padrão conhecido como "method chaining" ou "fluent interface".

---------------------------------------------------------------------------
7. __str__ e __repr__: representação em texto
---------------------------------------------------------------------------
Python chama automaticamente esses métodos especiais em diferentes
situações:

    __repr__: representação oficial — chamada no REPL e por repr()
              deve idealmente ser código válido Python para recriar o objeto
              é a fallback quando __str__ não está definido

    __str__:  representação legível — chamada por str() e print()
              deve ser amigável para o usuário final

    class Ponto:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __repr__(self):
            return f"Ponto({self.x}, {self.y})"   # ideal: recriar o objeto

        def __str__(self):
            return f"({self.x}, {self.y})"         # legível para usuário

    p = Ponto(3, 4)
    print(repr(p))   # Ponto(3, 4)   <- __repr__
    print(str(p))    # (3, 4)        <- __str__
    print(p)         # (3, 4)        <- print usa __str__

    # No REPL, digitar p diretamente usa __repr__
    # Em uma lista, __repr__ de cada elemento é usado
    print([p])       # [Ponto(3, 4)]  <- __repr__ dentro de coleções

QUANDO DEFINIR APENAS __repr__: se você só tem um deles, defina __repr__.
Python usa __repr__ como fallback quando __str__ não existe, mas não o
inverso. Com apenas __repr__, print() e repr() mostram o mesmo texto.

---------------------------------------------------------------------------
8. Inspecionando objetos
---------------------------------------------------------------------------
Python tem ferramentas para explorar objetos em tempo de execução:

    p = Ponto(3, 4)

    type(p)              # <class '__main__.Ponto'>
    type(p).__name__     # 'Ponto'

    isinstance(p, Ponto) # True
    isinstance(p, int)   # False

    vars(p)              # {'x': 3, 'y': 4}  — atributos de instância
    dir(p)               # lista todos os atributos e métodos (inclui herdados)

    p.__dict__           # {'x': 3, 'y': 4}  — equivalente a vars()
    p.__class__          # <class '__main__.Ponto'>

vars() e __dict__ mostram apenas os atributos de INSTÂNCIA (criados com
self), não os de classe nem os métodos. dir() mostra absolutamente tudo,
incluindo os herdados de object (como __init__, __class__, etc.).

id(p) retorna o identificador único do objeto na memória — o mesmo
número que aparece em repr(p) quando você não define __repr__.
""",
    exemplos=[
        Exemplo(
            titulo="Conta bancária: estado que persiste",
            codigo='''class ContaBancaria:
    """Representa uma conta bancaria simples."""

    taxa_manutencao = 9.90    # atributo de classe: igual para todas

    def __init__(self, titular, saldo=0.0):
        self.titular = titular
        self.saldo = saldo
        self._historico = []   # _ indica "uso interno"

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("valor deve ser positivo")
        self.saldo += valor
        self._historico.append(f"+ R${valor:.2f}")
        return self   # permite encadeamento

    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("valor deve ser positivo")
        if valor > self.saldo:
            raise ValueError("saldo insuficiente")
        self.saldo -= valor
        self._historico.append(f"- R${valor:.2f}")
        return self

    def extrato(self):
        print(f"Titular: {self.titular}")
        print(f"Saldo: R${self.saldo:.2f}")
        print("Historico:")
        for mov in self._historico:
            print(f"  {mov}")

    def __repr__(self):
        return f"ContaBancaria('{self.titular}', {self.saldo:.2f})"

    def __str__(self):
        return f"Conta de {self.titular}: R${self.saldo:.2f}"

conta = ContaBancaria("Ana", 1000.0)
conta.depositar(500).sacar(200)    # encadeamento
conta.extrato()
print(repr(conta))
print(str(conta))
''',
            explicacao="taxa_manutencao é atributo de classe — compartilhado. "
                       "_historico com underscore é convenção para 'atributo "
                       "interno, não acesse diretamente de fora'. "
                       "Retornar self em depositar/sacar permite encadear "
                       "chamadas como conta.depositar(500).sacar(200). "
                       "__repr__ segue a convenção de recriar o objeto.",
        ),
        Exemplo(
            titulo="Atributo de classe versus instância: vendo a diferença",
            codigo='''class Contador:
    total = 0     # atributo de CLASSE: compartilhado

    def __init__(self, nome):
        self.nome = nome          # atributo de INSTÂNCIA
        self.contagem = 0         # atributo de INSTÂNCIA
        Contador.total += 1       # incrementa o contador global

    def incrementar(self):
        self.contagem += 1

    def __repr__(self):
        return f"Contador('{self.nome}', contagem={self.contagem})"

c1 = Contador("A")
c2 = Contador("B")
c3 = Contador("C")

c1.incrementar()
c1.incrementar()
c2.incrementar()

print("c1:", c1)            # Contador('A', contagem=2)
print("c2:", c2)            # Contador('B', contagem=1)
print("c3:", c3)            # Contador('C', contagem=0)
print("Total criados:", Contador.total)  # 3

# Inspecionando
print("vars(c1):", vars(c1))   # so atributos de instancia
print("Classe de c1:", type(c1).__name__)
print("E Contador?", isinstance(c1, Contador))
''',
            explicacao="total é de classe: todos os Contador compartilham o mesmo. "
                       "contagem é de instância: cada objeto tem a sua própria. "
                       "vars(c1) mostra apenas {'nome': 'A', 'contagem': 2} — "
                       "o atributo total não aparece pois é da classe, não da instância. "
                       "Acessar Contador.total deixa claro que é um atributo de classe.",
        ),
        Exemplo(
            titulo="__str__ e __repr__ em situações diferentes",
            codigo='''class Fracao:
    """Representa uma fracao matematica."""

    def __init__(self, numerador, denominador):
        if denominador == 0:
            raise ValueError("denominador nao pode ser zero")
        # Simplifica automaticamente
        from math import gcd
        divisor = gcd(abs(numerador), abs(denominador))
        self.num = numerador // divisor
        self.den = denominador // divisor

    def __repr__(self):
        return f"Fracao({self.num}, {self.den})"  # recriar o objeto

    def __str__(self):
        if self.den == 1:
            return str(self.num)    # 4/1 exibe so "4"
        return f"{self.num}/{self.den}"

    def __add__(self, outra):
        novo_num = self.num * outra.den + outra.num * self.den
        novo_den = self.den * outra.den
        return Fracao(novo_num, novo_den)

f1 = Fracao(1, 2)
f2 = Fracao(1, 3)
f3 = f1 + f2

print(str(f1))    # 1/2   <- legivel
print(repr(f1))   # Fracao(1, 2)  <- para recriar
print(f3)         # 5/6   <- print usa __str__
print([f1, f2])   # [Fracao(1, 2), Fracao(1, 3)]  <- lista usa __repr__

# Simplificacao automatica
print(Fracao(6, 4))    # 3/2  (simplificado)
print(Fracao(4, 2))    # 2    (den=1 mostra so o inteiro)
''',
            explicacao="__repr__ segue a convenção: Fracao(1, 2) é código "
                       "Python válido que recriaria o objeto. "
                       "__str__ é mais amigável: '1/2'. "
                       "print() usa __str__; coleções como listas usam __repr__. "
                       "__add__ implementa o operador + — preview dos dunders do Dia 18.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d16e1",
            enunciado=(
                "Crie a classe Retangulo com:\n"
                "   __init__(self, base, altura): armazena base e altura\n"
                "   area(self): devolve base * altura\n"
                "   perimetro(self): devolve 2 * (base + altura)\n"
                "   eh_quadrado(self): devolve True se base == altura\n\n"
                "Exemplos:\n"
                "   Retangulo(3, 4).area()       -> 12\n"
                "   Retangulo(3, 4).perimetro()  -> 14\n"
                "   Retangulo(5, 5).eh_quadrado() -> True\n"
                "   Retangulo(5, 4).eh_quadrado() -> False\n\n"
                "Estrutura minima:\n"
                "   class Retangulo:\n"
                "       def __init__(self, base, altura):\n"
                "           self.base = base       <- salva em self\n"
                "           self.altura = altura   <- salva em self\n\n"
                "       def area(self):\n"
                "           return self.base * self.altura  <- acessa com self"
            ),
            funcao="Retangulo",
            assinatura="class Retangulo:\n    def __init__(self, base, altura):",
            testes=[
                ("Retangulo(3, 4).area()", "12"),
                ("Retangulo(3, 4).perimetro()", "14"),
                ("Retangulo(5, 5).eh_quadrado()", "True"),
                ("Retangulo(5, 4).eh_quadrado()", "False"),
            ],
            dica="Salve base e altura em self.__init__. Nos métodos, use self.base e self.altura.",
        ),
        Exercicio(
            id="d16e2",
            enunciado=(
                "O import math ja esta disponivel na assinatura.\n"
                "Crie a classe Ponto com:\n"
                "   __init__(self, x, y): armazena as coordenadas\n"
                "   distancia(self, outro): distancia euclidiana ate outro Ponto\n"
                "   __repr__(self): devolve 'Ponto(x, y)'\n\n"
                "Exemplos:\n"
                "   Ponto(0, 0).distancia(Ponto(3, 4)) -> 5.0\n"
                "   repr(Ponto(1, 2))                  -> 'Ponto(1, 2)'\n"
                "   Ponto(2, 2).distancia(Ponto(2, 2)) -> 0.0\n\n"
                "Distancia euclidiana entre (x1,y1) e (x2,y2):\n"
                "   sqrt((x2-x1)^2 + (y2-y1)^2)\n\n"
                "Use math.hypot(dx, dy) que calcula sqrt(dx^2 + dy^2):\n"
                "   dx = outro.x - self.x\n"
                "   dy = outro.y - self.y\n"
                "   return math.hypot(dx, dy)\n\n"
                "Em __repr__, o formato exato deve ser 'Ponto(x, y)'\n"
                "com os valores sem casas decimais se forem inteiros."
            ),
            funcao="Ponto",
            assinatura="import math\n\n\nclass Ponto:\n    def __init__(self, x, y):",
            testes=[
                ("Ponto(0, 0).distancia(Ponto(3, 4))", "5.0"),
                ("repr(Ponto(1, 2))", "'Ponto(1, 2)'"),
                ("Ponto(2, 2).distancia(Ponto(2, 2))", "0.0"),
            ],
            nivel="medio",
            dica="math.hypot(outro.x - self.x, outro.y - self.y) calcula a distância. __repr__ retorna f'Ponto({self.x}, {self.y})'.",
        ),
        Exercicio(
            id="d16e3",
            enunciado=(
                "Crie a classe Carrinho com:\n"
                "   __init__(self): cria self.itens = [] (lista vazia)\n"
                "   adicionar(self, nome, preco, qtd=1): adiciona item\n"
                "   total(self): soma preco*qtd de todos os itens\n"
                "   quantidade_itens(self): soma todas as quantidades\n\n"
                "Exemplos:\n"
                "   Carrinho().total() -> 0\n"
                "   c = Carrinho()\n"
                "   c.adicionar('x', 10, 2)\n"
                "   c.total() -> 20   (10 * 2)\n\n"
                "   c2 = Carrinho()\n"
                "   c2.adicionar('a', 5)     (qtd=1 por padrao)\n"
                "   c2.adicionar('b', 3, 3)  (qtd=3)\n"
                "   c2.quantidade_itens() -> 4   (1 + 3)\n\n"
                "ATENCAO CRITICA: crie self.itens = [] dentro de __init__,\n"
                "NUNCA no corpo da classe:\n"
                "   class Carrinho:\n"
                "       itens = []         <- ERRADO: compartilhado entre TODOS\n"
                "       def __init__(self):\n"
                "           self.itens = [] <- CORRETO: proprio de cada carrinho\n\n"
                "Sugestao: guarde cada item como dict ou tupla:\n"
                "   self.itens.append({'nome': nome, 'preco': preco, 'qtd': qtd})"
            ),
            funcao="Carrinho",
            assinatura="class Carrinho:\n    def __init__(self):",
            testes=[
                ("Carrinho().total()", "0"),
                ("(lambda c: (c.adicionar('x', 10, 2), c.total())[1])(Carrinho())", "20"),
                ("(lambda c: (c.adicionar('a', 5), c.adicionar('b', 3, 3), c.quantidade_itens())[2])(Carrinho())", "4"),
            ],
            nivel="dificil",
            dica="self.itens = [] no __init__. adicionar faz self.itens.append({'nome':nome,'preco':preco,'qtd':qtd}). total usa sum(i['preco']*i['qtd'] for i in self.itens).",
        ),
    ],
    quiz=[
        Quiz(
            "Por que self e necessario como primeiro parametro de todo metodo de instancia?",
            ["E uma exigencia arbitraria do Python sem motivo tecnico",
             "self recebe a referencia ao objeto que chamou o metodo, permitindo acessar seus atributos e outros metodos",
             "self e necessario apenas em __init__, nos outros metodos e opcional",
             "self e o nome da classe dentro do metodo"],
            1,
            "Quando voce faz p.metodo(), Python converte isso em Classe.metodo(p). "
            "O primeiro argumento sempre recebe o objeto chamador. "
            "Sem self, o metodo nao saberia a qual objeto os atributos pertencem. "
            "O nome 'self' e convencao universal — tecnicamente pode ser outro nome, "
            "mas nunca mude: e uma convencao sacrossanta da comunidade Python.",
        ),
        Quiz(
            "Qual o problema de definir uma lista como atributo de CLASSE?",
            ["Listas nao podem ser atributos de classe — causam SyntaxError",
             "Todos os objetos compartilham a MESMA lista — adicionar em um afeta todos",
             "A lista e somente leitura quando definida na classe",
             "Nao ha problema — funciona igual a definir em __init__"],
            1,
            "Atributos de classe sao compartilhados por TODAS as instancias. "
            "class Turma: alunos = [] cria UMA lista para todas as turmas. "
            "t1.alunos.append('Ana') muta essa lista unica, entao t2.alunos "
            "tambem mostra 'Ana'. Solucao: self.alunos = [] dentro de __init__.",
        ),
        Quiz(
            "Em qual situacao Python usa __repr__ em vez de __str__?",
            ["__repr__ nunca e usado automaticamente — so via repr()",
             "Dentro de colecoes (listas, dicionarios), no REPL ao inspecionar objetos, e como fallback quando __str__ nao existe",
             "__repr__ e usado por print() e __str__ pelo REPL",
             "__repr__ e __str__ sao sempre identicos — nao ha diferenca pratica"],
            1,
            "print(obj) usa __str__. "
            "print([obj]) usa __repr__ de obj (Python usa __repr__ dentro de colecoes). "
            "No REPL, digitar obj usa __repr__. "
            "Se so __repr__ existe, print() tambem o usa como fallback. "
            "Convencao: __repr__ deve produzir codigo Python valido para recriar o objeto.",
        ),
        Quiz(
            "O que vars(obj) retorna?",
            ["Todos os metodos e atributos do objeto, incluindo os herdados",
             "Apenas os atributos de INSTANCIA (self.x = ...) como dicionario",
             "O tipo e a classe do objeto",
             "O valor de retorno de __repr__"],
            1,
            "vars(obj) equivale a obj.__dict__: um dicionario com os atributos "
            "de instancia criados com self.nome = valor. "
            "Atributos de classe e metodos NAO aparecem em vars(). "
            "dir(obj) mostra absolutamente tudo, incluindo herdados de object.",
        ),
    ],
    projeto=(
        "Crie biblioteca.py com um sistema de biblioteca usando POO:\n\n"
        "   class Livro:\n"
        "       atributos: titulo, autor, ano, disponivel=True\n"
        "       metodos: emprestar(), devolver(), __str__, __repr__\n\n"
        "   class Biblioteca:\n"
        "       atributo de classe: total_livros = 0\n"
        "       atributos: nome, self.acervo = []\n"
        "       metodos:\n"
        "         adicionar(livro): adiciona ao acervo\n"
        "         buscar(termo): busca por titulo ou autor\n"
        "         emprestar(titulo): empresta se disponivel\n"
        "         devolver(titulo): marca como disponivel\n"
        "         relatorio(): exibe situacao do acervo\n\n"
        "DEMONSTRACAO:\n"
        "   - Crie uma biblioteca com 5 livros\n"
        "   - Empreste 2 livros\n"
        "   - Tente emprestar um ja emprestado (deve tratar o erro)\n"
        "   - Devolva 1\n"
        "   - Exiba o relatorio final\n\n"
        "BONUS: adicione um atributo de classe 'emprestimos_realizados'\n"
        "que conta o total de emprestimos feitos em TODAS as instancias\n"
        "de Biblioteca, e exiba no relatorio."
    ),
    leitura=[
        "docs.python.org/pt-br/3/tutorial/classes.html — classes em Python",
        "docs.python.org/pt-br/3/reference/datamodel.html — modelo de dados",
        "PEP 8 — secao sobre classes e nomenclatura",
    ],
))

# ---------------------------------------------------------------- DIA 17
DIAS.append(Dia(
    numero=17,
    titulo="POO II: propriedades, métodos de classe e estáticos",
    nivel="Intermediário",
    duracao="110 min",
    objetivos=[
        "Entender o problema que @property resolve e por que ele é preferível a getters/setters explícitos",
        "Criar propriedades com getter, setter e deleter, controlando acesso a atributos",
        "Reconhecer e evitar a armadilha de self._x versus self.x dentro do __init__",
        "Usar @classmethod para criar construtores alternativos com cls",
        "Usar @staticmethod para funções utilitárias que pertencem à classe conceitualmente",
        "Conhecer __slots__ e quando ele vale a pena usar",
    ],
    teoria="""
No Dia 16 você aprendeu a criar classes com atributos e métodos básicos.
Hoje vamos explorar recursos mais sofisticados: como controlar o acesso
aos atributos, criar formas alternativas de construir objetos e otimizar
o uso de memória.

---------------------------------------------------------------------------
1. O problema que @property resolve
---------------------------------------------------------------------------
Em linguagens como Java, é comum criar métodos getters e setters para
cada atributo, mesmo quando não há validação nenhuma:

    // Java: verboso e repetitivo
    public double getRaio() { return raio; }
    public void setRaio(double raio) {
        if (raio < 0) throw new Exception("raio negativo");
        this.raio = raio;
    }

O Python resolve isso de forma elegante: comece com atributo simples e,
SE precisar de validação ou computação no futuro, adicione @property
SEM QUEBRAR nenhum código que já usava o atributo diretamente.

CENÁRIO SEM @property (atributo simples):

    class Circulo:
        def __init__(self, raio):
            self.raio = raio         # atributo simples, acesso direto

    c = Circulo(5)
    c.raio = 10     # qualquer um pode colocar raio negativo!
    c.raio = -3     # Python não reclama — bug silencioso

CENÁRIO COM @property (acesso controlado):

    class Circulo:
        def __init__(self, raio):
            self.raio = raio     # ATENÇÃO: chama o SETTER, não armazena diretamente

        @property
        def raio(self):          # GETTER: executado ao ler c.raio
            return self._raio

        @raio.setter
        def raio(self, valor):   # SETTER: executado ao escrever c.raio = x
            if valor < 0:
                raise ValueError(f"raio não pode ser negativo: {valor}")
            self._raio = valor   # armazena no atributo "privado" _raio

    c = Circulo(5)
    print(c.raio)    # 5  — parece acesso a atributo, mas chama o getter
    c.raio = 10      # parece atribuição, mas chama o setter (com validação)
    c.raio = -3      # ValueError!

O código que usa a classe não muda: ainda escreve c.raio, não c.get_raio().
A validação acontece de forma transparente.

---------------------------------------------------------------------------
2. A anatomia completa de @property
---------------------------------------------------------------------------
Uma propriedade tem três partes opcionais além do getter:

    class Temperatura:
        def __init__(self, celsius=0):
            self.celsius = celsius     # chama o setter

        @property
        def celsius(self):             # GETTER
            return self._celsius

        @celsius.setter
        def celsius(self, valor):      # SETTER
            if valor < -273.15:
                raise ValueError(f"abaixo do zero absoluto: {valor}")
            self._celsius = valor

        @celsius.deleter
        def celsius(self):             # DELETER (raro, mas existe)
            del self._celsius

        @property
        def fahrenheit(self):          # PROPRIEDADE CALCULADA (só getter)
            return self._celsius * 9 / 5 + 32

    t = Temperatura(25)
    print(t.celsius)      # 25    — getter
    print(t.fahrenheit)   # 77.0  — propriedade calculada, sem setter

    t.celsius = 100       # setter
    del t.celsius         # deleter (deixa o objeto sem o atributo)

PROPRIEDADE SÓ DE LEITURA: defina apenas o @property sem o .setter.
Tentar escrever levanta AttributeError automaticamente.

    @property
    def area(self):
        return math.pi * self._raio ** 2

    c.area = 10    # AttributeError: can't set attribute

---------------------------------------------------------------------------
3. A armadilha _x versus x no __init__
---------------------------------------------------------------------------
Este é o erro mais comum ao aprender @property. Preste atenção:

    class Quadrado:
        def __init__(self, lado):
            self._lado = lado    # ARMAZENA direto no atributo interno
                                 # NÃO passa pela validação do setter!

        @property
        def lado(self):
            return self._lado

        @lado.setter
        def lado(self, valor):
            if valor <= 0:
                raise ValueError("lado deve ser positivo")
            self._lado = valor

    q = Quadrado(-5)   # NÃO levanta ValueError!
    print(q.lado)      # -5 — passou direto sem validação

A forma CORRETA é atribuir para self.lado (sem underscore) no __init__,
que chama o setter e aciona a validação:

    def __init__(self, lado):
        self.lado = lado     # CHAMA O SETTER — validação acontece!

    q = Quadrado(-5)   # ValueError: lado deve ser positivo ✓

Regra: dentro do __init__, use self.atributo (sem _) para que o setter
seja chamado. Dentro do getter e setter, use self._atributo (com _)
para acessar o valor armazenado diretamente, evitando recursão infinita.

---------------------------------------------------------------------------
4. @classmethod: construtores alternativos
---------------------------------------------------------------------------
Um classmethod recebe a CLASSE (cls) como primeiro argumento em vez da
instância (self). É a forma canônica de criar construtores alternativos:

    class Data:
        def __init__(self, ano, mes, dia):
            self.ano = ano
            self.mes = mes
            self.dia = dia

        @classmethod
        def de_string(cls, texto):        # construtor alternativo
            ano, mes, dia = texto.split("-")
            return cls(int(ano), int(mes), int(dia))

        @classmethod
        def hoje(cls):                    # outro construtor alternativo
            from datetime import date
            d = date.today()
            return cls(d.year, d.month, d.day)

        def __str__(self):
            return f"{self.ano:04d}-{self.mes:02d}-{self.dia:02d}"

    d1 = Data(2024, 7, 15)
    d2 = Data.de_string("2024-07-15")
    d3 = Data.hoje()

    print(d1)   # 2024-07-15
    print(d2)   # 2024-07-15

Por que usar cls em vez de escrever o nome da classe diretamente?

    @classmethod
    def de_string(cls, texto):
        return cls(...)         # CORRETO: respeita herança

    @classmethod
    def de_string(cls, texto):
        return Data(...)        # ERRADO: sempre cria Data, nunca subclasses

Se uma subclasse DataHora herdar de Data e chamar DataHora.de_string(...),
a versão com cls criará um DataHora. A versão com Data criaria um Data
errado. Sempre use cls em classmethods.

---------------------------------------------------------------------------
5. @staticmethod: funções que pertencem à classe, mas não ao objeto
---------------------------------------------------------------------------
Um staticmethod não recebe nem self nem cls. É uma função normal que
vive dentro da classe por organização, não por necessidade técnica:

    class Validador:
        @staticmethod
        def email_valido(email):
            return "@" in email and "." in email.split("@")[-1]

        @staticmethod
        def cpf_valido(cpf):
            return len(cpf.replace(".", "").replace("-", "")) == 11

    # Pode chamar pela classe ou por uma instância
    Validador.email_valido("ana@email.com")    # True
    Validador.cpf_valido("123.456.789-00")     # True

QUANDO USAR CADA UM:

    Precisa de self (acessa atributos da instância)?  -> método normal
    Precisa de cls  (acessa ou cria a classe)?        -> @classmethod
    Não precisa de nenhum dos dois?                   -> @staticmethod

    Regra prática: se você pode transformar em uma função pura fora da
    classe sem perder nada, é candidata a @staticmethod. Se ela está
    na classe só por organização temática, tudo bem — mas considere
    se uma função de módulo seria mais simples.

---------------------------------------------------------------------------
6. Propriedades calculadas: atributos que se derivam de outros
---------------------------------------------------------------------------
Uma propriedade sem setter é uma propriedade calculada — seu valor é
derivado de outros atributos e sempre está atualizado:

    class Retangulo:
        def __init__(self, base, altura):
            self.base = base
            self.altura = altura

        @property
        def area(self):
            return self.base * self.altura

        @property
        def perimetro(self):
            return 2 * (self.base + self.altura)

        @property
        def eh_quadrado(self):
            return self.base == self.altura

    r = Retangulo(3, 4)
    print(r.area)          # 12    — calculado na hora, parece atributo
    print(r.perimetro)     # 14

    r.base = 5             # muda a base
    print(r.area)          # 20    — recalculado automaticamente!

A vantagem sobre armazenar area como atributo: ela SEMPRE reflete o
estado atual. Se base mudar, area muda junto sem precisar de update manual.

---------------------------------------------------------------------------
7. __slots__: otimizando memória
---------------------------------------------------------------------------
Por padrão, cada instância Python tem um __dict__ (dicionário) que
armazena seus atributos — flexível, mas consome memória extra.

Para classes com MUITAS instâncias (dezenas de milhares), __slots__
elimina o __dict__ e armazena os atributos diretamente:

    class PontoNormal:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class PontoSlots:
        __slots__ = ("x", "y")     # lista os atributos permitidos

        def __init__(self, x, y):
            self.x = x
            self.y = y

    # Comparando memória
    import sys
    pn = PontoNormal(1, 2)
    ps = PontoSlots(1, 2)
    print(sys.getsizeof(pn.__dict__))  # ~200 bytes (o dicionário)
    print(sys.getsizeof(ps))           # menor — sem __dict__

RESTRIÇÕES do __slots__:
    - Não pode adicionar atributos que não estão em __slots__
    - ps.z = 3   # AttributeError!
    - vars(ps) não funciona (sem __dict__)
    - Herança com __slots__ tem detalhes específicos

QUANDO USAR: só quando você cria MUITAS instâncias e a memória é crítica.
Na maioria dos casos, o ganho não justifica a perda de flexibilidade.
""",
    exemplos=[
        Exemplo(
            titulo="@property com getter, setter e propriedade calculada",
            codigo='''import math

class Circulo:
    """Circulo com raio validado e propriedades calculadas."""

    def __init__(self, raio):
        self.raio = raio    # chama o setter — validacao acontece aqui!

    @property
    def raio(self):
        return self._raio

    @raio.setter
    def raio(self, valor):
        if valor < 0:
            raise ValueError(f"raio nao pode ser negativo: {valor}")
        self._raio = valor

    @property
    def area(self):               # propriedade calculada, so getter
        return round(math.pi * self._raio ** 2, 2)

    @property
    def diametro(self):           # calculada a partir do raio
        return self._raio * 2

    @diametro.setter
    def diametro(self, valor):    # setter alternativo: define pelo diametro
        self.raio = valor / 2     # chama o setter de raio (com validacao)

    def __repr__(self):
        return f"Circulo(raio={self._raio})"

c = Circulo(5)
print(c.raio)       # 5
print(c.area)       # 78.54
print(c.diametro)   # 10

c.diametro = 20     # setter do diametro -> setter do raio
print(c.raio)       # 10.0

try:
    c.raio = -1     # ValueError!
except ValueError as e:
    print(e)

try:
    c.area = 10     # AttributeError: sem setter!
except AttributeError as e:
    print(e)
''',
            explicacao="self.raio = raio no __init__ chama o setter — a validação "
                       "ocorre na criação. self._raio é o atributo interno real. "
                       "diametro.setter chama self.raio (sem _), o que aciona "
                       "o setter de raio com a validação — evita duplicar a lógica. "
                       "area não tem setter: tentar escrever levanta AttributeError.",
        ),
        Exemplo(
            titulo="@classmethod: construtores alternativos na prática",
            codigo='''class Cor:
    """Representa uma cor RGB."""

    def __init__(self, r, g, b):
        for nome, val in [("r", r), ("g", g), ("b", b)]:
            if not 0 <= val <= 255:
                raise ValueError(f"{nome}={val} deve estar entre 0 e 255")
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def de_hex(cls, hexcode):
        """Cria uma Cor a partir de um codigo hexadecimal '#RRGGBB'."""
        hexcode = hexcode.lstrip("#")
        r = int(hexcode[0:2], 16)
        g = int(hexcode[2:4], 16)
        b = int(hexcode[4:6], 16)
        return cls(r, g, b)    # usa cls, nao Cor — respeita herança!

    @classmethod
    def de_nome(cls, nome):
        """Cria uma Cor a partir de nomes basicos."""
        cores = {
            "vermelho": (255, 0, 0),
            "verde":    (0, 255, 0),
            "azul":     (0, 0, 255),
            "branco":   (255, 255, 255),
            "preto":    (0, 0, 0),
        }
        if nome not in cores:
            raise ValueError(f"cor '{nome}' desconhecida")
        return cls(*cores[nome])

    @staticmethod
    def hex_valido(hexcode):
        """Verifica se um codigo hex e valido."""
        import re
        return bool(re.match(r"^#[0-9A-Fa-f]{6}$", hexcode))

    def __repr__(self):
        return f"Cor({self.r}, {self.g}, {self.b})"

    def __str__(self):
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

c1 = Cor(255, 128, 0)
c2 = Cor.de_hex("#FF8000")
c3 = Cor.de_nome("azul")

print(c1, c2, c3)
print(Cor.hex_valido("#FF8000"))   # True
print(Cor.hex_valido("FF8000"))    # False (sem #)
''',
            explicacao="Três formas de criar uma Cor: diretamente, via hex e via nome. "
                       "cls(*cores[nome]) desempacota a tupla (255,0,0) como argumentos. "
                       "hex_valido é @staticmethod: não precisa de self nem cls — "
                       "só pertence à classe por organização temática. "
                       "int('FF', 16) converte hexadecimal para inteiro decimal.",
        ),
        Exemplo(
            titulo="Comparando método normal, classmethod e staticmethod",
            codigo='''class Funcionario:
    empresa = "TechCorp"    # atributo de classe

    def __init__(self, nome, salario):
        self.nome = nome
        self.salario = salario

    def aumentar(self, percentual):
        """Metodo de instancia: acessa e modifica self."""
        self.salario *= (1 + percentual / 100)
        return self

    @classmethod
    def mudar_empresa(cls, novo_nome):
        """Classmethod: modifica atributo da CLASSE."""
        cls.empresa = novo_nome

    @classmethod
    def de_string(cls, texto):
        """Classmethod: construtor alternativo."""
        nome, salario = texto.split(",")
        return cls(nome.strip(), float(salario))

    @staticmethod
    def calcular_ir(salario):
        """Staticmethod: calculo puro, sem self ou cls."""
        if salario <= 2259:   return 0.0
        if salario <= 2826:   return salario * 0.075
        if salario <= 3751:   return salario * 0.15
        if salario <= 4664:   return salario * 0.225
        return salario * 0.275

    def __str__(self):
        ir = Funcionario.calcular_ir(self.salario)
        return (f"{self.nome} @ {self.empresa}: "
                f"R${self.salario:.2f} (IR: R${ir:.2f})")

f1 = Funcionario("Ana", 5000)
f2 = Funcionario.de_string("Bruno, 3500")

print(f1)
print(f2)

f1.aumentar(10)
print(f1)

Funcionario.mudar_empresa("NewTech")
print(f1)   # empresa mudou para todos
print(f2)
''',
            explicacao="aumentar usa self: modifica apenas este funcionário. "
                       "mudar_empresa usa cls: modifica o atributo de classe, "
                       "afetando TODOS os funcionários existentes e futuros. "
                       "calcular_ir não precisa de nenhum contexto: é um cálculo "
                       "puro que poderia ser função livre, mas vive na classe "
                       "por coesão temática.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d17e1",
            enunciado=(
                "O import math ja esta disponivel na assinatura.\n"
                "Crie a classe Circulo com:\n"
                "   __init__(self, raio): usa o SETTER (self.raio = raio)\n"
                "   @property raio: getter que devolve self._raio\n"
                "   @raio.setter: valida raio >= 0 (raise ValueError se negativo)\n"
                "   @property area: calcula e devolve round(pi * raio^2, 2)\n\n"
                "Exemplos:\n"
                "   Circulo(1).area    -> 3.14\n"
                "   Circulo(2).raio    -> 2\n"
                "   Circulo(0)         -> ok (raio zero e valido)\n"
                "   Circulo(-5)        -> ValueError\n\n"
                "ATENCAO CRITICA: no __init__ use self.raio = raio\n"
                "   (SEM underscore) para que o setter seja chamado.\n"
                "   Se usar self._raio = raio, a validacao e ignorada!\n\n"
                "No getter: return self._raio  (COM underscore)\n"
                "No setter: self._raio = valor (COM underscore)\n"
                "No __init__: self.raio = raio (SEM underscore)"
            ),
            funcao="Circulo",
            assinatura="import math\n\n\nclass Circulo:\n    def __init__(self, raio):",
            testes=[
                ("Circulo(1).area", "3.14"),
                ("Circulo(2).raio", "2"),
                ("Circulo(0)", "!raise ValueError"),
                ("Circulo(-5)", "!raise ValueError"),
            ],
            nivel="medio",
            dica="No __init__: self.raio = raio (sem _). No setter: if valor < 0: raise ValueError. No getter: return self._raio. area: round(math.pi * self._raio**2, 2).",
        ),
        Exercicio(
            id="d17e2",
            enunciado=(
                "Crie a classe Produto com:\n"
                "   __init__(self, nome, preco): armazena nome e preco\n"
                "   @classmethod de_texto(cls, texto): construtor alternativo\n"
                "     recebe 'nome:preco' e devolve um Produto\n\n"
                "Exemplos:\n"
                "   Produto.de_texto('caneta:2.5').nome  -> 'caneta'\n"
                "   Produto.de_texto('caneta:2.5').preco -> 2.5\n"
                "   isinstance(Produto.de_texto('x:1'), Produto) -> True\n\n"
                "Estrategia do classmethod:\n"
                "   1. partes = texto.split(':')\n"
                "   2. nome = partes[0]\n"
                "   3. preco = float(partes[1])\n"
                "   4. return cls(nome, preco)  <- usa cls, nao Produto!\n\n"
                "Por que cls e nao Produto?\n"
                "   Se uma subclasse herdar Produto e chamar\n"
                "   SubProduto.de_texto(...), cls sera SubProduto.\n"
                "   Usando Produto diretamente, sempre criaria Produto,\n"
                "   nunca a subclasse — quebra o polimorfismo."
            ),
            funcao="Produto",
            assinatura="class Produto:\n    def __init__(self, nome, preco):",
            testes=[
                ("Produto.de_texto('caneta:2.5').nome", "'caneta'"),
                ("Produto.de_texto('caneta:2.5').preco", "2.5"),
                ("isinstance(Produto.de_texto('x:1'), Produto)", "True"),
            ],
            dica="@classmethod de_texto: partes = texto.split(':'); return cls(partes[0], float(partes[1]))",
        ),
        Exercicio(
            id="d17e3",
            enunciado=(
                "Crie a classe Celsius com:\n"
                "   __init__(self, valor=0): armazena self.valor\n"
                "   @property fahrenheit: calcula e devolve celsius*9/5+32\n"
                "   @fahrenheit.setter: converte fahrenheit para celsius\n"
                "     e armazena em self.valor\n\n"
                "Exemplos:\n"
                "   Celsius(100).fahrenheit       -> 212.0\n"
                "   c = Celsius()\n"
                "   c.fahrenheit = 32\n"
                "   c.valor                       -> 0.0\n\n"
                "   c2 = Celsius()\n"
                "   c2.fahrenheit = 212\n"
                "   round(c2.valor)               -> 100\n\n"
                "Formulas:\n"
                "   Celsius -> Fahrenheit: f = c * 9/5 + 32\n"
                "   Fahrenheit -> Celsius: c = (f - 32) * 5/9\n\n"
                "Aqui nao e necessario @property para self.valor —\n"
                "ele e um atributo simples. Apenas fahrenheit precisa\n"
                "de @property pois e calculado e tem setter de conversao."
            ),
            funcao="Celsius",
            assinatura="class Celsius:\n    def __init__(self, valor=0):",
            testes=[
                ("Celsius(100).fahrenheit", "212.0"),
                ("(lambda c: (setattr(c, 'fahrenheit', 32), c.valor)[1])(Celsius())", "0.0"),
                ("(lambda c: (setattr(c, 'fahrenheit', 212), round(c.valor))[1])(Celsius())", "100"),
            ],
            nivel="dificil",
            dica="@property fahrenheit: return self.valor * 9/5 + 32. @fahrenheit.setter: self.valor = (valor - 32) * 5/9.",
        ),
    ],
    quiz=[
        Quiz(
            "Qual a diferença entre self.raio = valor e self._raio = valor dentro do setter?",
            ["Nao ha diferenca — os dois fazem a mesma coisa",
             "self.raio = valor chamaria o setter novamente, causando recursao infinita; self._raio = valor armazena diretamente no atributo interno",
             "self._raio e mais rapido que self.raio",
             "self.raio so funciona dentro de __init__, self._raio em qualquer lugar"],
            1,
            "Dentro do setter de raio, escrever self.raio = valor chamaria "
            "o proprio setter de novo, que chamaria de novo, infinitamente. "
            "Por isso o setter armazena em self._raio (com underscore), "
            "o atributo interno real, sem passar pelo setter. "
            "O _ e convencao para 'uso interno — nao acesse diretamente'.",
        ),
        Quiz(
            "Por que @classmethod usa cls em vez do nome da classe diretamente?",
            ["cls e obrigatorio por sintaxe — Python nao aceita o nome da classe",
             "Para respeitar heranca: se uma subclasse chamar o metodo, cls sera a subclasse, nao a classe pai",
             "cls e mais rapido que usar o nome da classe",
             "Nao ha diferenca pratica — e so uma convencao"],
            1,
            "Se Produto.de_texto usa cls(nome, preco), e SubProduto herda Produto, "
            "SubProduto.de_texto retorna um SubProduto. "
            "Se usasse Produto(nome, preco) diretamente, sempre retornaria Produto, "
            "ignorando a subclasse — quebrando o polimorfismo do Dia 18.",
        ),
        Quiz(
            "Quando um metodo deve ser @staticmethod em vez de @classmethod?",
            ["Quando ele precisa acessar atributos da instancia",
             "Quando ele nao precisa nem de self nem de cls — e uma funcao pura que vive na classe por organizacao",
             "Quando ele precisa criar novas instancias da classe",
             "@staticmethod e @classmethod sao sinonimos"],
            1,
            "Metodo normal: precisa de self (acessa ou modifica o objeto). "
            "@classmethod: precisa de cls (acessa a classe, cria instancias, modifica atributos de classe). "
            "@staticmethod: nao precisa de nenhum dos dois — poderia ser uma funcao "
            "de modulo, mas vive na classe por coesao tematica.",
        ),
        Quiz(
            "O que acontece ao tentar escrever em uma propriedade que so tem @property (sem .setter)?",
            ["O valor e ignorado silenciosamente",
             "AttributeError: can't set attribute",
             "O Python cria um atributo de instancia com o mesmo nome",
             "TypeError: propriedades nao aceitam atribuicao"],
            1,
            "Uma propriedade sem setter e somente leitura. "
            "Tentar escrever levanta AttributeError automaticamente — "
            "nao e necessario nenhum codigo extra para proteger o atributo. "
            "Isso e util para propriedades calculadas como area e perimetro, "
            "que nao faz sentido definir diretamente.",
        ),
    ],
    projeto=(
        "Crie conta_poupanca.py com uma classe ContaPoupanca rica:\n\n"
        "   ATRIBUTOS (com @property e validacao):\n"
        "   - titular: str, nao pode ser vazio\n"
        "   - saldo: float, nao pode ser negativo (setter bloqueia)\n"
        "   - taxa_juros: float, entre 0 e 1 (ex: 0.05 para 5%)\n\n"
        "   PROPRIEDADES CALCULADAS (so getter):\n"
        "   - rendimento_mensal: saldo * taxa_juros / 12\n"
        "   - rendimento_anual: saldo * taxa_juros\n\n"
        "   CLASSMETHODS:\n"
        "   - de_string(cls, 'titular:saldo:taxa'): construtor alternativo\n"
        "   - padrao(cls, titular): cria com saldo=0 e taxa=0.06 (6% a.a.)\n\n"
        "   STATICMETHODS:\n"
        "   - calcular_tempo_dobrar(taxa): quantos anos para dobrar o capital\n"
        "     use a regra dos 72: 72 / (taxa * 100)\n\n"
        "   METODOS DE INSTANCIA:\n"
        "   - depositar(valor): valida (> 0) e adiciona ao saldo\n"
        "   - sacar(valor): valida (> 0, <= saldo) e subtrai\n"
        "   - aplicar_juros(): soma rendimento_mensal ao saldo\n"
        "   - __str__ e __repr__\n\n"
        "BONUS: simule 12 meses de juros compostos e exiba a evolucao\n"
        "do saldo mes a mes comparando duas contas com taxas diferentes."
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/functions.html#property — property embutida",
        "docs.python.org/pt-br/3/howto/descriptor.html — como property funciona internamente",
        "docs.python.org/pt-br/3/reference/datamodel.html#slots — __slots__",
    ],
))

# ---------------------------------------------------------------- DIA 18
DIAS.append(Dia(
    numero=18,
    titulo="POO III: herança, polimorfismo e métodos mágicos",
    nivel="Intermediário",
    duracao="120 min",
    objetivos=[
        "Criar hierarquias de classes com herança e entender o que é herdado e o que é sobrescrito",
        "Usar super() corretamente para aproveitar o comportamento da classe pai",
        "Entender polimorfismo e duck typing: o que importa é o comportamento, não o tipo",
        "Visualizar a MRO (Method Resolution Order) e prever qual método será chamado",
        "Implementar métodos mágicos para integrar objetos com os operadores e funções do Python",
        "Escolher entre herança e composição de forma consciente",
    ],
    teoria="""
Nos Dias 16 e 17 você aprendeu a criar classes individuais ricas. Hoje
vamos explorar como classes se RELACIONAM entre si: herança (uma classe
que herda de outra), polimorfismo (tratar objetos diferentes da mesma
forma) e os métodos mágicos que integram seus objetos ao Python.

---------------------------------------------------------------------------
1. Herança: o relacionamento "é um"
---------------------------------------------------------------------------
Herança permite que uma classe HERDE atributos e métodos de outra,
evitando repetição e criando hierarquias de especialização.

A regra de ouro para decidir se herança faz sentido:
    "Um Cachorro É UM Animal?"  → sim → herança faz sentido
    "Um Carro TEM UM Motor?"   → sim → composição faz sentido (não herança)

    class Animal:                  # classe BASE (ou pai, ou superclasse)
        def __init__(self, nome):
            self.nome = nome

        def respirar(self):
            return f"{self.nome} está respirando"

    class Cachorro(Animal):        # classe DERIVADA (ou filha, ou subclasse)
        def latir(self):
            return f"{self.nome} diz: Au au!"

    class Gato(Animal):
        def miar(self):
            return f"{self.nome} diz: Miau!"

    rex = Cachorro("Rex")
    print(rex.respirar())   # herdado de Animal: "Rex está respirando"
    print(rex.latir())      # próprio de Cachorro: "Rex diz: Au au!"

    isinstance(rex, Cachorro)  # True
    isinstance(rex, Animal)    # True — rex É UM Animal também!
    isinstance(rex, Gato)      # False

O QUE É HERDADO: todos os atributos e métodos da classe base, incluindo
__init__ (se a subclasse não definir o seu próprio).

---------------------------------------------------------------------------
2. Sobrescrita (override) e super()
---------------------------------------------------------------------------
Uma subclasse pode SOBRESCREVER qualquer método herdado, fornecendo
sua própria implementação:

    class Animal:
        def __init__(self, nome):
            self.nome = nome

        def falar(self):
            return "..."    # implementação genérica

    class Cachorro(Animal):
        def falar(self):         # sobrescreve Animal.falar
            return "Au au!"

    class Gato(Animal):
        def falar(self):         # sobrescreve Animal.falar
            return "Miau!"

SUPER(): chamando o método da classe pai

super() devolve um proxy para a classe pai, permitindo chamar métodos
que foram sobrescritos sem repetir código:

    class Animal:
        def __init__(self, nome, idade):
            self.nome = nome
            self.idade = idade

    class Cachorro(Animal):
        def __init__(self, nome, idade, raca):
            super().__init__(nome, idade)   # inicializa o que Animal precisa
            self.raca = raca               # adiciona o que Cachorro precisa

    class CachorroGuia(Cachorro):
        def __init__(self, nome, idade, raca, dono):
            super().__init__(nome, idade, raca)  # cadeia sobe até Animal
            self.dono = dono

POR QUE SUPER() EM VEZ DO NOME DA CLASSE?

    # ERRADO: acopla ao nome específico
    def __init__(self, nome, raca):
        Animal.__init__(self, nome)   # frágil: se a hierarquia mudar, quebra
        self.raca = raca

    # CORRETO: usa a MRO (próxima seção)
    def __init__(self, nome, raca):
        super().__init__(nome)        # seguro: segue a MRO automaticamente

---------------------------------------------------------------------------
3. Polimorfismo e duck typing
---------------------------------------------------------------------------
POLIMORFISMO significa tratar objetos de tipos diferentes da mesma forma,
desde que eles ofereçam o mesmo comportamento (interface).

    class Cachorro:
        def falar(self):
            return "Au au!"

    class Gato:
        def falar(self):
            return "Miau!"

    class Papagaio:
        def falar(self):
            return "Quer biscoito!"

    # Não importa o tipo — qualquer objeto com .falar() funciona
    animais = [Cachorro(), Gato(), Papagaio()]
    for animal in animais:
        print(animal.falar())    # polimorfismo em ação

DUCK TYPING: o nome vem do ditado "se anda como um pato e grasna como
um pato, é um pato". Python não verifica o tipo do objeto — só se ele
tem o método ou atributo necessário.

    # Esta função aceita QUALQUER objeto com .falar()
    # Não precisa herdar de Animal nem implementar interface
    def fazer_barulho(coisa):
        print(coisa.falar())    # funciona se coisa tiver .falar()

    class Aspirador:
        def falar(self):
            return "Vrummmmm!"

    fazer_barulho(Aspirador())    # funciona! "Vrummmmm!"

Duck typing é a razão pela qual Python raramente precisa de interfaces
formais como em Java. Se o objeto faz o que precisa, funciona.

---------------------------------------------------------------------------
4. MRO: Method Resolution Order
---------------------------------------------------------------------------
Quando Python procura um método, ele segue a MRO — a ordem em que as
classes são percorridas. Você pode ver a MRO com:

    Cachorro.__mro__
    # (<class 'Cachorro'>, <class 'Animal'>, <class 'object'>)

Para herança simples (A herda de B que herda de C), a MRO é direta:
subclasse → classe pai → classe avó → ... → object.

HERANÇA MÚLTIPLA: Python usa o algoritmo C3 para calcular a MRO:

    class A:
        def metodo(self): return "A"

    class B(A):
        def metodo(self): return "B"

    class C(A):
        def metodo(self): return "C"

    class D(B, C):     # herda de B e C
        pass

    D.__mro__
    # D -> B -> C -> A -> object

    D().metodo()    # "B" — Python encontra em B primeiro

super() segue a MRO, não apenas o pai direto. Em D, super().__init__()
chamaria B, que chamaria C, que chamaria A — garantindo que todos os
__init__ da cadeia sejam executados.

USE __mro__ ou mro() para depurar problemas de herança múltipla.

---------------------------------------------------------------------------
5. Métodos mágicos (dunders): integrando ao Python
---------------------------------------------------------------------------
Métodos com duplo underscore no nome (__init__, __str__...) são chamados
de "dunders" (de "double underscore") ou métodos especiais. Python os
chama automaticamente em resposta a operadores e funções embutidas.

REPRESENTAÇÃO:

    Dunder        Chamado por          Descrição
    ----------    ----------------     ----------------------------------
    __repr__      repr(obj), REPL      representação oficial
    __str__       str(obj), print()    representação legível
    __format__    f"{obj:spec}"        formatação personalizada
    __bytes__     bytes(obj)           representação em bytes

ARITMÉTICA:

    Dunder        Operador    Dunder reverso
    ----------    --------    --------------
    __add__       a + b       __radd__ (b + a quando b não suporta)
    __sub__       a - b       __rsub__
    __mul__       a * b       __rmul__
    __truediv__   a / b       __rtruediv__
    __floordiv__  a // b
    __mod__       a % b
    __pow__       a ** b
    __neg__       -a          (unário)
    __abs__       abs(a)

COMPARAÇÃO:

    Dunder        Operador    Notas
    ----------    --------    ------------------------------------------
    __eq__        a == b      define hash automaticamente se definido
    __ne__        a != b      automatico se __eq__ definido
    __lt__        a < b
    __le__        a <= b
    __gt__        a > b
    __ge__        a >= b

CONTÊINER:

    Dunder        Chamado por          Descrição
    ----------    ----------------     ----------------------------------
    __len__       len(obj)             comprimento
    __getitem__   obj[i]               acesso por índice/chave
    __setitem__   obj[i] = x           atribuição por índice
    __delitem__   del obj[i]           remoção por índice
    __contains__  x in obj             pertencimento
    __iter__      iter(obj), for       iteração
    __next__      next(obj)            próximo elemento

CONTEXTO E CONTROLE:

    Dunder        Chamado por          Descrição
    ----------    ----------------     ----------------------------------
    __call__      obj()                objeto chamável como função
    __enter__     with obj as x:       entrada do contexto (with)
    __exit__      fim do with          saída do contexto
    __bool__      bool(obj), if obj    valor booleano
    __hash__      hash(obj), sets      chave em dicionários e sets

SOBRE __hash__ E __eq__:
Quando você define __eq__, Python automaticamente torna o objeto não
hasheável (hash = None), porque dois objetos iguais devem ter o mesmo
hash. Se você precisa que o objeto seja hasheável (para usar em sets
ou como chave de dict), defina __hash__ explicitamente.

---------------------------------------------------------------------------
6. Herança versus composição
---------------------------------------------------------------------------
Herança não é a única forma de reutilizar comportamento. Composição
(um objeto TEM outro objeto) é frequentemente mais flexível:

    # Herança: Cachorro É UM Animal
    class Cachorro(Animal):
        pass

    # Composição: Carro TEM UM Motor
    class Motor:
        def __init__(self, potencia):
            self.potencia = potencia

        def ligar(self):
            return "Vrum!"

    class Carro:
        def __init__(self, modelo, potencia):
            self.modelo = modelo
            self.motor = Motor(potencia)   # TEM UM motor

        def acelerar(self):
            return self.motor.ligar()      # delega ao motor

QUANDO PREFERIR COMPOSIÇÃO:

    Prefira herança quando:
    - A relação é genuinamente "é um"
    - Você quer polimorfismo (tratar subclasses uniformemente)
    - A hierarquia é rasa (1-2 níveis)

    Prefira composição quando:
    - A relação é "tem um" ou "usa um"
    - Você quer flexibilidade: trocar o componente em tempo de execução
    - A herança criaria acoplamento excessivo
    - Você precisaria herdar de muitas classes ao mesmo tempo

A regra prática da comunidade Python: "Prefira composição a herança".
Herança profunda (4+ níveis) é quase sempre um sinal de design problemático.
""",
    exemplos=[
        Exemplo(
            titulo="Hierarquia com super() e polimorfismo",
            codigo='''class Forma:
    """Classe base para formas geometricas."""
    def __init__(self, cor="preto"):
        self.cor = cor

    def area(self):
        raise NotImplementedError("subclasse deve implementar area()")

    def descricao(self):
        # Metodo que usa polimorfismo: chama self.area() que sera da subclasse
        return f"{type(self).__name__} {self.cor}: area = {self.area():.2f}"

class Retangulo(Forma):
    def __init__(self, base, altura, cor="preto"):
        super().__init__(cor)    # inicializa Forma.__init__
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura

class Circulo(Forma):
    import math
    def __init__(self, raio, cor="preto"):
        super().__init__(cor)
        self.raio = raio

    def area(self):
        import math
        return math.pi * self.raio ** 2

class Triangulo(Forma):
    def __init__(self, base, altura, cor="preto"):
        super().__init__(cor)
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura / 2

# Polimorfismo: lista mista, tratamento uniforme
formas = [
    Retangulo(4, 5, "azul"),
    Circulo(3, "vermelho"),
    Triangulo(6, 4),
]

for forma in formas:
    print(forma.descricao())   # cada uma calcula sua propria area

total = sum(f.area() for f in formas)
print(f"Area total: {total:.2f}")

# isinstance com hierarquia
print(isinstance(formas[0], Retangulo))  # True
print(isinstance(formas[0], Forma))     # True (e uma Forma tambem!)
''',
            explicacao="descricao() está na classe base e chama self.area() — "
                       "o Python usará a area() da subclasse correta, não da base. "
                       "Isso é polimorfismo: um método, comportamentos diferentes. "
                       "NotImplementedError sinaliza que a subclasse DEVE sobrescrever "
                       "area() — uma forma leve de 'método abstrato'.",
        ),
        Exemplo(
            titulo="Métodos mágicos: vetor matemático completo",
            codigo='''import math

class Vetor:
    """Vetor 2D com operadores matematicos."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vetor({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, outro):       # v1 + v2
        return Vetor(self.x + outro.x, self.y + outro.y)

    def __sub__(self, outro):       # v1 - v2
        return Vetor(self.x - outro.x, self.y - outro.y)

    def __mul__(self, escalar):     # v * 3
        return Vetor(self.x * escalar, self.y * escalar)

    def __rmul__(self, escalar):    # 3 * v (escalar na esquerda)
        return self.__mul__(escalar)

    def __neg__(self):              # -v
        return Vetor(-self.x, -self.y)

    def __abs__(self):              # abs(v) = magnitude
        return math.hypot(self.x, self.y)

    def __eq__(self, outro):        # v1 == v2
        return self.x == outro.x and self.y == outro.y

    def __bool__(self):             # bool(v): False so se zero
        return self.x != 0 or self.y != 0

    def __len__(self):              # len(v): sempre 2D
        return 2

v1 = Vetor(1, 2)
v2 = Vetor(3, 4)

print(v1 + v2)       # (4, 6)
print(v1 - v2)       # (-2, -2)
print(v1 * 3)        # (3, 6)
print(3 * v1)        # (3, 6)  <- __rmul__
print(-v1)           # (-1, -2)
print(abs(v2))       # 5.0   <- magnitude do vetor (3,4,5)
print(v1 == Vetor(1, 2))   # True
print(bool(Vetor(0, 0)))   # False
print(len(v1))             # 2
''',
            explicacao="Cada dunder corresponde a um operador ou função Python. "
                       "__rmul__ é necessário para suportar 3 * v (escalar à esquerda): "
                       "Python tenta v.__rmul__(3) quando 3.__mul__(v) falha. "
                       "__abs__ é chamado por abs() e representa a magnitude do vetor. "
                       "Todos os métodos retornam um novo Vetor — objetos imutáveis.",
        ),
        Exemplo(
            titulo="MRO e herança múltipla na prática",
            codigo='''class Logger:
    """Mixin que adiciona logging a qualquer classe."""
    def log(self, mensagem):
        print(f"[{type(self).__name__}] {mensagem}")

class Serializavel:
    """Mixin que adiciona serialização."""
    def para_dict(self):
        return vars(self)

class Conta(Logger, Serializavel):
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self.saldo = saldo

    def depositar(self, valor):
        self.saldo += valor
        self.log(f"deposito de R${valor:.2f} — novo saldo: R${self.saldo:.2f}")

# MRO: Conta -> Logger -> Serializavel -> object
print(Conta.__mro__)

c = Conta("Ana", 1000)
c.depositar(500)

import json
print(json.dumps(c.para_dict()))

# Verificando a ordem de resolucao
class A:
    def metodo(self): return "A"

class B(A):
    def metodo(self): return f"B -> {super().metodo()}"

class C(A):
    def metodo(self): return f"C -> {super().metodo()}"

class D(B, C):
    def metodo(self): return f"D -> {super().metodo()}"

print(D().metodo())     # D -> B -> C -> A
print(D.__mro__)        # D, B, C, A, object
''',
            explicacao="Logger e Serializavel são 'mixins': classes pequenas "
                       "que adicionam comportamento sem representar uma entidade. "
                       "É uma forma comum de herança múltipla em Python. "
                       "super() em D chama B, depois C, depois A — seguindo a MRO. "
                       "vars(self) retorna o __dict__ da instância, "
                       "que funciona como serialização simples.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d18e1",
            enunciado=(
                "Crie a hierarquia de classes:\n\n"
                "   class Animal:\n"
                "       __init__(self, nome): armazena self.nome\n"
                "       falar(self): devolve '...' (generico)\n"
                "       apresentar(self): devolve '{nome} diz {falar()}'\n\n"
                "   class Cachorro(Animal):\n"
                "       falar(self): devolve 'au'\n\n"
                "   class Gato(Animal):\n"
                "       falar(self): devolve 'miau'\n\n"
                "Exemplos:\n"
                "   Cachorro('Rex').apresentar() -> 'Rex diz au'\n"
                "   Gato('Mia').apresentar()     -> 'Mia diz miau'\n"
                "   isinstance(Gato('x'), Animal) -> True\n\n"
                "DICA CHAVE: apresentar() fica APENAS em Animal e chama\n"
                "self.falar() — que sera o falar() da SUBCLASSE, nao de Animal.\n"
                "Isso e polimorfismo: um metodo, comportamentos diferentes.\n\n"
                "NÃO redefina apresentar() em Cachorro ou Gato.\n"
                "NÃO chame Animal.falar() diretamente em apresentar()."
            ),
            funcao="Animal",
            assinatura="class Animal:\n    def __init__(self, nome):",
            testes=[
                ("Cachorro('Rex').apresentar()", "'Rex diz au'"),
                ("Gato('Mia').apresentar()", "'Mia diz miau'"),
                ("isinstance(Gato('x'), Animal)", "True"),
            ],
            dica="apresentar retorna f'{self.nome} diz {self.falar()}'. Cachorro.falar retorna 'au'. Gato.falar retorna 'miau'.",
        ),
        Exercicio(
            id="d18e2",
            enunciado=(
                "Crie a classe Vetor com:\n"
                "   __init__(self, x, y): armazena as componentes\n"
                "   __add__(self, outro): soma dois vetores, devolve novo Vetor\n"
                "   __eq__(self, outro): True se x e y sao iguais\n"
                "   __repr__(self): devolve 'Vetor(x, y)'\n\n"
                "Exemplos:\n"
                "   repr(Vetor(1, 2) + Vetor(3, 4)) -> 'Vetor(4, 6)'\n"
                "   Vetor(1, 2) == Vetor(1, 2)      -> True\n"
                "   Vetor(1, 2) == Vetor(9, 9)      -> False\n\n"
                "IMPORTANTE: __add__ deve devolver um NOVO Vetor:\n"
                "   return Vetor(self.x + outro.x, self.y + outro.y)\n"
                "   Nao modifique self nem outro — vetores devem ser imutaveis.\n\n"
                "O operador + chama __add__ automaticamente:\n"
                "   v1 + v2  equivale a  v1.__add__(v2)\n\n"
                "__repr__ deve retornar exatamente 'Vetor(x, y)'\n"
                "para que repr(Vetor(4, 6)) == 'Vetor(4, 6)' seja True."
            ),
            funcao="Vetor",
            assinatura="class Vetor:\n    def __init__(self, x, y):",
            testes=[
                ("repr(Vetor(1, 2) + Vetor(3, 4))", "'Vetor(4, 6)'"),
                ("Vetor(1, 2) == Vetor(1, 2)", "True"),
                ("Vetor(1, 2) == Vetor(9, 9)", "False"),
            ],
            nivel="medio",
            dica="__add__: return Vetor(self.x + outro.x, self.y + outro.y). __eq__: return self.x == outro.x and self.y == outro.y. __repr__: return f'Vetor({self.x}, {self.y})'.",
        ),
        Exercicio(
            id="d18e3",
            enunciado=(
                "Crie a classe Pilha (stack: LIFO — last in, first out) com:\n"
                "   __init__(self): cria self._dados = []\n"
                "   empilhar(self, item): adiciona item ao topo\n"
                "   desempilhar(self): remove e devolve o topo (None se vazia)\n"
                "   __len__(self): numero de elementos\n"
                "   __bool__(self): False se vazia, True se tem elementos\n"
                "   __contains__(self, item): True se item estiver na pilha\n\n"
                "Exemplos:\n"
                "   len(Pilha())           -> 0\n"
                "   bool(Pilha())          -> False\n"
                "   p = Pilha()\n"
                "   p.empilhar(1); p.empilhar(2)\n"
                "   p.desempilhar()        -> 2  (ultimo que entrou)\n"
                "   5 in p (apos empilhar(5)) -> True\n"
                "   Pilha().desempilhar()  -> None  (pilha vazia: None)\n\n"
                "Delegue para a lista interna:\n"
                "   empilhar:     self._dados.append(item)\n"
                "   desempilhar:  self._dados.pop() se nao vazia, else None\n"
                "   __len__:      return len(self._dados)\n"
                "   __bool__:     return bool(self._dados)\n"
                "   __contains__: return item in self._dados"
            ),
            funcao="Pilha",
            assinatura="class Pilha:\n    def __init__(self):",
            testes=[
                ("len(Pilha())", "0"),
                ("bool(Pilha())", "False"),
                ("(lambda p: (p.empilhar(1), p.empilhar(2), p.desempilhar())[2])(Pilha())", "2"),
                ("(lambda p: (p.empilhar(5), 5 in p)[1])(Pilha())", "True"),
                ("Pilha().desempilhar()", "None"),
            ],
            nivel="dificil",
            dica="empilhar: self._dados.append(item). desempilhar: return self._dados.pop() if self._dados else None. __len__: return len(self._dados).",
        ),
    ],
    quiz=[
        Quiz(
            "Por que usar super().__init__() em vez de Animal.__init__(self)?",
            ["super() e mais rapido que chamar pelo nome",
             "super() segue a MRO, garantindo que todos os __init__ da cadeia sejam chamados corretamente, inclusive com heranca multipla",
             "Animal.__init__(self) causaria um erro de sintaxe",
             "Nao ha diferenca pratica entre os dois"],
            1,
            "Com Animal.__init__(self), voce acopla ao nome especifico Animal. "
            "Se a hierarquia mudar ou houver heranca multipla, pode pular "
            "__init__ de outras classes na cadeia. "
            "super() segue a MRO automaticamente, garantindo que toda a "
            "cadeia de inicializacao seja executada na ordem correta.",
        ),
        Quiz(
            "O que e duck typing e como se relaciona com polimorfismo em Python?",
            ["Duck typing exige que todos os objetos herdem de uma classe base comum",
             "Duck typing significa que Python so verifica se o objeto tem o metodo necessario, nao seu tipo — 'se anda como pato e grasna como pato, e um pato'",
             "Duck typing e um padrao de projeto especifico do Python",
             "Duck typing impede o uso de isinstance() no codigo"],
            1,
            "Em Java, voce declara interfaces e o compilador verifica tipos. "
            "Em Python, nao ha verificacao de tipo em tempo de compilacao — "
            "se o objeto tem o metodo falar(), ele funciona em fazer_barulho(), "
            "independente da classe ou hierarquia. "
            "Isso torna o Python extremamente flexivel, mas exige cuidado "
            "com documentacao de quais metodos sao esperados.",
        ),
        Quiz(
            "Dada a hierarquia D(B, C), B(A), C(A), qual a MRO de D?",
            ["D -> A -> B -> C -> object",
             "D -> B -> A -> C -> object",
             "D -> B -> C -> A -> object",
             "D -> C -> B -> A -> object"],
            2,
            "Python usa o algoritmo C3 para calcular a MRO. "
            "Para D(B, C): D primeiro, depois B (primeiro pai), depois C (segundo pai), "
            "depois A (base comum), depois object. "
            "Isso garante que nenhuma classe apareca antes de suas subclasses "
            "e que a ordem dos pais seja preservada.",
        ),
        Quiz(
            "Quando deve-se preferir composicao a heranca?",
            ["Nunca — heranca e sempre mais eficiente",
             "Quando a relacao e 'tem um' em vez de 'e um', ou quando voce quer flexibilidade para trocar componentes",
             "Apenas quando a classe base e da biblioteca padrao",
             "Quando ha mais de 5 metodos para herdar"],
            1,
            "Heranca modela 'e um': Cachorro e um Animal. "
            "Composicao modela 'tem um': Carro tem um Motor. "
            "Heranca profunda cria acoplamento forte — mudar a base quebra as filhas. "
            "Composicao e mais flexivel: voce pode trocar o Motor sem mudar o Carro. "
            "Regra da comunidade Python: 'prefira composicao a heranca'.",
        ),
    ],
    projeto=(
        "Crie rpg.py com um sistema de batalha simples usando POO:\n\n"
        "   class Personagem (base):\n"
        "       atributos: nome, vida, ataque, defesa\n"
        "       metodos:\n"
        "         receber_dano(dano): max(0, vida - max(0, dano - defesa))\n"
        "         esta_vivo: @property, True se vida > 0\n"
        "         atacar(alvo): causa self.ataque de dano em alvo\n"
        "         __str__: 'Nome (vida/vida_max HP)'\n"
        "         __repr__: 'Classe(nome, vida, ataque, defesa)'\n\n"
        "   class Guerreiro(Personagem):\n"
        "       ataque dobrado a cada 3 turnos (contador interno)\n"
        "       habilidade especial: golpe poderoso (2x ataque)\n\n"
        "   class Mago(Personagem):\n"
        "       ataque magico ignora defesa (dano direto)\n"
        "       mana: recurso que se esgota ao usar magia\n\n"
        "   class Arqueiro(Personagem):\n"
        "       atira em todos os inimigos com dano reduzido\n\n"
        "   DUNDERS EXTRAS no Personagem:\n"
        "       __lt__: compara pela vida (para ordenar por vida)\n"
        "       __bool__: True se esta_vivo\n\n"
        "SIMULACAO:\n"
        "   - Crie um grupo de heróis e um grupo de inimigos\n"
        "   - Simule rodadas de batalha ate um lado ser eliminado\n"
        "   - Use polimorfismo: todos atacam com o mesmo .atacar()\n"
        "   - Ao final, exiba o resultado ordenado por vida restante\n\n"
        "BONUS: adicione composicao — cada Personagem TEM um\n"
        "Inventario com items que dao bonus de ataque e defesa."
    ),
    leitura=[
        "docs.python.org/pt-br/3/reference/datamodel.html — metodos especiais",
        "docs.python.org/pt-br/3/tutorial/classes.html#multiple-inheritance",
        "PEP 3135 — super() sem argumentos",
    ],
))

# ---------------------------------------------------------------- DIA 19
DIAS.append(Dia(
    numero=19,
    titulo="dataclasses, Enum, NamedTuple e ABC",
    nivel="Intermediário",
    duracao="110 min",
    objetivos=[
        "Criar classes de dados com @dataclass, eliminando o boilerplate de __init__, __repr__ e __eq__",
        "Entender os campos obrigatórios, opcionais e calculados em dataclasses",
        "Usar Enum para representar conjuntos fixos de valores e evitar magic strings",
        "Criar tuplas nomeadas com NamedTuple para registros leves e imutáveis",
        "Definir contratos com ABC e @abstractmethod, forçando subclasses a implementar métodos",
        "Saber quando usar cada ferramenta: dict, namedtuple, dataclass ou classe normal",
    ],
    teoria="""
Python oferece ferramentas especializadas para padrões comuns de POO.
Em vez de escrever __init__, __repr__ e __eq__ manualmente toda vez,
você pode usar ferramentas que geram esse código automaticamente.

---------------------------------------------------------------------------
1. @dataclass: classes de dados sem boilerplate
---------------------------------------------------------------------------
Uma "classe de dados" é uma classe cujo principal propósito é GUARDAR
dados — pense em registros, configurações, resultados de cálculo. Sem
@dataclass, você escreve muito código repetitivo:

    # Sem @dataclass: muito código, toda vez
    class Ponto:
        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y

        def __repr__(self):
            return f"Ponto(x={self.x}, y={self.y})"

        def __eq__(self, outro):
            return self.x == outro.x and self.y == outro.y

    # Com @dataclass: mesma funcionalidade em 4 linhas
    from dataclasses import dataclass

    @dataclass
    class Ponto:
        x: float
        y: float

O decorator @dataclass lê as ANOTAÇÕES DE TIPO (x: float) e gera
automaticamente __init__, __repr__ e __eq__ equivalentes ao código
manual acima.

CAMPOS COM VALOR PADRÃO:

    @dataclass
    class Produto:
        nome: str
        preco: float
        quantidade: int = 1          # campo opcional com padrão
        ativo: bool = True

    Produto("caneta", 2.50)          # quantidade=1, ativo=True
    Produto("caderno", 15.90, 3)     # quantidade=3
    Produto("borracha", 1.20, 0, False)

REGRA: campos com padrão devem vir DEPOIS dos campos sem padrão.
Tentar colocar campo obrigatório depois de opcional gera TypeError.

CAMPOS CALCULADOS COM field() e __post_init__:
Para campos que dependem de outros campos, use __post_init__:

    from dataclasses import dataclass, field

    @dataclass
    class Retangulo:
        base: float
        altura: float
        area: float = field(init=False)   # excluído do __init__

        def __post_init__(self):
            self.area = self.base * self.altura   # calculado após __init__

    r = Retangulo(3, 4)
    print(r.area)    # 12.0 — calculado automaticamente

__post_init__ é chamado automaticamente ao final do __init__ gerado.
É o lugar certo para validação e campos calculados.

PARÂMETROS DO @dataclass:

    @dataclass(frozen=True)     # imutável: gera __hash__, bloqueia atribuição
    @dataclass(order=True)      # gera __lt__, __le__, __gt__, __ge__
    @dataclass(eq=False)        # não gera __eq__ (usa identidade)
    @dataclass(repr=False)      # não gera __repr__

frozen=True torna a dataclass imutável e hasheável (pode ser usada como
chave de dicionário ou em sets), equivalente a uma tupla nomeada, mas
com mais expressividade.

ANOTAÇÕES DE TIPO: o @dataclass exige anotações, mas o Python NÃO
verifica os tipos em tempo de execução. x: int = "texto" funciona sem
erro. As anotações servem de documentação e para ferramentas de análise
estática como mypy.

---------------------------------------------------------------------------
2. Enum: conjuntos fixos de valores
---------------------------------------------------------------------------
Um Enum representa um conjunto FIXO e FECHADO de valores possíveis.
É a solução para o problema das "magic strings" — strings espalhadas
pelo código que representam estados ou categorias:

    # Problema com strings: frágil e propenso a erros de digitação
    status = "pago"
    if status == "Pago":    # bug silencioso: maiúscula diferente
        enviar()

    # Solução com Enum: valores únicos, verificáveis, documentados
    from enum import Enum

    class Status(Enum):
        PENDENTE = "pendente"
        PAGO = "pago"
        CANCELADO = "cancelado"

    status = Status.PAGO
    if status == Status.PAGO:    # sem ambiguidade
        enviar()

ACESSANDO MEMBROS:

    Status.PAGO              # <Status.PAGO: 'pago'>
    Status.PAGO.name         # 'PAGO'   — o nome do membro
    Status.PAGO.value        # 'pago'   — o valor associado

    Status("pago")           # Status.PAGO — de valor para membro
    Status["PAGO"]           # Status.PAGO — de nome para membro

ITERANDO:

    list(Status)             # [Status.PENDENTE, Status.PAGO, Status.CANCELADO]
    for s in Status:
        print(s.name, s.value)

COMPARANDO:
    Enum usa identidade (is), não igualdade (==) de valor:

    Status.PAGO == Status.PAGO      # True
    Status.PAGO is Status.PAGO      # True (sempre o mesmo objeto)
    Status.PAGO == "pago"           # False! — tipo diferente

VARIANTES DE ENUM:

    from enum import Enum, IntEnum, Flag, auto

    class Cor(IntEnum):         # herda de int: pode comparar com números
        VERMELHO = 1
        VERDE = 2
        AZUL = 3

    class Permissao(Flag):      # suporta combinação bit a bit
        LER = auto()            # auto() gera valores automaticamente (1, 2, 4...)
        ESCREVER = auto()
        EXECUTAR = auto()
        ADMIN = LER | ESCREVER | EXECUTAR

    p = Permissao.LER | Permissao.ESCREVER
    Permissao.LER in p          # True

---------------------------------------------------------------------------
3. NamedTuple: tuplas com nomes nos campos
---------------------------------------------------------------------------
NamedTuple cria tuplas cujos campos têm nomes, tornando o código mais
legível do que usar índices numéricos:

    # Tupla comum: o que significa cada posição?
    ponto = (3, 4)
    x = ponto[0]     # o que é 0? confuso

    # NamedTuple: claro e autoexplicativo
    from typing import NamedTuple

    class Ponto(NamedTuple):
        x: float
        y: float
        z: float = 0.0    # campo com padrão

    p = Ponto(3, 4)
    print(p.x, p.y, p.z)    # 3  4  0.0
    print(p[0])              # 3  — ainda funciona como tupla
    print(len(p))            # 3

    # É uma tupla de verdade: imutável e hasheável
    p.x = 10    # AttributeError!
    {p: "ponto"}  # funciona como chave de dicionário

NAMEDTUPLE VERSUS DATACLASS:

    Característica      NamedTuple      @dataclass
    ----------------    ----------      ----------
    Imutável            sempre          só com frozen=True
    Hasheável           sempre          só com frozen=True
    Herança de tuple    sim             não
    Campos calculados   não             sim (__post_init__)
    Métodos extras      limitado        sim, completo
    Desempacotamento    x, y = ponto    x, y = dc.x, dc.y

Use NamedTuple para registros simples, imutáveis e leves.
Use @dataclass quando precisar de métodos, validação ou mutabilidade.

---------------------------------------------------------------------------
4. ABC: Classes Base Abstratas
---------------------------------------------------------------------------
Uma Classe Base Abstrata (ABC) define um CONTRATO que subclasses devem
cumprir. Ela não pode ser instanciada diretamente e exige que subclasses
implementem os métodos decorados com @abstractmethod.

    from abc import ABC, abstractmethod

    class Forma(ABC):             # herda de ABC
        @abstractmethod
        def area(self) -> float:  # contrato: toda Forma deve ter area()
            pass

        @abstractmethod
        def perimetro(self) -> float:
            pass

        def descricao(self):      # método concreto: funciona para todos
            return f"Area: {self.area():.2f}, Perim: {self.perimetro():.2f}"

    Forma()    # TypeError: Can't instantiate abstract class Forma
               # with abstract methods area, perimetro

    class Quadrado(Forma):
        def __init__(self, lado):
            self.lado = lado

        def area(self):
            return self.lado ** 2

        def perimetro(self):
            return 4 * self.lado

    Quadrado(5).area()    # 25 — funciona!
    Quadrado(5).descricao()  # herdado de Forma

    class Incompleta(Forma):
        def area(self):
            return 0
        # esqueceu perimetro!

    Incompleta()   # TypeError: Can't instantiate abstract class Incompleta
                   # with abstract method perimetro

ABC EM COMPARAÇÃO COM NotImplementedError (do Dia 18):

    # NotImplementedError: falha QUANDO o método é chamado
    class Forma:
        def area(self):
            raise NotImplementedError("implemente area()")

    Forma()            # funciona — cria o objeto
    Forma().area()     # só falha aqui

    # ABC: falha na CRIAÇÃO do objeto
    class Forma(ABC):
        @abstractmethod
        def area(self): pass

    Forma()            # falha aqui — antes de chamar qualquer método

ABC é mais seguro: o erro ocorre o mais cedo possível, na instanciação.
NotImplementedError é mais simples e funciona bem para hierarquias
onde você não quer a rigidez de ABC.

PROPRIEDADES ABSTRATAS:

    class Forma(ABC):
        @property
        @abstractmethod
        def nome(self) -> str:    # propriedade abstrata
            pass

    class Circulo(Forma):
        @property
        def nome(self) -> str:
            return "Círculo"

---------------------------------------------------------------------------
5. Quando usar cada ferramenta
---------------------------------------------------------------------------

    Ferramenta      Quando usar
    ----------      -----------------------------------------------------------
    dict            dados ad-hoc sem estrutura fixa; prototipagem rápida
    NamedTuple      registro simples, imutável, leve; pode usar como tupla
    @dataclass      classe de dados com métodos, validação ou mutabilidade
    Classe normal   comportamento complexo, herança rica, estado mutável
    Enum            conjunto fixo e fechado de valores (status, cores, dias)
    ABC             definir contratos que subclasses DEVEM implementar

A progressão natural:
    dict -> NamedTuple -> @dataclass -> classe normal
    (conforme o comportamento necessário aumenta)
""",
    exemplos=[
        Exemplo(
            titulo="@dataclass completa com validação e campo calculado",
            codigo='''from dataclasses import dataclass, field
from datetime import date

@dataclass(order=True)
class Funcionario:
    nome: str
    salario: float
    departamento: str
    data_admissao: date = field(default_factory=date.today)
    ativo: bool = True
    # campo calculado: excluido do __init__
    anos_empresa: int = field(init=False, repr=False)

    def __post_init__(self):
        # validacao e calculo apos __init__
        if self.salario < 0:
            raise ValueError(f"salario nao pode ser negativo: {self.salario}")
        hoje = date.today()
        delta = hoje - self.data_admissao
        self.anos_empresa = delta.days // 365

    def reajuste(self, percentual: float):
        self.salario *= (1 + percentual / 100)

    def __str__(self):
        return (f"{self.nome} ({self.departamento}) "
                f"- R${self.salario:.2f} - {self.anos_empresa} anos")

# @dataclass(order=True) permite comparar e ordenar pelo primeiro campo
f1 = Funcionario("Ana", 5000.0, "TI", date(2020, 1, 15))
f2 = Funcionario("Bruno", 4000.0, "RH", date(2021, 6, 1))
f3 = Funcionario("Carla", 6000.0, "TI", date(2019, 3, 10))

print(f1)
print(repr(f1))       # gerado automaticamente pelo @dataclass

funcionarios = [f1, f2, f3]
for f in sorted(funcionarios):    # ordena por nome (order=True)
    print(f)

f1.reajuste(10)
print(f"Apos reajuste: {f1.salario:.2f}")

# Igualdade gerada pelo @dataclass
f4 = Funcionario("Ana", 5000.0, "TI", date(2020, 1, 15))
''',
            explicacao="default_factory=date.today cria uma nova data para "
                       "cada instância — diferente de default=date.today() "
                       "que avaliaria a data UMA VEZ ao definir a classe. "
                       "order=True gera comparações baseadas nos campos em ordem. "
                       "__post_init__ é o lugar para validação e campos calculados. "
                       "repr=False exclui anos_empresa do __repr__ gerado.",
        ),
        Exemplo(
            titulo="Enum com lógica de negócio",
            codigo='''from enum import Enum, auto

class StatusPedido(Enum):
    RASCUNHO = auto()
    PENDENTE = auto()
    PAGO = auto()
    ENVIADO = auto()
    ENTREGUE = auto()
    CANCELADO = auto()

    def pode_cancelar(self) -> bool:
        """Retorna True se o pedido ainda pode ser cancelado."""
        return self in (StatusPedido.RASCUNHO,
                        StatusPedido.PENDENTE,
                        StatusPedido.PAGO)

    def proximo_status(self):
        """Retorna o proximo status valido na cadeia."""
        fluxo = {
            StatusPedido.RASCUNHO:  StatusPedido.PENDENTE,
            StatusPedido.PENDENTE:  StatusPedido.PAGO,
            StatusPedido.PAGO:      StatusPedido.ENVIADO,
            StatusPedido.ENVIADO:   StatusPedido.ENTREGUE,
        }
        return fluxo.get(self, None)

    def __str__(self):
        return self.name.capitalize()

# Testando
pedido = StatusPedido.PENDENTE
print(f"Status: {pedido}")
print(f"Pode cancelar: {pedido.pode_cancelar()}")
print(f"Proximo: {pedido.proximo_status()}")

# Navegando o fluxo
atual = StatusPedido.RASCUNHO
while atual:
    print(f"  -> {atual}")
    atual = atual.proximo_status()

# Enums sao singletons: use 'is' para comparar
print(StatusPedido.PAGO is StatusPedido.PAGO)    # True
print(StatusPedido.PAGO == StatusPedido.PAGO)    # True
print(StatusPedido.PAGO is StatusPedido.ENVIADO) # False
''',
            explicacao="Enums podem ter métodos — isso os torna muito mais poderosos "
                       "que simples constantes. pode_cancelar() encapsula a regra "
                       "de negócio no próprio Enum. "
                       "auto() gera valores inteiros sequenciais automaticamente — "
                       "o valor exato não importa, só a identidade do membro. "
                       "Enums são singletons: use 'is' para comparar, não '=='.",
        ),
        Exemplo(
            titulo="ABC garantindo o contrato",
            codigo='''from abc import ABC, abstractmethod
from typing import NamedTuple

class Ponto(NamedTuple):
    x: float
    y: float

class Forma(ABC):
    """Contrato: toda Forma deve implementar area e perimetro."""

    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimetro(self) -> float:
        pass

    @property
    @abstractmethod
    def nome(self) -> str:
        pass

    def descricao(self):    # concreto: disponivel para todas as subclasses
        return (f"{self.nome}: area={self.area():.2f}, "
                f"perimetro={self.perimetro():.2f}")

class Retangulo(Forma):
    def __init__(self, base: float, altura: float):
        self.base = base
        self.altura = altura

    @property
    def nome(self) -> str:
        return "Retangulo"

    def area(self) -> float:
        return self.base * self.altura

    def perimetro(self) -> float:
        return 2 * (self.base + self.altura)

class Circulo(Forma):
    import math
    def __init__(self, raio: float):
        self.raio = raio

    @property
    def nome(self) -> str:
        return "Circulo"

    def area(self) -> float:
        import math
        return math.pi * self.raio ** 2

    def perimetro(self) -> float:
        import math
        return 2 * math.pi * self.raio

# Polimorfismo garantido pelo contrato ABC
formas = [Retangulo(4, 5), Circulo(3)]
for f in formas:
    print(f.descricao())

# Tentando instanciar ABC diretamente
try:
    Forma()
except TypeError as e:
    print(f"Erro esperado: {e}")

# NamedTuple em acao
p = Ponto(3, 4)
print(f"Ponto: {p}, x={p.x}, y={p.y}")
print(f"E tupla: {isinstance(p, tuple)}")
x, y = p    # desempacota como tupla
print(f"Desempacotado: x={x}, y={y}")
''',
            explicacao="ABC garante que nenhuma subclasse incompleta seja "
                       "instanciada — o erro ocorre na criação, não quando "
                       "o método ausente é chamado. "
                       "A propriedade abstrata nome força que cada subclasse "
                       "declare seu próprio nome. "
                       "NamedTuple Ponto é uma tupla real: suporta desempacotamento, "
                       "indexação e len().",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d19e1",
            enunciado=(
                "O decorator @dataclass e o import ja estao na assinatura.\n"
                "Complete a dataclass Produto com os campos:\n"
                "   nome: str         (obrigatorio)\n"
                "   preco: float      (obrigatorio)\n"
                "   quantidade: int = 1  (opcional, padrao 1)\n\n"
                "E o metodo:\n"
                "   total(self) -> float: devolve preco * quantidade\n\n"
                "Exemplos:\n"
                "   Produto('x', 10.0, 3).total() -> 30.0\n"
                "   Produto('x', 5.0).total()     -> 5.0  (qtd=1)\n"
                "   Produto('x', 1.0) == Produto('x', 1.0) -> True\n"
                "   repr(Produto('x', 1.0, 2)) -> \"Produto(nome='x', preco=1.0, quantidade=2)\"\n\n"
                "@dataclass gera __init__, __repr__ e __eq__ automaticamente.\n"
                "Voce so precisa:\n"
                "   1. Declarar os campos com anotacoes de tipo\n"
                "   2. Colocar campos sem padrao ANTES dos com padrao\n"
                "   3. Adicionar o metodo total()"
            ),
            funcao="Produto",
            assinatura="from dataclasses import dataclass\n\n\n@dataclass\nclass Produto:",
            testes=[
                ("Produto('x', 10.0, 3).total()", "30.0"),
                ("Produto('x', 5.0).total()", "5.0"),
                ("Produto('x', 1.0) == Produto('x', 1.0)", "True"),
                ("repr(Produto('x', 1.0, 2))", "\"Produto(nome='x', preco=1.0, quantidade=2)\""),
            ],
            dica="Declare: nome: str; preco: float; quantidade: int = 1. Adicione def total(self): return self.preco * self.quantidade",
        ),
        Exercicio(
            id="d19e2",
            enunciado=(
                "O import Enum ja esta na assinatura.\n"
                "Crie o Enum Status com tres membros:\n"
                "   PENDENTE = 'pendente'\n"
                "   PAGO     = 'pago'\n"
                "   CANCELADO = 'cancelado'\n\n"
                "E a funcao (fora da classe):\n"
                "   pode_enviar(status) -> bool\n"
                "   Retorna True APENAS se status for Status.PAGO\n\n"
                "Exemplos:\n"
                "   pode_enviar(Status.PAGO)      -> True\n"
                "   pode_enviar(Status.PENDENTE)   -> False\n"
                "   Status('cancelado').name       -> 'CANCELADO'\n"
                "   len(list(Status))              -> 3\n\n"
                "Como comparar: use 'is' ou '==' para Enum:\n"
                "   return status is Status.PAGO\n"
                "   return status == Status.PAGO\n\n"
                "Status('cancelado') cria um membro a partir do VALOR —\n"
                "o Enum procura qual membro tem esse value e o devolve."
            ),
            funcao="Status",
            assinatura="from enum import Enum\n\n\nclass Status(Enum):",
            testes=[
                ("pode_enviar(Status.PAGO)", "True"),
                ("pode_enviar(Status.PENDENTE)", "False"),
                ("Status('cancelado').name", "'CANCELADO'"),
                ("len(list(Status))", "3"),
            ],
            nivel="medio",
            dica="class Status(Enum): PENDENTE='pendente'; PAGO='pago'; CANCELADO='cancelado'. def pode_enviar(status): return status is Status.PAGO",
        ),
        Exercicio(
            id="d19e3",
            enunciado=(
                "Os imports ABC e abstractmethod ja estao na assinatura.\n"
                "Crie:\n\n"
                "   class Forma(ABC):\n"
                "       @abstractmethod\n"
                "       def area(self) -> float: ...\n\n"
                "   class Quadrado(Forma):\n"
                "       def __init__(self, lado: float): ...\n"
                "       def area(self) -> float: ...\n\n"
                "Exemplos:\n"
                "   Quadrado(3).area()            -> 9\n"
                "   Forma()                        -> raise TypeError\n"
                "   isinstance(Quadrado(1), Forma) -> True\n\n"
                "ABC e @abstractmethod trabalham juntos:\n"
                "   - Forma herda de ABC\n"
                "   - area() fica decorado com @abstractmethod\n"
                "   - Tentar criar Forma() levanta TypeError automaticamente\n"
                "   - Quadrado implementa area() e pode ser instanciado\n\n"
                "O corpo do @abstractmethod pode ser 'pass' ou '...' —\n"
                "ele nunca e chamado diretamente, e so o contrato.\n\n"
                "Lembre: Quadrado(3).area() deve devolver 3*3 = 9"
            ),
            funcao="Forma",
            assinatura="from abc import ABC, abstractmethod\n\n\nclass Forma(ABC):",
            testes=[
                ("Quadrado(3).area()", "9"),
                ("Forma()", "!raise TypeError"),
                ("isinstance(Quadrado(1), Forma)", "True"),
            ],
            nivel="dificil",
            dica="Forma(ABC) com @abstractmethod def area. Quadrado(Forma) com def __init__(self, lado) e def area(self): return self.lado ** 2.",
        ),
    ],
    quiz=[
        Quiz(
            "O que @dataclass gera automaticamente a partir das anotacoes de tipo?",
            ["Apenas __init__",
             "__init__, __repr__ e __eq__ (e opcionalmente __lt__, __hash__ etc.)",
             "Apenas __repr__ e __str__",
             "Todos os dunders possiveis, sem excecao"],
            1,
            "Por padrao, @dataclass gera __init__ (com todos os campos como parametros), "
            "__repr__ (mostrando nome=valor de cada campo) e __eq__ (comparando todos os campos). "
            "Com order=True tambem gera __lt__, __le__, __gt__, __ge__. "
            "Com frozen=True tambem gera __hash__ e bloqueia atribuicao.",
        ),
        Quiz(
            "Por que Enum previne erros que strings comuns nao previnem?",
            ["Enums sao mais rapidos que strings",
             "Enums sao objetos unicos e verificaveis: erros de digitacao ou valores invalidos geram AttributeError/ValueError imediatamente",
             "Python converte strings para Enum automaticamente",
             "Enums so podem ter valores numericos, evitando ambiguidade"],
            1,
            "Status.PAGOO levanta AttributeError imediatamente — voce descobre o erro. "
            "status == 'Pago' falha silenciosamente se o correto for 'pago'. "
            "Enum garante que so os valores definidos existam, "
            "que comparacoes sejam por identidade (sem ambiguidade de case), "
            "e que iteracao sobre membros seja sempre completa.",
        ),
        Quiz(
            "Qual a diferenca principal entre NamedTuple e @dataclass(frozen=True)?",
            ["Nao ha diferenca — sao equivalentes em tudo",
             "NamedTuple herda de tuple (suporta desempacotamento, indexacao, len); @dataclass frozen nao e tupla mas e mais flexivel para metodos e heranca",
             "@dataclass frozen e imutavel; NamedTuple permite mutacao",
             "NamedTuple so aceita campos numericos"],
            1,
            "NamedTuple E uma tupla: x, y = ponto funciona, ponto[0] funciona, "
            "len(ponto) funciona. Isso e util quando voce precisa de compatibilidade com codigo que espera tuplas. "
            "@dataclass frozen nao e tupla: nao desempacota, nao indexa com []. "
            "Mas @dataclass suporta heranca completa, __post_init__, propriedades, etc.",
        ),
        Quiz(
            "Qual a vantagem de ABC sobre simplesmente usar raise NotImplementedError?",
            ["ABC e mais rapido",
             "ABC falha na CRIACAO do objeto se metodos abstratos nao foram implementados; NotImplementedError so falha quando o metodo e chamado",
             "NotImplementedError foi removido no Python 3.10",
             "Nao ha vantagem — sao equivalentes"],
            1,
            "Com NotImplementedError: Forma() funciona, o objeto e criado. "
            "O erro so aparece quando forma.area() e chamado — mais tarde, "
            "potencialmente longe do problema real. "
            "Com ABC: Forma() ja levanta TypeError — o erro ocorre o mais cedo possivel, "
            "facilitando depuracao. Principio: 'falhe cedo, falhe claramente'.",
        ),
    ],
    projeto=(
        "Crie sistema_pedidos.py combinando as ferramentas do dia:\n\n"
        "   from enum import Enum, auto\n"
        "   from dataclasses import dataclass, field\n"
        "   from abc import ABC, abstractmethod\n\n"
        "   class StatusPedido(Enum):\n"
        "       RASCUNHO, PENDENTE, PAGO, ENVIADO, ENTREGUE, CANCELADO\n"
        "       metodo: pode_cancelar() -> bool\n"
        "       metodo: proximo_status() -> StatusPedido | None\n\n"
        "   @dataclass\n"
        "   class Item:\n"
        "       nome: str\n"
        "       preco: float\n"
        "       quantidade: int = 1\n"
        "       subtotal: float = field(init=False)  # calculado\n\n"
        "   @dataclass\n"
        "   class Pedido:\n"
        "       cliente: str\n"
        "       itens: list = field(default_factory=list)\n"
        "       status: StatusPedido = StatusPedido.RASCUNHO\n"
        "       metodos: adicionar_item(), total(), avancar_status(), cancelar()\n\n"
        "   class Desconto(ABC):\n"
        "       @abstractmethod\n"
        "       def calcular(self, pedido: Pedido) -> float: ...\n\n"
        "   class DescontoPorcentagem(Desconto): ...\n"
        "   class DescontoFidelidade(Desconto): ...\n\n"
        "DEMONSTRACAO:\n"
        "   - Crie 3 pedidos com diferentes itens\n"
        "   - Avance os status de cada um\n"
        "   - Tente cancelar um que nao pode ser cancelado\n"
        "   - Aplique descontos usando polimorfismo\n"
        "   - Exiba relatorio final"
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/dataclasses.html — dataclasses",
        "docs.python.org/pt-br/3/library/enum.html — Enum",
        "docs.python.org/pt-br/3/library/abc.html — ABC e abstractmethod",
    ],
))

# ---------------------------------------------------------------- DIA 20
DIAS.append(Dia(
    numero=20,
    titulo="Iteradores, geradores e itertools",
    nivel="Intermediário",
    duracao="110 min",
    objetivos=[
        "Entender o protocolo de iteração: o que torna algo iterável em Python",
        "Distinguir iterável de iterador e por que a diferença importa",
        "Criar geradores com yield e entender como a execução é pausada e retomada",
        "Usar yield from para delegar a outro iterável",
        "Conhecer as ferramentas mais úteis do itertools para processamento eficiente",
        "Escolher entre lista, gerador e itertools para cada situação",
    ],
    teoria="""
Nos Dias 7 e 10 você usou for loops e expressões geradoras. Hoje vamos
entender o mecanismo por baixo: o PROTOCOLO DE ITERAÇÃO — o que permite
que listas, strings, dicionários, arquivos e objetos customizados sejam
percorridos com for da mesma forma.

---------------------------------------------------------------------------
1. O protocolo de iteração: iterável vs iterador
---------------------------------------------------------------------------
Python separa dois conceitos que parecem iguais mas são distintos:

ITERÁVEL: qualquer objeto que pode ser percorrido com for.
    Exemplos: list, str, dict, tuple, set, range, arquivo aberto.
    Requisito: ter o método __iter__() que retorna um ITERADOR.

ITERADOR: o objeto que faz a iteração acontecer de fato.
    Requisito: ter __iter__() (retorna a si mesmo) e __next__()
    (retorna o próximo valor ou levanta StopIteration).

    # O que o for faz por baixo dos panos:
    lista = [1, 2, 3]

    iterador = iter(lista)        # chama lista.__iter__()
    print(next(iterador))         # 1  — chama iterador.__next__()
    print(next(iterador))         # 2
    print(next(iterador))         # 3
    print(next(iterador))         # StopIteration — for captura isso e para

    # O for é equivalente a:
    iterador = iter(lista)
    while True:
        try:
            item = next(iterador)
            # corpo do for
        except StopIteration:
            break

DIFERENÇA PRÁTICA: listas são iteráveis, não iteradores.
    Você pode percorrer uma lista várias vezes.
    Um iterador é de uso único — após esgotar, não reinicia.

    lista = [1, 2, 3]
    for x in lista: print(x)   # 1 2 3
    for x in lista: print(x)   # 1 2 3 — funciona de novo!

    it = iter(lista)
    for x in it: print(x)      # 1 2 3
    for x in it: print(x)      # (nada) — esgotado!

---------------------------------------------------------------------------
2. Criando um iterador com classes
---------------------------------------------------------------------------
Você pode tornar qualquer classe iterável implementando __iter__ e __next__:

    class Contagem:
        def __init__(self, inicio, fim):
            self.atual = inicio
            self.fim = fim

        def __iter__(self):
            return self    # o próprio objeto é o iterador

        def __next__(self):
            if self.atual >= self.fim:
                raise StopIteration
            valor = self.atual
            self.atual += 1
            return valor

    for n in Contagem(1, 4):
        print(n)    # 1  2  3

    list(Contagem(5, 8))   # [5, 6, 7]

Implementar o protocolo manualmente é trabalhoso. Na prática, usamos
GERADORES — que fazem tudo isso automaticamente.

---------------------------------------------------------------------------
3. Geradores com yield: iteradores fáceis de escrever
---------------------------------------------------------------------------
Um gerador é uma função que usa yield em vez de return. Quando chamada,
ela não executa o corpo imediatamente — retorna um OBJETO GERADOR que
implementa o protocolo de iteração automaticamente.

    def contar(inicio, fim):
        atual = inicio
        while atual < fim:
            yield atual      # pausa aqui e entrega o valor
            atual += 1       # retoma aqui na próxima chamada de next()

    for n in contar(1, 4):
        print(n)    # 1  2  3

    list(contar(5, 8))   # [5, 6, 7]

COMO O YIELD FUNCIONA:
    1. Ao chamar contar(1, 4), o corpo NÃO executa — retorna um gerador.
    2. Na primeira chamada de next(), executa até o yield, entrega 1 e PAUSA.
    3. O estado local (atual, inicio, fim) é preservado entre chamadas.
    4. Na segunda chamada de next(), RETOMA de onde parou, incrementa e yield 2.
    5. Quando while termina, a função encerra e StopIteration é levantado.

GERADOR É UM ITERADOR: um objeto gerador implementa __iter__ e __next__
automaticamente. Tudo que você pode fazer com um iterador, pode fazer
com um gerador.

GERADOR VERSUS FUNÇÃO NORMAL:

    def normal(n):
        return [x * 2 for x in range(n)]   # cria TODA a lista de uma vez

    def gerador(n):
        for x in range(n):
            yield x * 2                    # produz um valor por vez

    # Para n=1.000.000:
    # normal: aloca memória para 1M inteiros (~8MB)
    # gerador: aloca memória para 1 inteiro de cada vez (~200 bytes)

---------------------------------------------------------------------------
4. yield from: delegando para outro iterável
---------------------------------------------------------------------------
yield from delega a produção de valores para outro iterável ou gerador,
equivalendo a um loop de yield:

    # Sem yield from
    def achatar(lista):
        for sublista in lista:
            for item in sublista:
                yield item

    # Com yield from (equivalente)
    def achatar(lista):
        for sublista in lista:
            yield from sublista    # delega cada sublista

    list(achatar([[1, 2], [3, 4], [5]]))    # [1, 2, 3, 4, 5]

yield from também funciona com qualquer iterável, não só listas:

    def encadear(*iteraveis):
        for iteravel in iteraveis:
            yield from iteravel

    list(encadear([1, 2], "AB", range(3)))   # [1, 2, 'A', 'B', 0, 1, 2]

---------------------------------------------------------------------------
5. Geradores infinitos: sequências sem fim
---------------------------------------------------------------------------
Geradores podem ser infinitos — eles produzem valores indefinidamente
e você para quando quiser:

    def naturais():
        n = 0
        while True:        # loop infinito intencional
            yield n
            n += 1

    def fibonacci_infinito():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    # Consumindo com next() manual
    gen = naturais()
    print(next(gen))   # 0
    print(next(gen))   # 1
    print(next(gen))   # 2

    # Ou com islice para pegar N elementos
    from itertools import islice
    print(list(islice(naturais(), 5)))          # [0, 1, 2, 3, 4]
    print(list(islice(fibonacci_infinito(), 8))) # [0, 1, 1, 2, 3, 5, 8, 13]

ATENÇÃO: nunca use list() ou for sem limite em um gerador infinito.
Isso tentaria gerar infinitos valores e travaria o programa.

---------------------------------------------------------------------------
6. itertools: ferramentas para iteração eficiente
---------------------------------------------------------------------------
O módulo itertools oferece funções de iteração preguiçosas (lazy) —
todas produzem valores sob demanda, sem criar listas intermediárias.

ITERTOOLS MAIS USADOS:

    from itertools import (
        count, cycle, repeat,
        chain, islice, takewhile, dropwhile,
        product, permutations, combinations,
        groupby, accumulate, starmap
    )

GERADORES INFINITOS:

    count(start, step)    conta de start em step infinitamente
    cycle(iteravel)       repete o iterável infinitamente
    repeat(obj, n)        repete obj n vezes (ou infinitamente)

    list(islice(count(10, 2), 5))   # [10, 12, 14, 16, 18]
    list(islice(cycle("AB"), 6))    # ['A', 'B', 'A', 'B', 'A', 'B']

FILTRAGEM E SELEÇÃO:

    islice(iteravel, n)           primeiros n elementos
    islice(iteravel, start, stop) fatia sem criar lista
    takewhile(pred, iteravel)     pega enquanto pred for True
    dropwhile(pred, iteravel)     pula enquanto pred for True

    list(takewhile(lambda x: x < 5, [1, 3, 5, 2]))  # [1, 3]
    list(dropwhile(lambda x: x < 5, [1, 3, 5, 2]))  # [5, 2]

COMBINAÇÃO:

    chain(*iteraveis)             une iteráveis em sequência
    chain.from_iterable(it)       achata um nível de aninhamento
    product(a, b)                 produto cartesiano
    permutations(it, r)           permutações de tamanho r
    combinations(it, r)           combinações sem repetição

    list(chain([1, 2], [3, 4], [5]))    # [1, 2, 3, 4, 5]
    list(product("AB", repeat=2))       # AA, AB, BA, BB
    list(permutations([1, 2, 3], 2))    # (1,2),(1,3),(2,1),(2,3),(3,1),(3,2)
    list(combinations([1, 2, 3], 2))    # (1,2),(1,3),(2,3)

ACUMULAÇÃO E AGRUPAMENTO:

    accumulate(iteravel, func)   acumula aplicando func (padrão: soma)
    groupby(iteravel, key)       agrupa elementos consecutivos iguais

    from itertools import accumulate
    list(accumulate([1, 2, 3, 4, 5]))           # [1, 3, 6, 10, 15]  somas parciais
    list(accumulate([1, 2, 3, 4], lambda a, b: a * b))  # [1, 2, 6, 24]  fatorial

    # groupby: EXIGE que os dados estejam ordenados pela chave
    from itertools import groupby
    dados = sorted([("A", 1), ("B", 2), ("A", 3)], key=lambda x: x[0])
    for chave, grupo in groupby(dados, key=lambda x: x[0]):
        print(chave, list(grupo))
    # A [('A', 1), ('A', 3)]
    # B [('B', 2)]

---------------------------------------------------------------------------
7. Expressão geradora vs lista: a escolha certa
---------------------------------------------------------------------------
A regra para escolher:

    USE LISTA quando:
    - Precisa do resultado mais de uma vez
    - Precisa de len(), indexação ou fatiamento
    - O resultado é pequeno e você quer simplicidade

    USE GERADOR quando:
    - Processa uma vez e descarta
    - O resultado é grande (memória importa)
    - Passa direto para sum(), any(), all(), max(), min()
    - Compõe com outras funções lazy (pipeline de transformações)

    # Memória: a diferença pode ser enorme
    import sys
    lista_g = [x**2 for x in range(1_000_000)]
    gen_g   = (x**2 for x in range(1_000_000))

    print(sys.getsizeof(lista_g))   # ~8.5 MB
    print(sys.getsizeof(gen_g))     # ~200 bytes

    # Resultado idêntico para operações de redução
    sum(lista_g) == sum(gen_g)     # True (mas gen_g já foi consumido!)
""",
    exemplos=[
        Exemplo(
            titulo="Geradores na prática: Fibonacci e janelas deslizantes",
            codigo='''def fibonacci_infinito():
    """Gerador infinito da sequencia de Fibonacci."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def janelas_deslizantes(seq, n):
    """Produz janelas de tamanho n deslizando sobre seq."""
    seq = list(seq)    # garante indexacao
    for i in range(len(seq) - n + 1):
        yield tuple(seq[i:i+n])

from itertools import islice

# Primeiros 10 Fibonacci
print("Fibonacci:", list(islice(fibonacci_infinito(), 10)))

# Verificando se um Fibonacci e par
gen = fibonacci_infinito()
pares = (x for x in islice(gen, 20) if x % 2 == 0)
print("Fibonacci pares:", list(pares))

# Janelas deslizantes: util para analise de sequencias
dados = [1, 3, 5, 7, 9, 11]
print("Janelas de 3:", list(janelas_deslizantes(dados, 3)))
print("Medias moveis:", [
    sum(j) / len(j)
    for j in janelas_deslizantes(dados, 3)
])
''',
            explicacao="fibonacci_infinito é seguro porque não cria nenhuma lista: "
                       "islice controla quantos valores consumir. "
                       "A expressão geradora 'pares' compõe com islice de forma lazy: "
                       "nenhuma das duas cria uma lista intermediária. "
                       "janelas_deslizantes é útil para médias móveis e análise "
                       "de tendências em séries temporais.",
        ),
        Exemplo(
            titulo="Pipeline lazy com geradores encadeados",
            codigo='''# Processamento de logs linha por linha — sem carregar o arquivo inteiro
import io

# Simula um arquivo de log grande
log_simulado = io.StringIO("""
2024-01-15 INFO usuario Ana fez login
2024-01-15 ERROR banco de dados indisponivel
2024-01-15 INFO usuario Bruno fez logout
2024-01-15 WARNING disco com 90% de uso
2024-01-15 ERROR timeout na conexao
2024-01-15 INFO relatorio gerado com sucesso
""".strip())

def ler_linhas(arquivo):
    for linha in arquivo:
        yield linha.strip()

def filtrar_nivel(linhas, nivel):
    for linha in linhas:
        if nivel in linha:
            yield linha

def extrair_mensagem(linhas):
    for linha in linhas:
        partes = linha.split(" ", 2)   # data hora nivel mensagem
        if len(partes) >= 3:
            yield partes[2]            # so a mensagem

# Pipeline: cada gerador processa a saida do anterior
# Nenhum carrega o arquivo inteiro na memoria!
linhas = ler_linhas(log_simulado)
erros  = filtrar_nivel(linhas, "ERROR")
msgs   = extrair_mensagem(erros)

print("Mensagens de erro:")
for msg in msgs:
    print(f"  -> {msg}")
''',
            explicacao="Cada função é um estágio do pipeline. "
                       "Nenhuma cria uma lista intermediária — o processamento "
                       "é totalmente lazy: a linha só é lida quando solicitada. "
                       "Para um arquivo de 10GB, esse pipeline usa a mesma "
                       "quantidade de memória que para um arquivo de 10 linhas. "
                       "Este padrão é a essência do processamento de streams.",
        ),
        Exemplo(
            titulo="itertools na prática",
            codigo='''from itertools import (
    chain, islice, groupby, accumulate,
    combinations, product, takewhile
)

# chain: une iteraveis sem criar lista intermediaria
todos = list(chain([1, 2], [3, 4], range(5, 8)))
print("chain:", todos)   # [1, 2, 3, 4, 5, 6, 7]

# accumulate: somas parciais (util para saldos)
movimentos = [1000, -200, 500, -150, 300]
saldos = list(accumulate(movimentos))
print("Saldos:", saldos)   # [1000, 800, 1300, 1150, 1450]

# groupby: agrupar por categoria (dados devem estar ordenados!)
vendas = [
    ("Norte", 100), ("Norte", 200),
    ("Sul", 150),   ("Sul",   50),
    ("Norte", 300),  # ATENCAO: nao consecutivo — cria novo grupo!
]
for regiao, grupo in groupby(vendas, key=lambda v: v[0]):
    total = sum(v[1] for v in grupo)
    print(f"{regiao}: R${total}")

print()
# Para agrupar corretamente: ordene primeiro!
for regiao, grupo in groupby(sorted(vendas), key=lambda v: v[0]):
    total = sum(v[1] for v in grupo)
    print(f"{regiao} (ordenado): R${total}")

# combinations: pares possiveis em um torneio
times = ["Flamengo", "Santos", "Gremio", "Atletico"]
print("Partidas:", len(list(combinations(times, 2))))
''',
            explicacao="chain une sequências sem criar lista: eficiente para "
                       "concatenar muitas coleções pequenas. "
                       "accumulate com padrão soma é perfeito para saldos e "
                       "totais acumulados. "
                       "groupby tem uma armadilha clássica: agrupa apenas "
                       "elementos CONSECUTIVOS iguais. Sempre ordene antes "
                       "com sorted() pela mesma chave.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d20e1",
            enunciado=(
                "Escreva a funcao geradora pares_ate(n) que produz\n"
                "todos os numeros PARES de 0 ate n-1 (exclusive).\n\n"
                "Exemplos:\n"
                "   list(pares_ate(10)) -> [0, 2, 4, 6, 8]\n"
                "   list(pares_ate(1))  -> [0]   (0 e par e < 1)\n"
                "   list(pares_ate(0))  -> []    (range(0) e vazio)\n\n"
                "Use yield dentro de um for com range:\n"
                "   for i in range(n):\n"
                "       if i % 2 == 0:\n"
                "           yield i\n\n"
                "Ou de forma mais direta usando range com passo 2:\n"
                "   for i in range(0, n, 2):\n"
                "       yield i\n\n"
                "Lembre: uma funcao com yield e um GERADOR.\n"
                "Ao chamar pares_ate(10), o corpo NAO executa.\n"
                "O corpo executa aos poucos quando voce itera (for, list, next)."
            ),
            funcao="pares_ate",
            assinatura="def pares_ate(n):",
            testes=[
                ("list(pares_ate(10))", "[0, 2, 4, 6, 8]"),
                ("list(pares_ate(1))", "[0]"),
                ("list(pares_ate(0))", "[]"),
            ],
            dica="for i in range(0, n, 2): yield i",
        ),
        Exercicio(
            id="d20e2",
            enunciado=(
                "Escreva a funcao geradora fibonacci(n) que produz\n"
                "os primeiros n numeros da sequencia de Fibonacci.\n\n"
                "A sequencia comeca em 0, 1, 1, 2, 3, 5, 8, 13...\n"
                "Cada numero e a soma dos dois anteriores.\n\n"
                "Exemplos:\n"
                "   list(fibonacci(7)) -> [0, 1, 1, 2, 3, 5, 8]\n"
                "   list(fibonacci(1)) -> [0]\n"
                "   list(fibonacci(0)) -> []\n\n"
                "Estrategia:\n"
                "   a, b = 0, 1           <- inicializa os dois primeiros\n"
                "   for _ in range(n):    <- repete exatamente n vezes\n"
                "       yield a           <- entrega o valor atual\n"
                "       a, b = b, a + b   <- avanca para o proximo par\n\n"
                "Rastreando para n=4:\n"
                "   iter 1: yield 0, depois a=1, b=1\n"
                "   iter 2: yield 1, depois a=1, b=2\n"
                "   iter 3: yield 1, depois a=2, b=3\n"
                "   iter 4: yield 2, depois a=3, b=5\n"
                "   resultado: [0, 1, 1, 2]"
            ),
            funcao="fibonacci",
            assinatura="def fibonacci(n):",
            testes=[
                ("list(fibonacci(7))", "[0, 1, 1, 2, 3, 5, 8]"),
                ("list(fibonacci(1))", "[0]"),
                ("list(fibonacci(0))", "[]"),
            ],
            nivel="medio",
            dica="a, b = 0, 1; for _ in range(n): yield a; a, b = b, a + b",
        ),
        Exercicio(
            id="d20e3",
            enunciado=(
                "Escreva a funcao geradora janelas(seq, n) que produz\n"
                "todas as janelas (subsequencias) de tamanho n de seq.\n\n"
                "Exemplos:\n"
                "   list(janelas([1, 2, 3, 4], 2)) -> [(1,2), (2,3), (3,4)]\n"
                "   list(janelas([1, 2], 3))        -> []   (janela maior que seq)\n"
                "   list(janelas([1, 2, 3], 3))     -> [(1, 2, 3)]\n\n"
                "Estrategia:\n"
                "   seq = list(seq)               <- garante indexacao\n"
                "   for i in range(len(seq) - n + 1):\n"
                "       yield tuple(seq[i:i+n])   <- fatia de i ate i+n\n\n"
                "Rastreando janelas([1,2,3,4], 2):\n"
                "   len=4, n=2, range(4-2+1) = range(3) = 0,1,2\n"
                "   i=0: seq[0:2] = [1,2] -> (1,2)\n"
                "   i=1: seq[1:3] = [2,3] -> (2,3)\n"
                "   i=2: seq[2:4] = [3,4] -> (3,4)\n\n"
                "Caso janela maior que seq: range(len-n+1) = range(negativo)\n"
                "range de numero negativo e vazio, entao o gerador nao produz nada."
            ),
            funcao="janelas",
            assinatura="def janelas(seq, n):",
            testes=[
                ("list(janelas([1, 2, 3, 4], 2))", "[(1, 2), (2, 3), (3, 4)]"),
                ("list(janelas([1, 2], 3))", "[]"),
                ("list(janelas([1, 2, 3], 3))", "[(1, 2, 3)]"),
            ],
            nivel="dificil",
            dica="seq = list(seq); for i in range(len(seq) - n + 1): yield tuple(seq[i:i+n])",
        ),
    ],
    quiz=[
        Quiz(
            "Qual a diferenca entre um ITERAVEL e um ITERADOR?",
            ["Sao sinonimos — qualquer objeto que funciona no for e um iterador",
             "Iteravel tem __iter__ que retorna um iterador; iterador tem __next__ e se esgota apos percorrido",
             "Iteravel so funciona com for; iterador so funciona com next()",
             "Listas sao iteradores; geradores sao iteraveis"],
            1,
            "Lista e iteravel: pode gerar um novo iterador a cada for. "
            "iter(lista) retorna um novo iterador cada vez que e chamado. "
            "Iterador e o objeto que guarda a posicao atual: depois de esgotado, "
            "percorrer de novo nao produz nada. "
            "Geradores sao iteradores: de uso unico.",
        ),
        Quiz(
            "O que acontece quando uma funcao geradora executa um yield?",
            ["A funcao encerra e o valor e retornado permanentemente",
             "A execucao e PAUSADA, o valor e entregue ao chamador, e o estado local e preservado ate o proximo next()",
             "A funcao reinicia do inicio na proxima chamada",
             "Um TypeError e levantado se yield for usado fora de um loop"],
            1,
            "yield pausa a execucao preservando todo o estado local "
            "(variaveis, posicao no codigo, contexto). "
            "Na proxima chamada de next(), a execucao RETOMA exatamente de onde parou. "
            "Isso e o que torna geradores eficientes: nao calculam nada antes de ser pedido.",
        ),
        Quiz(
            "Por que groupby do itertools exige que os dados estejam ordenados?",
            ["E uma limitacao tecnica que sera corrigida em versoes futuras",
             "groupby agrupa apenas elementos CONSECUTIVOS iguais — dados nao ordenados criam multiplos grupos para o mesmo valor",
             "groupby exige ordenacao apenas quando a chave e uma string",
             "Nao exige ordenacao — e um mito popular"],
            2,
            "groupby percorre o iteravel uma vez e cria um novo grupo sempre que "
            "o valor da chave MUDA. Se a=1,b=2,a=3 (nao ordenado), cria 3 grupos: "
            "um para 'a', um para 'b', outro para 'a'. "
            "Sempre use sorted(dados, key=sua_chave) antes de groupby(dados, key=sua_chave).",
        ),
        Quiz(
            "Quando um gerador e preferivel a uma lista por compreensao?",
            ["Sempre — geradores sao sempre mais rapidos e mais eficientes",
             "Quando o resultado sera percorrido uma unica vez e/ou o conjunto de dados e muito grande para caber na memoria",
             "Nunca — listas sao sempre preferidas por serem mais simples",
             "Apenas quando se usa itertools junto"],
            1,
            "Lista: calcula e armazena TUDO imediatamente. "
            "Gerador: calcula um valor por vez, sob demanda. "
            "Se voce vai percorrer uma vez e jogar fora (sum, any, all, max), "
            "o gerador evita alocar memoria desnecessaria. "
            "Se voce vai usar o resultado multiplas vezes ou precisa de len/indexacao, "
            "use lista.",
        ),
    ],
    projeto=(
        "Crie pipeline_dados.py com um sistema de processamento em pipeline:\n\n"
        "   GERADORES BASE:\n"
        "   1. ler_csv(texto) -> itera sobre as linhas como dicts\n"
        "      (use csv.DictReader e io.StringIO do Dia 14)\n\n"
        "   2. filtrar(registros, campo, valor) -> so os que batem\n"
        "      exemplo: filtrar(registros, 'regiao', 'Norte')\n\n"
        "   3. transformar(registros, campo, funcao) -> aplica funcao ao campo\n"
        "      exemplo: transformar(registros, 'valor', float)\n\n"
        "   4. limitar(registros, n) -> so os primeiros n\n\n"
        "   PIPELINE FINAL:\n"
        "   dados_csv = 'produto,regiao,valor\\n...'\n"
        "   pipeline = limitar(\n"
        "       filtrar(\n"
        "           transformar(ler_csv(dados_csv), 'valor', float),\n"
        "           'regiao', 'Norte'\n"
        "       ),\n"
        "       5\n"
        "   )\n\n"
        "   ANALISE:\n"
        "   Usando apenas itertools (sem criar listas intermediarias):\n"
        "   - Total de vendas por regiao (groupby apos sort)\n"
        "   - Saldo acumulado ao longo do tempo (accumulate)\n"
        "   - Todas as combinacoes de produto+regiao (product)\n\n"
        "BONUS: meça o tempo e memória de cada abordagem:\n"
        "   pipeline lazy vs listas intermediarias com timeit e tracemalloc."
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/itertools.html — itertools completo",
        "docs.python.org/pt-br/3/glossary.html#term-generator — definicao de gerador",
        "PEP 255 — Simple Generators (yield)",
    ],
))

# ---------------------------------------------------------------- DIA 21
DIAS.append(Dia(
    numero=21,
    titulo="Decoradores e functools",
    nivel="Avançado",
    duracao="120 min",
    objetivos=[
        "Entender o que um decorador faz mecanicamente: é uma função que transforma outra função",
        "Escrever decoradores simples e decoradores que aceitam argumentos",
        "Usar @functools.wraps para preservar a identidade da função decorada",
        "Aplicar decoradores de classe e empilhar múltiplos decoradores",
        "Usar functools.lru_cache, functools.partial e functools.reduce com consciência",
        "Reconhecer padrões onde decoradores são a solução mais elegante",
    ],
    teoria="""
No Dia 12 você aprendeu que funções são objetos de primeira classe:
podem ser passadas como argumento e retornadas de outras funções.
Decoradores são uma aplicação direta desse conceito — uma sintaxe
elegante para transformar funções sem modificar seu código.

---------------------------------------------------------------------------
1. O que é um decorador: mecanicamente
---------------------------------------------------------------------------
Um decorador é simplesmente uma função que recebe uma função e retorna
outra função (ou qualquer callable). A sintaxe com @ é açúcar sintático:

    @decorador
    def minha_funcao():
        pass

    # É EXATAMENTE equivalente a:
    def minha_funcao():
        pass
    minha_funcao = decorador(minha_funcao)

O decorador recebe a função original, faz algo com ela (geralmente
cria uma nova função que a envolve) e retorna o resultado.

O PADRÃO MAIS COMUM — função envelope (wrapper):

    def meu_decorador(func):
        def envelope(*args, **kwargs):        # aceita qualquer assinatura
            print(f"Antes de {func.__name__}")
            resultado = func(*args, **kwargs)  # chama a original
            print(f"Depois de {func.__name__}")
            return resultado
        return envelope    # retorna a função nova, sem chamar

    @meu_decorador
    def saudar(nome):
        return f"Olá, {nome}!"

    saudar("Ana")
    # Antes de saudar
    # Depois de saudar
    # 'Olá, Ana!'

Rastreando o que acontece:
    1. def saudar define a função original
    2. @meu_decorador chama meu_decorador(saudar)
    3. Dentro: envelope é criada, capturando func=saudar (closure!)
    4. envelope é retornada e atribuída ao nome saudar
    5. saudar agora aponta para envelope, não para a função original

---------------------------------------------------------------------------
2. @functools.wraps: preservando a identidade
---------------------------------------------------------------------------
Sem @functools.wraps, o envelope rouba a identidade da função original:

    @meu_decorador
    def saudar(nome):
        \"\"\"Cumprimenta pelo nome.\"\"\"
        return f"Olá, {nome}!"

    print(saudar.__name__)   # 'envelope'  — ERRADO!
    print(saudar.__doc__)    # None         — docstring perdida!
    help(saudar)             # mostra info de envelope, não de saudar

Com @functools.wraps(func), o envelope "rouba" os metadados da original:

    import functools

    def meu_decorador(func):
        @functools.wraps(func)     # copia __name__, __doc__, __module__...
        def envelope(*args, **kwargs):
            resultado = func(*args, **kwargs)
            return resultado
        return envelope

    @meu_decorador
    def saudar(nome):
        \"\"\"Cumprimenta pelo nome.\"\"\"
        return f"Olá, {nome}!"

    print(saudar.__name__)   # 'saudar'          — correto!
    print(saudar.__doc__)    # 'Cumprimenta...'  — correto!
    saudar.__wrapped__       # acesso à função original

REGRA: sempre use @functools.wraps(func) em todo decorador que você
escrever. É uma linha que custa nada e evita muitos bugs sutis.

---------------------------------------------------------------------------
3. Decoradores com argumentos: a fábrica de decoradores
---------------------------------------------------------------------------
Um decorador simples recebe a função. Para aceitar argumentos próprios,
você precisa de mais um nível de aninhamento — uma fábrica que retorna
o decorador:

    # Decorador simples
    @decorador
    def func(): ...

    # Decorador com argumentos
    @decorador(arg1, arg2)
    def func(): ...

    # Equivalente:
    # func = decorador(arg1, arg2)(func)
    # Três passos: decorador(args) -> retorna um decorador -> decorador(func) -> retorna envelope

EXEMPLO: decorador de retry (tentar N vezes em caso de falha)

    import functools, time

    def retry(vezes=3, espera=1.0):           # nível 1: fábrica
        def decorador(func):                   # nível 2: decorador real
            @functools.wraps(func)
            def envelope(*args, **kwargs):     # nível 3: envelope
                for tentativa in range(1, vezes + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if tentativa == vezes:
                            raise
                        print(f"Tentativa {tentativa} falhou: {e}. Aguardando...")
                        time.sleep(espera)
            return envelope
        return decorador

    @retry(vezes=3, espera=0.5)
    def conectar_banco():
        # código que pode falhar
        pass

    # Equivalente:
    # conectar_banco = retry(vezes=3, espera=0.5)(conectar_banco)

---------------------------------------------------------------------------
4. Empilhando decoradores
---------------------------------------------------------------------------
Você pode aplicar vários decoradores à mesma função. A ordem de aplicação
é de BAIXO para CIMA (o mais próximo da função é aplicado primeiro):

    @decorador_a
    @decorador_b
    @decorador_c
    def func():
        pass

    # Equivalente a:
    # func = decorador_a(decorador_b(decorador_c(func)))

    import functools

    def negrito(func):
        @functools.wraps(func)
        def envelope(*args, **kwargs):
            return f"<b>{func(*args, **kwargs)}</b>"
        return envelope

    def italico(func):
        @functools.wraps(func)
        def envelope(*args, **kwargs):
            return f"<i>{func(*args, **kwargs)}</i>"
        return envelope

    @negrito
    @italico
    def texto():
        return "Python"

    texto()    # '<b><i>Python</i></b>'
    # italico é aplicado primeiro (mais próximo), negrito depois

A ordem importa: @negrito @italico produz <b><i>...</i></b>.
@italico @negrito produziria <i><b>...</b></i>.

---------------------------------------------------------------------------
5. Decoradores de classe e para classes
---------------------------------------------------------------------------
Decoradores funcionam em classes também:

    # Decorando uma classe
    def registrar(cls):
        print(f"Classe registrada: {cls.__name__}")
        return cls

    @registrar
    class Produto:
        pass
    # imprime: Classe registrada: Produto

    # Usando uma classe como decorador (deve implementar __call__)
    class Cronometrar:
        def __init__(self, func):
            functools.wraps(func)(self)
            self.func = func
            self.tempo_total = 0

        def __call__(self, *args, **kwargs):
            import time
            inicio = time.perf_counter()
            resultado = self.func(*args, **kwargs)
            self.tempo_total += time.perf_counter() - inicio
            return resultado

    @Cronometrar
    def calcular(n):
        return sum(range(n))

    calcular(1_000_000)
    print(calcular.tempo_total)  # tempo gasto no último chamada

---------------------------------------------------------------------------
6. functools: ferramentas para funções
---------------------------------------------------------------------------
O módulo functools vai além do wraps. As ferramentas mais úteis:

FUNCTOOLS.LRU_CACHE: memoização automática

    from functools import lru_cache

    @lru_cache(maxsize=None)   # None = cache ilimitado
    def fib(n):
        if n < 2:
            return n
        return fib(n-1) + fib(n-2)

    fib(100)   # instantâneo! sem cache, levaria mais tempo que a vida do universo

    fib.cache_info()     # CacheInfo(hits=98, misses=101, maxsize=None, currsize=101)
    fib.cache_clear()    # limpa o cache

QUANDO USAR: funções puras (sem efeitos colaterais) que são chamadas
com os mesmos argumentos repetidamente. Fibonacci, análise de árvores,
Problemas de programação dinâmica.
ATENÇÃO: argumentos devem ser hasheáveis (strings, números, tuplas).

FUNCTOOLS.PARTIAL: congelando argumentos

    from functools import partial

    def potencia(base, expoente):
        return base ** expoente

    quadrado  = partial(potencia, expoente=2)   # congela expoente=2
    cubo      = partial(potencia, expoente=3)
    dobrar    = partial(potencia, expoente=1, base=2)  # base e expoente fixos

    quadrado(5)    # 25
    cubo(3)        # 27

    # Útil com map, filter e sorted
    lista = [3, 1, 4, 1, 5]
    sorted(lista, key=partial(potencia, expoente=2))  # ordena pelo quadrado

FUNCTOOLS.REDUCE: acumulando com uma função binária

    from functools import reduce

    # Equivale a: ((1 + 2) + 3) + 4
    reduce(lambda acc, x: acc + x, [1, 2, 3, 4])   # 10

    # Produto: 1 * 2 * 3 * 4 * 5 = 120
    reduce(lambda acc, x: acc * x, range(1, 6))

    # Valor inicial explícito
    reduce(lambda acc, x: acc + x, [], 0)   # 0 (sem valor inicial, lista vazia causaria TypeError)

FUNCTOOLS.SINGLEDISPATCH: despacho por tipo

    from functools import singledispatch

    @singledispatch
    def processar(valor):
        raise TypeError(f"Tipo não suportado: {type(valor)}")

    @processar.register(int)
    def _(valor):
        return valor * 2

    @processar.register(str)
    def _(valor):
        return valor.upper()

    @processar.register(list)
    def _(valor):
        return [processar(x) for x in valor]

    processar(5)           # 10
    processar("oi")        # 'OI'
    processar([1, "a"])    # [2, 'A']

---------------------------------------------------------------------------
7. Padrões clássicos de decoradores
---------------------------------------------------------------------------

    PADRÃO 1 — Logging: registrar cada chamada
    PADRÃO 2 — Timing: medir tempo de execução
    PADRÃO 3 — Validação: checar pré-condições
    PADRÃO 4 — Cache: memoizar resultados (lru_cache)
    PADRÃO 5 — Retry: tentar novamente em caso de falha
    PADRÃO 6 — Rate limiting: limitar frequência de chamadas
    PADRÃO 7 — Autenticação: exigir permissão (frameworks web)

Frameworks como Flask, FastAPI e Django usam decoradores extensivamente:
@app.route('/'), @login_required, @cache, @validator são todos
decoradores que adicionam comportamento sem modificar o código da função.
""",
    exemplos=[
        Exemplo(
            titulo="Decoradores essenciais: timing e validação",
            codigo='''import functools
import time

def cronometrar(func):
    """Mede e exibe o tempo de execucao."""
    @functools.wraps(func)
    def envelope(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        duracao = time.perf_counter() - inicio
        print(f"{func.__name__}: {duracao:.4f}s")
        return resultado
    return envelope

def validar_positivo(func):
    """Garante que todos os argumentos numericos sao positivos."""
    @functools.wraps(func)
    def envelope(*args, **kwargs):
        for i, arg in enumerate(args):
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError(
                    f"Argumento {i+1} de {func.__name__} deve ser positivo: {arg}"
                )
        return func(*args, **kwargs)
    return envelope

@cronometrar
@validar_positivo
def calcular_raiz(n, precisao=10):
    """Calcula raiz quadrada de n com a precisao dada."""
    import math
    return round(math.sqrt(n), precisao)

print(calcular_raiz(2))
print(calcular_raiz(144))

try:
    calcular_raiz(-5)
except ValueError as e:
    print(f"Erro: {e}")

# wraps preserva a identidade
print(calcular_raiz.__name__)   # 'calcular_raiz' -- correto!
print(calcular_raiz.__doc__)    # 'Calcula raiz...' -- correto!
''',
            explicacao="Os decoradores são aplicados de baixo para cima: "
                       "validar_positivo é aplicado primeiro (mais próximo da função), "
                       "cronometrar depois. Na execução, cronometrar chama validar_positivo "
                       "que chama calcular_raiz. "
                       "@functools.wraps preserva __name__ e __doc__ em ambos. "
                       "isinstance(arg, (int, float)) verifica se é número antes de comparar.",
        ),
        Exemplo(
            titulo="Decorador com argumentos: fábrica de decoradores",
            codigo='''import functools

def repetir(vezes):
    """Fabrica de decorador: repete a funcao 'vezes' vezes."""
    def decorador(func):
        @functools.wraps(func)
        def envelope(*args, **kwargs):
            resultados = []
            for _ in range(vezes):
                resultados.append(func(*args, **kwargs))
            return resultados
        return envelope
    return decorador

def limitar_chamadas(maximo):
    """Impede que a funcao seja chamada mais de 'maximo' vezes."""
    def decorador(func):
        @functools.wraps(func)
        def envelope(*args, **kwargs):
            if envelope.chamadas >= maximo:
                raise RuntimeError(
                    f"{func.__name__} excedeu o limite de {maximo} chamadas"
                )
            envelope.chamadas += 1
            return func(*args, **kwargs)
        envelope.chamadas = 0
        return envelope
    return decorador

@repetir(3)
def ola(nome):
    return f"Ola, {nome}!"

print(ola("Ana"))   # ['Ola, Ana!', 'Ola, Ana!', 'Ola, Ana!']

@limitar_chamadas(2)
def buscar_api(endpoint):
    return f"dados de {endpoint}"

print(buscar_api("/usuarios"))
print(buscar_api("/produtos"))
try:
    buscar_api("/pedidos")   # terceira chamada!
except RuntimeError as e:
    print(f"Limite: {e}")
''',
            explicacao="repetir é uma fábrica: retorna um decorador (não o envelope diretamente). "
                       "Três níveis de aninhamento: fábrica -> decorador -> envelope. "
                       "limitar_chamadas usa um atributo no próprio envelope (envelope.chamadas) "
                       "como estado persistente entre chamadas — uma técnica elegante "
                       "para adicionar estado a funções sem usar variáveis globais.",
        ),
        Exemplo(
            titulo="functools na prática: cache, partial e reduce",
            codigo='''from functools import lru_cache, partial, reduce

# LRU_CACHE: fibonacci com memoizacao
@lru_cache(maxsize=128)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

import time
inicio = time.perf_counter()
print(fib(50))   # 12586269025
print(f"Com cache: {time.perf_counter() - inicio:.6f}s")
print(fib.cache_info())

# PARTIAL: especializando funcoes
def formatar(valor, prefixo="", sufixo="", casas=2):
    return f"{prefixo}{valor:.{casas}f}{sufixo}"

em_reais    = partial(formatar, prefixo="R$ ", sufixo=" BRL")
porcentagem = partial(formatar, sufixo="%", casas=1)
inteiro     = partial(formatar, casas=0)

print(em_reais(1234.567))     # R$ 1234.57 BRL
print(porcentagem(0.856))     # 0.9%
print(inteiro(42.9))          # 43

# REDUCE: operacoes de acumulacao
from operator import mul

# Fatorial usando reduce
fatorial = lambda n: reduce(mul, range(1, n+1), 1)
print(fatorial(5))   # 120
print(fatorial(0))   # 1 (valor inicial)

# Maximo sem max()
numeros = [3, 1, 4, 1, 5, 9, 2, 6]
maximo = reduce(lambda a, b: a if a > b else b, numeros)
print("Maximo:", maximo)   # 9
''',
            explicacao="lru_cache memoriza os resultados: fib(50) calcula fib(49)+fib(48), "
                       "mas todas as chamadas intermediárias são lidas do cache. "
                       "cache_info() mostra hits (lidas do cache) e misses (calculadas de fato). "
                       "partial cria funções especializadas sem redefinir. "
                       "reduce com valor inicial (1) garante que listas vazias funcionem.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d21e1",
            enunciado=(
                "O import functools ja esta na assinatura.\n"
                "Escreva o decorador contar_chamadas(func) que adiciona\n"
                "um atributo '.chamadas' a funcao decorada, iniciando em 0\n"
                "e incrementando a cada chamada.\n\n"
                "Exemplos:\n"
                "   f = contar_chamadas(lambda x: x)\n"
                "   f.chamadas         -> 0  (antes de qualquer chamada)\n"
                "   f(1); f(2)\n"
                "   f.chamadas         -> 2  (chamada duas vezes)\n"
                "   contar_chamadas(lambda x: x*2)(5) -> 10  (funciona normal)\n\n"
                "Estrategia:\n"
                "   1. def envelope(*args, **kwargs):\n"
                "          envelope.chamadas += 1     <- incrementa o contador\n"
                "          return func(*args, **kwargs)\n"
                "   2. envelope.chamadas = 0          <- inicializa ANTES do return\n"
                "   3. return envelope\n\n"
                "O contador fica como ATRIBUTO do envelope:\n"
                "   envelope.chamadas = 0  define o atributo na funcao envelope.\n"
                "   Dentro do envelope, envelope.chamadas += 1 o incrementa.\n"
                "Use @functools.wraps(func) para preservar a identidade."
            ),
            funcao="contar_chamadas",
            assinatura="import functools\n\n\ndef contar_chamadas(func):",
            testes=[
                ("(lambda f: (f(1), f(2), f.chamadas)[2])(contar_chamadas(lambda x: x))", "2"),
                ("contar_chamadas(lambda: 1).chamadas", "0"),
                ("contar_chamadas(lambda x: x * 2)(5)", "10"),
            ],
            nivel="medio",
            dica="@functools.wraps(func); def envelope(*args, **kwargs): envelope.chamadas += 1; return func(*args, **kwargs); envelope.chamadas = 0; return envelope",
        ),
        Exercicio(
            id="d21e2",
            enunciado=(
                "O import functools ja esta na assinatura.\n"
                "Escreva o decorador maiusculas(func) que aplica .upper()\n"
                "no resultado de qualquer funcao que retorna string.\n\n"
                "Exemplos:\n"
                "   maiusculas(lambda: 'oi')()          -> 'OI'\n"
                "   maiusculas(lambda n: f'ola {n}')('ana') -> 'OLA ANA'\n\n"
                "Estrategia:\n"
                "   @functools.wraps(func)\n"
                "   def envelope(*args, **kwargs):\n"
                "       resultado = func(*args, **kwargs)  <- chama a original\n"
                "       return resultado.upper()           <- converte o retorno\n"
                "   return envelope\n\n"
                "Por que *args e **kwargs no envelope?\n"
                "   O decorador nao sabe a assinatura da funcao que vai receber.\n"
                "   *args captura argumentos posicionais (ex: 'ana').\n"
                "   **kwargs captura argumentos nomeados (ex: nome='ana').\n"
                "   Assim o envelope funciona com qualquer funcao."
            ),
            funcao="maiusculas",
            assinatura="import functools\n\n\ndef maiusculas(func):",
            testes=[
                ("maiusculas(lambda: 'oi')()", "'OI'"),
                ("maiusculas(lambda n: f'ola {n}')('ana')", "'OLA ANA'"),
            ],
            dica="@functools.wraps(func); def envelope(*args, **kwargs): return func(*args, **kwargs).upper(); return envelope",
        ),
        Exercicio(
            id="d21e3",
            enunciado=(
                "O import functools ja esta na assinatura.\n"
                "Escreva a FABRICA DE DECORADOR repetir(vezes) que retorna\n"
                "um decorador que chama a funcao 'vezes' vezes e devolve\n"
                "uma LISTA com todos os resultados.\n\n"
                "Exemplos:\n"
                "   repetir(3)(lambda: 'x')()      -> ['x', 'x', 'x']\n"
                "   repetir(2)(lambda a, b: a+b)(1, 2) -> [3, 3]\n"
                "   repetir(0)(lambda: 1)()         -> []  (zero vezes: lista vazia)\n\n"
                "Ha TRES niveis de aninhamento:\n"
                "   def repetir(vezes):            <- nivel 1: fabrica\n"
                "       def decorador(func):        <- nivel 2: decorador\n"
                "           @functools.wraps(func)\n"
                "           def envelope(*args, **kwargs): <- nivel 3: envelope\n"
                "               return [func(*args, **kwargs)\n"
                "                       for _ in range(vezes)]\n"
                "           return envelope         <- retorna envelope\n"
                "       return decorador            <- retorna decorador\n\n"
                "Uso: repetir(3) -> decorador -> repetir(3)(func) -> envelope\n"
                "     envelope() -> chama func 3 vezes -> ['x','x','x']"
            ),
            funcao="repetir",
            assinatura="import functools\n\n\ndef repetir(vezes):",
            testes=[
                ("repetir(3)(lambda: 'x')()", "['x', 'x', 'x']"),
                ("repetir(2)(lambda a, b: a + b)(1, 2)", "[3, 3]"),
                ("repetir(0)(lambda: 1)()", "[]"),
            ],
            nivel="dificil",
            dica="Três níveis: def repetir(vezes): def decorador(func): @wraps; def envelope(*a,**k): return [func(*a,**k) for _ in range(vezes)]; return envelope; return decorador; return decorador",
        ),
    ],
    quiz=[
        Quiz(
            "O que '@decorador' acima de uma funcao faz mecanicamente?",
            ["Cria uma subclasse da funcao com comportamento extra",
             "Equivale a 'funcao = decorador(funcao)' — passa a funcao para o decorador e substitui o nome pelo resultado",
             "Adiciona metadados a funcao sem alterar seu comportamento",
             "Torna a funcao privada, acessivel apenas dentro do modulo"],
            1,
            "@decorador def f(): ... e exatamente f = decorador(f). "
            "O decorador recebe f, pode criar um envelope que chama f, "
            "e retorna o envelope. O nome f passa a apontar para o envelope. "
            "E puro acucar sintatico sobre a tecnica de funcoes de alta ordem do Dia 12.",
        ),
        Quiz(
            "Por que @functools.wraps(func) e importante em todo decorador?",
            ["Sem ele, o decorador nao funciona",
             "Sem ele, o envelope substitui __name__, __doc__ e outros metadados da funcao original, quebrando help(), depuradores e ferramentas de documentacao",
             "Ele adiciona verificacao de tipos automatica",
             "Ele e opcional e raramente faz diferenca pratica"],
            1,
            "Sem @wraps, saudar.__name__ seria 'envelope', nao 'saudar'. "
            "help(saudar) mostraria a docstring do envelope (nenhuma). "
            "Ferramentas de profiling, logging e documentacao ficam confusas. "
            "@wraps copia __name__, __doc__, __module__, __qualname__ e __annotations__ "
            "do func para o envelope, preservando a identidade logica da funcao.",
        ),
        Quiz(
            "Dada a pilha '@a @b @c def f(): ...', em que ordem os decoradores sao aplicados?",
            ["a primeiro, depois b, depois c",
             "c primeiro, depois b, depois a",
             "Todos ao mesmo tempo",
             "A ordem e indefinida e pode variar"],
            1,
            "A pilha e lida de baixo para cima na aplicacao: c(f) primeiro, "
            "depois b(c(f)), depois a(b(c(f))). "
            "Na EXECUCAO, a ordem e de fora para dentro: a chama b que chama c que chama f. "
            "Por isso @negrito @italico produz <b><i>texto</i></b>: "
            "italico e aplicado primeiro, negrito depois.",
        ),
        Quiz(
            "Quando @functools.lru_cache NAO deve ser usado?",
            ["Nunca — lru_cache e sempre benefico",
             "Em funcoes com efeitos colaterais (que imprimem, escrevem arquivos, fazem requests) ou cujos argumentos sao mutaveis (listas, dicts)",
             "Em funcoes recursivas — causa recursao infinita",
             "Em funcoes com mais de 3 parametros"],
            1,
            "lru_cache memoriza: se os argumentos sao iguais, retorna o resultado cacheado "
            "SEM chamar a funcao novamente. "
            "Para funcoes puras (sem efeitos colaterais), isso e seguro. "
            "Para funcoes que imprimem (o print nao acontece no cache hit), "
            "fazem requests (a API nao e consultada) ou escrevem arquivos, "
            "o comportamento e surpreendente e geralmente errado. "
            "Argumentos mutaveis (list, dict) nao sao hasheaveis — causam TypeError.",
        ),
    ],
    projeto=(
        "Crie biblioteca_decoradores.py com uma colecao de decoradores uteis:\n\n"
        "   1. @cronometrar\n"
        "      Mede e armazena o tempo de cada chamada em func.tempos (lista).\n"
        "      func.tempo_medio() devolve a media dos tempos.\n\n"
        "   2. @cache_simples\n"
        "      Implementa memoizacao manual sem lru_cache:\n"
        "      guarda resultados em um dict {args: resultado}.\n"
        "      Adiciona func.cache (o dict) e func.limpar_cache().\n\n"
        "   3. @validar(**tipos)\n"
        "      Fabrica de decorador: valida tipos dos argumentos.\n"
        "      @validar(x=int, y=float) garante que x e int e y e float.\n"
        "      Levanta TypeError com mensagem clara se o tipo estiver errado.\n\n"
        "   4. @singleton\n"
        "      Garante que a classe decorada seja instanciada apenas uma vez.\n"
        "      Chamadas subsequentes retornam a mesma instancia.\n\n"
        "   5. @deprecated(mensagem)\n"
        "      Emite um warnings.warn ao chamar a funcao decorada.\n\n"
        "DEMONSTRACAO:\n"
        "   - Aplique @cronometrar + @cache_simples a uma funcao pesada\n"
        "   - Compare o tempo da primeira chamada com as subsequentes\n"
        "   - Mostre que @singleton retorna o mesmo objeto\n"
        "   - Combine @deprecated com @cronometrar e observe a ordem\n\n"
        "BONUS: implemente @retry(vezes, excecoes) que tenta novamente\n"
        "apenas para os tipos de excecao especificados."
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/functools.html — functools completo",
        "PEP 318 — Decorators for Functions and Methods",
        "docs.python.org/pt-br/3/glossary.html#term-decorator",
    ],
))

# ---------------------------------------------------------------- DIA 22
DIAS.append(Dia(
    numero=22,
    titulo="Context managers e gerenciamento de recursos",
    nivel="Avançado",
    duracao="100 min",
    objetivos=[
        "Entender o protocolo de contexto: __enter__ e __exit__ e o que acontece em cada um",
        "Criar context managers com classes implementando __enter__ e __exit__",
        "Criar context managers com @contextmanager de forma mais simples",
        "Usar contextlib para situações comuns: suppress, redirect_stdout, nullcontext",
        "Compor múltiplos context managers com 'with a, b, c'",
        "Reconhecer quando um context manager resolve um problema melhor que try/finally",
    ],
    teoria="""
No Dia 14 você usou 'with open(...)' para garantir que arquivos fossem
fechados automaticamente. Hoje vamos entender o mecanismo por trás do
'with' — o PROTOCOLO DE CONTEXTO — e aprender a criar nossos próprios
context managers para qualquer situação que precise de "abre e fecha".

---------------------------------------------------------------------------
1. O problema que context managers resolvem
---------------------------------------------------------------------------
Recursos como arquivos, conexões de banco, locks de thread e conexões de
rede precisam ser liberados após o uso, mesmo que ocorra um erro no meio.
Sem context managers, você usaria try/finally:

    # Sem context manager: verboso e perigoso
    arquivo = open("dados.txt")
    try:
        dados = arquivo.read()
        processar(dados)
    finally:
        arquivo.close()    # executa SEMPRE, mesmo se processar() falhar

    # Com context manager: conciso e seguro
    with open("dados.txt") as arquivo:
        dados = arquivo.read()
        processar(dados)
    # arquivo.close() é chamado automaticamente aqui

A vantagem não é só menos código — é a garantia SEMÂNTICA: o bloco
'with' comunica claramente "este recurso está reservado aqui dentro".

---------------------------------------------------------------------------
2. O protocolo de contexto: __enter__ e __exit__
---------------------------------------------------------------------------
Qualquer objeto que implemente __enter__ e __exit__ pode ser usado com
'with'. O que acontece por baixo dos panos:

    with expressao as variavel:
        corpo

    # Equivale a:
    gerenciador = expressao
    variavel = gerenciador.__enter__()   # "abrir": configura o recurso
    try:
        corpo
    except Exception as e:
        if not gerenciador.__exit__(type(e), e, e.__traceback__):
            raise    # re-levanta se __exit__ retornar False/None
    else:
        gerenciador.__exit__(None, None, None)   # sem exceção

__enter__(self):
    - Executado ao entrar no bloco with
    - O valor que RETORNA é o que vai para a variável após 'as'
    - Pode retornar self, outro objeto, ou None

__exit__(self, exc_type, exc_val, exc_tb):
    - Executado ao sair do bloco with (com ou sem exceção)
    - exc_type, exc_val, exc_tb: informações sobre a exceção (None se não houve)
    - Se retornar True (ou valor truthy): SUPRIME a exceção
    - Se retornar False/None: a exceção é re-levantada normalmente

CRIANDO UM CONTEXT MANAGER COM CLASSE:

    class Temporizador:
        def __enter__(self):
            import time
            self._inicio = time.perf_counter()
            return self    # retorna self para usar como 'as temporizador'

        def __exit__(self, exc_type, exc_val, exc_tb):
            import time
            self.duracao = time.perf_counter() - self._inicio
            print(f"Tempo: {self.duracao:.4f}s")
            return False   # não suprime exceções

    with Temporizador() as t:
        total = sum(range(1_000_000))
    print(f"Duração: {t.duracao:.4f}s")

---------------------------------------------------------------------------
3. Suprimindo exceções com __exit__
---------------------------------------------------------------------------
__exit__ pode decidir SUPRIMIR uma exceção retornando True:

    class SilenciarErro:
        def __init__(self, *tipos_de_erro):
            self.tipos = tipos_de_erro

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            # True suprime a exceção; False/None a re-levanta
            if exc_type is not None:
                return issubclass(exc_type, self.tipos)
            return False

    with SilenciarErro(ValueError, ZeroDivisionError):
        resultado = 1 / 0    # ZeroDivisionError é suprimida!
    print("Código continua normalmente")

    with SilenciarErro(ValueError):
        resultado = 1 / 0    # ZeroDivisionError NÃO é suprimida (TypeError?)
                              # Pois ZeroDivisionError não é ValueError

Suprimir exceções é poderoso mas perigoso — use com cuidado e apenas
quando você TEM CERTEZA de que a exceção é esperada e inofensiva.

---------------------------------------------------------------------------
4. @contextmanager: context managers sem classe
---------------------------------------------------------------------------
O decorator @contextmanager de contextlib transforma uma função
geradora em um context manager. É mais conciso do que escrever uma classe:

    from contextlib import contextmanager

    @contextmanager
    def temporizador():
        import time
        inicio = time.perf_counter()
        try:
            yield    # pausa aqui — o corpo do 'with' executa
        finally:
            duracao = time.perf_counter() - inicio
            print(f"Tempo: {duracao:.4f}s")

    with temporizador():
        total = sum(range(1_000_000))

A ESTRUTURA É SEMPRE A MESMA:

    @contextmanager
    def meu_gerenciador(argumentos):
        # CONFIGURAÇÃO (equivale ao __enter__)
        recurso = abrir_recurso(argumentos)
        try:
            yield recurso    # 'recurso' vai para 'as x' no with
        except TipoDeErro:
            tratar_erro()    # opcional: tratar exceções específicas
            raise            # re-levanta depois de tratar
        finally:
            fechar_recurso(recurso)    # equivale ao __exit__

REGRAS DO @contextmanager:
    - O gerador deve ter EXATAMENTE um yield
    - O que você coloca no yield vai para a variável 'as'
    - Código antes do yield = __enter__
    - Código depois do yield (no finally) = __exit__
    - Exceções do corpo do with chegam no ponto do yield

---------------------------------------------------------------------------
5. contextlib: ferramentas prontas
---------------------------------------------------------------------------
O módulo contextlib oferece context managers prontos para situações comuns:

SUPPRESS: silencia exceções específicas

    from contextlib import suppress

    with suppress(FileNotFoundError):
        os.remove("arquivo_que_pode_nao_existir.txt")
    # Se o arquivo não existe, a exceção é ignorada silenciosamente

    # Equivale a:
    try:
        os.remove("arquivo_que_pode_nao_existir.txt")
    except FileNotFoundError:
        pass

REDIRECT_STDOUT / REDIRECT_STDERR: redireciona saída

    import io
    from contextlib import redirect_stdout

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print("esta saída vai para o buffer, não para a tela")
    texto = buffer.getvalue()    # captura o que foi impresso

NULLCONTEXT: context manager que não faz nada (útil em condicionais)

    from contextlib import nullcontext

    # Sem nullcontext: código condicional complicado
    if deve_cronometrar:
        ctx = Temporizador()
    else:
        ctx = nullcontext()    # não faz nada, mas é um gerenciador válido

    with ctx:
        executar_tarefa()

CLOSING: garante que .close() seja chamado

    from contextlib import closing
    from urllib.request import urlopen

    with closing(urlopen("http://exemplo.com")) as resposta:
        dados = resposta.read()
    # resposta.close() é chamado automaticamente

EXITSTACK: pilha dinâmica de context managers

    from contextlib import ExitStack

    arquivos = ["a.txt", "b.txt", "c.txt"]
    with ExitStack() as pilha:
        handlers = [pilha.enter_context(open(f, "w")) for f in arquivos]
        for h in handlers:
            h.write("olá\n")
    # todos os arquivos são fechados ao sair

ExitStack é útil quando você não sabe quantos recursos precisará
gerenciar até o momento de execução.

---------------------------------------------------------------------------
6. Compondo múltiplos context managers
---------------------------------------------------------------------------
Python permite usar múltiplos context managers no mesmo with:

    # Forma antiga (ainda funciona)
    with open("entrada.txt") as f_in:
        with open("saida.txt", "w") as f_out:
            f_out.write(f_in.read())

    # Forma moderna (preferida): uma única linha
    with open("entrada.txt") as f_in, open("saida.txt", "w") as f_out:
        f_out.write(f_in.read())

    # Com parênteses (Python 3.10+, para linhas longas)
    with (
        open("entrada.txt") as f_in,
        open("saida.txt", "w") as f_out,
        Temporizador() as t,
    ):
        f_out.write(f_in.read())

A ordem de entrada é da esquerda para a direita.
A ordem de saída (__exit__) é da direita para a esquerda.

---------------------------------------------------------------------------
7. Quando usar context manager vs try/finally
---------------------------------------------------------------------------
Use context manager quando:
    - O padrão "abrir/usar/fechar" é claro e reutilizável
    - O mesmo padrão aparece em vários lugares do código
    - Você quer comunicar a intenção claramente (semântica)

Use try/finally quando:
    - É um caso específico e não reutilizável
    - Você precisa de lógica complexa na limpeza
    - O código de limpeza depende de resultados intermediários

EXEMPLOS DE USO REAL:
    with open(...):              abertura de arquivos
    with conexao.cursor():       transações de banco de dados
    with lock:                   locks de threading
    with patch(...):             mocking em testes (unittest.mock)
    with transaction.atomic():   transações do Django
    with tempfile.TemporaryDirectory(): diretórios temporários
""",
    exemplos=[
        Exemplo(
            titulo="Context manager com classe: banco de dados simulado",
            codigo='''class TransacaoBD:
    """Simula uma transacao de banco de dados."""

    def __init__(self, nome="db"):
        self.nome = nome
        self.operacoes = []
        self.confirmada = False

    def __enter__(self):
        print(f"[{self.nome}] Transacao iniciada")
        return self    # retorna self para poder usar como 'as t'

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # Sem excecao: confirma a transacao
            self.confirmada = True
            print(f"[{self.nome}] Commit: {len(self.operacoes)} operacoes")
        else:
            # Com excecao: cancela tudo
            self.operacoes.clear()
            print(f"[{self.nome}] Rollback por: {exc_type.__name__}: {exc_val}")
        return False    # nao suprime a excecao

    def executar(self, sql):
        self.operacoes.append(sql)
        print(f"[{self.nome}] SQL: {sql}")

# Caso feliz: commit automatico
with TransacaoBD("principal") as t:
    t.executar("INSERT INTO usuarios VALUES (1, 'Ana')")
    t.executar("UPDATE saldos SET valor = 100 WHERE id = 1")
print(f"Confirmada: {t.confirmada}")

print()

# Caso com erro: rollback automatico
try:
    with TransacaoBD("pagamento") as t2:
        t2.executar("UPDATE saldos SET valor = -50 WHERE id = 1")
        raise ValueError("saldo negativo nao permitido")
        t2.executar("INSERT INTO historico VALUES (...)")  # nunca executa
except ValueError:
    print(f"Transacao confirmada: {t2.confirmada}")
    print(f"Operacoes restantes: {t2.operacoes}")
''',
            explicacao="__enter__ inicia a transação e retorna self. "
                       "__exit__ recebe informações sobre a exceção: "
                       "exc_type é None se não houve erro, ou o tipo da exceção. "
                       "Retornar False re-levanta a exceção — o chamador ainda precisa tratá-la. "
                       "Este padrão de commit/rollback é exatamente o que "
                       "frameworks de banco de dados implementam.",
        ),
        Exemplo(
            titulo="@contextmanager: gerenciadores elegantes sem classe",
            codigo='''import time
import io
from contextlib import contextmanager, redirect_stdout

@contextmanager
def cronometrar(nome="operacao"):
    """Mede o tempo de execucao de um bloco."""
    inicio = time.perf_counter()
    try:
        yield    # corpo do with executa aqui
    finally:
        duracao = time.perf_counter() - inicio
        print(f"[{nome}] {duracao:.4f}s")

@contextmanager
def capturar_saida():
    """Captura tudo que seria impresso para a tela."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        yield buffer    # 'buffer' vai para a variavel 'as'
    # nao ha finally necessario: redirect_stdout ja gerencia o restore

@contextmanager
def ambiente_temporario(**variaveis):
    """Define variaveis de ambiente temporariamente."""
    import os
    originais = {k: os.environ.get(k) for k in variaveis}
    os.environ.update({k: v for k, v in variaveis.items()})
    try:
        yield
    finally:
        # Restaura os valores originais
        for k, original in originais.items():
            if original is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = original

# Usando os tres juntos
with cronometrar("fibonacci"):
    resultado = sum(range(1_000_000))

with capturar_saida() as saida:
    print("Linha 1")
    print("Linha 2")
texto_capturado = saida.getvalue()
print(f"Capturado: {repr(texto_capturado)}")

with ambiente_temporario(DEBUG="1", APP_ENV="test"):
    import os
    print(f"No bloco: DEBUG={os.environ.get('DEBUG')}")
print(f"Apos bloco: DEBUG={os.environ.get('DEBUG')}")
''',
            explicacao="@contextmanager transforma um gerador com exatamente "
                       "um yield em um context manager completo. "
                       "Código antes do yield = __enter__. "
                       "try/finally ao redor do yield = __exit__ com garantia de limpeza. "
                       "yield buffer passa o buffer para 'as b' — o que você coloca "
                       "no yield vai para a variável do 'as'.",
        ),
        Exemplo(
            titulo="contextlib: ferramentas prontas na prática",
            codigo='''import os
import io
from contextlib import suppress, ExitStack, nullcontext

# SUPPRESS: ignora erros especificos elegantemente
arquivos_para_limpar = ["temp1.txt", "temp2.txt", "nao_existe.txt"]
for nome in arquivos_para_limpar:
    with suppress(FileNotFoundError):
        os.remove(nome)
        print(f"Removido: {nome}")
print("Limpeza concluida (sem erros fatais)")

# EXITSTACK: numero dinamico de context managers
def processar_arquivos(nomes, modo="r"):
    """Abre e processa N arquivos, todos fechados ao terminar."""
    conteudos = []
    # Simula arquivos em memoria para o exemplo
    arquivos_virtuais = [io.StringIO(f"conteudo de {n}") for n in nomes]
    with ExitStack() as pilha:
        handles = [pilha.enter_context(f) for f in arquivos_virtuais]
        for h in handles:
            conteudos.append(h.read())
    # Todos os arquivos virtuais sao fechados aqui
    return conteudos

resultado = processar_arquivos(["a.txt", "b.txt", "c.txt"])
print("Conteudos:", resultado)

# NULLCONTEXT: context manager condicional
def executar(tarefa, medir_tempo=False):
    ctx = (
        __import__("contextlib").contextmanager(
            lambda: ((__import__("time").perf_counter(),),
                     (None for _ in range(1)))
        )()
        if medir_tempo else nullcontext()
    )
    # Versao mais limpa:
    import time
    from contextlib import contextmanager

    @contextmanager
    def timer():
        t = time.perf_counter()
        yield
        print(f"Tempo: {time.perf_counter()-t:.4f}s")

    with (timer() if medir_tempo else nullcontext()):
        return tarefa()

resultado = executar(lambda: sum(range(100_000)), medir_tempo=True)
print("Resultado:", resultado)
''',
            explicacao="suppress é equivalente a try/except: pass, mas mais legível "
                       "e comunica intenção. Use quando a exceção é esperada e inofensiva. "
                       "ExitStack resolve o problema de 'quantos arquivos abrir' "
                       "não ser conhecido em tempo de código. "
                       "nullcontext evita a necessidade de if/else ao redor do with.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d22e1",
            enunciado=(
                "A assinatura ja tem os metodos __enter__ e __exit__ da\n"
                "classe Coletor e a funcao somar_com. Complete-os.\n\n"
                "Coletor e um context manager que:\n"
                "   __enter__: inicializa self.valores = [] e devolve self\n"
                "   __exit__: calcula self.total = sum(self.valores)\n\n"
                "A funcao somar_com(valores) usa Coletor assim:\n"
                "   with Coletor() as c:\n"
                "       for v in valores:\n"
                "           c.valores.append(v)\n"
                "   return c.total   <- disponivel APOS o with\n\n"
                "Exemplos:\n"
                "   somar_com([1, 2, 3]) -> 6\n"
                "   somar_com([])        -> 0\n"
                "   somar_com([10])      -> 10\n\n"
                "__exit__ recebe (self, exc_type, exc_val, exc_tb).\n"
                "Use *exc para capturar os tres como tupla:\n"
                "   def __exit__(self, *exc):\n"
                "       self.total = sum(self.valores)\n"
                "       return False   <- nao suprime excecoes\n\n"
                "c.total so existe APOS o bloco with terminar,\n"
                "pois __exit__ e chamado ao sair do bloco."
            ),
            funcao="Coletor",
            assinatura="class Coletor:\n    def __enter__(self):\n        ...\n\n    def __exit__(self, *exc):\n        ...\n\n\ndef somar_com(valores):",
            testes=[
                ("somar_com([1, 2, 3])", "6"),
                ("somar_com([])", "0"),
                ("somar_com([10])", "10"),
            ],
            nivel="medio",
            dica="__enter__: self.valores = []; return self. __exit__: self.total = sum(self.valores); return False. somar_com: with Coletor() as c: [c.valores.append(v) for v em valores]; return c.total",
        ),
        Exercicio(
            id="d22e2",
            enunciado=(
                "Os imports io, contextmanager e redirect_stdout\n"
                "ja estao na assinatura.\n\n"
                "Complete o context manager 'silenciar' (com @contextmanager)\n"
                "que redireciona stdout para um buffer e faz yield do buffer.\n\n"
                "Complete 'capturar(texto)' que:\n"
                "   1. Usa 'with silenciar() as buf:'\n"
                "   2. Dentro do with: print(texto)\n"
                "   3. Retorna buf.getvalue()\n\n"
                "Exemplos:\n"
                "   capturar('oi') -> 'oi\\n'   (print adiciona newline)\n"
                "   capturar('')   -> '\\n'    (print de string vazia)\n\n"
                "Estrutura de silenciar:\n"
                "   @contextmanager\n"
                "   def silenciar():\n"
                "       buf = io.StringIO()\n"
                "       with redirect_stdout(buf):\n"
                "           yield buf   <- buf vai para 'as' do with externo\n\n"
                "Por que yield DENTRO do with redirect_stdout?\n"
                "O redirect_stdout precisa estar ATIVO durante o corpo do\n"
                "with externo. Fazer yield dentro garante que o redirecionamento\n"
                "permanece enquanto o codigo do usuario executa."
            ),
            funcao="silenciar",
            assinatura="import io\nfrom contextlib import contextmanager, redirect_stdout\n\n\n@contextmanager\ndef silenciar():\n    ...\n\n\ndef capturar(texto):",
            testes=[
                ("capturar('oi')", "'oi\\n'"),
                ("capturar('')", "'\\n'"),
            ],
            nivel="dificil",
            dica="silenciar: buf = io.StringIO(); with redirect_stdout(buf): yield buf. capturar: with silenciar() as buf: print(texto); return buf.getvalue()",
        ),
        Exercicio(
            id="d22e3",
            enunciado=(
                "O import 'suppress' de contextlib ja esta na assinatura.\n\n"
                "Escreva ignorar_erro(func) que:\n"
                "   1. Chama func() usando 'with suppress(Exception)'\n"
                "   2. Retorna o resultado se func() funcionar\n"
                "   3. Retorna None se func() levantar qualquer excecao\n\n"
                "Exemplos:\n"
                "   ignorar_erro(lambda: 10 / 2) -> 5.0   (sem erro)\n"
                "   ignorar_erro(lambda: 1 / 0)  -> None  (ZeroDivisionError suprimida)\n\n"
                "Estrategia:\n"
                "   resultado = None   <- valor padrao se der erro\n"
                "   with suppress(Exception):\n"
                "       resultado = func()  <- se der erro, suppress ignora\n"
                "                           <- resultado permanece None\n"
                "   return resultado\n\n"
                "Por que inicializar resultado = None ANTES do with?\n"
                "Se func() levantar excecao, a linha 'resultado = func()'\n"
                "nao completa — resultado nunca e atribuido dentro do with.\n"
                "Mas como suppress silencia a excecao, o codigo continua.\n"
                "Sem a inicializacao, 'return resultado' causaria NameError."
            ),
            funcao="ignorar_erro",
            assinatura="from contextlib import suppress\n\n\ndef ignorar_erro(func):",
            testes=[
                ("ignorar_erro(lambda: 10 / 2)", "5.0"),
                ("ignorar_erro(lambda: 1 / 0)", "None"),
            ],
            dica="resultado = None; with suppress(Exception): resultado = func(); return resultado",
        ),
    ],
    quiz=[
        Quiz(
            "O que __exit__ deve retornar para SUPRIMIR uma excecao que ocorreu no bloco with?",
            ["None (o padrao)",
             "False",
             "Um valor truthy como True",
             "A propria excecao"],
            2,
            "Se __exit__ retorna True (ou qualquer valor truthy), Python suprime a excecao "
            "e o codigo apos o with continua normalmente. "
            "Se retorna False ou None, a excecao e re-levantada. "
            "contextlib.suppress usa exatamente esse mecanismo: seu __exit__ "
            "retorna True quando a excecao e do tipo a ser suprimido.",
        ),
        Quiz(
            "Em '@contextmanager', onde deve estar o yield em relacao ao codigo de limpeza?",
            ["O yield deve ser a ultima linha da funcao",
             "O yield deve estar dentro de um bloco try, com o codigo de limpeza no finally",
             "Pode estar em qualquer lugar — a ordem nao importa",
             "Deve haver dois yields: um para __enter__ e um para __exit__"],
            1,
            "A estrutura correta e: codigo de configuracao; try: yield recurso; finally: codigo de limpeza. "
            "O finally garante que a limpeza ocorra mesmo se o corpo do with levantar uma excecao. "
            "Sem try/finally, uma excecao no corpo impediria a limpeza de executar. "
            "A funcao deve ter EXATAMENTE um yield.",
        ),
        Quiz(
            "Qual a principal vantagem de 'with suppress(FileNotFoundError)' sobre try/except?",
            ["suppress e mais rapido que try/except",
             "Comunica a intencao de forma mais clara e concisa: este erro e esperado e pode ser ignorado com seguranca",
             "suppress captura mais tipos de excecao que try/except",
             "Nao ha vantagem — sao identicos em todos os aspectos"],
            1,
            "suppress e semanticamente mais rico: ao ler 'with suppress(FileNotFoundError)', "
            "o leitor entende imediatamente que 'o arquivo pode nao existir e isso e ok'. "
            "try/except: pass e mais verboso e nao comunica a intencao com a mesma clareza. "
            "suppress tambem e mais seguro que except: pass (que capturaria qualquer Exception).",
        ),
        Quiz(
            "O que ExitStack resolve que 'with a, b, c' nao resolve?",
            ["ExitStack e mais rapido que multiplos with",
             "ExitStack permite abrir um numero DINAMICO de context managers, nao conhecido em tempo de codigo",
             "ExitStack suporta context managers assincronos",
             "Nao ha diferenca — ExitStack e apenas uma alternativa sintatica"],
            1,
            "'with a, b, c' requer que voce saiba em tempo de codigo quantos gerenciadores usar. "
            "Se voce tem uma lista de N arquivos para abrir (N desconhecido ate o runtime), "
            "nao pode usar 'with f1, f2, ...' pois N e variavel. "
            "ExitStack resolve: for f in arquivos: pilha.enter_context(open(f)). "
            "Todos sao fechados quando o with do ExitStack termina.",
        ),
    ],
    projeto=(
        "Crie gerenciador_recursos.py com context managers uteis:\n\n"
        "   1. @contextmanager\n"
        "      def diretorio_temporario():\n"
        "      Cria um diretorio temporario, faz yield do Path,\n"
        "      e apaga o diretorio (com tudo dentro) ao sair.\n"
        "      Use tempfile.mkdtemp() e shutil.rmtree().\n\n"
        "   2. class MedirMemoria:\n"
        "      Mede o uso de memoria antes e depois do bloco.\n"
        "      Use tracemalloc.start(), snapshot = tracemalloc.take_snapshot()\n"
        "      Atributos: self.antes, self.depois, self.diferenca\n\n"
        "   3. @contextmanager\n"
        "      def transacao(lista_operacoes):\n"
        "      Acumula operacoes numa lista durante o bloco.\n"
        "      Se nao houver excecao: confirma (imprime 'Commit').\n"
        "      Se houver excecao: limpa a lista (imprime 'Rollback').\n\n"
        "   4. class ConfiguracaoTemporaria:\n"
        "      Salva e restaura um dicionario de configuracao.\n"
        "      __enter__: faz backup da config atual\n"
        "      __exit__: restaura o backup (mesmo com excecao)\n\n"
        "DEMONSTRACAO:\n"
        "   with diretorio_temporario() as tmp:\n"
        "       (tmp / 'teste.txt').write_text('oi')\n"
        "       print(list(tmp.iterdir()))\n"
        "   # diretorio apagado aqui\n\n"
        "   with MedirMemoria() as mem:\n"
        "       grande = list(range(1_000_000))\n"
        "   print(f'Alocado: {mem.diferenca / 1024:.1f} KB')\n\n"
        "BONUS: combine todos em um pipeline:\n"
        "   with diretorio_temporario() as tmp, MedirMemoria() as mem:\n"
        "       processar_dados(tmp)"
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/contextlib.html — contextlib completo",
        "PEP 343 — The 'with' Statement",
        "docs.python.org/pt-br/3/reference/datamodel.html#context-managers",
    ],
))

# ---------------------------------------------------------------- DIA 23
DIAS.append(Dia(
    numero=23,
    titulo="Type hints e código auto-documentado",
    nivel="Avançado",
    duracao="100 min",
    objetivos=[
        "Entender o que são type hints e por que eles existem em uma linguagem dinamicamente tipada",
        "Anotar funções, variáveis e classes com os tipos corretos",
        "Usar os tipos genéricos de typing: Optional, Union, List, Dict, Tuple e os modernos",
        "Criar tipos personalizados com TypeVar, Protocol e TypedDict",
        "Usar ferramentas de verificação estática como mypy para encontrar bugs antes de rodar",
        "Escrever código auto-documentado combinando type hints com docstrings",
    ],
    teoria="""
Python é dinamicamente tipado: você não precisa declarar tipos e eles
podem mudar em tempo de execução. Mas isso torna difícil saber o que
uma função espera receber e o que ela retorna, especialmente em projetos
grandes. Type hints resolvem esse problema sem sacrificar a flexibilidade.

---------------------------------------------------------------------------
1. O que são type hints e por que usá-los
---------------------------------------------------------------------------
Type hints são ANOTAÇÕES que indicam os tipos esperados de variáveis,
parâmetros e retornos de função. O Python NÃO as verifica em tempo de
execução — elas servem para:

    - DOCUMENTAÇÃO: quem lê o código entende a intenção imediatamente
    - FERRAMENTAS: editores (VSCode, PyCharm) mostram autocompletar melhor
    - ANÁLISE ESTÁTICA: mypy encontra bugs de tipo antes de rodar o código
    - MANUTENÇÃO: erros ao refatorar são detectados mais cedo

A filosofia: type hints são OPCIONAIS. Você pode adicioná-los
gradualmente em um projeto existente, sem quebrar nada.

    # Sem type hints: o que é 'dados'? O que retorna?
    def processar(dados, modo):
        ...

    # Com type hints: autoexplicativo
    def processar(dados: list[str], modo: str) -> dict[str, int]:
        ...

---------------------------------------------------------------------------
2. Sintaxe básica de anotações
---------------------------------------------------------------------------
ANOTANDO FUNÇÕES:

    def somar(a: int, b: int) -> int:
        return a + b

    def saudar(nome: str, vezes: int = 1) -> None:
        for _ in range(vezes):
            print(f"Olá, {nome}!")

    # None como retorno: função não retorna valor útil
    # Sem '->': type checkers assumem que o retorno é desconhecido

ANOTANDO VARIÁVEIS:

    nome: str = "Ana"
    idade: int = 30
    preco: float = 29.90
    ativo: bool = True

    # Anotação sem atribuição (declara o tipo mas não cria a variável)
    resultado: int    # existe na tabela de tipos, mas não tem valor ainda

ACESSANDO ANOTAÇÕES EM TEMPO DE EXECUÇÃO:

    def calcular(x: float, y: float) -> float:
        return x + y

    calcular.__annotations__
    # {'x': <class 'float'>, 'y': <class 'float'>, 'return': <class 'float'>}

---------------------------------------------------------------------------
3. Tipos compostos: coleções e genéricos
---------------------------------------------------------------------------
Para tipos compostos, você anota o tipo do conteúdo também:

PYTHON 3.9+ (sintaxe moderna — preferida):

    lista_nomes: list[str]
    mapa_notas: dict[str, float]
    par: tuple[int, str]
    conjunto: set[int]

PYTHON 3.8 E ANTERIOR (importar de typing):

    from typing import List, Dict, Tuple, Set
    lista_nomes: List[str]
    mapa_notas: Dict[str, float]

Hoje (2024+), use sempre a sintaxe moderna com letras minúsculas.

TIPOS ESPECIAIS MAIS USADOS:

    from typing import Optional, Union, Any, Callable

    # Optional[X] = X | None (o valor pode ser X ou None)
    def buscar(id: int) -> Optional[str]:
        ...

    # Forma moderna (Python 3.10+)
    def buscar(id: int) -> str | None:
        ...

    # Union: pode ser um tipo OU outro
    def processar(valor: int | str) -> str:
        ...

    # Any: desativa a verificação de tipo (use com parcimônia)
    def aceitar_qualquer(x: Any) -> Any:
        ...

    # Callable: uma função
    from typing import Callable
    def aplicar(func: Callable[[int], str], valor: int) -> str:
        return func(valor)

TIPOS DE COLEÇÕES MAIS GENÉRICOS:

    from typing import Sequence, Iterable, Mapping

    # Sequence: qualquer coisa indexável (list, tuple, str)
    def primeiro(seq: Sequence[int]) -> int:
        return seq[0]

    # Iterable: qualquer coisa percorrível com for
    def somar(valores: Iterable[float]) -> float:
        return sum(valores)

    # Mapping: qualquer dict-like (dict, OrderedDict...)
    def chaves(m: Mapping[str, Any]) -> list[str]:
        return list(m.keys())

---------------------------------------------------------------------------
4. TypeVar: tipos genéricos
---------------------------------------------------------------------------
TypeVar cria uma VARIÁVEL DE TIPO — um placeholder que representa "algum
tipo T, o mesmo em toda a função":

    from typing import TypeVar, Sequence

    T = TypeVar("T")    # T pode ser qualquer tipo

    def primeiro(seq: Sequence[T]) -> T | None:
        return seq[0] if seq else None

    primeiro([1, 2, 3])       # retorna int (T = int)
    primeiro(["a", "b"])      # retorna str (T = str)
    primeiro([])              # retorna None

TypeVar garante que o tipo de entrada e saída sejam CONSISTENTES.
Sem TypeVar, você usaria Any, perdendo a informação de tipo.

TypeVar com restrições:

    from typing import TypeVar

    Numerico = TypeVar("Numerico", int, float)    # só int ou float

    def dobrar(x: Numerico) -> Numerico:
        return x * 2

    dobrar(5)      # int -> int
    dobrar(3.14)   # float -> float
    dobrar("oi")   # erro de tipo! str não é Numerico

---------------------------------------------------------------------------
5. TypedDict: dicionários com estrutura definida
---------------------------------------------------------------------------
TypedDict define a estrutura esperada de um dicionário — quais chaves
existem e quais tipos elas têm:

    from typing import TypedDict

    class Pessoa(TypedDict):
        nome: str
        idade: int
        email: str

    class PessoaOpcional(TypedDict, total=False):
        nome: str
        apelido: str          # campo opcional (total=False)

    def processar_pessoa(p: Pessoa) -> str:
        return f"{p['nome']}, {p['idade']} anos"

    # O type checker sabe que p['nome'] é str e p['cpf'] seria erro
    pessoa: Pessoa = {"nome": "Ana", "idade": 30, "email": "ana@ex.com"}
    processar_pessoa(pessoa)    # ok!

TypedDict é útil para validar estrutura de dicionários vindos de JSON,
APIs ou configurações, sem precisar criar uma classe completa.

---------------------------------------------------------------------------
6. Protocol: duck typing com verificação de tipo
---------------------------------------------------------------------------
Protocol define uma INTERFACE estrutural: qualquer classe que tenha os
métodos definidos satisfaz o protocolo, sem precisar herdar explicitamente:

    from typing import Protocol

    class TemArea(Protocol):
        def area(self) -> float:
            ...    # corpo vazio, só define a interface

    class Circulo:
        def area(self) -> float:
            return 3.14 * 5 ** 2

    class Quadrado:
        def area(self) -> float:
            return 4.0 ** 2

    def maior_area(formas: list[TemArea]) -> TemArea:
        return max(formas, key=lambda f: f.area())

    # Circulo e Quadrado satisfazem TemArea sem herdar dela!
    maior = maior_area([Circulo(), Quadrado()])

Protocol é a formalização do duck typing do Dia 18: em vez de "se tem
o método, funciona", você declara explicitamente quais métodos são
necessários — mantendo a flexibilidade sem sacrificar a documentação.

---------------------------------------------------------------------------
7. Anotações em classes
---------------------------------------------------------------------------

    from dataclasses import dataclass
    from typing import ClassVar

    class Produto:
        total_criados: ClassVar[int] = 0    # atributo de classe

        def __init__(self, nome: str, preco: float) -> None:
            self.nome: str = nome
            self.preco: float = preco
            Produto.total_criados += 1

        def aplicar_desconto(self, percentual: float) -> "Produto":
            # Aspas em 'Produto': forward reference (classe ainda sendo definida)
            novo = Produto(self.nome, self.preco * (1 - percentual / 100))
            return novo

    @dataclass
    class Ponto:
        x: float
        y: float
        label: str = ""    # com @dataclass, anotações definem os campos

---------------------------------------------------------------------------
8. mypy: verificação estática
---------------------------------------------------------------------------
mypy é o verificador de tipos mais usado para Python. Ele analisa seu
código sem executá-lo e encontra erros de tipo.

INSTALAÇÃO:

    pip install mypy

EXEMPLO DE USO:

    # arquivo: calculos.py
    def somar(a: int, b: int) -> int:
        return a + b

    resultado: str = somar(1, 2)    # bug: somar retorna int, não str!
    somar("um", "dois")             # bug: str, não int!

    # No terminal:
    # mypy calculos.py
    # calculos.py:4: error: Incompatible types in assignment
    # calculos.py:5: error: Argument 1 to "somar" has incompatible type "str"

NÍVEL DE RIGOR DO MYPY:

    mypy arquivo.py                  # verificação padrão
    mypy --strict arquivo.py         # verificação máxima
    mypy --ignore-missing-imports arquivo.py   # ignora libs sem stubs

CONFIGURAÇÃO (.mypy.ini ou pyproject.toml):

    [mypy]
    python_version = 3.12
    strict = true
    ignore_missing_imports = true

---------------------------------------------------------------------------
9. Boas práticas de type hints
---------------------------------------------------------------------------

    USE type hints quando:
    - Funções públicas de uma biblioteca
    - Código que será mantido por outros
    - Qualquer função que receba ou retorne tipos não óbvios

    EVITE type hints quando:
    - Scripts rápidos e descartáveis
    - Protótipos em desenvolvimento ativo
    - Código de testes simples

    REGRAS GERAIS:
    - Prefira tipos específicos a Any
    - Use Sequence em vez de list quando aceitar qualquer sequência
    - Use | None em vez de Optional (Python 3.10+)
    - Anote parâmetros e retornos de funções públicas sempre
    - ClassVar para atributos de classe
    - Não anote o self e o cls
""",
    exemplos=[
        Exemplo(
            titulo="Anotações completas em funções e classes",
            codigo='''from typing import Optional, Callable, TypeVar
from dataclasses import dataclass, field

T = TypeVar("T")

# Funcoes com anotacoes completas
def filtrar(
    items: list[T],
    predicado: Callable[[T], bool]
) -> list[T]:
    """Filtra items mantendo os que satisfazem o predicado."""
    return [x for x in items if predicado(x)]

def agrupar(
    items: list[T],
    chave: Callable[[T], str]
) -> dict[str, list[T]]:
    """Agrupa items pelo resultado de chave."""
    grupos: dict[str, list[T]] = {}
    for item in items:
        k = chave(item)
        grupos.setdefault(k, []).append(item)
    return grupos

# Usando as funcoes com type hints
numeros = [1, -2, 3, -4, 5]
positivos = filtrar(numeros, lambda x: x > 0)
print("Positivos:", positivos)

palavras = ["ana", "bia", "alice", "bruno", "carlos"]
por_inicial = agrupar(palavras, lambda p: p[0])
print("Por inicial:", por_inicial)

# Classe com anotacoes completas
@dataclass
class Pedido:
    cliente: str
    itens: list[str] = field(default_factory=list)
    desconto: float = 0.0
    ativo: bool = True

    def adicionar(self, item: str) -> "Pedido":
        self.itens.append(item)
        return self    # method chaining com tipo correto

    def total_itens(self) -> int:
        return len(self.itens)

p = Pedido("Ana")
p.adicionar("caneta").adicionar("caderno")
print(f"Pedido de {p.cliente}: {p.total_itens()} itens")
print(p.__annotations__)   # anotacoes do dataclass
''',
            explicacao="TypeVar T garante que filtrar retorna uma lista do "
                       "mesmo tipo que recebeu — se passar list[int], "
                       "o type checker sabe que o retorno é list[int]. "
                       "Callable[[T], bool] especifica uma função que recebe T e retorna bool. "
                       "'Pedido' entre aspas é uma forward reference — necessária "
                       "quando o tipo é a própria classe sendo definida.",
        ),
        Exemplo(
            titulo="Protocol e TypedDict na prática",
            codigo='''from typing import Protocol, TypedDict, runtime_checkable

# TypedDict: estrutura de dicionario com tipos
class ConfigBD(TypedDict):
    host: str
    porta: int
    banco: str
    usuario: str

class ConfigBDCompleta(ConfigBD, total=False):
    senha: str        # campo opcional
    timeout: float    # campo opcional

def conectar(config: ConfigBD) -> str:
    return f"Conectado a {config['host']}:{config['porta']}/{config['banco']}"

config: ConfigBD = {
    "host": "localhost",
    "porta": 5432,
    "banco": "producao",
    "usuario": "admin"
}
print(conectar(config))

# Protocol: interface estrutural (duck typing formal)
@runtime_checkable   # permite usar isinstance() com o Protocol
class Serializavel(Protocol):
    def para_dict(self) -> dict: ...
    def para_json(self) -> str: ...

class Usuario:
    def __init__(self, nome: str, email: str) -> None:
        self.nome = nome
        self.email = email

    def para_dict(self) -> dict:
        return {"nome": self.nome, "email": self.email}

    def para_json(self) -> str:
        import json
        return json.dumps(self.para_dict())

class Produto:
    def __init__(self, nome: str, preco: float) -> None:
        self.nome = nome
        self.preco = preco

    def para_dict(self) -> dict:
        return {"nome": self.nome, "preco": self.preco}

    def para_json(self) -> str:
        import json
        return json.dumps(self.para_dict())

def exportar(obj: Serializavel) -> str:
    return obj.para_json()

u = Usuario("Ana", "ana@email.com")
p = Produto("Caneta", 2.50)

print(exportar(u))
print(exportar(p))

# runtime_checkable permite isinstance
print(isinstance(u, Serializavel))   # True — tem os metodos!
''',
            explicacao="TypedDict com herança (ConfigBDCompleta herda de ConfigBD) "
                       "permite campos opcionais com total=False. "
                       "@runtime_checkable torna o Protocol verificável com isinstance() "
                       "— útil para validação em tempo de execução. "
                       "Sem herdar de Serializavel, Usuario e Produto satisfazem "
                       "o protocolo apenas por ter os métodos corretos.",
        ),
        Exemplo(
            titulo="Simulando mypy: encontrando bugs com anotações",
            codigo='''from typing import TypeVar, overload

# Exemplo de codigo que mypy detectaria erros
def dividir(a: float, b: float) -> float | None:
    """Divisao segura: retorna None se b for zero."""
    if b == 0:
        return None
    return a / b

resultado = dividir(10, 2)
# mypy sabe que resultado e 'float | None'
# Acessar resultado sem checar None e um erro de tipo!

# Correto: verificar antes de usar
if resultado is not None:
    print(f"Resultado: {resultado:.2f}")

# @overload: funcao com comportamento diferente por tipo
@overload
def processar(valor: int) -> str: ...
@overload
def processar(valor: str) -> int: ...
def processar(valor):    # implementacao real (sem anotacoes)
    if isinstance(valor, int):
        return str(valor)
    return len(valor)

# mypy sabe exatamente o que cada versao retorna
r1: str = processar(42)      # int -> str
r2: int = processar("ola")   # str -> int

print(r1, r2)

# TypeVar com bound: restringe a uma hierarquia
from typing import TypeVar

Comparavel = TypeVar("Comparavel", bound="SupportsLessThan")

class SupportsLessThan(Protocol):
    def __lt__(self, other) -> bool: ...

def minimo(a: Comparavel, b: Comparavel) -> Comparavel:
    return a if a < b else b

print(minimo(3, 5))        # 3
print(minimo("a", "z"))   # a
''',
            explicacao="float | None força o chamador a verificar None antes de usar — "
                       "mypy detecta usos sem verificação como erro. "
                       "@overload define assinaturas múltiplas para uma função "
                       "e o type checker usa a sobreposição correta. "
                       "TypeVar com bound restringe T a classes que implementam "
                       "a interface — mais restrito que TypeVar livre.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d23e1",
            enunciado=(
                "A assinatura ja tem as anotacoes de tipo. Complete a\n"
                "funcao media(notas: list[float]) -> float que calcula\n"
                "a media aritmetica da lista.\n\n"
                "Exemplos:\n"
                "   media([8.0, 6.0]) -> 7.0\n"
                "   media([])         -> 0.0   (lista vazia: retorna 0.0)\n"
                "   media.__annotations__['return'] is float -> True\n\n"
                "As anotacoes ficam em funcao.__annotations__:\n"
                "   media.__annotations__\n"
                "   -> {'notas': list[float], 'return': float}\n\n"
                "O teste verifica que '__annotations__['return'] is float'\n"
                "ou seja, que o tipo de retorno anotado e exatamente float.\n\n"
                "Implemente normalmente — as anotacoes da assinatura\n"
                "ja satisfazem o teste de __annotations__. Basta que\n"
                "a logica retorne 0.0 para lista vazia e a media correta\n"
                "para listas nao vazias."
            ),
            funcao="media",
            assinatura="def media(notas: list[float]) -> float:",
            testes=[
                ("media([8.0, 6.0])", "7.0"),
                ("media([])", "0.0"),
                ("media.__annotations__['return'] is float", "True"),
            ],
            dica="if not notas: return 0.0; return sum(notas) / len(notas)",
        ),
        Exercicio(
            id="d23e2",
            enunciado=(
                "Os imports e o TypeVar T ja estao na assinatura.\n"
                "Complete a funcao:\n"
                "   def primeiro(seq: Sequence[T]) -> T | None\n\n"
                "Ela devolve o primeiro elemento de qualquer sequencia,\n"
                "ou None se a sequencia estiver vazia.\n\n"
                "Exemplos:\n"
                "   primeiro([10, 20]) -> 10\n"
                "   primeiro([])       -> None\n"
                "   primeiro('abc')    -> 'a'\n\n"
                "Por que Sequence[T] em vez de list[T]?\n"
                "Sequence e mais abrangente: aceita list, tuple, str e\n"
                "qualquer outra sequencia indexavel. list[T] so aceitaria\n"
                "listas — 'abc' causaria erro de tipo no mypy.\n\n"
                "Por que T em vez de Any?\n"
                "T garante que o TIPO DE RETORNO e o mesmo da sequencia.\n"
                "primeiro([1, 2]) retorna int, primeiro(['a']) retorna str.\n"
                "Com Any, o type checker perderia essa informacao.\n\n"
                "Implementacao com clausula de guarda:\n"
                "   if not seq: return None\n"
                "   return seq[0]"
            ),
            funcao="primeiro",
            assinatura="from typing import Sequence, TypeVar\n\nT = TypeVar('T')\n\n\ndef primeiro(seq: Sequence[T]) -> T | None:",
            testes=[
                ("primeiro([10, 20])", "10"),
                ("primeiro([])", "None"),
                ("primeiro('abc')", "'a'"),
            ],
            dica="if not seq: return None; return seq[0]",
        ),
        Exercicio(
            id="d23e3",
            enunciado=(
                "O import Protocol e a classe TemArea ja estao na assinatura.\n"
                "Complete a funcao maior_area(formas) que recebe uma lista\n"
                "de objetos que satisfazem o protocolo TemArea e retorna\n"
                "o objeto com a maior area.\n\n"
                "O teste cria objetos anonimos com area() retornando 4.0 e 9.0\n"
                "e verifica que maior_area devolve o que tem area 9.0.\n\n"
                "Estrategia:\n"
                "   return max(formas, key=lambda f: f.area())\n\n"
                "Por que usar Protocol em vez de ABC?\n"
                "   - Com ABC: classes precisam HERDAR de TemArea\n"
                "   - Com Protocol: qualquer classe com .area() -> float funciona\n"
                "     mesmo sem herdar — duck typing com documentacao formal\n\n"
                "O protocolo TemArea ja esta definido:\n"
                "   class TemArea(Protocol):\n"
                "       def area(self) -> float: ...\n\n"
                "Sua funcao maior_area so precisa chamar max() com a\n"
                "key correta. Nao precisa verificar tipos — o Protocol\n"
                "e apenas documentacao para o type checker."
            ),
            funcao="maior_area",
            assinatura="from typing import Protocol\n\n\nclass TemArea(Protocol):\n    def area(self) -> float: ...\n\n\ndef maior_area(formas):",
            testes=[
                ("maior_area([type('Q', (), {'area': lambda s: 4.0})(), type('Q', (), {'area': lambda s: 9.0})()]).area()", "9.0"),
            ],
            nivel="dificil",
            dica="return max(formas, key=lambda f: f.area())",
        ),
    ],
    quiz=[
        Quiz(
            "Python verifica type hints em tempo de execucao?",
            ["Sim, sempre — TypeError e lancado se o tipo for errado",
             "Nao — type hints sao apenas anotacoes ignoradas pelo interpretador em tempo de execucao",
             "Depende: verifica para tipos primitivos mas ignora para colecoes",
             "Sim, mas so se você usar from __future__ import annotations"],
            1,
            "Type hints sao puramente decorativos para o Python: nao geram codigo, "
            "nao lancam excecoes, nao verificam nada em runtime. "
            "Eles existem para ferramentas externas como mypy, pyright e editores. "
            "funcao.__annotations__ guarda as anotacoes como metadados, "
            "mas o interpretador as ignora na execucao.",
        ),
        Quiz(
            "Qual a diferenca entre Optional[str] e str | None?",
            ["Optional[str] permite None; str | None nao permite",
             "Sao equivalentes: ambos significam 'str ou None'; | None e a sintaxe moderna do Python 3.10+",
             "str | None e menos preciso que Optional[str]",
             "Optional[str] e para parametros; str | None e so para retornos"],
            1,
            "Optional[X] foi criado quando nao existia o operador | para tipos. "
            "No Python 3.10+, X | None e preferido por ser mais legivel e consistente. "
            "Optional[str] ainda funciona e sera valido para sempre — "
            "mas novos codigos devem usar str | None.",
        ),
        Quiz(
            "Qual a vantagem de TypeVar T sobre Any ao anotar uma funcao generica?",
            ["T e mais rapido que Any em tempo de execucao",
             "T preserva a relacao entre tipos de entrada e saida; Any descarta essa informacao",
             "Any nao pode ser usado em funcoes — so em variaveis",
             "Nao ha diferenca pratica entre T e Any"],
            1,
            "def primeiro(seq: list[Any]) -> Any: o type checker nao sabe o tipo do retorno. "
            "def primeiro(seq: Sequence[T]) -> T: se passar list[int], sabe que retorna int. "
            "TypeVar 'captura' o tipo concreto e propaga a informacao — "
            "isso e o que permite autocompletar correto em editores.",
        ),
        Quiz(
            "Qual a diferenca entre Protocol e ABC no contexto de type hints?",
            ["Protocol e mais rapido que ABC",
             "ABC exige heranca explicita; Protocol usa tipagem estrutural (duck typing formal) — qualquer classe com os metodos corretos satisfaz o protocolo",
             "Protocol so funciona com type checkers; ABC funciona em runtime",
             "Sao identicos — Protocol e apenas um alias para ABC"],
            1,
            "ABC: class Circulo(Forma) — heranca explicita obrigatoria. "
            "Protocol: qualquer classe com def area(self) -> float satisfaz TemArea, "
            "mesmo sem herdar. "
            "Protocol formaliza o duck typing: voce documenta a interface sem impor heranca. "
            "Com @runtime_checkable, isinstance() tambem funciona.",
        ),
    ],
    projeto=(
        "Crie sistema_tipado.py com type hints completos em todas as\n"
        "funcoes e classes. Use mypy para verificar:\n\n"
        "   from typing import TypedDict, Protocol, TypeVar\n"
        "   from dataclasses import dataclass\n\n"
        "   class ItemVenda(TypedDict):\n"
        "       produto: str\n"
        "       quantidade: int\n"
        "       preco_unitario: float\n\n"
        "   class Desconto(Protocol):\n"
        "       def calcular(self, subtotal: float) -> float: ...\n\n"
        "   @dataclass\n"
        "   class Pedido:\n"
        "       cliente: str\n"
        "       itens: list[ItemVenda]\n"
        "       desconto: Desconto | None = None\n\n"
        "       def subtotal(self) -> float: ...\n"
        "       def total(self) -> float: ...\n"
        "       def adicionar(self, item: ItemVenda) -> 'Pedido': ...\n\n"
        "   class DescontoPorcentagem:\n"
        "       def __init__(self, pct: float) -> None: ...\n"
        "       def calcular(self, subtotal: float) -> float: ...\n\n"
        "   class DescontoFixo:\n"
        "       def __init__(self, valor: float) -> None: ...\n"
        "       def calcular(self, subtotal: float) -> float: ...\n\n"
        "   T = TypeVar('T')\n"
        "   def maior_por(items: list[T], chave: Callable[[T], float]) -> T | None:\n"
        "       ...\n\n"
        "Execute: mypy --strict sistema_tipado.py\n"
        "Objetivo: ZERO erros do mypy.\n\n"
        "BONUS: adicione @overload em uma funcao que aceita int e retorna\n"
        "str, ou aceita str e retorna int (conversao bidirecional)."
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/typing.html — modulo typing completo",
        "mypy.readthedocs.io — documentacao do mypy",
        "PEP 484 — Type Hints",
        "PEP 544 — Protocols: Structural subtyping",
    ],
))