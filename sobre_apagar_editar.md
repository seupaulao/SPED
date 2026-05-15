Em contabilidade, a regra principal é:

> **Você pode corrigir um lançamento enquanto ele ainda não produziu efeitos formais/fiscais definitivos.**
> Depois disso, normalmente não se apaga mais nada — faz-se ajuste, estorno ou lançamento complementar.

Isso é importante tanto tecnicamente quanto juridicamente, principalmente se seu sistema for usado para gerar SPED, ECD, balancetes, DRE ou servir de prova contábil.

---

# 1. Quando você PODE editar ou excluir

## Situação 1 — Lançamento ainda “provisório”

Você pode permitir edição/exclusão livre quando:

* o período ainda está aberto;
* o mês não foi encerrado;
* não houve emissão de relatórios oficiais;
* não foi entregue:

  * ECD;
  * ECF;
  * SPED;
  * folha;
  * obrigação fiscal;
* o lançamento ainda está em conferência interna.

Exemplo:

* digitou conta errada;
* duplicou lançamento;
* valor digitado incorretamente.

Nesse estágio:

* editar é aceitável;
* excluir também.

---

# 2. Quando NÃO deve mais apagar

Depois que:

* o mês foi fechado;
* houve conciliação;
* foi emitido balancete;
* foi entregue obrigação acessória;
* o contador assinou;
* houve auditoria;
* o cliente já recebeu relatório;

…o correto é:

* NÃO apagar;
* NÃO alterar historicamente.

Porque isso quebra:

* rastreabilidade;
* trilha de auditoria;
* integridade do razão;
* coerência do SPED.

---

# 3. O que fazer então?

Aí entram:

* estorno;
* ajuste;
* lançamento complementar.

---

# 4. Diferença entre ESTORNO e AJUSTE

## ESTORNO

O estorno “anula” um lançamento errado.

Você cria um lançamento inverso.

---

### Exemplo

Lançamento errado:

| Conta       | Débito | Crédito |
| ----------- | ------ | ------- |
| Combustível | 500    |         |
| Caixa       |        | 500     |

Mas era despesa de manutenção.

Você NÃO apaga.

Você faz:

### Estorno

| Conta       | Débito | Crédito |
| ----------- | ------ | ------- |
| Caixa       | 500    |         |
| Combustível |        | 500     |

Depois lança o correto:

| Conta      | Débito | Crédito |
| ---------- | ------ | ------- |
| Manutenção | 500    |         |
| Caixa      |        | 500     |

---

## AJUSTE

O ajuste corrige parcialmente um lançamento.

O lançamento original continua válido, mas incompleto/incorreto em parte.

---

### Exemplo

Salário lançado:

* R$ 1.500

Mas deveria:

* R$ 1.600

Você faz ajuste de:

* R$ 100

| Conta            | Débito | Crédito |
| ---------------- | ------ | ------- |
| Despesa Salários | 100    |         |
| Salários a Pagar |        | 100     |

---

# 5. Melhor prática para sistemas contábeis

O ideal é seu sistema ter:

## Estados do período

### Aberto

Permite:

* editar;
* excluir.

### Fechado

Bloqueia:

* edição;
* exclusão.

Permite apenas:

* estorno;
* ajuste.

---

# 6. Melhor prática profissional

## Nunca delete fisicamente

Mesmo antes do fechamento.

Em vez disso:

* use `deleted_at`;
* ou `ativo = false`;
* ou `status = ESTORNADO`.

Isso cria trilha de auditoria.

---

# 7. Modelo ideal de status

Exemplo:

| Status    | Significado                    |
| --------- | ------------------------------ |
| RASCUNHO  | Pode editar/excluir            |
| EFETIVADO | Entrou no razão                |
| FECHADO   | Não altera                     |
| ESTORNADO | Anulado por lançamento inverso |
| AJUSTADO  | Recebeu complemento            |

---

# 8. Como ERPs fazem

Softwares como:

* Domínio Sistemas
* Alterdata
* TOTVS Protheus
* Omie

normalmente:

* bloqueiam períodos fechados;
* exigem senha de supervisor para reabrir;
* geram logs;
* fazem estorno automático;
* mantêm histórico completo.

---

# 9. Estrutura recomendada para seu banco

No lançamento:

```sql
id
data
historico
valor
status
lancamento_origem_id
estornado_por_id
created_at
updated_at
deleted_at
usuario_id
```

---

# 10. Regra prática excelente para usar

## Regra simples

### Pode editar/excluir:

* enquanto o mês estiver ABERTO.

### Não pode:

* após fechamento contábil/fiscal.

### Após fechamento:

* somente:

  * estorno;
  * ajuste;
  * lançamento complementar.

---

# 11. O que eu recomendaria para seu sistema Python

## Implementar:

### 1. Fechamento mensal

Tabela:

```sql
periodos_contabeis
```

Com:

* mês;
* ano;
* status aberto/fechado.

---

### 2. Soft delete

Nunca apagar de verdade.

---

### 3. Log de alterações

Tabela:

```sql
auditoria_lancamentos
```

Guardando:

* usuário;
* antes;
* depois;
* timestamp.

---

### 4. Estorno automático

Botão:

* “Estornar lançamento”.

O sistema gera automaticamente o inverso.

---

# 12. Regra fiscal importante no Brasil

A escrituração contábil deve respeitar:

* ITG 2000;
* NBC TG;
* princípio da integridade;
* rastreabilidade documental.

Em auditoria:

* apagar lançamento histórico é muito mal visto;
* estorno é o procedimento correto.

---

# 13. Resumo final

## Antes do fechamento:

✅ editar
✅ excluir

## Depois do fechamento:

❌ não editar
❌ não excluir

### Faça:

✅ estorno
✅ ajuste
✅ complemento

---

Um modelo muito sólido é:

> “Razão imutável após fechamento.”

Isso aproxima seu sistema de um ERP contábil profissional e evita muitos problemas futuros com SPED, auditoria e consistência histórica.
