# REURB-S Requirements (Requisitos REURB Interesse Social)

Requisitos de elegibilidade para modalidade REURB-S (Regularização Fundiária Urbana de Interesse Social) conforme Lei 13.465/2017 destinada exclusivamente a população de baixa renda ocupante de núcleos urbanos informais consolidados estabelecendo critérios socioeconômicos territoriais e documentais que devem ser cumpridos para enquadramento nesta modalidade que garante isenção de custos cartoários e registrais além de procedimentos simplificados facilitando acesso à titularidade formal da propriedade. Critério de área estabelece limite máximo de 250 metros quadrados por unidade habitacional medidos considerando geometria espacial delimitada em planta técnica excluindo áreas comuns compartilhadas onde unidades que excedem este limite devem ser enquadradas em REURB-E mesmo que beneficiário atenda demais critérios sociais, permitindo exceções apenas em situações especiais justificadas por características geográficas específicas ou consolidação urbana que impossibilite redimensionamento sem comprometer moradia existente. Critério de renda familiar estabelece limite de até 3 salários mínimos nacionais vigentes calculados somando rendimentos de todos moradores do núcleo familiar que compartilham despesas domésticas comprovados mediante declaração de renda com responsabilidade criminal por informações falsas dispensando comprovação documental para facilitar acesso de população informal mas permitindo verificação amostral posterior, onde beneficiários que excedem limite de renda mas possuem renda familiar de até 5 salários mínimos podem ser enquadrados em REURB-E com custos subsidiados parcialmente. Critério de uso do imóvel estabelece que unidade deve ser destinada exclusivamente à moradia do beneficiário e família não sendo permitido uso comercial industrial ou misto exceto pequeno comércio familiar integrado à residência que não descaracterize função habitacional principal, comprovado mediante visita técnica de campo registrando fotos internas e externas e atestando ocupação efetiva da família. Critério de tempo de ocupação estabelece mínimo de 5 anos ininterruptos de posse mansa e pacífica sobre o imóvel contados retroativamente a partir da data de solicitação de regularização comprovados mediante documentos indiretos como contas de serviços públicos em nome do ocupante declarações de vizinhos fotografias datadas ou quaisquer evidências que demonstrem antiguidade da ocupação, dispensando comprovação formal de propriedade ou contrato de aluguel que normalmente população de baixa renda não possui. Critério de ausência de outra propriedade estabelece que beneficiário e cônjuge não podem ser proprietários de outro imóvel urbano ou rural em qualquer localidade do território nacional verificado mediante certidão negativa de propriedade emitida por cartório de registro de imóveis competente, exceto se propriedade anterior foi perdida por força maior como desastre natural ou desapropriação sem indenização justa, garantindo que benefício de regularização gratuita é destinado apenas a quem efetivamente necessita e não possui alternativa habitacional. Benefícios específicos de REURB-S incluem isenção total de custos de escritura registro cartorial emolumentos e taxas municipais relacionadas ao processo de regularização fundiária reduzindo barreira financeira que historicamente impediu população de baixa renda de acessar titularidade formal, procedimentos documentais simplificados aceitando declarações e documentos indiretos ao invés de comprovações formais que população vulnerável dificilmente possui, priorização no atendimento e processamento de solicitações REURB-S sobre REURB-E garantindo que casos sociais sejam resolvidos primeiro, e assistência técnica jurídica e social gratuita fornecida pelo poder público municipal ou estadual para auxiliar beneficiários em todas etapas do processo desde cadastramento inicial até emissão final de certidão de regularização.

**Critérios de elegibilidade REURB-S:**
- Área máxima: 250m² por unidade habitacional
- Renda familiar: até 3 salários mínimos
- Uso do imóvel: moradia exclusiva (pequeno comércio familiar permitido)
- Tempo de ocupação: mínimo 5 anos ininterruptos
- Ausência de propriedade: sem outro imóvel urbano/rural

**Benefícios REURB-S:**
- Isenção total de custos (escritura, registro, emolumentos, taxas)
- Procedimentos documentais simplificados
- Priorização no atendimento
- Assistência técnica jurídica e social gratuita

**Relacionamento com Domain Model:**
- Valida: `DOMAIN-MODEL/ENTITIES/25-legitimation-request.md` (campo modality = REURB_S)
- Valida: `DOMAIN-MODEL/ENTITIES/01-unit.md` (campo area_sqm ≤ 250)
- Valida: `DOMAIN-MODEL/ENTITIES/02-holder.md` (renda familiar)

**Implementações por projeto:**
- Backend .NET: (caminho de implementação)
- Frontend React: (caminho de implementação)
- Mobile React Native: (caminho de implementação)

---

**Última atualização:** 2025-01-06
**Status do arquivo**: Review
