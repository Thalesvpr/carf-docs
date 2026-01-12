# BUSINESS-RULES

Business rules restrições validações políticas negócio governam comportamento sistema assegurando compliance legal integridade dados aderência processos estabelecidos através regras explícitas verificáveis rastreáveis organizadas três categorias principais VALIDATION-RULES garantindo integridade consistência dados entidades validando campos relacionamentos restrições antes persistência CPF CNPJ email telefone coordenadas geográficas polígonos executadas durante criação atualização entidades antes commit transacional validação múltiplas camadas client-side API database constraints WORKFLOW-RULES governando transições status através state machines definindo quais mudanças estado permitidas baseadas status atual role usuário pré-condições negócio unit-status-transitions seis estados DRAFT PENDING_ANALYSIS IN_REVIEW APPROVED REJECTED REQUIRES_CHANGES legitimation-status-transitions onze estados workflow conforme Lei 13465/2017 enforcement backend validando requisições mudança status verificando transição permitida role adequado pré-condições atendidas registrando AuditLog disparando eventos domínio LEGITIMATION-RULES estabelecendo requisitos diferenciados modalidade REURB-S interesse social baixa renda área menor igual duzentos cinquenta metros quadrados gratuito documentação simplificada REURB-E interesse específico área menor igual quinhentos metros quadrados taxa cobrada documentação completa licenças ambientais contestation-rules período trinta dias legitimidade análise decisão recursos validação durante workflow legitimação conforme modalidade selecionada verificando elegibilidade documentação obrigatória custos aplicáveis condicionantes impostas enforcement implementado múltiplas camadas client-side validação básica formato formulários feedback imediato usuário API Layer validação negócio antes processar requisição Domain Layer validação profunda acesso repositórios serviços regras complexas envolvendo múltiplas entidades Database Layer constraints triggers última linha defesa unicidade foreign keys check constraints auditoria violações registradas AuditLog.

## Categorias

- **[VALIDATION-RULES/](./VALIDATION-RULES/README.md)** - Validação dados CPF CNPJ email telefone coordenadas geometrias
- **[WORKFLOW-RULES/](./WORKFLOW-RULES/README.md)** - Transições status state machines unit legitimation permissions
- **[LEGITIMATION-RULES/](./LEGITIMATION-RULES/README.md)** - Regras específicas Lei 13465/2017 REURB-S REURB-E

---

**Última atualização:** 2026-01-11
