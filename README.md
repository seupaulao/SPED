# PJLA Contabilidade

Aplicação de contabilidade em Python

- analise_tabelas_banco
- nota-aplicacao
- banco: contabilidade_simples.db

## passos
1. criar tela mapa demonstrações
  - consiste em montar os relatorios DVA,DFC,Balancete,Balanço,DRE aos padroes da entidade
    - permite modificar seu plano de contas e colocar contas novas para que vao compor esses campos
2. criar tela trava contabil
   - tela de trava contabil do exercicio
     - consiste em travar ou destravar o exercicio
       - a cada mes gerar um exercicio: mes ano is_closed = 1 [aberto]
         - quando ligar o programa, verificar se o exercicio existe ou nao
           - criar caso nao exista
       - travar exercicio:
         digite o mes e o ano, exercicio travado, nao pode mais :
           - criar, excluir, alterar lancamentos
           - pode estornar, ajustar lançamento  
       - destravar exercicio    
         digite o mes e o ano, exercicio destravado
       - so o contador pode travar ou destravar o exercicio

