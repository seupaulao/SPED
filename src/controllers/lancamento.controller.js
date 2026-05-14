// Placeholder controller for creating lançamentos
const service = require('../services/lancamento.service')

async function criar(req, res) {
  try {
    const result = await service.criarLancamento(req.body)
    return res.status(201).json(result)
  } catch (error) {
    return res.status(400).json({ erro: error.message })
  }
}

module.exports = { criar }
