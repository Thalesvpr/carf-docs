# Surveyor

Entidade representando profissional topógrafo engenheiro agrimensor responsável técnico levantamentos geodésicos processamento dados GPS assinatura memoriais descritivos plantas. Herda de BaseEntity fornecendo auditoria soft delete. Campos principais incluem AccountId Guid nullable FK Account se topógrafo também usuário sistema, Name string nome completo assinatura, CREA registro profissional obrigatório (CREA/RJ 12345-6), Specialty string nullable especialidade, Email contato e PhoneNumber telefone profissional.

Campos controle incluem IsActive bool controlando pode assinar novos documentos. Relacionamentos incluem SurveyProcessing responsável técnico processando GPS estações RbmcStation, DescriptiveMemorial assinando memoriais ART e LegitimationPlan assinando plantas legitimação.

Métodos incluem Activate()/Deactivate() controlando IsActive impedindo assinatura novos documentos mas preservando histórico, CanSignDocuments() verificando IsActive CREA válido e GetActiveDocuments() listando memoriais plantas pendentes. Validações garantem CREA único tenant, Name CREA obrigatórios assinatura digital e IsActive false não permite novos SurveyProcessing mas não invalida processamentos anteriores mantendo integridade documentos emitidos.

---

**Última atualização:** 2026-01-12
