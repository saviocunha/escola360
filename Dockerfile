# Usa uma imgagem oficial do Python, bem leve (alpine ou slim)

FROM python:3.12-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia apenas o arquivo de dependências primeiro (otimização de cache do Docker)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da aplicação para dentro do contêiner
COPY . .

# Comando para rodar a aplicação quando o contêiner iniciar
CMD ["python", "-m", "escola360.main"]

INSTRUCAO_INVALIDA
