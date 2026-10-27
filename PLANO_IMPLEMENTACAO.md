# Plano Único de Implementação — Escola360

> **Para quem:** você, que vai arrumar o projeto **manualmente**, linha por linha, mesmo começando agora.
> **Como usar:** execute as fases **nesta ordem**. Depois de cada passo, **salve (Ctrl+S)** e faça o teste indicado. Não pule.
> **Fonte:** este documento condensa os 4 planos de `/home/savio/Vídeos/` (`Plano_de_Melhoria_Escola360.md`, `CODE_REVIEW_ESCOLA360.md`, `CODE_REVIEW_ESCOLA360_DETALHADO.md`, `AUDITORIA_ROTEIRO_CORRECAO.md`) + `/home/savio/ROTEIRO_MELHORIAS.md`.

---

## 0. Diagnóstico resumido (o que está errado hoje)

| Frente | Problema real (verificado no código) | Gravidade |
|---|---|---|
| Rodar | `main.py:9` = `from avaliacao import...` → `ModuleNotFoundError`. README:66 diz "todos na mesma pasta" (falso hoje) | CRÍTICO |
| Segurança | Senha em texto plano `usuarios.py:49`, login com `==` `:107`. CPF só checa "não vazio" `:83`, e-mail só checa `"@"` `:73` | CRÍTICO |
| Encapsulamento | `__init__` ignora os setters (`:47-52`); acesso via `_Aluno__adicionar_nota` `usuarios.py:254,257,285,288,328` | ALTO |
| IDs | `len(lista)+1` duplica/colide: `usuarios.py:178,239,272` | ALTO |
| Design | `Usuario` não é abstrata de fato; `atualizar()` usa `hasattr(self.__class__, …)` `:129` | MÉDIO |
| Banco | `uk_notas UNIQUE(id_aluno,id_disciplina)` `SQL:266` impede 2ª nota; faltam `tipo_avaliacao`/`data_avaliacao`/`bimestre`; `CREATE DATABASE` `:19`; sem índices; `quant_alunos` `:50`; CASCADE apaga histórico | ALTO |
| Frontend | header/nav/footer copiados em 6 HTMLs; cores literais (`#16305c` etc.); `script.js` vazio; login `GET` + `type="text"` + `href="#"`; dashboard hardcoded | MÉDIO |
| Testes/Docs | Sem `tests/`, `pyproject.toml`, `requirements.txt`. README confunde "planejado" com "pronto" | MÉDIO |

**Já feito (parcial, antes deste plano):** `__init__.py` criado, imports prefixados com `escola360.` em `aluno.py`/`usuarios.py`/`main.py:5-7`, `.gitignore` existe. **Falta** `main.py:9`.

**Decisão sobre hash de senha:** usaremos `hashlib.pbkdf2_hmac` (já vem no Python, **zero instalação**), em vez de `bcrypt`. Assim uma criança consegue fazer sem `pip install` extra.

---

## FASE 1 — Fazer o projeto rodar (15 min)

**1.1 Corrigir o último import quebrado**

Abra `escola360/main.py` e, na **linha 9**, apague a linha abaixo:

```python
from avaliacao import Nota, Frequencia
```

Teste: dentro da pasta que contém a subpasta `escola360/`, rode:

```bash
python -m escola360.main
```

Deve imprimir as seções "CRIAÇÃO DE ENTIDADES", "LOGIN", etc.

**1.2 Corrigir o README**
- `README.md:66`: troque "que todos os arquivos estejam na mesma pasta" por "que você esteja na pasta raiz do repositório".
- `README.md:69`: troque `python main.py` por `python -m escola360.main`.

**1.3 Criar `requirements.txt`** (na raiz) com uma linha:
```
pytest
```

---

## FASE 2 — Segurança (senha, CPF, e-mail) (40 min)

**2.1 Adicionar imports no topo de `escola360/usuarios.py`** (depois da linha 9), cole:
```python
import hashlib
import hmac
import os
import re
from itertools import count
```

**2.2 Reescrever o `__init__` de `Usuario` (`usuarios.py:45-52`).**
- Apague as linhas 46 a 52 e escreva:
```python
        self.id_usuario = id_usuario   # usa o setter (valida)
        self.email = email             # usa o setter (valida)
        self.cpf = cpf                 # usa o setter (valida)
        self.telefone = telefone
        self.endereco = endereco
        salt = os.urandom(16)
        self.__senha_salt = salt
        self.__senha_hash = self._derivar_hash(senha, salt)
```
> Por que: agora criar usuário passa pelas regras (antes "entrava pela janela"). O nome do parâmetro continua `senha` para não quebrar quem chama.

