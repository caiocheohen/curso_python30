#!/usr/bin/env python3
"""CURSO DE PYTHON EM 30 DIAS - do zero ao avançado.

Programa interativo de terminal, escrito em Python puro (sem dependências
externas), para rodar em Linux.

Uso:
    python3 curso.py                 abre o menu principal
    python3 curso.py hoje            abre o próximo dia não concluído
    python3 curso.py dia 7           abre o dia 7
    python3 curso.py exercicio d07e2 abre/corrige um exercício
    python3 curso.py testar d07e2    corrige sem abrir a aula
    python3 curso.py quiz 7          responde o quiz do dia 7
    python3 curso.py progresso       mostra o painel de progresso
    python3 curso.py buscar zip      procura um assunto no material
    python3 curso.py ementa          lista os 30 dias
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import conteudo
from nucleo import avaliador, progresso, ui
from nucleo.ui import C


# --------------------------------------------------------------- exibição
def mostrar_cabecalho_dia(dia):
    ui.titulo(f"DIA {dia.numero:02d} - {dia.titulo.upper()}")
    print(f"  {C.CINZA}nível:{C.RESET} {dia.nivel}    "
          f"{C.CINZA}duração estimada:{C.RESET} {dia.duracao}")
    ui.secao("Objetivos de hoje")
    for o in dia.objetivos:
        print(f"   - {o}")


def mostrar_teoria(dia):
    ui.secao("Teoria")
    ui.paragrafo(dia.teoria)


def mostrar_exemplos(dia):
    if not dia.exemplos:
        return
    ui.secao("Exemplos comentados")
    for i, ex in enumerate(dia.exemplos, 1):
        print(f"\n  {C.NEGRITO}Exemplo {i}: {ex.titulo}{C.RESET}")
        ui.codigo(ex.codigo)
        if ex.explicacao:
            ui.info(ex.explicacao)


def mostrar_lista_exercicios(dia, dados):
    ui.secao("Exercícios práticos")
    for ex in dia.exercicios:
        feito = ex.id in dados["exercicios_ok"]
        marca = f"{C.VERDE}[x]{C.RESET}" if feito else f"{C.CINZA}[ ]{C.RESET}"
        print(f"  {marca} {C.NEGRITO}{ex.id}{C.RESET} ({ex.nivel})")
        for linha in ex.enunciado.strip().split("\n"):
            print(f"      {linha}")
        print()


def mostrar_projeto(dia):
    if not dia.projeto:
        return
    ui.secao("Projeto do dia")
    ui.paragrafo(dia.projeto)
    if dia.leitura:
        print()
        ui.info("Leitura recomendada: " + " | ".join(dia.leitura))


# --------------------------------------------------------------- quiz
def rodar_quiz(dia, dados):
    if not dia.quiz:
        ui.aviso("Este dia não tem quiz.")
        return
    ui.secao(f"Quiz do dia {dia.numero}")
    acertos = 0
    for i, q in enumerate(dia.quiz, 1):
        print(f"\n  {C.NEGRITO}{i}. {q.pergunta}{C.RESET}")
        for j, alt in enumerate(q.alternativas):
            print(f"     {chr(97 + j)}) {alt}")
        resposta = ui.perguntar("Resposta (a/b/c/d, ou 'p' para pular): ").lower()
        if resposta == "p":
            continue
        indice = ord(resposta[0]) - 97 if resposta and resposta[0].isalpha() else -1
        if indice == q.correta:
            acertos += 1
            ui.ok("Correto!")
        else:
            certa = chr(97 + q.correta)
            ui.erro(f"A resposta certa é {certa}) {q.alternativas[q.correta]}")
        if q.explicacao:
            ui.info(q.explicacao)

    total = len(dia.quiz)
    print()
    print("  Resultado: " + ui.barra(acertos, total))
    progresso.registrar_quiz(dados, dia.numero, acertos, total)
    if acertos == total:
        ui.ok("Teoria dominada.")
    elif acertos >= total / 2:
        ui.aviso("Bom, mas vale reler a teoria dos pontos errados.")
    else:
        ui.erro("Releia a teoria de hoje antes de seguir para os exercícios.")


# --------------------------------------------------------------- exercícios
def menu_exercicio(ex, dados):
    caminho = avaliador.preparar(ex)
    ui.secao(f"Exercício {ex.id} ({ex.nivel})")
    for linha in ex.enunciado.strip().split("\n"):
        print("  " + linha)
    print()
    ui.info(f"Edite este arquivo: {caminho}")
    ui.info("Sugestão: abra em outro terminal com  nano " + str(caminho))
    print()
    print(f"  {C.CINZA}Testes que precisam passar:{C.RESET}")
    for expr, esperado in ex.testes:
        alvo = ("levanta " + esperado.split(None, 1)[1]
                if esperado.startswith("!raise") else esperado)
        print(f"    {expr}  ->  {alvo}")

    while True:
        opcao = ui.menu([
            ("t", "Testar minha solução"),
            ("v", "Ver o arquivo atual"),
            ("d", "Ver a dica"),
            ("r", "Recriar o arquivo do zero (apaga o que escrevi)"),
            ("0", "Voltar"),
        ], "O que deseja fazer?")

        if opcao == "t":
            avaliador.corrigir(ex, dados)
            ui.pausar()
        elif opcao == "v":
            ui.codigo(caminho.read_text(encoding="utf-8"))
            ui.pausar()
        elif opcao == "d":
            ui.info(ex.dica or "Sem dica para este exercício.")
            ui.pausar()
        elif opcao == "r":
            if ui.perguntar("Tem certeza? (s/N): ").lower() == "s":
                avaliador.preparar(ex, sobrescrever=True)
                ui.ok("Arquivo recriado.")
        elif opcao in ("0", "q", ""):
            return


def menu_exercicios_do_dia(dia, dados):
    while True:
        ui.limpar()
        mostrar_lista_exercicios(dia, dados)
        opcoes = [(str(i), f"{ex.id} - {ex.enunciado.strip().splitlines()[0][:50]}")
                  for i, ex in enumerate(dia.exercicios, 1)]
        opcoes.append(("0", "Voltar"))
        escolha = ui.menu(opcoes, "Qual exercício?")
        if escolha in ("0", "q", ""):
            return
        if escolha.isdigit() and 1 <= int(escolha) <= len(dia.exercicios):
            menu_exercicio(dia.exercicios[int(escolha) - 1], dados)


# --------------------------------------------------------------- aula
def estudar_dia(numero, dados):
    dia = conteudo.por_numero(numero)
    if dia is None:
        ui.erro(f"Dia {numero} não existe. Use um valor de 1 a {conteudo.TOTAL_DIAS}.")
        return

    ui.limpar()
    mostrar_cabecalho_dia(dia)
    ui.pausar("ENTER para ver a teoria...")

    mostrar_teoria(dia)
    ui.pausar("ENTER para ver os exemplos...")

    mostrar_exemplos(dia)
    progresso.marcar_dia_lido(dados, dia.numero)

    while True:
        print()
        opcao = ui.menu([
            ("e", "Ir para os exercícios"),
            ("q", "Responder o quiz"),
            ("p", "Ver o projeto do dia"),
            ("t", "Reler a teoria"),
            ("x", "Reler os exemplos"),
            ("0", "Voltar ao menu principal"),
        ], f"Dia {dia.numero} - o que agora?")

        if opcao == "e":
            menu_exercicios_do_dia(dia, dados)
        elif opcao == "q":
            rodar_quiz(dia, dados)
            ui.pausar()
        elif opcao == "p":
            mostrar_projeto(dia)
            ui.pausar()
        elif opcao == "t":
            ui.limpar()
            mostrar_teoria(dia)
            ui.pausar()
        elif opcao == "x":
            ui.limpar()
            mostrar_exemplos(dia)
            ui.pausar()
        elif opcao in ("0", ""):
            return


# --------------------------------------------------------------- painéis
def painel_progresso(dados):
    ui.titulo("SEU PROGRESSO")
    lidos = len(dados["dias_lidos"])
    feitos = len(dados["exercicios_ok"])
    print("\n  Aulas concluídas    " + ui.barra(lidos, conteudo.TOTAL_DIAS))
    print("  Exercícios resolvidos " + ui.barra(feitos, conteudo.TOTAL_EXERCICIOS))

    acertos = sum(v["acertos"] for v in dados["quiz"].values())
    total_q = sum(v["total"] for v in dados["quiz"].values())
    print("  Quiz                " + ui.barra(acertos, total_q or 1))

    print(f"\n  {C.CINZA}Sequência atual:{C.RESET} {progresso.sequencia(dados)} dia(s)")
    print(f"  {C.CINZA}Dias com sessão:{C.RESET} {len(dados['sessoes'])}")
    print(f"  {C.CINZA}Arquivos em:{C.RESET} {progresso.diretorio_base()}")

    ui.secao("Mapa dos 30 dias")
    for d in conteudo.DIAS:
        exs = [e.id for e in d.exercicios]
        ok = sum(1 for e in exs if e in dados["exercicios_ok"])
        if d.numero in dados["dias_lidos"] and ok == len(exs):
            marca, cor = "OK ", C.VERDE
        elif d.numero in dados["dias_lidos"]:
            marca, cor = "...", C.AMARELO
        else:
            marca, cor = "   ", C.CINZA
        print(f"  {cor}[{marca}]{C.RESET} Dia {d.numero:02d}  {d.titulo[:46]:<46}"
              f" {C.CINZA}{ok}/{len(exs)} ex.{C.RESET}")

    prox = progresso.proximo_dia(dados, conteudo.TOTAL_DIAS)
    print()
    ui.info(f"Próximo passo sugerido: dia {prox}")


def mostrar_ementa():
    ui.titulo("EMENTA - 30 DIAS")
    nivel_atual = ""
    for d in conteudo.DIAS:
        if d.nivel != nivel_atual:
            nivel_atual = d.nivel
            print(f"\n  {C.NEGRITO}{C.AMARELO}--- {nivel_atual.upper()} ---{C.RESET}")
        print(f"  Dia {d.numero:02d}  {d.titulo}")
        print(f"          {C.CINZA}{len(d.exercicios)} exercícios | "
              f"{d.duracao}{C.RESET}")


def revisao(dados):
    """Revisão espaçada: quiz dos dias já lidos, priorizando os mais antigos."""
    lidos = [d for d in conteudo.DIAS if d.numero in dados["dias_lidos"] and d.quiz]
    if not lidos:
        ui.aviso("Estude pelo menos um dia antes de revisar.")
        return
    fracos = sorted(
        lidos,
        key=lambda d: (dados["quiz"].get(str(d.numero), {"acertos": 0})["acertos"],
                       d.numero),
    )[:3]
    ui.titulo("REVISÃO ESPAÇADA")
    ui.info("Revendo os dias com menor aproveitamento.")
    for d in fracos:
        rodar_quiz(d, dados)
        ui.pausar()


def buscar_assunto(termo):
    achados = conteudo.buscar(termo)
    ui.titulo(f"BUSCA: {termo}")
    if not achados:
        ui.aviso("Nada encontrado. Tente outra palavra.")
        return
    for d, trecho in achados:
        print(f"\n  {C.NEGRITO}Dia {d.numero:02d} - {d.titulo}{C.RESET}")
        print(f"  {C.CINZA}{trecho}{C.RESET}")


# --------------------------------------------------------------- menu
def menu_principal(dados):
    while True:
        ui.limpar()
        prox = progresso.proximo_dia(dados, conteudo.TOTAL_DIAS)
        ui.titulo("CURSO DE PYTHON EM 30 DIAS")
        print(f"  {C.CINZA}Do zero ao avançado - teoria + prática - Linux{C.RESET}")
        print()
        print("  Aulas      " + ui.barra(len(dados["dias_lidos"]), conteudo.TOTAL_DIAS))
        print("  Exercícios " + ui.barra(len(dados["exercicios_ok"]),
                                         conteudo.TOTAL_EXERCICIOS))

        opcao = ui.menu([
            ("1", f"Continuar de onde parei (dia {prox})"),
            ("2", "Escolher um dia (1-30)"),
            ("3", "Praticar exercícios de um dia"),
            ("4", "Quiz de um dia"),
            ("5", "Revisão espaçada"),
            ("6", "Ver ementa completa"),
            ("7", "Meu progresso"),
            ("8", "Buscar um assunto"),
            ("0", "Sair"),
        ], "Menu principal")

        if opcao == "1":
            estudar_dia(prox, dados)
        elif opcao == "2":
            n = ui.perguntar("Número do dia: ")
            if n.isdigit():
                estudar_dia(int(n), dados)
        elif opcao == "3":
            n = ui.perguntar("Número do dia: ")
            dia = conteudo.por_numero(int(n)) if n.isdigit() else None
            if dia:
                menu_exercicios_do_dia(dia, dados)
            else:
                ui.erro("Dia inválido.")
                ui.pausar()
        elif opcao == "4":
            n = ui.perguntar("Número do dia: ")
            dia = conteudo.por_numero(int(n)) if n.isdigit() else None
            if dia:
                rodar_quiz(dia, dados)
            else:
                ui.erro("Dia inválido.")
            ui.pausar()
        elif opcao == "5":
            revisao(dados)
        elif opcao == "6":
            mostrar_ementa()
            ui.pausar()
        elif opcao == "7":
            painel_progresso(dados)
            ui.pausar()
        elif opcao == "8":
            buscar_assunto(ui.perguntar("Assunto: "))
            ui.pausar()
        elif opcao in ("0", "q", "sair"):
            print(f"\n  {C.VERDE}Até a próxima sessão. Constância vence talento.{C.RESET}\n")
            return


# --------------------------------------------------------------- CLI
def principal(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    dados = progresso.carregar()

    if not argv:
        menu_principal(dados)
        return 0

    comando = argv[0].lower()
    arg = argv[1] if len(argv) > 1 else ""

    if comando in ("-h", "--help", "ajuda"):
        print(__doc__)
    elif comando == "hoje":
        estudar_dia(progresso.proximo_dia(dados, conteudo.TOTAL_DIAS), dados)
    elif comando == "dia":
        estudar_dia(int(arg) if arg.isdigit() else 1, dados)
    elif comando in ("exercicio", "ex"):
        ex = conteudo.exercicio_por_id(arg)
        if ex:
            menu_exercicio(ex, dados)
        else:
            ui.erro(f"Exercício '{arg}' não encontrado (formato: d07e2).")
            return 1
    elif comando == "testar":
        ex = conteudo.exercicio_por_id(arg)
        if not ex:
            ui.erro(f"Exercício '{arg}' não encontrado (formato: d07e2).")
            return 1
        return 0 if avaliador.corrigir(ex, dados) else 1
    elif comando == "quiz":
        dia = conteudo.por_numero(int(arg)) if arg.isdigit() else None
        if dia:
            rodar_quiz(dia, dados)
        else:
            ui.erro("Informe o número do dia. Ex.: python3 curso.py quiz 7")
            return 1
    elif comando == "progresso":
        painel_progresso(dados)
    elif comando == "ementa":
        mostrar_ementa()
    elif comando == "buscar":
        buscar_assunto(" ".join(argv[1:]))
    else:
        ui.erro(f"Comando desconhecido: {comando}")
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(principal())
    except KeyboardInterrupt:
        print("\n  Interrompido. Seu progresso está salvo.\n")
        sys.exit(130)
    except BrokenPipeError:
        # Acontece em `curso.py ementa | head`: o leitor fecha o cano antes do
        # fim. Redireciona o stdout para o vazio para o interpretador nao
        # tentar (e falhar ao) esvaziar o buffer no encerramento.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(141)
