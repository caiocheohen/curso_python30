"""Semana 4 - Dias 24 a 30: testes, sistema, concorrência, performance e projeto final."""

from nucleo.modelos import Dia, Exemplo, Exercicio, Quiz

DIAS = []

# ---------------------------------------------------------------- DIA 24
DIAS.append(Dia(
    numero=24,
    titulo="Testes automatizados: unittest, pytest e TDD",
    nivel="Avançado",
    duracao="110 min",
    objetivos=[
        "Explicar por que testes automatizados são o que permite mudar código sem medo",
        "Escrever testes com unittest (biblioteca padrão) e com pytest (padrão de mercado)",
        "Praticar o ciclo vermelho-verde-refatorar (TDD) num exemplo real",
        "Usar fixtures, parametrização e mocks para isolar o que está sendo testado",
        "Medir cobertura de testes e entender por que ela não é um objetivo em si mesma",
        "Conhecer doctest como forma de manter exemplos de documentação sempre corretos",
    ],
    teoria="""
1. Por que testar: o problema que os testes resolvem
------------------------------------------------------------
Teste automatizado não é burocracia nem "coisa de empresa grande" — é a
ferramenta que permite MUDAR código com confiança. Sem uma suíte de
testes, toda refatoração (melhorar a estrutura interna do código sem
mudar seu comportamento externo) é uma aposta: você só descobre se
quebrou algo quando um usuário (ou você mesmo, mais tarde) tropeça no bug.
Com testes, você roda a suíte depois de cada mudança e sabe, em segundos,
se o comportamento esperado continua de pé.

A "pirâmide de testes" é um modelo clássico para pensar no equilíbrio
certo: MUITOS testes de UNIDADE (rápidos, isolados, testando uma função
ou classe por vez), ALGUNS testes de INTEGRAÇÃO (verificando que peças
diferentes funcionam juntas), e POUCOS testes de PONTA A PONTA (simulando
o sistema inteiro, mais lentos e mais caros de manter). A ideia é que a
maior parte da sua confiança venha dos testes rápidos e baratos, com os
mais caros reservados para os fluxos mais críticos.

2. unittest: a biblioteca padrão para testes
--------------------------------------------------
    import unittest
    from calculadora import somar

    class TestSomar(unittest.TestCase):
        def setUp(self):                 # roda automaticamente ANTES de CADA método de teste
            self.dados = [1, 2, 3]

        def test_positivos(self):
            self.assertEqual(somar(2, 3), 5)

        def test_erro(self):
            with self.assertRaises(TypeError):
                somar("a", 1)

    if __name__ == "__main__":
        unittest.main()

    python3 -m unittest discover -v

`setUp` roda antes de CADA método `test_*`, garantindo que cada teste
comece com um estado limpo e previsível, sem depender da ordem em que os
testes são executados (que, aliás, não é garantida). As asserções mais
usadas: `assertEqual`, `assertTrue`/`assertFalse`, `assertIn`,
`assertIsNone`, `assertAlmostEqual` (essencial para comparar `float`,
retomando a imprecisão de ponto flutuante do Dia 2), `assertRaises`
(verifica que uma exceção específica é levantada) e `assertCountEqual`
(compara duas coleções ignorando a ordem).

3. pytest: o padrão de facto da comunidade
------------------------------------------------
    pip install pytest

    # test_calculadora.py
    import pytest
    from calculadora import somar, dividir

    def test_soma():
        assert somar(2, 3) == 5          # assert puro da linguagem, sem métodos especiais

    def test_divisao_por_zero():
        with pytest.raises(ZeroDivisionError):
            dividir(1, 0)

    @pytest.mark.parametrize("a,b,esperado", [(1, 1, 2), (0, 0, 0), (-1, 1, 0)])
    def test_varios(a, b, esperado):
        assert somar(a, b) == esperado

    @pytest.fixture
    def usuario():
        return {"nome": "Ana", "ativo": True}

    def test_usa_fixture(usuario):
        assert usuario["ativo"]

Embora não venha na biblioteca padrão, `pytest` se tornou o padrão de
mercado por uma razão prática: usa o `assert` NATIVO da linguagem (sem
precisar decorar métodos como `assertEqual`), e ainda assim produz
mensagens de erro detalhadas ao falhar, mostrando os valores reais
envolvidos na comparação. `@pytest.mark.parametrize` elimina a
necessidade de copiar e colar o mesmo teste várias vezes só trocando os
valores de entrada — uma única função de teste roda várias vezes, uma
para cada tupla de parâmetros fornecida. `@pytest.fixture` fornece dados
ou recursos prontos para os testes que os pedirem como parâmetro (aqui,
`usuario`), evitando repetir a mesma preparação em cada teste.

Comandos úteis na linha de comando: `pytest -v` (saída detalhada),
`pytest -k soma` (roda só testes cujo nome contém "soma"), `pytest --lf`
(roda só os que falharam na última execução — ótimo ao corrigir um bug
específico) e `pytest -x` (para na primeira falha, útil quando você só
quer o primeiro erro por vez).

4. Convenções de descoberta automática de testes
------------------------------------------------------
Tanto `unittest` quanto `pytest` seguem (por padrão) a convenção de
procurar arquivos chamados `test_*.py`, funções chamadas `test_*` e
classes chamadas `Test*`. A prática recomendada é colocar todos os
arquivos de teste numa pasta `tests/` na raiz do projeto, separada do
código de produção — isso deixa claro o que é teste e o que é
implementação, e evita que os testes acabem sendo empacotados junto com o
código de produção por engano.

5. TDD (Test-Driven Development) em três passos
------------------------------------------------------
    1. RED       escreva um teste que FALHA — ele define o comportamento desejado, antes mesmo do código existir
    2. GREEN     escreva o código MAIS SIMPLES possível que faz esse teste passar, sem se preocupar com elegância ainda
    3. REFACTOR  melhore o desenho do código, mantendo os testes verdes o tempo todo

O ganho de TDD não é apenas "ter mais cobertura de testes" — o efeito
mais valioso, na prática, é que escrever o teste PRIMEIRO obriga você a
pensar em como a função será USADA (sua API) antes de pensar em como ela
será IMPLEMENTADA por dentro. Isso tende a produzir interfaces mais
simples e mais fáceis de usar, porque você experimenta a perspectiva de
quem vai chamar a função antes de se comprometer com os detalhes internos.

6. Mocks: substituindo o que é lento, externo ou imprevisível
------------------------------------------------------------------
    from unittest.mock import patch, MagicMock

    @patch("meu_modulo.requests.get")
    def test_api(mock_get):
        mock_get.return_value.status_code = 200
        assert buscar_dados() == {...}

Um "mock" (objeto simulado) substitui temporariamente uma dependência real
por uma versão controlada, durante o teste. Isso é essencial para testar
código que depende de algo LENTO (uma chamada de rede real), EXTERNO (um
serviço de terceiros que pode estar fora do ar) ou NÃO DETERMINÍSTICO (a
hora atual, um número aleatório) — sem mock, esses testes ficariam lentos,
instáveis (passando às vezes, falhando outras) ou dependentes de recursos
fora do seu controle.

Um princípio importante: faça mock das DEPENDÊNCIAS externas da função sob
teste, nunca do próprio código que você está testando — se você "mockar"
a lógica que deveria estar sendo verificada, o teste passa a validar o
mock, não o comportamento real do seu programa.

7. Cobertura: uma bússola, não uma meta
--------------------------------------------
    pip install pytest-cov
    pytest --cov=meu_pacote --cov-report=term-missing

Cobertura mede qual PORCENTAGEM das linhas do seu código foi efetivamente
EXECUTADA durante a suíte de testes. É uma métrica útil para encontrar
áreas completamente esquecidas, mas tem uma limitação importante: 100% de
cobertura não garante qualidade nenhuma — uma linha pode ter sido
"executada" por um teste com uma asserção fraca ou ausente, sem realmente
VERIFICAR o comportamento esperado daquela linha. Trate a cobertura como
uma bússola que aponta o que ainda não foi tocado, não como um objetivo a
ser maximizado por si só.

8. doctest: exemplos de documentação que nunca ficam desatualizados
------------------------------------------------------------------------
    def dobrar(x):
        \"\"\"Dobra um número.

        >>> dobrar(4)
        8
        \"\"\"
        return x * 2

    python3 -m doctest -v modulo.py

`doctest` extrai trechos que parecem uma sessão de REPL (com `>>>`)
diretamente das docstrings e os EXECUTA como testes de verdade,
verificando se a saída documentada continua batendo com a saída real. É
uma ferramenta excelente especificamente para manter exemplos de
documentação honestos: se alguém mudar o comportamento de `dobrar` sem
atualizar a docstring, o doctest acusa a divergência automaticamente.
""",
    exemplos=[
        Exemplo(
            titulo="Suite unittest executada em memória",
            codigo='''import unittest

def eh_primo(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True

class TestPrimo(unittest.TestCase):
    def test_pequenos(self):
        self.assertTrue(eh_primo(2))
        self.assertFalse(eh_primo(1))

    def test_grandes(self):
        self.assertTrue(eh_primo(7919))
        self.assertFalse(eh_primo(7917))

resultado = unittest.TextTestRunner(verbosity=0).run(
    unittest.TestLoader().loadTestsFromTestCase(TestPrimo))
print("testes:", resultado.testsRun, "falhas:", len(resultado.failures))
''',
            explicacao="Dá para rodar a suite programaticamente e inspecionar "
                       "o objeto resultado, o que é útil para integrar testes "
                       "em ferramentas próprias, além do uso comum via terminal.",
        ),
        Exemplo(
            titulo="Ciclo TDD na prática, passo a passo",
            codigo='''# 1. RED - o teste existe ANTES da funcao (e falharia com NameError se rodado agora)
def test_slug():
    assert slug("Ola Mundo Python") == "ola-mundo-python"

# 2. GREEN - implementacao minima que faz o teste acima passar
def slug(texto):
    return texto.lower().replace(" ", "-")

# 3. REFACTOR - um novo teste revela um caso que a implementacao minima nao cobre
def test_slug_com_espacos_extras():
    assert slug("  Ola   Mundo  ") == "ola-mundo"

# a implementacao precisa evoluir para lidar com espacos multiplos e nas pontas
def slug(texto):
    return "-".join(texto.lower().split())
''',
            explicacao="Cada novo requisito entra primeiro como um teste que "
                       "falha, e só depois vira código — a ordem é o que "
                       "caracteriza TDD, não apenas 'ter testes'.",
        ),
        Exemplo(
            titulo="Parametrização evitando repetição no pytest",
            codigo='''# Sem parametrizacao, seria preciso repetir a funcao de teste tres vezes.
# Com @pytest.mark.parametrize, uma unica funcao cobre os tres casos:

# import pytest
#
# @pytest.mark.parametrize("entrada,esperado", [
#     (0, False),
#     (1, False),
#     (2, True),
#     (17, True),
# ])
# def test_eh_primo(entrada, esperado):
#     assert eh_primo(entrada) == esperado

def eh_primo(n):
    if n < 2:
        return False
    return all(n % d != 0 for d in range(2, int(n ** 0.5) + 1))

for entrada, esperado in [(0, False), (1, False), (2, True), (17, True)]:
    assert eh_primo(entrada) == esperado
print("todos os casos bateram")
''',
            explicacao="O bloco comentado mostra a sintaxe real do pytest; "
                       "a parte executável simula a mesma verificação com um "
                       "for simples, já que este curso não depende do pytest instalado.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d24e1",
            enunciado=(
                "TDD: implemente slug(texto) que devolve minúsculas, sem espaços nas\n"
                "pontas e com espaços internos (mesmo múltiplos) trocados por '-'."
            ),
            funcao="slug",
            assinatura="def slug(texto):",
            testes=[
                ("slug('Ola Mundo')", "'ola-mundo'"),
                ("slug('  Python   Puro  ')", "'python-puro'"),
                ("slug('')", "''"),
                ("slug('UM')", "'um'"),
            ],
            dica="'-'.join(texto.lower().split()) resolve todos os casos.",
        ),
        Exercicio(
            id="d24e2",
            enunciado=(
                "Escreva eh_primo(n) e rodar_testes() que monta uma TestCase com pelo\n"
                "menos 3 asserções e devolve o número de testes executados com sucesso\n"
                "(testsRun - falhas - erros)."
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
            dica="unittest.TextTestRunner(verbosity=0).run(suite) devolve um objeto com .testsRun.",
        ),
        Exercicio(
            id="d24e3",
            enunciado=(
                "Escreva dividir(a, b) que levanta ValueError com a mensagem\n"
                "'divisao por zero' quando b == 0 (e devolve a/b caso contrário)."
            ),
            funcao="dividir",
            assinatura="def dividir(a, b):",
            testes=[
                ("dividir(10, 4)", "2.5"),
                ("dividir(1, 0)", "!raise ValueError"),
                ("dividir(-6, 3)", "-2.0"),
            ],
            nivel="medio",
            dica="Cláusula de guarda no início: if b == 0: raise ValueError(...)",
        ),
    ],
    quiz=[
        Quiz("Qual a ordem correta do ciclo TDD?",
             ["Código, teste, refatoração", "Teste que falha, código mínimo, refatoração",
              "Refatoração, teste, código", "Teste, deploy, código"], 1,
             "Red (falha), green (passa com o mínimo), refactor (melhora mantendo verde)."),
        Quiz("O que significa cobertura de testes de 100%?",
             ["O código não tem bugs", "Todas as linhas foram executadas pelos testes, mas não necessariamente bem verificadas",
              "Todos os casos possíveis foram testados", "Os testes sempre passam"], 1,
             "Linha executada não é o mesmo que comportamento verificado com asserções fortes."),
        Quiz("Por que usar mock ao testar uma função que faz uma chamada de rede?",
             ["Para deixar o teste mais bonito", "Para evitar dependência de rede real, tornando o teste rápido, confiável e determinístico",
              "Porque testes nunca podem usar rede", "Mock só serve para bancos de dados"], 1,
             "Sem mock, o teste ficaria lento, instável (dependendo da rede estar disponível) e fora do controle do próprio teste."),
        Quiz("Qual a vantagem de @pytest.mark.parametrize sobre copiar e colar a mesma função de teste várias vezes?",
             ["Não há vantagem real, é só sintaxe", "Uma única função cobre vários casos, evitando duplicação e facilitando adicionar novos casos",
              "Só funciona com números", "Torna os testes mais lentos"], 1,
             "Cada tupla de parâmetros gera uma execução separada da mesma função de teste, sem repetir o corpo do teste."),
    ],
    projeto=(
        "Escolha um projeto anterior, crie a pasta tests/ e escreva uma suíte pytest "
        "com pelo menos 15 testes, incluindo parametrização, fixture e um caso de erro. Meça a cobertura."
    ),
    leitura=["docs.pytest.org", "docs.python.org/pt-br/3/library/unittest.html"],
))

# ---------------------------------------------------------------- DIA 25
DIAS.append(Dia(
    numero=25,
    titulo="Python no Linux: os, sys, subprocess, argparse e logging",
    nivel="Avançado",
    duracao="110 min",
    objetivos=[
        "Interagir com o sistema operacional através de os e sys",
        "Ler dados de um pipe do shell, tornando o script um cidadão de primeira classe no terminal",
        "Executar comandos externos com subprocess de forma segura, sem abrir brechas de injeção",
        "Criar interfaces de linha de comando profissionais com argparse",
        "Registrar eventos com logging em vez de print, e entender por que isso importa em produção",
        "Deixar um script executável e instalável no PATH do sistema",
    ],
    teoria="""
1. os e sys: a ponte com o sistema operacional
------------------------------------------------------
    import os, sys
    os.getcwd()                     diretório de trabalho atual
    os.listdir("."), os.walk(".")   navegação pelo sistema de arquivos
    os.environ.get("HOME")          lê uma variável de ambiente (None se não existir)
    os.environ["API_KEY"]           levanta KeyError se a variável não existir
    os.cpu_count()                   número de núcleos de CPU disponíveis
    os.getpid()                      identificador do processo atual

    sys.argv                        lista de argumentos de linha de comando (argv[0] é o próprio script)
    sys.exit(1)                     encerra o programa com o código de saída informado (0 = sucesso, no Linux)
    sys.stdin / sys.stdout / sys.stderr    os três fluxos padrão do processo
    sys.platform                    identifica o sistema operacional ('linux', 'darwin', 'win32')
    sys.version_info                 a versão do Python em execução, como uma tupla

Uma convenção importante no Linux (e em Unix em geral): mensagens de ERRO
devem ir para `stderr`, não para `stdout` — `print("falhou", file=sys.stderr)`.
Isso permite que o usuário redirecione a saída normal do programa para um
arquivo (`./script.py > saida.txt`) sem misturar mensagens de erro no meio
do resultado esperado, já que `stderr` continua aparecendo no terminal
mesmo quando `stdout` foi redirecionado.

2. Lendo de um pipe: integrando-se ao shell
--------------------------------------------------
    for linha in sys.stdin:
        print(linha.upper(), end="")

    cat arquivo.txt | python3 maiusculo.py

Escrever programas Python que leem de `stdin` e escrevem em `stdout` os
torna capazes de participar de PIPELINES do shell, encadeados com o
operador `|` junto de outros comandos Unix — exatamente como `grep`,
`sort` ou `wc` fazem. Essa é uma diferença de filosofia de design: em vez
de um script que só sabe processar UM arquivo específico, um programa que
lê de `stdin` funciona com qualquer fonte de dados que o shell consiga
canalizar até ele.

3. subprocess: executando outros programas com segurança
------------------------------------------------------------------
    import subprocess

    r = subprocess.run(["ls", "-la", "/tmp"],
                       capture_output=True, text=True, timeout=10, check=False)
    r.returncode, r.stdout, r.stderr

Regras de segurança e robustez que valem a pena internalizar:

- SEMPRE passe uma LISTA de argumentos separados (`["ls", "-la", "/tmp"]`),
  nunca uma string única montada por concatenação com dados vindos do
  usuário e `shell=True` — essa combinação abre uma brecha clássica de
  INJEÇÃO DE COMANDO, onde um usuário mal-intencionado poderia incluir
  `; rm -rf /` ou similar dentro do que parecia ser apenas um nome de
  arquivo;
- `check=True` faz `subprocess.run` levantar `CalledProcessError`
  automaticamente se o comando terminar com um código de saída diferente
  de zero — útil quando uma falha do comando externo deveria interromper
  seu script também;
- `text=True` decodifica a saída (que originalmente vem como bytes) para
  `str`, poupando uma conversão manual;
- sempre defina um `timeout` — sem ele, um comando externo que trave
  (aguardando entrada, por exemplo) prende seu programa indefinidamente.

4. argparse: interfaces de linha de comando profissionais
------------------------------------------------------------------
    import argparse

    p = argparse.ArgumentParser(description="Processa arquivos de log.")
    p.add_argument("arquivo", help="caminho do log")
    p.add_argument("-n", "--linhas", type=int, default=10)
    p.add_argument("-v", "--verboso", action="store_true")
    p.add_argument("--formato", choices=["json", "csv"], default="json")
    args = p.parse_args()          # ou parse_args(["a", "-n", "5"]) explicitamente, o que facilita TESTAR a CLI

Usar `argparse` em vez de analisar `sys.argv` manualmente traz uma série
de benefícios "de graça", sem código adicional: uma tela de `--help`
formatada automaticamente, validação do TIPO de cada argumento (o `type=int`
já rejeita um valor não numérico com uma mensagem clara), mensagens de
erro consistentes para argumentos ausentes ou inválidos, e o código de
saída apropriado quando a análise falha. Passar `argv` explicitamente para
`parse_args()` (em vez de deixá-lo ler `sys.argv` implicitamente) é o que
torna possível TESTAR a lógica de análise de argumentos com valores
fixos, sem depender do ambiente real de execução.

5. logging: a alternativa profissional ao print
--------------------------------------------------
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("app.log")],
    )
    log = logging.getLogger(__name__)

    log.debug("detalhe para depuracao")
    log.info("operacao concluida")
    log.warning("algo suspeito")
    log.error("falhou", exc_info=True)     # inclui o traceback completo automaticamente
    log.critical("desligando")

Os níveis de severidade, em ordem crescente, são: DEBUG < INFO < WARNING <
ERROR < CRITICAL. Configurar `level=logging.INFO` faz mensagens DEBUG
serem silenciadas automaticamente, sem precisar remover ou comentar
chamadas de log espalhadas pelo código — basta mudar essa única linha de
configuração para ajustar quanto detalhe aparece.

As vantagens de `logging` sobre `print` espalhado pelo código são
concretas, não apenas estéticas: níveis de severidade que podem ser
filtrados centralizadamente; múltiplos DESTINOS simultâneos (tela E
arquivo, por exemplo, como no `handlers=` acima); timestamp e nome do
módulo automáticos em cada linha; e a capacidade de silenciar TODO o
log de depuração em produção mudando uma única configuração, sem tocar
no restante do código.

6. Lidando com sinais e garantindo uma saída limpa
------------------------------------------------------------
    try:
        principal()
    except KeyboardInterrupt:
        print("\\ninterrompido", file=sys.stderr)
        sys.exit(130)

Capturar `KeyboardInterrupt` (disparado por Ctrl+C) permite que o
programa encerre de forma organizada — talvez salvando progresso parcial
ou exibindo uma mensagem clara — em vez de despejar um traceback completo
na tela do usuário. O código de saída `130` é a convenção Unix para
"processo interrompido pelo sinal SIGINT" (128 + o número do sinal, que é
2 para SIGINT).

7. Outras ferramentas úteis: shutil, tempfile, getpass
------------------------------------------------------------
    shutil.copy2, shutil.move, shutil.rmtree     operações de arquivo de alto nível
    shutil.which("git")                           encontra o caminho de um executável no PATH
    shutil.disk_usage(caminho)                    espaço em disco disponível
    tempfile.TemporaryDirectory(), NamedTemporaryFile()    arquivos e pastas temporários que se limpam sozinhos
    getpass.getpass("senha: ")                     lê uma entrada do terminal SEM ecoar na tela

8. Deixando um script executável e instalável
--------------------------------------------------
    #!/usr/bin/env python3
    chmod +x script.py
    sudo cp script.py /usr/local/bin/meucomando

Retomando o shebang do Dia 1, essas três linhas transformam um script
Python comum em um "comando" do sistema, executável de qualquer lugar
digitando apenas `meucomando`. Para distribuição mais séria (versionamento,
dependências, atualização), a forma recomendada é empacotar o projeto e
declarar um "entry point" através do `pyproject.toml`, tema do Dia 30.
""",
    exemplos=[
        Exemplo(
            titulo="CLI completa com argparse e logging",
            codigo='''#!/usr/bin/env python3
import argparse, logging, sys
from pathlib import Path

def montar_parser():
    p = argparse.ArgumentParser(prog="contar", description="Conta linhas de arquivos.")
    p.add_argument("arquivos", nargs="+", type=Path)
    p.add_argument("-v", "--verboso", action="store_true")
    return p

def principal(argv=None):
    args = montar_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verboso else logging.WARNING,
                        format="%(levelname)s: %(message)s")
    total = 0
    for arquivo in args.arquivos:
        if not arquivo.exists():
            logging.error("nao encontrado: %s", arquivo)
            continue
        n = len(arquivo.read_text(encoding="utf-8").splitlines())
        logging.debug("%s tem %d linhas", arquivo, n)
        total += n
    print(total)
    return 0

if __name__ == "__main__":
    sys.exit(principal())
''',
            explicacao="parse_args(argv) com o parâmetro explícito, em vez "
                       "de deixar argparse ler sys.argv sozinho, é o que "
                       "torna esta CLI testável com listas fixas de argumentos.",
        ),
        Exemplo(
            titulo="Chamando comandos do sistema com segurança",
            codigo='''import subprocess

r = subprocess.run(["uname", "-sr"], capture_output=True, text=True, timeout=5)
print("kernel:", r.stdout.strip(), "codigo:", r.returncode)

r2 = subprocess.run(["ls", "/nao_existe"], capture_output=True, text=True)
print("erro:", r2.returncode, r2.stderr.strip()[:40])
''',
            explicacao="Lista de argumentos, timeout definido e captura de "
                       "stdout/stderr separados: o padrão seguro e previsível "
                       "para chamar qualquer comando externo.",
        ),
        Exemplo(
            titulo="logging com múltiplos destinos e níveis",
            codigo='''import logging
import io

buffer = io.StringIO()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(buffer)],
    force=True,
)
log = logging.getLogger("demo")

log.debug("detalhe interno, so aparece com nivel DEBUG")
log.info("operacao concluida com sucesso")
log.warning("espaco em disco baixo")

print(buffer.getvalue())
''',
            explicacao="Trocar o destino de StreamHandler (aqui, um buffer "
                       "de memória em vez do terminal) é o mesmo mecanismo "
                       "usado para gravar logs em arquivo simultaneamente.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d25e1",
            enunciado=(
                "Escreva rodar(comando) que executa uma lista de argumentos com\n"
                "subprocess e devolve o stdout sem espaços nas pontas."
            ),
            funcao="rodar",
            assinatura="import subprocess\n\n\ndef rodar(comando):",
            testes=[
                ("rodar(['echo', 'ola'])", "'ola'"),
                ("rodar(['printf', 'a b'])", "'a b'"),
            ],
            dica="subprocess.run(..., capture_output=True, text=True).stdout.strip()",
        ),
        Exercicio(
            id="d25e2",
            enunciado=(
                "Monte um parser com argparse e escreva analisar(argv) que devolve a\n"
                "tupla (arquivo, linhas, verboso). Opções: posicional 'arquivo',\n"
                "-n/--linhas (int, padrão 10) e -v/--verboso (flag)."
            ),
            funcao="analisar",
            assinatura="import argparse\n\n\ndef analisar(argv):",
            testes=[
                ("analisar(['log.txt'])", "('log.txt', 10, False)"),
                ("analisar(['a.txt', '-n', '5', '-v'])", "('a.txt', 5, True)"),
                ("analisar(['b.txt', '--linhas', '3'])", "('b.txt', 3, False)"),
            ],
            nivel="dificil",
            dica="action='store_true' para a flag; parse_args(argv) recebe a lista.",
        ),
        Exercicio(
            id="d25e3",
            enunciado=(
                "Escreva tamanho_legivel(bytes_) convertendo para B, KB, MB, GB ou TB\n"
                "com 1 casa decimal (base 1024). Ex.: 1536 -> '1.5 KB'."
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
            dica="Percorra as unidades dividindo por 1024 enquanto o valor for >= 1024.",
        ),
    ],
    quiz=[
        Quiz("Por que evitar shell=True no subprocess quando há entrada de usuário envolvida?",
             ["É mais lento assim", "Permite injeção de comandos maliciosos se a entrada não for sanitizada",
              "Não funciona no Linux", "Impede a captura da saída"], 1,
             "Passar uma lista de argumentos evita que o shell interprete caracteres especiais inseridos pelo usuário."),
        Quiz("Qual a vantagem prática de logging sobre print espalhado pelo código?",
             ["logging produz um código mais curto", "Níveis de severidade, múltiplos destinos, timestamp automático e desligamento centralizado",
              "logging colore automaticamente a saída do terminal", "logging é mais rápido de executar que print"], 1,
             "logging separa o diagnóstico interno da saída principal do programa, com controle fino sobre o que é registrado e onde."),
        Quiz("Por que passar argv explicitamente para parse_args(argv) em vez de deixar argparse ler sys.argv sozinho?",
             ["Não faz diferença nenhuma", "Torna a lógica de análise de argumentos testável com listas fixas, sem depender do ambiente real",
              "É a única forma de usar flags como -v", "argparse não funciona sem esse parâmetro"], 1,
             "Testes automatizados (Dia 24) podem chamar a função de análise com argumentos simulados, sem precisar rodar o script de verdade."),
        Quiz("Para onde mensagens de erro deveriam ir, seguindo a convenção Unix?",
             ["sempre para stdout", "para stderr, para não se misturar com a saída normal redirecionada", "para um arquivo de log obrigatoriamente", "não há convenção sobre isso"], 1,
             "Isso permite redirecionar stdout para um arquivo sem perder as mensagens de erro, que continuam visíveis no terminal."),
    ],
    projeto=(
        "Crie organizador.py: uma CLI que varre um diretório e move arquivos para subpastas "
        "por extensão, com --dry-run, --verboso, logging em arquivo e código de saída correto."
    ),
    leitura=["docs.python.org/pt-br/3/library/argparse.html", "docs.python.org/pt-br/3/howto/logging.html"],
))
# ---------------------------------------------------------------- DIA 26
DIAS.append(Dia(
    numero=26,
    titulo="Expressões regulares e processamento de texto",
    nivel="Avançado",
    duracao="100 min",
    objetivos=[
        "Escrever padrões com metacaracteres e quantificadores, gulosos e preguiçosos",
        "Usar grupos, grupos nomeados e alternativas para extrair dados estruturados",
        "Aplicar search, findall, finditer e sub com função de substituição",
        "Usar flags para tornar padrões mais legíveis e mais flexíveis",
        "Reconhecer lookahead e lookbehind para casar contexto sem consumi-lo",
        "Saber quando NÃO usar regex, e o que usar no lugar",
    ],
    teoria=r"""
1. O módulo re: as funções essenciais
------------------------------------------
    import re
    re.search(padrao, texto)      encontra a PRIMEIRA ocorrência em qualquer posição -> Match ou None
    re.match(padrao, texto)       como search, mas ANCORADO no início da string
    re.fullmatch(padrao, texto)   exige que a string INTEIRA case com o padrão
    re.findall(padrao, texto)     lista de strings (ou de tuplas, se o padrão tem grupos)
    re.finditer(padrao, texto)    iterador de objetos Match, preservando as posições de cada ocorrência
    re.sub(padrao, troca, texto)  substituição de todas as ocorrências
    re.split(padrao, texto)       divide a string usando o padrão como separador
    re.compile(padrao)            pré-compila o padrão, útil para reutilizar em laços sem recompilar toda vez

Use SEMPRE uma string CRUA (raw string, Dia 4) para o padrão: `r"\d+"`.
Sem o prefixo `r`, o Python processaria `\d` como um escape de string
ANTES mesmo do módulo `re` ver o padrão — e como `\d` não é um escape
reconhecido pela linguagem, o resultado seria inconsistente entre versões
e ambientes. `r"\d+"` garante que a barra invertida chegue intacta ao
motor de regex, que tem seu próprio significado para ela.

2. Metacaracteres: o vocabulário básico de um padrão
------------------------------------------------------------
    .        qualquer caractere, exceto quebra de linha
    \d \D    um dígito / um caractere que NÃO é dígito
    \w \W    letra, número ou underscore ([a-zA-Z0-9_]) / o oposto disso
    \s \S    espaço em branco (espaço, tab, quebra de linha) / o oposto
    \b       fronteira de palavra (posição entre um \w e um não-\w)
    ^ $      início / fim da string (ou de cada linha, com a flag re.M)
    [abc]    classe de caracteres: casa QUALQUER UM destes três
    [^abc]   negação da classe: casa qualquer caractere QUE NÃO seja estes
    [a-z]    faixa de caracteres
    a|b      alternativa: casa "a" OU "b"
    \.       ponto literal (escapado, porque . sozinho é um metacaractere)

3. Quantificadores: quantas vezes o anterior se repete
------------------------------------------------------------
    *        0 ou mais repetições          +      1 ou mais repetições
    ?        0 ou 1 repetição               {3}    exatamente 3 repetições
    {2,5}    de 2 a 5 repetições             {2,}   2 ou mais repetições

Por padrão, quantificadores são GULOSOS (greedy): tentam casar o MÁXIMO
possível antes de recuar se necessário. Acrescentar `?` logo depois de um
quantificador o torna PREGUIÇOSO (lazy), casando o MÍNIMO possível:

    re.findall(r"<.+>", "<a><b>")     -> ['<a><b>']    (guloso: engoliu tudo até o último '>')
    re.findall(r"<.+?>", "<a><b>")    -> ['<a>', '<b>']  (preguiçoso: parou no primeiro '>' de cada vez)

Esse é um dos erros mais comuns ao escrever regex pela primeira vez:
esperar comportamento preguiçoso e receber o guloso por padrão, capturando
mais texto do que se pretendia.

4. Grupos: capturando partes específicas do padrão
------------------------------------------------------------
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})", "hoje: 28/07/2026")
    m.group(0)     '28/07/2026'   (o casamento INTEIRO, sempre no índice 0)
    m.group(1)     '28'           (o primeiro grupo entre parênteses)
    m.groups()     ('28', '07', '2026')     (todos os grupos, como tupla)
    m.span()       as posições (início, fim) do casamento inteiro na string

GRUPOS NOMEADOS deixam o padrão muito mais legível, especialmente em
padrões complexos, permitindo acessar cada parte pelo NOME em vez de um
número posicional fácil de confundir:

    m = re.search(r"(?P<dia>\d{2})/(?P<mes>\d{2})/(?P<ano>\d{4})", texto)
    m.group("ano")
    m.groupdict()      # {'dia': '28', 'mes': '07', 'ano': '2026'}

Um grupo NÃO CAPTURANTE, `(?:...)`, agrupa parte do padrão (por exemplo,
para aplicar um quantificador a um trecho inteiro) SEM guardar esse trecho
como um grupo numerado — útil quando você precisa de agrupamento
estrutural, mas não do valor capturado.

Na substituição (`re.sub`), grupos capturados podem ser referenciados com
`\1`, `\2` (posicionais) ou `\g<nome>` (nomeados):

    re.sub(r"(\d{2})/(\d{2})/(\d{4})", r"\3-\2-\1", "28/07/2026")
    # '2026-07-28'  -- os grupos sao reorganizados na substituicao

5. Flags: ajustando o comportamento do motor de regex
------------------------------------------------------------
    re.I   ignora diferença entre maiúsculas e minúsculas
    re.M   faz ^ e $ casarem o início/fim de CADA LINHA, não só da string inteira
    re.S   faz . também casar quebras de linha (por padrão, . não casa \n)
    re.X   (verbose) permite espaços em branco e comentários dentro do próprio padrão, para legibilidade

    padrao = re.compile(
        r'''
        (?P<usuario>[\w.+-]+)   # parte antes do @
        @
        (?P<dominio>[\w-]+\.\w+)
        ''', re.X)

A flag `re.X` é particularmente valiosa para padrões longos e complexos:
ela permite quebrar o padrão em várias linhas, adicionar espaços para
legibilidade e até comentários explicando cada trecho — sem esses
recursos, um padrão complexo vira uma sequência ilegível de símbolos numa
única linha.

6. Lookahead e lookbehind: casando contexto sem consumi-lo
------------------------------------------------------------------
    (?=...)   lookahead positivo: SEGUIDO de (mas o que vem depois não entra no casamento)
    (?!...)   lookahead negativo: NÃO seguido de
    (?<=...)  lookbehind positivo: PRECEDIDO de
    (?<!...)  lookbehind negativo: NÃO precedido de

    re.findall(r"\d+(?= reais)", "10 reais e 20 dolares")   -> ['10']
    # o "(?= reais)" exige que " reais" venha em seguida, mas essa parte
    # nao aparece no resultado capturado -- so o numero e devolvido

Um exemplo clássico de uso combinado: validar uma senha com múltiplos
requisitos, todos verificados a partir do MESMO ponto de início (por isso
lookaheads, que não avançam a posição de leitura):
`r"^(?=.*[A-Z])(?=.*\d).{8,}$"` exige pelo menos uma maiúscula, pelo menos
um dígito, e comprimento mínimo de 8 caracteres — tudo isso sem que os
lookaheads "consumam" caracteres da string sendo verificada.

7. Quando NÃO usar regex
------------------------------
- para analisar HTML, XML ou JSON: use um PARSER de verdade para esses
  formatos (`html.parser`, o módulo `json`, bibliotecas como `lxml`) — a
  estrutura aninhada e as regras de escape desses formatos não se prestam
  bem a expressões regulares, que não lidam naturalmente com aninhamento
  arbitrário;
- para buscas simples: `"x" in texto`, `.startswith()`, `.split()` (Dia 4)
  são mais claros e mais rápidos que uma regex equivalente, quando o
  problema não exige de fato um padrão;
- para validar e-mail de forma "100% correta": a especificação real do
  formato de e-mail é surpreendentemente complexa e cheia de casos
  extremos; na prática, é mais produtivo validar apenas o formato básico
  com uma regex simples e confirmar a validade de fato enviando um e-mail
  de confirmação.

Regex é poderosa e ilegível quase na mesma proporção: comente padrões
complexos (usando `re.X`) e, sempre que possível, escreva testes
automatizados (Dia 24) para eles — é fácil um padrão parecer correto e
esconder um caso extremo não coberto.

8. Uma nota sobre desempenho e segurança
------------------------------------------------
Compile o padrão FORA de um laço (com `re.compile`) quando ele for reusado
muitas vezes, para não pagar o custo de compilação repetidamente. Prefira
classes de caracteres (`[abc]`) a longas cadeias de alternativas (`a|b|c`)
quando possível. E evite ANINHAR quantificadores de forma ambígua, como
`r"(a+)+"` — certos padrões desse tipo podem causar uma EXPLOSÃO
COMBINATÓRIA de tentativas de casamento em certas entradas, um problema
conhecido como ReDoS (Regular Expression Denial of Service), capaz de
travar um programa processando uma entrada aparentemente inofensiva.
""",
    exemplos=[
        Exemplo(
            titulo="Extraindo dados estruturados de um log",
            codigo=r'''import re

log = """2026-07-28 10:15:02 ERRO usuario=ana codigo=500
2026-07-28 10:15:44 INFO usuario=bia codigo=200
2026-07-28 10:16:01 ERRO usuario=caio codigo=503"""

padrao = re.compile(
    r"(?P<data>\d{4}-\d{2}-\d{2}) (?P<hora>[\d:]+) "
    r"(?P<nivel>\w+) usuario=(?P<usuario>\w+) codigo=(?P<codigo>\d+)"
)
for m in padrao.finditer(log):
    if m.group("nivel") == "ERRO":
        print(m.group("hora"), m.group("usuario"), m.group("codigo"))
''',
            explicacao="Grupos nomeados transformam o padrão em documentação: "
                       "m.group('usuario') é muito mais claro que m.group(4).",
        ),
        Exemplo(
            titulo="Substituição com função em vez de string fixa",
            codigo=r'''import re

def mascarar(m):
    numero = m.group(0)
    return numero[:4] + "*" * (len(numero) - 8) + numero[-4:]

texto = "cartao 1234567812345678 aprovado"
print(re.sub(r"\b\d{16}\b", mascarar, texto))
''',
            explicacao="re.sub aceita uma FUNÇÃO como substituição, chamada "
                       "para cada ocorrência encontrada — útil quando a "
                       "substituição depende do próprio texto casado.",
        ),
        Exemplo(
            titulo="Guloso versus preguiçoso, lado a lado",
            codigo=r'''import re

html = "<b>negrito</b> e <i>italico</i>"

guloso = re.findall(r"<.+>", html)
preguicoso = re.findall(r"<.+?>", html)

print("guloso:    ", guloso)       # ['<b>negrito</b> e <i>italico</i>'] -- tudo de uma vez
print("preguicoso:", preguicoso)   # ['<b>', '</b>', '<i>', '</i>'] -- cada tag separada
''',
            explicacao="O ? depois do quantificador muda drasticamente o "
                       "resultado — este é o erro mais comum de quem "
                       "escreve regex pela primeira vez para casar tags.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d26e1",
            enunciado="Escreva extrair_emails(texto) devolvendo a lista de e-mails encontrados.",
            funcao="extrair_emails",
            assinatura="import re\n\n\ndef extrair_emails(texto):",
            testes=[
                ("extrair_emails('fale com ana@x.com ou bia@y.com.br')",
                 "['ana@x.com', 'bia@y.com.br']"),
                ("extrair_emails('nenhum aqui')", "[]"),
            ],
            nivel="medio",
            dica=r"Algo como r'[\w.+-]+@[\w-]+\.[\w.]+' resolve os casos comuns.",
        ),
        Exercicio(
            id="d26e2",
            enunciado=(
                "Escreva converter_datas(texto) trocando todas as datas no formato\n"
                "DD/MM/AAAA por AAAA-MM-DD."
            ),
            funcao="converter_datas",
            assinatura="import re\n\n\ndef converter_datas(texto):",
            testes=[
                ("converter_datas('venceu em 28/07/2026 e 01/01/2027')",
                 "'venceu em 2026-07-28 e 2027-01-01'"),
                ("converter_datas('sem data')", "'sem data'"),
            ],
            nivel="medio",
            dica=r"re.sub(r'(\d{2})/(\d{2})/(\d{4})', r'\3-\2-\1', texto)",
        ),
        Exercicio(
            id="d26e3",
            enunciado=(
                "Escreva validar_telefone(numero) aceitando os formatos brasileiros\n"
                "'(21) 99999-8888' e '21999998888' (11 dígitos com o 9)."
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
            dica="Uma opção robusta: remova tudo que não é dígito e verifique se sobraram 11.",
        ),
    ],
    quiz=[
        Quiz("Por que usar string crua r'' nos padrões regex?",
             ["É mais rápido em tempo de execução", "Evita que o Python processe as barras invertidas como escapes de string antes do re vê-las",
              "Permite acentos no padrão", "É uma exigência obrigatória da sintaxe do módulo re"], 1,
             "Sem raw string, '\\d' poderia ser interpretado de forma inconsistente, já que \\d não é um escape reconhecido pela linguagem."),
        Quiz("Qual a diferença entre .+ e .+? em um padrão regex?",
             ["Nenhuma diferença prática", "O segundo é preguiçoso e casa o mínimo possível de caracteres",
              "O segundo é sintaxe inválida", "O primeiro casa apenas letras, nunca números"], 1,
             "O ? após um quantificador o torna não guloso (lazy), parando assim que a condição mínima é satisfeita."),
        Quiz("Por que usar (?P<nome>...) em vez de apenas (...) para capturar grupos?",
             ["Grupos nomeados são mais rápidos de processar", "Tornam o padrão mais legível, acessando cada parte por nome em vez de posição numérica",
              "Só grupos nomeados podem ser usados em re.sub", "Não há diferença funcional real"], 1,
             "m.group('ano') é muito mais claro e menos propenso a erro que m.group(3) num padrão complexo."),
        Quiz("Por que evitar padrões como r'(a+)+' aninhando quantificadores de forma ambígua?",
             ["Eles nunca funcionam corretamente", "Podem causar uma explosão combinatória de tentativas de casamento (ReDoS) em certas entradas",
              "São apenas mais lentos, sem risco real", "Só afetam padrões muito curtos"], 1,
             "Certas entradas podem fazer o motor de regex testar exponencialmente muitas combinações, travando o programa."),
    ],
    projeto=(
        "Escreva um analisador de logs de servidor: extraia IP, data, método, rota e status "
        "com grupos nomeados, e gere um relatório com as 10 rotas mais acessadas e a taxa de erros 5xx."
    ),
    leitura=["docs.python.org/pt-br/3/howto/regex.html", "regex101.com"],
))

# ---------------------------------------------------------------- DIA 27
DIAS.append(Dia(
    numero=27,
    titulo="Concorrência: threads, processos e o GIL",
    nivel="Avançado",
    duracao="110 min",
    objetivos=[
        "Entender o que é o GIL e suas consequências práticas para threads em Python",
        "Escolher entre threads e processos com base no tipo de trabalho (I/O ou CPU)",
        "Usar ThreadPoolExecutor e ProcessPoolExecutor da API concurrent.futures",
        "Identificar condições de corrida e protegê-las com Lock",
        "Usar Queue para comunicação segura entre threads, em vez de compartilhar estado diretamente",
        "Aplicar a regra de ouro: medir antes de adicionar complexidade de concorrência",
    ],
    teoria="""
1. O GIL em uma frase, e o que ele realmente significa na prática
------------------------------------------------------------------------------
O CPython (a implementação padrão do Python, que você tem instalada) tem
um bloqueio interno chamado GIL (Global Interpreter Lock) que permite a
execução de apenas UM bytecode Python por vez, mesmo que seu programa
tenha várias THREADS rodando "ao mesmo tempo".

A consequência prática, que organiza toda a decisão deste dia:

    trabalho de I/O (rede, disco, banco de dados)   -> THREADS ajudam MUITO
    trabalho de CPU (cálculo pesado, processar imagem) -> THREADS NÃO ajudam; use PROCESSOS

O porquê é sutil, mas importante: enquanto uma thread está ESPERANDO por
uma operação de I/O (uma resposta de rede, uma leitura de disco), ela
LIBERA o GIL, permitindo que outra thread rode nesse meio tempo. Mas
durante um CÁLCULO puro em Python, a thread MANTÉM o GIL o tempo todo,
impedindo qualquer outra thread de avançar — por isso threads não trazem
ganho real de velocidade para trabalho intensivo de CPU, apenas para
trabalho que passa a maior parte do tempo esperando por algo externo.

(O Python 3.13 introduziu um modo experimental sem GIL, mas o raciocínio
acima continua sendo o padrão prático para o código que a grande maioria
dos programas escreve hoje, incluindo este curso.)

2. concurrent.futures: a API recomendada para a maioria dos casos
------------------------------------------------------------------------------
    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

    with ThreadPoolExecutor(max_workers=8) as executor:
        resultados = list(executor.map(baixar, urls))       # a ordem dos resultados é preservada

    with ThreadPoolExecutor() as executor:
        futuros = [executor.submit(baixar, u) for u in urls]
        for f in as_completed(futuros):                     # processa conforme cada um termina, não na ordem de envio
            try:
                print(f.result())
            except Exception as e:
                print("falhou:", e)

O bloco `with` do executor GARANTE que todas as tarefas submetidas
terminem antes de sair do bloco — não é preciso chamar `.join()`
manualmente como no `threading` de mais baixo nível. Um detalhe fácil de
esquecer, mas crítico: exceções que ocorrem DENTRO de uma tarefa não são
propagadas imediatamente — elas ficam guardadas no objeto `Future`
correspondente, e só são relevantadas quando você chama `.result()` sobre
ele. Ignorar esse resultado (nunca chamar `.result()` nem verificar
erros) faz falhas desaparecerem silenciosamente.

3. threading direto: quando você precisa de controle mais fino
------------------------------------------------------------------------
    import threading

    t = threading.Thread(target=funcao, args=(1,), daemon=True)
    t.start()
    t.join(timeout=5)

`concurrent.futures` cobre a maioria dos casos de forma mais simples, mas
o módulo `threading` de baixo nível continua sendo útil quando você
precisa de controle mais fino — por exemplo, um laço de fundo de longa
duração, ou um "watchdog" que monitora algo continuamente em segundo
plano, casos que não se encaixam bem no modelo de "submeta uma tarefa e
espere o resultado" dos executors.

4. Condição de corrida e Lock: protegendo estado compartilhado
------------------------------------------------------------------------
    contador = 0
    def incrementar():
        global contador
        for _ in range(100_000):
            contador += 1        # esta linha NÃO é atômica: envolve ler, somar e gravar

Se duas threads executam `contador += 1` "ao mesmo tempo", pode acontecer
de as duas LEREM o mesmo valor antigo de `contador` antes de qualquer uma
gravar o novo valor — resultando em um incremento PERDIDO. Esse fenômeno é
chamado de CONDIÇÃO DE CORRIDA (race condition), e é um dos bugs mais
difíceis de reproduzir de forma consistente, porque depende do momento
exato (imprevisível) em que cada thread é interrompida pelo sistema.

A solução é um `Lock` (também chamado de mutex), que garante que apenas
UMA thread por vez execute o trecho protegido:

    lock = threading.Lock()
    with lock:
        contador += 1

Outros primitivos de sincronização da biblioteca padrão incluem `RLock`
(um lock que a mesma thread pode adquirir novamente sem travar a si
mesma), `Semaphore` (limita quantas threads podem acessar algo
simultaneamente — não apenas uma), `Event` (sinalização simples entre
threads) e `Condition`/`Barrier` (coordenação mais elaborada entre várias
threads).

5. Queue: comunicação entre threads sem compartilhar estado diretamente
------------------------------------------------------------------------------
    from queue import Queue
    fila = Queue()
    fila.put(item)
    item = fila.get(); ...; fila.task_done()
    fila.join()

`queue.Queue` já é THREAD-SAFE por construção — internamente, ela já
implementa os locks necessários para que múltiplas threads possam colocar
(`put`) e retirar (`get`) itens sem risco de condição de corrida. O
princípio de design que essa ferramenta encoraja é: em vez de várias
threads compartilharem e modificarem a mesma variável diretamente (o que
exige locks manuais e é fácil de errar), prefira que elas se COMUNIQUEM
por MENSAGENS através de uma fila — um padrão conhecido como
produtor/consumidor, muito mais fácil de raciocinar corretamente.

6. Multiprocessing: paralelismo real para trabalho de CPU
------------------------------------------------------------------------
    with ProcessPoolExecutor() as ex:
        resultados = list(ex.map(calculo_pesado, dados))

Diferente de threads (que compartilham o mesmo processo e, portanto, o
mesmo GIL), cada PROCESSO criado por `ProcessPoolExecutor` tem seu próprio
interpretador Python e sua própria memória, completamente independentes.
Isso traz consequências importantes:

- ganha-se PARALELISMO REAL para trabalho de CPU, aproveitando múltiplos
  núcleos de verdade — o problema que threads não resolvem, dado o GIL;
- os dados trocados entre processos precisam ser SERIALIZÁVEIS (via
  `pickle`), já que processos não compartilham memória diretamente;
- o custo de CRIAR um processo novo e TRANSFERIR dados entre processos é
  significativamente mais alto que criar uma thread — por isso,
  multiprocessing só compensa quando o trabalho em si é grande o
  suficiente para diluir esse custo fixo;
- no Linux, o método padrão de criação de processo é `fork`, e é
  importante proteger o código de nível de módulo com
  `if __name__ == "__main__":` (Dia 13), para que ele não seja
  reexecutado indevidamente em cada processo filho criado.

7. Escolhendo a ferramenta certa para cada situação
------------------------------------------------------------------------
    I/O com muitas esperas (rede, disco)         -> asyncio (Dia 28) ou threads
    trabalho intensivo de CPU                      -> processos (ProcessPoolExecutor)
    muitas tarefas independentes e curtas          -> executor.map (threads ou processos, conforme o tipo de trabalho)
    pipeline no estilo produtor/consumidor         -> Queue + threads

8. A regra de ouro: meça antes de adicionar concorrência
------------------------------------------------------------------
Concorrência multiplica a complexidade do código e a dificuldade de
depurar problemas (condições de corrida só aparecem às vezes,
dependendo de timing) — por isso, a prática recomendada é só adotar
threads ou processos quando o GANHO de desempenho já foi comprovado por
MEDIÇÃO real (retomando o Dia 29 adiante: meça, não adivinhe), não por
intuição sobre "isso deveria ser mais rápido em paralelo".
""",
    exemplos=[
        Exemplo(
            titulo="Threads para I/O simulado",
            codigo='''import time
from concurrent.futures import ThreadPoolExecutor

def tarefa_io(n):
    time.sleep(0.2)          # simula espera de rede
    return n * 2

inicio = time.perf_counter()
with ThreadPoolExecutor(max_workers=10) as ex:
    resultados = list(ex.map(tarefa_io, range(10)))
print(resultados, f"{time.perf_counter()-inicio:.2f}s")   # ~0.2s, não 2s
''',
            explicacao="Dez esperas de 0.2s acontecem em paralelo, porque "
                       "cada thread libera o GIL enquanto aguarda o sleep, "
                       "permitindo que as outras avancem nesse meio tempo.",
        ),
        Exemplo(
            titulo="Lock evitando condição de corrida",
            codigo='''import threading

contador = 0
lock = threading.Lock()

def incrementar(vezes):
    global contador
    for _ in range(vezes):
        with lock:
            contador += 1

threads = [threading.Thread(target=incrementar, args=(50_000,)) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(contador)      # sempre 200000, garantido pelo lock
''',
            explicacao="Sem o lock, o total variaria de execução para "
                       "execução, quase sempre ficando abaixo de 200000 "
                       "por causa de incrementos perdidos na condição de corrida.",
        ),
        Exemplo(
            titulo="Threads não ajudam trabalho de CPU puro",
            codigo='''import time
from concurrent.futures import ThreadPoolExecutor

def calculo_pesado(n):
    return sum(i * i for i in range(n))

valores = [2_000_000] * 4

inicio = time.perf_counter()
sequencial = [calculo_pesado(v) for v in valores]
print("sequencial:", f"{time.perf_counter()-inicio:.2f}s")

inicio = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as ex:
    paralelo = list(ex.map(calculo_pesado, valores))
print("com threads:", f"{time.perf_counter()-inicio:.2f}s")
# os dois tempos ficam parecidos -- o GIL impede o ganho que threads
# trariam para trabalho de I/O; aqui seria necessario ProcessPoolExecutor
''',
            explicacao="Este é o experimento que comprova na prática por "
                       "que trabalho de CPU precisa de processos, não "
                       "threads, para ganhar velocidade real.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d27e1",
            enunciado=(
                "Escreva processar_paralelo(valores) que usa ThreadPoolExecutor para\n"
                "aplicar uma função (que dorme 0.01s e devolve o quadrado) e devolve\n"
                "a lista de resultados NA ORDEM de entrada."
            ),
            funcao="processar_paralelo",
            assinatura=("import time\nfrom concurrent.futures import ThreadPoolExecutor"
                        "\n\n\ndef processar_paralelo(valores):"),
            testes=[
                ("processar_paralelo([1, 2, 3])", "[1, 4, 9]"),
                ("processar_paralelo([])", "[]"),
            ],
            nivel="medio",
            dica="executor.map preserva a ordem; envolva em list().",
        ),
        Exercicio(
            id="d27e2",
            enunciado=(
                "Escreva contar_seguro(n_threads, incrementos) que soma com várias\n"
                "threads usando Lock e devolve o total (deve ser exato sempre)."
            ),
            funcao="contar_seguro",
            assinatura="import threading\n\n\ndef contar_seguro(n_threads, incrementos):",
            testes=[
                ("contar_seguro(4, 10000)", "40000"),
                ("contar_seguro(1, 5)", "5"),
                ("contar_seguro(0, 100)", "0"),
            ],
            nivel="dificil",
            dica="Use uma variável nonlocal ou uma lista de 1 posição protegida pelo lock.",
        ),
        Exercicio(
            id="d27e3",
            enunciado=(
                "Escreva produtor_consumidor(itens) que usa queue.Queue: uma thread\n"
                "produtora coloca os itens e uma consumidora soma tudo. Devolva a soma."
            ),
            funcao="produtor_consumidor",
            assinatura="import threading\nfrom queue import Queue\n\n\ndef produtor_consumidor(itens):",
            testes=[
                ("produtor_consumidor([1, 2, 3, 4])", "10"),
                ("produtor_consumidor([])", "0"),
            ],
            nivel="dificil",
            dica="Use um sentinela (None) para avisar o consumidor de que acabou.",
        ),
    ],
    quiz=[
        Quiz("Para trabalho pesado de CPU (não I/O), o que geralmente usar em Python?",
             ["Threads", "Processos (ProcessPoolExecutor)", "asyncio", "Tanto faz, o resultado é o mesmo"], 1,
             "O GIL impede que threads tragam paralelismo real de bytecode; processos têm seus próprios interpretadores independentes."),
        Quiz("Por que `contador += 1` não é seguro quando várias threads o executam ao mesmo tempo?",
             ["É uma operação lenta", "Envolve ler, somar e gravar em passos separados — pode ser interrompida no meio por outra thread",
              "Precisa obrigatoriamente de global para funcionar", "Só funciona corretamente com números pequenos"], 1,
             "Sem um lock protegendo essa sequência de passos, incrementos concorrentes podem se perder."),
        Quiz("Por que threads ajudam trabalho de I/O mas não trabalho de CPU puro em Python?",
             ["Threads nunca ajudam em nada", "Uma thread libera o GIL enquanto espera I/O, mas o mantém durante cálculo puro",
              "CPU é sempre mais rápida que I/O de qualquer forma", "Isso depende só da versão do sistema operacional"], 1,
             "É exatamente essa liberação do GIL durante a espera que permite outras threads avançarem nesse intervalo."),
        Quiz("Por que preferir queue.Queue a threads compartilhando e modificando a mesma variável diretamente?",
             ["Queue é sempre mais rápida", "Queue já é thread-safe internamente, evitando a necessidade de gerenciar locks manualmente para cada acesso",
              "Variáveis compartilhadas nunca funcionam entre threads", "Queue não pode ser usada com Lock"], 1,
             "O padrão de comunicação por mensagens (produtor/consumidor) é mais fácil de raciocinar corretamente que estado compartilhado direto."),
    ],
    projeto=(
        "Escreva um verificador de links: dada uma lista de URLs, cheque todas em paralelo com "
        "ThreadPoolExecutor (timeout, tratamento de erro por item) e compare o tempo com a versão sequencial."
    ),
    leitura=["docs.python.org/pt-br/3/library/concurrent.futures.html", "docs.python.org/pt-br/3/library/threading.html"],
))

# ---------------------------------------------------------------- DIA 28
DIAS.append(Dia(
    numero=28,
    titulo="Programação assíncrona com asyncio",
    nivel="Avançado",
    duracao="110 min",
    objetivos=[
        "Diferenciar concorrência cooperativa (asyncio) de concorrência preemptiva (threads)",
        "Escrever e executar corrotinas com async/await",
        "Executar tarefas concorrentemente com gather e TaskGroup",
        "Controlar timeout e limitar concorrência com semáforo",
        "Reconhecer e evitar o erro mais grave em asyncio: bloquear o event loop",
        "Saber quando asyncio é a ferramenta certa, comparado a threads e processos",
    ],
    teoria="""
1. A ideia central: concorrência cooperativa em uma única thread
------------------------------------------------------------------------
`asyncio` implementa concorrência COOPERATIVA rodando inteiramente em UMA
única thread: enquanto uma corrotina está esperando por I/O, ela
DEVOLVE VOLUNTARIAMENTE o controle ao "event loop" (o laço de eventos
central), que aproveita esse tempo para rodar outra corrotina. Não existe
paralelismo real de CPU aqui — o que existe é a ELIMINAÇÃO DO TEMPO
OCIOSO gasto esperando, redirecionando-o para outro trabalho útil.

A distinção-chave entre os dois modelos de concorrência vistos neste
curso: com THREADS (Dia 27), o sistema operacional decide, de forma
PREEMPTIVA, quando interromper uma thread para dar vez a outra — você não
controla exatamente quando isso acontece. Com `asyncio`, é o SEU PRÓPRIO
CÓDIGO que decide, de forma COOPERATIVA, em cada `await`, quando "ceder a
vez" — o controle é explícito e previsível, o que elimina inteiramente a
classe de bugs de condição de corrida vista no Dia 27 (já que só uma
coisa roda por vez, e as trocas só acontecem em pontos marcados
explicitamente com `await`).

2. Corrotinas: funções que podem pausar e retomar
------------------------------------------------------------
    import asyncio

    async def buscar(nome):
        print("iniciando", nome)
        await asyncio.sleep(1)          # cede o controle ao event loop aqui
        return f"{nome} pronto"

    asyncio.run(buscar("a"))            # ponto de entrada único de um programa asyncio

`async def` declara uma FUNÇÃO CORROTINA. Um detalhe que surpreende quem
está começando: chamar `buscar("a")` SEM `await` não executa nada do
corpo — apenas cria e devolve um OBJETO corrotina, ainda não iniciado
(muito parecido com chamar uma função geradora sem consumi-la, Dia 20).
`await` só pode aparecer DENTRO de uma função declarada com `async def` —
usá-lo fora disso é um erro de sintaxe.

3. Concorrência de verdade: gather em vez de await sequencial
------------------------------------------------------------------------
    async def principal():
        # sequencial: as tres esperas se SOMAM, totalizando 3 segundos
        a = await buscar("a"); b = await buscar("b"); c = await buscar("c")

        # concorrente: as tres esperas se SOBREPOEM, totalizando ~1 segundo
        a, b, c = await asyncio.gather(buscar("a"), buscar("b"), buscar("c"))

    asyncio.run(principal())

A diferença entre as duas abordagens é a explicação central de todo o
capítulo: `await` sozinho, um atrás do outro, executa cada corrotina até o
FIM antes de começar a próxima — se cada uma espera 1 segundo, o total é
3 segundos. `asyncio.gather` inicia todas ao mesmo tempo e as deixa
avançar concorrentemente, aproveitando o tempo de espera de cada uma para
avançar as outras — o tempo total fica próximo do MAIOR tempo individual,
não da SOMA de todos.

`gather(..., return_exceptions=True)` muda o comportamento padrão diante
de erros: em vez de interromper tudo assim que uma corrotina falha, ele
devolve a EXCEÇÃO como se fosse um valor de retorno normal na posição
correspondente, permitindo que você trate cada resultado individualmente.

4. Tasks e TaskGroup: agendando trabalho explicitamente
------------------------------------------------------------------
    tarefa = asyncio.create_task(buscar("x"))     # AGENDA a execução imediatamente, sem esperar ainda
    resultado = await tarefa                       # só aqui espera pelo resultado

    async with asyncio.TaskGroup() as tg:         # Python 3.11+, geralmente preferível a gather
        t1 = tg.create_task(buscar("a"))
        t2 = tg.create_task(buscar("b"))
    # ao SAIR do bloco `async with`, todas as tarefas já terminaram;
    # se uma delas falhar, as demais são canceladas automaticamente

`asyncio.create_task` inicia a execução da corrotina imediatamente (sem
esperar por um `await` explícito), permitindo que ela avance em segundo
plano enquanto outro código roda. `TaskGroup` (mais recente que `gather`)
oferece uma semântica mais segura em caso de erro: se qualquer tarefa
dentro do grupo falhar, todas as outras são automaticamente canceladas, em
vez de continuarem rodando "esquecidas" em segundo plano.

5. Timeout e limite de concorrência
----------------------------------------
    async with asyncio.timeout(2):        # Python 3.11+
        await operacao_lenta()

    resultado = await asyncio.wait_for(operacao_lenta(), timeout=2)    # forma equivalente, disponível antes do 3.11

    sem = asyncio.Semaphore(10)
    async def limitado(url):
        async with sem:                   # no máximo 10 corrotinas executando este bloco ao mesmo tempo
            return await baixar(url)

Limitar a concorrência com um semáforo é essencial ao lidar com centenas
ou milhares de requisições simultâneas: sem esse limite, seu programa
poderia abrir tantas conexões simultâneas que sobrecarregaria o servidor
de destino (ou até seus próprios recursos locais) — o semáforo garante
que, no máximo, um número fixo de operações rode ao mesmo tempo, mesmo
que muito mais tarefas estejam "esperando a vez".

6. O pecado capital do asyncio: bloquear o event loop
------------------------------------------------------------------
    time.sleep(1)          # PARA TUDO -- nenhuma outra corrotina avanca durante este segundo inteiro
    await asyncio.sleep(1) # correto: cede o controle, permitindo outras corrotinas avancarem

    requests.get(url)      # bloqueante -> prefira bibliotecas assincronas como aiohttp/httpx
    open(...).read()       # bloqueante -> aiofiles, ou delegue a uma thread:

    resultado = await asyncio.to_thread(funcao_bloqueante, arg)

Como todo o modelo do `asyncio` depende de corrotinas CEDEREM o controle
voluntariamente nos pontos de `await`, uma única chamada BLOQUEANTE
tradicional (uma função síncrona que não cede controle nenhum, como
`time.sleep` comum, ou uma requisição de rede feita com uma biblioteca
síncrona) CONGELA o event loop inteiro por sua duração — nenhuma outra
corrotina consegue avançar nesse meio tempo, mesmo que existam dezenas
esperando. `asyncio.to_thread` é o mecanismo de escape para código
bloqueante que você não pode reescrever de forma assíncrona: ele delega a
chamada para uma thread separada, liberando o event loop principal
enquanto aguarda o resultado.

7. Iteração assíncrona
--------------------------
    async def gerar():
        for i in range(3):
            await asyncio.sleep(0.1)
            yield i

    async for x in gerar():
        print(x)

Assim como existem geradores comuns (Dia 20), existem GERADORES
ASSÍNCRONOS: funções que combinam `async def` com `yield`, percorridas com
`async for` em vez de `for` comum. Também existem gerenciadores de
contexto assíncronos (`async with`, para recursos cuja entrada/saída
também envolve espera de I/O) e compreensões assíncronas, seguindo o
mesmo padrão de "adicionar `async` na frente" das construções síncronas
equivalentes.

8. Quando usar asyncio, comparado com threads e processos
------------------------------------------------------------------
    milhares de conexões de rede simultâneas         -> asyncio (uma única thread lida com todas)
    poucas chamadas bloqueantes, em bibliotecas sem suporte assíncrono   -> threads
    cálculo pesado de CPU                              -> processos

O ecossistema construído especificamente para `asyncio` inclui frameworks
web como FastAPI, bibliotecas de requisições HTTP como `aiohttp` e
`httpx`, drivers de banco de dados como `asyncpg`, e clientes de cache
como `redis.asyncio` — todos desenhados para NUNCA bloquear o event loop,
completando o ecossistema necessário para aproveitar de fato os
benefícios da programação assíncrona em uma aplicação real.
""",
    exemplos=[
        Exemplo(
            titulo="Sequencial versus concorrente",
            codigo='''import asyncio, time

async def tarefa(nome, segundos):
    await asyncio.sleep(segundos)
    return f"{nome} ({segundos}s)"

async def principal():
    inicio = time.perf_counter()
    resultados = await asyncio.gather(
        tarefa("a", 0.3), tarefa("b", 0.3), tarefa("c", 0.3)
    )
    print(resultados, f"{time.perf_counter()-inicio:.2f}s")   # ~0.3s

asyncio.run(principal())
''',
            explicacao="Três esperas de 0.3s custam apenas 0.3s no total, "
                       "porque gather permite que as três avancem "
                       "concorrentemente em vez de uma atrás da outra.",
        ),
        Exemplo(
            titulo="Limitando a concorrência com semáforo",
            codigo='''import asyncio

async def baixar(i, sem):
    async with sem:
        await asyncio.sleep(0.1)
        return i

async def principal():
    sem = asyncio.Semaphore(3)          # no maximo 3 por vez
    return await asyncio.gather(*(baixar(i, sem) for i in range(9)))

print(asyncio.run(principal()))
''',
            explicacao="Sem o semáforo, as nove tarefas rodariam todas ao "
                       "mesmo tempo — com ele, apenas 3 executam "
                       "simultaneamente, protegendo o recurso de destino.",
        ),
        Exemplo(
            titulo="O que acontece ao bloquear o event loop por engano",
            codigo='''import asyncio, time

async def rapida(nome):
    await asyncio.sleep(0.1)
    print(nome, "terminou")

async def bloqueia_tudo():
    time.sleep(0.5)     # ERRADO dentro de uma corrotina: bloqueia o loop inteiro
    print("bloqueante terminou")

async def principal():
    inicio = time.perf_counter()
    await asyncio.gather(rapida("a"), rapida("b"), bloqueia_tudo())
    print(f"{time.perf_counter()-inicio:.2f}s")
    # em vez de ~0.5s (o maior tempo), o total fica proximo de 0.6s+,
    # porque time.sleep impediu "a" e "b" de progredirem durante ele

asyncio.run(principal())
''',
            explicacao="Mesmo dentro de asyncio.gather, uma única chamada "
                       "bloqueante como time.sleep (em vez de await "
                       "asyncio.sleep) anula boa parte do ganho esperado.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d28e1",
            enunciado=(
                "Escreva a corrotina dobrar(x) (com um await asyncio.sleep(0)) e a\n"
                "função síncrona executar(x) que a roda com asyncio.run e devolve o valor."
            ),
            funcao="executar",
            assinatura="import asyncio\n\n\nasync def dobrar(x):\n    ...\n\n\ndef executar(x):",
            testes=[
                ("executar(5)", "10"),
                ("executar(0)", "0"),
                ("asyncio.iscoroutinefunction(dobrar)", "True"),
            ],
            dica="return asyncio.run(dobrar(x))",
        ),
        Exercicio(
            id="d28e2",
            enunciado=(
                "Escreva executar_todos(valores) que usa asyncio.gather para dobrar\n"
                "todos os valores concorrentemente e devolve a lista de resultados."
            ),
            funcao="executar_todos",
            assinatura=("import asyncio\n\n\nasync def dobrar(x):\n    await asyncio.sleep(0)\n"
                        "    return x * 2\n\n\ndef executar_todos(valores):"),
            testes=[
                ("executar_todos([1, 2, 3])", "[2, 4, 6]"),
                ("executar_todos([])", "[]"),
            ],
            nivel="medio",
            dica="Crie uma corrotina interna async def principal(): return await asyncio.gather(*(...)).",
        ),
        Exercicio(
            id="d28e3",
            enunciado=(
                "Escreva com_timeout(segundos, limite) que roda asyncio.sleep(segundos)\n"
                "com asyncio.wait_for(limite) e devolve 'ok' ou 'timeout'."
            ),
            funcao="com_timeout",
            assinatura="import asyncio\n\n\ndef com_timeout(segundos, limite):",
            testes=[
                ("com_timeout(0.01, 1)", "'ok'"),
                ("com_timeout(1, 0.01)", "'timeout'"),
            ],
            nivel="dificil",
            dica="Capture asyncio.TimeoutError (ou TimeoutError) em volta do wait_for.",
        ),
    ],
    quiz=[
        Quiz("O que acontece se você chamar time.sleep(5) (não asyncio.sleep) dentro de uma corrotina?",
             ["Nada de especial acontece", "Bloqueia o event loop inteiro por 5 segundos, impedindo qualquer outra corrotina de avançar",
              "Gera um erro de sintaxe imediatamente", "Roda automaticamente em outra thread"], 1,
             "asyncio depende de cessão voluntária de controle; time.sleep não cede nada, travando tudo."),
        Quiz("Qual a diferença prática entre 'await f(); await g()' e 'await asyncio.gather(f(), g())'?",
             ["Nenhuma diferença de comportamento", "gather executa as duas corrotinas concorrentemente; await sequencial soma os tempos de espera",
              "gather sempre é mais lento", "gather só aceita uma corrotina por vez"], 1,
             "await sozinho espera cada uma terminar antes de iniciar a próxima; gather inicia todas e deixa avançarem juntas."),
        Quiz("Qual a diferença central entre a concorrência de threads e a do asyncio?",
             ["Não há diferença nenhuma entre os dois modelos", "Threads são preemptivas (o SO decide quando trocar); asyncio é cooperativo (o código decide, em cada await)",
              "asyncio sempre usa múltiplos núcleos de CPU", "Threads nunca podem rodar código de I/O"], 1,
             "Essa diferença de controle é o que elimina condições de corrida em asyncio: só uma coisa roda por vez, com trocas em pontos explícitos."),
        Quiz("Para que serve asyncio.Semaphore num cenário de milhares de requisições?",
             ["Para acelerar cada requisição individual", "Para limitar quantas operações rodam concorrentemente ao mesmo tempo, protegendo o recurso de destino",
              "Para ordenar os resultados", "Semaphore só funciona com threading, não com asyncio"], 1,
             "Sem esse limite, todas as tarefas tentariam rodar ao mesmo tempo, potencialmente sobrecarregando o servidor ou o próprio programa."),
    ],
    projeto=(
        "Escreva um raspador assíncrono: dada uma lista de URLs, faça as requisições com httpx/aiohttp "
        "limitando a 10 simultâneas, com timeout e retentativa, e grave os resultados em JSON."
    ),
    leitura=["docs.python.org/pt-br/3/library/asyncio.html", "PEP 492"],
))
# ---------------------------------------------------------------- DIA 29
DIAS.append(Dia(
    numero=29,
    titulo="Desempenho: complexidade, medição e otimização",
    nivel="Avançado",
    duracao="100 min",
    objetivos=[
        "Estimar a complexidade de um algoritmo usando a notação O grande",
        "Conhecer o custo real das operações mais comuns em listas, dicts e sets no CPython",
        "Medir desempenho com timeit e cProfile antes de qualquer otimização",
        "Aplicar as otimizações que costumam valer a pena, e reconhecer as que não valem",
        "Saber quando Python simplesmente não é a ferramenta certa para o problema",
        "Internalizar a ordem correta: funcione, teste, meça, otimize o gargalo real, meça de novo",
    ],
    teoria="""
1. Notação O grande: como o tempo cresce com o tamanho da entrada
------------------------------------------------------------------------------
    O(1)        tempo constante: acesso a índice, dict[chave], x in set
    O(log n)    cresce muito devagar: busca binária (Dia 12)
    O(n)        cresce proporcionalmente: percorrer uma lista, x in lista
    O(n log n)  o melhor possível para ordenação por comparação: sort()
    O(n**2)     cresce com o quadrado: laços aninhados sobre a mesma coleção
    O(2**n)     cresce exponencialmente: recursão sem memoização (fibonacci ingênuo, Dia 21)

A notação O grande descreve como o TEMPO de execução cresce conforme o
TAMANHO da entrada (`n`) aumenta — não é uma medida de tempo absoluto (em
segundos), mas de TAXA DE CRESCIMENTO. Um algoritmo O(n) processando 10
elementos pode ser mais lento, em segundos, que um O(n²) processando 5
elementos — a notação O só importa de verdade quando `n` cresce
significativamente.

O erro mais comum de desempenho encontrado em código Python real NÃO é
"a linguagem é lenta" — é um `x in lista` escondido DENTRO de um laço
`for`, transformando silenciosamente um algoritmo que parecia O(n) em um
O(n²) real, porque cada checagem de pertencimento percorre a lista
inteira de novo.

2. Custo real das estruturas de dados no CPython
------------------------------------------------------------------------
    lista:  acesso por índice O(1) | append O(1) | insert(0)/pop(0) O(n) | `in` O(n)
    dict:   get/set/`in` O(1) em média
    set:    add/`in` O(1) em média
    deque:  appendleft/popleft O(1)   <- use como fila, em vez de lista (Dia 8)
    heapq:  push/pop O(log n)          <- fila de prioridade
    string: imutável; concatenar repetidamente em laço com += é O(n²) no total, use "".join(partes) em vez disso

Esta tabela é, na prática, o "manual de referência rápida" mais útil deste
capítulo: antes de escrever um laço que faz buscas repetidas, checar
"devo usar lista, dict ou set aqui?" já resolve a maioria dos problemas de
desempenho antes mesmo deles aparecerem.

3. Meça, não adivinhe: as ferramentas certas
------------------------------------------------------------------------
    import timeit
    timeit.timeit("sum(range(1000))", number=10000)

    python3 -m timeit -s "d={i:i for i in range(1000)}" "999 in d"

    import cProfile
    cProfile.run("principal()", sort="cumtime")

    python3 -m cProfile -s tottime script.py

`timeit` mede o tempo de um trecho PEQUENO e ISOLADO de código, rodando-o
muitas vezes para reduzir o ruído de medições individuais — ideal para
comparar duas formas alternativas de fazer a mesma coisa. `cProfile` mede
um PROGRAMA INTEIRO (ou uma função complexa), mostrando quanto tempo foi
gasto em CADA função chamada — essencial para descobrir ONDE, dentro de um
programa grande, o tempo está de fato sendo gasto, em vez de otimizar por
palpite.

Para análise mais fina, `line_profiler` mede tempo LINHA POR LINHA dentro
de uma função específica; para investigar consumo de MEMÓRIA (não tempo),
`tracemalloc` (da biblioteca padrão) e `memory_profiler` cumprem esse
papel:

    import tracemalloc
    tracemalloc.start()
    ...
    print(tracemalloc.get_traced_memory())

4. Otimizações que costumam valer a pena, em ordem de impacto
------------------------------------------------------------------------------
    a) trocar a estrutura de dados (lista -> set/dict, quando o uso é busca repetida);
    b) melhorar o ALGORITMO em si (transformar O(n²) em O(n log n) ou O(n));
    c) memoizar com @lru_cache (Dia 21) o que é puro (sempre o mesmo resultado para os mesmos argumentos) e repetitivo;
    d) preferir funções embutidas e compreensões (Dia 10) — elas rodam em código C internamente, mais rápido que um laço Python equivalente;
    e) usar "".join() em vez de += repetido para concatenar strings (Dia 4);
    f) evitar trabalho desnecessário: filtre cedo, saia cedo (cláusulas de guarda, Dia 5), prefira geradores (Dia 20) quando não precisa materializar tudo;
    g) para processamento numérico em massa, usar `numpy` costuma trazer ganhos de ordens de grandeza sobre laços Python puros.

Esses itens estão ordenados aproximadamente por RELAÇÃO custo-benefício:
trocar uma estrutura de dados costuma exigir poucas linhas e trazer ganho
enorme; já as micro-otimizações da próxima seção exigem reescrever código
inteiro para um ganho quase imperceptível.

5. Micro-otimizações que raramente importam na prática
------------------------------------------------------------------------
Trocar `for` por `while`, remover uma variável temporária "para economizar
memória", usar `map()` em vez de uma compreensão equivalente — esses
ajustes trazem ganho MARGINAL de desempenho, mas custo ALTO em
legibilidade do código. A citação clássica de Donald Knuth resume bem o
princípio: "otimização prematura é a raiz de todo o mal" — otimizar antes
de saber ONDE está o gargalo real é, na melhor das hipóteses, desperdício
de esforço, e na pior, torna o código mais difícil de manter sem ganho
real algum.

A ordem correta de trabalho, sempre: primeiro FUNCIONE (o código faz o
que deveria); depois TESTE (Dia 24, para garantir que continue
funcionando); depois MEÇA (com as ferramentas da seção 3); só então
OTIMIZE especificamente o GARGALO identificado pela medição; e MEÇA DE
NOVO, para confirmar que a otimização realmente trouxe o ganho esperado
— e não introduziu um bug novo no processo.

6. Quando Python puro simplesmente não basta
------------------------------------------------------------------------
    numpy / pandas / polars      processamento numérico e de tabelas em escala, com operações vetorizadas em C
    numba (@jit) / cython        compilam trechos críticos de Python para código de máquina
    ctypes / cffi / PyO3         permitem chamar código C ou Rust diretamente
    multiprocessing               distribui trabalho entre todos os núcleos de CPU disponíveis (Dia 27)
    PyPy                          uma implementação alternativa de Python com compilação just-in-time (JIT)

Para a imensa maioria dos programas do dia a dia, Python puro (com boas
escolhas de estrutura de dados e algoritmo) já é rápido o suficiente. Essa
lista existe para os casos, relativamente raros, em que a medição
comprova que o gargalo está no próprio interpretador Python e não há mais
o que otimizar dentro dele.

7. Uma nota sobre memória, não só tempo
------------------------------------------------------------------------
    __slots__ (Dia 17) reduz o consumo de memória em classes com muitas instâncias
    geradores (Dia 20) em vez de listas, quando não é necessário guardar tudo de uma vez
    array.array, para sequências grandes de números de um único tipo (mais compacto que uma lista comum)
    sys.getsizeof(obj) mostra o tamanho RASO de um objeto em bytes (não conta o que ele referencia internamente)
""",
    exemplos=[
        Exemplo(
            titulo="O(n**2) virando O(n) com uma troca de estrutura",
            codigo='''import time

def comuns_lento(a, b):
    return [x for x in a if x in b]          # b e lista -> cada 'in' e O(m), total O(n*m)

def comuns_rapido(a, b):
    conjunto = set(b)                        # O(m), pago uma unica vez
    return [x for x in a if x in conjunto]   # cada 'in' agora e O(1), total O(n)

a = list(range(20000)); b = list(range(10000, 30000))
for f in (comuns_lento, comuns_rapido):
    t = time.perf_counter(); f(a, b)
    print(f.__name__, f"{time.perf_counter()-t:.3f}s")
''',
            explicacao="Uma única linha (transformar b em set) muda a "
                       "ordem de grandeza do algoritmo inteiro, sem "
                       "precisar reescrever mais nada.",
        ),
        Exemplo(
            titulo="Concatenação de strings: += repetido versus join",
            codigo='''import timeit

lento = """
s = ""
for i in range(10000):
    s += str(i)
"""
rapido = """
partes = [str(i) for i in range(10000)]
s = "".join(partes)
"""
print("+=  :", round(timeit.timeit(lento, number=50), 3))
print("join:", round(timeit.timeit(rapido, number=50), 3))
''',
            explicacao="Cada += cria uma string inteiramente NOVA (strings "
                       "são imutáveis, Dia 4); join calcula o tamanho final "
                       "e aloca a memória uma única vez.",
        ),
        Exemplo(
            titulo="Perfilando para descobrir onde o tempo realmente vai",
            codigo='''import cProfile
import pstats
import io

def trabalho_rapido():
    return sum(range(1000))

def trabalho_lento():
    total = 0
    for i in range(200000):
        total += i
    return total

def principal():
    trabalho_rapido()
    trabalho_lento()

buffer = io.StringIO()
perfil = cProfile.Profile()
perfil.enable()
principal()
perfil.disable()

stats = pstats.Stats(perfil, stream=buffer).sort_stats("cumulative")
stats.print_stats(3)
print(buffer.getvalue()[:400])
''',
            explicacao="cProfile revela QUAL função consumiu mais tempo, "
                       "em vez de você precisar adivinhar olhando o código "
                       "e cronometrar manualmente cada trecho suspeito.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d29e1",
            enunciado=(
                "Escreva interseccao_rapida(a, b) devolvendo a lista dos elementos de\n"
                "`a` que também estão em `b`, preservando a ordem de `a`, sem repetir,\n"
                "e com complexidade O(n + m)."
            ),
            funcao="interseccao_rapida",
            assinatura="def interseccao_rapida(a, b):",
            testes=[
                ("interseccao_rapida([1, 2, 3, 2], [2, 3, 9])", "[2, 3]"),
                ("interseccao_rapida([], [1])", "[]"),
                ("interseccao_rapida([5, 5], [5])", "[5]"),
            ],
            nivel="medio",
            dica="Converta b em set e use outro set para controlar o que já foi incluído.",
        ),
        Exercicio(
            id="d29e2",
            enunciado=(
                "Escreva fib(n) com memoização (lru_cache ou dicionário próprio),\n"
                "capaz de calcular fib(80) instantaneamente. fib(0)=0, fib(1)=1."
            ),
            funcao="fib",
            assinatura="from functools import lru_cache\n\n\n@lru_cache(maxsize=None)\ndef fib(n):",
            testes=[
                ("fib(10)", "55"),
                ("fib(0)", "0"),
                ("fib(80)", "23416728348467685"),
            ],
            nivel="medio",
            dica="A recursão ingênua já funciona — o cache faz o resto.",
        ),
        Exercicio(
            id="d29e3",
            enunciado=(
                "Escreva top_n(texto, n) devolvendo a lista das n palavras mais\n"
                "frequentes como tuplas (palavra, contagem), em ordem decrescente."
            ),
            funcao="top_n",
            assinatura="from collections import Counter\n\n\ndef top_n(texto, n):",
            testes=[
                ("top_n('a b a c a b', 2)", "[('a', 3), ('b', 2)]"),
                ("top_n('', 3)", "[]"),
                ("top_n('x', 5)", "[('x', 1)]"),
            ],
            nivel="medio",
            dica="Counter(texto.split()).most_common(n) já devolve o formato pedido.",
        ),
    ],
    quiz=[
        Quiz("Qual a complexidade de `x in lista` e `x in set`, respectivamente?",
             ["O(1) e O(1)", "O(n) e O(1) em média", "O(n) e O(n)", "O(log n) e O(1)"], 1,
             "set usa hashing para localizar o elemento diretamente; lista precisa percorrer item a item no pior caso."),
        Quiz("Qual deveria ser o primeiro passo antes de otimizar qualquer código?",
             ["Reescrever partes críticas em C", "Medir e encontrar o gargalo real com ferramentas como cProfile",
              "Trocar todo for por while", "Adicionar threads ou processos imediatamente"], 1,
             "Sem medição, o esforço de otimização frequentemente recai sobre trechos que já eram rápidos o suficiente."),
        Quiz("Por que 's += str(i)' repetido em laço é mais lento que '\"\".join(partes)'?",
             ["+= é sintaxe inválida em laços", "Cada += cria uma string nova inteira, já que strings são imutáveis; join aloca uma vez só",
              "join só funciona com números", "Não há diferença de desempenho real entre os dois"], 1,
             "A imutabilidade das strings (Dia 4) torna cada += uma cópia completa; join evita essas cópias repetidas."),
        Quiz("O que a notação O grande realmente descreve?",
             ["O tempo exato de execução em segundos", "Como o tempo de execução cresce conforme o tamanho da entrada aumenta",
              "A quantidade de memória RAM disponível", "A versão do Python necessária"], 1,
             "É uma medida de taxa de crescimento, não de tempo absoluto — por isso não diz nada sobre entradas pequenas isoladamente."),
    ],
    projeto=(
        "Pegue um script seu que demore mais de 1 segundo, perfile com cProfile, identifique "
        "o gargalo, otimize e documente o antes/depois com números."
    ),
    leitura=["docs.python.org/pt-br/3/library/profile.html", "wiki.python.org/moin/TimeComplexity"],
))

# ---------------------------------------------------------------- DIA 30
DIAS.append(Dia(
    numero=30,
    titulo="Projeto final: estrutura, empacotamento e boas práticas",
    nivel="Avançado",
    duracao="130 min",
    objetivos=[
        "Estruturar um projeto Python seguindo o layout profissional com src/",
        "Escrever um pyproject.toml e instalar o projeto em modo editável",
        "Configurar ferramentas de qualidade (linter, formatador, tipos, testes) e integração contínua",
        "Gerenciar segredos e configuração sem versioná-los por engano",
        "Empacotar e distribuir um projeto Python no Linux",
        "Sintetizar os 30 dias num checklist prático para o projeto final do curso",
    ],
    teoria="""
1. Estrutura recomendada de um projeto (layout src)
------------------------------------------------------------
    meu_projeto/
        pyproject.toml
        README.md
        LICENSE
        .gitignore
        src/
            meu_pacote/
                __init__.py
                cli.py
                modelos.py
                servicos.py
        tests/
            test_modelos.py
        docs/

O layout com uma pasta `src/` intermediária (em vez de colocar o pacote
direto na raiz do projeto) resolve um problema sutil, mas real: sem
`src/`, é fácil que os testes importem acidentalmente o código do
DIRETÓRIO ATUAL (onde você está rodando os testes) em vez do pacote
efetivamente INSTALADO no ambiente virtual — um erro clássico que
mascara problemas reais de empacotamento, porque "funciona na minha
máquina" mesmo quando a instalação de verdade estaria quebrada para outra
pessoa.

2. pyproject.toml: a configuração central do projeto moderno
------------------------------------------------------------------------
    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"

    [project]
    name = "meu-pacote"
    version = "0.1.0"
    description = "Faz algo útil"
    readme = "README.md"
    requires-python = ">=3.10"
    dependencies = ["requests>=2.31"]

    [project.optional-dependencies]
    dev = ["pytest", "mypy", "ruff"]

    [project.scripts]
    meucomando = "meu_pacote.cli:principal"

    [tool.ruff]
    line-length = 100

`pyproject.toml` (formalizado pelas PEP 518 e PEP 621) unificou o que
antes era espalhado por `setup.py`, `setup.cfg` e `requirements.txt`
separados — hoje é o arquivo único e padrão para descrever nome, versão,
dependências e configuração de ferramentas do projeto. A seção
`[project.scripts]` é particularmente valiosa: ela declara um "entry
point" (`meucomando`), que faz o comando existir automaticamente no PATH
do ambiente virtual assim que o pacote é instalado — sem precisar do
`chmod +x` e do shebang manual vistos no Dia 25.

Instalação em modo de DESENVOLVIMENTO:

    python3 -m venv .venv && source .venv/bin/activate
    pip install -e ".[dev]"

O `-e` (editable) instala o pacote de forma que mudanças no código-fonte
tenham efeito IMEDIATO, sem precisar reinstalar a cada alteração — o
`[dev]` entre colchetes instala também as dependências opcionais
declaradas em `optional-dependencies.dev` (aqui, pytest, mypy e ruff).

3. Ferramentas de qualidade que compõem um fluxo de trabalho sólido
------------------------------------------------------------------------------
    ruff check . && ruff format .     linter + formatador (rápido; substitui a combinação flake8+black+isort)
    mypy src/                          checagem estática de tipos (Dia 23)
    pytest --cov=src                   testes e cobertura (Dia 24)
    pre-commit install                 roda automaticamente essas checagens antes de CADA commit

`ruff`, escrito em Rust, tornou-se o padrão emergente da comunidade por
combinar em uma única ferramenta, muito rápida, o que antes exigia três
ferramentas separadas (um linter, um formatador e um organizador de
imports). `pre-commit` automatiza a execução dessas checagens no exato
momento do commit, prevenindo que código com problemas óbvios (estilo
inconsistente, erros de tipo simples) sequer entre no histórico do
repositório.

4. Git no dia a dia de um projeto
--------------------------------------
    git init && git add -A && git commit -m "feat: primeira versao"
    git switch -c feature/x
    .gitignore: .venv/, __pycache__/, *.pyc, .pytest_cache/, dist/, .env

Uma regra que não admite exceção: NUNCA versione segredos (senhas, tokens
de API, chaves privadas) diretamente no repositório — mesmo removendo o
arquivo depois, ele permanece no HISTÓRICO do git, acessível a qualquer
um com acesso ao repositório. A prática recomendada é usar variáveis de
AMBIENTE para valores sensíveis, e versionar apenas um arquivo
`.env.example` (sem valores reais) mostrando quais variáveis o projeto
espera encontrar.

5. Configuração e segredos em tempo de execução
------------------------------------------------------------------
    import os
    TOKEN = os.environ["API_TOKEN"]          # falha ALTO (KeyError) se a variável faltar — comportamento correto
    DEBUG = os.getenv("DEBUG", "0") == "1"   # usa um valor padrão explícito quando a variável está ausente

Retomando o princípio do Dia 15 ("falhe cedo e alto"): usar
`os.environ["CHAVE"]` (colchetes) para configuração OBRIGATÓRIA é
deliberado — se a variável de ambiente não estiver definida, o programa
falha imediatamente com uma mensagem clara, em vez de continuar rodando
com um valor `None` silencioso que só causaria um erro confuso mais
adiante. Já `os.getenv("CHAVE", padrao)` é apropriado quando existe um
valor padrão razoável para o caso da variável estar ausente.

6. Integração contínua com GitHub Actions (esqueleto)
------------------------------------------------------------------
    on: [push, pull_request]
    jobs:
      testes:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with: {python-version: "3.12"}
          - run: pip install -e ".[dev]"
          - run: ruff check . && mypy src/ && pytest

Um workflow de CI (integração contínua) roda essas checagens
automaticamente a CADA push ou pull request, antes mesmo de alguém
revisar o código manualmente — funcionando como uma rede de segurança
que pega problemas óbvios (testes quebrados, erros de tipo, violações de
estilo) antes que cheguem à branch principal do projeto.

7. Empacotamento e distribuição no Linux
------------------------------------------------------------------
    python3 -m build                 gera os arquivos dist/*.whl e dist/*.tar.gz, os formatos padrão de distribuição
    twine upload dist/*              publica esses arquivos no PyPI (o repositório público de pacotes Python)
    pipx install meu-pacote          instala CLIs Python em ambientes isolados automaticamente, sem conflitar com outros projetos
    Docker: FROM python:3.12-slim + pip install .    empacota o projeto inteiro, com suas dependências, numa imagem de container
    systemd: um "unit file" permite rodar o projeto como um serviço de fundo gerenciado pelo próprio sistema operacional Linux

8. Checklist prático para o projeto final
------------------------------------------------------------
    [ ] resolve um problema real seu, não um exercício artificial
    [ ] estrutura de pacote com src/ e tests/, seguindo o padrão deste dia
    [ ] CLI com argparse e uma tela de --help decente (Dia 25)
    [ ] persistência de dados (JSON, CSV ou SQLite)
    [ ] tratamento de erros com exceções próprias (Dia 15)
    [ ] type hints em todo o código público (Dia 23)
    [ ] pelo menos 15 testes passando (Dia 24)
    [ ] README com instalação, uso e exemplos
    [ ] logging configurável em vez de print (Dia 25)
    [ ] versionado no git, com commits descritivos ao longo do desenvolvimento

9. O que estudar depois destes 30 dias
------------------------------------------
    Web: FastAPI, Django, Flask
    Dados: pandas, polars, matplotlib, scikit-learn
    Banco de dados: sqlite3, SQLAlchemy, psycopg
    Automação: Playwright, paramiko, Ansible
    Infraestrutura: Docker, systemd, cron
    Fundamentos mais profundos: estruturas de dados avançadas, SQL, redes, design de sistemas

O melhor próximo passo, depois de qualquer curso — inclusive este — é
sempre o mesmo: escrever um programa que VOCÊ vai efetivamente usar toda
semana. Ler documentação enquanto se constrói algo real e útil ensina
mais, de forma duradoura, do que qualquer sequência de exercícios
fechados — é exatamente por isso que o projeto final pede um problema
seu, não mais um enunciado artificial.
""",
    exemplos=[
        Exemplo(
            titulo="Esqueleto de CLI instalável, com subcomandos",
            codigo='''# src/tarefas/cli.py
import argparse
import json
import sys
from pathlib import Path

ARQUIVO = Path.home() / ".tarefas.json"

def carregar() -> list[dict]:
    if not ARQUIVO.exists():
        return []
    return json.loads(ARQUIVO.read_text(encoding="utf-8"))

def salvar(tarefas: list[dict]) -> None:
    ARQUIVO.write_text(json.dumps(tarefas, ensure_ascii=False, indent=2),
                       encoding="utf-8")

def principal(argv=None) -> int:
    p = argparse.ArgumentParser(prog="tarefas")
    sub = p.add_subparsers(dest="comando", required=True)
    add = sub.add_parser("add"); add.add_argument("titulo")
    sub.add_parser("listar")
    ok = sub.add_parser("concluir"); ok.add_argument("indice", type=int)

    args = p.parse_args(argv)
    tarefas = carregar()

    if args.comando == "add":
        tarefas.append({"titulo": args.titulo, "feita": False})
        salvar(tarefas)
    elif args.comando == "listar":
        for i, t in enumerate(tarefas):
            print(f"{i} [{'x' if t['feita'] else ' '}] {t['titulo']}")
    elif args.comando == "concluir":
        tarefas[args.indice]["feita"] = True
        salvar(tarefas)
    return 0

if __name__ == "__main__":
    sys.exit(principal())
''',
            explicacao="Subcomandos com add_subparsers seguem o mesmo "
                       "padrão de CLIs conhecidas como git (git commit, "
                       "git push) — cada subcomando com seus próprios argumentos.",
        ),
        Exemplo(
            titulo="Comparando versões corretamente",
            codigo='''def versao_tupla(v: str) -> tuple[int, ...]:
    return tuple(int(p) for p in v.split("."))

print(versao_tupla("1.10.0") > versao_tupla("1.9.9"))   # True
print(sorted(["1.0.0", "1.10.0", "1.2.0"], key=versao_tupla))
''',
            explicacao="Comparar as versões como TEXTO puro daria a "
                       "resposta errada ('1.10.0' < '1.9.9' alfabeticamente, "
                       "porque '1' < '9'); convertendo para tupla de int, a "
                       "comparação numérica funciona corretamente.",
        ),
        Exemplo(
            titulo="Configuração via variáveis de ambiente, falhando cedo",
            codigo='''import os

def carregar_configuracao():
    modo_debug = os.getenv("DEBUG", "0") == "1"
    try:
        limite_conexoes = int(os.getenv("LIMITE_CONEXOES", "10"))
    except ValueError:
        raise ValueError("LIMITE_CONEXOES precisa ser um numero inteiro") from None
    return {"debug": modo_debug, "limite_conexoes": limite_conexoes}

print(carregar_configuracao())
# Uma chave OBRIGATORIA (sem valor padrao razoavel) usaria colchetes:
# TOKEN = os.environ["API_TOKEN"]  -- levanta KeyError se faltar, de proposito
''',
            explicacao="Valores com padrão razoável usam getenv com "
                       "fallback; valores realmente obrigatórios usam "
                       "colchetes, para falhar alto e cedo se estiverem ausentes.",
        ),
    ],
    exercicios=[
        Exercicio(
            id="d30e1",
            enunciado=(
                "Escreva comparar_versoes(a, b) devolvendo 1 se a > b, -1 se a < b e 0\n"
                "se forem iguais (formato 'X.Y.Z')."
            ),
            funcao="comparar_versoes",
            assinatura="def comparar_versoes(a, b):",
            testes=[
                ("comparar_versoes('1.10.0', '1.9.9')", "1"),
                ("comparar_versoes('1.0.0', '1.0.0')", "0"),
                ("comparar_versoes('0.9.0', '1.0.0')", "-1"),
            ],
            nivel="medio",
            dica="Converta em tuplas de int e compare diretamente.",
        ),
        Exercicio(
            id="d30e2",
            enunciado=(
                "Escreva serializar(tarefas) e desserializar(texto) usando JSON, de modo\n"
                "que desserializar(serializar(x)) == x."
            ),
            funcao="serializar",
            assinatura="import json\n\n\ndef serializar(tarefas):\n    ...\n\n\ndef desserializar(texto):",
            testes=[
                ("desserializar(serializar([{'t': 'a', 'feita': False}]))",
                 "[{'t': 'a', 'feita': False}]"),
                ("desserializar(serializar([]))", "[]"),
                ("isinstance(serializar([]), str)", "True"),
            ],
            dica="json.dumps e json.loads, com ensure_ascii=False.",
        ),
        Exercicio(
            id="d30e3",
            enunciado=(
                "Projeto integrador: escreva GerenciadorTarefas com adicionar(titulo),\n"
                "concluir(indice), pendentes() e resumo() -> '2/3 concluidas'.\n"
                "concluir com índice inválido deve levantar IndexError."
            ),
            funcao="GerenciadorTarefas",
            assinatura="class GerenciadorTarefas:\n    def __init__(self):",
            testes=[
                ("(lambda g: (g.adicionar('a'), g.adicionar('b'), g.concluir(0), "
                 "g.resumo())[3])(GerenciadorTarefas())", "'1/2 concluidas'"),
                ("(lambda g: (g.adicionar('a'), g.pendentes())[1])(GerenciadorTarefas())",
                 "['a']"),
                ("GerenciadorTarefas().resumo()", "'0/0 concluidas'"),
                ("GerenciadorTarefas().concluir(5)", "!raise IndexError"),
            ],
            nivel="dificil",
            dica="Guarde dicionários {'titulo': ..., 'feita': False} numa lista de instância.",
        ),
    ],
    quiz=[
        Quiz("Para que serve `pip install -e .`?",
             ["Instalar uma versão publicada do PyPI", "Instalar o projeto local em modo editável, refletindo mudanças no código imediatamente",
              "Exportar as dependências para um arquivo", "Criar um ambiente virtual novo"], 1,
             "Mudanças no código-fonte passam a valer sem precisar reinstalar o pacote a cada alteração."),
        Quiz("Qual arquivo centraliza a configuração de projetos Python modernos?",
             ["setup.py", "pyproject.toml", "requirements.txt", "config.ini"], 1,
             "As PEP 518 e 621 tornaram o pyproject.toml o padrão, substituindo a combinação antiga de setup.py/setup.cfg."),
        Quiz("Por que usar o layout com uma pasta src/ intermediária, em vez do pacote direto na raiz?",
             ["É apenas uma preferência estética sem efeito real", "Evita que os testes importem acidentalmente o código do diretório atual em vez do pacote instalado",
              "src/ é exigido pela sintaxe do Python", "Torna o código mais rápido de importar"], 1,
             "Sem src/, um erro de empacotamento pode passar despercebido porque os testes rodam contra o código local, não o instalado de fato."),
        Quiz("Por que usar os.environ['CHAVE'] (colchetes) em vez de os.getenv('CHAVE') para um token de API obrigatório?",
             ["Não há diferença nenhuma entre as duas formas", "Colchetes fazem o programa falhar imediatamente (KeyError) se a variável faltar, evitando um erro confuso mais tarde",
              "getenv não existe no módulo os", "Colchetes são mais rápidos de executar"], 1,
             "Falhar cedo e alto (Dia 15) é preferível a continuar rodando com um valor ausente que só causaria problemas adiante."),
    ],
    projeto=(
        "PROJETO FINAL: escolha um problema real (organizador de arquivos, controle de gastos, "
        "leitor de RSS, gerador de relatórios) e entregue o pacote completo seguindo o checklist "
        "da seção 8: estrutura src/, CLI, persistência, tipos, testes, README e logging."
    ),
    leitura=["packaging.python.org", "PEP 621", "docs.astral.sh/ruff"],
))
