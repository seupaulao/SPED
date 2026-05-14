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

module.exports = { balancete, dre }
