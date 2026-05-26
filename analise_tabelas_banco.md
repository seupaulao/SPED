# Análise das Tabelas do Banco de Dados - SPED / Contabilidade

Documento baseado no script `banco_sqlite3_novo.sql`. O arquivo descreve cada tabela criada, seu propósito e relacionamentos principais.

---

## Tabela: `empresa`
Armazena os dados básicos das empresas/clientes atendidos pelo escritório contábil.

Campos principais:
- `id`: chave primária autoincrement.
- `cnpj`, `nome`: identificação obrigatória da empresa.
- `uf`, `municipio`: localização fiscal.
- `data_inicio`, `data_fim`: período de vigência ou atividade.
- `created_at`: registro de criação.
- `excluido_at`: marca de exclusão lógica.

Uso: central para isolar dados de cada cliente; referenciada por planos de contas, lançamentos, centros de custo e configuração.

---


## Tabela: `trava_contabil`
Representa o fechamento contábil de períodos.

Campos:
- `id`: chave primária textual.
- `empresa_id`: empresa afetada.
- `ano`, `mes`: período fechado.
- `is_closed`: flag de fechamento.
- `closed_by`: usuário que fechou.
- `closed_at`: data do fechamento.

Uso: controle de travamento de períodos contábeis.

---

## Tabela: `plano_contas`
Registra o plano de contas da empresa, com estrutura hierárquica e atributos contábeis.

Campos:
- `id`: chave primária autoincrement.
- `empresa_id`: vincula a conta à empresa.
- `plano_contas_referencial_id`: link opcional ao catálogo referencial.
- `codigo`, `descricao`: identificação da conta.
- `tipo`: tipo de conta (sintética ou analítica).
- `natureza`, `nivel`, `conta_pai_id`: hierarquia e natureza contábil.
- `codigo_referencial`, `aceita_lancamento`: integração externa e controle de lançamentos.
- `grupo`, `subgrupo`, `dre_grupo`, `fluxo_caixa_tipo`: classificações para relatórios.
- `created_at`, `excluido_at`: auditoria e exclusão lógica.

Uso: é o núcleo do sistema contábil, referenciado por itens de lançamento, mapas de demonstrativos e SPED.

---

## Tabela: `lancamento`
Cabeçalho dos lançamentos contábeis.

Campos:
- `id`: chave primária autoincrement.
- `empresa_id`: empresa do lançamento.
- `data`: data do lançamento.
- `historico`: descrição livre.
- `tipo`: tipo de lançamento, padrão `N`.
- `created_at`, `excluido_at`: auditoria e exclusão lógica.

Uso: agrupa itens de débito e crédito, representando cada transação contábil.

---

## Tabela: `lancamento_item`
Itens de cada lançamento, implementando partidas dobradas.

Campos:
- `id`: chave primária.
- `lancamento_id`: referência ao cabeçalho de lançamento, com `ON DELETE CASCADE`.
- `conta_id`: conta afetada.
- `centro_custo_id`: centro de custo opcional.
- `tipo`: `D` ou `C` (débito ou crédito).
- `valor`: valor do item.

Uso: registra linhas de débito/crédito e permite validação de equilíbrio entre lançamentos.

---

## Tabela: `mapa_demonstracoes`
Mapeia contas a categorias de demonstrações financeiras.

Campos:
- `id`: chave primária autoincrement.
- `conta_id`: conta mapeada.
- `tipo`: tipo de demonstração.
- `categoria`: categoria dentro do relatório.
- `excluido_at`: exclusão lógica.

Uso: fornece classificação alternativa para relatórios mesmo quando o plano de contas não tem todos os campos preenchidos.

---

## Tabela: `usuarios`
Cadastro de usuários do sistema.

Campos:
- `id`: chave primária textual.
- `nome`, `email`, `password_hash`: informações de login.
- `is_active`: usuário ativo/inativo.
- `last_login_at`, `created_at`: auditoria.

Uso: controle de acesso e autenticação.

---

## Tabela: `audit_logs`
Registra auditoria de ações no sistema.

Campos:
- `id`: chave primária textual.
- `company_id`: empresa afetada.
- `user_id`: usuário que executou a ação.
- `entity_name`, `entity_id`: entidade alterada.
- `action`: tipo de ação.
- `old_data`, `new_data`: estado antes e depois.
- `created_at`: momento da ação.

Uso: histórico de alterações para auditoria e rastreabilidade.


---

## Tabela: `assinaturas_digitais`
Guarda assinaturas eletrônicas de arquivos ECD.

Campos:
- `id`: chave primária textual.
- `ecd_file_id`: referência a `ecd_files(id)` no script, mas a tabela real é `ecd_arquivos`.
- `signed_by`: usuário assinante.
- `certificate_id`: referência a `digital_certificates(id)` no script, mas a tabela real é `certificados_digitais`.
- `signature_hash`: hash da assinatura.
- `signed_at`: data da assinatura.

Uso: registro de assinatura digital de arquivos.

---

## Tabela: `certificados_digitais`
Armazena certificados digitais usados por empresa.

Campos:
- `id`: chave primária textual.
- `empresa_id`: empresa dona do certificado.
- `certificate_name`, `serial_number`, `issuer`: dados do certificado.
- `valid_from`, `valid_until`: validade.
- `encrypted_pfx`: certificado criptografado.
- `created_at`: auditoria.

Uso: suporte a assinaturas digitais e certificação fiscal.

---

## Tabela: `sped_entregas`
Registra entregas de SPED.

Campos:
- `id`: chave primária textual.
- `empresa_id`: empresa da entrega.
- `sped_type`: tipo de SPED.
- `fiscal_year`: ano fiscal.
- `protocol`, `receipt_number`: comprovantes de entrega.
- `delivered_at`: data de entrega.
- `status`: situação da entrega.

Uso: acompanhamento de envios de SPED.

---

## Tabela: `sped_mappings`
Mapeia contas do plano de contas para códigos SPED.

Campos:
- `id`: chave primária textual.
- `conta_id`: conta associada.
- `sped_code`: código SPED.
- `description`: descrição do mapeamento.

Uso: vincula contas internas aos códigos do SPED para exportação fiscal.

---

## Tabela: `ecd_arquivos`
Armazena arquivos ECD gerados.

Campos:
- `id`: chave primária textual.
- `empresa_id`: empresa associada.
- `fiscal_year`: ano fiscal.
- `file_name`, `file_hash`: metadados do arquivo.
- `generated_by`: usuário gerador.
- `generated_at`, `signed_at`, `delivered_at`: datas do ciclo.
- `status`: status do arquivo.

Uso: controla geração e entrega de arquivos ECD.

---

## Tabela: `jobs`
Fila de jobs assíncronos.

Campos:
- `id`: chave primária textual.
- `queue_name`: nome da fila.
- `payload`: dados do job.
- `status`: estado do job.
- `retries`: número de tentativas.
- `created_at`: data de criação.
- `processed_at`: data de processamento.

Uso: tarefas em background, como geração de relatórios ou exportações.

