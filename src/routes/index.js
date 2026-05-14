const Router = require('express').Router()
const empresaRoutes = require('./empresa.routes')
const lancamentoRoutes = require('./lancamento.routes')
const relatorioRoutes = require('./relatorio.routes')

Router.use('/empresas', empresaRoutes)
Router.use('/lancamentos', lancamentoRoutes)
Router.use('/relatorios', relatorioRoutes)

module.exports = Router
