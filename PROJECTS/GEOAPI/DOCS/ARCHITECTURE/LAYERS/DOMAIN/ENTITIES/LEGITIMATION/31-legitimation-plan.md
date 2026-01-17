# LegitimationPlan

Entidade representando planta legitimação fundiária desenho técnico cartográfico plotando graficamente Unit vértices medidas confrontações norte geográfico escala convenções ABNT elaborada Surveyor documento visual complementar DescriptiveMemorial visualização espacial registro processos. Herda de BaseEntity fornecendo auditoria temporal. Campos principais incluem UnitId Guid FK unidade representada, MemorialId Guid FK memorial correspondente Vertices fonte coordenadas, CertificateId Guid nullable FK LegitimationCertificate se gerada junto, SurveyorId Guid FK responsável técnico e PlanNumber string único (PLANT-2025-00098).

Campos formato incluem Format string papel (A4 A3 A2 A1 A0), Scale string cartográfica (1:500 1:1000 1:2000) relação papel terreno e Layout JSON nullable posicionamento elementos legenda norte escala carimbo. Campos armazenamento DwgPath string nullable S3 AutoCAD layers editável, PdfPath S3 PDF impressão, PngPath string nullable PNG preview 300dpi, GeneratedAt DateTime, GeneratedBy Guid FK Account e Observations string nullable.

Métodos incluem GenerateDwg() netDXF plotando polígono Vertices textos medidas azimutes confrontações norte escala carimbo layers organizados, GeneratePdf() convertendo ou gerando direto, GeneratePng() preview, CalculateScale() determinando adequado área Format e Validate() MemorialId existe Vertices válidos SurveyorId CREA. Regra negócio Memorial validado antes gerar, Scale adequado convenções cartográficas (100m² 1:200, 500m² 1:500, >500m² 1:1000+), Format comporta escala. Completa trio certidão+memorial+planta pacote documentação exportação PDF DWG PNG entrega cliente cartório.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
