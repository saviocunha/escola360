from datetime import date
import pytest
from escola360.usuarios import Professor, Usuario


def _prof():
    """
    Cria uma instância base para se usada nos testes.
    """

    return Professor(
        id_usuario=1, email="prof@escola.com", senha="segura123",
        cpf="529.982.247-25", telefone="88985243285", endereco="Rua A",
        id_professor=1, nome="Ana Maria", data_nascimento=date(1990, 1, 1),
    )


def test_login_certo(): # Testa o sucesso no login
    assert _prof().fazer_login("prof@escola.com", "segura123") is True


def test_login_errado(): # Testa a falha de autenticação
    assert _prof().fazer_login("prof@escola.com", "errada") is False #False


def test_cpf_invalido(): # Testa se o sistema levanta um erro ao receber um CPF em formato inválido
    with pytest.raises(ValueError):
        p = _prof()
        p.cpf = "111"

print(variavel_que_nao_existe)
