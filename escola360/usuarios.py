# Implementa os usuários do Sistema Escola 360
# Interfaces: Autenticavel, GeradorRelatorio (Abstratas).
# Classe base: Usuario (Abstrata, herda de Autenticavel).
# Subclasses: Gestor, Professor, Responsavel (concreto).


from abc import ABC, abstractmethod
from datetime import date
from typing import List

# Imports necessários para Professor (lancar_nota, registrar_frequencia)
from escola360.avaliacao import Nota, Frequencia
# Import necessário para Gestor (gerar_relatorio)
from escola360.relatorios import Relatorio


# ====================== INTERFACE (Classes Abstratas com métodos abstratos) ======================

class Autenticavel(ABC):
    """
    Interface (Contrato) que define que qualquer classe que a implemente
    deve ter o método fazer_login.
    """
    @abstractmethod
    def fazer_login(self, email: str, senha: str) -> bool:
        """Verifica se credenciais são válidas."""
        raise NotImplementedError

class GeradorRelatorio(ABC):
    """
    Interface (Contrato) para classes que podem gerar relatórios.
    Usada pelo Gestor.
    """
    @abstractmethod
    def gerar_relatorio(self) -> "Relatorio":
        raise NotImplementedError
        
# ====================== CLASSE BASE (Herda de Autenticavel e ABC) ======================

class Usuario(Autenticavel, ABC):
    """
    Classe base abstrata para todos os usuários do sistema.
    Contém os atributos e métodos comuns a todos os tipos de usuários.
    """
    def __init__(self, id_usuario: int, email: str, senha: str, cpf: str, telefone: str, endereco: str):
        # Atributos privados de dados de login e contato/pessoal
        self.__id_usuario = id_usuario
        self.__email = email
        self.__senha = senha # Armazenamento de senha em texto plano (simplificação didática)
        self.__cpf = cpf
        self.__telefone = telefone
        self.__endereco = endereco

# -------- getters / setters (Properties) -------
# Implementa validações básicas em alguns setters (regras de negócio).

    @property
    def id_usuario(self) -> int:
        return self.__id_usuario

    @id_usuario.setter
    def id_usuario(self, value: int) -> None:
        if value <= 0:
            raise ValueError("id_usuario deve ser positivo") # Validação de ID
        self.__id_usuario = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        if "@" not in value:
            raise ValueError("email inválido") # Validação mínima de email
        self.__email = value

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, value: str) -> None:
        if not value:
            raise ValueError("cpf não pode ser vazio") # Validação de CPF
        self.__cpf = value

    @property
    def telefone(self) -> str:
        return self.__telefone

    @telefone.setter
    def telefone(self, value: str) -> None:
        self.__telefone = value

    @property
    def endereco(self) -> str:
        return self.__endereco

    @endereco.setter
    def endereco(self, value: str) -> None:
        self.__endereco = value

   # --- operações de usuário ---

    def fazer_login(self, email: str, senha: str) -> bool:
        """Implementação concreta do método da interface Autenticavel."""
        return self.__email == email and self.__senha == senha

    def criar(self) -> None:
        """Método de demonstração (CRUD)."""
        print(f"[USUARIO] criando usuário {self.__id_usuario}")

    def ler(self) -> dict:
        """Método de demonstração (CRUD). Retorna dados de leitura."""
        return {
            "id": self.__id_usuario,
            "email": self.__email,
            "cpf": self.__cpf,
            "telefone": self.__telefone,
            "endereco": self.__endereco,
        }

    def atualizar(self, **dados) -> None:
        """
        Método de demonstração (CRUD). Atualiza atributos via setters/properties.
        Permite atualizar atributos como email, telefone, etc.
        """
        for campo, valor in dados.items():
            if hasattr(self.__class__, campo):
                setattr(self, campo, valor)

    def excluir(self) -> None:
        """Método de demonstração (CRUD)."""
        print(f"[USUARIO] excluindo usuário {self.__id_usuario}")


# ====================== SUBTIPOS DE USUARIO =========

# ====================== GESTOR ======================

class Gestor(Usuario, GeradorRelatorio):
    """
    Especialização de Usuario. Responsável por funções administrativas,
    incluindo a geração de relatórios (implementa GeradorRelatorio).
    """
    def __init__(self, id_usuario: int, email: str, senha: str,
                 cpf: str, telefone: str, endereco: str,
                 id_gestor: int, nome: str, cargo: str):
        super().__init__(id_usuario, email, senha, cpf, telefone, endereco)
        self.__id_gestor = id_gestor
        self.__nome = nome
        self.__cargo = cargo
        self.__relatorios: List["Relatorio"] = [] # Lista de relatórios gerados pelo gestor

    @property
    def id_gestor(self) -> int:
        return self.__id_gestor

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def cargo(self) -> str:
        return self.__cargo

    @property
    def relatorios(self) -> List["Relatorio"]:
        # Retorna uma cópia da lista (encapsulamento)
        return list(self.__relatorios)

    def gerar_relatorio(self) -> "Relatorio":
        """
        Implementa o método da interface GeradorRelatorio.
        Cria um novo objeto Relatorio e o associa ao gestor.
        """
        relatorio = Relatorio(
            id_relatorio=len(self.__relatorios) + 1,
            nome_relatorio=f"Relatório do gestor {self.__nome}",
            data_geracao=date.today(),
        )
        self.__relatorios.append(relatorio)
        return relatorio


