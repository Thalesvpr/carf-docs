# BUSINESS

Validações de regras de negócio do CARF. age-validation.md titular deve ter >= 18 anos calculado birth_date vs today. email-validation.md formato RFC 5322 regex, domain MX record check opcional. phone-validation.md formato brasileiro (XX) XXXXX-XXXX ou (XX) XXXX-XXXX, DDD válido (11-99). unit-status-transitions.md valida transições Rascunho→Pendente (requer titular principal), Pendente→Em Análise (requer role Técnico), Em Análise→Aprovado/Rejeitado (requer role Fiscal). holder-uniqueness.md CPF único por tenant, email único. community-constraints.md unidade pertence apenas 1 community ativa. Validações estruturais em camada de aplicação coordinando múltiplas rules.

---

**Última atualização:** 2025-01-05
