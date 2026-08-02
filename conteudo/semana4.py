"""Semana 4 - Dias 24 a 30: testes, sistema, concorrência, performance e projeto final."""

from nucleo.modelos import Dia, Exemplo, Exercicio, Quiz

DIAS = []

# ---------------------------------------------------------------- DIA 24
DIAS.append(Dia(
    numero=24,
    titulo="Testes automatizados: unittest, pytest e TDD",
    nivel="Avançado",
    duracao="120 min",
    objetivos=[
        "Entender por que testes automatizados existem e o custo real de não tê-los",
        "Escrever testes com unittest usando TestCase, métodos de asserção e fixtures",
        "Usar subTest para testar múltiplos casos sem parar no primeiro erro",
        "Conhecer pytest e por que ele é preferido ao unittest em projetos modernos",
        "Aplicar o ciclo TDD: Red -> Green -> Refactor com um exemplo real",
        "Usar mocks para isolar dependências externas nos testes",
    ],
    teoria="""
Você já sabe escrever código que funciona. Mas como você TEM CERTEZA
de que ele funciona? E como sabe que continua funcionando depois de
uma mudança? A resposta são os testes automatizados.

---------------------------------------------------------------------------
1. Por que testar? O custo real de não testar
---------------------------------------------------------------------------
Sem testes automatizados, verificar que o código funciona exige rodar
o programa manualmente e checar os resultados visualmente. Isso significa:

    - Cada mudança exige verificação manual (lenta e propensa a erro)
    - Bugs em partes "não tocadas" são descobertos tarde ou pelo usuário
    - Refatorar código se torna arriscado: "e se eu quebrar algo?"
    - Integrar código de outra pessoa vira uma aposta

COM TESTES AUTOMATIZADOS:
    - Bugs são detectados em segundos, não em horas
    - Refatoração é segura: se os testes passam, o comportamento não mudou
    - Testes são documentação viva: mostram COMO o código deve se comportar
    - Integração contínua (CI) executa testes automaticamente a cada commit

A PIRÂMIDE DE TESTES:

    Topo (poucos):    Testes E2E — testam o sistema inteiro do início ao fim
    Meio:             Testes de integração — testam componentes juntos
    Base (muitos):    Testes unitários — testam uma função ou classe isolada

Testes unitários são a base: rápidos, baratos, isolados, fáceis de
escrever. O foco deste dia é neles.

---------------------------------------------------------------------------
2. unittest: o framework padrão da biblioteca
---------------------------------------------------------------------------
unittest é o framework de testes que vem com Python (inspirado no JUnit
do Java). Você cria classes que herdam de unittest.TestCase:

    import unittest

    def somar(a, b):
        return a + b

    class TestSomar(unittest.TestCase):

        def test_positivos(self):
            self.assertEqual(somar(2, 3), 5)

        def test_negativos(self):
            self.assertEqual(somar(-1, -2), -3)

        def test_zero(self):
            self.assertEqual(somar(0, 5), 5)

    if __name__ == "__main__":
        unittest.main()

CONVENCOES DO UNITTEST:
    - A classe deve herdar de unittest.TestCase
    - Metodos de teste DEVEM comecar com test_
    - Metodos que nao comecam com test_ nao sao executados como testes
    - Cada metodo deve testar UMA coisa (uma asserção principal)

EXECUTANDO:

    python -m unittest arquivo.py
    python -m unittest discover tests/

---------------------------------------------------------------------------
3. Métodos de asserção: mais informativos que assert simples
---------------------------------------------------------------------------
TestCase oferece métodos que produzem mensagens de erro muito mais
detalhadas do que um assert simples:

    Metodo                          O que verifica
    ----------------------------    ----------------------------------------
    assertEqual(a, b)               a == b
    assertNotEqual(a, b)            a != b
    assertTrue(expr)                bool(expr) e True
    assertFalse(expr)               bool(expr) e False
    assertIsNone(x)                 x is None
    assertIsNotNone(x)              x is not None
    assertIn(item, container)       item in container
    assertRaises(Exc, func, *args)  func(*args) levanta Exc
    assertAlmostEqual(a, b)         abs(a-b) <= 7 casas decimais
    assertGreater(a, b)             a > b
    assertIsInstance(obj, cls)      isinstance(obj, cls)

Por que usar assertEqual em vez de assert a == b?

    assert a == b            # falha: AssertionError (sem detalhes)
    self.assertEqual(a, b)   # falha: AssertionError: 5 != 3  <- mostra valores!

A mensagem informativa acelera muito a depuração.

---------------------------------------------------------------------------
4. Fixtures: setUp e tearDown
---------------------------------------------------------------------------
Fixtures são código que prepara o ambiente antes de cada teste e limpa
depois. Sem fixtures, você repetiria a inicialização em cada test_:

    class TestConta(unittest.TestCase):

        def setUp(self):
            \"\"\"Executado ANTES de cada metodo test_.\"\"\"
            self.conta = ContaBancaria("Ana", 1000.0)

        def tearDown(self):
            \"\"\"Executado DEPOIS de cada test_, mesmo se falhou.\"\"\"
            pass   # limpar arquivos, fechar conexoes...

        @classmethod
        def setUpClass(cls):
            \"\"\"Executado UMA VEZ antes de TODOS os testes da classe.\"\"\"
            cls.conexao = conectar_banco()

        @classmethod
        def tearDownClass(cls):
            \"\"\"Executado UMA VEZ depois de TODOS os testes da classe.\"\"\"
            cls.conexao.fechar()

        def test_deposito(self):
            self.conta.depositar(500)
            self.assertEqual(self.conta.saldo, 1500)

        def test_saque(self):
            self.conta.sacar(200)
            self.assertEqual(self.conta.saldo, 800)

setUp garante que cada teste começa com estado limpo e INDEPENDENTE.
Sem setUp, um teste poderia influenciar o resultado de outro (bug de
ordem de execução — muito difícil de depurar).

---------------------------------------------------------------------------
5. subTest: testando múltiplos casos sem parar no primeiro erro
---------------------------------------------------------------------------
Quando você tem vários casos de teste para a mesma função, usar um loop
com subTest é muito melhor do que múltiplos métodos iguais:

    class TestEhPrimo(unittest.TestCase):

        def test_numeros_primos(self):
            primos = [2, 3, 5, 7, 11, 13, 17, 19]
            for n in primos:
                with self.subTest(n=n):      # identifica qual falhou!
                    self.assertTrue(eh_primo(n))

        def test_nao_primos(self):
            nao_primos = [0, 1, 4, 6, 8, 9, 15]
            for n in nao_primos:
                with self.subTest(n=n):
                    self.assertFalse(eh_primo(n))

Sem subTest, um loop de asserções para no PRIMEIRO que falha e você
não sabe se os outros também falhariam. Com subTest, Python continua
e mostra TODOS os casos que falharam de uma vez.

---------------------------------------------------------------------------
6. Testando exceções
---------------------------------------------------------------------------
Duas formas de verificar que uma função levanta a exceção correta:

    # Forma preferida: assertRaises como context manager
    def test_divisao_por_zero(self):
        with self.assertRaises(ZeroDivisionError):
            dividir(10, 0)

    # Verificando também a mensagem da exceção
    def test_mensagem_de_erro(self):
        with self.assertRaises(ValueError) as ctx:
            sacar(-100)
        self.assertIn("negativo", str(ctx.exception))

    # Forma alternativa (menos comum)
    def test_forma_alternativa(self):
        self.assertRaises(ZeroDivisionError, dividir, 10, 0)

---------------------------------------------------------------------------
7. pytest: o framework moderno
---------------------------------------------------------------------------
pytest é o framework mais popular para Python moderno. Mais simples que
unittest e com recursos muito mais poderosos.

INSTALACAO:

    pip install pytest

VANTAGEM PRINCIPAL: use assert normal, pytest mostra erro detalhado:

    # unittest (verboso)
    self.assertEqual(resultado, 42)

    # pytest (simples e igualmente informativo)
    assert resultado == 42
    # Falha mostra: assert 5 == 42 (valores reais!)

ESTRUTURA DE UM ARQUIVO PYTEST:

    # test_calculos.py
    import pytest

    def test_somar():
        assert somar(2, 3) == 5

    def test_divisao_zero():
        with pytest.raises(ZeroDivisionError):
            1 / 0

EXECUTANDO:

    pytest                    # descobre e roda todos os test_*.py
    pytest -v                 # verbose: nome de cada teste
    pytest -k "primo"         # so testes com "primo" no nome
    pytest --tb=short         # traceback resumido

FIXTURES DO PYTEST:

    import pytest

    @pytest.fixture
    def conta():
        return ContaBancaria("Ana", 1000.0)   # nova para cada teste

    def test_deposito(conta):     # pytest injeta automaticamente!
        conta.depositar(500)
        assert conta.saldo == 1500

PARAMETRIZE: o equivalente ao subTest, mas mais elegante:

    @pytest.mark.parametrize("entrada, esperado", [
        (2,   True),
        (3,   True),
        (4,   False),
        (7,   True),
        (100, False),
    ])
    def test_eh_primo(entrada, esperado):
        assert eh_primo(entrada) == esperado

---------------------------------------------------------------------------
8. TDD: Test-Driven Development
---------------------------------------------------------------------------
TDD é uma metodologia onde você escreve o TESTE ANTES do código:

    CICLO RED -> GREEN -> REFACTOR:

    1. RED:      Escreva um teste que FALHA (o codigo nao existe ainda)
    2. GREEN:    Escreva o MINIMO de codigo para o teste passar
    3. REFACTOR: Melhore o codigo mantendo os testes passando
    4. Repita para o proximo comportamento

EXEMPLO PRATICO — desenvolvendo slug():

    # PASSO 1 (RED): teste escrito, slug nao existe
    def test_slug_basico():
        assert slug("Ola Mundo") == "ola-mundo"
    # Falha: NameError: slug nao definido

    # PASSO 2 (GREEN): codigo minimo para passar
    def slug(texto):
        return "-".join(texto.lower().split())
    # Passa!

    # PASSO 3 (REFACTOR/EXPANDIR): novo caso de teste
    def test_slug_espacos_extras():
        assert slug("  Python   Puro  ") == "python-puro"
    # split() sem args ja lida com multiplos espacos -> passa!

BENEFICIOS DO TDD:
    - Voce pensa na INTERFACE antes da implementacao
    - O codigo tem alta cobertura desde o inicio
    - Design emergente: codigo testavel tende a ser bem estruturado
    - Os testes sao a documentacao mais atualizada do comportamento

---------------------------------------------------------------------------
9. Mocks: isolando dependências externas
---------------------------------------------------------------------------
Testes unitários devem ser ISOLADOS: sem banco de dados, rede, relógio
ou sistema de arquivos. Mocks simulam essas dependências:

    from unittest.mock import Mock, patch

    # Mock basico
    servico = Mock()
    servico.buscar.return_value = {"nome": "Ana"}
    resultado = servico.buscar(42)
    print(resultado)              # {'nome': 'Ana'}
    servico.buscar.assert_called_once_with(42)   # verifica a chamada!

    # patch: substitui objeto real por mock durante o teste
    def test_enviar_email():
        with patch("modulo.enviar_email") as mock_email:
            processar_pedido(pedido)
            mock_email.assert_called_once_with("cliente@email.com", "OK")

    # patch como decorador
    @patch("modulo.requests.get")
    def test_buscar_usuario(mock_get):
        mock_get.return_value.json.return_value = {"nome": "Ana"}
        usuario = buscar_usuario(1)
        assert usuario["nome"] == "Ana"
""",
    exemplos=[
        Exemplo(
            titulo="Suite completa com unittest e subTest",
            codigo='''import unittest

def eh_primo(n):
    """Verifica se n e um numero primo."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def slug(texto):
    """Converte texto para formato URL-amigavel."""
    return "-".join(texto.lower().split())

class TestEhPrimo(unittest.TestCase):

    def test_primos_conhecidos(self):
        primos = [2, 3, 5, 7, 11, 13, 17, 19, 23]
        for p in primos:
            with self.subTest(n=p):     # identifica qual falhou!
                self.assertTrue(eh_primo(p))

    def test_nao_primos(self):
        nao_primos = [0, 1, 4, 6, 8, 9, 10, 15, 25]
        for n in nao_primos:
            with self.subTest(n=n):
                self.assertFalse(eh_primo(n))

    def test_primo_grande(self):
        self.assertTrue(eh_primo(7919))    # o 1000o primo

class TestSlug(unittest.TestCase):

    def setUp(self):
        self.casos = [
            ("Ola Mundo",          "ola-mundo"),
            ("  Python   Puro  ",  "python-puro"),
            ("UM",                 "um"),
        ]

    def test_conversao(self):
        for entrada, esperado in self.casos:
            with self.subTest(entrada=entrada):
                self.assertEqual(slug(entrada), esperado)

    def test_string_vazia(self):
        self.assertEqual(slug(""), "")

# Rodando a suite
suite = unittest.TestLoader().loadTestsFromModule(__import__("__main__"))
runner = unittest.TextTestRunner(verbosity=2)
resultado = runner.run(suite)
''',
            explicacao="subTest() permite rodar o mesmo teste com múltiplos "
                       "valores e mostrar QUAL valor falhou, em vez de parar "
                       "no primeiro. Sem subTest, um loop de asserções para no "
                       "primeiro falso e você não descobre os outros problemas. "
                       "setUp garante que self.casos é recriado para cada teste — "
                       "independência entre testes é fundamental.",
        ),
        Exemplo(
            titulo="TDD na pratica: desenvolvendo soma_digitos",
            codigo='''import unittest

# TDD: os testes vem ANTES do codigo

class TestSomaDigitos(unittest.TestCase):
    """Desenvolvemos soma_digitos usando o ciclo RED->GREEN->REFACTOR."""

    # PASSO 1 (RED): testes escritos — todos falham porque a funcao nao existe

    def test_digito_unico(self):
        self.assertEqual(soma_digitos(5), 5)

    def test_numero_positivo(self):
        self.assertEqual(soma_digitos(123), 6)    # 1+2+3

    def test_zero(self):
        self.assertEqual(soma_digitos(0), 0)

    def test_numero_grande(self):
        self.assertEqual(soma_digitos(9999), 36)  # 9+9+9+9

    def test_retorna_inteiro(self):
        self.assertIsInstance(soma_digitos(42), int)


# PASSO 2 (GREEN): implementacao minima para todos os testes passarem
def soma_digitos(n):
    """Soma os digitos de um numero inteiro nao negativo."""
    return sum(int(d) for d in str(n))


# PASSO 3 (REFACTOR): testes ainda passam? Podemos melhorar o codigo?
# A implementacao com str() e simples e clara.
# Alternativa matematica: while n > 0: soma += n % 10; n //= 10
# Os testes garantem que qualquer alternativa e equivalente.

suite = unittest.TestLoader().loadTestsFromTestCase(TestSomaDigitos)
resultado = unittest.TextTestRunner(verbosity=0).run(suite)
print(f"Testes: {resultado.testsRun} | Falhas: {len(resultado.failures)}")
''',
            explicacao="O TDD força você a pensar nos casos de teste ANTES "
                       "de escrever o código. Resultado: cobertura completa "
                       "desde o início, e a implementação emerge para "
                       "satisfazer os testes — não o contrário. "
                       "Note que test_retorna_inteiro verifica o TIPO, "
                       "não apenas o valor — útil quando a função poderia "
                       "retornar float acidentalmente.",
        ),
        Exemplo(
            titulo="Testando excecoes e usando mocks",
            codigo='''import unittest
from unittest.mock import Mock

def dividir(a, b):
    if b == 0:
        raise ValueError("divisao por zero nao permitida")
    return a / b

def buscar_preco(produto_id, servico):
    """Busca preco usando um servico externo."""
    resposta = servico.buscar(produto_id)
    if resposta is None:
        raise ValueError(f"Produto {produto_id} nao encontrado")
    return float(resposta["preco"])

class TestDividir(unittest.TestCase):

    def test_divisao_normal(self):
        self.assertEqual(dividir(10, 2), 5.0)

    def test_divisao_por_zero(self):
        with self.assertRaises(ValueError) as ctx:
            dividir(10, 0)
        self.assertIn("zero", str(ctx.exception).lower())

    def test_divisao_negativa(self):
        self.assertAlmostEqual(dividir(-6, 4), -1.5)

class TestBuscarPreco(unittest.TestCase):

    def test_produto_encontrado(self):
        # Mock do servico externo: nao faz requisicao real!
        servico_mock = Mock()
        servico_mock.buscar.return_value = {"preco": "29.90"}

        preco = buscar_preco(42, servico_mock)

        self.assertEqual(preco, 29.90)
        servico_mock.buscar.assert_called_once_with(42)   # verificou a chamada!

    def test_produto_nao_encontrado(self):
        servico_mock = Mock()
        servico_mock.buscar.return_value = None

        with self.assertRaises(ValueError):
            buscar_preco(999, servico_mock)

suite = unittest.TestLoader().loadTestsFromModule(__import__("__main__"))
resultado = unittest.TextTestRunner(verbosity=0).run(suite)
print(f"OK: {resultado.wasSuccessful()}")
''',
            explicacao="assertRaises como context manager captura a exceção "
                       "e permite verificar a mensagem com ctx.exception. "
                       "Mock() cria um objeto que registra todas as chamadas. "
                       "assert_called_once_with verifica não só SE foi chamado, "
                       "mas COM QUAIS ARGUMENTOS — essencial para garantir "
                       "que a integração com o serviço externo está correta "
                       "sem fazer chamadas reais.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d24e1",
            enunciado=(
                "Escreva a funcao slug(texto) que converte texto para\n"
                "formato URL-amigavel:\n"
                "   - Converte para minusculas\n"
                "   - Remove espacos das pontas e extras entre palavras\n"
                "   - Junta palavras com hifens\n\n"
                "Exemplos:\n"
                "   slug('Ola Mundo')         -> 'ola-mundo'\n"
                "   slug('  Python   Puro  ') -> 'python-puro'\n"
                "   slug('')                  -> ''\n"
                "   slug('UM')               -> 'um'\n\n"
                "Dica: .split() sem argumentos ja faz tudo:\n"
                "   - Remove espacos das pontas automaticamente\n"
                "   - Divide por qualquer quantidade de espacos\n"
                "   - Retorna lista vazia para string vazia\n\n"
                "Entao: '-'.join('  Python   Puro  '.lower().split())\n"
                "   = '-'.join(['python', 'puro'])\n"
                "   = 'python-puro'"
            ),
            funcao="slug",
            assinatura="def slug(texto):",
            testes=[
                ("slug('Ola Mundo')", "'ola-mundo'"),
                ("slug('  Python   Puro  ')", "'python-puro'"),
                ("slug('')", "''"),
                ("slug('UM')", "'um'"),
            ],
            dica="return '-'.join(texto.lower().split())",
        ),
        Exercicio(
            id="d24e2",
            enunciado=(
                "Os imports e a estrutura ja estao na assinatura.\n"
                "Complete duas funcoes:\n\n"
                "1. eh_primo(n) -> bool:\n"
                "   - False se n < 2\n"
                "   - True se n == 2\n"
                "   - False se n par (n % 2 == 0)\n"
                "   - Verifica divisores impares de 3 ate sqrt(n)\n\n"
                "2. rodar_testes() -> int:\n"
                "   Cria e executa uma suite unittest que testa eh_primo.\n"
                "   Deve conter PELO MENOS 1 teste.\n"
                "   Retorna o numero de testes executados.\n\n"
                "Exemplos:\n"
                "   eh_primo(7919) -> True   (7919 e o 1000o primo)\n"
                "   eh_primo(1)    -> False\n"
                "   eh_primo(9)    -> False  (9 = 3 x 3)\n"
                "   rodar_testes() >= 1 -> True\n\n"
                "Estrutura de rodar_testes:\n"
                "   class MeusTestes(unittest.TestCase):\n"
                "       def test_primo(self):\n"
                "           self.assertTrue(eh_primo(7))\n"
                "   suite = unittest.TestLoader().loadTestsFromTestCase(MeusTestes)\n"
                "   resultado = unittest.TextTestRunner(verbosity=0).run(suite)\n"
                "   return resultado.testsRun\n\n"
                "verbosity=0 suprime a saida para nao poluir o corretor."
            ),
            funcao="rodar_testes",
            assinatura="import unittest\n\n\ndef eh_primo(n):\n    ...\n\n\ndef rodar_testes():",
            testes=[
                ("eh_primo(7919)", "True"),
                ("eh_primo(1)", "False"),
                ("eh_primo(9)", "False"),
                ("rodar_testes() >= 1", "True"),
            ],
            nivel="dificil",
            dica="eh_primo: if n<2: False; if n==2: True; if n%2==0: False; for i in range(3,int(n**0.5)+1,2): if n%i==0: False; True. rodar_testes: crie TestCase com test_, carregue suite, TextTestRunner(verbosity=0).run(suite), return .testsRun",
        ),
        Exercicio(
            id="d24e3",
            enunciado=(
                "Escreva dividir(a, b) que divide a por b.\n"
                "Se b for zero, levanta ValueError.\n\n"
                "Exemplos:\n"
                "   dividir(10, 4)  -> 2.5\n"
                "   dividir(1, 0)   -> raise ValueError\n"
                "   dividir(-6, 3)  -> -2.0\n\n"
                "Use clausula de guarda:\n"
                "   if b == 0:\n"
                "       raise ValueError('divisao por zero')\n"
                "   return a / b\n\n"
                "O operador / sempre retorna float:\n"
                "   10 / 4 = 2.5   (nao 2)\n"
                "   -6 / 3 = -2.0  (nao -2)\n\n"
                "O teste '!raise ValueError' verifica que a excecao\n"
                "e levantada — a mensagem pode ser qualquer texto."
            ),
            funcao="dividir",
            assinatura="def dividir(a, b):",
            testes=[
                ("dividir(10, 4)", "2.5"),
                ("dividir(1, 0)", "!raise ValueError"),
                ("dividir(-6, 3)", "-2.0"),
            ],
            nivel="medio",
            dica="if b == 0: raise ValueError('divisao por zero'). return a / b",
        ),
    ],
    quiz=[
        Quiz(
            "Por que os metodos de TestCase (assertEqual, assertRaises) sao preferidos ao assert simples?",
            ["Sao mais rapidos de executar",
             "Produzem mensagens de erro muito mais informativas, mostrando os valores reais que falharam",
             "assert simples nao funciona dentro de classes TestCase",
             "Os metodos de TestCase checam o tipo alem do valor"],
            1,
            "assert a == b falha com 'AssertionError' sem detalhes. "
            "self.assertEqual(a, b) falha com 'AssertionError: 5 != 3' "
            "mostrando os valores reais — muito mais facil de depurar. "
            "A informatividade e a principal razao para usar os metodos do TestCase.",
        ),
        Quiz(
            "Qual a vantagem de subTest sobre um loop simples de asserções?",
            ["subTest e mais rapido que um loop",
             "Com subTest, todos os casos sao testados mesmo que um falhe — voce ve TODOS os problemas de uma vez",
             "subTest so funciona com numeros",
             "subTest substitui o setUp e o tearDown"],
            1,
            "Sem subTest: um loop de assertEqual para no primeiro que falha. "
            "Voce corrige, roda de novo, descobre o proximo falho, e assim por diante. "
            "Com subTest: Python continua o loop mesmo apos falhas e mostra "
            "todos os casos que falharam, identificados pelo parametro passado.",
        ),
        Quiz(
            "No ciclo TDD Red->Green->Refactor, o que 'Red' significa?",
            ["O codigo tem um erro de runtime",
             "Voce escreve um teste que FALHA porque o codigo que implementa o comportamento ainda nao existe",
             "O teste e deletado e reescrito do zero",
             "O terminal exibe erros em vermelho por configuracao"],
            1,
            "Red = teste escrito mas falhando (o codigo nao existe). "
            "Green = codigo minimo para o teste passar. "
            "Refactor = melhorar o codigo mantendo os testes verdes. "
            "A ideia central: so escreva codigo de producao quando "
            "ha um teste falhando que justifica aquele codigo.",
        ),
        Quiz(
            "Qual a principal vantagem de usar Mock() em vez de uma dependencia real?",
            ["Mocks sao mais rapidos de escrever",
             "Mocks isolam o teste da dependencia externa: sem rede, banco ou sistema de arquivos — o teste e rapido, deterministico e sem efeitos colaterais",
             "Mocks verificam automaticamente que o codigo esta correto",
             "Mocks so funcionam com pytest"],
            1,
            "Testes com dependencias reais sao lentos (rede, banco), frageis "
            "(falham se a API estiver fora) e tem efeitos colaterais. "
            "Mock() cria um objeto que registra chamadas e retorna valores configurados. "
            "assert_called_once_with() verifica nao so se foi chamado, "
            "mas com quais argumentos exatos.",
        ),
    ],
    projeto=(
        "Crie test_calculadora.py com testes para uma Calculadora usando TDD:\n\n"
        "   PASSO 1 (RED): escreva todos os testes primeiro\n"
        "   class Calculadora:\n"
        "       def somar(self, a, b): ...\n"
        "       def subtrair(self, a, b): ...\n"
        "       def multiplicar(self, a, b): ...\n"
        "       def dividir(self, a, b): ...\n"
        "       def historico(self): -> list[str]\n"
        "       def limpar(self): ...\n\n"
        "   TESTES QUE DEVEM EXISTIR:\n"
        "   - Operacoes basicas com valores normais\n"
        "   - Valores negativos e zero\n"
        "   - Divisao por zero (deve levantar ValueError)\n"
        "   - Historico: cada operacao e registrada como string\n"
        "   - Limpar: historico fica vazio apos limpar()\n"
        "   - setUp: cada teste recebe uma Calculadora nova\n\n"
        "   PASSO 2 (GREEN): implemente a Calculadora para passar\n"
        "   PASSO 3 (REFACTOR): melhore o codigo mantendo testes verdes\n\n"
        "Use subTest para testar multiplos pares de entrada em somar\n"
        "e subtrair sem duplicar metodos.\n\n"
        "BONUS: adicione um Mock para simular um servico de historico\n"
        "externo e verifique que ele e chamado corretamente."
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/unittest.html — unittest oficial",
        "docs.pytest.org — documentacao do pytest",
        "docs.python.org/pt-br/3/library/unittest.mock.html — mocks",
    ],
))
# ---------------------------------------------------------------- DIA 25
DIAS.append(Dia(
    numero=25,
    titulo="Python no Linux: os, sys, subprocess, argparse e logging",
    nivel="Avançado",
    duracao="110 min",
    objetivos=[
        "Navegar e manipular o sistema de arquivos com os e pathlib de forma segura",
        "Ler variáveis de ambiente, argumentos de linha de comando e informações do processo com os e sys",
        "Executar comandos externos com subprocess e capturar sua saída corretamente",
        "Construir interfaces de linha de comando profissionais com argparse",
        "Configurar o módulo logging para registrar eventos em diferentes níveis e destinos",
        "Reconhecer quando usar cada módulo: os, sys, subprocess, shutil ou pathlib",
    ],
    teoria="""
Python é uma das linguagens mais usadas para automação e scripts de
sistema no Linux. Os módulos os, sys, subprocess, argparse e logging
são os cinco pilares dessa integração — e aparecem em praticamente
todo script Python de produção.

---------------------------------------------------------------------------
1. os: interagindo com o sistema operacional
---------------------------------------------------------------------------
O módulo os oferece uma interface para funcionalidades do sistema
operacional que funcionam em qualquer plataforma (Linux, macOS, Windows):

INFORMAÇÕES DO PROCESSO:

    import os

    os.getpid()           # ID do processo atual
    os.getppid()          # ID do processo pai
    os.getcwd()           # diretório de trabalho atual (como pwd)
    os.getlogin()         # nome do usuário logado
    os.cpu_count()        # número de CPUs disponíveis

VARIÁVEIS DE AMBIENTE:

    os.environ            # dict-like com todas as variáveis de ambiente
    os.environ["HOME"]    # /home/usuario
    os.environ["PATH"]    # caminho de busca de executáveis
    os.getenv("PORTA", "8080")  # com valor padrão se não existir

    # Definindo variáveis (só para o processo atual e filhos)
    os.environ["MINHA_VAR"] = "valor"

SISTEMA DE ARQUIVOS (operações básicas):

    os.listdir(".")           # lista arquivos e diretórios (como ls)
    os.mkdir("novo_dir")      # cria um diretório
    os.makedirs("a/b/c", exist_ok=True)  # cria toda a hierarquia
    os.remove("arquivo.txt")  # apaga um arquivo
    os.rmdir("dir_vazio")     # apaga diretório vazio
    os.rename("velho", "novo")  # renomeia
    os.stat("arquivo.txt")    # metadados (tamanho, datas, permissões)

CAMINHOS COM os.path:

    os.path.join("pasta", "sub", "arquivo.txt")  # monta caminho
    os.path.exists("/etc/hosts")    # True se existe
    os.path.isfile("arq.txt")       # True se é arquivo
    os.path.isdir("/tmp")           # True se é diretório
    os.path.getsize("arquivo.txt")  # tamanho em bytes
    os.path.abspath("relativo")     # caminho absoluto
    os.path.basename("/a/b/arq.txt")  # 'arq.txt'
    os.path.dirname("/a/b/arq.txt")   # '/a/b'

PREFERÊNCIA MODERNA: use pathlib (Dia 14) para operações de caminho.
os.path ainda é muito comum em código legado — vale conhecer os dois.

PERCORRENDO DIRETÓRIOS RECURSIVAMENTE:

    for raiz, dirs, arquivos in os.walk("/home/usuario"):
        for arquivo in arquivos:
            caminho = os.path.join(raiz, arquivo)
            print(caminho)

    # Com pathlib (mais moderno):
    from pathlib import Path
    for caminho in Path("/home/usuario").rglob("*.py"):
        print(caminho)

---------------------------------------------------------------------------
2. sys: informações do interpretador e do processo
---------------------------------------------------------------------------
O módulo sys expõe informações sobre o interpretador Python e permite
controlar o comportamento do processo:

    import sys

    sys.argv              # lista de argumentos da linha de comando
                          # sys.argv[0] é o nome do script
                          # sys.argv[1:] são os argumentos passados

    sys.version           # versão do Python como string
    sys.platform          # 'linux', 'darwin', 'win32'
    sys.path              # lista de diretórios onde Python busca módulos

    sys.stdin             # entrada padrão (para leitura)
    sys.stdout            # saída padrão (para escrita)
    sys.stderr            # saída de erro

    sys.exit(0)           # encerra o processo (0 = sucesso, != 0 = erro)
    sys.exit("mensagem")  # encerra com mensagem de erro no stderr

    sys.getrecursionlimit()   # limite atual da pilha de recursão
    sys.getsizeof(objeto)     # tamanho do objeto em bytes

SAÍDA PARA STDERR:

    print("Erro crítico!", file=sys.stderr)   # aparece em vermelho no terminal
    # Scripts bem escritos enviam erros para stderr, não stdout

VERIFICANDO A PLATAFORMA:

    if sys.platform == "linux":
        caminho_config = Path.home() / ".config" / "app"
    elif sys.platform == "darwin":
        caminho_config = Path.home() / "Library" / "Application Support" / "app"

---------------------------------------------------------------------------
3. subprocess: executando comandos externos
---------------------------------------------------------------------------
subprocess permite executar programas externos (comandos do shell,
outros scripts, ferramentas de linha de comando) de dentro do Python:

A FUNÇÃO PRINCIPAL: subprocess.run()

    import subprocess

    # Forma segura: lista de argumentos (NUNCA string com shell=True em produção)
    resultado = subprocess.run(
        ["ls", "-la", "/tmp"],
        capture_output=True,    # captura stdout e stderr
        text=True,              # decodifica como texto (UTF-8)
        timeout=30,             # mata o processo após 30s se não terminar
    )

    resultado.returncode    # 0 = sucesso, != 0 = erro
    resultado.stdout        # saída padrão como string
    resultado.stderr        # saída de erro como string

VERIFICANDO SUCESSO:

    resultado = subprocess.run(["ls", "/caminho_invalido"],
                               capture_output=True, text=True)

    # Forma manual
    if resultado.returncode != 0:
        raise RuntimeError(resultado.stderr)

    # Forma automática: levanta CalledProcessError se returncode != 0
    resultado = subprocess.run([...], check=True)

POR QUE LISTA E NÃO STRING?

    # PERIGOSO: injeção de comandos
    nome = "arquivo.txt; rm -rf /"
    subprocess.run(f"ls {nome}", shell=True)   # executa rm -rf /!

    # SEGURO: lista — cada elemento é um argumento literal
    subprocess.run(["ls", nome])   # ls trata o nome inteiro como argumento

VARIANTES:

    subprocess.check_output(["cmd"])          # retorna só o stdout, levanta erro
    subprocess.call(["cmd"])                  # retorna só o returncode
    subprocess.Popen(["cmd"])                 # controle total (stdin/stdout/pipes)

OBTENDO SAÍDA:

    saida = subprocess.run(
        ["python3", "--version"],
        capture_output=True,
        text=True
    ).stdout.strip()
    print(saida)    # Python 3.12.3

---------------------------------------------------------------------------
4. argparse: interfaces de linha de comando profissionais
---------------------------------------------------------------------------
argparse transforma sys.argv numa interface de linha de comando com
ajuda automática, validação e tipos:

    import argparse

    def criar_parser():
        parser = argparse.ArgumentParser(
            description="Processa um arquivo de log"
        )

        # Argumento posicional (obrigatório)
        parser.add_argument("arquivo", help="arquivo de log para processar")

        # Opção com valor (--linhas 20)
        parser.add_argument(
            "-n", "--linhas",
            type=int,
            default=10,
            help="número de linhas a exibir (padrão: 10)"
        )

        # Flag booleana (--verbose ou -v)
        parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="exibe informações detalhadas"
        )

        # Opção com escolhas limitadas
        parser.add_argument(
            "--formato",
            choices=["json", "csv", "texto"],
            default="texto"
        )

        return parser

    # Usando
    parser = criar_parser()
    args = parser.parse_args()        # lê sys.argv automaticamente
    args = parser.parse_args(argv)    # ou uma lista de strings (para testes!)

    print(args.arquivo)    # string
    print(args.linhas)     # int (argparse converteu automaticamente)
    print(args.verbose)    # bool

    # Ajuda gerada automaticamente ao rodar com --help:
    # usage: script.py [-h] [-n LINHAS] [-v] arquivo
    # Processa um arquivo de log
    # ...

ARGPARSE EM FUNÇÕES TESTÁVEIS:

    def analisar(argv=None):
        parser = criar_parser()
        args = parser.parse_args(argv)   # None = usa sys.argv
        return args.arquivo, args.linhas, args.verbose

    # Testável sem tocar sys.argv:
    analisar(["log.txt", "-n", "5", "--verbose"])

---------------------------------------------------------------------------
5. logging: registros estruturados e configuráveis
---------------------------------------------------------------------------
print() para depuração não escala. logging oferece níveis, formatação,
múltiplos destinos e controle fino do que aparece onde:

NÍVEIS DE LOG (do menos ao mais grave):

    Nível       Valor    Uso típico
    ---------   -----    ------------------------------------------
    DEBUG       10       Detalhes técnicos, apenas em desenvolvimento
    INFO        20       Eventos normais de operação
    WARNING     30       Algo inesperado mas não grave
    ERROR       40       Erro que impede uma operação específica
    CRITICAL    50       Erro grave que pode parar o sistema

CONFIGURAÇÃO BÁSICA:

    import logging

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="app.log",    # omita para escrever no terminal
        filemode="a",          # 'a' = append, 'w' = sobrescreve
    )

    logger = logging.getLogger(__name__)   # logger com nome do módulo

    logger.debug("variavel x = %s", x)    # formato printf — mais eficiente
    logger.info("processando arquivo: %s", nome)
    logger.warning("disco com %d%% de uso", uso)
    logger.error("falha ao conectar: %s", str(e))
    logger.critical("banco de dados inacessível!")

POR QUE USAR LOGGER E NÃO LOGGING DIRETO?

    logging.info("mensagem")   # usa o logger raiz — evite em módulos
    logger = logging.getLogger(__name__)  # logger com nome do arquivo
    logger.info("mensagem")    # permite filtrar por módulo

MÚLTIPLOS HANDLERS (terminal + arquivo ao mesmo tempo):

    logger = logging.getLogger("meu_app")
    logger.setLevel(logging.DEBUG)

    # Handler para o terminal
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)   # só WARNING+ no terminal

    # Handler para arquivo
    arquivo = logging.FileHandler("debug.log")
    arquivo.setLevel(logging.DEBUG)     # tudo no arquivo

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    console.setFormatter(formatter)
    arquivo.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(arquivo)

---------------------------------------------------------------------------
6. shutil: operações de alto nível em arquivos
---------------------------------------------------------------------------
shutil complementa os com operações que envolvem múltiplos arquivos:

    import shutil

    shutil.copy("origem.txt", "destino.txt")      # copia arquivo
    shutil.copy2("origem.txt", "destino/")        # copia preservando metadados
    shutil.copytree("dir_orig", "dir_dest")       # copia diretório inteiro
    shutil.move("origem", "destino")              # move (como mv)
    shutil.rmtree("dir_com_conteudo")             # apaga diretório e conteúdo
    shutil.make_archive("backup", "zip", "pasta") # cria arquivo zip
    shutil.disk_usage("/")                        # espaço em disco
    shutil.which("python3")                       # onde está o executável

GUIA DE DECISÃO:

    Preciso de:                    Use:
    --------------------------     ------------------
    Caminho como objeto            pathlib.Path
    Info de ambiente/processo      os / sys
    Executar comando externo       subprocess
    Copiar/mover/zipar arquivos    shutil
    Argumentos CLI                 argparse
    Logs estruturados              logging
""",
    exemplos=[
        Exemplo(
            titulo="os e sys: inspecionando o ambiente",
            codigo='''import os
import sys
from pathlib import Path

# Informacoes do processo
print(f"PID: {os.getpid()}")
print(f"Diretorio atual: {os.getcwd()}")
print(f"Python: {sys.version.split()[0]}")
print(f"Plataforma: {sys.platform}")

# Variaveis de ambiente
home = os.environ.get("HOME", "desconhecido")
path = os.environ.get("PATH", "")
print(f"HOME: {home}")
print(f"PATH tem {len(path.split(':'))} entradas")

# Percorrendo arquivos por extensao
def listar_por_extensao(diretorio, extensao):
    """Lista arquivos de uma extensao em um diretorio."""
    return sorted(
        p for p in Path(diretorio).rglob(f"*.{extensao}")
        if p.is_file()
    )

# Inspecionando tamanho total de .py no diretorio atual
arquivos_py = listar_por_extensao(".", "py")
total = sum(f.stat().st_size for f in arquivos_py)
print(f"Arquivos .py encontrados: {len(arquivos_py)}")
print(f"Tamanho total: {total:,} bytes")

# Verificando argumentos da linha de comando
print(f"Script chamado como: {sys.argv[0]}")
print(f"Argumentos extras: {sys.argv[1:]}")
''',
            explicacao="os.environ.get() com valor padrão é mais seguro que "
                       "os.environ[] pois não levanta KeyError se a variável "
                       "não existir. "
                       "Path.rglob('*.py') percorre recursivamente todos os "
                       "subdiretórios sem precisar de os.walk. "
                       "stat().st_size retorna o tamanho em bytes — útil para "
                       "relatórios de uso de disco.",
        ),
        Exemplo(
            titulo="subprocess: executando comandos com segurança",
            codigo='''import subprocess
import sys

def rodar_comando(cmd, entrada=None):
    """Executa um comando e retorna (returncode, stdout, stderr)."""
    resultado = subprocess.run(
        cmd,
        input=entrada,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return resultado.returncode, resultado.stdout.strip(), resultado.stderr.strip()

# Exemplos de uso seguro
codigo, saida, erro = rodar_comando(["python3", "--version"])
print(f"Python versao: {saida}")

codigo, saida, erro = rodar_comando(["echo", "Ola do subprocess!"])
print(f"echo retornou: {repr(saida)}")

# Passando entrada para o processo
codigo, saida, erro = rodar_comando(
    ["python3", "-c", "import sys; print(sys.stdin.read().upper())"],
    entrada="hello world\n"
)
print(f"Maiusculas: {saida}")

# Verificando erro
codigo, saida, erro = rodar_comando(["ls", "/caminho_que_nao_existe"])
if codigo != 0:
    print(f"Falhou (codigo {codigo}): {erro}")

# Forma com check=True: levanta excecao automaticamente
try:
    subprocess.run(
        ["ls", "/caminho_invalido"],
        check=True,
        capture_output=True,
        text=True
    )
except subprocess.CalledProcessError as e:
    print(f"CalledProcessError: codigo={e.returncode}")
    print(f"stderr: {e.stderr.strip()}")
''',
            explicacao="capture_output=True captura stdout e stderr separadamente. "
                       "text=True decodifica os bytes como texto UTF-8. "
                       "input= permite passar dados para o stdin do processo. "
                       "check=True é a forma mais concisa de verificar sucesso — "
                       "levanta CalledProcessError com toda a informação do processo. "
                       "NUNCA use shell=True com dados do usuário.",
        ),
        Exemplo(
            titulo="argparse + logging: script profissional completo",
            codigo='''import argparse
import logging
import sys
from pathlib import Path

# Configuracao do logging
def configurar_log(verbose: bool, arquivo_log: str | None = None):
    nivel = logging.DEBUG if verbose else logging.INFO
    handlers = [logging.StreamHandler(sys.stdout)]
    if arquivo_log:
        handlers.append(logging.FileHandler(arquivo_log))
    logging.basicConfig(
        level=nivel,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
        handlers=handlers,
    )
    return logging.getLogger(__name__)

# Parser da CLI
def criar_parser():
    p = argparse.ArgumentParser(
        description="Analisa um arquivo e exibe estatisticas."
    )
    p.add_argument("arquivo", help="arquivo a analisar")
    p.add_argument("-n", "--linhas", type=int, default=10,
                   help="numero de linhas (padrao: 10)")
    p.add_argument("-v", "--verbose", action="store_true",
                   help="modo detalhado")
    p.add_argument("--log", metavar="ARQUIVO",
                   help="grava log neste arquivo")
    return p

def main(argv=None):
    args = criar_parser().parse_args(argv)
    log = configurar_log(args.verbose, args.log)

    caminho = Path(args.arquivo)
    log.debug("Verificando arquivo: %s", caminho)

    if not caminho.exists():
        log.error("Arquivo nao encontrado: %s", caminho)
        sys.exit(1)

    log.info("Processando %s (%d bytes)", caminho.name, caminho.stat().st_size)
    linhas = caminho.read_text().splitlines()

    log.debug("Total de linhas: %d", len(linhas))
    print(f"Arquivo: {caminho.name}")
    print(f"Linhas:  {len(linhas)}")
    print(f"Primeiras {args.linhas}:")
    for i, l in enumerate(linhas[:args.linhas], 1):
        print(f"  {i:3}: {l}")

# Simula chamada com argumentos (sem tocar sys.argv)
import tempfile, os
tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
tmp.write("linha 1\nlinha 2\nlinha 3\nlinha 4\nlinha 5\n")
tmp.close()
main([tmp.name, "-n", "3", "-v"])
os.unlink(tmp.name)
''',
            explicacao="configurar_log aceita múltiplos handlers dinamicamente — "
                       "o logger pode escrever no terminal e em arquivo ao mesmo tempo. "
                       "log.debug('%s', valor) é mais eficiente que "
                       "log.debug(f'{valor}') porque a string só é formatada "
                       "se o nível DEBUG estiver ativo. "
                       "main(argv=None) torna o script testável sem modificar sys.argv.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d25e1",
            enunciado=(
                "O import subprocess ja esta na assinatura.\n"
                "Escreva a funcao rodar(comando) que recebe uma LISTA\n"
                "de strings representando um comando e seus argumentos,\n"
                "executa o comando e retorna a saida como string (sem\n"
                "espacos/quebras nas pontas).\n\n"
                "Exemplos:\n"
                "   rodar(['echo', 'ola'])    -> 'ola'\n"
                "   rodar(['printf', 'a b'])  -> 'a b'\n\n"
                "Use subprocess.run() com:\n"
                "   capture_output=True  <- captura stdout e stderr\n"
                "   text=True            <- decodifica como texto UTF-8\n\n"
                "Depois acesse .stdout e aplique .strip() para remover\n"
                "a quebra de linha que echo adiciona no final.\n\n"
                "Estrutura:\n"
                "   resultado = subprocess.run(\n"
                "       comando,\n"
                "       capture_output=True,\n"
                "       text=True\n"
                "   )\n"
                "   return resultado.stdout.strip()"
            ),
            funcao="rodar",
            assinatura="import subprocess\n\n\ndef rodar(comando):",
            testes=[
                ("rodar(['echo', 'ola'])", "'ola'"),
                ("rodar(['printf', 'a b'])", "'a b'"),
            ],
            dica="return subprocess.run(comando, capture_output=True, text=True).stdout.strip()",
        ),
        Exercicio(
            id="d25e2",
            enunciado=(
                "O import argparse ja esta na assinatura.\n"
                "Escreva analisar(argv) que configura um ArgumentParser\n"
                "e retorna uma TUPLA (arquivo, linhas, verbose).\n\n"
                "O parser deve aceitar:\n"
                "   arquivo        argumento posicional obrigatorio (str)\n"
                "   -n/--linhas    numero inteiro, padrao 10\n"
                "   -v/--verbose   flag booleana (store_true)\n\n"
                "Exemplos:\n"
                "   analisar(['log.txt'])              -> ('log.txt', 10, False)\n"
                "   analisar(['a.txt', '-n', '5', '-v']) -> ('a.txt', 5, True)\n"
                "   analisar(['b.txt', '--linhas', '3']) -> ('b.txt', 3, False)\n\n"
                "Estrutura:\n"
                "   parser = argparse.ArgumentParser()\n"
                "   parser.add_argument('arquivo')\n"
                "   parser.add_argument('-n', '--linhas', type=int, default=10)\n"
                "   parser.add_argument('-v', '--verbose', action='store_true')\n"
                "   args = parser.parse_args(argv)  <- recebe a lista diretamente\n"
                "   return args.arquivo, args.linhas, args.verbose\n\n"
                "parse_args(argv) com a lista explícita permite testar\n"
                "sem modificar sys.argv — essencial para o corretor."
            ),
            funcao="analisar",
            assinatura="import argparse\n\n\ndef analisar(argv):",
            testes=[
                ("analisar(['log.txt'])", "('log.txt', 10, False)"),
                ("analisar(['a.txt', '-n', '5', '-v'])", "('a.txt', 5, True)"),
                ("analisar(['b.txt', '--linhas', '3'])", "('b.txt', 3, False)"),
            ],
            nivel="dificil",
            dica="parser.add_argument('-n','--linhas', type=int, default=10); parser.add_argument('-v','--verbose', action='store_true'); args = parser.parse_args(argv); return args.arquivo, args.linhas, args.verbose",
        ),
        Exercicio(
            id="d25e3",
            enunciado=(
                "Escreva tamanho_legivel(bytes_) que converte um numero\n"
                "de bytes para uma string legivel com a unidade correta.\n\n"
                "Exemplos:\n"
                "   tamanho_legivel(0)          -> '0.0 B'\n"
                "   tamanho_legivel(1536)        -> '1.5 KB'\n"
                "   tamanho_legivel(1048576)     -> '1.0 MB'\n"
                "   tamanho_legivel(5368709120)  -> '5.0 GB'\n\n"
                "Unidades: B, KB, MB, GB, TB (cada uma e 1024 da anterior)\n\n"
                "Estrategia:\n"
                "   unidades = ['B', 'KB', 'MB', 'GB', 'TB']\n"
                "   valor = float(bytes_)\n"
                "   for unidade in unidades:\n"
                "       if valor < 1024:            <- cabe nesta unidade?\n"
                "           return f'{valor:.1f} {unidade}'\n"
                "       valor /= 1024               <- passa para a proxima\n"
                "   return f'{valor:.1f} TB'         <- maior que tudo\n\n"
                "Verificacao:\n"
                "   0 B:   0.0 / 1024 = 0.0 < 1024 -> '0.0 B'\n"
                "   1536 B: 1536 >= 1024 -> divide -> 1.5 < 1024 -> '1.5 KB'\n"
                "   1048576: / 1024 = 1024.0 >= 1024 -> / 1024 = 1.0 -> '1.0 MB'"
            ),
            funcao="tamanho_legivel",
            assinatura="def tamanho_legivel(bytes_):",
            testes=[
                ("tamanho_legivel(0)", "'0.0 B'"),
                ("tamanho_legivel(1536)", "'1.5 KB'"),
                ("tamanho_legivel(1048576)", "'1.0 MB'"),
                ("tamanho_legivel(5368709120)", "'5.0 GB'"),
            ],
            nivel="medio",
            dica="unidades = ['B','KB','MB','GB','TB']; valor = float(bytes_); for u in unidades: if valor < 1024: return f'{valor:.1f} {u}'; valor /= 1024; return f'{valor:.1f} TB'",
        ),
    ],
    quiz=[
        Quiz(
            "Por que passar uma LISTA para subprocess.run em vez de uma string com shell=True?",
            ["Listas sao mais rapidas de processar",
             "Com lista, cada elemento e um argumento literal — impossivel injecao de comandos; com shell=True e string, um usuario malicioso pode injetar comandos arbitrarios",
             "shell=True nao funciona no Linux",
             "Nao ha diferenca de seguranca entre os dois"],
            1,
            "Se nome = 'arquivo.txt; rm -rf /', entao:\n"
            "subprocess.run(f'ls {nome}', shell=True) executa 'rm -rf /'!\n"
            "subprocess.run(['ls', nome]) trata o nome inteiro como argumento — "
            "o shell nunca ve o ponto-e-virgula. "
            "Use shell=True apenas com strings que voce mesmo construiu, "
            "nunca com dados vindos do usuario.",
        ),
        Quiz(
            "Qual a diferenca entre os.environ['VAR'] e os.getenv('VAR', 'padrao')?",
            ["Nao ha diferenca — sao identicos",
             "os.environ['VAR'] levanta KeyError se VAR nao existir; os.getenv retorna None (ou o padrao) sem erro",
             "os.getenv e mais lento que os.environ",
             "os.environ so funciona para variaveis do sistema; getenv para variaveis do usuario"],
            1,
            "os.environ['VAR'] funciona como dict: KeyError se a chave nao existe. "
            "os.getenv('VAR') retorna None se nao existe. "
            "os.getenv('VAR', 'padrao') retorna 'padrao' se nao existe. "
            "Para variaveis que podem nao estar definidas, getenv com padrao e mais robusto.",
        ),
        Quiz(
            "Por que usar log.debug('%s', valor) em vez de log.debug(f'{valor}')?",
            ["Nao ha diferenca pratica — e so estilo",
             "Com %s, a string so e formatada se o nivel DEBUG estiver ativo — economiza processamento quando o log esta desabilitado",
             "f-strings nao funcionam dentro de chamadas de log",
             "log.debug so aceita strings simples, nao f-strings"],
            1,
            "log.debug(f'valor={valor}') SEMPRE formata a string, mesmo que DEBUG "
            "esteja desabilitado (o que e comum em producao). "
            "log.debug('valor=%s', valor) so formata se o logger for emitir a mensagem. "
            "Em loops com milhoes de iteracoes, isso faz diferenca real de desempenho.",
        ),
        Quiz(
            "O que action='store_true' faz num argumento do argparse?",
            ["Armazena a string 'true' como valor do argumento",
             "Cria uma flag booleana: False por padrao, True se o argumento estiver presente na linha de comando",
             "Torna o argumento obrigatorio",
             "Converte automaticamente o valor para booleano"],
            1,
            "store_true cria um argumento opcional que nao recebe valor. "
            "Se '--verbose' aparecer: args.verbose = True. "
            "Se '--verbose' nao aparecer: args.verbose = False. "
            "E o padrao para flags on/off como --debug, --quiet, --force.",
        ),
    ],
    projeto=(
        "Crie analisador_log.py — um script de linha de comando completo:\n\n"
        "   INTERFACE CLI (argparse):\n"
        "   analisador_log.py <arquivo> [opcoes]\n"
        "   -n/--linhas N      exibe as N primeiras linhas (padrao: 20)\n"
        "   -l/--nivel NIVEL   filtra por nivel de log (DEBUG/INFO/WARNING/ERROR)\n"
        "   -v/--verbose       modo detalhado\n"
        "   --stats            exibe contagem por nivel\n"
        "   --saida ARQUIVO    salva resultado num arquivo\n\n"
        "   FUNCIONALIDADES:\n"
        "   1. Le o arquivo de log linha a linha (uma linha por vez, nao tudo)\n"
        "   2. Filtra por nivel se --nivel for especificado\n"
        "   3. Exibe as N primeiras linhas que passaram no filtro\n"
        "   4. Com --stats: conta quantas linhas de cada nivel existem\n"
        "   5. Com --saida: escreve o resultado no arquivo indicado\n\n"
        "   LOGGING INTERNO:\n"
        "   O proprio script deve usar logging para registrar:\n"
        "   - INFO: arquivo aberto, linhas processadas\n"
        "   - DEBUG: cada linha lida (so com -v)\n"
        "   - ERROR: arquivo nao encontrado, formato invalido\n\n"
        "   BONUS: use subprocess para chamar 'wc -l arquivo' e\n"
        "   exibir o total de linhas antes de processar."
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/os.html — modulo os",
        "docs.python.org/pt-br/3/library/subprocess.html — subprocess",
        "docs.python.org/pt-br/3/library/argparse.html — argparse",
        "docs.python.org/pt-br/3/library/logging.html — logging",
    ],
))
# ---------------------------------------------------------------- DIA 26
DIAS.append(Dia(
    numero=26,
    titulo="Expressoes regulares e processamento de texto",
    nivel="Avancado",
    duracao="110 min",
    objetivos=[
        "Entender o que sao expressoes regulares e quando elas resolvem o que strings nao resolvem",
        "Escrever padroes com os metacaracteres essenciais: . * + ? [] {} ^ $ | () \\",
        "Usar re.search, re.match, re.findall, re.sub e re.compile corretamente",
        "Extrair grupos de captura e grupos nomeados de um match",
        "Usar flags como re.IGNORECASE e re.MULTILINE para ajustar o comportamento",
        "Saber quando NAO usar regex: casos onde split, strip ou replace sao suficientes",
    ],
    teoria="""
Strings tem metodos poderosos: find(), replace(), split(), strip().
Mas esses metodos so encontram padroes FIXOS. Como encontrar qualquer
endereco de email? Qualquer data no formato DD/MM/AAAA? Qualquer numero
de telefone independente da formatacao? Para padroes variaveis, a
ferramenta certa sao as expressoes regulares.

---------------------------------------------------------------------------
1. O que e uma expressao regular
---------------------------------------------------------------------------
Uma expressao regular (ou regex) e um padrao de texto que descreve um
conjunto de strings possiveis. Em vez de buscar "ana@email.com" (fixo),
voce descreve o padrao "[qualquer coisa]@[qualquer coisa].[qualquer coisa]".

    import re

    # Busca simples: encontrar "python" (case-insensitive)
    re.search(r"python", "Eu amo Python!", re.IGNORECASE)
    # Match object -- encontrou!

    re.search(r"python", "Eu amo Java!")
    # None -- nao encontrou

SEMPRE USE RAW STRINGS (r"...") para padroes regex:
Backslash (\) tem significado especial tanto em strings Python quanto em
regex. r"\d" sao dois caracteres: barra e d. Sem o r, "\d" precisaria
ser "\\d" -- confuso e propenso a erros.

---------------------------------------------------------------------------
2. Metacaracteres: os blocos de construcao do regex
---------------------------------------------------------------------------
CORRESPONDENDO CARACTERES:

    Padrao    Corresponde a
    -------   -------------------------------------------------------
    .         qualquer caractere, exceto newline
    \d        digito: [0-9]
    \D        nao-digito: [^0-9]
    \w        caractere de palavra: [a-zA-Z0-9_]
    \W        nao-palavra
    \s        espaco em branco: [ \t\n\r\f\v]
    \S        nao-espaco
    [abc]     a, b ou c (classe de caracteres)
    [a-z]     qualquer letra minuscula
    [^abc]    qualquer coisa EXCETO a, b ou c

QUANTIFICADORES (quantas vezes o anterior pode aparecer):

    Padrao    Significado
    -------   -------------------------------------------------------
    *         0 ou mais vezes (guloso)
    +         1 ou mais vezes (guloso)
    ?         0 ou 1 vez (torna opcional)
    {n}       exatamente n vezes
    {n,m}     entre n e m vezes
    *?        0 ou mais vezes (preguicoso/lazy)
    +?        1 ou mais vezes (preguicoso/lazy)

ANCORAS (posicao, nao caractere):

    Padrao    Corresponde a posicao
    -------   -------------------------------------------------------
    ^         inicio da string (ou linha com re.MULTILINE)
    $         fim da string (ou linha com re.MULTILINE)
    \b        fronteira de palavra (entre \w e \W)
    \B        nao e fronteira de palavra

GRUPOS E ALTERNANCIA:

    Padrao       Significado
    ----------   -------------------------------------------------------
    (abc)        grupo de captura: captura o que casou
    (?:abc)      grupo sem captura: agrupa mas nao captura
    (?P<nome>)   grupo nomeado: captura com nome acessivel
    a|b          a ou b (alternancia)

GULOSO VERSUS PREGUICOSO:
Por padrao, quantificadores sao GULOSOS: tentam corresponder o maximo
possivel.

    texto = "<b>negrito</b> e <i>italico</i>"
    re.findall(r"<.+>",  texto)   # ['<b>negrito</b> e <i>italico</i>'] -- guloso!
    re.findall(r"<.+?>", texto)   # ['<b>', '</b>', '<i>', '</i>'] -- preguicoso

---------------------------------------------------------------------------
3. As funcoes do modulo re
---------------------------------------------------------------------------
SEARCH vs MATCH:

    re.search(padrao, texto)  -- procura em QUALQUER posicao da string
    re.match(padrao, texto)   -- procura SOMENTE no inicio da string

    re.search(r"\d+", "abc 123")   # Match: encontrou '123'
    re.match(r"\d+",  "abc 123")   # None: '123' nao esta no inicio
    re.match(r"\d+",  "123 abc")   # Match: '123' esta no inicio

FINDALL e FINDITER:

    re.findall(padrao, texto)   -- retorna LISTA de todas as ocorrencias
    re.finditer(padrao, texto)  -- retorna ITERADOR de Match objects (lazy)

    re.findall(r"\d+", "a1b23c456")   # ['1', '23', '456']

    for m in re.finditer(r"\d+", "a1b23c456"):
        print(m.group(), m.start(), m.end())

SUB e SUBN:

    re.sub(padrao, substituto, texto)   -- substitui todas as ocorrencias
    re.subn(padrao, substituto, texto)  -- retorna (resultado, num_subs)

    re.sub(r"\d", "X", "a1b2c3")        # 'aXbXcX'
    re.sub(r"(\d+)", r"[\1]", "1 2 3")  # '[1] [2] [3]'  (\1 = primeiro grupo)

SPLIT:

    re.split(padrao, texto)   -- divide por qualquer padrao

    re.split(r"\s+",    "  a  b    c  ")   # ['', 'a', 'b', 'c', '']
    re.split(r"[,;]\s*", "a, b;c,d")       # ['a', 'b', 'c', 'd']

COMPILE -- reutilizando padroes compilados:

    EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")

    emails = EMAIL.findall(texto1)
    if EMAIL.search(texto2):
        print("tem email")

---------------------------------------------------------------------------
4. Grupos de captura
---------------------------------------------------------------------------
Grupos () capturam partes do padrao que voce pode extrair separadamente:

    texto = "Data: 28/07/2026"
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})", texto)

    if m:
        m.group(0)   # '28/07/2026'  -- match completo
        m.group(1)   # '28'          -- primeiro grupo (dia)
        m.group(2)   # '07'          -- segundo grupo (mes)
        m.group(3)   # '2026'        -- terceiro grupo (ano)
        m.groups()   # ('28', '07', '2026') -- todos os grupos

GRUPOS NOMEADOS -- mais legiveis:

    m = re.search(r"(?P<dia>\d{2})/(?P<mes>\d{2})/(?P<ano>\d{4})", texto)
    m.group("dia")   # '28'
    m.group("mes")   # '07'
    m.group("ano")   # '2026'
    m.groupdict()    # {'dia': '28', 'mes': '07', 'ano': '2026'}

BACKREFERENCES EM SUB:
Grupos capturados podem ser referenciados no substituto com \1, \2...:

    # Convertendo DD/MM/AAAA -> AAAA-MM-DD
    re.sub(r"(\d{2})/(\d{2})/(\d{4})", r"\3-\2-\1", "28/07/2026")
    # '2026-07-28'

    # Com grupos nomeados (mais legivel):
    re.sub(
        r"(?P<d>\d{2})/(?P<m>\d{2})/(?P<a>\d{4})",
        r"\g<a>-\g<m>-\g<d>",
        "28/07/2026"
    )
    # '2026-07-28'

---------------------------------------------------------------------------
5. Flags: modificando o comportamento
---------------------------------------------------------------------------

    Flag              Abrev    Efeito
    ---------------   ------   --------------------------------------------
    re.IGNORECASE     re.I     case-insensitive: 'a' casa 'A' e 'a'
    re.MULTILINE      re.M     ^ e $ casam inicio/fim de CADA linha
    re.DOTALL         re.S     . casa newline tambem
    re.VERBOSE        re.X     permite comentarios e espacos no padrao
    re.ASCII          re.A     \w, \d etc. casam apenas ASCII

MULTIPLAS FLAGS:

    re.findall(r"python", texto, re.IGNORECASE | re.MULTILINE)

RE.VERBOSE -- padroes documentados com comentarios:

    EMAIL = re.compile(r'''
        [\w.+-]+    # parte local (antes do @)
        @           # arroba literal
        [\w-]+      # dominio
        \.          # ponto literal (escapado)
        [\w.]+      # TLD (pode ter subdomínios como .com.br)
    ''', re.VERBOSE)

---------------------------------------------------------------------------
6. Receitas comuns
---------------------------------------------------------------------------

    # Email (versao simplificada)
    r"[\w.+-]+@[\w-]+\.[\w.]+"

    # Data DD/MM/AAAA
    r"\d{2}/\d{2}/\d{4}"

    # CPF (com ou sem formatacao)
    r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}"

    # CEP brasileiro
    r"\d{5}-?\d{3}"

    # URL simples
    r"https?://[\w./%-]+"

    # Numero com decimal opcional
    r"-?\d+(?:\.\d+)?"

    # Palavra inteira (fronteiras de palavra)
    r"\bpython\b"    # casa 'python' mas nao 'pythonista'

---------------------------------------------------------------------------
7. Quando NAO usar regex
---------------------------------------------------------------------------
Regex e poderosa mas nao e a ferramenta certa para tudo:

    NAO USE regex quando strings simples resolvem:
    "ana@email.com".split("@")       # mais claro que regex
    "  texto  ".strip()              # mais claro que regex
    texto.startswith("http")         # mais claro que regex
    "python" in texto                # mais claro que regex

    NAO USE regex para parsear estruturas:
    - HTML/XML:  use BeautifulSoup ou lxml
    - JSON:      use json.loads()
    - CSV:       use csv.reader()

A regra: se voce precisa de um comentario para explicar o regex,
talvez haja uma abordagem mais clara. Regex deve ser usada quando
o padrao e genuinamente variavel e nao estruturado.
""",
    exemplos=[
        Exemplo(
            titulo="Extraindo informacoes com grupos de captura",
            codigo='''import re

# Extraindo emails de texto livre
texto = """
Contatos da equipe:
  - Comercial: vendas@empresa.com.br e suporte@empresa.com
  - Dev: dev+alerts@github.io
  - Invalido: nao-e-email, tampouco @isso
"""

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
emails = EMAIL.findall(texto)
print("Emails:", emails)

# Extraindo e reformatando datas
texto_datas = "Contratos: 01/03/2024, 15/07/2024, 31/12/2024"

# Encontrando todas as datas
datas = re.findall(r"\d{2}/\d{2}/\d{4}", texto_datas)
print("Datas:", datas)

# Convertendo DD/MM/AAAA -> AAAA-MM-DD com grupos de captura
iso = re.sub(r"(\d{2})/(\d{2})/(\d{4})", r"\3-\2-\1", texto_datas)
print("Formato ISO:", iso)

# Grupos nomeados para maior clareza
for m in re.finditer(
    r"(?P<dia>\d{2})/(?P<mes>\d{2})/(?P<ano>\d{4})",
    texto_datas
):
    d = m.groupdict()
    print(f"  {d['ano']}-{d['mes']}-{d['dia']}")
''',
            explicacao="EMAIL compilado com re.compile fica reutilizavel e legivel. "
                       "findall sem grupos retorna lista de strings. "
                       "re.sub com \\1, \\2, \\3 referencia os grupos capturados "
                       "em ordem -- muito mais limpo do que fazer um loop com finditer. "
                       "Grupos nomeados tornam \\1 obsoleto para padroes complexos.",
        ),
        Exemplo(
            titulo="Padroes gulosos vs preguicosos e flags",
            codigo='''import re

# Guloso vs preguicoso
html = "<b>negrito</b> e texto <i>italico</i> aqui"

guloso      = re.findall(r"<.+>",  html)
preguicoso  = re.findall(r"<.+?>", html)
sem_gt      = re.findall(r"<[^>]+>", html)   # alternativa mais precisa

print("Guloso:     ", guloso)
print("Preguicoso: ", preguicoso)
print("Sem >:      ", sem_gt)

# re.IGNORECASE
palavras = ["Python", "PYTHON", "python", "PyThOn", "Java"]
pythons = [p for p in palavras if re.search(r"^python$", p, re.IGNORECASE)]
print("Case-insensitive:", pythons)

# re.MULTILINE: ^ e $ casam cada linha
texto_multi = """inicio da primeira linha
outra linha no meio
inicio da ultima linha"""

inicios = re.findall(r"^inicio\w*", texto_multi, re.MULTILINE)
print("Linhas com 'inicio':", inicios)

# re.VERBOSE: regex documentada com comentarios
TELEFONE = re.compile(r"""
    (\(?\d{2}\)?)   # DDD com ou sem parenteses
    \s?             # espaco opcional
    (9?\d{4})       # 4 ou 5 digitos (com ou sem 9 inicial)
    [-\s]?          # separador opcional
    (\d{4})         # ultimos 4 digitos
""", re.VERBOSE)

testes = ["(21) 99999-8888", "11 98765-4321", "21999998888"]
for t in testes:
    m = TELEFONE.search(t)
    if m:
        print(f"'{t}' -> grupos: {m.groups()}")
''',
            explicacao="<.+> captura do primeiro < ate o ULTIMO > da string inteira. "
                       "<.+?> para no primeiro > disponivel. "
                       "<[^>]+> e ainda mais preciso: 'um ou mais caracteres que nao sejam >'. "
                       "re.MULTILINE muda o significado de ^ e $ -- sem a flag, "
                       "^ so casa o inicio da string inteira. "
                       "re.VERBOSE permite escrever regex em multiplas linhas "
                       "com comentarios -- essencial para padroes complexos.",
        ),
        Exemplo(
            titulo="Processamento de texto com regex: pipeline completo",
            codigo='''import re
from collections import Counter

def normalizar(texto):
    """Limpa e normaliza texto para analise."""
    sem_html    = re.sub(r"<[^>]+>", "", texto)
    sem_extras  = re.sub(r"\s+", " ", sem_html).strip()
    limpo       = re.sub(r"[^\w\s-]", "", sem_extras)
    return limpo.lower()

def parse_log(linha):
    """Extrai campos de uma linha de log."""
    padrao = re.compile(r"""
        (?P<data>\d{4}-\d{2}-\d{2})   # data AAAA-MM-DD
        \s
        (?P<hora>\d{2}:\d{2}:\d{2})   # hora HH:MM:SS
        \s\|\s
        (?P<nivel>\w+)                  # nivel (INFO, ERROR...)
        \s\|\s
        (?P<msg>.+)                     # mensagem
    """, re.VERBOSE)
    m = padrao.match(linha)
    return m.groupdict() if m else None

# Testando normalizacao
texto_html = "<h1>Titulo</h1><p>Conteudo   com   espacos  extras.</p>"
print("Normalizado:", normalizar(texto_html))

# Testando parse de log
logs = [
    "2024-07-28 10:30:00 | INFO | usuario Ana fez login",
    "2024-07-28 10:31:15 | ERROR | falha ao conectar banco",
    "linha mal formatada sem padrao",
    "2024-07-28 10:32:00 | WARNING | disco com 90% de uso",
]

niveis = []
for linha in logs:
    parsed = parse_log(linha)
    if parsed:
        niveis.append(parsed["nivel"])
        print(f"[{parsed['nivel']}] {parsed['hora']}: {parsed['msg']}")

print("Contagem por nivel:", dict(Counter(niveis)))
''',
            explicacao="re.sub(r'<[^>]+>', '', texto) remove tags HTML. "
                       "[^>]+ significa 'um ou mais caracteres que nao sejam >'. "
                       "Sem isso, .+ seria guloso e comeria tudo entre o "
                       "primeiro < e o ultimo >. "
                       "O parser de log usa re.VERBOSE e grupos nomeados -- "
                       "cada campo e auto-documentado no proprio padrao. "
                       "groupdict() retorna None se a linha nao casar.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d26e1",
            enunciado=(
                "O import re ja esta na assinatura.\n"
                "Escreva extrair_emails(texto) que encontra todos os\n"
                "enderecos de email em um texto e retorna uma lista.\n\n"
                "Exemplos:\n"
                "   extrair_emails('fale com ana@x.com ou bia@y.com.br')\n"
                "   -> ['ana@x.com', 'bia@y.com.br']\n\n"
                "   extrair_emails('nenhum aqui') -> []\n\n"
                "Padrao sugerido: r'[\\w.+-]+@[\\w-]+\\.[\\w.]+'\n\n"
                "Explicando o padrao:\n"
                "   [\\w.+-]+   parte local: letras, digitos, pontos, +, -\n"
                "   @          o @ literal\n"
                "   [\\w-]+     dominio: letras, digitos, hifens\n"
                "   \\.         ponto literal (. sem barra = qualquer char)\n"
                "   [\\w.]+     TLD: letras e pontos (para .com.br etc.)\n\n"
                "Use re.findall(padrao, texto) que retorna diretamente\n"
                "a lista de todas as ocorrencias encontradas."
            ),
            funcao="extrair_emails",
            assinatura="import re\n\n\ndef extrair_emails(texto):",
            testes=[
                ("extrair_emails('fale com ana@x.com ou bia@y.com.br')",
                 "['ana@x.com', 'bia@y.com.br']"),
                ("extrair_emails('nenhum aqui')", "[]"),
            ],
            nivel="medio",
            dica="return re.findall(r'[\\w.+-]+@[\\w-]+\\.[\\w.]+', texto)",
        ),
        Exercicio(
            id="d26e2",
            enunciado=(
                "O import re ja esta na assinatura.\n"
                "Escreva converter_datas(texto) que substitui todas as\n"
                "datas no formato DD/MM/AAAA pelo formato AAAA-MM-DD.\n\n"
                "Exemplos:\n"
                "   converter_datas('venceu em 28/07/2026 e 01/01/2027')\n"
                "   -> 'venceu em 2026-07-28 e 2027-01-01'\n\n"
                "   converter_datas('sem data') -> 'sem data'\n\n"
                "Use re.sub com grupos de captura:\n"
                "   padrao:    r'(\\d{2})/(\\d{2})/(\\d{4})'\n"
                "   substituto: r'\\3-\\2-\\1'\n\n"
                "Como funciona:\n"
                "   (\\d{2}) = grupo 1 = dia\n"
                "   (\\d{2}) = grupo 2 = mes\n"
                "   (\\d{4}) = grupo 3 = ano\n"
                "   \\3-\\2-\\1 = ano-mes-dia  (ordem invertida)\n\n"
                "re.sub substitui TODAS as ocorrencias de uma vez --\n"
                "nao precisa de loop."
            ),
            funcao="converter_datas",
            assinatura="import re\n\n\ndef converter_datas(texto):",
            testes=[
                ("converter_datas('venceu em 28/07/2026 e 01/01/2027')",
                 "'venceu em 2026-07-28 e 2027-01-01'"),
                ("converter_datas('sem data')", "'sem data'"),
            ],
            nivel="medio",
            dica="return re.sub(r'(\\d{2})/(\\d{2})/(\\d{4})', r'\\3-\\2-\\1', texto)",
        ),
        Exercicio(
            id="d26e3",
            enunciado=(
                "O import re ja esta na assinatura.\n"
                "Escreva validar_telefone(numero) que retorna True se\n"
                "o numero for um celular brasileiro valido (11 digitos:\n"
                "DDD + 9 + 8 digitos), False caso contrario.\n\n"
                "Formatos validos (sempre 11 digitos numericos):\n"
                "   '(21) 99999-8888'  -> True\n"
                "   '21999998888'      -> True\n\n"
                "Formatos invalidos:\n"
                "   '123'              -> False  (poucos digitos)\n"
                "   '(21) 9999-8888'   -> False  (10 digitos = fixo)\n\n"
                "Estrategia: remova tudo que nao for digito e verifique:\n"
                "   1. digitos = re.sub(r'\\D', '', numero)\n"
                "      \\D = qualquer coisa que nao seja digito\n"
                "   2. len(digitos) == 11  (deve ter exatamente 11)\n"
                "   3. digitos[2] == '9'   (3o digito e o 9 do celular)\n"
                "      DDD ocupa os 2 primeiros digitos (indices 0 e 1)\n"
                "      O 9 do celular fica no indice 2\n\n"
                "   return len(digitos) == 11 and digitos[2] == '9'"
            ),
            funcao="validar_telefone",
            assinatura="import re\n\n\ndef validar_telefone(numero):",
            testes=[
                ("validar_telefone('(21) 99999-8888')", "True"),
                ("validar_telefone('21999998888')", "True"),
                ("validar_telefone('123')", "False"),
                ("validar_telefone('(21) 9999-8888')", "False"),
            ],
            nivel="dificil",
            dica="digitos = re.sub(r'\\D', '', numero); return len(digitos) == 11 and digitos[2] == '9'",
        ),
    ],
    quiz=[
        Quiz(
            "Qual a diferenca entre re.search e re.match?",
            ["search e mais rapido que match",
             "search procura em qualquer posicao da string; match so procura no INICIO",
             "match retorna todos os resultados; search retorna apenas o primeiro",
             "search e case-sensitive; match e case-insensitive por padrao"],
            1,
            "re.match(r'\\d+', 'abc 123') retorna None porque '123' nao esta no inicio. "
            "re.search(r'\\d+', 'abc 123') encontra '123' em qualquer posicao. "
            "Para garantir correspondencia na string inteira, use ^ e $ no padrao.",
        ),
        Quiz(
            "O que r'<.+>' captura em '<b>texto</b> e <i>mais</i>'?",
            ["['<b>', '</b>', '<i>', '</i>'] -- cada tag separadamente",
             "'<b>texto</b> e <i>mais</i>' -- tudo do primeiro < ao ultimo >",
             "['<b>texto</b>', '<i>mais</i>'] -- cada par de tags",
             "Nada -- ponto nao casa com letras"],
            1,
            "+ e guloso: tenta corresponder o MAXIMO possivel. "
            "<.+> vai do primeiro < ate o ULTIMO > da string. "
            "Para capturar cada tag use o preguicoso: r'<.+?>' "
            "ou mais preciso: r'<[^>]+>' (tudo exceto >).",
        ),
        Quiz(
            "Por que usar raw strings r'...' para padroes regex?",
            ["Raw strings sao mais rapidas de processar",
             "Backslash tem significado especial tanto em strings Python quanto em regex -- raw strings evitam a dupla interpretacao",
             "Raw strings desabilitam os metacaracteres do regex",
             "Nao e necessario -- e apenas convencao opcional"],
            1,
            "\\d em string normal seria interpretado como 'd' (barra descartada). "
            "Para ter \\d no padrao regex voce precisaria escrever '\\\\d'. "
            "Com r'\\d' a barra e preservada e o regex a interpreta como 'digito'. "
            "Sempre use r'...' -- e mais claro e menos propenso a bugs.",
        ),
        Quiz(
            "No re.sub, o que r'\\3-\\2-\\1' faz como substituto?",
            ["Substitui pelo texto literal '\\3-\\2-\\1'",
             "Insere o terceiro grupo capturado, um hifem, o segundo e um hifem e o primeiro",
             "Inverte a string capturada",
             "Remove os grupos e insere hifens"],
            1,
            "No substituto do re.sub, \\1, \\2, \\3 referenciam os grupos de captura. "
            "Para o padrao r'(\\d{2})/(\\d{2})/(\\d{4})' com '28/07/2026': "
            "\\1='28' (dia), \\2='07' (mes), \\3='2026' (ano). "
            "r'\\3-\\2-\\1' = '2026-07-28' -- data reformatada para ISO 8601.",
        ),
    ],
    projeto=(
        "Crie extrator_contatos.py que processa texto livre e extrai\n"
        "informacoes estruturadas usando regex:\n\n"
        "   ENTRADA: texto livre com contatos misturados\n"
        "   ex: 'Ligue para Ana (21) 99999-8888 ou email ana@empresa.com.br\n"
        "        Bruno: 11987654321, bruno@dev.io'\n\n"
        "   FUNCOES:\n"
        "   1. extrair_emails(texto) -> list[str]\n"
        "   2. extrair_telefones(texto) -> list[str]\n"
        "      retorna numeros com apenas os digitos (11 digitos)\n"
        "   3. extrair_ceps(texto) -> list[str]\n"
        "      padrao: NNNNN-NNN ou NNNNNNNN\n"
        "   4. extrair_urls(texto) -> list[str]\n"
        "      padrao: http:// ou https:// seguido de caracteres validos\n"
        "   5. analisar(texto) -> dict\n"
        "      retorna {'emails': [...], 'telefones': [...], 'urls': [...]}\n\n"
        "   LIMPEZA:\n"
        "   6. normalizar(texto) -> str\n"
        "      remove HTML, normaliza espacos, converte datas DD/MM para ISO\n\n"
        "BONUS: adicione um modo CLI (argparse do Dia 25) que:\n"
        "   - Recebe um arquivo .txt como argumento\n"
        "   - Exibe os contatos extraidos formatados\n"
        "   - Com --json exporta como JSON"
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/re.html -- modulo re completo",
        "regex101.com -- testador interativo de regex",
        "docs.python.org/pt-br/3/howto/regex.html -- guia oficial de regex",
    ],
))
# ---------------------------------------------------------------- DIA 27
DIAS.append(Dia(
    numero=27,
    titulo="Concorrencia: threads, processos e o GIL",
    nivel="Avancado",
    duracao="120 min",
    objetivos=[
        "Entender o que e concorrencia versus paralelismo e quando cada um faz sentido",
        "Compreender o GIL: o que e, por que existe e como ele afeta threads em Python",
        "Usar threading para tarefas I/O-bound com Thread, Lock e Queue",
        "Usar multiprocessing para tarefas CPU-bound que escapam do GIL",
        "Usar concurrent.futures como interface unificada de alto nivel",
        "Reconhecer condicoes de corrida e protege-las com Lock",
    ],
    teoria="""
Ate agora, seus programas faziam uma coisa de cada vez: executavam
linha por linha, esperando cada operacao terminar antes de comecar a
proxima. Para muitos problemas isso e suficiente. Mas quando voce precisa
baixar 100 arquivos da internet, processar 1000 imagens ou responder
multiplos usuarios ao mesmo tempo, fazer uma coisa de cada vez se torna
um gargalo enorme.

---------------------------------------------------------------------------
1. Concorrencia versus paralelismo
---------------------------------------------------------------------------
Esses dois termos sao frequentemente confundidos, mas significam coisas
diferentes:

CONCORRENCIA: lidar com muitas coisas ao mesmo tempo.
    Multiplas tarefas EXISTEM simultaneamente, mas em qualquer instante
    apenas uma esta realmente em execucao. O sistema alterna rapidamente
    entre elas, dando a ilusao de simultaneidade.
    Analogia: um cozinheiro que coloca macacao para cozinhar, enquanto
    espera prepara o molho, enquanto molho aquece corta legumes.

PARALELISMO: fazer muitas coisas ao mesmo tempo.
    Multiplas tarefas realmente executam ao mesmo tempo, em nucleos
    de CPU diferentes.
    Analogia: dois cozinheiros na mesma cozinha, cada um fazendo uma
    coisa diferente simultaneamente.

Em Python:
    Threads   -> concorrencia (GIL impede paralelismo real para CPU)
    Processos -> paralelismo real (cada processo tem seu proprio GIL)
    asyncio   -> concorrencia cooperativa (veremos no Dia 28)

QUANDO CADA UM AJUDA:

    Tarefa        Exemplo                        Solucao
    ----------    --------------------------     -----------------------
    I/O-bound     download, banco, API           threads ou asyncio
    CPU-bound     calculos, imagens, ML          processos (multiprocessing)
    Misto         web scraping com parse         processos + threads

I/O-bound: o programa passa a maior parte do tempo ESPERANDO -- a rede
responder, o disco ler, o banco processar. Durante a espera o CPU fica
ocioso -- perfil ideal para threads.

CPU-bound: o programa passa a maior parte do tempo CALCULANDO --
comprimindo imagens, treinando modelos, calculando hashes. O CPU esta
sempre ocupado -- threads Python nao ajudam por causa do GIL.

---------------------------------------------------------------------------
2. O GIL: o que e e por que importa
---------------------------------------------------------------------------
GIL = Global Interpreter Lock (Trava Global do Interpretador).

E um mutex -- uma trava -- dentro do CPython que garante que apenas UMA
thread Python execute codigo bytecode de cada vez, mesmo que o computador
tenha multiplos nucleos.

POR QUE O GIL EXISTE?
O gerenciamento de memoria do CPython usa contagem de referencias. Cada
objeto Python tem um contador que rastreia quantas variaveis apontam para
ele. Sem protecao, duas threads poderiam decrementar o mesmo contador
simultaneamente e causar corrupcao de memoria. O GIL resolve isso de
forma simples: so uma thread executa por vez, entao nao ha conflito.

O QUE O GIL SIGNIFICA NA PRATICA:

    Para I/O-bound (download, leitura de arquivo, banco de dados):
    Threads FUNCIONAM BEM. Quando uma thread espera I/O, ela LIBERA
    o GIL para outra thread executar. Voce obtem concorrencia real.

    Para CPU-bound (calculos pesados):
    Threads NAO AJUDAM. Cada thread precisa do GIL para executar
    e elas se revezam uma de cada vez. Resultado: igual ou pior
    que uma thread so, com overhead de coordenacao.

    Para CPU-bound, use multiprocessing: cada PROCESSO tem seu
    proprio GIL, entao multiplos processos rodam em paralelo real.

---------------------------------------------------------------------------
3. threading: concorrencia com threads
---------------------------------------------------------------------------
O modulo threading permite criar e gerenciar threads:

    import threading
    import time

    def tarefa(nome, duracao):
        print(f"[{nome}] iniciando...")
        time.sleep(duracao)     # simula I/O: libera o GIL durante o sleep
        print(f"[{nome}] concluido!")

    t1 = threading.Thread(target=tarefa, args=("Alpha", 2))
    t2 = threading.Thread(target=tarefa, args=("Beta", 1))

    t1.start()   # inicia a thread (nao bloqueia)
    t2.start()

    t1.join()    # espera t1 terminar
    t2.join()    # espera t2 terminar

    # Beta termina antes por dormir menos:
    # [Alpha] iniciando...
    # [Beta] iniciando...
    # [Beta] concluido!
    # [Alpha] concluido!

join() e crucial: sem ele, o programa principal pode terminar antes
das threads. t.join() bloqueia ate que a thread t termine.

THREADS DAEMON:

    t = threading.Thread(target=tarefa, daemon=True)
    t.start()
    # Quando o programa principal terminar, threads daemon sao
    # encerradas automaticamente (mesmo que nao tenham terminado)

---------------------------------------------------------------------------
4. Condicoes de corrida e Lock
---------------------------------------------------------------------------
Quando multiplas threads compartilham e modificam o mesmo dado, pode
ocorrer uma CONDICAO DE CORRIDA (race condition): o resultado depende
da ordem imprevisivel de execucao.

EXEMPLO CLASSICO:

    contador = 0

    def incrementar():
        global contador
        for _ in range(100_000):
            contador += 1    # NAO e atomico! sao 3 operacoes: ler, somar, escrever

Por que e um problema? contador += 1 equivale a:
    temp = contador    # thread 1 le 5
    temp = temp + 1    # thread 1 calcula 6
    # thread 2 tambem le 5 e calcula 6 (antes de thread 1 salvar!)
    contador = temp    # thread 1 salva 6
    contador = temp    # thread 2 salva 6 -- sobreescreveu! perdeu um incremento

Com 2 threads fazendo 100.000 incrementos cada, esperamos 200.000.
O resultado real e menor e varia a cada execucao.

SOLUCAO: Lock (mutex)

    lock = threading.Lock()
    contador = 0

    def incrementar_seguro():
        global contador
        for _ in range(100_000):
            with lock:          # adquire o lock
                contador += 1   # so uma thread por vez aqui
                                 # lock liberado ao sair do with

Com Lock, o resultado e sempre 200.000.

Lock garante que apenas uma thread execute o bloco protegido por vez.
O custo: contencao de lock. Se muitas threads brigam pelo mesmo lock,
voce perde o beneficio da concorrencia -- por isso proteja apenas o
minimo necessario (o trecho critico), nao o loop inteiro.

OUTROS PRIMITIVOS DE SINCRONIZACAO:

    threading.RLock()       Lock reentrante (mesma thread pode adquirir varias vezes)
    threading.Event()       sinaliza entre threads (set/wait/clear)
    threading.Semaphore(n)  permite ate n threads simultaneas
    threading.Condition()   wait/notify para comunicacao entre threads

---------------------------------------------------------------------------
5. Queue: comunicacao segura entre threads
---------------------------------------------------------------------------
queue.Queue e uma fila thread-safe: projetada para comunicacao entre
threads sem precisar de locks manuais:

    from queue import Queue
    import threading

    fila = Queue()

    def produtor():
        for i in range(5):
            fila.put(i)       # coloca na fila (thread-safe)
        fila.put(None)        # sentinela: sinaliza "acabou"

    def consumidor():
        while True:
            item = fila.get()        # retira da fila (bloqueia se vazia)
            if item is None:
                break
            print(f"Processando {item}")
            fila.task_done()

O padrao PRODUTOR-CONSUMIDOR desacopla quem gera dados de quem processa,
permitindo que operem em velocidades diferentes. Queue cuida da
sincronizacao automaticamente.

task_done() informa que o item foi processado -- necessario se voce
usar fila.join() para esperar que todos os itens sejam processados.

---------------------------------------------------------------------------
6. multiprocessing: paralelismo real
---------------------------------------------------------------------------
Para tarefas CPU-bound, use multiprocessing. Cada processo tem seu
proprio espaco de memoria e GIL:

    from multiprocessing import Pool

    def calcular(n):
        return sum(range(n))

    if __name__ == '__main__':    # OBRIGATORIO em multiprocessing!
        with Pool(processes=4) as pool:
            resultados = pool.map(calcular, [1_000_000] * 8)
        print(resultados)

POR QUE if __name__ == '__main__' E OBRIGATORIO?
No Windows e em alguns modos do Linux, o modulo multiprocessing importa
o script ao criar novos processos. Sem a guarda, cada processo filho
tentaria criar mais filhos infinitamente (fork bomb).

COMPARTILHANDO ESTADO ENTRE PROCESSOS:
Processos NAO compartilham memoria. Para compartilhar, use:

    from multiprocessing import Value, Manager

    contador = Value('i', 0)    # 'i' = inteiro compartilhado
    with contador.get_lock():
        contador.value += 1

    with Manager() as manager:
        lista = manager.list([1, 2, 3])   # lista compartilhada (mais lenta)

---------------------------------------------------------------------------
7. concurrent.futures: interface de alto nivel
---------------------------------------------------------------------------
concurrent.futures oferece uma interface unificada para threads e
processos, mais simples que threading e multiprocessing diretos:

    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
    import time

    def simular_download(url):
        time.sleep(0.1)
        return f"dados de {url}"

    urls = ["url1", "url2", "url3", "url4", "url5"]

    # ThreadPoolExecutor para I/O-bound
    with ThreadPoolExecutor(max_workers=5) as executor:
        # map: equivalente a map() mas com threads, PRESERVA A ORDEM
        resultados = list(executor.map(simular_download, urls))

        # submit: envia uma tarefa, retorna um Future
        futures = [executor.submit(simular_download, url) for url in urls]
        resultados = [f.result() for f in futures]

    # ProcessPoolExecutor para CPU-bound (mesma interface!)
    with ProcessPoolExecutor(max_workers=4) as executor:
        resultados = list(executor.map(calcular, dados))

FUTURE: representa um resultado que ainda nao esta disponivel.

    future = executor.submit(tarefa)
    future.done()           # True se terminou
    future.result()         # bloqueia ate ter resultado (ou levanta excecao)
    future.cancel()         # tenta cancelar (pode nao funcionar se ja iniciou)
    future.exception()      # a excecao levantada, se houver

AS_COMPLETED: processar resultados na ordem em que terminam:

    from concurrent.futures import as_completed

    futures = {executor.submit(simular_download, url): url for url in urls}
    for future in as_completed(futures):
        url = futures[future]
        resultado = future.result()
        print(f"{url} -> {resultado}")

---------------------------------------------------------------------------
8. Escolhendo a abordagem certa
---------------------------------------------------------------------------

    Situacao                          Recomendacao
    ------------------------------    ----------------------------------
    I/O simples, sequencial           nenhuma concorrencia necessaria
    Multiplos downloads/requests      ThreadPoolExecutor
    Muitas requisicoes de API         asyncio (Dia 28)
    Calculo pesado (multi-nucleo)     ProcessPoolExecutor
    Comunicacao entre threads         Queue (nao variaveis globais)
    Servidor web                      framework (FastAPI, Django)
""",
    exemplos=[
        Exemplo(
            titulo="Threads para I/O: downloads simulados",
            codigo='''import threading
import time
from concurrent.futures import ThreadPoolExecutor

def simular_download(url):
    time.sleep(0.1)    # libera o GIL durante o sleep
    return f"conteudo_de_{url}"

# Sequencial: 5 x 0.1s = 0.5s
inicio = time.perf_counter()
resultados_seq = [simular_download(f"url{i}") for i in range(1, 6)]
tempo_seq = time.perf_counter() - inicio
print(f"Sequencial:  {tempo_seq:.2f}s ({len(resultados_seq)} itens)")

# Com ThreadPoolExecutor: ~0.1s (todas rodam ao mesmo tempo)
inicio = time.perf_counter()
with ThreadPoolExecutor(max_workers=5) as executor:
    resultados_pool = list(executor.map(simular_download,
                                        [f"url{i}" for i in range(1, 6)]))
tempo_pool = time.perf_counter() - inicio
print(f"Com pool:    {tempo_pool:.2f}s ({len(resultados_pool)} itens)")
print(f"Speedup:     {tempo_seq/tempo_pool:.1f}x")

# Threads manuais com Lock protegendo a lista de resultados
resultados_manual = []
lock = threading.Lock()

def baixar(url):
    dado = simular_download(url)
    with lock:
        resultados_manual.append(dado)

inicio = time.perf_counter()
threads = [threading.Thread(target=baixar, args=(f"url{i}",))
           for i in range(1, 6)]
for t in threads: t.start()
for t in threads: t.join()
tempo_manual = time.perf_counter() - inicio
print(f"Manual:      {tempo_manual:.2f}s ({len(resultados_manual)} itens)")
''',
            explicacao="time.sleep() libera o GIL -- e I/O simulado. "
                       "Por isso 5 threads com sleep(0.1) completam em ~0.1s total, "
                       "nao em 0.5s. "
                       "ThreadPoolExecutor com map e mais limpo que threads manuais: "
                       "gerencia o pool, coleta resultados e preserva a ordem. "
                       "O Lock na versao manual protege o append na lista -- "
                       "list.append e thread-safe em CPython, mas o Lock garante "
                       "corretude mesmo em implementacoes diferentes.",
        ),
        Exemplo(
            titulo="Condicao de corrida e Lock na pratica",
            codigo='''import threading

# VERSAO COM BUG: condicao de corrida
contador_bug = [0]

def incrementar_bug(n):
    for _ in range(n):
        contador_bug[0] += 1    # nao e atomico!

threads_bug = [threading.Thread(target=incrementar_bug, args=(10_000,))
               for _ in range(4)]
for t in threads_bug: t.start()
for t in threads_bug: t.join()
print(f"Com bug    (esperado 40000): {contador_bug[0]}")  # provavelmente menor!

# VERSAO CORRETA: protegida por Lock
contador_ok = [0]
lock = threading.Lock()

def incrementar_seguro(n):
    for _ in range(n):
        with lock:
            contador_ok[0] += 1   # so uma thread por vez

threads_ok = [threading.Thread(target=incrementar_seguro, args=(10_000,))
              for _ in range(4)]
for t in threads_ok: t.start()
for t in threads_ok: t.join()
print(f"Com lock   (esperado 40000): {contador_ok[0]}")   # sempre 40000!

# Event: sincronizando o inicio de multiplas threads
evento = threading.Event()

def aguardar_e_rodar(nome):
    print(f"[{nome}] aguardando sinal...")
    evento.wait()    # bloqueia ate evento.set()
    print(f"[{nome}] executando!")

t1 = threading.Thread(target=aguardar_e_rodar, args=("Alpha",))
t2 = threading.Thread(target=aguardar_e_rodar, args=("Beta",))
t1.start(); t2.start()

import time; time.sleep(0.1)
print("Disparando evento para todas as threads...")
evento.set()        # libera todas as threads que estao em wait()
t1.join(); t2.join()
''',
            explicacao="A lista de 1 elemento [0] e usada no lugar de variavel "
                       "global para simplificar o closures -- funciona igual "
                       "mas sem precisar de 'global' ou 'nonlocal'. "
                       "Com 4 threads fazendo 10.000 incrementos, o esperado e "
                       "40.000 -- sem Lock o resultado e menor e varia a cada execucao. "
                       "threading.Event e mais limpo que sleep para sincronizar: "
                       "uma thread sinaliza, todas as que estao em wait() sao liberadas.",
        ),
        Exemplo(
            titulo="Produtor-consumidor com Queue",
            codigo='''import threading
from queue import Queue
import time

def produtor(fila, itens):
    for item in itens:
        print(f"[Produtor] gerando {item}")
        time.sleep(0.05)
        fila.put(item)
    fila.put(None)    # sentinela: sinaliza "acabou"

def consumidor(fila, resultados, lock):
    while True:
        item = fila.get()        # bloqueia se a fila estiver vazia
        if item is None:
            fila.task_done()
            break
        print(f"  [Consumidor] processando {item}")
        time.sleep(0.02)
        with lock:
            resultados.append(item * 2)
        fila.task_done()

fila = Queue(maxsize=3)   # buffer limitado: produtor espera se fila cheia
resultados = []
lock = threading.Lock()

t_prod = threading.Thread(target=produtor, args=(fila, [1, 2, 3, 4, 5]))
t_cons = threading.Thread(target=consumidor, args=(fila, resultados, lock))

t_prod.start()
t_cons.start()
t_prod.join()
t_cons.join()

print(f"Resultados: {sorted(resultados)}")
''',
            explicacao="Queue(maxsize=3) limita o buffer: se a fila tiver 3 itens "
                       "e o consumidor for lento, o produtor bloqueia automaticamente. "
                       "Isso evita que o produtor sobrecarregue a memoria. "
                       "O sentinela None sinaliza o fim da producao -- padrao mais "
                       "limpo que usar eventos ou flags booleanas. "
                       "Queue ja tem sincronizacao interna -- o Lock extra aqui "
                       "protege apenas o append na lista de resultados.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d27e1",
            enunciado=(
                "Os imports ja estao na assinatura.\n"
                "Escreva processar_paralelo(valores) que recebe uma lista\n"
                "de numeros e devolve uma lista com o QUADRADO de cada um,\n"
                "calculado com ThreadPoolExecutor.\n\n"
                "Exemplos:\n"
                "   processar_paralelo([1, 2, 3]) -> [1, 4, 9]\n"
                "   processar_paralelo([])         -> []\n\n"
                "Estrategia:\n"
                "   def quadrado(n):\n"
                "       return n * n\n\n"
                "   with ThreadPoolExecutor() as executor:\n"
                "       return list(executor.map(quadrado, valores))\n\n"
                "Por que ThreadPoolExecutor.map?\n"
                "   - Gerencia o pool de threads automaticamente\n"
                "   - PRESERVA A ORDEM dos resultados (importante!)\n"
                "   - list() e necessario: map retorna um iterador\n\n"
                "Nota: para calculos simples como este, threads nao dao\n"
                "speedup real (e CPU-bound e o GIL limita). O exercicio\n"
                "demonstra a interface do ThreadPoolExecutor, que brilha\n"
                "em tarefas I/O-bound como downloads e chamadas de API."
            ),
            funcao="processar_paralelo",
            assinatura="import time\nfrom concurrent.futures import ThreadPoolExecutor\n\n\ndef processar_paralelo(valores):",
            testes=[
                ("processar_paralelo([1, 2, 3])", "[1, 4, 9]"),
                ("processar_paralelo([])", "[]"),
            ],
            nivel="medio",
            dica="with ThreadPoolExecutor() as executor: return list(executor.map(lambda n: n*n, valores))",
        ),
        Exercicio(
            id="d27e2",
            enunciado=(
                "O import threading ja esta na assinatura.\n"
                "Escreva contar_seguro(n_threads, incrementos) que:\n"
                "   - Cria n_threads threads\n"
                "   - Cada thread incrementa um contador 'incrementos' vezes\n"
                "   - Usa Lock para evitar condicao de corrida\n"
                "   - Retorna o valor final do contador\n\n"
                "Exemplos:\n"
                "   contar_seguro(4, 10000) -> 40000  (sempre!)\n"
                "   contar_seguro(1, 5)     -> 5\n"
                "   contar_seguro(0, 100)   -> 0  (sem threads, contador = 0)\n\n"
                "Estrategia com lista de 1 elemento (evita nonlocal):\n"
                "   contador = [0]\n"
                "   lock = threading.Lock()\n\n"
                "   def incrementar():\n"
                "       for _ in range(incrementos):\n"
                "           with lock:\n"
                "               contador[0] += 1\n\n"
                "   threads = [threading.Thread(target=incrementar)\n"
                "              for _ in range(n_threads)]\n"
                "   for t in threads: t.start()\n"
                "   for t in threads: t.join()\n"
                "   return contador[0]\n\n"
                "Por que lista [0] em vez de variavel inteira?\n"
                "Inteiros sao imutaveis: dentro da funcao interna, fazer\n"
                "'contador += 1' criaria uma variavel LOCAL, nao alterando\n"
                "o contador externo. Ja 'contador[0] += 1' muta a lista,\n"
                "que e mutavel e acessivel pelo closure sem nonlocal."
            ),
            funcao="contar_seguro",
            assinatura="import threading\n\n\ndef contar_seguro(n_threads, incrementos):",
            testes=[
                ("contar_seguro(4, 10000)", "40000"),
                ("contar_seguro(1, 5)", "5"),
                ("contar_seguro(0, 100)", "0"),
            ],
            nivel="dificil",
            dica="contador=[0]; lock=threading.Lock(); def inc(): [with lock: contador[0]+=1 for _ in range(incrementos)]; threads=[Thread(target=inc) for _ in range(n_threads)]; start/join todos; return contador[0]",
        ),
        Exercicio(
            id="d27e3",
            enunciado=(
                "Os imports ja estao na assinatura.\n"
                "Escreva produtor_consumidor(itens) que:\n"
                "   - Cria uma Queue compartilhada\n"
                "   - Thread PRODUTORA: coloca cada item na fila\n"
                "     e ao terminar coloca None (sentinela)\n"
                "   - Thread CONSUMIDORA: retira itens da fila e\n"
                "     acumula a SOMA; para ao ver None\n"
                "   - Retorna a soma de todos os itens\n\n"
                "Exemplos:\n"
                "   produtor_consumidor([1, 2, 3, 4]) -> 10\n"
                "   produtor_consumidor([])            -> 0\n\n"
                "Estrutura:\n"
                "   fila = Queue()\n"
                "   total = [0]\n\n"
                "   def produtor():\n"
                "       for item in itens: fila.put(item)\n"
                "       fila.put(None)   # sentinela de fim\n\n"
                "   def consumidor():\n"
                "       while True:\n"
                "           item = fila.get()\n"
                "           if item is None: break\n"
                "           total[0] += item\n\n"
                "   t_p = Thread(target=produtor)\n"
                "   t_c = Thread(target=consumidor)\n"
                "   t_p.start(); t_c.start()\n"
                "   t_p.join();  t_c.join()\n"
                "   return total[0]\n\n"
                "O sentinela None e o sinal de 'acabou' -- o consumidor\n"
                "para o loop ao receber None em vez de um item real.\n"
                "Queue.get() bloqueia automaticamente se a fila estiver\n"
                "vazia, entao o consumidor espera o produtor sem busy-wait."
            ),
            funcao="produtor_consumidor",
            assinatura="import threading\nfrom queue import Queue\n\n\ndef produtor_consumidor(itens):",
            testes=[
                ("produtor_consumidor([1, 2, 3, 4])", "10"),
                ("produtor_consumidor([])", "0"),
            ],
            nivel="dificil",
            dica="fila=Queue(); total=[0]; def prod(): [fila.put(i) for i in itens]; fila.put(None); def cons(): while True: i=fila.get(); if i is None: break; total[0]+=i; Thread(prod)+Thread(cons); join; return total[0]",
        ),
    ],
    quiz=[
        Quiz(
            "Por que threads Python nao aceleram tarefas CPU-bound?",
            ["Threads sao mais lentas que processos em Python",
             "O GIL garante que apenas uma thread execute bytecode Python por vez, entao multiplas threads se revezam em vez de rodar em paralelo",
             "Python nao suporta threads para calculos matematicos",
             "Threads so funcionam para operacoes de string"],
            1,
            "O GIL (Global Interpreter Lock) e um mutex dentro do CPython que "
            "protege a contagem de referencias do gerenciador de memoria. "
            "Para tarefas I/O-bound threads funcionam porque o GIL e liberado "
            "durante a espera de I/O. "
            "Para CPU-bound use ProcessPoolExecutor: cada processo tem seu "
            "proprio GIL e rodam em nucleos diferentes.",
        ),
        Quiz(
            "O que acontece sem Lock ao incrementar um contador com multiplas threads?",
            ["O contador e incrementado corretamente pois Python e thread-safe",
             "Ocorre condicao de corrida: threads podem ler o mesmo valor e sobrescrever o incremento da outra, resultando em contagem menor que o esperado",
             "Uma excecao RuntimeError e levantada automaticamente",
             "O programa trava em deadlock"],
            1,
            "contador += 1 nao e atomico: sao 3 operacoes (ler, somar, escrever). "
            "Thread 1 le contador=5, Thread 2 le contador=5, "
            "Thread 1 escreve 6, Thread 2 escreve 6 -- perdeu um incremento! "
            "Lock garante que apenas uma thread execute o bloco critico por vez.",
        ),
        Quiz(
            "Qual a vantagem de Queue sobre variaveis compartilhadas com Lock?",
            ["Queue e mais rapida que Lock",
             "Queue gerencia a sincronizacao internamente, eliminando locks manuais e implementando bloqueio automatico se vazia ou cheia",
             "Queue nao requer threads -- funciona com processos tambem",
             "Queue permite compartilhar funcoes entre threads"],
            1,
            "Queue e thread-safe por design: put() e get() ja tem sincronizacao "
            "interna. Voce nao precisa de locks manuais. "
            "Queue(maxsize=N) automaticamente bloqueia o produtor se a fila "
            "estiver cheia e bloqueia o consumidor se estiver vazia. "
            "O resultado e codigo mais limpo e menos propenso a deadlocks.",
        ),
        Quiz(
            "Por que 'if __name__ == \"__main__\"' e obrigatorio com multiprocessing?",
            ["E apenas convencao -- o codigo funciona sem ela",
             "Ao criar processos filhos, o modulo multiprocessing importa o script principal; sem a guarda, cada filho tentaria criar mais filhos infinitamente",
             "multiprocessing nao funciona no Linux sem essa linha",
             "E necessario apenas no Windows, nao no Linux"],
            1,
            "No Windows e em alguns modos no Linux, novos processos sao criados "
            "importando o modulo principal. Sem a guarda, o codigo de criacao "
            "de processos executaria em cada filho, que criaria mais filhos -- "
            "um fork bomb. "
            "No Linux com fork o problema e menos grave, mas a guarda "
            "e boa pratica universal.",
        ),
    ],
    projeto=(
        "Crie baixador_paralelo.py que demonstre threads vs sequencial:\n\n"
        "   def simular_download(url, delay=0.1):\n"
        "       time.sleep(delay)\n"
        "       return f'dados de {url} ({len(url)} bytes)'\n\n"
        "   1. SEQUENCIAL: baixa 10 URLs uma por uma, mede o tempo\n\n"
        "   2. THREADPOOLEXECUTOR: mesmas 10 URLs com executor.map\n"
        "      - Compare o tempo com o sequencial\n\n"
        "   3. AS_COMPLETED: processa na ordem de conclusao\n"
        "      - Use futures = {executor.submit(f, url): url for url in urls}\n"
        "      - Exibe cada resultado assim que termina\n\n"
        "   4. PRODUTOR-CONSUMIDOR:\n"
        "      - 1 thread produtora coloca URLs na Queue\n"
        "      - 3 threads consumidoras processam as URLs\n"
        "      - Use sentinelas para sinalizar fim (um por consumidor)\n\n"
        "   RELATORIO FINAL:\n"
        "   Metodo               Tempo    Speedup\n"
        "   ------------------   ------   -------\n"
        "   Sequencial           1.00s    1.0x\n"
        "   ThreadPoolExecutor   0.11s    9.1x\n"
        "   Prod-consumidor      0.11s    9.1x\n\n"
        "BONUS: adicione tratamento de erros -- simule falhas aleatorias\n"
        "em alguns downloads e use future.exception() para detecta-las."
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/threading.html -- threading",
        "docs.python.org/pt-br/3/library/concurrent.futures.html -- concurrent.futures",
        "docs.python.org/pt-br/3/library/queue.html -- Queue thread-safe",
        "PEP 703 -- Making the GIL Optional in CPython",
    ],
))