**2.3 Trocar os métodos de senha (`usuarios.py:105-107`).** Apague `fazer_login` e escreva:
```python
    @staticmethod
    def _derivar_hash(senha: str, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, 260_000)

    def verificar_senha(self, senha: str) -> bool:
        candidato = self._derivar_hash(senha, self.__senha_salt)
        return hmac.compare_digest(candidato, self.__senha_hash)

    def fazer_login(self, email: str, senha: str) -> bool:
        return self.email == email and self.verificar_senha(senha)

    def alterar_senha(self, senha_atual: str, nova_senha: str) -> None:
        if not self.verificar_senha(senha_atual):
            raise ValueError("Senha atual incorreta")
        if len(nova_senha) < 8:
            raise ValueError("Nova senha deve ter ao menos 8 caracteres")
        salt = os.urandom(16)
        self.__senha_salt = salt
        self.__senha_hash = self._derivar_hash(nova_senha, salt)
```

**2.4 Endurecer e-mail (`usuarios.py:71-75`).** Apague o setter e escreva (a regex vai no topo, junto dos imports):
```python
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
```
```python
    @email.setter
    def email(self, value: str) -> None:
        if not _EMAIL_RE.match(value or ""):
            raise ValueError(f"Email inválido: {value!r}")
        self.__email = value
```

**2.5 Validar CPF de verdade (`usuarios.py:81-85`).** Apague o setter e escreva:
```python
    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        d = re.sub(r"\D", "", cpf or "")
        if len(d) != 11 or len(set(d)) == 1:
            return False
        for i in (9, 10):
            soma = sum(int(d[j]) * (i + 1 - j) for j in range(i))
            if (soma * 10) % 11 % 10 != int(d[i]):
                return False
        return True

    @cpf.setter
    def cpf(self, value: str) -> None:
        if not self.validar_cpf(value):
            raise ValueError(f"CPF inválido: {value!r}")
        self.__cpf = value
```
- **ATENÇÃO:** agora o `main.py` vai falhar de propósito (usa `cpf="111"` e `"444"`). Troque em `main.py` **linha 21** `cpf="111"` por `cpf="529.982.247-25"` e **linha 29** `cpf="444"` por `cpf="111.444.777-35"`. (CPFs de teste matematicamente válidos.)
- Teste: `python -m escola360.main` roda; e ao criar alguém com `cpf="111"` deve aparecer `ValueError`.

---

## FASE 3 — Encapsulamento e IDs (30 min)

**3.1 Tirar o "nome secreto" (`_Aluno__…`).**
- `aluno.py` linhas **70, 75, 79**: troque `def __adicionar_responsavel/nota/frequencia` por `def _adicionar_responsavel/nota/frequencia` (um `_` só).
- `disciplinas.py` linhas **39 e 43**: `def __adicionar_nota/frequencia` → `def _adicionar_nota/frequencia`.
- `usuarios.py`, nas linhas **254, 257, 285, 288, 328**, troque:
  - `aluno._Aluno__adicionar_nota(nota)` → `aluno._adicionar_nota(nota)`
  - `disciplina._Disciplina__adicionar_nota(nota)` → `disciplina._adicionar_nota(nota)`
  - `aluno._Aluno__adicionar_frequencia(freq)` → `aluno._adicionar_frequencia(freq)`
  - `disciplina._Disciplina__adicionar_frequencia(freq)` → `disciplina._adicionar_frequencia(freq)`
  - `aluno._Aluno__adicionar_responsavel(self)` → `aluno._adicionar_responsavel(self)`
- Teste: busque no projeto por `_Aluno__` → deve achar **zero**.

