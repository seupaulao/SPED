## WebApp Node.js + PostgreSQL — Métodos Base para Sistema Contábil

### Stack sugerida
Node.js
Express
PostgreSQL
Knex.js ou Prisma
JWT
pg (driver PostgreSQL)

### Estrutura sugerida

```
src/
 ├── db/
 │    ├── connection.js
 │    └── migrations/
 │
 ├── modules/
 │    ├── empresa/
 │    ├── plano-contas/
 │    ├── lancamentos/
 │    ├── relatorios/
 │    └── auth/
 │
 ├── services/
 ├── repositories/
 ├── controllers/
 ├── routes/
 ├── middlewares/
 └── app.js
```

### Instalação

```
npm init -y
npm install express pg dotenv cors
npm install nodemon --save-dev
```

### Conexão PostgreSQL

src/db/connection.js

```
const { Pool } = require('pg')
require('dotenv').config()

const pool = new Pool({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
})

module.exports = pool
```

.env

```
PORT=3000
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=123456
DB_NAME=contabilidade
APP EXPRESS
```

src/app.js
```
const express = require('express')
const cors = require('cors')

const empresaRoutes = require('./routes/empresa.routes')
const lancamentoRoutes = require('./routes/lancamento.routes')
const relatorioRoutes = require('./routes/relatorio.routes')

const app = express()

app.use(cors())
app.use(express.json())

app.use('/empresas', empresaRoutes)
app.use('/lancamentos', lancamentoRoutes)
app.use('/relatorios', relatorioRoutes)

app.listen(3000, () => {
  console.log('Servidor iniciado na porta 3000')
})
```

### EMPRESAS

Repository

src/repositories/empresa.repository.js

```
const db = require('../db/connection')


async function listar() {
  const result = await db.query(`
    SELECT *
    FROM empresa
    ORDER BY nome
  `)


  return result.rows
}


async function buscarPorId(id) {
  const result = await db.query(`
    SELECT *
    FROM empresa
    WHERE id = $1
  `, [id])


  return result.rows[0]
}


async function criar(data) {
  const result = await db.query(`
    INSERT INTO empresa
    (
      cnpj,
      nome,
      uf,
      municipio,
      data_inicio
    )
    VALUES ($1,$2,$3,$4,$5)
    RETURNING *
  `, [
    data.cnpj,
    data.nome,
    data.uf,
    data.municipio,
    data.data_inicio
  ])


  return result.rows[0]
}


module.exports = {
  listar,
  buscarPorId,
  criar
}
```

### CONTROLLER EMPRESA

src/controllers/empresa.controller.js


```
const repository = require('../repositories/empresa.repository')


async function listar(req, res) {
  const empresas = await repository.listar()


  return res.json(empresas)
}


async function criar(req, res) {
  try {
    const empresa = await repository.criar(req.body)


    return res.status(201).json(empresa)
  } catch (error) {
    return res.status(500).json({
      erro: error.message
    })
  }
}


module.exports = {
  listar,
  criar
}
```

### ROUTES EMPRESA

src/routes/empresa.routes.js

```
const router = require('express').Router()
const controller = require('../controllers/empresa.controller')


router.get('/', controller.listar)
router.post('/', controller.criar)


module.exports = router
```

### PLANO DE CONTAS

**Criar conta**

src/repositories/plano.repository.js

```
const db = require('../db/connection')


async function criar(data) {
  const result = await db.query(`
    INSERT INTO plano_contas
    (
      empresa_id,
      codigo,
      descricao,
      tipo,
      natureza,
      nivel,
      conta_pai_id,
      aceita_lancamento
    )
    VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
    RETURNING *
  `, [
    data.empresa_id,
    data.codigo,
    data.descricao,
    data.tipo,
    data.natureza,
    data.nivel,
    data.conta_pai_id,
    data.aceita_lancamento
  ])


  return result.rows[0]
}


async function listarPorEmpresa(empresaId) {
  const result = await db.query(`
    SELECT *
    FROM plano_contas
    WHERE empresa_id = $1
    ORDER BY codigo
  `, [empresaId])


  return result.rows
}


module.exports = {
  criar,
  listarPorEmpresa
}
```

### LANÇAMENTOS CONTÁBEIS

**Regra importante**

Sempre:

- soma débitos = soma créditos

**Criar lançamento completo**

src/services/lancamento.service.js

```
const db = require('../db/connection')
    }


    const lancamentoResult = await client.query(`
      INSERT INTO lancamento
      (
        empresa_id,
        data,
        historico,
        valor_total,
        tipo
      )
      VALUES ($1,$2,$3,$4,$5)
      RETURNING *
    `, [
      data.empresa_id,
      data.data,
      data.historico,
      totalDebitos,
      'N'
    ])


    const lancamento = lancamentoResult.rows[0]


    for (const item of data.itens) {
      await client.query(`
        INSERT INTO lancamento_item
        (
          lancamento_id,
          conta_id,
          tipo,
          valor,
          historico
        )
        VALUES ($1,$2,$3,$4,$5)
      `, [
        lancamento.id,
        item.conta_id,
        item.tipo,
        item.valor,
        item.historico
      ])
    }


    await client.query('COMMIT')


    return lancamento


  } catch (error) {
    await client.query('ROLLBACK')
    throw error
  } finally {
    client.release()
  }
}


module.exports = {
  criarLancamento
}
```

**Controller lançamento**

src/controllers/lancamento.controller.js

```
const service = require('../services/lancamento.service')


async function criar(req, res) {
  try {
    const result = await service.criarLancamento(req.body)


    return res.status(201).json(result)


  } catch (error) {
    return res.status(400).json({
      erro: error.message
    })
  }
}


module.exports = {
  criar
}
```

