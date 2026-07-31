"""Semana 3 - Dias 16 a 23: orientação a objetos e recursos avançados da linguagem."""

from nucleo.modelos import Dia, Exemplo, Exercicio, Quiz

DIAS = []

# ---------------------------------------------------------------- DIA 16
DIAS.append(Dia(
    numero=16,
    titulo="POO I: classes, objetos e estado",
    nivel="Intermediário",
    duracao="100 min",
    objetivos=[
        "Explicar por que agrupar dados e comportamento numa classe resolve um problema real",
        "Definir classes com __init__ e métodos, entendendo o papel exato de self",
        "Diferenciar atributo de instância de atributo de classe, e a armadilha do atributo mutável",
        "Usar __str__ e __repr__ para dar identidade legível a um objeto",
        "Aplicar as convenções de encapsulamento do Python (_ e __) e saber seus limites reais",
        "Reconhecer quando um problema pede uma classe e quando pede apenas uma função ou dataclass",
    ],
    teoria="""
1. Por que objetos? O problema que a POO resolve
-----------------------------------------------------------
Até aqui, seus programas guardaram dados em dicionários e listas, e
comportamento em funções separadas que recebiam esses dados como
parâmetro. Isso funciona bem para programas pequenos, mas começa a doer
quando o mesmo conjunto de dados precisa passar por MUITAS funções
diferentes, todas esperando exatamente o mesmo formato de dicionário — e
nada impede que uma delas receba um dicionário incompleto ou mal formado.

Uma classe resolve isso agrupando ESTADO (os atributos, ou seja, os dados)
e COMPORTAMENTO (os métodos, ou seja, as funções que operam sobre esses
dados) sob um único nome, e garantindo — através do construtor — que todo
objeto criado já nasça em um estado consistente, sem depender de quem o usa
lembrar de preencher tudo corretamente.

2. Anatomia de uma classe
------------------------------
    class ContaBancaria:
        \"\"\"Conta simples com depósito e saque.\"\"\"

        taxa_manutencao = 2.5          # atributo de CLASSE (compartilhado por todas as contas)

        def __init__(self, titular, saldo=0.0):
            self.titular = titular      # atributo de INSTÂNCIA (cada conta tem o seu)
            self.saldo = saldo
            self._historico = []        # o _ no início sinaliza "uso interno"

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
    print(c)             # usa __str__ automaticamente

`__init__` é o CONSTRUTOR: o método especial chamado automaticamente
sempre que uma nova instância é criada com `ContaBancaria(...)`. É ali, e
só ali, que o objeto recebe seus valores iniciais — depois de sair do
`__init__`, o objeto já deve estar em um estado válido e utilizável.

3. self: o objeto se referenciando a si mesmo
----------------------------------------------------
`self` é o próprio objeto, passado AUTOMATICAMENTE como primeiro
argumento sempre que você chama um método através de uma instância. Na
prática, `c.depositar(50)` é apenas açúcar sintático para
`ContaBancaria.depositar(c, 50)` — Python insere o objeto `c` como
primeiro argumento por trás dos panos.

O nome `self` é apenas uma CONVENÇÃO — tecnicamente você poderia chamar
esse primeiro parâmetro de qualquer coisa —, mas quebrar essa convenção é
considerado um erro de estilo grave, porque toda a comunidade Python
espera encontrar `self` ali, e ferramentas de análise de código também
assumem essa convenção.

4. Atributo de instância versus atributo de classe
--------------------------------------------------------
    ContaBancaria.taxa_manutencao = 3.0    # muda o valor para TODAS as contas existentes e futuras
    c.taxa_manutencao = 0.0                # cria um atributo NOVO, só para o objeto c

Atributos de CLASSE (declarados diretamente no corpo da classe, fora de
qualquer método) são compartilhados por todas as instâncias — mudar o
valor pela classe afeta todo mundo que ainda não tenha um valor próprio
sobrescrevendo-o. Atributos de INSTÂNCIA (criados dentro de `__init__` com
`self.algo = ...`) pertencem exclusivamente àquele objeto.

Existe uma armadilha séria aqui, muito parecida com a do valor padrão
mutável em funções (Dia 11): se o atributo de CLASSE for um objeto
MUTÁVEL (uma lista, por exemplo), ele é compartilhado entre TODAS as
instâncias, o que quase nunca é o que se pretende:

    class Carrinho:
        itens = []              # ERRADO: existe UMA lista para TODOS os carrinhos!

    a = Carrinho()
    b = Carrinho()
    a.itens.append("caneta")
    print(b.itens)               # ['caneta'] — apareceu no carrinho de b também!

A correção é sempre criar listas, dicionários e outros objetos mutáveis
DENTRO de `__init__`, atribuindo a `self`, para que cada instância receba
o seu próprio objeto independente:

    class Carrinho:
        def __init__(self):
            self.itens = []      # CORRETO: uma lista nova a cada objeto criado

5. __str__ versus __repr__: dois públicos diferentes
------------------------------------------------------------
    __str__   texto amigável, pensado para o USUÁRIO FINAL (usado por print() e str())
    __repr__  texto técnico, pensado para o DESENVOLVEDOR (usado no REPL e dentro de listas)

Se você só puder implementar um dos dois, implemente `__repr__` — ele
serve como reserva automática para `__str__` quando este não existe (mas o
inverso não é verdade). A convenção da comunidade é que `__repr__`
pareça código Python válido, capaz de recriar o objeto: algo como
`Ponto(x=1, y=2)`, não uma frase em português.

6. Encapsulamento em Python: convenção, não imposição
------------------------------------------------------------
Diferente de linguagens como Java ou C++, Python não tem um modificador
`private` de verdade que IMPEÇA o acesso externo a um atributo. Existem
apenas convenções, respeitadas por acordo cultural entre programadores:

    nome        público — parte da interface oficial da classe
    _nome       "interno": um aviso de "não mexa aqui se você não escreveu esta classe"
    __nome      name mangling: o Python renomeia internamente para _Classe__nome,
                dificultando (mas não impedindo) colisões acidentais em herança

Essa filosofia é resumida na expressão "somos todos adultos aqui" (we're
all consenting adults), presente até no Zen do Python: a linguagem confia
que o programador vai respeitar as convenções, em vez de impor barreiras
técnicas rígidas que, em outras linguagens, às vezes acabam sendo
contornadas de formas ainda mais complicadas.

7. Introspecção: perguntando ao objeto sobre si mesmo
------------------------------------------------------------
    isinstance(c, ContaBancaria)     # True: c é uma instância dessa classe (ou de uma subclasse)
    type(c).__name__                 # 'ContaBancaria': o nome do tipo, como texto
    c.__dict__                       # dicionário com os atributos de INSTÂNCIA de c
    dir(c)                           # lista tudo que o objeto sabe fazer (métodos e atributos)
    hasattr(c, "saldo")              # True/False: o objeto tem esse atributo?
    getattr(c, "saldo", 0)           # pega o atributo, ou devolve 0 se não existir

Essas ferramentas são particularmente úteis ao explorar uma biblioteca ou
classe desconhecida no REPL, sem precisar abrir a documentação — o próprio
objeto revela sua estrutura.

8. Como saber se um problema realmente pede uma classe?
------------------------------------------------------------------
Um sinal claro de que uma classe está "escondida" no seu código: você
percebe que várias funções diferentes sempre recebem os mesmos parâmetros
juntos, ou que um mesmo dicionário circula por dez funções distintas,
sempre com as mesmas chaves esperadas. Isso sugere que esses dados e
funções deveriam estar reunidos sob uma classe.

Por outro lado, se o que você precisa é apenas um AGRUPAMENTO de dados,
sem comportamento associado (sem métodos que fazem cálculos ou validações
sobre esses dados), a ferramenta mais adequada costuma ser uma
`dataclass` (Dia 19) ou até uma tupla nomeada — estruturas mais leves que
uma classe completa escrita à mão.
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
            explicacao="!r dentro da f-string aplica repr ao valor, útil "
                       "para ver aspas em strings dentro de mensagens de depuração.",
        ),
        Exemplo(
            titulo="Contador de instâncias com atributo de classe",
            codigo='''class Usuario:
    total = 0

    def __init__(self, nome):
        self.nome = nome
        Usuario.total += 1        # note: Usuario, nao self — e proposital

a, b = Usuario("ana"), Usuario("bia")
print(Usuario.total)      # 2
''',
            explicacao="Usar self.total += 1 aqui criaria um atributo de "
                       "INSTÂNCIA chamado total, deixando o contador de "
                       "classe intocado — o oposto do que se pretende.",
        ),
        Exemplo(
            titulo="A armadilha do atributo de classe mutável, ao vivo",
            codigo='''class CarrinhoErrado:
    itens = []          # UMA lista compartilhada por TODOS os carrinhos

class CarrinhoCerto:
    def __init__(self):
        self.itens = []  # uma lista NOVA a cada carrinho criado

a1, a2 = CarrinhoErrado(), CarrinhoErrado()
a1.itens.append("caneta")
print(a2.itens)          # ['caneta']  -- vazou para o outro carrinho!

b1, b2 = CarrinhoCerto(), CarrinhoCerto()
b1.itens.append("caneta")
print(b2.itens)          # []  -- cada carrinho tem sua propria lista
''',
            explicacao="O mesmo padrão de bug do argumento padrão mutável "
                       "(Dia 11), agora no contexto de atributos de classe.",
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
             "self é o primeiro parâmetro e recebe o próprio objeto, passado automaticamente pelo Python."),
        Quiz("Onde criar uma lista que deve ser exclusiva de cada objeto?",
             ["No corpo da classe", "Dentro de __init__ com self.",
              "Como variável global", "Em __repr__"], 1,
             "No corpo da classe ela vira atributo de classe, compartilhado entre todas as instâncias."),
        Quiz("Se você não implementar __str__ mas implementar __repr__, o que print(objeto) mostra?",
             ["Um erro, pois __str__ é obrigatório", "O endereço de memória cru",
              "O resultado de __repr__, que serve de reserva", "Sempre 'object at 0x...'"], 2,
             "__repr__ funciona como fallback automático para __str__ quando este não é definido."),
        Quiz("O prefixo __nome (dois underscores) em um atributo faz o quê exatamente?",
             ["Torna o atributo impossível de acessar de fora", "Aplica name mangling, renomeando para _Classe__nome (dificulta, mas não impede acesso)",
              "Cria um atributo de classe", "Não tem efeito nenhum"], 1,
             "É uma barreira de convenção mais forte que o _ simples, mas ainda contornável — Python não tem private de verdade."),
    ],
    projeto=(
        "Modele uma Biblioteca com as classes Livro e Biblioteca: emprestar, devolver, "
        "listar disponíveis e buscar por autor, com validações. Preste atenção especial "
        "em onde a lista de livros emprestados é criada."
    ),
    leitura=["docs.python.org/pt-br/3/tutorial/classes.html", "PEP 20 (o Zen do Python, item sobre 'namespaces')"],
))

# ---------------------------------------------------------------- DIA 17
DIAS.append(Dia(
    numero=17,
    titulo="POO II: propriedades, métodos de classe e estáticos",
    nivel="Intermediário",
    duracao="100 min",
    objetivos=[
        "Explicar o problema que @property resolve e por que Python o faz de forma diferente de Java",
        "Validar dados no setter de uma propriedade, sem quebrar quem já usa o atributo",
        "Criar atributos calculados, somente leitura, com @property",
        "Usar @classmethod como construtor alternativo (padrão de fábrica)",
        "Saber quando @staticmethod é apropriado, e quando na verdade deveria ser uma função de módulo",
        "Conhecer __slots__ como otimização de memória, e seu trade-off",
    ],
    teoria="""
1. O problema que motiva @property
----------------------------------------
    conta.saldo = -1000     # nada impede isso, se saldo for um atributo comum

Em linguagens como Java, a prática recomendada desde o início é NUNCA
expor atributos diretamente — sempre criar `getSaldo()`/`setSaldo()`,
mesmo quando eles só fazem a atribuição trivial, "por garantia". Python
segue uma filosofia diferente: comece com o atributo público simples
(`self.saldo = saldo`), e SÓ SE, mais tarde, você precisar de validação
ou de um cálculo, converta esse atributo em uma propriedade — sem que o
código que já usa `objeto.saldo = valor` precise mudar uma única linha.
Essa é uma das vantagens práticas mais citadas do design de `@property`.

2. @property: getter, setter e atributo calculado
--------------------------------------------------------
    class Produto:
        def __init__(self, preco):
            self.preco = preco            # já passa pelo SETTER, mesmo aqui no __init__!

        @property
        def preco(self):                  # o GETTER
            return self._preco

        @preco.setter
        def preco(self, valor):
            if valor < 0:
                raise ValueError("preco negativo")
            self._preco = valor

        @property
        def preco_com_imposto(self):      # atributo CALCULADO, só leitura (sem setter)
            return round(self._preco * 1.18, 2)

    p = Produto(100)
    p.preco = 200            # passa pela validação do setter
    p.preco_com_imposto      # acessado SEM parênteses, como um atributo comum
    p.preco_com_imposto = 5  # AttributeError: não existe @preco_com_imposto.setter

Note que, dentro do próprio `__init__`, a linha `self.preco = preco` já
passa pelo setter decorado — é assim que a validação se aplica também na
criação do objeto, não só em atribuições posteriores.

A regra prática para decidir entre `@property` e um método comum: se o
cálculo é BARATO (rápido) e semanticamente PARECE um dado do objeto (como
"preço com imposto"), use property; se é CARO (uma consulta a banco de
dados, uma chamada de rede) ou tem EFEITO COLATERAL, prefira deixá-lo como
um método comum (`objeto.calcular_algo()`), para que quem lê o código veja
os parênteses e entenda que ali pode haver trabalho sendo feito.

3. @classmethod: fábricas de construção alternativas
-----------------------------------------------------------
Um método de classe recebe `cls` (a própria CLASSE) como primeiro
argumento, em vez de `self` (a instância). O uso mais comum, de longe, é
criar CONSTRUTORES ALTERNATIVOS — formas diferentes de montar um objeto a
partir de dados em outro formato:

    class Data:
        def __init__(self, dia, mes, ano):
            self.dia, self.mes, self.ano = dia, mes, ano

        @classmethod
        def de_texto(cls, texto):          # recebe algo como '25/12/2026'
            d, m, a = map(int, texto.split("/"))
            return cls(d, m, a)            # cls(...), não Data(...) — respeita subclasses!

    Data.de_texto("25/12/2026")

Usar `cls(...)` em vez de escrever o nome da classe diretamente
(`Data(...)`) é o que garante que, se alguém criar uma subclasse de
`Data`, chamar `Subclasse.de_texto(...)` produza uma instância de
`Subclasse`, não de `Data` — o método herda o comportamento correto
automaticamente, sem precisar ser reescrito.

4. @staticmethod: uma função guardada por afinidade temática
------------------------------------------------------------------
Um método estático não recebe nem `self` nem `cls` — na prática, é apenas
uma função comum que vive DENTRO do namespace da classe, por conveniência
de organização:

    class Validador:
        @staticmethod
        def cpf_valido(cpf):
            return len(cpf) == 11 and cpf.isdigit()

O critério prático para escolher `@staticmethod`: se o método não usa nem
`self` nem `cls` E faz sentido logicamente "pertencer" àquela classe (por
exemplo, uma validação diretamente relacionada aos dados que a classe
representa), é um bom candidato. Se ele não usa nem um nem outro e também
não tem relação temática forte com a classe, talvez devesse simplesmente
ser uma função solta no módulo — forçar tudo a virar método estático
"porque parece mais organizado" é um antipadrão comum entre quem está
aprendendo POO.

5. Resumo comparativo dos três tipos de método
------------------------------------------------------
    método comum (padrão)   recebe self    opera sobre uma INSTÂNCIA específica
    @classmethod             recebe cls     opera sobre a CLASSE (fábricas, contadores globais)
    @staticmethod             não recebe nada especial   utilitário relacionado ao tema da classe

6. __slots__: um bônus de otimização de memória
------------------------------------------------------
    class Ponto:
        __slots__ = ("x", "y")

Por padrão, cada instância de uma classe Python carrega um dicionário
interno (`__dict__`) para guardar seus atributos — flexível, mas com um
custo de memória por objeto. Declarar `__slots__` com os nomes exatos dos
atributos permitidos elimina esse dicionário, reduzindo o consumo de
memória por instância — uma otimização que só costuma valer a pena quando
seu programa cria MILHÕES de objetos da mesma classe. O custo é perder a
flexibilidade de adicionar atributos dinamicamente fora da lista declarada
em `__slots__` — tentar isso levanta `AttributeError`.

7. Reforçando: atributos "privados" de verdade não existem
------------------------------------------------------------------
    self.__segredo = 1     # continua acessível de fora, como obj._Classe__segredo

Isso retoma o ponto do Dia 16: mesmo o name mangling do `__` duplo não é
uma barreira de segurança real, apenas uma dificuldade adicional para
colisões acidentais. A cultura Python continua sendo "somos todos adultos
responsáveis" — o underscore comunica INTENÇÃO ("não deveria mexer
aqui"), não impõe uma restrição técnica inquebrável.
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
            explicacao="Os dois atributos ficam sincronizados por "
                       "construção: alterar fahrenheit recalcula celsius, "
                       "porque o setter de fahrenheit delega para o setter de celsius.",
        ),
        Exemplo(
            titulo="Construtores alternativos com classmethod e staticmethod",
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
            explicacao="cls(...) garante que subclasses de Pessoa criem "
                       "instâncias do tipo certo ao chamar de_string; "
                       "maioridade nem precisa de um objeto para ser chamado.",
        ),
        Exemplo(
            titulo="O mesmo atributo, com e sem property",
            codigo='''class SemProtecao:
    def __init__(self, saldo):
        self.saldo = saldo

class ComProtecao:
    def __init__(self, saldo):
        self.saldo = saldo    # ja passa pelo setter

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        if valor < 0:
            raise ValueError("saldo nao pode ser negativo")
        self._saldo = valor

a = SemProtecao(100)
a.saldo = -500          # aceito sem aviso nenhum

b = ComProtecao(100)
try:
    b.saldo = -500
except ValueError as e:
    print("bloqueado:", e)
''',
            explicacao="A interface pública (objeto.saldo) é idêntica nos "
                       "dois casos — a diferença fica invisível para quem "
                       "usa a classe corretamente, e só aparece quando "
                       "alguém tenta um valor inválido.",
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
        Quiz("Qual a vantagem de @property sobre get_x()/set_x() escritos manualmente?",
             ["É mais rápida em tempo de execução", "Permite adicionar validação ou cálculo sem mudar a interface pública (objeto.x continua funcionando)",
              "É obrigatória em toda classe Python", "Cria atributos privados de verdade"], 1,
             "Quem já usava objeto.x continua usando exatamente da mesma forma, mesmo depois de você adicionar lógica no setter."),
        Quiz("O que @classmethod recebe como primeiro parâmetro?",
             ["self", "cls (a classe)", "nada", "o módulo"], 1,
             "cls permite que o método crie instâncias respeitando a subclasse que o chamou, não só a classe original."),
        Quiz("Quando faz mais sentido usar @staticmethod em vez de uma função solta no módulo?",
             ["Sempre, staticmethod é sempre melhor", "Quando o método não usa self/cls, mas tem forte relação temática com a classe",
              "Nunca, staticmethod é um recurso obsoleto", "Apenas quando a classe tem herança múltipla"], 1,
             "Se não há relação temática nem uso de self/cls, geralmente uma função de módulo comum é mais simples."),
        Quiz("Qual é o principal custo de usar __slots__ numa classe?",
             ["O código fica mais lento", "Perde-se a flexibilidade de adicionar atributos fora dos declarados",
              "Não é mais possível criar métodos", "A classe deixa de aceitar herança"], 1,
             "__slots__ economiza memória eliminando o __dict__ por instância, mas restringe quais atributos podem existir."),
    ],
    projeto=(
        "Evolua a ContaBancaria: saldo como property somente leitura, limite validado, "
        "classmethod de_dict() e staticmethod validar_agencia()."
    ),
    leitura=["docs.python.org/pt-br/3/library/functions.html#property", "docs.python.org/pt-br/3/reference/datamodel.html#slots"],
))

