Arquitetura da solução (resumo enxuto)

Visão geral
- Backend em Node.js usando Express. Persistência em PostgreSQL.
- Arquitetura em camadas: Routes -> Controllers -> Services -> Repositories -> DB.
- Lançamentos contábeis criados via serviço que executa transação no banco (garantia de atomicidade).

Diretório principal (src/)
- src/routes: definição de rotas HTTP
- src/controllers: tratamento de requisições e respostas
- src/services: lógica de negócio (ex: criar lançamento com validação e transação)
- src/repositories: consultas SQL e operações diretas no DB
- src/db: conexão e utilitários do banco
- src/middlewares: autenticação, validação

Decisões operacionais
- Usar Pool do driver 'pg' para conexões; considerar Prisma ou Knex para migrations/ORM conforme preferência.
- Garantir validação de integridade contábil (débito = crédito) antes de persistir.
- APIs REST simples para empresa, plano de contas, lançamentos e relatórios (balancete, DRE).

Escalabilidade futura
- Separar serviços em módulos, introduzir Redis/BullMQ para tarefas assíncronas, API Gateway e Docker/Kubernetes quando necessário.

Observação final
- Mínimo viável já criado; próximos passos: migrations, completar módulos e testes.
