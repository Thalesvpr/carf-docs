# Legitimation Rules (Regras de Legitimação)

Regras de negócio específicas para processos de regularização fundiária urbana e rural (REURB) conforme Lei 13.465/2017 estabelecendo critérios de elegibilidade, requisitos documentais, limites de área, modalidades de atendimento e procedimentos legais que devem ser cumpridos para emissão de certidão de regularização fundiária garantindo conformidade com legislação brasileira e assegurando direitos dos beneficiários. Estas regras complementam regras de validação técnica definindo quando e como unidade habitacional pode ser legitimada considerando aspectos jurídicos sociais e econômicos do processo de regularização fundiária onde modalidade REURB-S (interesse social) atende população de baixa renda com isenção de custos e critérios simplificados enquanto REURB-E (interesse específico) atende demais casos com custos compartilhados e documentação adicional requerida. Regras estabelecem limites de área conforme modalidade, critérios de titularidade incluindo número máximo de titulares por unidade e percentuais de propriedade permitidos, requisitos documentais obrigatórios por modalidade especificando documentos pessoais comprovantes de ocupação e documentos técnicos necessários, e base legal da Lei 13.465/2017 detalhando prazos procedimentos e direitos dos beneficiários durante processo de legitimação. Aplicação destas regras garante que processos de legitimação cumprem requisitos legais minimizando risco de contestações judiciais ou invalidação de certidões emitidas protegendo tanto beneficiários quanto órgão público responsável pela regularização.

## Regras Documentadas

### Modalidades REURB
- **[reurb-s-requirements.md](./reurb-s-requirements.md)** - Requisitos REURB-S (interesse social): área ≤250m², renda ≤3 SM, isenção total custos, procedimentos simplificados
- **[reurb-e-requirements.md](./reurb-e-requirements.md)** - Requisitos REURB-E (interesse específico): área 250-500m², sem limite renda, custos progressivos, documentação técnica robusta

### Critérios e Requisitos
- **[ownership-criteria.md](./ownership-criteria.md)** - Critérios de titularidade: titular primário + máximo 3 co-titulares, percentuais de propriedade somam 100%, posse qualificada 5 anos
- **[documentation-requirements.md](./documentation-requirements.md)** - Requisitos documentais por modalidade: docs pessoais, comprovantes ocupação, docs técnicos, certidões obrigatórias
- **[contestation-rules.md](./contestation-rules.md)** - Regras de contestações administrativas (período 30 dias, legitimidade, análise, decisão, recursos)

### Base Legal
- **[lei-13465-2017.md](./lei-13465-2017.md)** - Lei Federal 13.465/2017: prazos 120 dias, legitimação fundiária, direitos beneficiários, vedações

**Relacionamento com Domain Model:**
- Aplica-se a: `DOMAIN-MODEL/AGGREGATES/03-legitimation-request-aggregate.md`
- Valida: `DOMAIN-MODEL/ENTITIES/25-legitimation-request.md`
- Eventos afetados: `DOMAIN-MODEL/EVENTS/12-request-submitted-event.md` a `19-correction-requested-event.md`

**Implementações por projeto:**
- Backend .NET: (caminho de implementação)
- Frontend React: (caminho de implementação)
- Mobile React Native: (caminho de implementação)

---

**Última atualização:** 2025-01-06