# ---------------------------------------------------------------- DIA 28
DIAS.append(Dia(
    numero=28,
    titulo="Programacao assincrona com asyncio",
    nivel="Avancado",
    duracao="120 min",
    objetivos=[
        "Entender a diferenca entre concorrencia com threads e concorrencia com asyncio",
        "Compreender o event loop, corrotinas e o que await realmente faz",
        "Escrever e executar corrotinas com async def, await e asyncio.run",
        "Executar multiplas corrotinas em paralelo com asyncio.gather",
        "Usar asyncio.wait_for para impor limites de tempo",
        "Reconhecer quando asyncio e melhor que threads e quando nao e",
    ],
    teoria="""
No Dia 27 voce aprendeu a usar threads para executar tarefas de forma
concorrente. asyncio e uma segunda abordagem para o mesmo problema --
mas com uma filosofia completamente diferente.

---------------------------------------------------------------------------
1. Threads versus asyncio: duas formas de concorrencia
---------------------------------------------------------------------------
Ambas as abordagens resolvem o problema de I/O-bound: nao desperdicar
tempo de CPU esperando a rede ou o disco. Mas a forma como fazem isso
e muito diferente:

THREADS (concorrencia preemptiva):
    O sistema operacional decide quando trocar de thread -- a thread nao
    tem controle. Pode ser interrompida a qualquer momento.
    Exige Lock para proteger dados compartilhados.
    Mais simples de entender inicialmente.
    Funciona com bibliotecas sincronas existentes (requests, psycopg2...).

ASYNCIO (concorrencia cooperativa):
    A corrotina decide quando ceder o controle, usando await.
    So uma corrotina executa por vez, mas troca voluntariamente.
    NAO exige Lock para dados compartilhados (nao ha troca involuntaria).
    Exige bibliotecas async (aiohttp, asyncpg...) -- nao funciona com
    bibliotecas sincronas.
    Mais eficiente para grande volume de conexoes simultaneas (milhares).

QUANDO USAR CADA UM:

    Situacao                         Recomendacao
    ----------------------------     ---------------------------------
    Poucas tarefas I/O (< 100)       threads (mais simples)
    Muitas conexoes simultaneas      asyncio (mais eficiente)
    Codigo legado com libs sincronas  threads
    Novo projeto com suporte async    asyncio
    CPU-bound                         multiprocessing (ambos falham)

---------------------------------------------------------------------------
2. O event loop: o coracao do asyncio
---------------------------------------------------------------------------
O event loop e um loop que:
    1. Pega a proxima corrotina pronta para executar
    2. Executa ate ela fazer await (ceder o controle)
    3. Enquanto essa corrotina espera, executa outra
    4. Quando o I/O termina, volta a executar a corrotina original

E como um gerente que distribui trabalho: quando um funcionario para
para esperar uma resposta, o gerente passa a tarefa para outro funcionario
e volta ao primeiro quando a resposta chegar.

asyncio.run(corrotina) cria o event loop, executa a corrotina ate o
fim e encerra o loop. E a forma padrao de iniciar um programa asyncio:

    import asyncio

    async def principal():
        print("iniciando")
        await asyncio.sleep(1)    # cede o controle por 1 segundo
        print("terminando")

    asyncio.run(principal())

---------------------------------------------------------------------------
3. async def e await: a sintaxe central
---------------------------------------------------------------------------
async def define uma CORROTINA -- uma funcao que pode ser pausada:

    async def buscar_dados(url):
        # ... codigo assincrono ...
        return dados

Chamar uma corrotina NAO a executa -- cria um objeto corrotina:

    resultado = buscar_dados("http://api.com")   # nao executou nada!
    resultado = await buscar_dados("http://api.com")   # executa e espera

await so pode ser usado DENTRO de uma funcao async def.
await faz duas coisas:
    1. Executa a corrotina (ou aguarda o awaitable)
    2. CEDE O CONTROLE ao event loop enquanto espera

    async def exemplo():
        print("antes do await")
        resultado = await alguma_operacao_lenta()  # cede aqui
        print("depois do await")                    # retoma aqui
        return resultado

O ponto crucial: enquanto exemplo() esta "esperando" em await, o event
loop pode executar OUTRAS corrotinas. Isso e a concorrencia do asyncio.

AWAITABLES: o que pode ser usado com await:
    - Corrotinas (async def)
    - asyncio.Future
    - asyncio.Task
    - Qualquer objeto com __await__

---------------------------------------------------------------------------
4. asyncio.sleep: o I/O simulado
---------------------------------------------------------------------------
asyncio.sleep(n) e o equivalente assincrono de time.sleep(n):

    time.sleep(1)           # BLOQUEIA a thread inteira por 1 segundo
    await asyncio.sleep(1)  # CEDE o controle por 1 segundo (nao bloqueia)

A diferenca e critica: time.sleep dentro de uma corrotina bloqueia o
event loop inteiro -- nenhuma outra corrotina executa durante esse tempo.
asyncio.sleep cede o controle para que outras corrotinas possam rodar.

    # ERRADO: bloqueia o event loop
    async def tarefa_errada():
        time.sleep(1)    # bloqueia TUDO

    # CORRETO: cede o controle
    async def tarefa_certa():
        await asyncio.sleep(1)   # outras corrotinas rodam enquanto espera

A regra: dentro de corrotinas, nunca use funcoes bloqueantes (time.sleep,
requests.get, open em modo padrao). Use sempre as versoes async.

---------------------------------------------------------------------------
5. asyncio.gather: executando multiplas corrotinas em paralelo
---------------------------------------------------------------------------
asyncio.gather executa multiplas corrotinas e aguarda TODAS terminarem:

    import asyncio

    async def buscar(url):
        await asyncio.sleep(0.1)   # simula download
        return f"dados de {url}"

    async def principal():
        # Executa as 3 simultaneamente, nao uma por vez!
        resultados = await asyncio.gather(
            buscar("url1"),
            buscar("url2"),
            buscar("url3"),
        )
        print(resultados)   # ['dados de url1', 'dados de url2', 'dados de url3']

    asyncio.run(principal())

gather retorna uma lista com os resultados NA MESMA ORDEM das corrotinas
passadas -- mesmo que algumas terminem antes de outras.

PASSANDO UMA LISTA DINAMICA:

    corrotinas = [buscar(f"url{i}") for i in range(10)]
    resultados = await asyncio.gather(*corrotinas)   # desempacota a lista

TRATANDO ERROS EM GATHER:

    # Por padrao: se uma corrotina levantar excecao, gather propaga
    # Com return_exceptions=True: erros viram resultados normais
    resultados = await asyncio.gather(
        corrotina1(),
        corrotina2(),
        return_exceptions=True,
    )
    for r in resultados:
        if isinstance(r, Exception):
            print(f"Erro: {r}")
        else:
            print(f"OK: {r}")

---------------------------------------------------------------------------
6. asyncio.create_task: executando sem esperar
---------------------------------------------------------------------------
asyncio.gather espera todas as corrotinas de uma vez. create_task permite
iniciar uma corrotina "em background" e continuar executando outras coisas:

    async def principal():
        task1 = asyncio.create_task(buscar("url1"))   # inicia agora
        task2 = asyncio.create_task(buscar("url2"))   # inicia agora

        # Faz outras coisas enquanto as tasks rodam
        await asyncio.sleep(0)   # cede o controle (deixa as tasks progredir)

        resultado1 = await task1   # espera task1
        resultado2 = await task2   # espera task2

Tasks sao como "threads asyncio" -- uma vez criadas, rodam de forma
independente no event loop. gather e uma forma conveniente de criar
e esperar multiplas tasks de uma vez.

---------------------------------------------------------------------------
7. asyncio.wait_for: impondo limites de tempo
---------------------------------------------------------------------------
wait_for executa uma corrotina com um limite de tempo:

    async def operacao_lenta():
        await asyncio.sleep(10)
        return "resultado"

    async def principal():
        try:
            resultado = await asyncio.wait_for(
                operacao_lenta(),
                timeout=2.0     # cancela se nao terminar em 2 segundos
            )
            print("OK:", resultado)
        except asyncio.TimeoutError:
            print("Timeout! operacao muito lenta")

Se o timeout estourar, asyncio.TimeoutError e levantada e a corrotina
interna e cancelada automaticamente. Muito util para chamadas de rede
onde o servidor pode nao responder.

---------------------------------------------------------------------------
8. asyncio.Queue: comunicacao entre corrotinas
---------------------------------------------------------------------------
Assim como queue.Queue para threads, asyncio.Queue e thread-safe para
corrotinas:

    async def produtor(fila):
        for i in range(5):
            await fila.put(i)
            await asyncio.sleep(0.01)
        await fila.put(None)   # sentinela

    async def consumidor(fila):
        while True:
            item = await fila.get()
            if item is None:
                break
            print(f"Processando {item}")
            fila.task_done()

    async def principal():
        fila = asyncio.Queue()
        await asyncio.gather(
            produtor(fila),
            consumidor(fila),
        )

---------------------------------------------------------------------------
9. Integrando asyncio com codigo sincrono
---------------------------------------------------------------------------
asyncio.run() e a ponte entre codigo sincrono e assincrono:

    # Codigo sincrono chamando asyncio:
    def funcao_sincrona(x):
        return asyncio.run(corrotina_assincrona(x))

    # Corrotina chamando codigo sincrono (nao bloqueante):
    async def corrotina():
        resultado = await asyncio.to_thread(funcao_bloqueante, args)
        # to_thread executa a funcao em uma thread separada para nao
        # bloquear o event loop

asyncio.to_thread e util para integrar bibliotecas sincronas (como
requests) em codigo asyncio sem bloquear o event loop.
""",
    exemplos=[
        Exemplo(
            titulo="Corrotinas basicas: do sequencial ao concorrente",
            codigo='''import asyncio
import time

async def simular_download(url, delay):
    print(f"[inicio] {url}")
    await asyncio.sleep(delay)    # cede o controle aqui
    print(f"[fim]    {url}")
    return f"dados de {url}"

# SEQUENCIAL: await um por vez
async def sequencial():
    inicio = time.perf_counter()
    r1 = await simular_download("url1", 0.3)
    r2 = await simular_download("url2", 0.2)
    r3 = await simular_download("url3", 0.1)
    tempo = time.perf_counter() - inicio
    print(f"Sequencial: {tempo:.2f}s -> {[r1, r2, r3]}")

# CONCORRENTE: gather executa todas ao mesmo tempo
async def concorrente():
    inicio = time.perf_counter()
    resultados = await asyncio.gather(
        simular_download("url1", 0.3),
        simular_download("url2", 0.2),
        simular_download("url3", 0.1),
    )
    tempo = time.perf_counter() - inicio
    print(f"Concorrente: {tempo:.2f}s -> {resultados}")

print("=== SEQUENCIAL (0.6s esperado) ===")
asyncio.run(sequencial())

print("\n=== CONCORRENTE (0.3s esperado) ===")
asyncio.run(concorrente())
''',
            explicacao="await um por um e sequencial: 0.3 + 0.2 + 0.1 = 0.6s. "
                       "gather executa todas ao mesmo tempo: o maior delay domina = 0.3s. "
                       "Repare na ordem da saida do modo concorrente: url3 termina "
                       "antes de url1, mas os resultados de gather preservam a ordem "
                       "original -- independente de qual terminou primeiro.",
        ),
        Exemplo(
            titulo="Tasks, timeouts e tratamento de erros",
            codigo='''import asyncio

async def operacao(nome, delay, falhar=False):
    await asyncio.sleep(delay)
    if falhar:
        raise ValueError(f"{nome}: falhou apos {delay}s")
    return f"{nome}: ok ({delay}s)"

# TASKS: iniciar e esperar separadamente
async def exemplo_tasks():
    t1 = asyncio.create_task(operacao("A", 0.1))
    t2 = asyncio.create_task(operacao("B", 0.2))

    # Faz outra coisa enquanto as tasks rodam
    await asyncio.sleep(0.05)
    print("Tasks em andamento...")

    r1 = await t1
    r2 = await t2
    print(r1, r2)

asyncio.run(exemplo_tasks())

# TIMEOUT: limitando o tempo de espera
async def com_timeout():
    try:
        resultado = await asyncio.wait_for(
            operacao("lenta", 2.0),
            timeout=0.5
        )
        print("OK:", resultado)
    except asyncio.TimeoutError:
        print("Timeout! operacao cancelada.")

asyncio.run(com_timeout())

# GATHER COM ERROS: capturando excecoes individualmente
async def com_erros():
    resultados = await asyncio.gather(
        operacao("ok1",   0.1),
        operacao("falha", 0.1, falhar=True),
        operacao("ok2",   0.1),
        return_exceptions=True,
    )
    for r in resultados:
        if isinstance(r, Exception):
            print(f"  ERRO: {r}")
        else:
            print(f"  OK: {r}")

asyncio.run(com_erros())
''',
            explicacao="create_task inicia a corrotina imediatamente -- ela ja "
                       "comeca a rodar quando voce faz await asyncio.sleep(0.05). "
                       "wait_for cancela a corrotina se ela nao terminar no tempo. "
                       "return_exceptions=True e essencial em producao: sem ele, "
                       "a primeira excecao cancela todas as outras corrotinas "
                       "do gather e propaga o erro.",
        ),
        Exemplo(
            titulo="Padrao produtor-consumidor assincrono",
            codigo='''import asyncio
import time

async def produtor(fila, itens):
    for item in itens:
        print(f"  [prod] colocando {item}")
        await fila.put(item)
        await asyncio.sleep(0.02)   # simula producao lenta
    await fila.put(None)            # sentinela

async def consumidor(fila, nome, resultados):
    while True:
        item = await fila.get()     # bloqueia cooperativamente se vazia
        if item is None:
            fila.task_done()
            break
        print(f"  [{nome}] processando {item}")
        await asyncio.sleep(0.05)   # simula processamento
        resultados.append(item * 2)
        fila.task_done()

async def principal():
    fila = asyncio.Queue(maxsize=3)
    resultados = []

    inicio = time.perf_counter()
    await asyncio.gather(
        produtor(fila, [1, 2, 3, 4, 5]),
        consumidor(fila, "C1", resultados),
    )
    print(f"Tempo: {time.perf_counter()-inicio:.2f}s")
    print(f"Resultados: {sorted(resultados)}")

asyncio.run(principal())
''',
            explicacao="asyncio.Queue funciona como queue.Queue mas com "
                       "versoes assincronas: await fila.put() e await fila.get(). "
                       "maxsize=3 limita o buffer: se cheia, put() cede o controle "
                       "ate o consumidor retirar um item. "
                       "task_done() e importante se voce usar fila.join() para "
                       "esperar que todos os itens sejam processados.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d28e1",
            enunciado=(
                "Os imports e a estrutura ja estao na assinatura.\n"
                "Complete duas partes:\n\n"
                "1. async def dobrar(x): deve retornar x * 2\n\n"
                "2. def executar(x): funcao SINCRONA que executa\n"
                "   a corrotina dobrar(x) e retorna o resultado\n\n"
                "Exemplos:\n"
                "   executar(5)  -> 10\n"
                "   executar(0)  -> 0\n"
                "   asyncio.iscoroutinefunction(dobrar) -> True\n\n"
                "O terceiro teste verifica que dobrar e de fato uma\n"
                "corrotina (definida com async def).\n\n"
                "Estrategia de executar:\n"
                "   return asyncio.run(dobrar(x))\n\n"
                "asyncio.run() e a ponte entre codigo sincrono e\n"
                "assincrono: cria o event loop, executa a corrotina\n"
                "ate o fim, fecha o loop e retorna o resultado.\n\n"
                "dobrar(x) sozinho nao executa nada -- cria um objeto\n"
                "corrotina. So asyncio.run() ou await realmente executam."
            ),
            funcao="executar",
            assinatura="import asyncio\n\n\nasync def dobrar(x):\n    ...\n\n\ndef executar(x):",
            testes=[
                ("executar(5)", "10"),
                ("executar(0)", "0"),
                ("asyncio.iscoroutinefunction(dobrar)", "True"),
            ],
            dica="async def dobrar(x): return x * 2. def executar(x): return asyncio.run(dobrar(x))",
        ),
        Exercicio(
            id="d28e2",
            enunciado=(
                "Os imports e a corrotina dobrar ja estao na assinatura.\n"
                "Escreva def executar_todos(valores) que executa dobrar()\n"
                "para cada valor em paralelo e retorna a lista de resultados.\n\n"
                "Exemplos:\n"
                "   executar_todos([1, 2, 3]) -> [2, 4, 6]\n"
                "   executar_todos([])         -> []\n\n"
                "Estrategia:\n"
                "   async def principal():\n"
                "       return await asyncio.gather(\n"
                "           *[dobrar(v) for v in valores]\n"
                "       )\n\n"
                "   return asyncio.run(principal())\n\n"
                "Por que gather em vez de varios await separados?\n"
                "   await dobrar(1) -> await dobrar(2) -> await dobrar(3)\n"
                "   Isso e SEQUENCIAL: espera cada um antes do proximo.\n\n"
                "   gather(dobrar(1), dobrar(2), dobrar(3))\n"
                "   Isso e CONCORRENTE: todas rodam ao mesmo tempo.\n\n"
                "O * desempacota a lista em argumentos separados:\n"
                "   gather(*[dobrar(1), dobrar(2)]) == gather(dobrar(1), dobrar(2))"
            ),
            funcao="executar_todos",
            assinatura="import asyncio\n\n\nasync def dobrar(x):\n    await asyncio.sleep(0)\n    return x * 2\n\n\ndef executar_todos(valores):",
            testes=[
                ("executar_todos([1, 2, 3])", "[2, 4, 6]"),
                ("executar_todos([])", "[]"),
            ],
            nivel="medio",
            dica="async def principal(): return await asyncio.gather(*[dobrar(v) for v in valores]); return asyncio.run(principal())",
        ),
        Exercicio(
            id="d28e3",
            enunciado=(
                "O import asyncio ja esta na assinatura.\n"
                "Escreva def com_timeout(segundos, limite) que:\n"
                "   - Cria uma corrotina que dorme 'segundos'\n"
                "   - Tenta executa-la com timeout de 'limite' segundos\n"
                "   - Retorna 'ok' se terminar a tempo\n"
                "   - Retorna 'timeout' se o limite for estourado\n\n"
                "Exemplos:\n"
                "   com_timeout(0.01, 1)    -> 'ok'      (0.01s < 1s limite)\n"
                "   com_timeout(1, 0.01)    -> 'timeout' (1s > 0.01s limite)\n\n"
                "Estrategia:\n"
                "   async def principal():\n"
                "       try:\n"
                "           await asyncio.wait_for(\n"
                "               asyncio.sleep(segundos),\n"
                "               timeout=limite\n"
                "           )\n"
                "           return 'ok'\n"
                "       except asyncio.TimeoutError:\n"
                "           return 'timeout'\n\n"
                "   return asyncio.run(principal())\n\n"
                "asyncio.wait_for cancela a corrotina automaticamente\n"
                "quando o timeout estoura e levanta asyncio.TimeoutError.\n"
                "Em Python 3.11+ TimeoutError (sem prefixo) tambem funciona."
            ),
            funcao="com_timeout",
            assinatura="import asyncio\n\n\ndef com_timeout(segundos, limite):",
            testes=[
                ("com_timeout(0.01, 1)", "'ok'"),
                ("com_timeout(1, 0.01)", "'timeout'"),
            ],
            nivel="dificil",
            dica="async def principal(): try: await asyncio.wait_for(asyncio.sleep(segundos), timeout=limite); return 'ok'; except asyncio.TimeoutError: return 'timeout'; return asyncio.run(principal())",
        ),
    ],
    quiz=[
        Quiz(
            "Qual a diferenca fundamental entre threads e asyncio para concorrencia?",
            ["asyncio e sempre mais rapido que threads",
             "Threads sao preemptivas (o SO decide quando trocar); asyncio e cooperativo (a corrotina decide quando ceder com await)",
             "asyncio funciona com qualquer biblioteca; threads so com bibliotecas especiais",
             "Threads usam multiplos nucleos; asyncio usa apenas um"],
            1,
            "Threads: o sistema operacional pode interromper a thread a qualquer "
            "momento -- por isso precisam de Lock para dados compartilhados. "
            "asyncio: a corrotina so cede o controle em um await -- entao voce "
            "sabe exatamente onde a troca ocorre e nao precisa de Lock. "
            "Essa previsibilidade torna asyncio menos propenso a race conditions.",
        ),
        Quiz(
            "O que acontece quando voce chama uma corrotina sem await?",
            ["A corrotina executa normalmente e retorna o resultado",
             "Um objeto corrotina e criado mas NADA e executado -- voce obtem um aviso 'coroutine was never awaited'",
             "Python levanta TypeError imediatamente",
             "A corrotina executa em background automaticamente"],
            1,
            "async def f(): return 42 -- f() nao executa nada. "
            "Cria apenas um objeto corrotina, como uma receita que nao foi cozinhada. "
            "Para executar: await f() (dentro de async def) ou asyncio.run(f()). "
            "Python 3.x avisa 'RuntimeWarning: coroutine was never awaited' "
            "se o objeto for descartado sem ser executado.",
        ),
        Quiz(
            "Qual a diferenca entre asyncio.gather e criar tasks sequenciais com await?",
            ["Nao ha diferenca -- os dois executam na mesma ordem",
             "gather executa todas as corrotinas CONCORRENTEMENTE; await sequencial espera cada uma terminar antes de comecar a proxima",
             "gather e mais lento que await sequencial",
             "Tasks so funcionam dentro de gather"],
            1,
            "await c1(); await c2(); await c3() -- sequencial: 0.3+0.2+0.1 = 0.6s. "
            "await gather(c1(), c2(), c3()) -- concorrente: max(0.3, 0.2, 0.1) = 0.3s. "
            "gather deixa todas rodarem ao mesmo tempo, trocando entre elas "
            "a cada await interno. Os resultados sao retornados na ordem original.",
        ),
        Quiz(
            "Por que time.sleep() dentro de uma corrotina e um problema?",
            ["time.sleep nao funciona dentro de funcoes async",
             "time.sleep bloqueia a thread inteira -- o event loop para completamente e nenhuma outra corrotina executa durante o sleep",
             "time.sleep e mais lento que asyncio.sleep",
             "Nao e um problema -- funciona normalmente"],
            1,
            "asyncio roda em uma thread. time.sleep(1) bloqueia essa thread "
            "por 1 segundo -- o event loop nao pode executar nenhuma outra "
            "corrotina durante esse tempo. "
            "asyncio.sleep(1) cede o controle: o event loop executa outras "
            "corrotinas enquanto aguarda. "
            "Regra: dentro de corrotinas, nunca use funcoes bloqueantes. "
            "Use sempre versoes async (asyncio.sleep, aiohttp, asyncpg...).",
        ),
    ],
    projeto=(
        "Crie cliente_assincrono.py que simula um cliente de API assincrono:\n\n"
        "   async def buscar_usuario(id, delay=0.1):\n"
        "       await asyncio.sleep(delay)   # simula latencia de rede\n"
        "       return {'id': id, 'nome': f'User{id}', 'ativo': id % 2 == 0}\n\n"
        "   async def buscar_posts(user_id, delay=0.2):\n"
        "       await asyncio.sleep(delay)\n"
        "       return [{'titulo': f'Post {i} de {user_id}'} for i in range(3)]\n\n"
        "   1. SEQUENCIAL: busca 5 usuarios um por vez, mede o tempo\n\n"
        "   2. PARALELO: busca os 5 usuarios com gather, mede o tempo\n\n"
        "   3. ANINHADO: para cada usuario, busca tambem seus posts\n"
        "      usando gather para paralelizar as buscas de posts\n\n"
        "   4. COM TIMEOUT: busca com limite de 0.15s por usuario\n"
        "      Usuarios com delay > 0.15s retornam None no resultado\n\n"
        "   5. COM ERROS: alguns usuarios lancam excecao aleatoriamente\n"
        "      Use return_exceptions=True e separe erros de sucessos\n\n"
        "   RELATORIO:\n"
        "   Metodo        Tempo    Usuarios OK\n"
        "   -----------   ------   -----------\n"
        "   Sequencial    0.50s    5\n"
        "   Paralelo      0.10s    5\n"
        "   Com timeout   0.15s    3\n\n"
        "BONUS: adicione asyncio.Queue para um produtor que gera IDs\n"
        "e N consumidores que buscam os dados em paralelo."
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/asyncio.html -- asyncio completo",
        "docs.python.org/pt-br/3/library/asyncio-task.html -- corrotinas e tasks",
        "PEP 492 -- Coroutines with async and await syntax",
    ],
))
# ---------------------------------------------------------------- DIA 29
DIAS.append(Dia(
    numero=29,
    titulo="Desempenho: complexidade, medicao e otimizacao",
    nivel="Avancado",
    duracao="110 min",
    objetivos=[
        "Entender notacao O e prever como o tempo de execucao cresce com o tamanho da entrada",
        "Medir desempenho com timeit, time e cProfile para encontrar gargalos reais",
        "Conhecer o custo das operacoes mais comuns de lista, dict e set",
        "Aplicar otimizacoes classicas: memoizacao, estruturas certas e geradores",
        "Saber quando otimizar e quando nao otimizar",
        "Usar collections.Counter, deque e heapq como alternativas mais eficientes",
    ],
    teoria="""
Codigo correto e a primeira prioridade. Codigo eficiente vem depois --
e so quando necessario. Donald Knuth disse: "premature optimization is
the root of all evil" (otimizacao prematura e a raiz de todo o mal).
Isso significa: primeiro faca funcionar, depois meca, depois otimize
apenas o que as medicoes mostram ser um problema real.

---------------------------------------------------------------------------
1. Notacao O: como o tempo cresce com o tamanho da entrada
---------------------------------------------------------------------------
A notacao O (leia "O grande") descreve como o tempo de execucao ou uso
de memoria cresce quando o tamanho da entrada (n) aumenta. Ela ignora
constantes e se concentra no comportamento assintotic -- o que domina
quando n fica muito grande.

    Notacao     Nome             Exemplo concreto
    --------    ---------------  ----------------------------------------
    O(1)        Constante        lista[i], dict[chave], set add/remove
    O(log n)    Logaritmico      busca binaria, heappush/heappop
    O(n)        Linear           percorrer lista, busca linear
    O(n log n)  Linearitimico   sort(), sorted(), merge sort
    O(n^2)      Quadratico       dois loops aninhados, bubble sort
    O(2^n)      Exponencial      fibonacci recursivo sem cache
    O(n!)       Fatorial         permutacoes de n elementos

Como ler na pratica:

    n = 1.000 elementos

    O(1):      1 operacao    -- sempre instantaneo
    O(log n):  10 operacoes  -- muito rapido
    O(n):      1.000         -- rapido
    O(n log n): 10.000       -- aceitavel
    O(n^2):    1.000.000     -- pode ficar lento
    O(2^n):    10^300        -- impraticavel

O impacto de escolher a estrutura errada:

    lista = list(range(1_000_000))
    busca_lista = 999_999 in lista      # O(n): percorre ate 1M elementos
    conjunto = set(lista)
    busca_set = 999_999 in conjunto     # O(1): calculo de hash direto

    Para n=1.000.000, busca em lista pode ser 1.000.000x mais lenta
    do que busca em set para o pior caso.

---------------------------------------------------------------------------
2. Custo das operacoes mais comuns
---------------------------------------------------------------------------
Conhecer o custo de cada operacao permite escolher a estrutura certa:

LISTA:

    Operacao              Custo    Motivo
    -------------------   ------   ----------------------------------------
    lista[i]              O(1)     acesso direto por indice de memoria
    lista.append(x)       O(1)     adiciona no final sem mover nada
    lista.pop()           O(1)     remove do final sem mover nada
    lista.insert(0, x)    O(n)     empurra todos os elementos uma posicao
    lista.pop(0)          O(n)     desloca todos os elementos uma posicao
    x in lista            O(n)     percorre ate encontrar (ou nao)
    lista.sort()          O(n log n) algoritmo Timsort
    len(lista)            O(1)     Python guarda o tamanho separado

DICIONARIO E SET (baseados em tabela hash):

    Operacao              Custo    Notas
    -------------------   ------   ----------------------------------------
    dict[chave]           O(1)     caso medio; O(n) pior caso (raro)
    chave in dict         O(1)     muito mais rapido que in lista
    dict[chave] = valor   O(1)
    del dict[chave]       O(1)
    x in set              O(1)
    set.add(x)            O(1)
    set1 & set2           O(min(len(s1), len(s2)))

Para insercao e remocao frequente no INICIO de uma sequencia,
use collections.deque em vez de lista:

    from collections import deque
    d = deque([1, 2, 3])
    d.appendleft(0)    # O(1) -- lista.insert(0, x) seria O(n)
    d.popleft()        # O(1) -- lista.pop(0) seria O(n)

---------------------------------------------------------------------------
3. Medindo desempenho: timeit e cProfile
---------------------------------------------------------------------------
Nao adivinhe onde esta o gargalo. MECA.

TIMEIT: para comparar implementacoes pequenas

    import timeit

    # Mede o tempo medio de 1 milhao de execucoes
    tempo = timeit.timeit(
        stmt="x in lista",
        setup="lista = list(range(1000)); x = 999",
        number=100_000,
    )
    print(f"Busca em lista: {tempo:.4f}s")

    # Forma mais pratica: usar a funcao diretamente
    import timeit

    def busca_lista(n):
        lista = list(range(n))
        return n - 1 in lista

    def busca_set(n):
        conjunto = set(range(n))
        return n - 1 in conjunto

    t_lista = timeit.timeit(lambda: busca_lista(10_000), number=100)
    t_set   = timeit.timeit(lambda: busca_set(10_000),   number=100)
    print(f"Lista: {t_lista:.4f}s  |  Set: {t_set:.4f}s")
    print(f"Set e {t_lista/t_set:.1f}x mais rapido")

TIME MANUAL: para medir blocos maiores

    import time

    inicio = time.perf_counter()    # mais preciso que time.time()
    resultado = funcao_pesada()
    duracao = time.perf_counter() - inicio
    print(f"Duracao: {duracao:.4f}s")

CPROFILE: para encontrar gargalos em programas inteiros

    import cProfile
    cProfile.run("minha_funcao(dados)", sort="cumulative")

    # Ou na linha de comando:
    # python -m cProfile -s cumulative meu_script.py

cProfile mostra: quantas vezes cada funcao foi chamada, tempo total
em cada funcao e tempo proprio (excluindo chamadas internas). Procure
as funcoes com maior "tottime" ou "cumtime" -- esse e o gargalo.

---------------------------------------------------------------------------
4. Memoizacao: evitando recalcular o que ja foi calculado
---------------------------------------------------------------------------
Memoizacao e guardar o resultado de uma funcao pura para reutilizar
quando os mesmos argumentos aparecerem novamente.

O problema classico -- Fibonacci recursivo ingenuo:

    def fib_lento(n):
        if n < 2: return n
        return fib_lento(n-1) + fib_lento(n-2)

    fib_lento(40)   # ~20 segundos! calcula fib(38) mais de 1 bilhao de vezes

Com @lru_cache, cada resultado e calculado apenas UMA vez:

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def fib_rapido(n):
        if n < 2: return n
        return fib_rapido(n-1) + fib_rapido(n-2)

    fib_rapido(80)   # instantaneo! calculou apenas 81 valores distintos

    fib_rapido.cache_info()
    # CacheInfo(hits=78, misses=81, maxsize=None, currsize=81)

QUANDO USAR lru_cache:
    - Funcao PURA: mesmo argumento sempre retorna o mesmo resultado
    - Chamada com os mesmos argumentos multiplas vezes
    - Argumentos sao hasheaveis (int, str, tuple -- nao list ou dict)

NAO USE lru_cache:
    - Funcoes com efeitos colaterais (print, escrita em arquivo...)
    - Funcoes com argumentos mutaveis (listas, dicionarios)
    - Quando o espaco de argumentos e muito grande (cache pode crescer demais)

---------------------------------------------------------------------------
5. Geradores versus listas: memoria sob controle
---------------------------------------------------------------------------
Geradores calculam valores sob demanda -- economizam memoria quando voce
so vai usar cada valor uma vez:

    import sys

    # Lista: todos os valores na memoria de uma vez
    lista = [x**2 for x in range(1_000_000)]
    print(sys.getsizeof(lista))    # ~8.5 MB

    # Gerador: calcula um valor por vez, ocupa quase nada
    gen = (x**2 for x in range(1_000_000))
    print(sys.getsizeof(gen))      # ~120 bytes

    # Para reducoes, use gerador diretamente:
    total = sum(x**2 for x in range(1_000_000))   # sem lista intermediaria

QUANDO USAR GERADOR:
    - Voce so vai percorrer uma vez
    - Passa direto para sum(), any(), all(), max(), min()
    - O conjunto de dados e grande (economiza RAM)

QUANDO USAR LISTA:
    - Precisa percorrer mais de uma vez
    - Precisa de indexacao (lista[i]) ou len()
    - Quer inspecionar o resultado durante depuracao

---------------------------------------------------------------------------
6. collections: estruturas especializadas
---------------------------------------------------------------------------
O modulo collections oferece estruturas otimizadas para casos especificos:

COUNTER: contando ocorrencias eficientemente

    from collections import Counter

    palavras = "a b a c a b d".split()
    contagem = Counter(palavras)
    print(contagem)                  # Counter({'a': 3, 'b': 2, 'c': 1, 'd': 1})
    print(contagem.most_common(2))   # [('a', 3), ('b', 2)]

    # Equivalente manual (mais lento):
    contagem = {}
    for p in palavras:
        contagem[p] = contagem.get(p, 0) + 1

DEQUE: fila dupla com insercao O(1) nas duas pontas

    from collections import deque

    d = deque([1, 2, 3], maxlen=3)   # maxlen: descarta automaticamente
    d.appendleft(0)    # [0, 1, 2, 3] -> maxlen descarta o 3: [0, 1, 2]
    d.popleft()        # 0, fila vira [1, 2]
    d.rotate(1)        # rotaciona: [2, 1]

    # Perfeito para filas e historico de tamanho fixo:
    historico = deque(maxlen=100)   # guarda os ultimos 100 itens

DEFAULTDICT: dicionario com valor padrao automatico

    from collections import defaultdict

    grupos = defaultdict(list)
    for palavra in ["ana", "bia", "alice", "bob"]:
        grupos[palavra[0]].append(palavra)   # sem verificar se a chave existe
    # {'a': ['ana', 'alice'], 'b': ['bia', 'bob']}

HEAPQ: fila de prioridade (min-heap)

    import heapq

    h = []
    heapq.heappush(h, 3)
    heapq.heappush(h, 1)
    heapq.heappush(h, 2)
    heapq.heappop(h)    # 1 -- sempre retorna o menor

    # Top N elementos de uma sequencia grande:
    heapq.nlargest(3,  [5, 1, 8, 3, 9, 2])   # [9, 8, 5]
    heapq.nsmallest(3, [5, 1, 8, 3, 9, 2])   # [1, 2, 3]

---------------------------------------------------------------------------
7. Outras otimizacoes classicas
---------------------------------------------------------------------------
CONSTRUCAO DE STRING: use join, nao +=

    # LENTO: cada += cria uma nova string (O(n^2) no total)
    resultado = ""
    for palavra in lista_de_palavras:
        resultado += palavra + " "

    # RAPIDO: join e O(n)
    resultado = " ".join(lista_de_palavras)

LOOKUP EM SET em vez de lista para verificar pertencimento:

    # O(n) para cada verificacao
    palavras_validas = ["python", "java", "go", "rust"]
    if palavra in palavras_validas:    # percorre a lista

    # O(1) para cada verificacao
    palavras_validas = {"python", "java", "go", "rust"}
    if palavra in palavras_validas:    # hash direto

EVITE ATRIBUTO LOOKUP REPETIDO EM LOOPS:

    # Mais lento: lookup de append a cada iteracao
    for x in dados:
        lista.append(x * 2)

    # Mais rapido: referencia local ao metodo
    append = lista.append
    for x in dados:
        append(x * 2)

COMPREENSOES SAO MAIS RAPIDAS QUE LOOPS EQUIVALENTES:
    # Loop tradicional: mais lento
    resultado = []
    for x in range(1000):
        resultado.append(x * 2)

    # Compreensao: mais rapido (implementada em C)
    resultado = [x * 2 for x in range(1000)]
""",
    exemplos=[
        Exemplo(
            titulo="Comparando complexidades na pratica",
            codigo='''import timeit
import sys

n = 10_000

# O(n) vs O(1): busca em lista vs set
lista = list(range(n))
conjunto = set(lista)

t_lista = timeit.timeit(lambda: (n - 1) in lista,   number=10_000)
t_set   = timeit.timeit(lambda: (n - 1) in conjunto, number=10_000)
print(f"Busca em lista: {t_lista:.4f}s")
print(f"Busca em set:   {t_set:.4f}s")
print(f"Set e {t_lista/t_set:.0f}x mais rapido para n={n}")

# O(n^2) vs O(n log n): algoritmos de ordenacao
import random
dados = list(range(1000))
random.shuffle(dados)

def bubble_sort(lst):
    lst = lst[:]
    n = len(lst)
    for i in range(n):
        for j in range(n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst

t_bubble = timeit.timeit(lambda: bubble_sort(dados), number=10)
t_sorted = timeit.timeit(lambda: sorted(dados),       number=10)
print(f"\nBubble sort O(n^2): {t_bubble:.4f}s")
print(f"sorted()   O(n lg n): {t_sorted:.6f}s")
print(f"sorted() e {t_bubble/t_sorted:.0f}x mais rapido")

# Memoria: lista vs gerador
lista_g = [x**2 for x in range(100_000)]
gen_g   = (x**2 for x in range(100_000))
print(f"\nLista:   {sys.getsizeof(lista_g):>10,} bytes")
print(f"Gerador: {sys.getsizeof(gen_g):>10,} bytes")
''',
            explicacao="A diferenca entre O(n) e O(1) parece abstrata ate voce "
                       "medir: para n=10.000, set e dezenas de vezes mais rapido. "
                       "Para n=1.000.000 a diferenca seria de milhoes de vezes. "
                       "Bubble sort O(n^2) vs sorted() O(n log n): para n=1000, "
                       "sorted() ja e dezenas de vezes mais rapido. "
                       "A diferenca de memoria entre lista e gerador e dramatica: "
                       "800KB vs 120 bytes para 100.000 elementos.",
        ),
        Exemplo(
            titulo="Memoizacao: lru_cache vs recursao ingenua",
            codigo='''import timeit
from functools import lru_cache

# Fibonacci LENTO: recalcula o mesmo valor exponencialmente
def fib_lento(n):
    if n < 2: return n
    return fib_lento(n-1) + fib_lento(n-2)

# Fibonacci RAPIDO: cada valor calculado apenas uma vez
@lru_cache(maxsize=None)
def fib_cache(n):
    if n < 2: return n
    return fib_cache(n-1) + fib_cache(n-2)

# Fibonacci ITERATIVO: O(n) sem overhead de recursao
def fib_iter(n):
    if n < 2: return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

# Comparando para n=30
n = 30
t_lento = timeit.timeit(lambda: fib_lento(n), number=10)
t_cache = timeit.timeit(lambda: fib_cache(n), number=10_000)
t_iter  = timeit.timeit(lambda: fib_iter(n),  number=10_000)

print(f"fib_lento({n}):  {t_lento:.4f}s (x10 chamadas)")
print(f"fib_cache({n}):  {t_cache:.6f}s (x10.000 chamadas)")
print(f"fib_iter({n}):   {t_iter:.6f}s (x10.000 chamadas)")
print(f"Resultado: {fib_cache(80)}")
print(f"Cache info: {fib_cache.cache_info()}")
''',
            explicacao="fib_lento(35) faz mais de 29 milhoes de chamadas. "
                       "fib_cache(35) faz apenas 36 chamadas distintas -- "
                       "o resto vem do cache. "
                       "fib_iter e ainda mais eficiente: sem overhead de recursao "
                       "e sem dicionario de cache. "
                       "cache_info() mostra hits (respostas do cache) vs misses "
                       "(calculados de fato) -- util para avaliar a eficiencia do cache.",
        ),
        Exemplo(
            titulo="collections e otimizacoes de string",
            codigo='''from collections import Counter, deque, defaultdict
import timeit

# COUNTER: contando palavras eficientemente
texto = "o rato roeu a roupa do rei de roma o rato e o rei"
c = Counter(texto.split())
print("Top 3 palavras:", c.most_common(3))

# DEQUE: fila de historico com tamanho fixo
historico = deque(maxlen=5)
for i in range(10):
    historico.append(i)
print("Ultimos 5:", list(historico))   # [5, 6, 7, 8, 9]

# DEFAULTDICT: agrupando sem verificar chave
palavras = "abacate banana amora blueberry caju acai".split()
por_inicial = defaultdict(list)
for p in palavras:
    por_inicial[p[0]].append(p)
print("Por inicial:", dict(por_inicial))

# STRING JOIN vs += em loop
partes = ["parte"] * 10_000

def concatenar_mais():
    r = ""
    for p in partes:
        r += p
    return r

def concatenar_join():
    return "".join(partes)

t_mais = timeit.timeit(concatenar_mais, number=100)
t_join = timeit.timeit(concatenar_join, number=100)
print(f"\n+=   : {t_mais:.4f}s")
print(f"join : {t_join:.4f}s")
print(f"join e {t_mais/t_join:.1f}x mais rapido")
''',
            explicacao="Counter.most_common(n) usa internamente um heap para "
                       "encontrar os N mais frequentes sem ordenar tudo -- O(m log n). "
                       "deque com maxlen descarta automaticamente o elemento mais antigo: "
                       "perfeito para janelas deslizantes e historico de tamanho fixo. "
                       "join e mais rapido que += porque calcula o tamanho total antes "
                       "de alocar memoria, enquanto += recria a string a cada iteracao.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d29e1",
            enunciado=(
                "Escreva interseccao_rapida(a, b) que retorna uma lista\n"
                "com os elementos que aparecem em AMBAS as listas,\n"
                "SEM duplicatas, em O(n+m) usando set.\n\n"
                "Exemplos:\n"
                "   interseccao_rapida([1, 2, 3, 2], [2, 3, 9]) -> [2, 3]\n"
                "   interseccao_rapida([], [1])                  -> []\n"
                "   interseccao_rapida([5, 5], [5])              -> [5]\n\n"
                "Por que usar set?\n"
                "   Abordagem ingenua: para cada elemento de a, percorre b\n"
                "   -> O(n*m): lento para listas grandes\n\n"
                "   Com set: converter b para set e O(m), depois\n"
                "   verificar pertencimento e O(1) por elemento\n"
                "   -> O(n+m): muito mais rapido\n\n"
                "Estrategia:\n"
                "   conjunto_b = set(b)    # O(m)\n"
                "   vistos = set()         # controla duplicatas no resultado\n"
                "   resultado = []\n"
                "   for x in a:            # O(n)\n"
                "       if x in conjunto_b and x not in vistos:\n"
                "           resultado.append(x)\n"
                "           vistos.add(x)\n"
                "   return resultado"
            ),
            funcao="interseccao_rapida",
            assinatura="def interseccao_rapida(a, b):",
            testes=[
                ("interseccao_rapida([1, 2, 3, 2], [2, 3, 9])", "[2, 3]"),
                ("interseccao_rapida([], [1])", "[]"),
                ("interseccao_rapida([5, 5], [5])", "[5]"),
            ],
            nivel="medio",
            dica="conjunto_b = set(b); vistos = set(); resultado = []; for x in a: if x in conjunto_b and x not in vistos: resultado.append(x); vistos.add(x); return resultado",
        ),
        Exercicio(
            id="d29e2",
            enunciado=(
                "O import lru_cache e o decorator @lru_cache ja estao\n"
                "na assinatura. Complete a funcao fib(n) que calcula o\n"
                "n-esimo numero de Fibonacci de forma recursiva.\n\n"
                "Exemplos:\n"
                "   fib(10) -> 55\n"
                "   fib(0)  -> 0\n"
                "   fib(80) -> 23416728348467685\n\n"
                "A sequencia de Fibonacci:\n"
                "   fib(0) = 0\n"
                "   fib(1) = 1\n"
                "   fib(n) = fib(n-1) + fib(n-2)  para n >= 2\n\n"
                "Implemente a recursao ingenua -- o cache cuida do resto:\n"
                "   if n < 2: return n\n"
                "   return fib(n-1) + fib(n-2)\n\n"
                "Sem @lru_cache, fib(80) seria impraticavel:\n"
                "   fib_sem_cache(40) ja leva varios segundos\n"
                "   fib_sem_cache(80) levaria mais tempo que a vida do universo\n\n"
                "Com @lru_cache(maxsize=None), cada valor e calculado\n"
                "apenas UMA vez. Resultados anteriores sao reutilizados."
            ),
            funcao="fib",
            assinatura="from functools import lru_cache\n\n\n@lru_cache(maxsize=None)\ndef fib(n):",
            testes=[
                ("fib(10)", "55"),
                ("fib(0)", "0"),
                ("fib(80)", "23416728348467685"),
            ],
            nivel="medio",
            dica="if n < 2: return n; return fib(n-1) + fib(n-2)",
        ),
        Exercicio(
            id="d29e3",
            enunciado=(
                "O import Counter ja esta na assinatura.\n"
                "Escreva top_n(texto, n) que retorna as n palavras mais\n"
                "frequentes de um texto, como lista de tuplas (palavra, contagem),\n"
                "ordenadas da mais para a menos frequente.\n\n"
                "Exemplos:\n"
                "   top_n('a b a c a b', 2) -> [('a', 3), ('b', 2)]\n"
                "   top_n('', 3)            -> []\n"
                "   top_n('x', 5)           -> [('x', 1)]\n\n"
                "Estrategia:\n"
                "   palavras = texto.split()           # divide em lista\n"
                "   if not palavras: return []         # caso vazio\n"
                "   return Counter(palavras).most_common(n)\n\n"
                "Counter(lista) conta automaticamente as ocorrencias.\n"
                "most_common(n) retorna as n mais comuns em ordem decrescente.\n"
                "Se n for maior que o vocabulario, retorna tudo que existe.\n\n"
                "Internamente, most_common(n) usa um heap para encontrar\n"
                "os n maiores sem ordenar o contador inteiro -- O(m log n)\n"
                "onde m e o numero de palavras unicas."
            ),
            funcao="top_n",
            assinatura="from collections import Counter\n\n\ndef top_n(texto, n):",
            testes=[
                ("top_n('a b a c a b', 2)", "[('a', 3), ('b', 2)]"),
                ("top_n('', 3)", "[]"),
                ("top_n('x', 5)", "[('x', 1)]"),
            ],
            nivel="medio",
            dica="palavras = texto.split(); if not palavras: return []; return Counter(palavras).most_common(n)",
        ),
    ],
    quiz=[
        Quiz(
            "Qual operacao em lista tem custo O(n) e deve ser evitada em loops?",
            ["lista.append(x) -- adiciona ao final",
             "lista[i] -- acesso por indice",
             "lista.insert(0, x) -- insere no inicio, deslocando todos os elementos",
             "len(lista) -- retorna o tamanho"],
            2,
            "lista.insert(0, x) e lista.pop(0) sao O(n): todos os elementos "
            "precisam ser deslocados uma posicao. "
            "append e pop() (sem indice) sao O(1): operam no final sem mover nada. "
            "Para insercao e remocao frequente no inicio, use collections.deque "
            "que tem appendleft e popleft em O(1).",
        ),
        Quiz(
            "Por que @lru_cache transforma fib(80) de impraticavel em instantaneo?",
            ["lru_cache paraleliza a recursao automaticamente",
             "lru_cache memoriza resultados ja calculados -- cada valor de fib e calculado apenas uma vez em vez de exponencialmente",
             "lru_cache converte a recursao em iteracao",
             "lru_cache aumenta o limite de recursao do Python"],
            1,
            "Sem cache: fib(80) chama fib(79) e fib(78), cada um chama dois mais, "
            "e assim por diante. O numero de chamadas cresce exponencialmente. "
            "Com lru_cache: fib(79) e calculado uma vez, o resultado fica no cache. "
            "Quando fib(80) precisa de fib(79) de novo, le do cache -- O(1). "
            "Total: apenas 81 calculos distintos em vez de 2^80.",
        ),
        Quiz(
            "Qual a diferenca de complexidade entre 'x in lista' e 'x in conjunto'?",
            ["Ambos sao O(1) -- Python otimiza automaticamente",
             "lista e O(n) pois percorre ate encontrar; set e O(1) pois usa hash para localizar diretamente",
             "set e mais lento que lista para elementos no inicio",
             "Depende do tipo do elemento"],
            1,
            "Lista: percorre elemento por elemento ate achar x ou chegar ao fim. "
            "Para o pior caso (x nao existe), percorre TODOS os n elementos: O(n). "
            "Set: calcula hash(x) e vai diretamente ao bucket correspondente: O(1). "
            "Para verificacoes frequentes de pertencimento, converta para set uma vez "
            "e economize O(n) por verificacao.",
        ),
        Quiz(
            "Por que 'join' e mais rapido que '+=' para construir strings em loop?",
            ["join usa multiplos nucleos internamente",
             "'+=' cria uma nova string a cada iteracao (O(n) por operacao, O(n^2) no total); join calcula o tamanho total antes de alocar memoria uma unica vez",
             "join usa bytes em vez de unicode",
             "Nao ha diferenca -- ambos sao equivalentes"],
            1,
            "Strings sao imutaveis. resultado += parte cria uma NOVA string a cada vez, "
            "copiando todo o conteudo anterior. Para n partes, o total de operacoes "
            "e 1+2+3+...+n = O(n^2). "
            "join calcula o tamanho total (soma dos len()), aloca uma vez e copia. "
            "Para n partes de tamanho m: O(n*m) em vez de O(n^2*m).",
        ),
    ],
    projeto=(
        "Crie benchmarks.py que compare implementacoes de diferentes\n"
        "complexidades para o mesmo problema:\n\n"
        "   PROBLEMA 1 -- Busca de duplicatas:\n"
        "   def tem_duplicata_o_n2(lista): dois loops aninhados\n"
        "   def tem_duplicata_o_n(lista):  usando set\n"
        "   Compare para listas de 100, 1000, 10000 elementos\n\n"
        "   PROBLEMA 2 -- Contagem de palavras:\n"
        "   def contar_manual(texto):  loop com dict.get()\n"
        "   def contar_counter(texto): Counter(texto.split())\n"
        "   Compare para textos de 10, 100, 1000 palavras\n\n"
        "   PROBLEMA 3 -- Concatenacao de strings:\n"
        "   def concatenar_mais(partes): loop com +=\n"
        "   def concatenar_join(partes): ''.join(partes)\n"
        "   Compare para 100, 1000, 10000 partes\n\n"
        "   RELATORIO:\n"
        "   Para cada problema, exiba uma tabela:\n"
        "   n       O(n^2)    O(n)    speedup\n"
        "   -----   -------   -----   -------\n"
        "   100     0.001s    0.0001s  10x\n"
        "   1000    0.100s    0.001s   100x\n"
        "   10000   10.000s   0.010s   1000x\n\n"
        "BONUS: use cProfile em uma funcao com gargalo artificial\n"
        "e mostre como identificar a funcao mais lenta pelo relatorio."
    ),
    leitura=[
        "docs.python.org/pt-br/3/library/timeit.html -- modulo timeit",
        "docs.python.org/pt-br/3/library/profile.html -- cProfile",
        "docs.python.org/pt-br/3/library/collections.html -- collections",
        "wiki.python.org/moin/TimeComplexity -- custo das operacoes",
    ],
))

