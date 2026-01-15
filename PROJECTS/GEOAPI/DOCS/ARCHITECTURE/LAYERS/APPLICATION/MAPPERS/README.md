# MAPPERS

Estratégias de mapeamento entre domain entities e DTOs do GEOAPI usando AutoMapper profiles ou métodos explícitos ToDto/FromDto para conversão bidirecional preservando encapsulamento. AutoMapper profiles centralizam configurações de mapeamento por feature (UnitsProfile, HoldersProfile, CommunitiesProfile) definindo transformações como ForMember para propriedades específicas, ProjectTo para projeções eficientes diretamente de IQueryable sem carregar entidades completas, e ReverseMap quando conversão inversa é simétrica. Métodos explícitos ToDto() em entities e FromDto() em DTOs fornecem controle total sobre conversão sendo preferíveis quando lógica é complexa ou assimétrica evitando magic do AutoMapper. Value objects mapeados via conversores customizados (CpfConverter transforma entre CPF value object e string, GeoPolygonConverter entre PostGIS geometry e GeoJSON). Mapeamento sempre unidirecional de entity para DTO na apresentação e de DTO para entity apenas em commands validados nunca expondo métodos públicos que permitam modificar entity via DTO diretamente.

## Arquivos Principais (a criar)

**AutoMapper Profiles:**
- 01-units-mapping-profile.md
- 02-holders-mapping-profile.md
- 03-communities-mapping-profile.md
- 04-teams-mapping-profile.md
- 05-legitimation-mapping-profile.md

**Custom Converters:**
- 06-cpf-converter.md
- 07-geo-polygon-converter.md
- 08-geo-point-converter.md
- 09-address-converter.md

**Explicit Mappers:**
- 10-unit-mapper.md - Métodos ToDto/FromDto explícitos
- 11-holder-mapper.md - Métodos ToDto/FromDto explícitos

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Incompleto
Descrição: Falta seção GENERATED com índice automático; Muitas listas com bullets (11) antes do rodapé - considerar converter para parágrafo denso.
