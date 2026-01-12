# DTOS

Data Transfer Objects do GEOAPI implementados como records imutáveis C# para transferência de dados entre camadas e contratos de API, organizados por feature (Units, Holders, Communities) com sufixos indicando propósito (CreateUnitDto para input, UnitDto para output, UnitSummaryDto para listagens). DTOs evitam expor entidades de domínio diretamente protegendo encapsulamento, permitem diferentes representações de mesma entidade para diferentes contextos (detalhes vs resumo vs formulário), e facilitam versionamento de API pois mudanças em domain não quebram contratos públicos. Input DTOs contêm apenas dados necessários para operação validados por FluentValidation, output DTOs projetam entidades de domínio em formato otimizado para apresentação incluindo dados relacionados já carregados, e DTOs podem ter propriedades extras como links HATEOAS, metadados de paginação ou campos calculados não presentes em domain. Mapeamento entre entities e DTOs feito via AutoMapper profiles ou métodos explícitos ToDto/FromDto garantindo separação clara de responsabilidades.

## Arquivos Principais (a criar)

**Units DTOs:**
- 01-unit-dto.md - Output completo de unidade
- 02-unit-summary-dto.md - Resumo para listagens
- 03-create-unit-dto.md - Input para criação
- 04-update-unit-dto.md - Input para atualização

**Holders DTOs:**
- 05-holder-dto.md - Output completo de titular
- 06-holder-summary-dto.md - Resumo para listagens
- 07-create-holder-dto.md - Input para criação
- 08-update-holder-dto.md - Input para atualização

**Communities DTOs:**
- 09-community-dto.md - Output completo de comunidade
- 10-community-summary-dto.md - Resumo para listagens
- 11-create-community-dto.md - Input para criação

**Teams DTOs:**
- 12-team-dto.md - Output completo de equipe
- 13-team-member-dto.md - Output de membro
- 14-create-team-dto.md - Input para criação

**Legitimation DTOs:**
- 15-legitimation-request-dto.md - Output de solicitação
- 16-create-legitimation-request-dto.md - Input para criação
- 17-legitimation-certificate-dto.md - Output de certidão

**Common DTOs:**
- 18-address-dto.md - Endereço completo
- 19-geo-point-dto.md - Coordenada geográfica
- 20-paged-result-dto.md - Resultado paginado

---

**Última atualização:** 2026-01-12
