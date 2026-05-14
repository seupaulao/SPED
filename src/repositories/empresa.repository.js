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