# ---------------------------------------------------------------- DIA 18
DIAS.append(Dia(
    numero=18,
    titulo="POO III: herança, polimorfismo e métodos mágicos",
    nivel="Avançado",
    duracao="110 min",
    objetivos=[
        "Reutilizar código com herança, usando super() corretamente",
        "Explicar polimorfismo e duck typing com exemplos concretos",
        "Entender a ordem de resolução de métodos (MRO) em herança múltipla",
        "Implementar métodos mágicos (dunder) que integram uma classe à linguagem",
        "Decidir entre herança ('é um') e composição ('tem um') com um critério prático",
        "Usar classes abstratas (ABC) para impor um contrato a subclasses",
    ],
    teoria="""
1. Herança: reaproveitando comportamento entre classes relacionadas
------------------------------------------------------------------------------
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
            super().__init__(nome)        # SEMPRE chame o inicializador do pai
            self.vidas = vidas
        def falar(self):
            return "miau"

`super()` delega a chamada para a PRÓXIMA classe na ordem de resolução de
métodos (MRO, seção 3) — que, em herança simples, é a superclasse direta,
mas em herança múltipla pode ser outra classe na cadeia. É exatamente esse
mecanismo, mais sofisticado do que "chamar o pai diretamente", que permite
herança múltipla funcionar de forma previsível, sem chamar o mesmo
inicializador duas vezes acidentalmente.

Um princípio a internalizar: sempre que você sobrescrever `__init__` numa
subclasse, chame `super().__init__(...)` explicitamente, a menos que
tenha um motivo deliberado para não inicializar a parte herdada — do
contrário, atributos que a classe base esperava configurar (como `self.nome`
aqui) simplesmente não existirão na subclasse.

2. Polimorfismo e duck typing
-----------------------------------
    for bicho in [Cachorro("Rex"), Gato("Mia")]:
        print(bicho.apresentar())      # cada um responde à sua própria maneira

Polimorfismo é a ideia de que o MESMO código (`bicho.apresentar()`) produz
comportamentos diferentes dependendo do tipo real do objeto, sem que quem
escreveu o laço precise saber qual subclasse específica está em mãos.

Em Python, essa flexibilidade vai além da herança formal: o que
efetivamente importa é o objeto TER o método esperado, não descender de
uma classe específica — o princípio conhecido como "duck typing" ("se anda
como um pato e grasna como um pato, é tratado como um pato"). Por essa
razão, funções Python idiomáticas raramente fazem checagens explícitas de
`isinstance()` antes de chamar um método — elas simplesmente chamam o
método e confiam que, se o objeto não o tiver, um erro claro (`AttributeError`)
vai aparecer ali mesmo.

3. MRO (Method Resolution Order): a ordem de busca em herança múltipla
------------------------------------------------------------------------------
    class A: ...
    class B(A): ...
    class C(A): ...
    class D(B, C): ...
    D.__mro__        # (D, B, C, A, object)

Quando uma classe herda de mais de uma classe ao mesmo tempo (herança
múltipla), Python precisa de uma regra determinística para decidir, ao
buscar um método, em qual ordem procurar entre as várias classes-base. O
algoritmo usado é o C3 linearization: busca da esquerda para a direita,
sem repetir uma classe já visitada, e sempre respeitando a ordem de
declaração de herança.

Herança múltipla direta costuma ser complexa de raciocinar; a comunidade
Python geralmente recomenda usar esse recurso através de MIXINS — classes
pequenas, sem estado próprio (sem `__init__` que crie atributos), que
adicionam UM comportamento específico e bem isolado (por exemplo, uma
`SerializavelJSONMixin` que só adiciona um método `para_json()`).

4. Métodos mágicos (dunder): integrando sua classe à linguagem
------------------------------------------------------------------------
    __init__            construção do objeto
    __repr__ __str__    representação textual (Dia 16)
    __eq__ __lt__       comparação (com functools.total_ordering, os demais operadores saem "de graça")
    __hash__            permite que instâncias sejam usadas em set/dict (defina sempre junto com __eq__)
    __len__ __bool__    tamanho (para len(obj)) e veracidade (para if obj:)
    __getitem__ __setitem__ __contains__     indexação (obj[i]) e o operador in
    __iter__ __next__   protocolo de iteração (Dia 20)
    __add__ __sub__ __mul__                  sobrecarga de operadores aritméticos
    __call__            torna instâncias do objeto CHAMÁVEIS, como se fossem funções: obj(x)
    __enter__ __exit__  protocolo de context manager (Dia 22)

Implementar dunders é literalmente o que torna sua classe "cidadã de
primeira classe" na linguagem: depois de definir `__len__`, `len(obj)`
passa a funcionar; depois de `__add__`, `obj1 + obj2` funciona; depois de
`__iter__`, `for x in obj` funciona — tudo isso sem que o usuário da
classe precise chamar métodos com nomes especiais, só os operadores e
funções que já conhece dos tipos embutidos.

5. Herança ("é um") versus composição ("tem um")
------------------------------------------------------------
Herança expressa uma relação "É UM": um Gato É UM Animal, então herdar faz
sentido semântico. Composição expressa uma relação "TEM UM": um Carro TEM
UM Motor — o Carro não deveria HERDAR de Motor, apenas guardar uma
instância de Motor como atributo.

    class Motor:
        def ligar(self): ...

    class Carro:
        def __init__(self):
            self.motor = Motor()      # composição: Carro TEM UM Motor
        def ligar(self):
            self.motor.ligar()        # delega a chamada

A razão prática para preferir composição quando a relação é "tem um": herança
cria um ACOPLAMENTO FORTE — qualquer mudança na classe base pode afetar
(às vezes de forma inesperada) TODAS as subclasses que dependem dela.
Composição é mais flexível: trocar a implementação interna (o Motor) não
exige mudar a estrutura de herança do Carro. Um princípio de design
conhecido resume isso: "prefira composição a herança" sempre que a
motivação for apenas REAPROVEITAR código, guardando herança para quando
existe de fato uma relação de tipo (é-um) legítima.

6. Classes abstratas: impondo um contrato
----------------------------------------------
    from abc import ABC, abstractmethod

    class Forma(ABC):
        @abstractmethod
        def area(self): ...

    Forma()        # TypeError: Can't instantiate abstract class Forma with abstract method area

Herdar de `ABC` e marcar um método com `@abstractmethod` garante, em
TEMPO DE EXECUÇÃO, que nenhuma subclasse consiga ser instanciada sem
implementar todos os métodos abstratos declarados — é a forma explícita de
Python de definir uma INTERFACE que qualquer implementação concreta é
obrigada a respeitar, algo que outras linguagens fariam com uma palavra-
chave `interface` dedicada.
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
            explicacao="super().pagamento() reaproveita a lógica da base "
                       "(devolver o salário) e só ACRESCENTA a comissão, "
                       "sem duplicar o cálculo do salário base.",
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
            explicacao="Depois de implementados, esses operadores passam a "
                       "funcionar em Vetor exatamente como funcionam em int "
                       "ou float — sem nenhuma sintaxe especial extra no uso.",
        ),
        Exemplo(
            titulo="Herança versus composição, lado a lado",
            codigo='''class Motor:
    def __init__(self, potencia):
        self.potencia = potencia
    def ligar(self):
        return f"motor de {self.potencia}cv ligado"

# Composicao: Carro TEM UM motor -- mais flexivel
class Carro:
    def __init__(self, potencia):
        self.motor = Motor(potencia)
    def ligar(self):
        return self.motor.ligar()

carro = Carro(120)
print(carro.ligar())
print(isinstance(carro, Motor))   # False -- e o esperado: Carro nao E UM Motor
''',
            explicacao="Se Carro herdasse de Motor, ele passaria a ser um "
                       "tipo de Motor tecnicamente, o que não corresponde à "
                       "relação real entre os dois conceitos.",
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
             "Sem isso, os atributos que o __init__ da base configuraria não existiriam na subclasse."),
        Quiz("O que é duck typing?",
             ["Herdar de várias classes ao mesmo tempo", "Importar tipos de outros módulos",
              "O que importa é o objeto ter o método esperado, não seu tipo declarado ou sua hierarquia",
              "Um tipo específico de erro de execução"], 2,
             "O comportamento (ter o método) define a compatibilidade, não a árvore de herança formal."),
        Quiz("Qual critério prático ajuda a escolher entre herança e composição?",
             ["Herança é sempre melhor por reaproveitar mais código", "Se a relação é 'é um', considere herança; se é 'tem um', prefira composição",
              "Composição nunca deve ser usada em Python", "A escolha não faz diferença prática"], 1,
             "Um Gato É UM Animal (herança faz sentido); um Carro TEM UM Motor (composição é mais apropriada)."),
        Quiz("O que acontece ao tentar instanciar uma classe ABC com um @abstractmethod não implementado?",
             ["Funciona normalmente, o método fica None", "TypeError é levantado, impedindo a instanciação",
              "Um aviso é impresso, mas o objeto é criado", "Apenas ferramentas como mypy detectam isso"], 1,
             "A checagem ocorre em tempo de execução: Python literalmente impede a criação do objeto."),
    ],
    projeto=(
        "Crie um sistema de formas geométricas: base abstrata Forma com area() e perimetro(), "
        "subclasses Circulo, Retangulo e Triangulo, __repr__ e uma função que ordena por área."
    ),
    leitura=["docs.python.org/pt-br/3/reference/datamodel.html", "docs.python.org/pt-br/3/tutorial/classes.html#multiple-inheritance"],
))
# ---------------------------------------------------------------- DIA 19
DIAS.append(Dia(
    numero=19,
    titulo="dataclasses, Enum, NamedTuple e ABC",
    nivel="Avançado",
    duracao="90 min",
    objetivos=[
        "Eliminar boilerplate repetitivo com @dataclass, entendendo o que ele gera automaticamente",
        "Representar conjuntos fixos e nomeados de valores com Enum, evitando 'strings mágicas'",
        "Usar NamedTuple para registros imutáveis e leves",
        "Definir contratos formais com ABC e diferenciar quando usar cada uma dessas quatro ferramentas",
    ],
    teoria="""
1. @dataclass: quando a classe é principalmente sobre dados
------------------------------------------------------------------
    from dataclasses import dataclass, field

    @dataclass
    class Produto:
        nome: str
        preco: float
        quantidade: int = 1
        tags: list = field(default_factory=list)

        def total(self):
            return self.preco * self.quantidade

Escrever uma classe "tradicional" só para guardar alguns campos exige
repetir o mesmo `__init__` (atribuindo cada parâmetro a `self`), depois um
`__repr__` para debug legível, e depois um `__eq__` para comparar duas
instâncias por conteúdo — um boilerplate mecânico que praticamente nunca
muda de padrão. O decorador `@dataclass` GERA essas três coisas
automaticamente a partir das anotações de tipo dos campos: `__init__`,
`__repr__` e `__eq__` já vêm prontos, sem você escrever uma linha.

Opções úteis do decorador, combináveis entre si:

    @dataclass(frozen=True)     torna a instância IMUTÁVEL e HASHÁVEL (pode entrar em set/dict)
    @dataclass(order=True)      gera <, <=, >, >=, comparando campo a campo, na ordem declarada
    @dataclass(slots=True)      usa __slots__ por baixo dos panos (Python 3.10+), mais leve em memória

Para um valor padrão que seja um objeto MUTÁVEL (lista, dicionário,
conjunto), é preciso usar `field(default_factory=...)` em vez de escrever o
valor diretamente — a própria linguagem levanta um erro se você tentar
`tags: list = []` diretamente, JUSTAMENTE para evitar a armadilha do
argumento padrão mutável (Dia 11), que aqui teria o mesmo efeito
colateral perigoso entre instâncias diferentes.

Algumas funções auxiliares do módulo `dataclasses` completam o pacote:
`asdict(obj)` converte a instância para um dicionário comum;
`astuple(obj)` converte para tupla; `replace(obj, preco=9)` cria uma CÓPIA
do objeto com apenas um campo alterado, sem mutar o original (útil
principalmente com `frozen=True`). E `__post_init__`, se você o definir,
roda automaticamente logo depois do `__init__` gerado — o lugar ideal para
validações que dependem de mais de um campo ao mesmo tempo.

2. Enum: dando nome a um conjunto fixo de valores
--------------------------------------------------------
    from enum import Enum, auto

    class Status(Enum):
        PENDENTE = "pendente"
        PAGO = "pago"
        CANCELADO = auto()          # gera um valor automaticamente (aqui, um int)

    Status.PAGO.name      # 'PAGO'   -- o nome do membro
    Status.PAGO.value     # 'pago'   -- o valor associado
    Status("pago")        # busca um membro PELO VALOR
    list(Status)          # itera todos os membros da enumeração

Antes de `Enum` existir, era comum representar status ou categorias com
strings soltas espalhadas pelo código (`"pendente"`, `"pago"`), o que traz
dois problemas: um erro de digitação (`"pendete"`) só é descoberto em
tempo de execução, silenciosamente, e não há como o editor de código
autocompletar os valores válidos. `Enum` resolve os dois: qualquer valor
inválido falha imediatamente ao tentar criar o membro (`Status("invalido")`
levanta `ValueError`), e o autocompletar da IDE já sugere os membros
existentes. `IntEnum` e `StrEnum` (este último desde o Python 3.11) vão
além: seus membros também se comportam como `int` ou `str` de verdade,
facilitando a integração direta com JSON e bancos de dados.

3. NamedTuple: um registro imutável que também é uma tupla
------------------------------------------------------------------
    from typing import NamedTuple

    class Ponto(NamedTuple):
        x: float
        y: float = 0.0

    p = Ponto(1, 2)
    p.x, p[0]          # acesso por NOME e por ÍNDICE funcionam igualmente
    p._replace(x=9)    # cria uma cópia com um campo alterado (não muta p)
    x, y = p           # desempacota exatamente como uma tupla comum

`NamedTuple` é a escolha certa quando o registro é imutável, pequeno, e
precisa circular pelo programa se comportando como uma tupla comum em
qualquer lugar que espere uma (por exemplo, como chave de dicionário, ou
desempacotado num `for`). Um resumo comparativo entre as três estruturas
mais usadas para "agrupar dados relacionados":

    NamedTuple   imutável, leve, comporta-se como tupla (aceito onde tuplas são esperadas)
    dataclass    mutável por padrão (a menos que frozen=True), aceita métodos, mais flexível
    dict comum   chaves totalmente dinâmicas, sem garantia estrutural nenhuma sobre quais existem

4. ABC — classe base abstrata, formalizando um contrato
------------------------------------------------------------------
    from abc import ABC, abstractmethod

    class Repositorio(ABC):
        @abstractmethod
        def salvar(self, item): ...

        @abstractmethod
        def buscar(self, id_): ...

        def salvar_varios(self, itens):     # método CONCRETO, herdado normalmente
            for i in itens:
                self.salvar(i)

Uma `ABC` pode misturar métodos abstratos (que toda subclasse É OBRIGADA a
implementar, sob pena de não conseguir ser instanciada — como vimos no Dia
18) com métodos CONCRETOS já prontos, que todas as subclasses herdam
gratuitamente (aqui, `salvar_varios` já funciona para qualquer subclasse
que tenha implementado `salvar`). Essa combinação é a forma mais explícita
que Python oferece de definir uma INTERFACE com parte da implementação já
compartilhada.

Um critério rápido para escolher entre as quatro ferramentas deste dia:
dados fixos e imutáveis que circulam como tupla -> `NamedTuple`; dados que
podem mudar e/ou têm métodos próprios -> `dataclass`; um conjunto fechado
e nomeado de opções válidas -> `Enum`; um contrato que várias
implementações diferentes precisam seguir -> `ABC`.
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
            explicacao="compare=False remove nome e tags da comparação "
                       "gerada automaticamente, deixando a ordenação "
                       "depender só do campo prioridade.",
        ),
        Exemplo(
            titulo="Enum controlando o fluxo do programa",
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
            explicacao="Compare membros de Enum com `is`, não `==` — eles "
                       "são valores únicos e singleton, então is funciona "
                       "com segurança e é a convenção recomendada.",
        ),
        Exemplo(
            titulo="As quatro ferramentas, lado a lado",
            codigo='''from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple
from abc import ABC, abstractmethod

class Prioridade(Enum):          # conjunto fechado de opções nomeadas
    BAIXA = 1
    ALTA = 2

class Coordenada(NamedTuple):    # registro fixo, imutavel, tupla-like
    x: float
    y: float

@dataclass
class Tarefa:                     # dados mutaveis, com metodos proprios
    titulo: str
    prioridade: Prioridade

class Notificador(ABC):           # contrato que implementacoes seguem
    @abstractmethod
    def enviar(self, mensagem): ...

t = Tarefa("revisar PR", Prioridade.ALTA)
c = Coordenada(10, 20)
print(t, c)
''',
            explicacao="Cada ferramenta resolve um problema diferente: "
                       "escolher a certa evita reescrever manualmente o "
                       "que ela já oferece pronto.",
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
        Quiz("O que @dataclass gera automaticamente a partir dos campos anotados?",
             ["Só __init__", "__init__, __repr__ e __eq__", "Métodos de acesso a banco de dados", "Nada, é apenas decorativo"], 1,
             "E, opcionalmente, comparação de ordem (order=True), imutabilidade (frozen=True) e slots (slots=True)."),
        Quiz("Como declarar corretamente uma lista como valor padrão em uma dataclass?",
             ["tags: list = []", "tags: list = field(default_factory=list)",
              "tags = list()", "não é possível ter listas em dataclass"], 1,
             "default_factory garante uma lista NOVA por instância, evitando o compartilhamento indevido."),
        Quiz("Por que comparar membros de Enum com 'is' é preferível a '=='?",
             ["is é apenas uma preferência estética sem diferença real", "Membros de Enum são valores únicos (singleton); is expressa isso com precisão e é a convenção",
              "== não funciona com Enum", "is é mais lento, mas mais seguro"], 1,
             "Cada membro existe uma única vez no programa, tornando is tanto correto quanto idiomático."),
        Quiz("Quando NamedTuple é mais apropriado que dataclass?",
             ["Sempre, NamedTuple substitui completamente dataclass", "Quando o registro é pequeno, imutável e precisa se comportar como uma tupla comum",
              "Quando você precisa de métodos complexos", "NamedTuple e dataclass são idênticos em tudo"], 1,
             "NamedTuple é aceito em qualquer lugar que espera uma tupla (desempacotamento, chave de dict); dataclass é mais flexível, mas não tem essa propriedade."),
    ],
    projeto=(
        "Modele um sistema de pedidos: dataclass Pedido com itens, Enum StatusPedido, "
        "NamedTuple ItemPedido e uma ABC MeioPagamento com implementações Pix e Cartao."
    ),
    leitura=["docs.python.org/pt-br/3/library/dataclasses.html", "docs.python.org/pt-br/3/library/enum.html"],
))

