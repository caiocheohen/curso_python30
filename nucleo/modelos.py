"""Estruturas de dados que descrevem o conteudo do curso."""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Exemplo:
    """Um trecho de codigo demonstrativo, com explicacao."""
    titulo: str
    codigo: str
    explicacao: str = ""


@dataclass
class Exercicio:
    """Exercicio pratico corrigido automaticamente.

    `testes` e uma lista de pares (expressao, resultado_esperado), ambos como
    strings de codigo Python que serao avaliadas dentro do arquivo do aluno.
    """
    id: str
    enunciado: str
    funcao: str
    assinatura: str
    testes: List[Tuple[str, str]]
    dica: str = ""
    nivel: str = "basico"          # basico | medio | dificil

    @property
    def dia(self) -> int:
        # id no formato d07e2 -> dia 7
        return int(self.id[1:3])


@dataclass
class Quiz:
    pergunta: str
    alternativas: List[str]
    correta: int                    # indice em `alternativas`
    explicacao: str = ""


@dataclass
class Dia:
    numero: int
    titulo: str
    nivel: str                      # Iniciante | Intermediario | Avancado
    duracao: str
    objetivos: List[str]
    teoria: str
    exemplos: List[Exemplo] = field(default_factory=list)
    exercicios: List[Exercicio] = field(default_factory=list)
    quiz: List[Quiz] = field(default_factory=list)
    projeto: str = ""
    leitura: List[str] = field(default_factory=list)