**3.2 IDs que nunca repetem.**
- `avaliacao.py`: adicione `from itertools import count` no topo e, dentro de `class Nota`, a linha `_ids = count(1)`; dentro de `class Frequencia`, `_ids = count(1)`. No `__init__` de cada uma, troque `self.__id_nota = id_nota` por `self.__id_nota = next(Nota._ids)` (e `self.__id_frequencia = next(Frequencia._ids)`).
- `relatorios.py`: adicione `from itertools import count` e `_ids = count(1)` na classe; troque `self.__id_relatorio = id_relatorio` por `self.__id_relatorio = next(Relatorio._ids)`.
- Em `usuarios.py`, troque `id_relatorio=len(self.__relatorios) + 1` (`:178`) por `id_relatorio=next(Relatorio._ids)`; `id_nota=len(self.__notas_lancadas) + 1` (`:239`) por `id_nota=next(Nota._ids)`; `id_frequencia=len(self.__frequencias) + 1` (`:272`) por `id_frequencia=next(Frequencia._ids)`.
- Teste: `python -m escola360.main` roda e as notas saem com IDs diferentes.

**3.3 Consertar `atualizar()` (`usuarios.py:123-130`).** Apague o `for` e escreva:
```python
        permitidos = {"email", "telefone", "endereco"}
        for campo, valor in dados.items():
            if campo not in permitidos:
                raise ValueError(f"campo não editável: {campo}")
            setattr(self, campo, valor)
```

---

## FASE 4 — Classe abstrata de verdade + cálculos no lugar certo (20 min)

**4.1 Tornar `Usuario` realmente abstrata.** Em `usuarios.py`, dentro de `class Usuario`, adicione:
```python
    @property
    @abstractmethod
    def tipo_usuario(self) -> str:
        ...
```
E em **cada** subclasse (`Gestor`, `Professor`, `Responsavel` em `usuarios.py`; `Aluno` em `aluno.py`) adicione:
```python
    @property
    def tipo_usuario(self) -> str:
        return "GESTOR"   # ou "PROFESSOR", "RESPONSAVEL", "ALUNO"
```
- Teste: `Usuario(1,"a@b.com","x","529.982.247-25","","")` deve dar `TypeError`.

**4.2 Mover os cálculos do `main.py` para o `Aluno`.** Em `aluno.py` adicione:
```python
    def calcular_frequencia(self, disciplina) -> float:
        freqs = [f for f in self.__frequencias if f.disciplina is disciplina]
        if not freqs:
            return 0.0
        return sum(f.status_frequencia == "P" for f in freqs) / len(freqs) * 100

    def calcular_media(self, disciplina) -> float:
        notas = [n.valor for n in self.__notas if n.disciplina is disciplina]
        return sum(notas) / len(notas) if notas else 0.0
```
Depois substitua o cálculo solto em `main.py:101-111` por chamadas a esses métodos.

---

## FASE 5 — Banco de dados (30 min)

**5.1** Em `Database/Projeto_Fisico_Escola360.sql`, **apague a linha 19** `CREATE DATABASE escola360;` e escreva no lugar:
```sql
-- Conecte antes de rodar:  \c escola360
```
**5.2 Idempotência** — no topo (logo após os comentários), acrescente `DROP TABLE IF EXISTS` para todas as tabelas na ordem inversa (avisos, frequencias, notas, prof_turma_lotacao, responsavel_aluno, responsaveis, gestores, professores, alunos, disciplinas, turmas, usuarios).

**5.3 Consertar `notas` (linhas 234-267).** Apague as linhas 239-240 (`valor_nota`, `data_lancamento`) e a constraint `uk_notas` (266-267), e escreva:
```sql
  valor          NUMERIC(4,2) NOT NULL,
  tipo_avaliacao VARCHAR(30)  NOT NULL,
  data_avaliacao DATE         NOT NULL,
  bimestre       SMALLINT,
```
E adicione ao final da tabela:
```sql
  CONSTRAINT uk_nota_avaliacao
    UNIQUE (id_aluno, id_disciplina, data_avaliacao, tipo_avaliacao)
```
> Explique pro "eu criança": antes só cabia 1 nota por matéria; agora cabem Prova + Trabalho, mas não duas iguais no mesmo dia.

**5.4 Trocar `ON DELETE CASCADE` por `ON DELETE RESTRICT`** nas FKs de `notas` e `frequencias`. (Assim apagar um professor não apaga o histórico.)

**5.5 Índices** (antes de `-- Fim do script`):
```sql
CREATE INDEX IF NOT EXISTS ix_notas_aluno       ON notas(id_aluno);
CREATE INDEX IF NOT EXISTS ix_notas_disciplina  ON notas(id_disciplina);
CREATE INDEX IF NOT EXISTS ix_freq_aluno        ON frequencias(id_aluno);
CREATE INDEX IF NOT EXISTS ix_freq_disciplina   ON frequencias(id_disciplina);
CREATE INDEX IF NOT EXISTS ix_alunos_turma      ON alunos(id_turma);
```

