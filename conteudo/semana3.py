"""Semana 3 - Dias 16 a 23: orientação a objetos e recursos avançados da linguagem."""

from nucleo.modelos import Dia, Exemplo, Exercicio, Quiz

DIAS = []

# ---------------------------------------------------------------- DIA 16
DIAS.append(Dia(
    numero=16,
    titulo="POO I: classes, objetos e estado",
    nivel="Intermediário",
    duracao="90 min",
    objetivos=[
        "Definir classes com __init__ e métodos",
        "Entender self e a diferença entre atributo de instância e de classe",
        "Modelar um problema com objetos",
        "Usar __str__ e __repr__",
    ],
    teoria="""
1. Por que objetos?
-------------------
Quando dados e comportamento andam juntos, passar dicionários e funções soltas
começa a doer. Uma classe agrupa ESTADO (atributos) e COMPORTAMENTO (métodos)
sob um mesmo nome e garante que o objeto sempre nasça consistente.

2. Anatomia
-----------
    class ContaBancaria:
        \"\"\"Conta simples com depósito e saque.\"\"\"

        taxa_manutencao = 2.5          # atributo de CLASSE (compartilhado)

        def __init__(self, titular, saldo=0.0):
            self.titular = titular      # atributo de INSTÂNCIA
            self.saldo = saldo
            self._historico = []        # _ indica uso interno

        def depositar(self, valor):
            if valor <= 0:
                raise ValueError("valor deve ser positivo")
            self.saldo += valor
            self._historico.append(("deposito", valor))
            return self.saldo

        def __str__(self):
            return f"Conta de {self.titular}: R$ {self.saldo:.2f}"

    c = ContaBancaria("Ana", 100)
    c.depositar(50)
    print(c)             # usa __str__

3. self
-------
`self` é o próprio objeto, passado automaticamente na chamada.
`c.depositar(50)` é açúcar para `ContaBancaria.depositar(c, 50)`.
O nome self é convenção — mas quebrá-la é considerado erro de estilo grave.

4. Atributo de classe x de instância
------------------------------------
    ContaBancaria.taxa_manutencao = 3.0    # muda para TODOS
    c.taxa_manutencao = 0.0                # cria um atributo SÓ para c

Armadilha: atributo de classe MUTÁVEL é compartilhado por todas as instâncias.

    class Carrinho:
        itens = []              # ERRADO: uma lista para todo mundo
Correto: criar em __init__ (`self.itens = []`).

5. __str__ x __repr__
---------------------
    __str__   texto amigável para o usuário final (usado por print e str())
    __repr__  texto técnico para o desenvolvedor (usado no REPL e em listas)

Se você só implementar um, implemente __repr__ — ele serve de reserva para o
__str__. O ideal é que repr pareça código: `Ponto(x=1, y=2)`.

6. Métodos e encapsulamento (visão inicial)
-------------------------------------------
Python não tem private de verdade. As convenções:
    nome        público
    _nome       interno (não mexa se você não escreveu a classe)
    __nome      name mangling: vira _Classe__nome, evita colisão em herança

7. Introspecção
---------------
    isinstance(c, ContaBancaria)     # True
    type(c).__name__                 # 'ContaBancaria'
    c.__dict__                       # atributos de instância
    dir(c), hasattr(c, "saldo"), getattr(c, "saldo", 0)

8. Como saber se precisa de classe?
-----------------------------------
Se você tem várias funções que recebem sempre os mesmos parâmetros, ou um
dicionário passeando por dez funções, provavelmente há uma classe escondida
ali. Se é só um agrupamento de dados sem comportamento, prefira dataclass
(Dia 19) ou até uma tupla nomeada.
""",
    exemplos=[
        Exemplo(
            titulo="Classe completa com validação",
            codigo='''class ContaBancaria:
    def __init__(self, titular, saldo=0.0):
        self.titular = titular
        self.saldo = float(saldo)
        self.extrato = []

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("deposito deve ser positivo")
        self.saldo += valor
        self.extrato.append(f"+{valor:.2f}")
        return self.saldo

    def sacar(self, valor):
        if valor > self.saldo:
            return False
        self.saldo -= valor
        self.extrato.append(f"-{valor:.2f}")
        return True

    def __repr__(self):
        return f"ContaBancaria({self.titular!r}, {self.saldo:.2f})"

c = ContaBancaria("Ana", 100)
c.depositar(50); c.sacar(30)
print(c, c.extrato)
''',
            explicacao="!r dentro da f-string aplica repr ao valor.",
        ),
        Exemplo(
            titulo="Contador de instâncias com atributo de classe",
            codigo='''class Usuario:
    total = 0

    def __init__(self, nome):
        self.nome = nome
        Usuario.total += 1        # note: Usuario, não self

a, b = Usuario("ana"), Usuario("bia")
print(Usuario.total)      # 2
''',
            explicacao="Usar self.total += 1 criaria um atributo de instância.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d16e1",
            enunciado=(
                "Crie a classe Retangulo(base, altura) com os métodos area(),\n"
                "perimetro() e eh_quadrado()."
            ),
            funcao="Retangulo",
            assinatura="class Retangulo:\n    def __init__(self, base, altura):",
            testes=[
                ("Retangulo(3, 4).area()", "12"),
                ("Retangulo(3, 4).perimetro()", "14"),
                ("Retangulo(5, 5).eh_quadrado()", "True"),
                ("Retangulo(5, 4).eh_quadrado()", "False"),
            ],
            dica="Guarde base e altura em self e use nos métodos.",
        ),
        Exercicio(
            id="d16e2",
            enunciado=(
                "Crie Ponto(x, y) com distancia(outro) — distância euclidiana —\n"
                "e __repr__ devolvendo exatamente 'Ponto(1, 2)'."
            ),
            funcao="Ponto",
            assinatura="import math\n\n\nclass Ponto:\n    def __init__(self, x, y):",
            testes=[
                ("Ponto(0, 0).distancia(Ponto(3, 4))", "5.0"),
                ("repr(Ponto(1, 2))", "'Ponto(1, 2)'"),
                ("Ponto(2, 2).distancia(Ponto(2, 2))", "0.0"),
            ],
            nivel="medio",
            dica="math.hypot(dx, dy) calcula a hipotenusa diretamente.",
        ),
        Exercicio(
            id="d16e3",
            enunciado=(
                "Crie Carrinho() com adicionar(nome, preco, qtd=1), total() e\n"
                "quantidade_itens(). Cada carrinho deve ter sua PRÓPRIA lista."
            ),
            funcao="Carrinho",
            assinatura="class Carrinho:\n    def __init__(self):",
            testes=[
                ("Carrinho().total()", "0"),
                ("(lambda c: (c.adicionar('x', 10, 2), c.total())[1])(Carrinho())", "20"),
                ("(lambda c: (c.adicionar('a', 5), c.adicionar('b', 3, 3), "
                 "c.quantidade_itens())[2])(Carrinho())", "4"),
            ],
            nivel="dificil",
            dica="Crie self.itens = [] dentro de __init__, nunca no corpo da classe.",
        ),
    ],
    quiz=[
        Quiz("O que é `self` em um método?",
             ["Uma palavra reservada", "A referência à instância atual",
              "A classe", "Um módulo"], 1,
             "self é o primeiro parâmetro e recebe o próprio objeto."),
        Quiz("Onde criar uma lista que deve ser exclusiva de cada objeto?",
             ["No corpo da classe", "Dentro de __init__ com self.",
              "Como variável global", "Em __repr__"], 1,
             "No corpo da classe ela vira atributo de classe, compartilhado."),
    ],
    projeto=(
        "Modele uma Biblioteca com as classes Livro e Biblioteca: emprestar, devolver, "
        "listar disponíveis e buscar por autor, com validações."
    ),
    leitura=["docs.python.org/pt-br/3/tutorial/classes.html"],
))

