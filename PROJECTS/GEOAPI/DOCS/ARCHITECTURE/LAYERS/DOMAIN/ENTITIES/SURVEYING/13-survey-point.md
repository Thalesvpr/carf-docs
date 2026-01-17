# SurveyPoint

Entidade representando ponto topográfico coletado campo via receptor GNSS com workflow desde coordenadas brutas até aprovação final uso memoriais descritivos rastreando processamento validação técnica. Herda de BaseEntity fornecendo auditoria soft delete. Campos principais incluem CommunityId Guid FK Community contextualizando geograficamente, Code string único comunidade (PC-001 MARCO-A), Name string descrição, GeoPoint Location coordenadas brutas GPS, ProcessedLocation GeoPoint nullable corrigidas após processamento e Altitude decimal nullable metros.

Campos controle incluem PointType (MARCO PIQUETE NATURAL) determinando precisão requerida necessidade monografia e PointStatus (COLLECTED PROCESSED APPROVED REJECTED) controlando workflow. Relacionamentos incluem Community localização, SurveyProcessing detalhando correção diferencial e Monograph se Type MARCO documentando acesso fotos.

Métodos incluem Process(surveyProcessingId processedCoordinates) atualizando ProcessedLocation Status PROCESSED, Approve(accountId) validando precisão mudando APPROVED disparando SurveyPointApprovedEvent, Reject(accountId reason) marcando recoleta e CanUseInDocuments() verificando APPROVED. Validações garantem Code único Community, MARCO requer Monograph antes aprovação e precisão SurveyProcessing atende requisito mínimo Type MinimumPrecision().

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