**5.6 Remover dado duplicado** — apague a coluna `quant_alunos` (linha 50) da tabela `turmas`.

**5.7 Criar `Database/seed.sql`** com exemplos:
```sql
INSERT INTO disciplinas (nome_disciplina) VALUES ('Matemática'), ('Português');
-- 2 notas do MESMO aluno na MESMA matéria (prova que agora pode!)
INSERT INTO notas (id_aluno, id_disciplina, id_professor, valor, tipo_avaliacao, data_avaliacao, bimestre)
VALUES (1, 1, 1, 9.0, 'PROVA', '2026-05-12', 2),
       (1, 1, 1, 8.5, 'TRABALHO', '2026-05-20', 2);
```
- Teste: rode o script 2 vezes seguidas (não deve dar erro) e `SELECT * FROM notas;` deve mostrar as 2 linhas.

---

## FASE 6 — Frontend (45 min)

**6.1 Caixinha de lápis de cor (tokens).** No topo de `docs/css/base.css` escreva:
```css
:root {
  --cor-primaria: #16305c;
  --cor-primaria-escura: rgb(3, 3, 90);
  --cor-fundo: #003f69;
  --cor-suave: #dbe9ff;
  --cor-acento: #1e5bd6;
  --cor-texto-suave: #667085;
}
```
Depois, em todos os `.css`, substitua:
`#16305c`→`var(--cor-primaria)`, `rgb(3, 3, 90)`→`var(--cor-primaria-escura)`, `#003f69`→`var(--cor-fundo)`, `#dbe9ff`→`var(--cor-suave)`, `#1e5bd6`→`var(--cor-acento)`, `#667085`→`var(--cor-texto-suave)`.
- Teste: busque por `#16305c` em `docs/css` → zero; visual continua igual.

**6.2 Parar de bloquear o site (`style.css` usa `@import`).** Em **cada** HTML (index + 5 em `paginas/`), na linha do `<link ... href="...css/style.css">`, **apague** e escreva (caminho `css/` no index e `../css/` dentro de `paginas/`):
```html
<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="css/header.css">
<link rel="stylesheet" href="css/home.css">
<link rel="stylesheet" href="css/login.css">
<link rel="stylesheet" href="css/pages.css">
<link rel="stylesheet" href="css/dashboard.css">
<link rel="stylesheet" href="css/responsive.css">
```
(Não precisa apagar `style.css`, ele só deixa de ser usado.)

**6.3 Consertar o login (`docs/paginas/login.html`).**
- Linha **40**: `<form action="dashboard.html" method="GET">` → `<form action="dashboard.html" method="POST" id="form-login">`
- Linha **43**: `type="text"` → `type="email"` (e acrescente `aria-describedby="erro-email"`)
- Linha **55**: `<a href="#">Esqueceu a senha?</a>` → `<a href="suporte.html">Esqueceu a senha?</a>`

**6.4 Meta description** — cole dentro do `<head>` de cada página (menos index, que já tem):
```html
<meta name="description" content="Escola360 - plataforma de gestão escolar.">
```

**6.5 Dashboard sem números "colados".** Crie `docs/js/dados.js`:
```javascript
const DASHBOARD_MOCK = {
  stats: { alunos: 482, professores: 38, turmas: 24, aprovacao: 92 },
  alunos: [
    { nome: "Ana Souza", turma: "9º A", media: 9.8 },
    { nome: "Bruno Lima", turma: "8º B", media: 9.5 }
  ]
};
```
E ligue via `<script src="../js/dados.js"></script>` + `<script src="../js/script.js"></script>` no fim do `dashboard.html`, preenchendo os `<span class="stat-num">` pelo `script.js`.

**6.6 Acessibilidade rápida** — no `<label for="menu-check">` de cada HTML, mantenha `aria-label="Abrir menu"`; acrescente no `<nav>` `aria-label="Menu principal"` e nos `<th>` da tabela do dashboard `scope="col"`.

---

## FASE 7 — Testes e documentação (30 min)

