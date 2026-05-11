/**
 * financialRatios.js
 * Funções de indicadores financeiros para análise de demonstrações contábeis
 * Todas as funções assumem valores numéricos (Number)
 */

const FinancialRatios = {

  // ==============================
  // 💧 LIQUIDEZ
  // ==============================

  /**
   * Current Ratio (Liquidez Corrente)
   * Mede a capacidade de pagar obrigações de curto prazo
   * Fórmula: Current Assets / Current Liabilities
   * 🎯 Ideal: > 1.5 (seguro), > 2 (muito confortável)
   */
  currentRatio: (currentAssets, currentLiabilities) => {
    return currentAssets / currentLiabilities;
  },

  /**
   * Quick Ratio (Liquidez Seca)
   * Exclui estoques (menos líquidos)
   * Fórmula: (Current Assets - Inventory) / Current Liabilities
   * 🎯 Ideal: > 1
   */
  quickRatio: (currentAssets, inventory, currentLiabilities) => {
    return (currentAssets - inventory) / currentLiabilities;
  },

  /**
   * Cash Ratio (Liquidez Imediata)
   * Mede capacidade de pagar dívidas apenas com caixa
   * Fórmula: Cash / Current Liabilities
   * 🎯 Ideal: 0.2 a 0.5 (muito alto pode indicar ociosidade)
   */
  cashRatio: (cash, currentLiabilities) => {
    return cash / currentLiabilities;
  },

  /**
   * Working Capital (Capital de Giro)
   * Recursos disponíveis no curto prazo
   * Fórmula: Current Assets - Current Liabilities
   * 🎯 Ideal: Positivo
   */
  workingCapital: (currentAssets, currentLiabilities) => {
    return currentAssets - currentLiabilities;
  },

  // ==============================
  // 🏦 ENDIVIDAMENTO
  // ==============================

  /**
   * Debt to Equity (D/E)
   * Mede o quanto a empresa depende de capital de terceiros
   * Fórmula: Total Debt / Equity
   * 🎯 Ideal: < 1 (depende do setor)
   */
  debtToEquity: (totalDebt, equity) => {
    return totalDebt / equity;
  },

  /**
   * Debt Ratio
   * Percentual dos ativos financiados por dívida
   * Fórmula: Total Debt / Total Assets
   * 🎯 Ideal: < 0.6
   */
  debtRatio: (totalDebt, totalAssets) => {
    return totalDebt / totalAssets;
  },

  /**
   * Interest Coverage Ratio
   * Capacidade de pagar juros
   * Fórmula: EBIT / Interest Expense
   * 🎯 Ideal: > 3 (seguro), > 5 (excelente)
   */
  interestCoverage: (ebit, interestExpense) => {
    return ebit / interestExpense;
  },

  /**
   * Debt Service Coverage Ratio (DSCR)
   * Capacidade de pagar dívida total (juros + principal)
   * Fórmula: Operating Income / Debt Service
   * 🎯 Ideal: > 1.2
   */
  dscr: (operatingIncome, debtService) => {
    return operatingIncome / debtService;
  },

  // ==============================
  // 📈 RENTABILIDADE
  // ==============================

  /**
   * Gross Margin
   * Lucro bruto sobre receita
   * Fórmula: (Revenue - COGS) / Revenue
   * 🎯 Ideal: Quanto maior, melhor (depende do setor)
   */
  grossMargin: (revenue, cogs) => {
    return (revenue - cogs) / revenue;
  },

  /**
   * Operating Margin
   * Eficiência operacional
   * Fórmula: Operating Income / Revenue
   * 🎯 Ideal: > 10% geralmente bom
   */
  operatingMargin: (operatingIncome, revenue) => {
    return operatingIncome / revenue;
  },

  /**
   * Net Profit Margin
   * Lucro líquido sobre receita
   * Fórmula: Net Income / Revenue
   * 🎯 Ideal: > 10% bom, > 20% excelente
   */
  netMargin: (netIncome, revenue) => {
    return netIncome / revenue;
  },

  /**
   * Return on Assets (ROA)
   * Eficiência dos ativos
   * Fórmula: Net Income / Total Assets
   * 🎯 Ideal: > 5%
   */
  roa: (netIncome, totalAssets) => {
    return netIncome / totalAssets;
  },

  /**
   * Return on Equity (ROE)
   * Retorno para os sócios
   * Fórmula: Net Income / Equity
   * 🎯 Ideal: > 15%
   */
  roe: (netIncome, equity) => {
    return netIncome / equity;
  },

  /**
   * Return on Invested Capital (ROIC)
   * Eficiência do capital investido
   * Fórmula: NOPAT / Invested Capital
   * 🎯 Ideal: > custo de capital (WACC)
   */
  roic: (nopat, investedCapital) => {
    return nopat / investedCapital;
  },

  // ==============================
  // 🔄 EFICIÊNCIA
  // ==============================

  /**
   * Asset Turnover
   * Uso eficiente dos ativos
   * Fórmula: Revenue / Total Assets
   * 🎯 Ideal: Quanto maior, melhor
   */
  assetTurnover: (revenue, totalAssets) => {
    return revenue / totalAssets;
  },

  /**
   * Inventory Turnover
   * Velocidade de giro do estoque
   * Fórmula: COGS / Inventory
   * 🎯 Ideal: Alto (depende do setor)
   */
  inventoryTurnover: (cogs, inventory) => {
    return cogs / inventory;
  },

  /**
   * Receivables Turnover
   * Eficiência na cobrança
   * Fórmula: Revenue / Accounts Receivable
   * 🎯 Ideal: Alto
   */
  receivablesTurnover: (revenue, receivables) => {
    return revenue / receivables;
  },

  /**
   * Payables Turnover
   * Frequência de pagamento a fornecedores
   * Fórmula: COGS / Accounts Payable
   * 🎯 Ideal: Moderado (não muito alto)
   */
  payablesTurnover: (cogs, payables) => {
    return cogs / payables;
  },

  // ==============================
  // ⏱️ CICLO DE CAIXA
  // ==============================

  /**
   * Days Sales Outstanding (DSO)
   * Prazo médio de recebimento
   * Fórmula: (Accounts Receivable / Revenue) * 365
   * 🎯 Ideal: Baixo
   */
  dso: (receivables, revenue) => {
    return (receivables / revenue) * 365;
  },

  /**
   * Days Inventory Outstanding (DIO)
   * Tempo médio de estoque
   * Fórmula: (Inventory / COGS) * 365
   * 🎯 Ideal: Baixo
   */
  dio: (inventory, cogs) => {
    return (inventory / cogs) * 365;
  },

  /**
   * Days Payables Outstanding (DPO)
   * Prazo médio de pagamento
   * Fórmula: (Accounts Payable / COGS) * 365
   * 🎯 Ideal: Alto (sem prejudicar fornecedores)
   */
  dpo: (payables, cogs) => {
    return (payables / cogs) * 365;
  },

  /**
   * Cash Conversion Cycle (CCC)
   * Tempo para converter investimento em caixa
   * Fórmula: DSO + DIO - DPO
   * 🎯 Ideal: Baixo ou negativo
   */
  ccc: (dso, dio, dpo) => {
    return dso + dio - dpo;
  },

  // ==============================
  // 💸 FLUXO DE CAIXA
  // ==============================

  /**
   * Free Cash Flow (FCF)
   * Caixa disponível após investimentos
   * Fórmula: Operating Cash Flow - CAPEX
   * 🎯 Ideal: Positivo e crescente
   */
  freeCashFlow: (operatingCashFlow, capex) => {
    return operatingCashFlow - capex;
  },

  /**
   * Cash Flow Margin
   * Geração de caixa sobre receita
   * Fórmula: Operating Cash Flow / Revenue
   * 🎯 Ideal: Alto
   */
  cashFlowMargin: (operatingCashFlow, revenue) => {
    return operatingCashFlow / revenue;
  }

};

module.exports = FinancialRatios;
