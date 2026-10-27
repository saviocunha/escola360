from datetime import date
import pytest
from escola360.usuarios import Professor


def _prof():
    return Professor(
        id_usuario=1, email="prof@escola.com", senha="segura123",
        cpf="529.982.247-25", telefone="88985243285", endereco="Rua A",
        id_professor=1, nome="Ana Maria", data_nascimento=date(1990, 1, 1),
    )


def test_login_certo():
    assert _prof().fazer_login("prof@escola.com", "segura123") is True


def test_login_errado():
    assert _prof().fazer_login("prof@escola.com", "errada") is False


def test_cpf_invalido():
    with pytest.raises(ValueError):
        p = _prof()
        p.cpf = "111"