# ---------------------------------------------------------------- DIA 20
DIAS.append(Dia(
    numero=20,
    titulo="Iteradores, geradores e itertools",
    nivel="Avançado",
    duracao="100 min",
    objetivos=[
        "Entender o protocolo de iteração que sustenta todo 'for' da linguagem",
        "Escrever um iterador manualmente, para depois apreciar o que o yield economiza",
        "Escrever geradores com yield e explicar por que eles pausam e retomam a execução",
        "Processar dados potencialmente enormes com memória praticamente constante",
        "Usar as ferramentas mais úteis de itertools em vez de reimplementá-las",
        "Reconhecer as limitações de um gerador: esgota-se, não tem len(), não reinicia",
    ],
    teoria="""
1. O protocolo de iteração: o que `for` realmente faz por baixo
------------------------------------------------------------------------
Todo `for x in obj:` que você já escreveu, desde o Dia 7, é, na verdade,
açúcar sintático para um processo mais explícito:

    it = iter(obj)          # chama obj.__iter__(), pedindo um ITERADOR
    while True:
        try:
            x = next(it)    # chama it.__next__(), pedindo o PRÓXIMO valor
        except StopIteration:
            break            # o iterador sinalizou "acabou"

A distinção entre ITERÁVEL e ITERADOR, embora sutil, explica um
comportamento que costuma confundir: um ITERÁVEL é qualquer objeto que tem
`__iter__` (uma lista, por exemplo); um ITERADOR tem tanto `__iter__`
quanto `__next__`, E se ESGOTA depois de percorrido uma vez. Uma lista é
iterável, mas NÃO é ela mesma um iterador — cada `for` sobre a mesma lista
cria um iterador novo do zero, por isso você pode percorrer a mesma lista
quantas vezes quiser. Um GERADOR (seção 3), por outro lado, é ao mesmo
tempo iterável e iterador — e por isso só serve para UMA única passada.

2. Escrevendo um iterador manualmente, à moda antiga
------------------------------------------------------------
    class Contador:
        def __init__(self, fim):
            self.atual, self.fim = 0, fim
        def __iter__(self):
            return self                    # o próprio objeto é seu iterador
        def __next__(self):
            if self.atual >= self.fim:
                raise StopIteration         # sinaliza o fim da iteração
            self.atual += 1
            return self.atual - 1

Esse padrão — implementar `__iter__` (devolvendo `self`) e `__next__`
(devolvendo o próximo valor ou levantando `StopIteration`) — é o jeito
"manual", explícito, de criar algo que funciona com `for`. Funciona, mas
exige gerenciar o estado (`self.atual`) manualmente, com um risco real de
bugs se essa lógica ficar mais complexa.

3. Gerador: o mesmo resultado, com três linhas
--------------------------------------------------
    def contador(fim):
        atual = 0
        while atual < fim:
            yield atual          # PAUSA a execução aqui e devolve o valor
            atual += 1

A palavra-chave `yield` é o que transforma uma função comum em uma
FUNÇÃO GERADORA: ao encontrar `yield`, a execução da função CONGELA
naquele exato ponto (preservando todas as variáveis locais, como `atual`
aqui) e devolve o valor para quem chamou `next()`. Na PRÓXIMA chamada de
`next()`, a execução RETOMA exatamente de onde parou, como se nada tivesse
acontecido no meio.

Um detalhe que surpreende iniciantes: CHAMAR a função geradora
(`contador(5)`) NÃO executa nada do corpo ainda — apenas cria e devolve o
objeto gerador. O corpo só começa a rodar de fato quando algo pede o
primeiro valor (via `next()` ou um `for`).

4. Por que isso importa na prática: memória constante
------------------------------------------------------------
    def ler_linhas(caminho):
        with open(caminho, encoding="utf-8") as f:
            for linha in f:
                yield linha.rstrip("\\n")

Um arquivo de 10 GB pode ser processado linha a linha com este gerador
usando uma quantidade de memória praticamente CONSTANTE — nunca mais que
algumas linhas por vez estão na memória simultaneamente, independente do
tamanho total do arquivo. Geradores também permitem representar SEQUÊNCIAS
INFINITAS (que jamais caberiam numa lista) e encadear PIPELINES de
transformação, onde nada é de fato calculado até que alguém, no final da
cadeia, efetivamente consuma o resultado:

    numeros = (n for n in contador_infinito())
    pares = (n for n in numeros if n % 2 == 0)
    primeiros = itertools.islice(pares, 5)     # só agora, ao materializar, algo é calculado

5. yield from e o valor de retorno de um gerador
------------------------------------------------------------
    def achatar(dados):
        for item in dados:
            if isinstance(item, list):
                yield from achatar(item)    # delega TODOS os valores do subgerador
            else:
                yield item

`yield from` é um atalho para "produza cada valor deste outro iterável,
um por um", evitando escrever um `for` interno explícito com `yield` a
cada item — muito usado em geradores recursivos, como este exemplo que
achata uma lista aninhada (compare com a versão recursiva não-geradora do
Dia 12).

Um gerador também pode ter um `return` com valor (diferente de uma função
comum, esse valor não é "perdido" — ele se torna o atributo `.value` da
exceção `StopIteration` levantada ao final, algo usado principalmente por
bibliotecas avançadas de coroutines, mas raro no dia a dia).

6. itertools: as ferramentas prontas antes de reinventar a roda
------------------------------------------------------------------------
    count(10, 2)                 infinito: 10, 12, 14, 16...
    cycle("ab")                  infinito: a, b, a, b, a, b...
    repeat(0, 3)                 0, 0, 0
    chain([1,2], [3])            encadeia vários iteráveis em sequência, como se fossem um só
    islice(iteravel, 2, 5)       fatia um iterável sem precisar materializá-lo em lista antes
    pairwise([1,2,3])            produz (1,2), (2,3)                      [Python 3.10+]
    groupby(dados, key=...)      agrupa elementos CONSECUTIVOS (é preciso ordenar antes!)
    product("ab", repeat=2)      produto cartesiano
    permutations([1,2,3], 2)     arranjos (ordem importa)
    combinations([1,2,3], 2)     combinações (ordem não importa)
    accumulate([1,2,3])          somas parciais, produzindo 1, 3, 6
    tee(iteravel, 2)             duplica um iterador em dois independentes

7. Cuidados ao trabalhar com geradores
------------------------------------------
- um gerador ESGOTADO não reinicia sozinho: se você precisar percorrer os
  mesmos valores de novo, é preciso chamar a função geradora NOVAMENTE,
  criando um objeto gerador novo;
- `len()` não funciona em um gerador — ele não sabe, de antemão, quantos
  valores ainda vai produzir (em alguns casos, nem existe um limite);
- imprimir um gerador diretamente não mostra os valores dentro dele (mostra
  algo como `<generator object ... at 0x...>`) — para ver os valores,
  `list(gerador)` funciona, mas isso CONSOME o gerador por completo, então
  ele não pode mais ser usado depois disso.
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
            explicacao="Uma sequência INFINITA (numeros()) é consumida sob "
                       "demanda através de duas transformações encadeadas, "
                       "usando memória constante o tempo todo.",
        ),
        Exemplo(
            titulo="Agrupando com groupby",
            codigo='''from itertools import groupby

dados = [("TI", "Ana"), ("RH", "Bruno"), ("TI", "Cris")]
dados.sort(key=lambda p: p[0])              # groupby EXIGE que os dados ja estejam ordenados
for setor, grupo in groupby(dados, key=lambda p: p[0]):
    print(setor, [nome for _, nome in grupo])
''',
            explicacao="Sem o sort explícito antes, grupos com o mesmo "
                       "setor mas não-consecutivos apareceriam separados, "
                       "porque groupby só agrupa elementos vizinhos.",
        ),
        Exemplo(
            titulo="Um gerador se esgota; uma lista, não",
            codigo='''def gerar_tres():
    yield 1
    yield 2
    yield 3

g = gerar_tres()
print(list(g))     # [1, 2, 3]
print(list(g))     # [] -- o gerador ja foi consumido inteiramente!

lista = [1, 2, 3]
print(list(lista)) # [1, 2, 3]
print(list(lista)) # [1, 2, 3] -- listas podem ser percorridas quantas vezes quiser
''',
            explicacao="Se você precisar percorrer os mesmos valores mais "
                       "de uma vez, chame gerar_tres() novamente para obter "
                       "um gerador novo, ou materialize em lista desde o início.",
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
             ["Executa o corpo inteiro imediatamente", "Devolve um objeto gerador, sem executar o corpo ainda",
              "Levanta um erro", "Devolve uma lista já pronta"], 1,
             "O corpo só começa a rodar quando algo pede o primeiro valor via next() ou for."),
        Quiz("Qual a principal vantagem de um gerador sobre uma lista já construída?",
             ["O código fica mais curto para escrever", "Usa memória praticamente constante e permite sequências infinitas",
              "Permite acesso por índice, como lista[3]", "Gera sempre valores ordenados"], 1,
             "Ele produz um item por vez, sob demanda, sem guardar tudo na memória de uma só vez."),
        Quiz("O que acontece se você tentar percorrer um gerador já esgotado pela segunda vez?",
             ["Ele reinicia do começo automaticamente", "Devolve uma sequência vazia, sem erro",
              "Levanta uma exceção obrigatoriamente", "Devolve os mesmos valores de antes"], 1,
             "Um gerador esgotado simplesmente não produz mais nada; para repetir, é preciso criar um gerador novo chamando a função de novo."),
        Quiz("Por que itertools.groupby exige que os dados estejam ordenados pela chave antes de usá-lo?",
             ["Não exige nada disso, é só uma recomendação estética", "Ele só agrupa elementos CONSECUTIVOS; sem ordenação, grupos iguais não-vizinhos aparecem separados",
              "groupby ordena os dados sozinho por padrão", "Só funciona com números, nunca com strings"], 1,
             "groupby percorre a sequência uma vez e fecha um grupo assim que o valor da chave muda — por isso precisa vir pré-ordenada."),
    ],
    projeto=(
        "Escreva um processador de log em streaming: gerador que lê o arquivo linha a linha, "
        "outro que filtra ERRO, outro que extrai a data, e um resumo por dia — tudo sem carregar o arquivo na memória."
    ),
    leitura=["docs.python.org/pt-br/3/library/itertools.html", "docs.python.org/pt-br/3/tutorial/classes.html#generators"],
))

# ---------------------------------------------------------------- DIA 21
DIAS.append(Dia(
    numero=21,
    titulo="Decoradores e functools",
    nivel="Avançado",
    duracao="100 min",
    objetivos=[
        "Entender decoradores como açúcar sintático de funções de alta ordem, sem mistério",
        "Escrever decoradores simples e decoradores que aceitam argumentos próprios",
        "Explicar por que functools.wraps é essencial, e o que quebra sem ele",
        "Adicionar estado a um decorador (contadores, cache manual)",
        "Usar lru_cache, partial e reduce da biblioteca padrão em vez de reimplementá-los",
        "Reconhecer decoradores já usados em dias anteriores do curso, agora entendendo como funcionam por dentro",
    ],
    teoria="""
1. A ideia central: decorador é só uma função de alta ordem
------------------------------------------------------------------
    @meu_decorador
    def f(): ...

é EXATAMENTE equivalente, sem mágica nenhuma escondida, a:

    def f(): ...
    f = meu_decorador(f)

Um decorador é simplesmente uma função que RECEBE uma função e DEVOLVE
outra função (geralmente uma versão "envelopada" da original, com
comportamento extra antes e/ou depois). O `@` é apenas uma forma mais
legível de escrever essa reatribuição, colocada logo acima da definição em
vez de logo abaixo dela.

2. O modelo básico de um decorador
----------------------------------------
    import functools

    def registrar(func):
        @functools.wraps(func)               # preserva nome e docstring da funcao original
        def envelope(*args, **kwargs):
            print(f"chamando {func.__name__}")
            resultado = func(*args, **kwargs)
            print(f"{func.__name__} devolveu {resultado!r}")
            return resultado
        return envelope

    @registrar
    def somar(a, b):
        return a + b

O uso de `*args, **kwargs` na assinatura de `envelope` garante que o
decorador funcione com QUALQUER função decorada, não importa quantos
parâmetros ela receba — o envelope simplesmente repassa tudo adiante, sem
precisar conhecer a assinatura específica da função original.

Sem `functools.wraps(func)`, algo sutil e prejudicial acontece:
`somar.__name__` passaria a valer `'envelope'` (o nome da função interna do
decorador), e a docstring original de `somar` desapareceria completamente
— o que quebra `help(somar)`, ferramentas de depuração, e frameworks que
dependem de introspecção (como geradores automáticos de documentação de
API). `functools.wraps` copia esses metadados da função original para o
envelope, corrigindo esse efeito colateral.

3. Decorador que recebe argumentos próprios: mais um nível
------------------------------------------------------------------
Quando o PRÓPRIO decorador precisa de parâmetros (não a função decorada),
é necessário um nível a mais de aninhamento: uma FÁBRICA de decoradores, que
recebe os argumentos do decorador e devolve o decorador de verdade:

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

Repare na cadeia de chamadas: `repetir(3)` executa primeiro e devolve
`decorador`; `@decorador` então é aplicado sobre `ola`, exatamente como um
decorador comum de um nível só. `repetir(3)` é o que introduz o parâmetro
extra (`vezes`) que um decorador "simples" não teria como receber.

4. Guardando estado dentro de um decorador
------------------------------------------------
    def contar_chamadas(func):
        @functools.wraps(func)
        def envelope(*a, **k):
            envelope.chamadas += 1
            return func(*a, **k)
        envelope.chamadas = 0        # atributo criado NA PRÓPRIA FUNÇÃO envelope
        return envelope

Funções em Python são objetos (Dia 12) e, como todo objeto, podem receber
atributos arbitrários — aqui, `envelope.chamadas` guarda um contador que
persiste entre chamadas sucessivas da função decorada, sem precisar de uma
variável global nem de uma classe.

5. Empilhando vários decoradores na mesma função
------------------------------------------------------------
    @a
    @b
    def f(): ...
    # equivale a: f = a(b(f))  --  aplicados de BAIXO para CIMA

A ordem importa: o decorador mais PRÓXIMO da função (`@b`, escrito por
último antes do `def`) é aplicado PRIMEIRO, e o resultado dessa aplicação
é que passa pelo decorador de cima (`@a`) em seguida. Inverter a ordem dos
decoradores pode mudar o comportamento final, então vale prestar atenção
quando mais de um decorador está empilhado sobre a mesma função.

6. Ferramentas essenciais de functools
---------------------------------------------
    @lru_cache(maxsize=None)     memoização automática (funciona só com argumentos hasháveis)
    @cache                       atalho equivalente a lru_cache(maxsize=None)  [Python 3.9+]
    partial(func, arg_fixo)      cria uma nova função com um ou mais argumentos já pré-preenchidos
    reduce(func, iteravel, ini)  reduz um iterável inteiro a um único valor acumulado
    @total_ordering              a partir de __eq__ e um dos operadores (__lt__, por exemplo), gera os demais
    @singledispatch              permite "sobrecarregar" uma função com base no tipo do primeiro argumento

    @lru_cache
    def fib(n):
        return n if n < 2 else fib(n-1) + fib(n-2)
    fib(100)          # praticamente instantâneo; sem cache, seria computacionalmente inviável

`lru_cache` (least recently used cache) guarda os resultados já
calculados para cada combinação de argumentos vista antes, e devolve o
valor guardado em vez de recalcular quando os mesmos argumentos aparecem
de novo — transformando, no caso do Fibonacci recursivo, um algoritmo de
complexidade exponencial em um de complexidade linear, com uma única linha
de código adicionada.

7. Você já usou decoradores antes, mesmo sem saber como funcionavam por dentro
------------------------------------------------------------------------------------
`@property`, `@classmethod`, `@staticmethod` (Dia 17), `@dataclass` e
`@abstractmethod` (Dia 19) são todos decoradores — agora que você entende
o mecanismo geral (uma função recebendo e devolvendo outra função, ou uma
classe recebendo e devolvendo outra classe), o comportamento deles deixa de
parecer sintaxe especial arbitrária e passa a ser apenas uma aplicação
concreta do mesmo padrão. Frameworks populares seguem exatamente essa
mesma ideia: `@app.route(...)` no Flask, `@pytest.fixture` no pytest.

8. Decoradores também podem decorar classes
------------------------------------------------------
`@dataclass` é o exemplo mais visto até aqui — ele recebe uma CLASSE
inteira e devolve uma versão dela com métodos adicionais gerados. Quando o
estado interno de um decorador fica complexo o suficiente para justificar,
é possível também escrever o decorador como uma CLASSE com `__call__`
(Dia 18) implementado, em vez de uma função — uma técnica mais avançada,
útil quando o decorador precisa manter configuração ou estado elaborado
entre usos.
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
            explicacao="finally garante que a medição de tempo seja "
                       "impressa mesmo que a função decorada levante uma "
                       "exceção — a medição não depende do caminho feliz.",
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
            explicacao="Uma única linha de decorador transforma um "
                       "algoritmo exponencial em um linear, reaproveitando "
                       "cálculos já feitos em chamadas anteriores.",
        ),
        Exemplo(
            titulo="A ordem de empilhamento de decoradores importa",
            codigo='''def gritar(func):
    def envelope(*a, **k):
        return func(*a, **k).upper()
    return envelope

def exclamar(func):
    def envelope(*a, **k):
        return func(*a, **k) + "!"
    return envelope

@gritar
@exclamar
def saudacao():
    return "ola"

@exclamar
@gritar
def saudacao_invertida():
    return "ola"

print(saudacao())              # OLA!   (exclamar roda primeiro, gritar por cima)
print(saudacao_invertida())    # OLA!   (aqui tambem, mas MAIUSCULA! nao seria igual em outros casos)
''',
            explicacao="Embora o resultado final coincida neste exemplo, "
                       "em decoradores que alteram estrutura (não só texto) "
                       "a ordem de empilhamento pode mudar o resultado de fato.",
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
             "O decorador recebe a função original e o resultado dessa chamada substitui f."),
        Quiz("Para que serve functools.wraps dentro de um decorador?",
             ["Acelerar a execução da função", "Preservar __name__ e __doc__ da função original no envelope",
              "Criar um cache automaticamente", "Validar os tipos dos argumentos"], 1,
             "Sem ele, ferramentas de introspecção (help, debuggers) enxergariam apenas o envelope genérico, não a função real."),
        Quiz("Em '@a\\n@b\\ndef f(): ...', qual decorador é aplicado primeiro?",
             ["a, porque está mais acima", "b, o mais próximo da definição da função",
              "Os dois ao mesmo tempo", "Depende da ordem alfabética"], 1,
             "A aplicação ocorre de baixo para cima: f = a(b(f)) — b atua primeiro sobre f original."),
        Quiz("Por que lru_cache transforma o Fibonacci recursivo de exponencial para linear?",
             ["Porque ele reescreve o algoritmo para ser iterativo", "Porque ele evita recalcular fib(n) para o mesmo n mais de uma vez, guardando o resultado",
              "Porque ele aumenta o limite de recursão automaticamente", "lru_cache só funciona com listas, não com números"], 1,
             "Sem cache, fib(n-1) e fib(n-2) recalculam subproblemas idênticos repetidamente; o cache elimina esse desperdício."),
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
    duracao="90 min",
    objetivos=[
        "Entender exatamente o que o bloco with faz por baixo, via __enter__/__exit__",
        "Criar context managers com uma classe própria",
        "Criar context managers mais simples com @contextlib.contextmanager",
        "Suprimir e tratar exceções deliberadamente na saída de um bloco with",
        "Usar as ferramentas prontas de contextlib em vez de reimplementar padrões comuns",
        "Combinar múltiplos gerenciadores de contexto num único bloco with",
    ],
    teoria="""
1. O que o `with` realmente faz
------------------------------------
    with EXPR as var:
        corpo

é equivalente, de forma simplificada, a:

    gerenciador = EXPR
    var = gerenciador.__enter__()
    try:
        corpo
    finally:
        gerenciador.__exit__(tipo, valor, traceback)

Em outras palavras: `with` GARANTE que a "limpeza" (`__exit__`) aconteça,
não importa se o bloco terminou normalmente ou foi interrompido por uma
exceção no meio do caminho — exatamente o mesmo papel que um `finally`
manual cumpriria, mas empacotado de forma reutilizável dentro de um
objeto. Esse padrão serve para qualquer recurso que precise ser
"liberado" ao final: arquivos (Dia 14), conexões de rede, locks de
concorrência (Dia 27), transações de banco de dados, cronômetros,
diretórios temporários, e até redirecionamento temporário da saída padrão.

2. Implementando um context manager com uma classe
------------------------------------------------------------
    class Cronometro:
        def __enter__(self):
            self.inicio = time.perf_counter()
            return self                 # o valor que vai para a variável do `as`

        def __exit__(self, exc_tipo, exc_valor, tb):
            self.duracao = time.perf_counter() - self.inicio
            return False                # False = propaga a exceção adiante (não suprime)

`__enter__` é chamado ao ENTRAR no bloco `with`, e seu valor de retorno é
o que fica disponível através do `as var` (se houver). `__exit__` é
chamado ao SAIR do bloco, recebendo três informações sobre uma eventual
exceção (o tipo, o valor, e o traceback) — se nenhuma exceção ocorreu,
todos os três parâmetros chegam como `None`.

O valor de retorno de `__exit__` tem um significado especial e importante:
se ele devolver um valor "verdadeiro" (`True`, por exemplo), a exceção que
ocorreu dentro do bloco é SUPRIMIDA — como se ela nunca tivesse
acontecido, o programa simplesmente continua depois do `with` sem
propagar o erro. Isso é útil em casos deliberados e raros, mas é também um
bug clássico quando acontece por engano: um `__exit__` que devolve `True`
sem essa intenção faz erros reais desaparecerem silenciosamente, sem
nenhum aviso — um problema tão sério quanto o `except: pass` do Dia 15.

3. Implementando um context manager de forma mais simples com @contextmanager
--------------------------------------------------------------------------------------
Escrever uma classe inteira com `__enter__`/`__exit__` é verboso para casos
simples. `contextlib.contextmanager` permite escrever a mesma ideia como
uma função geradora (Dia 20), usando `yield` para separar visualmente a
parte de "entrada" da parte de "saída":

    from contextlib import contextmanager

    @contextmanager
    def transacao(conexao):
        try:
            yield conexao          # tudo ANTES do yield é o que __enter__ faria
            conexao.commit()       # tudo DEPOIS do yield (no caminho normal) é o __exit__
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()

A função decorada deve ter EXATAMENTE UM `yield` — ele é o ponto onde a
execução do bloco `with` "acontece" de fato, entre o código antes e o
código depois do `yield`. O `try/finally` ao redor do `yield` é essencial
sempre que a limpeza precisa acontecer MESMO que uma exceção seja
levantada dentro do bloco `with` — sem o `try`, uma exceção no meio do
`with` faria a função geradora simplesmente parar ali, pulando qualquer
código de limpeza que viria depois do `yield`.

4. Ferramentas prontas do módulo contextlib
--------------------------------------------------
    suppress(FileNotFoundError)      ignora silenciosamente exceções específicas listadas
    redirect_stdout(buffer)          captura tudo que seria impresso com print()
    closing(objeto)                  garante a chamada de objeto.close() ao sair do bloco
    nullcontext(valor)               um context manager que "não faz nada" — útil como valor padrão
    ExitStack()                      uma pilha DINÂMICA de gerenciadores de contexto

    from contextlib import suppress
    with suppress(FileNotFoundError):
        Path("talvez.txt").unlink()      # se o arquivo não existir, simplesmente ignora

    with ExitStack() as pilha:
        arquivos = [pilha.enter_context(open(n)) for n in nomes]   # quantidade variável, decidida em tempo de execução

`suppress` é preferível a um `try/except: pass` manual justamente porque
comunica a INTENÇÃO explicitamente: "sei que este erro específico pode
acontecer aqui, e é seguro ignorá-lo" — diferente do `except: pass` genérico
do Dia 15, que engole qualquer coisa sem distinção. `ExitStack` resolve um
problema que uma sequência fixa de `with`s não resolve: quando o NÚMERO de
recursos a gerenciar só é conhecido em tempo de execução (por exemplo, uma
lista de nomes de arquivo vinda de uma variável), não há como escrever um
`with a, b, c:` fixo — `ExitStack` permite adicionar gerenciadores
dinamicamente, um por um, garantindo que todos sejam fechados corretamente
ao final, na ordem inversa em que foram abertos.

5. Vários gerenciadores de contexto em um único bloco
------------------------------------------------------------
    with open("a") as fa, open("b", "w") as fb:
        fb.write(fa.read())

Separar por vírgula abre e (ao sair) fecha ambos os recursos, na ordem
correta — o segundo é fechado antes do primeiro, seguindo a mesma lógica
de "o que abriu por último, fecha primeiro" que vimos em pilhas (Dia 8).
Desde o Python 3.10, é possível envolver a lista inteira em parênteses
para quebrar em várias linhas, o que ajuda a legibilidade quando há muitos
recursos:

    with (
        open("a") as fa,
        open("b") as fb,
    ):
        ...

6. Casos práticos que você provavelmente vai usar em breve
------------------------------------------------------------------
    tempfile.TemporaryDirectory()    cria uma pasta temporária que se apaga sozinha ao sair do with
    threading.Lock()                 protege uma seção crítica em código concorrente (Dia 27)
    unittest.mock.patch()            substitui temporariamente algo durante um teste automatizado (Dia 24)
    decimal.localcontext()           ajusta a precisão de cálculos com Decimal apenas dentro do bloco

Esses exemplos ilustram o padrão geral: qualquer situação onde algo
precisa ser "montado" no início e "desmontado" garantidamente no final —
mesmo que algo dê errado no meio — é candidata natural a um context
manager, seja escrito por você ou já pronto na biblioteca padrão.
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
            explicacao="Devolver self em __enter__ permite consultar dados "
                       "do cronômetro (como c.duracao) depois que o bloco "
                       "with já terminou, através da variável do 'as'.",
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
        temporario.replace(destino)     # só troca se tudo correu bem ate aqui
    except BaseException:
        arquivo.close()
        temporario.unlink(missing_ok=True)
        raise

with escrita_atomica("/tmp/config.txt") as f:
    f.write("tema=escuro\\n")
print(Path("/tmp/config.txt").read_text())
''',
            explicacao="Retoma a técnica de escrita segura do Dia 14, "
                       "agora encapsulada num context manager reutilizável "
                       "— o arquivo final nunca fica corrompido pela metade.",
        ),
        Exemplo(
            titulo="__exit__ devolvendo True suprime a exceção (com cuidado!)",
            codigo='''class IgnorarDivisaoPorZero:
    def __enter__(self):
        return self
    def __exit__(self, tipo, valor, tb):
        if tipo is ZeroDivisionError:
            print("dividir por zero, seguindo em frente")
            return True     # suprime SOMENTE esta excecao especifica
        return False        # qualquer outra excecao continua propagando normalmente

with IgnorarDivisaoPorZero():
    resultado = 10 / 0
    print("esta linha nunca roda")

print("o programa continua normalmente aqui")
''',
            explicacao="Suprimir só o tipo específico esperado (aqui, "
                       "ZeroDivisionError) e devolver False para qualquer "
                       "outro caso evita esconder erros inesperados.",
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
             ["Nada muda", "A exceção que ocorreu dentro do with é suprimida", "O bloco with reinicia do começo", "Sempre gera um erro"], 1,
             "Devolver True engole a exceção — só faça isso deliberadamente, filtrando o tipo específico esperado."),
        Quiz("Quantos yields uma função decorada com @contextmanager deve ter?",
             ["Zero", "Exatamente um", "Dois, um para entrada e outro para saída", "Quantos quiser"], 1,
             "O código antes do yield equivale a __enter__; o código depois equivale a __exit__."),
        Quiz("Por que contextlib.suppress é preferível a um try/except: pass manual?",
             ["Não há diferença nenhuma entre os dois", "suppress comunica explicitamente qual exceção específica é esperada e segura de ignorar",
              "suppress é mais rápido de executar", "except: pass não é sintaxe válida em Python"], 1,
             "suppress(TipoEspecifico) documenta a intenção; except: pass genérico esconde qualquer erro, mesmo os inesperados."),
        Quiz("Quando ExitStack é mais apropriado que uma sequência fixa de with a, b, c?",
             ["Sempre, ExitStack deveria substituir todo with comum", "Quando o número de recursos a gerenciar só é conhecido em tempo de execução",
              "Nunca, é um recurso obsoleto", "Apenas para arquivos, não para outros recursos"], 1,
             "ExitStack permite adicionar gerenciadores de contexto dinamicamente, um a um, quando a quantidade não é fixa no código."),
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
    duracao="90 min",
    objetivos=[
        "Anotar funções, variáveis e classes, entendendo que isso não muda a execução",
        "Usar a sintaxe moderna de tipos (list[str], X | None) em vez da antiga do módulo typing",
        "Anotar parâmetros e retornos com Callable, e criar aliases de tipo",
        "Escrever funções e classes genéricas com TypeVar/Generic",
        "Usar Protocol para expressar duck typing de forma verificável por ferramentas",
        "Verificar tipos estaticamente com mypy e entender o que ele pega que o Python não pega sozinho",
    ],
    teoria="""
1. Anotações de tipo não mudam absolutamente nada na execução
------------------------------------------------------------------------
    def somar(a: int, b: int) -> int:
        return a + b

    somar("x", "y")     # roda NORMALMENTE! Python NÃO valida tipos em tempo de execução

Este é o ponto mais importante e mais mal compreendido sobre type hints em
Python: eles são puramente INFORMATIVOS para quem lê o código e para
ferramentas externas — o interpretador Python, ao rodar o programa,
simplesmente IGNORA as anotações de tipo, exatamente como ignora
comentários. `somar("x", "y")` de fato concatena as duas strings (`"xy"`),
sem erro nenhum, apesar da anotação dizer `int`.

O ganho real de anotar tipos está em outro lugar: legibilidade (a
assinatura já documenta o contrato esperado, sem precisar de comentário
separado), autocompletar mais preciso em editores e IDEs, e — o mais
valioso — a possibilidade de rodar uma ferramenta de análise ESTÁTICA
(como `mypy` ou `pyright`) que detecta incompatibilidades de tipo ANTES de
o programa rodar, sem executar uma linha sequer.

2. Sintaxe moderna (Python 3.9+ e 3.10+)
--------------------------------------------
    nomes: list[str] = []
    notas: dict[str, float] = {}
    par: tuple[int, str] = (1, "a")
    varios: tuple[int, ...] = (1, 2, 3)         # tupla de tamanho variável, todos int
    talvez: str | None = None            # substitui o antigo Optional[str]
    numero: int | float = 0              # substitui o antigo Union[int, float]

Antes do Python 3.9, era necessário importar `List`, `Dict`, `Tuple` do
módulo `typing` para anotar coleções (`List[str]` em vez de `list[str]`).
Hoje, com Python 3.9 ou mais recente, os próprios tipos embutidos
(`list`, `dict`, `tuple`) já aceitam a sintaxe de colchetes diretamente,
tornando essas importações desnecessárias na maioria dos casos. O operador
`|` (Python 3.10+) para "ou" também substitui `Optional`/`Union` na
maioria dos usos cotidianos, sendo mais curto e mais legível.

3. Callable, Any e aliases de tipo
----------------------------------------
    from typing import Callable, Any, Iterable, Iterator, Sequence

    def aplicar(f: Callable[[int, int], int], a: int, b: int) -> int:
        return f(a, b)

    Matriz = list[list[float]]                # um ALIAS: um nome mais legível para um tipo composto
    def processar(dados: Iterable[str]) -> Iterator[str]: ...

`Callable[[int, int], int]` descreve "uma função que recebe dois `int` e
devolve um `int`" — útil para anotar parâmetros que são, eles próprios,
funções (retomando as funções de alta ordem do Dia 12).

Uma boa prática de anotação, seguida por bibliotecas profissionais, é
preferir o tipo mais ABSTRATO possível nos PARÂMETROS de uma função
(`Iterable`, `Sequence`, `Mapping` — que aceitam qualquer implementação
compatível) e o tipo mais CONCRETO possível no RETORNO (`list`, `dict` — que
dizem exatamente o que quem recebe o valor pode esperar). Isso maximiza a
flexibilidade de quem chama a função, sem sacrificar clareza sobre o que
ela devolve.

4. Genéricos: funções e classes que funcionam com qualquer tipo
------------------------------------------------------------------------
    from typing import TypeVar, Generic
    T = TypeVar("T")

    class Caixa(Generic[T]):
        def __init__(self, item: T) -> None:
            self.item = item
        def pegar(self) -> T:
            return self.item

    def primeiro(seq: Sequence[T]) -> T | None:
        return seq[0] if seq else None

`TypeVar` declara uma "variável de tipo" — um espaço reservado que
representa "qualquer tipo, mas SEMPRE o mesmo tipo dentro desta mesma
chamada". Isso permite que uma ferramenta como mypy verifique, por
exemplo, que `primeiro([1, 2, 3])` devolve um `int | None`, mas
`primeiro(["a", "b"])` devolve um `str | None` — o tipo de retorno
"acompanha" o tipo de entrada, sem precisar escrever uma função separada
para cada tipo possível.

A partir do Python 3.12, existe uma sintaxe mais enxuta e nativa para
isso, dispensando a declaração explícita de `TypeVar`:
`def primeiro[T](seq: Sequence[T]) -> T | None:` — o `[T]` logo após o
nome da função já declara a variável de tipo inline.

5. Protocol: duck typing que ferramentas conseguem verificar
------------------------------------------------------------------
    from typing import Protocol

    class TemArea(Protocol):
        def area(self) -> float: ...

    def maior(formas: list[TemArea]) -> TemArea:
        return max(formas, key=lambda f: f.area())

Retomando o duck typing do Dia 18 ("o que importa é o objeto TER o
método, não herdar de uma classe específica"), `Protocol` formaliza essa
ideia de um jeito que ferramentas de checagem estática também conseguem
entender: qualquer classe que tenha um método `area() -> float`,
INDEPENDENTE de herdar de `TemArea` ou não, é considerada compatível com o
protocolo. Isso combina a flexibilidade do duck typing dinâmico de Python
com a segurança de checagem estática — o melhor dos dois mundos, sem
forçar uma hierarquia de herança artificial só para satisfazer o
verificador de tipos.

6. TypedDict e Literal: tipando dicionários e valores fixos
------------------------------------------------------------------
    from typing import TypedDict, Literal, Final

    class Usuario(TypedDict):
        nome: str
        idade: int

    Nivel = Literal["debug", "info", "erro"]     # só aceita EXATAMENTE uma dessas três strings
    VERSAO: Final = "1.0"                          # sinaliza que este valor não deve ser reatribuído

`TypedDict` permite anotar a FORMA esperada de um dicionário comum (quais
chaves existem e o tipo de cada uma), útil quando você trabalha com dados
vindos de JSON ou APIs externas, mas ainda quer os benefícios de checagem
estática sem converter tudo para uma classe de verdade. `Literal` restringe
um valor a um conjunto fixo e específico de opções literais (mais
granular que apenas dizer "é uma string qualquer").

7. mypy na prática: checagem estática de tipos
----------------------------------------------------
    pip install mypy
    mypy meu_arquivo.py
    mypy --strict pacote/

`mypy` lê seu código anotado e aponta incompatibilidades de tipo SEM
executar o programa — por exemplo, ele acusaria a chamada
`somar("x", "y")` do início desta lição como um erro, mesmo que o Python
em si a execute sem problema nenhum. A recomendação prática para adotar
mypy num projeto existente é começar SEM a flag `--strict` (que exige
anotação em absolutamente tudo), anotar primeiro as funções públicas mais
importantes, e ir apertando o rigor aos poucos. Quando um caso pontual
precisa ser ignorado deliberadamente, `# type: ignore[codigo_do_erro]` na
linha específica silencia aquele aviso sem desativar a checagem do resto
do arquivo.

Em tempo de EXECUÇÃO (não apenas estático), a função
`typing.get_type_hints(func)` devolve as anotações já resolvidas de uma
função — é exatamente esse mecanismo de introspecção que bibliotecas como
Pydantic e FastAPI usam por baixo dos panos para gerar validação de dados
e documentação de API automaticamente a partir das suas anotações de tipo.
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
            explicacao="A assinatura de aprovados já explica sozinha o "
                       "contrato esperado (uma coleção de Aluno, um corte "
                       "numérico opcional, devolve nomes) sem exigir comentário.",
        ),
        Exemplo(
            titulo="Protocol em ação: duck typing verificável",
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
            explicacao="Pedido não herda de Serializavel em nenhum momento, "
                       "mas satisfaz o protocolo por ter o método esperado "
                       "com a assinatura certa — mypy aceitaria isso normalmente.",
        ),
        Exemplo(
            titulo="O que mypy pegaria, e o Python não pega sozinho",
            codigo='''def dobrar(x: int) -> int:
    return x * 2

resultado_bom = dobrar(21)          # ok, 42
resultado_ruim = dobrar("21")       # Python roda isso! devolve '2121', nao um erro

print(resultado_bom, resultado_ruim)
# rodando "mypy este_arquivo.py", a segunda chamada seria sinalizada como
# incompativel: Argument 1 to "dobrar" has incompatible type "str"; expected "int"
''',
            explicacao="Sem mypy, o erro de tipo só apareceria (talvez) "
                       "muito depois, quando algo tentasse tratar "
                       "resultado_ruim como um número de verdade.",
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
        Quiz("O que acontece se você passar o tipo errado numa função anotada, ao rodar o programa normalmente?",
             ["TypeError é levantado na hora", "Nada acontece em tempo de execução; só ferramentas estáticas (mypy, pyright) acusam o problema",
              "O valor é convertido automaticamente para o tipo certo", "O programa se recusa a iniciar"], 1,
             "Anotações são metadados: o Python não valida tipos sozinho ao executar o código."),
        Quiz("Como escrever 'string ou None' usando a sintaxe moderna do Python 3.10+?",
             ["str|None", "Optional(str)", "str?", "Maybe[str]"], 0,
             "O operador | substitui Optional/Union na maioria dos usos cotidianos."),
        Quiz("Qual a vantagem de Protocol sobre exigir herança de uma classe base comum?",
             ["Protocol é mais rápido em tempo de execução", "Permite checagem estática de duck typing sem forçar uma hierarquia de herança artificial",
              "Protocol impede qualquer tipo de erro", "Não há vantagem real, é só sintaxe alternativa"], 1,
             "Uma classe satisfaz o Protocol só por ter os métodos certos, sem precisar herdar dele explicitamente."),
        Quiz("Por que é uma boa prática usar tipos mais abstratos (Iterable, Sequence) nos parâmetros e mais concretos (list, dict) no retorno?",
             ["É apenas uma convenção estética sem efeito prático", "Maximiza a flexibilidade de quem chama a função, sem sacrificar clareza sobre o que ela devolve",
              "Tipos abstratos são mais rápidos de processar", "É uma exigência obrigatória do mypy"], 1,
             "Aceitar qualquer Iterable dá mais liberdade a quem chama; devolver um list concreto deixa claro o que o chamador recebe de volta."),
    ],
    projeto=(
        "Pegue um dos seus projetos anteriores, anote todas as funções e classes, "
        "rode mypy --strict e corrija até zerar os avisos."
    ),
    leitura=["docs.python.org/pt-br/3/library/typing.html", "PEP 484", "PEP 604"],
))
