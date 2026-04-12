---
type: leaf
status: approved
updated: 2026-01-25
---

# Business Validation

Validacoes de regras de negocio do CARF aplicadas em camada de aplicacao. Titular deve ter idade minima de 18 anos calculada comparando data de nascimento com data atual. Email segue formato RFC 5322 com validacao de regex e verificacao opcional de registro MX do dominio. Telefone segue formato brasileiro com DDD valido entre 11 e 99.

Transicoes de status de unidade seguem regras especificas. Rascunho para Pendente requer titular principal vinculado. Pendente para Em Analise requer papel de Analista. Em Analise para Aprovado ou Rejeitado requer papel de Gestor. CPF e email devem ser unicos por tenant prevenindo duplicacao de cadastros. Unidade pertence a apenas uma comunidade ativa.
