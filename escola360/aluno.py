#Implementa a Classe Aluno e seus Métodos
from __future__ import annotations
from datetime import date
from typing import List, TYPE_CHECKING

from escola360.usuarios import Usuario  # Aluno é uma especialização de Usuario
if TYPE_CHECKING:
    from escola360.avaliacao import Nota, Frequencia
    from escola360.usuarios import Responsavel


class Aluno(Usuario)
    """
    Especialização da classe Usuario.
    Representa o aluno e contém todas as suas informações e registros acadêmicos.
    """
    @property
    def tipo_usuario(self) -> str:
        return "ALUNO"
    
    def __init__(self, id_usuario: int, email: str, senha: str,
                 cpf: str, telefone: str, endereco: str,
                 id_aluno: int, nome: str, data_nascimento: date):
        super().__init__(id_usuario, email, senha, cpf, telefone, endereco)
        self.__id_aluno = id_aluno
        self.__nome = nome
        self.__data_nascimento = data_nascimento
        
        # Registros de relacionamento e dados acadêmicos
        self.__responsaveis: List["Responsavel"] = [] # Relacionamento N:M com Responsavel
        self.__notas: List["Nota"] = []               # Lista de objetos Nota (desempenho)
        self.__frequencias: List["Frequencia"] = []   # Lista de objetos Frequencia (assiduidade)

    @property
    def id_aluno(self) -> int:
        return self.__id_aluno

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def data_nascimento(self) -> date:
        return self.__data_nascimento

    @property
    def responsaveis(self) -> List["Responsavel"]:
        # Retorna uma cópia da lista (encapsulamento)
        return list(self.__responsaveis)

    @property
    def notas(self) -> List["Nota"]:
        # Retorna uma cópia da lista (encapsulamento)
        return list(self.__notas)

    @property
    def frequencias(self) -> List["Frequencia"]:
        # Retorna uma cópia da lista (encapsulamento)
        return list(self.__frequencias)

    # Métodos de consulta pública para o aluno
    
    def consultar_nota(self) -> List["Nota"]:
        """Retorna uma cópia da lista de todas as notas do aluno."""
        return list(self.__notas)

    def consultar_frequencia(self) -> List["Frequencia"]:
        """Retorna uma cópia da lista de todas as frequências do aluno."""
        return list(self.__frequencias)

    def calcular_frequencia(self, disciplina) -> float:
        """Calcula a % de presença do aluno em uma disciplina."""
        freqs = [f for f in self.__frequencias if f.disciplina is disciplina]
        if not freqs:
            return 0.0
        return sum(f.status_frequencia == "P" for f in freqs) / len(freqs)*100

    def calcular_media(self, disciplina) -> float:
        """Calcula a média das notas do aluno em uma disciplina."""
        notas = [n.valor for n in self.__notas if n.disciplina is disciplina]
        return sum(notas) / len(notas) if notas else 0.0

    # métodos internos (privados) usados por Professor e Responsavel para
    # manter a consistência do modelo (sincronização de relacionamentos)

    def _adicionar_responsavel(self, responsavel: "Responsavel") -> None:
        """Adiciona um Responsavel ao aluno (chamado por Responsavel.adicionar_aluno)."""
        if responsavel not in self.__responsaveis:
            self.__responsaveis.append(responsavel)

    def _adicionar_nota(self, nota: "Nota") -> None:
        """Adiciona uma Nota ao aluno (chamado por Professor.lancar_nota)."""
        self.__notas.append(nota)

    def _adicionar_frequencia(self, frequencia: "Frequencia") -> None:
        """Adiciona uma Frequencia ao aluno (chamado por Professor.registrar_frequencia)."""
        self.__frequencias.append(frequencia)