# ---------------------------------------------------------------- DIA 17
DIAS.append(Dia(
    numero=17,
    titulo="POO II: propriedades, métodos de classe e estáticos",
    nivel="Intermediário",
    duracao="90 min",
    objetivos=[
        "Controlar acesso a atributos com @property",
        "Validar dados no setter",
        "Usar @classmethod como construtor alternativo",
        "Saber quando usar @staticmethod",
    ],
    teoria="""
1. O problema
-------------
    conta.saldo = -1000     # ninguém impediu

Em Java, criaríamos getSaldo/setSaldo desde o início. Em Python, começamos com
o atributo simples e, SE precisarmos de lógica, convertemos em propriedade sem
quebrar quem já usava `objeto.saldo`.

2. @property
------------
    class Produto:
        def __init__(self, preco):
            self.preco = preco            # já passa pelo setter!

        @property
        def preco(self):                  # getter
            return self._preco

        @preco.setter
        def preco(self, valor):
            if valor < 0:
                raise ValueError("preco negativo")
            self._preco = valor

        @property
        def preco_com_imposto(self):      # atributo CALCULADO, só leitura
            return round(self._preco * 1.18, 2)

    p = Produto(100)
    p.preco = 200            # validado
    p.preco_com_imposto      # sem parênteses
    p.preco_com_imposto = 5  # AttributeError (não há setter)

Regra: se o cálculo é barato e parece um dado, use property; se é caro ou tem
efeito colateral, deixe como método comum.

3. @classmethod
---------------
Recebe a classe (cls) em vez da instância. Uso principal: construtores
alternativos (fábricas).

    class Data:
        def __init__(self, dia, mes, ano):
            self.dia, self.mes, self.ano = dia, mes, ano

        @classmethod
        def de_texto(cls, texto):          # '25/12/2026'
            d, m, a = map(int, texto.split("/"))
            return cls(d, m, a)            # cls respeita subclasses

    Data.de_texto("25/12/2026")

4. @staticmethod
----------------
Não recebe self nem cls: é apenas uma função guardada dentro da classe por
afinidade temática.

    class Validador:
        @staticmethod
        def cpf_valido(cpf):
            return len(cpf) == 11 and cpf.isdigit()

Se o método não usa nem self nem cls e não faz sentido "pertencer" à classe,
talvez devesse ser uma função de módulo. Não force.

5. Resumo comparativo
---------------------
    método comum     recebe self   opera na INSTÂNCIA
    @classmethod     recebe cls    opera na CLASSE (fábricas, contadores)
    @staticmethod    não recebe    utilitário relacionado

6. __slots__ (bônus)
--------------------
    class Ponto:
        __slots__ = ("x", "y")
Impede a criação de atributos não previstos e reduz memória (útil quando você
cria milhões de objetos). Perde a flexibilidade de atributos dinâmicos.

7. Atributos privados de verdade não existem
--------------------------------------------
    self.__segredo = 1     # acessível como obj._Classe__segredo
A cultura Python é "somos todos adultos responsáveis": o _ comunica intenção,
não impõe barreira.
""",
    exemplos=[
        Exemplo(
            titulo="Property com validação e cálculo",
            codigo='''class Temperatura:
    def __init__(self, celsius=0):
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, valor):
        if valor < -273.15:
            raise ValueError("abaixo do zero absoluto")
        self._celsius = valor

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, valor):
        self.celsius = (valor - 32) * 5 / 9

t = Temperatura(25)
print(t.fahrenheit)      # 77.0
t.fahrenheit = 212
print(t.celsius)         # 100.0
''',
            explicacao="Os dois atributos ficam sincronizados por construção.",
        ),
        Exemplo(
            titulo="Construtores alternativos",
            codigo='''class Pessoa:
    def __init__(self, nome, idade):
        self.nome, self.idade = nome, idade

    @classmethod
    def de_string(cls, linha):
        nome, idade = linha.split(",")
        return cls(nome.strip(), int(idade))

    @staticmethod
    def maioridade(idade):
        return idade >= 18

    def __repr__(self):
        return f"Pessoa({self.nome!r}, {self.idade})"

p = Pessoa.de_string("Ana, 30")
print(p, Pessoa.maioridade(p.idade))
''',
            explicacao="cls(...) garante que subclasses criem instâncias do tipo certo.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d17e1",
            enunciado=(
                "Crie Circulo(raio) com property raio que rejeita valores <= 0\n"
                "(ValueError) e property area (somente leitura, arredondada em 2 casas)."
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
            dica="No __init__ atribua self.raio = raio para passar pelo setter.",
        ),
        Exercicio(
            id="d17e2",
            enunciado=(
                "Crie Produto(nome, preco) com o classmethod de_texto('caneta:2.5')\n"
                "que cria o objeto a partir de uma string nome:preco."
            ),
            funcao="Produto",
            assinatura="class Produto:\n    def __init__(self, nome, preco):",
            testes=[
                ("Produto.de_texto('caneta:2.5').nome", "'caneta'"),
                ("Produto.de_texto('caneta:2.5').preco", "2.5"),
                ("isinstance(Produto.de_texto('x:1'), Produto)", "True"),
            ],
            dica="Use split(':'), converta o preço com float e devolva cls(...).",
        ),
        Exercicio(
            id="d17e3",
            enunciado=(
                "Crie Celsius(valor) com property fahrenheit LEGÍVEL e GRAVÁVEL:\n"
                "escrever em fahrenheit deve atualizar o valor em celsius."
            ),
            funcao="Celsius",
            assinatura="class Celsius:\n    def __init__(self, valor=0):",
            testes=[
                ("Celsius(100).fahrenheit", "212.0"),
                ("(lambda c: (setattr(c, 'fahrenheit', 32), c.valor)[1])(Celsius())", "0.0"),
                ("(lambda c: (setattr(c, 'fahrenheit', 212), round(c.valor))[1])(Celsius())", "100"),
            ],
            nivel="dificil",
            dica="No setter de fahrenheit, converta e grave em self.valor.",
        ),
    ],
    quiz=[
        Quiz("Qual a vantagem de @property sobre get_x()/set_x()?",
             ["É mais rápida", "Permite adicionar lógica sem mudar o código que usa o atributo",
              "É obrigatória", "Cria atributos privados"], 1,
             "A interface pública continua sendo objeto.x."),
        Quiz("O que @classmethod recebe como primeiro parâmetro?",
             ["self", "cls (a classe)", "nada", "o módulo"], 1,
             "cls permite criar instâncias respeitando a subclasse."),
    ],
    projeto=(
        "Evolua a ContaBancaria: saldo como property somente leitura, limite validado, "
        "classmethod de_dict() e staticmethod validar_agencia()."
    ),
    leitura=["docs.python.org/pt-br/3/library/functions.html#property"],
))

# ---------------------------------------------------------------- DIA 18
DIAS.append(Dia(
    numero=18,
    titulo="POO III: herança, polimorfismo e métodos mágicos",
    nivel="Avançado",
    duracao="100 min",
    objetivos=[
        "Reutilizar código com herança e super()",
        "Aplicar polimorfismo e duck typing",
        "Implementar dunder methods",
        "Preferir composição quando fizer sentido",
    ],
    teoria="""
1. Herança
----------
    class Animal:
        def __init__(self, nome):
            self.nome = nome
        def falar(self):
            raise NotImplementedError
        def apresentar(self):
            return f"{self.nome} diz {self.falar()}"

    class Cachorro(Animal):
        def falar(self):
            return "au"

    class Gato(Animal):
        def __init__(self, nome, vidas=7):
            super().__init__(nome)        # chame SEMPRE o pai
            self.vidas = vidas
        def falar(self):
            return "miau"

`super()` delega para a próxima classe na ordem de resolução — não
necessariamente a superclasse direta, e é isso que faz herança múltipla
funcionar de forma previsível.

2. Polimorfismo e duck typing
-----------------------------
    for bicho in [Cachorro("Rex"), Gato("Mia")]:
        print(bicho.apresentar())      # cada um responde à sua maneira

Em Python, o que importa é o objeto TER o método, não herdar de alguém:
"se anda como pato e grasna como pato, é um pato". Por isso funções genéricas
raramente checam isinstance.

3. MRO (Method Resolution Order)
--------------------------------
    class A: ...
    class B(A): ...
    class C(A): ...
    class D(B, C): ...
    D.__mro__        # D, B, C, A, object

Python usa o algoritmo C3: da esquerda para a direita, sem repetir, respeitando
a ordem de herança. Herança múltipla funciona melhor com MIXINS: classes
pequenas, sem estado, que agregam um comportamento (ex.: SerializavelJSONMixin).

4. Métodos mágicos (dunder)
---------------------------
    __init__            construção
    __repr__ __str__    representação
    __eq__ __lt__       comparação (com functools.total_ordering, os demais saem de graça)
    __hash__            permite usar em set/dict (defina junto com __eq__)
    __len__ __bool__    tamanho e veracidade
    __getitem__ __setitem__ __contains__     indexação e `in`
    __iter__ __next__   iteração
    __add__ __sub__ __mul__                  operadores
    __call__            torna o objeto chamável
    __enter__ __exit__  context manager (Dia 22)

Implementar dunders é o que integra sua classe à linguagem: len(obj),
obj1 + obj2, for x in obj passam a funcionar naturalmente.

5. Herança x composição
-----------------------
Herança expressa "É UM" (Gato É UM Animal). Composição expressa "TEM UM"
(Carro TEM UM Motor). Herança acopla fortemente: mudanças na base afetam todos
os filhos. Prefira composição quando você quer só reaproveitar código.

6. Classes abstratas
--------------------
    from abc import ABC, abstractmethod

    class Forma(ABC):
        @abstractmethod
        def area(self): ...

    Forma()        # TypeError: não pode instanciar classe abstrata

Isso garante em tempo de execução que subclasses implementem o contrato.
""",
    exemplos=[
        Exemplo(
            titulo="Hierarquia com super() e polimorfismo",
            codigo='''class Funcionario:
    def __init__(self, nome, salario):
        self.nome, self.salario = nome, salario

    def pagamento(self):
        return self.salario

    def __repr__(self):
        return f"{type(self).__name__}({self.nome!r}, {self.pagamento():.2f})"

class Vendedor(Funcionario):
    def __init__(self, nome, salario, vendas):
        super().__init__(nome, salario)
        self.vendas = vendas

    def pagamento(self):
        return super().pagamento() + self.vendas * 0.05

equipe = [Funcionario("Ana", 3000), Vendedor("Bruno", 2000, 50000)]
for f in equipe:
    print(f)
''',
            explicacao="super().pagamento() reaproveita a lógica da base.",
        ),
        Exemplo(
            titulo="Classe que se integra à linguagem via dunders",
            codigo='''class Vetor:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, outro):
        return Vetor(self.x + outro.x, self.y + outro.y)

    def __mul__(self, k):
        return Vetor(self.x * k, self.y * k)

    def __eq__(self, outro):
        return (self.x, self.y) == (outro.x, outro.y)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __repr__(self):
        return f"Vetor({self.x}, {self.y})"

v = Vetor(1, 2) + Vetor(3, 4)
print(v, v * 2, abs(Vetor(3, 4)))
''',
            explicacao="Operadores passam a funcionar como em tipos nativos.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d18e1",
            enunciado=(
                "Crie Animal(nome) com o método falar() e as subclasses Cachorro e\n"
                "Gato. apresentar() deve devolver '<nome> diz <som>'."
            ),
            funcao="Animal",
            assinatura="class Animal:\n    def __init__(self, nome):",
            testes=[
                ("Cachorro('Rex').apresentar()", "'Rex diz au'"),
                ("Gato('Mia').apresentar()", "'Mia diz miau'"),
                ("isinstance(Gato('x'), Animal)", "True"),
            ],
            dica="apresentar() fica só na base e chama self.falar().",
        ),
        Exercicio(
            id="d18e2",
            enunciado=(
                "Crie Vetor(x, y) com __add__, __eq__ e __repr__ no formato\n"
                "'Vetor(1, 2)'."
            ),
            funcao="Vetor",
            assinatura="class Vetor:\n    def __init__(self, x, y):",
            testes=[
                ("repr(Vetor(1, 2) + Vetor(3, 4))", "'Vetor(4, 6)'"),
                ("Vetor(1, 2) == Vetor(1, 2)", "True"),
                ("Vetor(1, 2) == Vetor(9, 9)", "False"),
            ],
            nivel="medio",
            dica="__add__ deve devolver um NOVO Vetor.",
        ),
        Exercicio(
            id="d18e3",
            enunciado=(
                "Crie Pilha() com empilhar(x), desempilhar(), __len__, __bool__ e\n"
                "__contains__. desempilhar() em pilha vazia devolve None."
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
            dica="Guarde uma lista interna e delegue os dunders a ela.",
        ),
    ],
    quiz=[
        Quiz("Para que serve super().__init__(...)?",
             ["Criar uma nova classe", "Executar o inicializador da classe base",
              "Apagar atributos", "Declarar herança"], 1,
             "Sem isso, a inicialização da base não acontece."),
        Quiz("O que é duck typing?",
             ["Herdar de várias classes", "Importar tipos",
              "Importar o que importa é o objeto ter o método, não o seu tipo",
              "Um tipo de erro"], 2,
             "O comportamento define a compatibilidade, não a hierarquia."),
    ],
    projeto=(
        "Crie um sistema de formas geométricas: base abstrata Forma com area() e perimetro(), "
        "subclasses Circulo, Retangulo e Triangulo, __repr__ e uma função que ordena por área."
    ),
    leitura=["docs.python.org/pt-br/3/reference/datamodel.html"],
))

# ---------------------------------------------------------------- DIA 19
DIAS.append(Dia(
    numero=19,
    titulo="dataclasses, Enum, NamedTuple e ABC",
    nivel="Avançado",
    duracao="80 min",
    objetivos=[
        "Eliminar boilerplate com @dataclass",
        "Representar conjuntos fixos de valores com Enum",
        "Usar NamedTuple para registros imutáveis",
        "Definir contratos com ABC",
    ],
    teoria="""
1. @dataclass
-------------
    from dataclasses import dataclass, field

    @dataclass
    class Produto:
        nome: str
        preco: float
        quantidade: int = 1
        tags: list = field(default_factory=list)

        def total(self):
            return self.preco * self.quantidade

O decorador gera automaticamente __init__, __repr__ e __eq__. Opções úteis:

    @dataclass(frozen=True)     imutável e hashável (pode ir em set/dict)
    @dataclass(order=True)      gera <, <=, >, >= comparando campo a campo
    @dataclass(slots=True)      usa __slots__ (3.10+), mais leve

Para valores padrão MUTÁVEIS use `field(default_factory=list)` — passar
`tags: list = []` levanta erro justamente para evitar a armadilha do Dia 11.

Funções auxiliares: `asdict(obj)`, `astuple(obj)`, `replace(obj, preco=9)`.
`__post_init__` roda depois do __init__ gerado — lugar ideal para validação.

2. Enum
-------
    from enum import Enum, auto

    class Status(Enum):
        PENDENTE = "pendente"
        PAGO = "pago"
        CANCELADO = auto()

    Status.PAGO.name      # 'PAGO'
    Status.PAGO.value     # 'pago'
    Status("pago")        # busca pelo valor
    list(Status)          # itera os membros

Enum elimina "strings mágicas" espalhadas pelo código, permite autocompletar e
falha alto quando alguém inventa um valor inválido. `IntEnum` e `StrEnum`
(3.11+) se comportam também como int/str, facilitando integração com JSON.

3. NamedTuple
-------------
    from typing import NamedTuple

    class Ponto(NamedTuple):
        x: float
        y: float = 0.0

    p = Ponto(1, 2)
    p.x, p[0]          # acesso por nome E por índice
    p._replace(x=9)
    x, y = p           # desempacota como tupla

Use quando o registro é imutável, pequeno e vai circular como tupla.
Comparação rápida:
    NamedTuple   imutável, leve, comporta-se como tupla
    dataclass    mutável por padrão, com métodos, mais flexível
    dict         chaves dinâmicas, sem garantias de estrutura

4. ABC — classe base abstrata
-----------------------------
    from abc import ABC, abstractmethod

    class Repositorio(ABC):
        @abstractmethod
        def salvar(self, item): ...

        @abstractmethod
        def buscar(self, id_): ...

        def salvar_varios(self, itens):     # método concreto herdado
            for i in itens:
                self.salvar(i)

Quem herdar e não implementar todos os métodos abstratos não consegue nem
instanciar a classe. É a forma explícita de definir uma interface.
""",
    exemplos=[
        Exemplo(
            titulo="dataclass com validação e ordenação",
            codigo='''from dataclasses import dataclass, field, asdict

@dataclass(order=True)
class Item:
    prioridade: int
    nome: str = field(compare=False)
    tags: list = field(default_factory=list, compare=False)

    def __post_init__(self):
        if self.prioridade < 0:
            raise ValueError("prioridade negativa")

itens = [Item(2, "b"), Item(1, "a")]
print(sorted(itens)[0].nome)      # a
print(asdict(itens[0]))
''',
            explicacao="compare=False deixa a ordenação só pela prioridade.",
        ),
        Exemplo(
            titulo="Enum controlando o fluxo",
            codigo='''from enum import Enum

class Status(Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    CANCELADO = "cancelado"

def pode_enviar(status):
    return status is Status.PAGO

print(pode_enviar(Status("pago")))     # True
print([s.value for s in Status])
''',
            explicacao="Compare membros de Enum com `is`.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d19e1",
            enunciado=(
                "Use @dataclass para criar Produto(nome, preco, quantidade=1)\n"
                "com o método total()."
            ),
            funcao="Produto",
            assinatura="from dataclasses import dataclass\n\n\n@dataclass\nclass Produto:",
            testes=[
                ("Produto('x', 10.0, 3).total()", "30.0"),
                ("Produto('x', 5.0).total()", "5.0"),
                ("Produto('x', 1.0) == Produto('x', 1.0)", "True"),
                ("repr(Produto('x', 1.0, 2))", "\"Produto(nome='x', preco=1.0, quantidade=2)\""),
            ],
            dica="Anote os tipos dos campos: nome: str, preco: float, quantidade: int = 1.",
        ),
        Exercicio(
            id="d19e2",
            enunciado=(
                "Crie o Enum Status com PENDENTE='pendente', PAGO='pago' e\n"
                "CANCELADO='cancelado', e a função pode_enviar(status) que só\n"
                "devolve True para PAGO."
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
            dica="Compare com `is Status.PAGO`.",
        ),
        Exercicio(
            id="d19e3",
            enunciado=(
                "Crie a classe abstrata Forma (ABC) com area() abstrata e a subclasse\n"
                "Quadrado(lado). Instanciar Forma diretamente deve falhar."
            ),
            funcao="Forma",
            assinatura="from abc import ABC, abstractmethod\n\n\nclass Forma(ABC):",
            testes=[
                ("Quadrado(3).area()", "9"),
                ("Forma()", "!raise TypeError"),
                ("isinstance(Quadrado(1), Forma)", "True"),
            ],
            nivel="dificil",
            dica="Decore o método com @abstractmethod e herde de ABC.",
        ),
    ],
    quiz=[
        Quiz("O que @dataclass gera automaticamente?",
             ["Só __init__", "__init__, __repr__ e __eq__", "Métodos de banco", "Nada"], 1,
             "E opcionalmente ordenação, imutabilidade e slots."),
        Quiz("Como declarar uma lista como valor padrão em dataclass?",
             ["tags: list = []", "tags: list = field(default_factory=list)",
              "tags = list()", "não é possível"], 1,
             "default_factory cria uma lista nova por instância."),
    ],
    projeto=(
        "Modele um sistema de pedidos: dataclass Pedido com itens, Enum StatusPedido, "
        "NamedTuple ItemPedido e uma ABC MeioPagamento com implementações Pix e Cartao."
    ),
    leitura=["docs.python.org/pt-br/3/library/dataclasses.html"],
))

# ---------------------------------------------------------------- DIA 20
DIAS.append(Dia(
    numero=20,
    titulo="Iteradores, geradores e itertools",
    nivel="Avançado",
    duracao="90 min",
    objetivos=[
        "Entender o protocolo de iteração",
        "Escrever geradores com yield",
        "Processar dados grandes com memória constante",
        "Usar itertools",
    ],
    teoria="""
1. O protocolo de iteração
--------------------------
`for x in obj` faz, por baixo:

    it = iter(obj)          # chama obj.__iter__()
    while True:
        try:
            x = next(it)    # chama it.__next__()
        except StopIteration:
            break

Iterável: tem __iter__. Iterador: tem __iter__ E __next__, e se esgota.
Uma lista é iterável mas não iterador — por isso pode ser percorrida várias
vezes; um gerador só serve uma vez.

2. Iterador escrito à mão
-------------------------
    class Contador:
        def __init__(self, fim):
            self.atual, self.fim = 0, fim
        def __iter__(self):
            return self
        def __next__(self):
            if self.atual >= self.fim:
                raise StopIteration
            self.atual += 1
            return self.atual - 1

3. Gerador: o mesmo, com 3 linhas
---------------------------------
    def contador(fim):
        atual = 0
        while atual < fim:
            yield atual          # PAUSA aqui e devolve o valor
            atual += 1

`yield` congela o estado da função. Na próxima chamada de next(), a execução
retoma exatamente de onde parou. Chamar a função NÃO executa o corpo: devolve
um objeto gerador.

4. Por que isso importa
-----------------------
    def ler_linhas(caminho):
        with open(caminho, encoding="utf-8") as f:
            for linha in f:
                yield linha.rstrip("\\n")

Um arquivo de 10 GB é processado com memória constante. Geradores permitem
sequências infinitas e pipelines encadeados:

    numeros = (n for n in contador_infinito())
    pares = (n for n in numeros if n % 2 == 0)
    primeiros = itertools.islice(pares, 5)

Nada é calculado até alguém consumir.

5. yield from e retorno
-----------------------
    def achatar(dados):
        for item in dados:
            if isinstance(item, list):
                yield from achatar(item)    # delega ao subgerador
            else:
                yield item

    def contar():
        yield 1
        return "fim"        # vira o valor de StopIteration

6. itertools — as ferramentas
-----------------------------
    count(10, 2)                 infinito: 10, 12, 14...
    cycle("ab")                  infinito: a, b, a, b...
    repeat(0, 3)                 0, 0, 0
    chain([1,2], [3])            encadeia iteráveis
    islice(iteravel, 2, 5)       fatia sem materializar
    pairwise([1,2,3])            (1,2), (2,3)          [3.10+]
    groupby(dados, key=...)      agrupa CONSECUTIVOS (ordene antes!)
    product("ab", repeat=2)      produto cartesiano
    permutations([1,2,3], 2)     arranjos
    combinations([1,2,3], 2)     combinações
    accumulate([1,2,3])          somas parciais: 1, 3, 6
    tee(iteravel, 2)             duplica um iterador

7. Cuidados
-----------
- gerador esgotado não reinicia: chame a função de novo;
- len() não funciona em geradores;
- imprimir um gerador não mostra os valores: use list(g) — mas isso o consome.
""",
    exemplos=[
        Exemplo(
            titulo="Pipeline preguiçoso de processamento",
            codigo='''import itertools

def numeros():
    n = 1
    while True:
        yield n
        n += 1

quadrados = (n * n for n in numeros())
pares = (q for q in quadrados if q % 2 == 0)
print(list(itertools.islice(pares, 5)))   # [4, 16, 36, 64, 100]
''',
            explicacao="Sequência infinita consumida sob demanda, memória constante.",
        ),
        Exemplo(
            titulo="Agrupando com groupby",
            codigo='''from itertools import groupby

dados = [("TI", "Ana"), ("RH", "Bruno"), ("TI", "Cris")]
dados.sort(key=lambda p: p[0])              # groupby exige ordenado
for setor, grupo in groupby(dados, key=lambda p: p[0]):
    print(setor, [nome for _, nome in grupo])
''',
            explicacao="Sem o sort, grupos repetidos apareceriam separados.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d20e1",
            enunciado="Escreva o GERADOR pares_ate(n) que produz os números pares de 0 a n-1.",
            funcao="pares_ate",
            assinatura="def pares_ate(n):",
            testes=[
                ("list(pares_ate(10))", "[0, 2, 4, 6, 8]"),
                ("list(pares_ate(1))", "[0]"),
                ("list(pares_ate(0))", "[]"),
            ],
            dica="Use yield dentro de um for com range.",
        ),
        Exercicio(
            id="d20e2",
            enunciado=(
                "Escreva fibonacci(n) como gerador dos n primeiros termos\n"
                "começando em 0, 1."
            ),
            funcao="fibonacci",
            assinatura="def fibonacci(n):",
            testes=[
                ("list(fibonacci(7))", "[0, 1, 1, 2, 3, 5, 8]"),
                ("list(fibonacci(1))", "[0]"),
                ("list(fibonacci(0))", "[]"),
            ],
            nivel="medio",
            dica="a, b = 0, 1 e, a cada passo, yield a antes de a, b = b, a + b.",
        ),
        Exercicio(
            id="d20e3",
            enunciado=(
                "Escreva o gerador janelas(seq, n) que produz tuplas com as janelas\n"
                "deslizantes de tamanho n. Se n > len(seq), não produz nada."
            ),
            funcao="janelas",
            assinatura="def janelas(seq, n):",
            testes=[
                ("list(janelas([1, 2, 3, 4], 2))", "[(1, 2), (2, 3), (3, 4)]"),
                ("list(janelas([1, 2], 3))", "[]"),
                ("list(janelas([1, 2, 3], 3))", "[(1, 2, 3)]"),
            ],
            nivel="dificil",
            dica="for i in range(len(seq) - n + 1): yield tuple(seq[i:i+n])",
        ),
    ],
    quiz=[
        Quiz("O que acontece ao chamar uma função que contém yield?",
             ["Executa tudo", "Devolve um gerador sem executar o corpo",
              "Erro", "Devolve uma lista"], 1,
             "O corpo só roda quando você consome o gerador."),
        Quiz("Qual a principal vantagem de um gerador sobre uma lista?",
             ["É mais curto", "Usa memória constante e permite sequências infinitas",
              "Permite índices", "É ordenado"], 1,
             "Ele produz um item por vez, sob demanda."),
    ],
    projeto=(
        "Escreva um processador de log em streaming: gerador que lê o arquivo linha a linha, "
        "outro que filtra ERRO, outro que extrai a data, e um resumo por dia — tudo sem carregar o arquivo na memória."
    ),
    leitura=["docs.python.org/pt-br/3/library/itertools.html"],
))

# ---------------------------------------------------------------- DIA 21
DIAS.append(Dia(
    numero=21,
    titulo="Decoradores e functools",
    nivel="Avançado",
    duracao="90 min",
    objetivos=[
        "Entender decoradores como açúcar sintático de funções de alta ordem",
        "Escrever decoradores com e sem argumentos",
        "Preservar metadados com functools.wraps",
        "Usar lru_cache, partial e reduce",
    ],
    teoria="""
1. A ideia
----------
    @meu_decorador
    def f(): ...

é exatamente o mesmo que:

    def f(): ...
    f = meu_decorador(f)

Decorador é uma função que recebe uma função e devolve outra função.

2. Modelo básico
----------------
    import functools

    def registrar(func):
        @functools.wraps(func)               # preserva nome e docstring
        def envelope(*args, **kwargs):
            print(f"chamando {func.__name__}")
            resultado = func(*args, **kwargs)
            print(f"{func.__name__} devolveu {resultado!r}")
            return resultado
        return envelope

    @registrar
    def somar(a, b):
        return a + b

`*args, **kwargs` no envelope garante que o decorador funcione com qualquer
assinatura. Sem `functools.wraps`, `somar.__name__` viraria 'envelope' e a
docstring sumiria — o que quebra help(), debuggers e frameworks.

3. Decorador com argumentos
---------------------------
Precisa de mais um nível: uma FÁBRICA de decoradores.

    def repetir(vezes):
        def decorador(func):
            @functools.wraps(func)
            def envelope(*args, **kwargs):
                return [func(*args, **kwargs) for _ in range(vezes)]
            return envelope
        return decorador

    @repetir(3)
    def ola():
        return "oi"
    ola()      # ['oi', 'oi', 'oi']

4. Estado no decorador
----------------------
    def contar_chamadas(func):
        @functools.wraps(func)
        def envelope(*a, **k):
            envelope.chamadas += 1
            return func(*a, **k)
        envelope.chamadas = 0        # atributo na própria função
        return envelope

5. Empilhamento
---------------
    @a
    @b
    def f(): ...
    # equivale a f = a(b(f)) — de baixo para cima

6. functools essencial
----------------------
    @lru_cache(maxsize=None)     memoização automática (argumentos hasháveis)
    @cache                       atalho para lru_cache(None)  [3.9+]
    partial(func, arg_fixo)      pré-preenche argumentos
    reduce(func, iteravel, ini)  reduz a um único valor
    @total_ordering              gera os operadores de comparação a partir de __eq__ e __lt__
    @singledispatch              sobrecarga por tipo do primeiro argumento

    @lru_cache
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)
    fib(100)          # instantâneo; sem cache seria inviável

7. Onde você já viu decoradores
-------------------------------
@property, @classmethod, @staticmethod, @dataclass, @abstractmethod, e nos
frameworks: @app.route (Flask), @pytest.fixture, @task (Celery).

8. Decoradores de classe
------------------------
Também é possível decorar classes (@dataclass é um exemplo) ou usar uma classe
com __call__ como decorador quando o estado fica complexo.
""",
    exemplos=[
        Exemplo(
            titulo="Cronômetro reutilizável",
            codigo='''import functools, time

def cronometrar(func):
    @functools.wraps(func)
    def envelope(*args, **kwargs):
        inicio = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            dur = time.perf_counter() - inicio
            print(f"{func.__name__} levou {dur:.4f}s")
    return envelope

@cronometrar
def soma_lenta(n):
    return sum(range(n))

soma_lenta(1_000_000)
''',
            explicacao="finally garante a medição mesmo se a função levantar erro.",
        ),
        Exemplo(
            titulo="Memoização com lru_cache",
            codigo='''from functools import lru_cache
import time

def fib_lento(n):
    return n if n < 2 else fib_lento(n-1) + fib_lento(n-2)

@lru_cache(maxsize=None)
def fib_rapido(n):
    return n if n < 2 else fib_rapido(n-1) + fib_rapido(n-2)

t = time.perf_counter(); fib_lento(28)
print("sem cache:", round(time.perf_counter()-t, 3))
t = time.perf_counter(); fib_rapido(200)
print("com cache:", round(time.perf_counter()-t, 6), fib_rapido.cache_info())
''',
            explicacao="Uma linha transforma exponencial em linear.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d21e1",
            enunciado=(
                "Escreva o decorador contar_chamadas(func) que adiciona o atributo\n"
                ".chamadas à função decorada, incrementado a cada chamada."
            ),
            funcao="contar_chamadas",
            assinatura="import functools\n\n\ndef contar_chamadas(func):",
            testes=[
                ("(lambda f: (f(1), f(2), f.chamadas)[2])(contar_chamadas(lambda x: x))", "2"),
                ("contar_chamadas(lambda: 1).chamadas", "0"),
                ("contar_chamadas(lambda x: x * 2)(5)", "10"),
            ],
            nivel="medio",
            dica="Defina envelope.chamadas = 0 antes de devolver o envelope.",
        ),
        Exercicio(
            id="d21e2",
            enunciado=(
                "Escreva o decorador maiusculas(func) que converte o resultado\n"
                "(string) da função para maiúsculas, preservando o nome original."
            ),
            funcao="maiusculas",
            assinatura="import functools\n\n\ndef maiusculas(func):",
            testes=[
                ("maiusculas(lambda: 'oi')()", "'OI'"),
                ("maiusculas(lambda n: f'ola {n}')('ana')", "'OLA ANA'"),
            ],
            dica="Chame a função, aplique .upper() no retorno e use @functools.wraps.",
        ),
        Exercicio(
            id="d21e3",
            enunciado=(
                "Escreva a fábrica repetir(vezes) que devolve um decorador; a função\n"
                "decorada passa a devolver a LISTA com `vezes` execuções do resultado."
            ),
            funcao="repetir",
            assinatura="import functools\n\n\ndef repetir(vezes):",
            testes=[
                ("repetir(3)(lambda: 'x')()", "['x', 'x', 'x']"),
                ("repetir(2)(lambda a, b: a + b)(1, 2)", "[3, 3]"),
                ("repetir(0)(lambda: 1)()", "[]"),
            ],
            nivel="dificil",
            dica="Três níveis: repetir -> decorador -> envelope.",
        ),
    ],
    quiz=[
        Quiz("@dec sobre def f() equivale a:",
             ["f = dec", "f = dec(f)", "dec = f", "f()"], 1,
             "O decorador substitui a função pelo retorno da chamada."),
        Quiz("Para que serve functools.wraps?",
             ["Acelerar a função", "Preservar __name__ e __doc__ da função original",
              "Criar cache", "Validar argumentos"], 1,
             "Sem ele, a introspecção enxerga o envelope."),
    ],
    projeto=(
        "Crie um módulo de decoradores utilitários: @cronometrar, @tentar_novamente(n) com espera, "
        "@validar_tipos usando anotações e @memorizar próprio — e demonstre todos."
    ),
    leitura=["docs.python.org/pt-br/3/library/functools.html", "PEP 318"],
))

# ---------------------------------------------------------------- DIA 22
DIAS.append(Dia(
    numero=22,
    titulo="Context managers e gerenciamento de recursos",
    nivel="Avançado",
    duracao="70 min",
    objetivos=[
        "Entender o protocolo __enter__/__exit__",
        "Criar context managers com contextlib",
        "Suprimir e tratar exceções na saída",
        "Usar ExitStack para recursos dinâmicos",
    ],
    teoria="""
1. O que o `with` faz
---------------------
    with EXPR as var:
        corpo

vira, aproximadamente:

    gerenciador = EXPR
    var = gerenciador.__enter__()
    try:
        corpo
    finally:
        gerenciador.__exit__(tipo, valor, traceback)

Ou seja: garante a limpeza. Serve para arquivos, sockets, locks, transações de
banco, cronômetros, diretórios temporários, redirecionamento de saída.

2. Implementando com classe
---------------------------
    class Cronometro:
        def __enter__(self):
            self.inicio = time.perf_counter()
            return self                 # o que vai para o `as`

        def __exit__(self, exc_tipo, exc_valor, tb):
            self.duracao = time.perf_counter() - self.inicio
            return False                # False = propaga a exceção

Se __exit__ devolver True, a exceção é SUPRIMIDA. Devolver True sem querer é
um bug clássico: erros somem silenciosamente.

3. Implementando com @contextmanager
------------------------------------
    from contextlib import contextmanager

    @contextmanager
    def transacao(conexao):
        try:
            yield conexao          # tudo antes do yield = __enter__
            conexao.commit()       # tudo depois = __exit__
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()

Deve haver exatamente UM yield. O try/finally é obrigatório se você precisa
garantir a limpeza mesmo com exceção.

4. Ferramentas do contextlib
----------------------------
    suppress(FileNotFoundError)      ignora exceções específicas
    redirect_stdout(buffer)          captura prints
    closing(objeto)                  chama .close() na saída
    nullcontext(valor)               "não faz nada" (útil como padrão)
    ExitStack()                      pilha dinâmica de gerenciadores

    from contextlib import suppress
    with suppress(FileNotFoundError):
        Path("talvez.txt").unlink()

    with ExitStack() as pilha:
        arquivos = [pilha.enter_context(open(n)) for n in nomes]

5. Vários gerenciadores de uma vez
----------------------------------
    with open("a") as fa, open("b", "w") as fb:
        fb.write(fa.read())

Parênteses para quebrar em linhas (3.10+):
    with (open("a") as fa, open("b") as fb):
        ...

6. Casos práticos
-----------------
    tempfile.TemporaryDirectory()    pasta que se apaga sozinha
    threading.Lock()                 região crítica
    unittest.mock.patch()            substituição temporária em testes
    decimal.localcontext()           precisão local
""",
    exemplos=[
        Exemplo(
            titulo="Cronômetro como context manager",
            codigo='''import time

class Cronometro:
    def __init__(self, nome="bloco"):
        self.nome = nome

    def __enter__(self):
        self.inicio = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self.duracao = time.perf_counter() - self.inicio
        print(f"{self.nome}: {self.duracao:.4f}s")
        return False

with Cronometro("soma") as c:
    total = sum(range(2_000_000))
print(total, round(c.duracao, 3))
''',
            explicacao="Devolver self permite consultar dados depois do bloco.",
        ),
        Exemplo(
            titulo="Escrita atômica com @contextmanager",
            codigo='''from contextlib import contextmanager
from pathlib import Path

@contextmanager
def escrita_atomica(caminho):
    destino = Path(caminho)
    temporario = destino.with_suffix(destino.suffix + ".tmp")
    arquivo = temporario.open("w", encoding="utf-8")
    try:
        yield arquivo
        arquivo.close()
        temporario.replace(destino)     # só troca se deu tudo certo
    except BaseException:
        arquivo.close()
        temporario.unlink(missing_ok=True)
        raise

with escrita_atomica("/tmp/config.txt") as f:
    f.write("tema=escuro\\n")
print(Path("/tmp/config.txt").read_text())
''',
            explicacao="O arquivo final nunca fica pela metade.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d22e1",
            enunciado=(
                "Crie a classe Coletor (context manager): dentro do with, add(x)\n"
                "acumula valores e, ao SAIR do bloco, o atributo .total guarda a soma.\n"
                "Escreva também somar_com(valores), que usa `with Coletor() as c`,\n"
                "adiciona cada valor e devolve c.total DEPOIS do bloco."
            ),
            funcao="Coletor",
            assinatura=("class Coletor:\n    def __enter__(self):\n        ...\n\n"
                        "    def __exit__(self, *exc):\n        ...\n\n\n"
                        "def somar_com(valores):"),
            testes=[
                ("somar_com([1, 2, 3])", "6"),
                ("somar_com([])", "0"),
                ("somar_com([10])", "10"),
            ],
            nivel="medio",
            dica="Crie a lista em __enter__ (devolvendo self) e calcule self.total em __exit__.",
        ),
        Exercicio(
            id="d22e2",
            enunciado=(
                "Use @contextmanager para criar silenciar(), que captura o que for\n"
                "impresso no bloco (o objeto do `as` deve ter .getvalue()).\n"
                "Escreva também capturar(texto), que imprime texto dentro do with e\n"
                "devolve o conteúdo capturado."
            ),
            funcao="silenciar",
            assinatura=("import io\nfrom contextlib import contextmanager, redirect_stdout"
                        "\n\n\n@contextmanager\ndef silenciar():\n    ...\n\n\n"
                        "def capturar(texto):"),
            testes=[
                ("capturar('oi')", "'oi\\n'"),
                ("capturar('')", "'\\n'"),
            ],
            nivel="dificil",
            dica="Dentro de silenciar: buf = io.StringIO(); with redirect_stdout(buf): yield buf",
        ),
        Exercicio(
            id="d22e3",
            enunciado=(
                "Escreva ignorar_erro(func) que executa func() dentro de um bloco\n"
                "com contextlib.suppress(ZeroDivisionError) e devolve o resultado\n"
                "ou None se a divisão por zero foi suprimida."
            ),
            funcao="ignorar_erro",
            assinatura="from contextlib import suppress\n\n\ndef ignorar_erro(func):",
            testes=[
                ("ignorar_erro(lambda: 10 / 2)", "5.0"),
                ("ignorar_erro(lambda: 1 / 0)", "None"),
            ],
            dica="Inicialize resultado = None antes do with e atribua dentro.",
        ),
    ],
    quiz=[
        Quiz("O que acontece se __exit__ devolver True?",
             ["Nada", "A exceção é suprimida", "O bloco reinicia", "Erro"], 1,
             "Devolver True engole a exceção — use com cuidado."),
        Quiz("Quantos yields deve ter uma função com @contextmanager?",
             ["Zero", "Exatamente um", "Dois", "Quantos quiser"], 1,
             "Antes do yield é a entrada; depois, a saída."),
    ],
    projeto=(
        "Implemente um gerenciador de conexão simulado com commit/rollback automático, "
        "um TempDir próprio e um MudarDiretorio que volta ao diretório original ao sair."
    ),
    leitura=["docs.python.org/pt-br/3/library/contextlib.html", "PEP 343"],
))

# ---------------------------------------------------------------- DIA 23
DIAS.append(Dia(
    numero=23,
    titulo="Type hints e código auto-documentado",
    nivel="Avançado",
    duracao="80 min",
    objetivos=[
        "Anotar funções, variáveis e classes",
        "Usar Optional, Union, tipos genéricos e Callable",
        "Verificar tipos estaticamente com mypy",
        "Conhecer Protocol e TypedDict",
    ],
    teoria="""
1. Anotações não mudam a execução
---------------------------------
    def somar(a: int, b: int) -> int:
        return a + b

    somar("x", "y")     # roda normalmente! Python NÃO valida em tempo de execução

O ganho está em: leitura, autocompletar da IDE, detecção de erros antes de
rodar (mypy, pyright) e documentação que não desatualiza.

2. Sintaxe moderna (3.9+/3.10+)
-------------------------------
    nomes: list[str] = []
    notas: dict[str, float] = {}
    par: tuple[int, str] = (1, "a")
    varios: tuple[int, ...] = (1, 2, 3)
    talvez: str | None = None            # antes: Optional[str]
    numero: int | float = 0              # antes: Union[int, float]

Antes do 3.9 era preciso importar List, Dict, Tuple de `typing`. Hoje use os
tipos nativos.

3. Callable, Any, TypeAlias
---------------------------
    from typing import Callable, Any, Iterable, Iterator, Sequence

    def aplicar(f: Callable[[int, int], int], a: int, b: int) -> int:
        return f(a, b)

    Matriz = list[list[float]]                # alias
    def processar(dados: Iterable[str]) -> Iterator[str]: ...

Prefira o tipo mais ABSTRATO possível nos parâmetros (Iterable, Sequence,
Mapping) e o mais CONCRETO no retorno.

4. Genéricos
------------
    from typing import TypeVar, Generic
    T = TypeVar("T")

    class Caixa(Generic[T]):
        def __init__(self, item: T) -> None:
            self.item = item
        def pegar(self) -> T:
            return self.item

    def primeiro(seq: Sequence[T]) -> T | None:
        return seq[0] if seq else None

Em 3.12+ há a sintaxe enxuta: `def primeiro[T](seq: Sequence[T]) -> T | None:`

5. Protocol — duck typing tipado
--------------------------------
    from typing import Protocol

    class TemArea(Protocol):
        def area(self) -> float: ...

    def maior(formas: list[TemArea]) -> TemArea:
        return max(formas, key=lambda f: f.area())

Qualquer classe com o método area() é compatível — sem herdar nada.

6. TypedDict e Literal
----------------------
    from typing import TypedDict, Literal, Final

    class Usuario(TypedDict):
        nome: str
        idade: int

    Nivel = Literal["debug", "info", "erro"]
    VERSAO: Final = "1.0"

7. mypy na prática
------------------
    pip install mypy
    mypy meu_arquivo.py
    mypy --strict pacote/

Comece sem --strict, anote as funções públicas primeiro e vá apertando.
`# type: ignore[codigo]` silencia um caso pontual.
Em tempo de execução, `typing.get_type_hints(func)` devolve as anotações
resolvidas — é assim que Pydantic e FastAPI funcionam.
""",
    exemplos=[
        Exemplo(
            titulo="Módulo totalmente anotado",
            codigo='''from dataclasses import dataclass
from typing import Iterable

@dataclass
class Aluno:
    nome: str
    notas: list[float]

    def media(self) -> float:
        return sum(self.notas) / len(self.notas) if self.notas else 0.0

def aprovados(alunos: Iterable[Aluno], corte: float = 6.0) -> list[str]:
    return [a.nome for a in alunos if a.media() >= corte]

print(aprovados([Aluno("Ana", [9, 8]), Aluno("Bo", [4, 5])]))
''',
            explicacao="A assinatura já explica o contrato sem precisar de comentário.",
        ),
        Exemplo(
            titulo="Protocol em ação",
            codigo='''from typing import Protocol

class Serializavel(Protocol):
    def para_dict(self) -> dict: ...

class Pedido:
    def __init__(self, id_: int) -> None:
        self.id = id_
    def para_dict(self) -> dict:
        return {"id": self.id}

def exportar(itens: list[Serializavel]) -> list[dict]:
    return [i.para_dict() for i in itens]

print(exportar([Pedido(1), Pedido(2)]))
''',
            explicacao="Pedido não herda de Serializavel, mas satisfaz o protocolo.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d23e1",
            enunciado=(
                "Escreva media(notas: list[float]) -> float, anotada, devolvendo 0.0\n"
                "para lista vazia. Os testes checam as anotações."
            ),
            funcao="media",
            assinatura="def media(notas: list[float]) -> float:",
            testes=[
                ("media([8.0, 6.0])", "7.0"),
                ("media([])", "0.0"),
                ("media.__annotations__['return'] is float", "True"),
            ],
            dica="As anotações ficam disponíveis em funcao.__annotations__.",
        ),
        Exercicio(
            id="d23e2",
            enunciado=(
                "Escreva primeiro(seq) anotada com TypeVar, devolvendo o primeiro\n"
                "elemento ou None se a sequência estiver vazia."
            ),
            funcao="primeiro",
            assinatura=("from typing import Sequence, TypeVar\n\nT = TypeVar('T')\n\n\n"
                        "def primeiro(seq: Sequence[T]) -> T | None:"),
            testes=[
                ("primeiro([10, 20])", "10"),
                ("primeiro([])", "None"),
                ("primeiro('abc')", "'a'"),
            ],
            dica="Uma cláusula de guarda resolve: if not seq: return None.",
        ),
        Exercicio(
            id="d23e3",
            enunciado=(
                "Crie o Protocol TemArea (com area() -> float) e a função\n"
                "maior_area(formas) que devolve o objeto de maior área."
            ),
            funcao="maior_area",
            assinatura=("from typing import Protocol\n\n\nclass TemArea(Protocol):\n"
                        "    def area(self) -> float: ...\n\n\ndef maior_area(formas):"),
            testes=[
                ("maior_area([type('Q', (), {'area': lambda s: 4.0})(), "
                 "type('Q', (), {'area': lambda s: 9.0})()]).area()", "9.0"),
            ],
            nivel="dificil",
            dica="max(formas, key=lambda f: f.area())",
        ),
    ],
    quiz=[
        Quiz("O que acontece se você passar o tipo errado numa função anotada?",
             ["TypeError na hora", "Nada em tempo de execução; só ferramentas estáticas acusam",
              "O valor é convertido", "O programa não inicia"], 1,
             "Anotações são metadados; a checagem é feita por mypy/pyright."),
        Quiz("Como escrever 'string ou None' em Python 3.10+?",
             ["str|None", "Optional(str)", "str?", "Maybe[str]"], 0,
             "O operador | substituiu Optional/Union."),
    ],
    projeto=(
        "Pegue um dos seus projetos anteriores, anote todas as funções e classes, "
        "rode mypy --strict e corrija até zerar os avisos."
    ),
    leitura=["docs.python.org/pt-br/3/library/typing.html", "PEP 484", "PEP 604"],
))