const router = require('express').Router()
const controller = require('../controllers/empresa.controller')

router.get('/', controller.listar)
router.post('/', controller.criar)

module.exports = router