# ====================== PROFESSOR ======================

class Professor(Usuario):
    """
    Especialização de Usuario. Responsável pelo registro de notas e frequências.
    Mantém registros do que lançou para fins de auditoria/consulta.
    """
    def __init__(self, id_usuario: int, email: str, senha: str,
                 cpf: str, telefone: str, endereco: str,
                 id_professor: int, nome: str, data_nascimento: date):
        super().__init__(id_usuario, email, senha, cpf, telefone, endereco)
        self.__id_professor = id_professor
        self.__nome = nome
        self.__data_nascimento = data_nascimento
        self.__frequencias: List["Frequencia"] = [] # Frequências registradas por este professor
        self.__notas_lancadas: List["Nota"] = []    # Notas lançadas por este professor

    @property
    def id_professor(self) -> int:
        return self.__id_professor

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def data_nascimento(self) -> date:
        return self.__data_nascimento

    @property
    def frequencias(self) -> List["Frequencia"]:
        return list(self.__frequencias)

    @property
    def notas_lancadas(self) -> List["Nota"]:
        return list(self.__notas_lancadas)

    def lancar_nota(self, aluno: "Aluno", disciplina: "Disciplina",
                    data_avaliacao: date, tipo_avaliacao: str,
                    valor: float) -> "Nota":
        """
        Cria um objeto Nota e sincroniza o relacionamento:
        1. Adiciona Nota à lista de notas_lancadas do Professor.
        2. Adiciona Nota à lista de notas do Aluno.
        3. Adiciona Nota à lista de notas da Disciplina.
        """
        # Validação de regras de negócio (dupla verificação, mas essencial)
        if not (0.0 <= valor <= 10.0):
            # A classe Nota também valida, mas é bom validar antes de criar.
            raise ValueError("valor da nota deve estar entre 0 e 10")
        
        # Cria o objeto Nota
        nota = Nota(
            id_nota=len(self.__notas_lancadas) + 1,
            data_avaliacao=data_avaliacao,
            tipo_avaliacao=tipo_avaliacao,
            valor=valor,
            aluno=aluno,
            disciplina=disciplina,
        )
        
        # 1. Adiciona ao registro do professor
        self.__notas_lancadas.append(nota)
        
        # 2. Adiciona ao registro do aluno (acesso ao método privado _Aluno__adicionar_nota)
        # O acesso direto ao método privado ('_Classe__método') é usado aqui
        # para garantir a consistência do modelo de domínio, pois é o Professor
        # que orquestra o lançamento.
        aluno._Aluno__adicionar_nota(nota)
        
        # 3. Adiciona ao registro da disciplina
        disciplina._Disciplina__adicionar_nota(nota)
        
        return nota

    def registrar_frequencia(self, aluno: "Aluno", disciplina: "Disciplina",
                             data_aula: date, presente: bool) -> "Frequencia":
        """
        Cria um objeto Frequencia e sincroniza o relacionamento:
        1. Adiciona Frequencia à lista de frequencias do Professor.
        2. Adiciona Frequencia à lista de frequencias do Aluno.
        3. Adiciona Frequencia à lista de frequencias da Disciplina.
        """
        
        # Cria o objeto Frequencia
        freq = Frequencia(
            id_frequencia=len(self.__frequencias) + 1,
            data_aula=data_aula,
            # Converte o booleano 'presente' para o status 'P' ou 'F'
            status_frequencia="P" if presente else "F",
            professor=self,
            aluno=aluno,
            disciplina=disciplina,
        )
        
        # 1. Adiciona ao registro do professor
        self.__frequencias.append(freq)
        
        # 2. Adiciona ao registro do aluno (acesso ao método privado)
        aluno._Aluno__adicionar_frequencia(freq)
        
        # 3. Adiciona ao registro da disciplina
        disciplina._Disciplina__adicionar_frequencia(freq)
        
        return freq


# ====================== RESPONSÁVEL ======================

class Responsavel(Usuario):
    """
    Especialização de Usuario. Responsável por acompanhar o(s) Aluno(s) associado(s).
    Mantém uma lista de alunos sob sua responsabilidade.
    """
    def __init__(self, id_usuario: int, email: str, senha: str,
                 cpf: str, telefone: str, endereco: str,
                 id_responsavel: int, nome: str):
        super().__init__(id_usuario, email, senha, cpf, telefone, endereco)
        self.__id_responsavel = id_responsavel
        self.__nome = nome
        self.__alunos: List["Aluno"] = [] # Lista de Alunos que este Responsavel cuida

    @property
    def id_responsavel(self) -> int:
        return self.__id_responsavel

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def alunos(self) -> List["Aluno"]:
        return list(self.__alunos)

    def adicionar_aluno(self, aluno: "Aluno") -> None:
        """
        Adiciona um Aluno à lista de responsabilidade.
        Sincroniza o relacionamento: Adiciona o Responsavel à lista de responsaveis do Aluno.
        """
        if aluno not in self.__alunos:
            self.__alunos.append(aluno)
            # Adiciona o Responsavel à lista do Aluno (sincronização de relacionamento)
            aluno._Aluno__adicionar_responsavel(self)






