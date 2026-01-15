# Plot

Entidade representando lote terreno individual subdivisão Block estabelecendo parcela cadastral que pode ou não estar vinculada Unit permitindo flexibilidade áreas parcelamento definido mas ocupação irregular. Herda de BaseEntity fornecendo auditoria soft delete. Campos principais incluem BlockId Guid FK estabelecendo hierarquia, Code string único dentro quadra (LT-01 LOTE-15), GeoPolygon nullable delimitando perímetro, Area decimal nullable m² e FrontLength Depth decimais nullable testada profundidade metros.

Campo Confrontations string nullable JSON texto descrevendo confrontantes cada divisa (Frente Rua A, Fundos Lote 02, Laterais). Relacionamentos incluem Block pai e Unit nullable vinculada quando ocupação edificada existe. Métodos incluem CalculateDimensions() calculando Area FrontLength Depth PostGIS análise espacial, LinkUnit(unitId) vinculando validando geometry Unit contida Plot, UnlinkUnit() removendo vínculo e GetConfrontationsFromGeometry() gerando confrontações automaticamente ST_Touches Plots vizinhos.

Permite Plot sem Unit representando lote vago não cadastrado e Unit sem PlotId áreas informais sem parcelamento definido suportando realidade mista assentamentos onde parte tem organização cadastral formal parte ocupação irregular sem subdivisão lotes.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
