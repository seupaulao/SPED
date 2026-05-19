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

## Tabela: `report_types`
Define tipos de demonstração ou relatórios financeiros suportados.

Campos:
- `id`: identificador textual único.
- `code`: código único curto (`BALANCO`, `DRE`, `DFC`, `DVA`, `BALANCETE`).
- `name`: nome legível do relatório.

Uso: serve para tipar templates, versões de relatórios e permitir flexibilidade de relatórios.

---

## Tabela: `plano_contas_referencial`
Armazena uma tabela de contas referencial, que pode ser usada como modelo ou catálogo de contas padrão.

Campos:
- `id`: chave primária textual.
- `parent_id`: relação hierárquica autoreferenciada.
- `codigo`, `nome`: dados da conta referencial.
- `tipo_conta`, `level`, `aceita_entrada`, `is_ativo`: atributos do referencial.
- `tipo`, `natureza`, `nivel`, `grupo`, `dre_grupo`, `fluxo_caixa_tipo`: classificação contábil.
- `created_at`, `excluded_at`: auditoria e exclusão lógica.

Uso: refere-se a base de contas que pode ser reutilizada na criação de planos de contas de empresas.

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

## Tabela: `centro_custo`
Registra centros de custo vinculados a uma empresa.

Campos:
- `id`: chave primária textual.
- `empresa_id`: referência à empresa.
- `codigo`, `nome`: identificação do centro de custo.
- `created_at`: auditoria.

Uso: permite classificar lançamentos por centro de custo em cada empresa.

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

## Tabela: `report_templates`
Define templates de relatórios configuráveis.

Campos:
- `id`: chave primária textual.
- `empresa_id`: empresa associada (observação: o FK aponta para `empresas(id)` mas a tabela definida no script é `empresa`).
- `report_type_id`: tipo de relatório.
- `name`: nome do template.
- `is_default`: flag de template padrão.
- `created_at`: auditoria.

Uso: modela relatórios reutilizáveis por empresa e tipo.

---

## Tabela: `report_template_lines`
Linhas de um template de relatório.

Campos:
- `id`: chave primária textual.
- `template_id`: referência ao template.
- `parent_id`: permite hierarquia de linhas.
- `line_order`: ordem da linha.
- `code`, `title`, `line_type`: identificação da linha.
- `formula`: fórmula opcional para cálculo.
- `is_bold`: estilo de apresentação.
- `created_at`: auditoria.

Uso: estrutura as linhas do relatório, permitindo seções, subtítulos e cálculos.

---

## Tabela: `report_line_accounts`
Associa contas a linhas de relatório.

Campos:
- `id`: chave primária textual.
- `report_line_id`: linha de template.
- `conta_id`: conta do plano de contas.

Uso: define quais contas entram em cada linha de relatório.

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

## Tabela: `tags`
Armazena tags para classificação adicional.

Campos:
- `id`: chave primária textual.
- `empresa_id`: referência à empresa (`empresas(id)` no script).
- `name`: nome da tag.

Uso: rotular lançamentos ou linhas com etiquetas livres.

---

## Tabela: `lancamento_item_tags`
Tabela de relacionamento many-to-many entre linhas e tags.

Campos:
- `lancamento_item_id`: referência a uma linha de lançamento (`lancamento_item(id)`),
- `tag_id`: referência a `tags(id)`.
- chave primária composta em `(lancamento_item_id, tag_id)`.

Uso: permite atribuir várias tags a cada linha.

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

## Tabela: `usuarios`
Cadastro de usuários do sistema.

Campos:
- `id`: chave primária textual.
- `nome`, `email`, `password_hash`: informações de login.
- `is_active`: usuário ativo/inativo.
- `last_login_at`, `created_at`: auditoria.

Uso: controle de acesso e autenticação.

---

## Tabela: `regras`
Define papéis de usuário.

Campos:
- `id`: chave primária textual.
- `code`: código único do papel.
- `name`: nome legível.

Uso: classifica usuários em perfis como `SUPER_ADMIN`, `ACCOUNTANT`, `ASSISTANT`, `AUDITOR`, `CLIENT`.

---

## Tabela: `permissoes`
Define permissões do sistema.

Campos:
- `id`: chave primária textual.
- `code`: código único da permissão.
- `descricao`: descrição legível.

