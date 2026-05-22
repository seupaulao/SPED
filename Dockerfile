# =========================================================
# Dockerfile – PostgreSQL com banco de contabilidade
# =========================================================
FROM postgres:16-alpine

# Variáveis de ambiente para configuração inicial do banco
ENV POSTGRES_DB=contabilidade
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# Copia o script de inicialização para o diretório que o
# entrypoint do postgres executa automaticamente na primeira vez
COPY scripts_banco_dados/banco_postgresql.sql /docker-entrypoint-initdb.d/01_init.sql

# Porta padrão do PostgreSQL
EXPOSE 5432
