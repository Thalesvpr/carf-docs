# Block

Entidade representando quadra urbana subdivisão espacial Community organizando território áreas menores contendo múltiplos Plot facilitando referenciamento cartográfico cadastro sistemático áreas urbanizadas. Herda de BaseEntity fornecendo auditoria soft delete. Campos principais incluem CommunityId Guid FK estabelecendo hierarquia Community > Block > Plot > Unit, Code string identificador único dentro comunidade (QD-01 QUADRA-A), Name string nullable descritivo opcional, GeoPolygon nullable delimitando perímetro visualização cartográfica e Area decimal nullable m² calculada ou informada.

Relacionamentos incluem Community pai, coleção Plots filhos subdividindo quadra lotes individuais e Unit opcionalmente vinculadas diretamente quando BlockId desnormalizado preenchido queries eficientes. Métodos incluem AddPlot(code geometry) criando lote validando código único geometria dentro perímetro, CalculateArea() recalculando PostGIS ST_Area e ValidateGeometry() verificando Plots filhos contidos perímetro quadra.

Hierarquia espacial opcional permitindo Communities sem Blocks áreas rurais assentamentos informais não organizados quadras, mas quando presente facilita organização cadastral geração plantas por quadra relatórios agrupados subdivisão territorial seguindo lógica parcelamento urbano tradicional.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