**Routes lançamento**

src/routes/lancamento.routes.js

```
const router = require('express').Router()
const controller = require('../controllers/lancamento.controller')


router.post('/', controller.criar)


module.exports = router
```

### EXEMPLO JSON 

POST /lancamentos

```
{
  "empresa_id": 1,
  "data": "2026-05-01",
  "historico": "Recebimento consultas",
  "itens": [
    {
      "conta_id": 2,
      "tipo": "D",
      "valor": 12000
    },
    {
      "conta_id": 4,
      "tipo": "C",
      "valor": 12000
    }
  ]
}
```

### RAZÃO CONTÁBIL

src/repositories/razao.repository.js

```
const db = require('../db/connection')


async function razao(contaId, dataInicio, dataFim) {
  const result = await db.query(`
    SELECT
      l.data,
      l.historico,
      li.tipo,
      li.valor


    FROM lancamento_item li


    INNER JOIN lancamento l
      ON l.id = li.lancamento_id


    WHERE li.conta_id = $1
      AND l.data BETWEEN $2 AND $3


    ORDER BY l.data
  `, [contaId, dataInicio, dataFim])


  return result.rows
}


module.exports = {
  razao
}
```

### BALANCETE

src/repositories/balancete.repository.js

```
const db = require('../db/connection')


async function balancete(empresaId) {
  const result = await db.query(`
    SELECT
      pc.codigo,
      pc.descricao,


      SUM(
        CASE
          WHEN li.tipo = 'D' THEN li.valor
          ELSE 0
        END
      ) AS debitos,


      SUM(
        CASE
          WHEN li.tipo = 'C' THEN li.valor
          ELSE 0
        END
      ) AS creditos


    FROM plano_contas pc


    LEFT JOIN lancamento_item li
      ON li.conta_id = pc.id


    LEFT JOIN lancamento l
      ON l.id = li.lancamento_id


    WHERE pc.empresa_id = $1


    GROUP BY
      pc.codigo,
      pc.descricao


    ORDER BY pc.codigo
  `, [empresaId])


  return result.rows
}


module.exports = {
  balancete
}
```

### DRE

src/repositories/dre.repository.js

```
const db = require('../db/connection')


async function dre(empresaId) {
  const result = await db.query(`
    SELECT
      md.categoria,


      SUM(
        CASE
          WHEN li.tipo = 'C' THEN li.valor
          ELSE -li.valor
        END
      ) AS total


    FROM mapa_demonstracoes md


    INNER JOIN plano_contas pc
      ON pc.id = md.conta_id


    INNER JOIN lancamento_item li
      ON li.conta_id = pc.id


    INNER JOIN lancamento l
      ON l.id = li.lancamento_id


    WHERE md.tipo = 'DRE'
      AND pc.empresa_id = $1


    GROUP BY md.categoria


    ORDER BY md.categoria
  `, [empresaId])


  return result.rows
}


module.exports = {
  dre
}
```

### RELATÓRIOS CONTROLLER

src/controllers/relatorio.controller.js

```
const balanceteRepository = require('../repositories/balancete.repository')
const dreRepository = require('../repositories/dre.repository')


async function balancete(req, res) {
  const empresaId = req.params.empresaId


  const data = await balanceteRepository.balancete(empresaId)


  return res.json(data)
}


async function dre(req, res) {
  const empresaId = req.params.empresaId


  const data = await dreRepository.dre(empresaId)


  return res.json(data)
}


module.exports = {
  balancete,
  dre
}
```

### RELATÓRIOS ROUTES

src/routes/relatorio.routes.js

```
const router = require('express').Router()
const controller = require('../controllers/relatorio.controller')


router.get('/balancete/:empresaId', controller.balancete)
router.get('/dre/:empresaId', controller.dre)


module.exports = router
```

### EXEMPLO DE LANÇAMENTO DA MÉDICA
```
const axios = require('axios')


async function teste() {
  await axios.post('http://localhost:3000/lancamentos', {
    empresa_id: 1,
    data: '2026-01-10',
    historico: 'Consultas Janeiro',


    itens: [
      {
        conta_id: 2,
        tipo: 'D',
        valor: 12000
      },
      {
        conta_id: 4,
        tipo: 'C',
        valor: 12000
      }
    ]
  })
}

teste()
```


### MELHORIAS FUTURAS
1. Autenticação JWT
`npm install jsonwebtoken bcrypt`

2. Multi-tenant

Adicionar `usuario_id` nas empresas.

3. Fechamento contábil

Tabela:

`periodo_fechado`

4. SPED ECD

Você já possui estrutura quase pronta para:

I050
I200
I250

5. Importação OFX

Muito importante para automação bancária.

6. Dashboard React

Você pode consumir:

- `/relatorios/balancete`
- `/relatorios/dre`
- `/lancamentos`

para gerar:

- gráficos
- fluxo de caixa
- DRE mensal
- indicadores

**Sugestão importante**

Você deve criar:

Tabela usuarios

```
CREATE TABLE usuario (
  id SERIAL PRIMARY KEY,
  nome TEXT,
  email TEXT UNIQUE,
  senha_hash TEXT
);
```

**Sugestão de evolução arquitetural**

MVP
- Express
- PostgreSQL
- React

Escalável
- NestJS
- Prisma
- Redis
- BullMQ
- RabbitMQ
- Docker
- Kubernetes

Fluxo ideal do sistema
1. Cadastro empresa
2. Importação plano contas
3. Cadastro histórico padrão
4. Lançamentos
5. Balancete
6. DRE
7. Encerramento
8. SPED
9. PDF
10. Assinatura digital

