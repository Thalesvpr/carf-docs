---
modules: [GEOWEB, REURBCAD]
epic: units
---

# UC-005-FE-002: Erro de Validação no Servidor

Fluxo de exceção do UC-005 Sincronizar Dados Offline ocorrendo na fase PUSH quando servidor GEOAPI recebe dados do app mobile executa validações de regras de negócio (CPF válido usando algoritmo verificador de dígitos, geometria válida verificando ST_IsValid retornando true sem auto-interseções, percentuais de titulares somando ≤100% via aggregate SUM, área construída ≤ área terreno comparando numéricamente) e detecta violação retornando HTTP 400 Bad Request com response JSON contendo array errors estruturado com field indicando campo problemático, code identificando tipo de erro (INVALID_CPF INVALID_GEOMETRY PERCENTAGE_EXCEEDED REQUIRED_FIELD), e message descritiva em português "CPF 123.456.789-00 inválido. Verifique os dígitos", onde app recebe response 400 interrompe processamento do item atual mantendo needs_sync=true sem incrementar retry_count pois requer correção manual não automática, exibe modal vermelho erro com ícone de alerta título "Erro de Validação" listando todos erros retornados agrupados por unidade mostrando "Unidade #1234: CPF inválido (campo titular_cpf), Percentual excedido (soma 105%)" com botão Editar Agora abrindo formulário de edição da unidade problemática pré-carregando dados atuais e destacando campos com erro em vermelho com mensagens inline copiadas de errors[].message, FIELD_AGENT corrige valores inválidos editando CPF corrigindo dígitos ou ajustando percentuais reduzindo soma para ≤100%, salva alterações atualizando registro local em units_local mantendo needs_sync=true para retry, e clica Sincronizar novamente reenviando dados corrigidos onde servidor re-executa validações agora passando todas regras retornando HTTP 200 Success com server_id permitindo app marcar synced_at=NOW() e needs_sync=false finalizando, garantindo integridade de dados no servidor impedindo estados inconsistentes enquanto fornece feedback claro permitindo correção rápida em campo sem perder trabalho já realizado.

**Ponto de Desvio:** Fase PUSH do UC-005 (após servidor processar batch)

**Retorno:** Dados permanecem pendentes, FIELD_AGENT corrige e retenta sincronização

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
