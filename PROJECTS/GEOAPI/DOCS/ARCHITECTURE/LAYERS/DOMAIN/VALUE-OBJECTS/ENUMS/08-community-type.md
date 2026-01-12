# CommunityType

Value object enum representando tipo de comunidade ou assentamento conforme classificação da Lei 13.465/2017 de regularização fundiária, determinando legislação aplicável, requisitos documentais e processos específicos para cada contexto. Valores possíveis são URBANA (núcleo urbano informal aplicando REURB-S social ou REURB-E empresarial), RURAL (assentamento em zona rural seguindo regulamentação INCRA), QUILOMBOLA (comunidade quilombola com titulação coletiva conforme Decreto 4887/2003) e RIBEIRINHA (comunidade tradicional às margens de rios com particularidades de ocupação sazonal).

Métodos incluem IsUrban() verificando se é tipo urbano, RequiresEnvironmentalLicense() determinando necessidade de licenciamento ambiental, AllowsCollectiveTitling() verificando se permite titulação coletiva (apenas QUILOMBOLA), e GetApplicableLegislation() retornando lista de normas legais relevantes para o tipo.

Usado em Community.Type para definir regras de validação específicas (ex: QUILOMBOLA requer certidão da Fundação Palmares), determinar campos obrigatórios em formulários de cadastro, filtrar relatórios por tipo de regularização, e gerar documentação conforme legislação aplicável, garantindo que processos sigam marcos legais corretos para cada contexto territorial.

---

**Última atualização:** 2026-01-12
