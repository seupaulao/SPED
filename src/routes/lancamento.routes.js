const router = require('express').Router()
const controller = require('../controllers/lancamento.controller')

router.post('/', controller.criar)

module.exports = router
