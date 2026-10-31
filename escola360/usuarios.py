# Implementa os usuários do Sistema Escola 360
# Interfaces: Autenticavel, GeradorRelatorio (Abstratas).
# Classe base: Usuario (Abstrata, herda de Autenticavel).
# Subclasses: Gestor, Professor, Responsavel (concreto).


from abc import ABC, abstractmethod
from datetime import date
from typing import List, TYPE_CHECKING
import hashlib
import hmac
import os
from itertools import count
import re

# Expressão regular para validação de e-mail.
# Garante o formato basico 'usuario@dominio.extensao'.
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$") 

# Imports de entidades relacionadas para criação de avaliações, frequências e relatórios.
from escola360.avaliacao import Nota, Frequencia
from escola360.relatorios import Relatorio

if TYPE_CHECKING:
    from escola360.aluno import Aluno
    from escola360.disciplinas import Disciplina

# =============================================================================
# INTERFACES (Classes Abstratas Puras - Contratos)
# =============================================================================

class Autenticavel(ABC):
    """
    Interface/Contrato para qualquer entidade que exija autenticação no sistema.
    Obrigada as sub-classes a implementar o método fazer_login.
    """
    @abstractmethod
    def fazer_login(self, email: str, senha: str) -> bool:
        """Verifica se credenciais são válidas."""
        raise NotImplementedError

class GeradorRelatorio(ABC):
    """
    Interface/Contrato para classes capazes de emitir relatórios administrativos.
    Usada principalmente pela classe Gestor.
    """
    @abstractmethod
    def gerar_relatorio(self) -> "Relatorio":
        """Gera e retorna uma nova instância de Relatorio."""
        raise NotImplementedError
        
# =============================================================================
# CLASSE BASE (Abstrata - Modelo de Usuário)
# =============================================================================


class Usuario(Autenticavel, ABC):
    """
    Classe base abstrata para todos os atores do sistema.
    Concentra o gerenciamento de identidade, segurança de senha e dados cadastrais.
    """
    @property
    @abstractmethod
    def tipo_usuario(self) -> str:
        ...
    
    def __init__(self, id_usuario: int, email: str, senha: str, cpf: str, telefone: str, endereco: str):
        # A atribuição via propriedades (setters) garante que os dados passem
        # pelas validações de negócio logo na instanciação (ex: CPF e e-mail).
        self.id_usuario = id_usuario
        self.email = email
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco

        # Criptografia de Senha: Gera um salt aleatório criptograficamente seguro (16 bytes)
        # e armazena a senha derivada usando PBKDF2-HMAC-SHA256 para evitar senhas em texto puro.
        salt = os.urandom(16)
        self.__senha_salt = salt
        self.__senha_hash = self._derivar_hash(senha, salt)

# -------- getters / setters (Properties) -------
# Implementa validações básicas em alguns setters (regras de negócio).

    @property
    def id_usuario(self) -> int:
        return self.__id_usuario

    @id_usuario.setter
    def id_usuario(self, value: int) -> None:
        """Garante que o ID do usuário seja um inteiro positivo."""
        if value <= 0:
            raise ValueError("id_usuario deve ser positivo")
        self.__id_usuario = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        """Valida o formato do e-mail usando a regex do módulo antes de atribuir."""
        if not _EMAIL_RE.match(value or ""):
            raise ValueError(f'Email inválido: {value!r}')
        self.__email = value

    @property
    def cpf(self) -> str:
        return self.__cpf

    @staticmethod
    def validar_cpf(cpf:str) -> bool:
        """
        Método utilitário estático que implementa a validação matemática oficial de CPF:
        1. Remove caracteres não numéricos.
        2. Rejeita CPFs com menos de 11 dígitos ou com sequências repetidas (ex: 111.111.111-11).
        3. Calcula os 2 dígitos verificadores através do cálculo ponderado de módulo 11.
        """
        d = re.sub(r"\D", "", cpf or "")
        if len(d) != 11 or len(set(d)) ==1:
            return False
        for i in (9,10):
            soma = sum(int(d[j])* (i + 1 - j) for j in range (i))
            if (soma * 10) % 11 % 10 != int(d[i]):
                return False
        return True
    
    @cpf.setter
    def cpf(self, value:str) -> None:
        """Valida a integridade do CPF antes de salvá-lo."""
        if not self.validar_cpf(value):
            raise ValueError(f"CPF inválido: {value!r}")
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

    # -------------------------------------------------------------------------
    # MÉTODOS DE AUTENTICAÇÃO E SEGURANÇA
    # -------------------------------------------------------------------------

    @staticmethod
    def _derivar_hash(senha:str, salt: bytes) -> bytes:
        """Aplica a função de derivação de chave PBKDF2 com 260.000 iterações."""
        return hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, 260_000)

    def verificar_senha(self, senha:str) -> bool:
        """
        Deriva o hash da senha de teste usando o mesmo salt armazenado
        e compara usando hmac.compare_digest para prevenir 'timing attacks'.
        """
        candidato = self._derivar_hash(senha, self.__senha_salt)
        return hmac.compare_digest(candidato, self.__senha_hash)

    def fazer_login(self, email:str, senha:str) -> bool:
        """Implementação concreta do contrato Autenticavel."""
        return self.email == email and self.verificar_senha(senha)

    def alterar_senha(self, senha_atual: str, nova_senha:str) -> None:
        """Valida a senha antiga, checa requisitos de complexidade e re-criptografa."""
        if not self.verificar_senha(senha_atual):
            raise ValueError ("Senha incorreta")
        if len(nova_senha) < 8:
            raise ValueError("Nova senha deve ter pelo menos 8 carateres")
        salt = os.urandom(16)
        self.__senha_salt = salt
        self.__senha_hash = self._derivar_hash(nova_senha, salt)

    # -------------------------------------------------------------------------
    # OPERAÇÕES DE CRUD (Demonstração / Persistência)
    # -------------------------------------------------------------------------

    def criar(self) -> None:
        """Simula a persistência do usuário no banco de dados."""
        print(f"[USUARIO] criando usuário {self.__id_usuario}")

    def ler(self) -> dict:
        """Retorna os dados cadastrais do usuário encapsulados em um dicionário."""
        return {
            "id": self.__id_usuario,
            "email": self.__email,
            "cpf": self.__cpf,
            "telefone": self.__telefone,
            "endereco": self.__endereco,
        }

    def atualizar(self, **dados) -> None:
        """Atualiza dinamicamente atributos do usuário passando pelos setters correspondentes."""
        permitidos = {'email', 'telefone','endereço'}
        for campo, valor in dados.items():
            if campo not in permitidos:
                raise ValueError(f'campo não editável: {campo}')
            setattr(self, campo, valor)

    def excluir(self) -> None:
        """Simula a remoção do usuário do sistema."""
        print(f"[USUARIO] excluindo usuário {self.__id_usuario}")

