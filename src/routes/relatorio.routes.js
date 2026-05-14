const router = require('express').Router()
const controller = require('../controllers/relatorio.controller')

router.get('/balancete/:empresaId', controller.balancete)
router.get('/dre/:empresaId', controller.dre)

module.exports = router
