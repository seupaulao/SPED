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
    return res.status(500).json({ erro: error.message })
  }
}

module.exports = {
  listar,
  criar
}