Uso: lista de ações autorizáveis.

---

## Tabela: `regra_permissao`
Relaciona papéis a permissões.

Campos:
- `role_id`: referência a `regras(id)`.
- `permission_id`: referência a `permissoes(id)`.
- chave primária composta.

Uso: define quais permissões cada papel possui.

---

## Tabela: `empresa_usuario`
Associa usuários a empresas com um papel.

Campos:
- `user_id`: referência a `usuarios(id)`.
- `company_id`: referência a `empresa(id)`.
- `role_id`: papel do usuário.
- chave primária composta.

Uso: modela multiempresa e papéis por empresa.

---

## Tabela: `usuario_sessoes`
Rastrea sessões de usuário.

Campos:
- `id`: chave primária textual.
- `user_id`: usuário da sessão.
- `token`: token único de sessão.
- `ip_address`, `user_agent`: contexto da sessão.
- `expires_at`: expiração da sessão.
- `revoked`: flag de revogação.
- `created_at`: auditoria.

Uso: gerenciar autenticação e sessões ativas.

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

## Tabela: `sped_natureza`
Define a natureza fiscal de contas SPED.

Campos:
- `id`: chave primária textual.
- `code`: código único (`01` a `06`).
- `description`: descrição da natureza.

Uso: classificar contas por natureza no SPED.

---

## Tabela: `report_versions`
Registra versões geradas de relatórios.

Campos:
- `id`: chave primária textual.
- `empresa_id`: empresa geradora.
- `report_template_id`: template usado.
- `report_type_id`: tipo de relatório.
- `version_number`: número da versão.
- `fiscal_year`, `start_period`, `end_period`: período fiscal.
- `generated_by`: usuário gerador (`users(id)` no script, mas a tabela é `usuarios`).
- `is_locked`: bloqueio da versão.
- `notes`: observações.
- `created_at`: auditoria.

Uso: histórico de relatórios gerados e versões fechadas.

---

## Tabela: `report_version_lines`
Armazena linhas de uma versão de relatório.

Campos:
- `id`: chave primária textual.
- `report_version_id`: referência à versão.
- `line_order`, `code`, `title`: definição da linha.
- `amount`: valor calculado.
- `created_at`: auditoria.

Uso: guarda o resultado final de cada linha de relatório gerado.

---

## Tabela: `trava_contabil`
Representa o fechamento contábil de períodos.

Campos:
- `id`: chave primária textual.
- `empresa_id`: empresa afetada.
- `year`, `month`: período fechado.
- `is_closed`: flag de fechamento.
- `closed_by`: usuário que fechou.
- `closed_at`: data do fechamento.

Uso: controle de travamento de períodos contábeis.

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

---

## Visões

### `user_permissions_view`
View que junta `empresa_usuario`, `regra_permissao` e `permissoes` para expor as permissões de cada usuário por empresa.

### `trial_balance_view`
View que tenta agregar débitos e créditos por conta, mas referencia colunas `a.code` e `a.name` que não existem em `plano_contas` no script atual.

---

## Tabela: `empresa_configuracao`
Configuração específica por empresa.

Campos:
- `empresa_id`: chave primária e referência a `companies(id)` no script, novamente inconsistente com a tabela `empresa`.
- `permitir_dinheiro_negativo`: flag de limite de caixa.
- `periodo_fechamento_automatico`: fechamento automático.
- `default_report_template`: template de relatório padrão.
- `created_at`: auditoria.

Uso: mantém preferências e configurações por empresa.

---

## Observações gerais

- O script é uma conversão de PostgreSQL para SQLite e contém várias referências de FK que não foram ajustadas para os nomes de tabelas presentes (`empresas` vs `empresa`, `companies` vs `empresa`, `users` vs `usuarios`, `ecd_files` vs `ecd_arquivos`, `digital_certificates` vs `certificados_digitais`, `journal_entry_lines` ausente).
- Algumas views também fazem referência a colunas ou tabelas inexistentes no esquema atual.
- A estrutura central de contabilidade está presente: empresas, plano de contas, lançamentos, itens, mapas de demonstrativos e relatórios.
- A parte de usuário/permissão e auditoria também está modelada, embora precise de correções de nome de tabela para funcionar sem erros.
