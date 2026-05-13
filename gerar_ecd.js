function formatDate(date) {
  return date.replace(/-/g, '');
}

function line(reg, fields) {
  return `|${reg}|${fields.join('|')}|`;
}

function isContaAnalitica(conta) {
	return conta.tipo == 'A';
}

function reg0000(empresa) {
  return line("0000", [
    "LECD",
    empresa.nome,
    empresa.cnpj,
    empresa.uf,
    empresa.inscricaoEstadual || "",
    empresa.municipio,
    formatDate(empresa.dataInicio),
    formatDate(empresa.dataFim),
    "BRL"
  ]);
}

function reg0007(contador) {
  return line("0007", [
    contador.nome,
    contador.cpf,
    contador.crc
  ]);
}

function regI010() {
  return line("I010", ["G"]);
}

function regI050(conta) {
  return line("I050", [
    formatDate(conta.dataInclusao || "2025-01-01"),
    conta.codigo,
    conta.codigo_pai || "",
    conta.descricao,
    "",
    conta.tipo, // A ou S
    conta.natureza || "",
    conta.codigo_referencial || ""
  ]);
}

function regI200(lcto) {
  return line("I200", [
    formatDate(lcto.data),
    lcto.numLcto,
    lcto.valorTotal.toFixed(2),
    ""
  ]);
}

function regI250(partida) {
  return line("I250", [
    partida.codConta,
    partida.codHist,
    partida.valor.toFixed(2),
    partida.tipo // D ou C
  ]);
}

function regI350(saldo) {
  return line("I350", [
    saldo.conta,
    saldo.saldoInicial.toFixed(2),
    saldo.naturezaInicial,
    saldo.debitos.toFixed(2),
    saldo.creditos.toFixed(2),
    saldo.saldoFinal.toFixed(2),
    saldo.naturezaFinal
  ]);
}

function regJ100(item) {
  return line("J100", [
    item.codigo,
    item.descricao,
    item.valor.toFixed(2),
    item.natureza
  ]);
}

function regJ150(item) {
  return line("J150", [
    item.codigo,
    item.descricao,
    item.valor.toFixed(2)
  ]);
}

function reg9999(totalLinhas) {
  return line("9999", [totalLinhas]);
}

function gerarECD(dados) {
  let linhas = [];

  linhas.push(reg0000(dados.empresa));
  linhas.push(reg0007(dados.contador));

  linhas.push(regI010());

  dados.contas.forEach(c => linhas.push(regI050(c)));

  dados.lancamentos.forEach(l => {
    linhas.push(regI200(l));
    l.partidas.forEach(p => linhas.push(regI250(p)));
  });

  dados.saldos.forEach(s => linhas.push(regI350(s)));

  dados.balanco.forEach(b => linhas.push(regJ100(b)));
  dados.dre.forEach(d => linhas.push(regJ150(d)));

  linhas.push(reg9999(linhas.length + 1));

  return linhas.join("\n");
}

function getProlabore(receita, percentual) {
	 return receita * percentual;
}

function getINSS(prolabore) { return 0.11 * prolabore; }

function getIRPJ(base) { return 0.15 * base; }

function getCSLL(base) { return 0.09 * base; }

function getPIS(receita) { return 0.0065 * receita; }

function getCOFINS(receita) { return 0.03 * receita; }

function getISS(receita) { return 0.05 * receita; }

function getAnexoSN(prolabore, receita) {
	let razao = prolabore / receita;
    return razao >= 0.28 ? 3 : 5;
}

function getAliquotaSimples(prolabore, receita) {
	return getAnexoSN(prolabore, receita) == 3 ? 0.06 : 0.15; 
}

function calcularDASSimplesNacional(receita, percentualProlab) {
	 let prolabore = getProlabore(percentualProlab);
     return receita * getAliquotaSimples(prolabore, receita);	 
}

function calcularDASLucroPresumido(receita) {
	 let base = 0.32 * receita;
	 let csll = getCSLL(base);
	 let irpj = getIRPJ(base);
	 let pis = getPIS(receita);
	 let cofins = getCOFINS(receita);
	 let iss = getISS(receita);
	 return csll + irpj + pis + cofins + iss;
}

function getMaisVantajoso(receita, percentualProlabore) {
	 let snacional = calcularDASSimplesNacional(receita, percentualProlabore) ;
	 let presumido = calcularDASLucroPresumido(receita);
	 return snacional > presumido ? presumido : snacional;
}

function calcularDASLiquido(das, retencoes) {
	 return Math.max(0, das - retencoes);
}

function addDASINSS(receita, percentualProlabore, retencoes) {
	 let das = getMaisVantajoso(receita, percentualProlabore);
	 let dasliquido = calcularDASLiquido(das, retencoes);
	 let prolabore = getProlabore(percentualProlab);
	 let inss = getINSS(prolabore);
	 return dasliquido + inss;
}

function isPrecisoECD(receita, despesa) {
	let presuncaoFiscal = 0.32;
	let limiteIsento = receita * presuncaoFiscal;
	let lucroContabil = receita - despesa;
	let distribuicaoIsenta = Math.min(lucro, limiteIsento);
	let excedenteTributavel = Math.max(0, lucro - limiteIsento);
	return excedenteTributavel > 0;
}
