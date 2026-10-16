#Implementa a Classe Nota.
#Implementa a Classe Frequência.
#Implementa os respectivos métodos e atributos privados para as Classes Nota e Frequência.

from __future__ import annotations
from datetime import date
from itertools import count

# Importa a funcionalidade de anotações de tipo de importações futuras.
# Permite referenciar classes que ainda não foram totalmente definidas.
# (ex: "Aluno" e "Disciplina" dentro da classe Nota).

class Nota:
    """
    Representa o registro de uma nota obtida por um Aluno em uma Disciplina.
    Implementa validação de regra de negócio para o valor da nota (0.0 a 10.0).
    """
    _ids = count(1)
    def __init__(self, data_avaliacao: date,
                 tipo_avaliacao: str, valor: float,
                 aluno: "Aluno", disciplina: "Disciplina"):
        # Regra de negócio: A nota deve estar entre 0.0 e 10.0
        if not (0.0 <= valor <= 10.0):
            raise ValueError("valor da nota deve estar entre 0 e 10")
        
        # Atributos privados para encapsulamento (usando '__').
        self.__id_nota = next(Nota._ids)
        self.__data_avaliacao = data_avaliacao
        self.__tipo_avaliacao = tipo_avaliacao  # Ex: 'Prova Mensal', 'Trabalho'
        self.__valor = valor
        self.__aluno = aluno        # Referência ao objeto Aluno
        self.__disciplina = disciplina # Referência ao objeto Disciplina

    # Properties de leitura (getters) para acessar os atributos privados
    # de forma segura e padronizada.

    @property
    def id_nota(self) -> int:
        return self.__id_nota

    @property
    def data_avaliacao(self) -> date:
        return self.__data_avaliacao

    @property
    def tipo_avaliacao(self) -> str:
        return self.__tipo_avaliacao

    @property
    def valor(self) -> float:
        return self.__valor

    @property
    def aluno(self) -> "Aluno":
        return self.__aluno

    @property
    def disciplina(self) -> "Disciplina":
        return self.__disciplina


class Frequencia:
    """
    Representa o registro de frequência de um Aluno em uma aula de Disciplina.
    Implementa validação para o status (P=Presente, F=Falta).
    """
    _ids = count(1)
    def __init__(self, data_aula: date,
                 status_frequencia: str, professor: "Professor",
                 aluno: "Aluno", disciplina: "Disciplina"):
        
        # Regra de negócio: O status deve ser 'P' (Presente) ou 'F' (Falta)
        if status_frequencia not in ("P", "F"):
            raise ValueError("status_frequencia deve ser 'P' ou 'F'")
        
        # Atributos privados
        self.__id_frequencia = next(Frequencia._ids)
        self.__data_aula = data_aula
        self.__status_frequencia = status_frequencia
        self.__professor = professor   # Referência ao Professor que registrou
        self.__aluno = aluno           # Referência ao objeto Aluno
        self.__disciplina = disciplina # Referência ao objeto Disciplina

    # Properties de leitura (getters)

    @property
    def id_frequencia(self) -> int:
        return self.__id_frequencia

    @property
    def data_aula(self) -> date:
        return self.__data_aula

    @property
    def status_frequencia(self) -> str:
        return self.__status_frequencia

    @property
    def professor(self) -> "Professor":
        return self.__professor

    @property
    def aluno(self) -> "Aluno":
        return self.__aluno

    @property
    def disciplina(self) -> "Disciplina":
        return self.__disciplina