# =============================================================================
# SUBCLASSES CONCRETAS DE USUARIO
# =============================================================================

# ====================== GESTOR ======================
class Gestor(Usuario, GeradorRelatorio):
    """
    Especialização de Usuario com perfil administrativo.
    Herda características de Usuario e implementa a interface GeradorRelatorio.
    """
    @property
    def tipo_usuario(self) -> str:
        return "GESTOR"
    
    def __init__(self, id_usuario: int, email: str, senha: str,
                 cpf: str, telefone: str, endereco: str,
                 id_gestor: int, nome: str, cargo: str):
        super().__init__(id_usuario, email, senha, cpf, telefone, endereco)
        self.__id_gestor = id_gestor
        self.__nome = nome
        self.__cargo = cargo
        self.__relatorios: List["Relatorio"] = [] 

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
        """Retorna uma cópia rasa da lista para preservar o encapsulamento do atributo privado."""
        return list(self.__relatorios)

    def gerar_relatorio(self) -> "Relatorio":
        """
        Implementa o método da interface GeradorRelatorio.
        Cria um novo objeto Relatorio e o associa ao gestor.
        """
        relatorio = Relatorio(
            nome_relatorio=f"Relatório do gestor {self.__nome}",
            data_geracao=date.today(),
        )
        self.__relatorios.append(relatorio)
        return relatorio


# ====================== PROFESSOR ======================

class Professor(Usuario):
    """
    Especialização de Usuario responsável pela gestão pedagógica de alunos.
    Orquestra o lançamento de notas e registros de presença/ausência.
    """
    @property
    def tipo_usuario(self) -> str:
        return "PROFESSOR"
    
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
        Cria uma Nota e realiza o vínculo bidirecional entre as entidades afetadas:
        1. Valida o intervalo numérico da nota [0.0, 10.0].
        2. Adiciona a Nota ao histórico do Professor.
        3. Adiciona a Nota ao registro do Aluno e da Disciplina envolvida.
        """
        # Validação de regras de negócio (dupla verificação, mas essencial)
        if not (0.0 <= valor <= 10.0):
            # A classe Nota também valida, mas é bom validar antes de criar.
            raise ValueError("valor da nota deve estar entre 0 e 10")
        
        # Cria o objeto Nota
        nota = Nota(
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
        aluno._adicionar_nota(nota)
        
        # 3. Adiciona ao registro da disciplina
        disciplina._adicionar_nota(nota)
        
        return nota

    def registrar_frequencia(self, aluno: "Aluno", disciplina: "Disciplina",
                             data_aula: date, presente: bool) -> "Frequencia":
        """
        Cria um registro de Frequencia ('P' para presente, 'F' para falta)
        e atualiza os históricos do Professor, Aluno e Disciplina.
        """
        
        # Cria o objeto Frequencia
        freq = Frequencia(
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
        aluno._adicionar_frequencia(freq)
        
        # 3. Adiciona ao registro da disciplina
        disciplina._adicionar_frequencia(freq)
        
        return freq


# ====================== RESPONSÁVEL ======================

class Responsavel(Usuario):
    """
    Especialização de Usuario representando pais/tutores legais dos alunos.
    Permite o acompanhamento de um ou múltiplos estudantes.
    """
    @property
    def tipo_usuario(self) -> str:
        return "RESPONSAVEL"
    
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
        Associa um aluno a este responsável e realiza a sincronização bidirecional,
        adicionando este responsável à lista de responsáveis do aluno.
        """
        if aluno not in self.__alunos:
            self.__alunos.append(aluno)
            # Adiciona o Responsavel à lista do Aluno (sincronização de relacionamento)
            aluno._adicionar_responsavel(self)






