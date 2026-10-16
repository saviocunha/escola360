# Implementa a Classe Disciplina.
# Define os métodos para a classe Disciplina.

from __future__ import annotations
from typing import List

class Disciplina:
    """
    Representa uma disciplina curricular oferecida pela instituição.
    Mantém registros agregados de Notas e Frequências associadas a ela.
    """
    def __init__(self, id_disciplina: int, nome: str):
        self.__id_disciplina = id_disciplina
        self.__nome = nome
        self.__notas: List["Nota"] = []                 # Notas lançadas nesta disciplina
        self.__frequencias: List["Frequencia"] = []     # Frequências registradas nesta disciplina

    @property
    def id_disciplina(self) -> int:
        return self.__id_disciplina

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def notas(self) -> List["Nota"]:
        # Retorna uma cópia da lista (encapsulamento)
        return list(self.__notas)

    @property
    def frequencias(self) -> List["Frequencia"]:
        # Retorna uma cópia da lista (encapsulamento)
        return list(self.__frequencias)

    # métodos internos (privados) usados pelo Professor para
    # manter a consistência do modelo (sincronização de relacionamentos)

    def _adicionar_nota(self, nota: "Nota") -> None:
        """Adiciona uma Nota à disciplina (chamado por Professor.lancar_nota)."""
        self.__notas.append(nota)

    def _adicionar_frequencia(self, frequencia: "Frequencia") -> None:
        """Adiciona uma Frequencia à disciplina (chamado por Professor.registrar_frequencia)."""
        self.__frequencias.append(frequencia)