**7.1** Crie a pasta `tests/` com `tests/test_seguranca.py`:
```python
from datetime import date
import pytest
from escola360.usuarios import Professor

def _prof():
    return Professor(id_usuario=1, email="prof@escola.com", senha="segura123",
                     cpf="529.982.247-25", telefone="88", endereco="Rua A",
                     id_professor=1, nome="Ana", data_nascimento=date(1990, 1, 1))

def test_login_certo():
    assert _prof().fazer_login("prof@escola.com", "segura123") is True

def test_login_errado():
    assert _prof().fazer_login("prof@escola.com", "errada") is False

def test_cpf_invalido():
    with pytest.raises(ValueError):
        p = _prof(); p.cpf = "111"
```
**7.2** Rode na raiz:
```bash
pip install -r requirements.txt
python -m pytest -v
```
Tudo verde = sucesso.

**7.3 README/docs:** marque com badges o que é **implementado** vs **planejado**; corrija os typos ("aprendento"→"aprendente", "visualisar"→"visualizar", "formado"→"formato" no SQL:35).

---

## Teste final (deve passar tudo)
```bash
python -m escola360.main        # demo roda
python -m pytest -v             # testes verdes
# busca por "_Aluno__" no projeto → 0
# busca por 'senha="123"' no código → 0
```

---

# APÊNDICE AVANÇADO — Roadmap (API, autenticação, deploy)

> **Isto NÃO é correção de bug.** É o caminho para transformar o domínio POO em um produto com banco e site dinâmicos. Faça **somente depois** que as Fases 1–7 estiverem verdes. Use uma branch nova (`git checkout -b feat/api`).

## A1. Modelagem relacional alinhada (migração)
- Centralizar `cpf`/`telefone`/`endereco` em `usuarios` e remover das tabelas de perfil (`alunos`, `professores`, `gestores`, `responsaveis`) — elimina denormalização (D-04 do ROTEIRO).
- Criar `turmas` com `UNIQUE (nome_turma, turno, ano_letivo)` e `CHECK (ano_letivo BETWEEN 2000 AND 2100)`.
- Criar `avisos` com escopo (`id_turma` opcional + `publico_alvo`) e `TIMESTAMPTZ`.
- Vínculo usuário × perfil: `UNIQUE (id_usuario, tipo_usuario)` e FK composta em cada perfil.
- Um responsável principal por aluno: `CREATE UNIQUE INDEX uq_responsavel_principal ON responsavel_aluno (id_aluno) WHERE responsavel_principal;`.
- Trocar `length(lista)` por sequências vindas do banco.

## A2. Persistência com SQLAlchemy
- `pip install sqlalchemy psycopg2-binary alembic`.
- Criar `escola360/infra/` com `database.py` (engine + Session) e mapear as classes de domínio em modelos ORM (ou repositórios que convertam POO ↔ tabelas).
- Escrever `alembic init migrations` e a primeira migração a partir do SQL corrigido.

## A3. API leve (FastAPI)
- `pip install fastapi uvicorn`.
- Endpoints previstos:
  - `POST /api/v1/auth/login` (retorna token JWT)
  - `GET  /api/v1/alunos`, `GET /api/v1/alunos/{id}`
  - `GET  /api/v1/disciplinas`
  - `GET/POST /api/v1/notas`, `GET/POST /api/v1/frequencias`
  - `GET  /api/v1/relatorios/{id_aluno}`
- Teste: `curl http://localhost:8000/api/v1/disciplinas` retorna JSON.

## A4. Autenticação real (JWT + perfis)
- `pip install "python-jose[cryptography]" "passlib[bcrypt]"`.
- Reaproveitar o `tipo_usuario` (já criado na Fase 4.1) para controlar rotas: professor não acessa rota de gestor.
- Frontend: guardar token e redirecionar por perfil.

## A5. Frontend consumindo a API
- Em `docs/js/script.js`, trocar `fetch` do `DASHBOARD_MOCK` por chamadas à API; manter `dados.js` como **fallback** offline.
- Estados de carregamento/erro nas telas.

## A6. Deploy
- `docker-compose.yml` com 3 serviços: `postgres`, `api` (FastAPI), `frontend` (nginx servindo `docs/`).
- `Dockerfile` para a API.
- (Opcional) GitHub Actions: rodar `ruff`, `mypy`, `pytest` a cada push.

## A7. Longo prazo (já documentado no Projeto_Arquitetural)
- WhatsApp Business API, SendGrid (e-mails), Amazon S3 (arquivos), Google Gemini (apoio pedagógico), MFA.
- Só iniciar após A1–A6 estáveis.

---

*Plano gerado como apoio didático. Marque cada item com `[x]` conforme concluir.*
