# Arquivo de testes das entidades e métodos implementados e definidos.
from datetime import date

# Importações de classes de outros módulos para uso na demonstração
from escola360.usuarios import Professor, Gestor, Responsavel
from escola360.aluno import Aluno
from escola360.disciplinas import Disciplina


def demo() -> None:
    """Função principal de demonstração do sistema."""
    
    ## 1. CRIAÇÃO DE USUÁRIOS E ENTIDADES

    print("--- 1. CRIAÇÃO DE ENTIDADES ---")

    # Criação do objeto Professor
    prof = Professor(
        id_usuario=1, email="joao@escola.com", senha="123",
        cpf="529.982.247-25", telefone="9999", endereco="Rua X",
        id_professor=10, nome="João Silva", data_nascimento=date(1980, 1, 1),
    )
    print(f"Professor criado: {prof.nome} (ID: {prof.id_professor})")

    # Criação do objeto Aluno
    aluno_ana = Aluno(
        id_usuario=4, email="ana@escola.com", senha="123",
        cpf="111.444.777-35", telefone="6666", endereco="Rua W",
        id_aluno=40, nome="Ana Pereira", data_nascimento=date(2010, 5, 10),
    )
    
    # Criação dos objetos Disciplinas
    disc_mat = Disciplina(id_disciplina=100, nome="Matemática")
    disc_port = Disciplina(id_disciplina=101, nome="Português")

    print("-" * 40)

    ## 2. TESTES DE AUTENTICAÇÃO (LOGIN)
    print("--- 2. TESTES DE AUTENTICAÇÃO ---")
    
    # Login correto (deve retornar True)
    if prof.fazer_login("joao@escola.com", "123"):
        print(f"Login de {prof.nome}: SUCESSO.")
    
    # Login incorreto (deve retornar False)
    if not prof.fazer_login("joao@escola.com", "senha_errada"):
        print(f"Login de {prof.nome}: FALHA (esperado).")

    print("-" * 40)

    ## 3. SIMULAÇÃO DO PROFESSOR: LANÇAMENTO E VALIDAÇÃO
    print("--- 3. LANÇAMENTO DE NOTAS E VALIDAÇÃO ---")

    # Lançamento 1: Nota válida (9.0)
    prof.lancar_nota(
        aluno=aluno_ana,
        disciplina=disc_mat,
        data_avaliacao=date(2025, 10, 15),
        tipo_avaliacao="Prova Mensal",
        valor=9.0,
    )
    print(f"Nota 9.0 em {disc_mat.nome} lançada com sucesso.")

    # Lançamento 2: Nota válida (7.5)
    prof.lancar_nota(
        aluno=aluno_ana,
        disciplina=disc_port,
        data_avaliacao=date(2025, 10, 20),
        tipo_avaliacao="Trabalho",
        valor=7.5,
    )
    print(f"Nota 7.5 em {disc_port.nome} lançada com sucesso.")

    # Teste de Validação de Erro (Nota fora do range - 11.0)
    try:
        prof.lancar_nota(
            aluno=aluno_ana,
            disciplina=disc_mat,
            data_avaliacao=date.today(),
            tipo_avaliacao="Recuperação",
            valor=11.0,  # Valor inválido (deve gerar ValueError)
        )
    except ValueError as e:
        # Captura o erro esperado, demonstrando a regra de negócio
        print(f"Teste de Erro de Nota: SUCESSO. Erro capturado: {e}")
    
    print("-" * 40)

    ## 4. TESTES DE FREQUÊNCIA E CÁLCULOS
    print("--- 4. TESTES DE FREQUÊNCIA E CÁLCULOS ---")

    # Registro de múltiplas frequências em Matemática
    prof.registrar_frequencia(aluno_ana, disc_mat, date(2025, 11, 1), presente=True)
    prof.registrar_frequencia(aluno_ana, disc_mat, date(2025, 11, 2), presente=True)
    prof.registrar_frequencia(aluno_ana, disc_mat, date(2025, 11, 3), presente=False) # Falta
    prof.registrar_frequencia(aluno_ana, disc_mat, date(2025, 11, 4), presente=True)
    prof.registrar_frequencia(aluno_ana, disc_mat, date(2025, 11, 5), presente=False) # Falta

    # O cálculo é feito próprio Aluno (método da classe)
    porcentagem = aluno_ana.calcular_frequencia(disc_mat)
    print(f"Porcentagem de Frequência em {disc_mat.nome}: {porcentagem:.2f}%")

    # A média é calculada pelo metodo do Aluno
    media = aluno_ana.calcular_media(disc_mat)
    print(f"Media de {aluno_ana.nome} em {disc_mat.nome}: {media:.2f}")


    print("-" * 40)

    ## 5. TESTES DE RELACIONAMENTO (CONSULTA ALUNO/DISCIPLINA)
    print("--- 5. TESTES DE RELACIONAMENTO ---")
    
    # Consulta das notas de Ana (usando o método público do Aluno)
    print(f"Notas registradas para {aluno_ana.nome}:")
    for n in aluno_ana.consultar_nota():
        print(f"  > {n.disciplina.nome}: {n.valor} ({n.tipo_avaliacao})")

    # Consulta das notas na Disciplina de Matemática (usando o property da Disciplina)
    print(f"Notas registradas em {disc_mat.nome}:")
    for n in disc_mat.notas:
        # A Nota tem referência ao Aluno
        print(f"  > Aluno: {n.aluno.nome}, Nota: {n.valor}")

    print("-" * 40)

if __name__ == "__main__":
    # Execução da demonstração ao rodar o script
    demo()