# ---------------------------------------------------------------- DIA 30
DIAS.append(Dia(
    numero=30,
    titulo="Projeto final: estrutura, empacotamento e boas praticas",
    nivel="Avancado",
    duracao="150 min",
    objetivos=[
        "Organizar um projeto Python com estrutura de diretorios profissional",
        "Configurar pyproject.toml como descritor moderno do projeto",
        "Escrever README, docstrings e comentarios que realmente ajudam",
        "Usar linter (ruff) e formatador (black) para padronizar o codigo",
        "Entender o fluxo de publicacao no PyPI",
        "Integrar tudo que foi aprendido nos 30 dias em um projeto coeso",
    ],
    teoria="""
Voce chegou ao Dia 30. Ao longo do curso voce aprendeu a escrever
codigo Python correto, eficiente, testado e bem documentado. Hoje
vamos falar de algo igualmente importante: como ORGANIZAR e EMPACOTAR
esse codigo para que outras pessoas (e voce mesmo no futuro) consigam
usar, entender e contribuir com ele.

---------------------------------------------------------------------------
1. Estrutura de diretorios de um projeto Python moderno
---------------------------------------------------------------------------
Nao existe uma estrutura universal obrigatoria, mas ha convencoes
amplamente adotadas que tornam projetos faceis de navegar:

ESTRUTURA SRC (recomendada para bibliotecas):

    meu_projeto/
    +-- src/
    |   +-- meu_projeto/
    |       +-- __init__.py       torna o diretorio um pacote
    |       +-- core.py           logica principal
    |       +-- utils.py          funcoes utilitarias
    |       +-- cli.py            interface de linha de comando
    |       +-- models.py         tipos de dados / dataclasses
    +-- tests/
    |   +-- __init__.py
    |   +-- test_core.py
    |   +-- test_utils.py
    +-- docs/
    |   +-- index.md
    +-- pyproject.toml            configuracao do projeto (moderno)
    +-- README.md                 apresentacao do projeto
    +-- LICENSE                   licenca de uso
    +-- .gitignore                o que o git deve ignorar
    +-- .github/
        +-- workflows/
            +-- ci.yml            CI: testa automaticamente a cada commit

Por que src/? Separa o codigo-fonte instalavel do resto do projeto.
Evita importar acidentalmente o pacote local em vez do instalado,
o que causa bugs sutis nos testes.

ESTRUTURA SIMPLES (para scripts e projetos pequenos):

    meu_script/
    +-- meu_script.py
    +-- tests/
    |   +-- test_meu_script.py
    +-- pyproject.toml
    +-- README.md

---------------------------------------------------------------------------
2. pyproject.toml: o descritor moderno do projeto
---------------------------------------------------------------------------
pyproject.toml e o arquivo de configuracao padrao atual do Python,
substituindo setup.py, setup.cfg e requirements.txt de forma unificada.

    [project]
    name = "meu-projeto"
    version = "0.1.0"
    description = "Uma ferramenta para processar dados"
    readme = "README.md"
    requires-python = ">=3.10"
    license = {text = "MIT"}
    authors = [
        {name = "Seu Nome", email = "voce@email.com"},
    ]
    dependencies = [
        "requests>=2.28",
        "click>=8.0",
    ]

    [project.optional-dependencies]
    dev = [
        "pytest>=7.0",
        "ruff>=0.1",
        "black>=23.0",
    ]

    [project.scripts]
    meu-projeto = "meu_projeto.cli:main"

    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"

    [tool.ruff]
    line-length = 88
    select = ["E", "F", "I"]

    [tool.pytest.ini_options]
    testpaths = ["tests"]

A secao [project.scripts] define um comando de terminal:
ao instalar o pacote, "meu-projeto" passa a ser um comando
disponivel no PATH que chama a funcao main() do modulo cli.py.

---------------------------------------------------------------------------
3. Gerenciando dependencias com ambientes virtuais
---------------------------------------------------------------------------
Cada projeto deve ter seu proprio ambiente virtual:

    python3 -m venv .venv
    source .venv/bin/activate

    pip install -e ".[dev]"       instala o projeto em modo editavel
    pip freeze > requirements.lock congela versoes exatas

FERRAMENTAS MODERNAS: uv e extremamente rapido e gerencia venv e
dependencias de forma integrada.

    uv venv
    uv pip install -e ".[dev]"
    uv run pytest

---------------------------------------------------------------------------
4. README.md: a porta de entrada do projeto
---------------------------------------------------------------------------
O README e a primeira coisa que qualquer pessoa ve. Um bom README
responde cinco perguntas:

    1. O QUE FAZ: uma frase descrevendo o projeto
    2. POR QUE USAR: qual problema resolve
    3. COMO INSTALAR: comandos exatos, sem ambiguidade
    4. COMO USAR: exemplos de codigo funcionando
    5. COMO CONTRIBUIR: como rodar testes, como submeter mudancas

ESTRUTURA MINIMA:

    # Nome do Projeto

    Descricao curta em uma ou duas frases.

    ## Instalacao

        pip install meu-projeto

    ## Uso rapido

        from meu_projeto import processar
        resultado = processar("entrada.csv")

    ## Desenvolvimento

        git clone https://github.com/usuario/meu-projeto
        cd meu-projeto
        python -m venv .venv && source .venv/bin/activate
        pip install -e ".[dev]"
        pytest

    ## Licenca

    MIT -- veja LICENSE para detalhes.

---------------------------------------------------------------------------
5. Qualidade de codigo: linters e formatadores
---------------------------------------------------------------------------
RUFF: linter e formatador extremamente rapido

    pip install ruff
    ruff check .          verifica erros e problemas de estilo
    ruff check --fix .    corrige automaticamente o que for possivel
    ruff format .         formata o codigo

O que ruff verifica:
    E: erros de estilo PEP 8 (espacos, comprimento de linha...)
    F: erros do pyflakes (variaveis nao usadas, imports nao usados...)
    I: ordenacao de imports

BLACK: formatador opinativo

    pip install black
    black .               formata todos os arquivos .py

Black e "sem configuracao": ele decide o estilo e voce nao discute.
O ganho e que discussoes de estilo acabam -- o black decide.

MYPY: verificador de tipos (Dia 23)

    pip install mypy
    mypy src/

---------------------------------------------------------------------------
6. Controle de versao semantico
---------------------------------------------------------------------------
Versoes seguem o padrao MAJOR.MINOR.PATCH (ex: 2.1.4):

    PATCH (2.1.4 -> 2.1.5): correcao de bug, nao quebra nada
    MINOR (2.1.x -> 2.2.0): nova funcionalidade, compativel com anterior
    MAJOR (2.x.x -> 3.0.0): mudanca que quebra compatibilidade

Na pratica:
    0.x.x : desenvolvimento inicial, API pode mudar a qualquer momento
    1.0.0 : primeira versao estavel, API publica definida
    1.x.0 : novas funcionalidades, compativel com 1.0.0
    2.0.0 : mudancas que quebram codigo que usava 1.x

---------------------------------------------------------------------------
7. Publicando no PyPI
---------------------------------------------------------------------------
PyPI e o repositorio de pacotes Python onde pip install busca os pacotes.

    pip install build twine

    python -m build
    # Gera: dist/meu_projeto-0.1.0.tar.gz
    #       dist/meu_projeto-0.1.0-py3-none-any.whl

    twine upload --repository testpypi dist/*    teste primeiro!
    twine upload dist/*                          publicacao real

    # Qualquer pessoa pode instalar:
    pip install meu-projeto

Use tokens de API (pypi.org/manage/account/token/) em vez de senha.

---------------------------------------------------------------------------
8. CI/CD com GitHub Actions
---------------------------------------------------------------------------
CI (Continuous Integration) roda os testes a cada push automaticamente.
Crie o arquivo .github/workflows/ci.yml no repositorio:

    name: CI
    on: [push, pull_request]
    jobs:
      test:
        runs-on: ubuntu-latest
        strategy:
          matrix:
            python-version: ["3.10", "3.11", "3.12"]
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: ${{ matrix.python-version }}
          - run: pip install -e ".[dev]"
          - run: ruff check .
          - run: pytest --tb=short

Cada push no GitHub aciona esse workflow. Se qualquer passo falhar,
voce recebe notificacao e o PR nao pode ser mergeado.

---------------------------------------------------------------------------
9. O que voce construiu em 30 dias
---------------------------------------------------------------------------
    Semana 1 (Dias 1-7):   tipos, operadores, strings, condicionais,
                            while, for
    Semana 2 (Dias 8-14):  colecoes, compreensoes, funcoes, modulos,
                            arquivos, JSON, CSV
    Semana 3 (Dias 15-23): excecoes, POO (3 dias), dataclasses/Enum/ABC,
                            iteradores, decoradores, context managers,
                            type hints
    Semana 4 (Dias 24-30): testes, Linux, regex, concorrencia, asyncio,
                            desempenho, projeto final

Voce tem agora as ferramentas para construir:
    - Scripts de automacao e processamento de dados
    - APIs e servicos web (com FastAPI ou Django)
    - Ferramentas de linha de comando
    - Bibliotecas reutilizaveis
    - Pipelines de dados e ETL
    - Aplicacoes com concorrencia e assincronia

O proximo passo: escolha UM projeto real que resolva um problema
que voce tem, e construa-o. A melhor forma de consolidar 30 dias de
aprendizado e colocar tudo em pratica em algo que importa para voce.
""",
    exemplos=[
        Exemplo(
            titulo="Modulo profissional com dataclass, tipagem e docstrings",
            codigo='''from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import json


@dataclass
class Tarefa:
    """Representa uma tarefa com titulo e estado de conclusao."""

    titulo: str
    feita: bool = False

    def __post_init__(self) -> None:
        if not self.titulo.strip():
            raise ValueError("titulo nao pode ser vazio")

    def concluir(self) -> None:
        """Marca a tarefa como concluida."""
        self.feita = True

    def __str__(self) -> str:
        icone = "x" if self.feita else " "
        return f"[{icone}] {self.titulo}"


class GerenciadorTarefas:
    """Gerencia uma colecao de tarefas com persistencia em JSON."""

    def __init__(self, arquivo: Optional[str] = None) -> None:
        self._tarefas: list[Tarefa] = []
        self._arquivo = Path(arquivo) if arquivo else None
        if self._arquivo and self._arquivo.exists():
            self._carregar()

    def adicionar(self, titulo: str) -> Tarefa:
        """Adiciona uma nova tarefa e retorna ela."""
        t = Tarefa(titulo)
        self._tarefas.append(t)
        return t

    def concluir(self, indice: int) -> None:
        """Conclui a tarefa no indice dado. Levanta IndexError se invalido."""
        if not 0 <= indice < len(self._tarefas):
            raise IndexError(f"indice {indice} invalido")
        self._tarefas[indice].concluir()

    def pendentes(self) -> list[str]:
        """Retorna titulos das tarefas ainda nao concluidas."""
        return [t.titulo for t in self._tarefas if not t.feita]

    def resumo(self) -> str:
        """Retorna 'X/Y concluidas'."""
        feitas = sum(1 for t in self._tarefas if t.feita)
        return f"{feitas}/{len(self._tarefas)} concluidas"

    def _carregar(self) -> None:
        dados = json.loads(self._arquivo.read_text(encoding="utf-8"))
        self._tarefas = [Tarefa(**d) for d in dados]

    def salvar(self) -> None:
        """Persiste as tarefas no arquivo configurado."""
        if not self._arquivo:
            raise RuntimeError("nenhum arquivo configurado")
        dados = [{"titulo": t.titulo, "feita": t.feita}
                 for t in self._tarefas]
        self._arquivo.write_text(
            json.dumps(dados, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


g = GerenciadorTarefas()
g.adicionar("Aprender Python")
g.adicionar("Fazer projeto final")
g.adicionar("Publicar no GitHub")
g.concluir(0)
g.concluir(1)

for t in g._tarefas:
    print(t)
print(g.resumo())
print("Pendentes:", g.pendentes())
''',
            explicacao="Optional[str] = None aceita string ou nenhum valor. "
                       "__post_init__ valida dados apos a criacao da dataclass. "
                       "_tarefas e _arquivo com underscore sinalizam uso interno. "
                       "Cada metodo publico tem docstring de uma linha -- suficiente "
                       "para metodos simples, mais detalhado so quando necessario. "
                       "O modulo e autocontido: pode ser importado ou executado.",
        ),
        Exemplo(
            titulo="Comparacao de versoes e serializacao JSON",
            codigo='''import json


def comparar_versoes(a: str, b: str) -> int:
    # Converte 'MAJOR.MINOR.PATCH' em tupla de inteiros para comparacao correta
    # '1.10.0' como string < '1.9.9' (errado); como inteiros (1,10,0) > (1,9,9) (certo)
    def para_tupla(v: str) -> tuple:
        return tuple(int(x) for x in v.split("."))

    ta, tb = para_tupla(a), para_tupla(b)
    if ta > tb:
        return 1
    if ta < tb:
        return -1
    return 0


def serializar(dados) -> str:
    # ensure_ascii=False preserva acentos e UTF-8 no JSON
    return json.dumps(dados, ensure_ascii=False)


def desserializar(texto: str):
    return json.loads(texto)


# Testando comparacao de versoes
casos = [
    ("1.10.0", "1.9.9"),    # 1.10 > 1.9 numericamente
    ("1.0.0",  "1.0.0"),
    ("0.9.0",  "1.0.0"),
    ("2.0.0",  "1.99.99"),
]
for a, b in casos:
    r = comparar_versoes(a, b)
    sinal = {1: ">", -1: "<", 0: "="}[r]
    print(f"{a} {sinal} {b}")

# Testando serializacao (ida e volta)
tarefas = [
    {"titulo": "Aprender Python", "feita": True},
    {"titulo": "Fazer projeto",   "feita": False},
]
json_str = serializar(tarefas)
print("\nJSON:", json_str)
print("Ida e volta:", desserializar(json_str) == tarefas)
''',
            explicacao="A comparacao de versoes como string falha porque "
                       "'1.10.0' < '1.9.9' lexicograficamente (compara '1' com '1', "
                       "depois '1' com '9' -- e '1' < '9'). "
                       "Convertendo para tupla de inteiros (1,10,0) vs (1,9,9): "
                       "Python compara elemento a elemento e 10 > 9 -- correto. "
                       "ensure_ascii=False e essencial para projetos em portugues: "
                       "sem ele, 'Sao Paulo' viraria 'S\\u00e3o Paulo' no JSON.",
        ),
        Exemplo(
            titulo="CLI completa com subcomandos e testes sem sys.argv",
            codigo='''import argparse
import json
import sys
from pathlib import Path

ARQUIVO = Path.home() / ".tarefas.json"


def carregar():
    if not ARQUIVO.exists():
        return []
    return json.loads(ARQUIVO.read_text(encoding="utf-8"))


def salvar(tarefas):
    ARQUIVO.write_text(
        json.dumps(tarefas, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def cmd_adicionar(args):
    tarefas = carregar()
    tarefas.append({"titulo": args.titulo, "feita": False})
    salvar(tarefas)
    print(f"Adicionado: {args.titulo}")


def cmd_listar(args):
    tarefas = carregar()
    if not tarefas:
        print("Nenhuma tarefa.")
        return
    for i, t in enumerate(tarefas):
        icone = "x" if t["feita"] else " "
        print(f"  {i}. [{icone}] {t['titulo']}")


def cmd_concluir(args):
    tarefas = carregar()
    if not 0 <= args.indice < len(tarefas):
        print(f"Indice invalido: {args.indice}", file=sys.stderr)
        sys.exit(1)
    tarefas[args.indice]["feita"] = True
    salvar(tarefas)
    print(f"Concluida: {tarefas[args.indice]['titulo']}")


def cmd_resumo(args):
    tarefas = carregar()
    feitas = sum(1 for t in tarefas if t["feita"])
    print(f"{feitas}/{len(tarefas)} concluidas")


def criar_parser():
    p = argparse.ArgumentParser(description="Gerenciador de tarefas")
    sub = p.add_subparsers(dest="comando", required=True)

    add = sub.add_parser("adicionar")
    add.add_argument("titulo")
    add.set_defaults(func=cmd_adicionar)

    lst = sub.add_parser("listar")
    lst.set_defaults(func=cmd_listar)

    done = sub.add_parser("concluir")
    done.add_argument("indice", type=int)
    done.set_defaults(func=cmd_concluir)

    res = sub.add_parser("resumo")
    res.set_defaults(func=cmd_resumo)

    return p


def main(argv=None):
    # argv=None usa sys.argv; passar lista permite testar sem modificar sys.argv
    args = criar_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()

# Simulando uso sem modificar sys.argv
main(["adicionar", "Estudar Python"])
main(["adicionar", "Fazer projeto"])
main(["concluir", "0"])
main(["listar"])
main(["resumo"])
''',
            explicacao="set_defaults(func=cmd_xxx) associa cada subcomando a sua funcao. "
                       "args.func(args) despacha sem if/elif -- cada subparser carrega "
                       "sua propria funcao. "
                       "main(argv=None) e o padrao testavel: em producao usa sys.argv, "
                       "em testes passa uma lista. "
                       "sys.exit(1) sinaliza erro ao shell -- convencao Unix: "
                       "0 = sucesso, qualquer outro valor = erro.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d30e1",
            enunciado=(
                "Escreva comparar_versoes(a, b) que compara duas strings\n"
                "de versao semantica no formato 'MAJOR.MINOR.PATCH'.\n\n"
                "Retorna:\n"
                "    1  se a e maior que b\n"
                "    0  se sao iguais\n"
                "   -1  se a e menor que b\n\n"
                "Exemplos:\n"
                "   comparar_versoes('1.10.0', '1.9.9') ->  1\n"
                "   comparar_versoes('1.0.0',  '1.0.0') ->  0\n"
                "   comparar_versoes('0.9.0',  '1.0.0') -> -1\n\n"
                "Por que nao basta comparar as strings diretamente?\n"
                "   '1.10.0' < '1.9.9' como strings (lexicografico)\n"
                "   porque '1' < '9' ao comparar o segundo campo -- ERRADO!\n"
                "   Como inteiros: (1,10,0) > (1,9,9) -- CORRETO!\n\n"
                "Estrategia:\n"
                "   Converta cada versao em tupla de inteiros:\n"
                "   '1.10.0' -> (1, 10, 0)\n"
                "   '1.9.9'  -> (1, 9, 9)\n"
                "   Compare as tuplas: (1,10,0) > (1,9,9) -> True\n\n"
                "Python compara tuplas elemento a elemento:\n"
                "   (1,10,0) vs (1,9,9): 1==1, depois 10 > 9 -> maior"
            ),
            funcao="comparar_versoes",
            assinatura="def comparar_versoes(a, b):",
            testes=[
                ("comparar_versoes('1.10.0', '1.9.9')", "1"),
                ("comparar_versoes('1.0.0', '1.0.0')", "0"),
                ("comparar_versoes('0.9.0', '1.0.0')", "-1"),
            ],
            nivel="medio",
            dica="ta = tuple(int(x) for x in a.split('.')); tb = tuple(int(x) for x in b.split('.')); return 1 if ta > tb else -1 if ta < tb else 0",
        ),
        Exercicio(
            id="d30e2",
            enunciado=(
                "O import json ja esta na assinatura.\n"
                "Complete duas funcoes:\n\n"
                "1. serializar(tarefas) -> str:\n"
                "   Converte a lista de dicionarios para JSON (string).\n\n"
                "2. desserializar(texto) -> list:\n"
                "   Converte a string JSON de volta para lista.\n\n"
                "Exemplos:\n"
                "   desserializar(serializar([{'t': 'a', 'feita': False}]))\n"
                "   -> [{'t': 'a', 'feita': False}]\n\n"
                "   desserializar(serializar([])) -> []\n"
                "   isinstance(serializar([]), str) -> True\n\n"
                "serializar deve retornar uma STRING (json.dumps).\n"
                "desserializar deve retornar um objeto Python (json.loads).\n\n"
                "Use ensure_ascii=False para preservar acentos no JSON.\n\n"
                "Juntas formam um par de IDA E VOLTA:\n"
                "   desserializar(serializar(dados)) == dados"
            ),
            funcao="serializar",
            assinatura="import json\n\n\ndef serializar(tarefas):\n    ...\n\n\ndef desserializar(texto):",
            testes=[
                ("desserializar(serializar([{'t': 'a', 'feita': False}]))",
                 "[{'t': 'a', 'feita': False}]"),
                ("desserializar(serializar([]))", "[]"),
                ("isinstance(serializar([]), str)", "True"),
            ],
            dica="serializar: return json.dumps(tarefas, ensure_ascii=False). desserializar: return json.loads(texto)",
        ),
        Exercicio(
            id="d30e3",
            enunciado=(
                "Crie a classe GerenciadorTarefas com:\n\n"
                "   __init__(self):\n"
                "       self._tarefas = []  <- NUNCA no corpo da classe!\n\n"
                "   adicionar(self, titulo: str) -> None:\n"
                "       Adiciona {'titulo': titulo, 'feita': False}\n\n"
                "   concluir(self, indice: int) -> None:\n"
                "       Marca tarefas[indice]['feita'] = True\n"
                "       Levanta IndexError se indice invalido\n\n"
                "   pendentes(self) -> list:\n"
                "       Retorna titulos das tarefas com feita=False\n\n"
                "   resumo(self) -> str:\n"
                "       Retorna 'X/Y concluidas'\n\n"
                "Exemplos:\n"
                "   g = GerenciadorTarefas()\n"
                "   g.adicionar('a'); g.adicionar('b')\n"
                "   g.concluir(0)\n"
                "   g.resumo()    -> '1/2 concluidas'\n"
                "   g.pendentes() -> ['b']\n"
                "   GerenciadorTarefas().resumo()    -> '0/0 concluidas'\n"
                "   GerenciadorTarefas().concluir(5) -> IndexError\n\n"
                "Validando o indice em concluir:\n"
                "   if not 0 <= indice < len(self._tarefas):\n"
                "       raise IndexError(f'indice {indice} invalido')"
            ),
            funcao="GerenciadorTarefas",
            assinatura="class GerenciadorTarefas:\n    def __init__(self):",
            testes=[
                ("(lambda g: (g.adicionar('a'), g.adicionar('b'), g.concluir(0), g.resumo())[3])(GerenciadorTarefas())",
                 "'1/2 concluidas'"),
                ("(lambda g: (g.adicionar('a'), g.pendentes())[1])(GerenciadorTarefas())",
                 "['a']"),
                ("GerenciadorTarefas().resumo()", "'0/0 concluidas'"),
                ("GerenciadorTarefas().concluir(5)", "!raise IndexError"),
            ],
            nivel="dificil",
            dica="self._tarefas=[]; adicionar: append({'titulo':titulo,'feita':False}); concluir: if not 0<=i<len: raise IndexError; self._tarefas[i]['feita']=True; pendentes: [t['titulo'] for t in ... if not t['feita']]; resumo: f'{feitas}/{total} concluidas'",
        ),
    ],
    quiz=[
        Quiz(
            "Para que serve a estrutura src/ em um projeto Python?",
            ["E uma convencao puramente estetica sem impacto tecnico",
             "Separa o codigo instalavel do resto e evita importar acidentalmente o pacote local em vez do instalado nos testes",
             "E obrigatoria para publicar no PyPI",
             "Permite ter multiplos pacotes em um mesmo repositorio"],
            1,
            "Sem src/, ao rodar pytest na raiz do projeto, Python pode importar "
            "o diretorio local meu_projeto/ em vez do pacote instalado no venv. "
            "Isso causa bugs sutis onde os testes passam localmente mas falham "
            "apos a instalacao. Com src/, o pacote so e encontrado se instalado.",
        ),
        Quiz(
            "O que [project.scripts] em pyproject.toml define?",
            ["Os scripts de CI/CD que rodam no GitHub Actions",
             "Comandos de terminal disponiveis apos instalar o pacote, mapeados para funcoes Python especificas",
             "Scripts de banco de dados para migracao",
             "Aliases para comandos do pip"],
            1,
            "[project.scripts] define entry points: apos 'pip install meu-projeto', "
            "o comando 'meu-projeto' fica disponivel no terminal e chama "
            "a funcao main() do modulo cli.py. "
            "E assim que ferramentas como pytest, black e ruff viram "
            "comandos de terminal apos instalacao.",
        ),
        Quiz(
            "No versionamento semantico, quando deve-se incrementar o MAJOR?",
            ["A cada nova funcionalidade adicionada",
             "Apenas para correcoes de bugs criticos",
             "Quando ha mudancas que quebram compatibilidade com versoes anteriores",
             "A cada novo commit no repositorio"],
            2,
            "PATCH (x.y.Z): correcao de bug, nao quebra nada. "
            "MINOR (x.Y.0): nova funcionalidade, compativel com anterior. "
            "MAJOR (X.0.0): mudanca que quebra codigo que usava a versao anterior "
            "(remover funcao publica, mudar assinatura, alterar comportamento). "
            "Versoes 0.x.x sinalizam desenvolvimento inicial -- API instavel.",
        ),
        Quiz(
            "Por que main(argv=None) e melhor que main() para scripts CLI?",
            ["Nao ha diferenca -- e apenas convencao",
             "Com argv=None a funcao usa sys.argv automaticamente; passando uma lista permite testar sem modificar sys.argv",
             "argv=None torna o argparse mais rapido",
             "E necessario para que o argparse funcione com subparsers"],
            1,
            "parse_args(None) le sys.argv[1:] -- comportamento padrao em producao. "
            "parse_args(['adicionar', 'titulo']) usa a lista diretamente -- "
            "permite testar sem modificar sys.argv ou chamar o script de verdade. "
            "Esse padrao e fundamental para ter testes unitarios em CLIs.",
        ),
    ],
    projeto=(
        "PROJETO FINAL: construa um gerenciador de tarefas completo\n"
        "integrando tudo o que voce aprendeu nos 30 dias.\n\n"
        "ESTRUTURA DO PROJETO:\n\n"
        "   tarefas/\n"
        "   +-- src/\n"
        "   |   +-- tarefas/\n"
        "   |       +-- __init__.py\n"
        "   |       +-- models.py     (Tarefa como dataclass)\n"
        "   |       +-- storage.py    (serializar/carregar JSON)\n"
        "   |       +-- core.py       (GerenciadorTarefas)\n"
        "   |       +-- cli.py        (argparse com subcomandos)\n"
        "   +-- tests/\n"
        "   |   +-- test_models.py\n"
        "   |   +-- test_core.py\n"
        "   |   +-- test_storage.py\n"
        "   +-- pyproject.toml\n"
        "   +-- README.md\n\n"
        "FUNCIONALIDADES MINIMAS:\n"
        "   tarefas adicionar 'Titulo da tarefa'\n"
        "   tarefas listar [--pendentes | --concluidas]\n"
        "   tarefas concluir <indice>\n"
        "   tarefas remover <indice>\n"
        "   tarefas resumo\n"
        "   tarefas exportar --formato [json|csv]\n\n"
        "REQUISITOS DE QUALIDADE:\n"
        "   - Type hints em todas as funcoes publicas\n"
        "   - Docstrings em classes e metodos publicos\n"
        "   - Testes para todos os metodos do GerenciadorTarefas\n"
        "   - ruff check . sem erros\n"
        "   - README com instalacao, uso e exemplos\n\n"
        "BONUS:\n"
        "   - Prioridade nas tarefas (alta/media/baixa)\n"
        "   - Data de criacao e conclusao\n"
        "   - Filtro por prioridade\n"
        "   - Desfazer a ultima acao"
    ),
    leitura=[
        "packaging.python.org -- guia oficial de empacotamento Python",
        "PEP 621 -- pyproject.toml como descritor de projeto",
        "docs.astral.sh/ruff -- documentacao do ruff",
        "semver.org -- especificacao de versionamento semantico",
    ],
))