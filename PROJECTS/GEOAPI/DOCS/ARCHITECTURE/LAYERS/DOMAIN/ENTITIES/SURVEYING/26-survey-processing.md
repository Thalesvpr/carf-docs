# SurveyProcessing

Entidade representando processamento dados GPS SurveyPoint usando estações RbmcStation como base correção diferencial transformando coordenadas brutas campo geodésicas precisas com cálculo precisões XYZ validação qualidade topográfica. Herda de BaseEntity fornecendo auditoria temporal. Campos principais incluem SurveyPointId Guid FK ponto processado, RbmcStation1Id Guid FK estação base primária, RbmcStation2Id Guid nullable FK secundária opcional múltiplas bases, SurveyorId Guid FK responsável técnico e ProcessedAt DateTime quando executado.

Campos técnicos incluem Software string (RTKLIB IBGE-PPP Leica Infinity), PrecisionX PrecisionY PrecisionZ decimais precisão metros (0.001-0.050 trabalhos topográficos), AntennaHeight decimal altura antena metros marco até centro fase e ProcessingNotes string nullable observações topógrafo. Campos storage RawFilePath ReportPath strings nullable caminhos S3 arquivo bruto RINEX UBX e relatório PDF processamento.

Métodos incluem CalculateAccuracy() precisão 3D combinada sqrt(X²+Y²+Z²) classificar qualidade, MeetsStandard(requiredAccuracyMeters) verificando padrão NBR 13133, ApplyToSurveyPoint() atualizando ProcessedLocation transitando Status PROCESSED e GetStationDistance() validando range estação. Regra negócio PrecisionXYZ menores 1.0m válido, AntennaHeight 0.5-3.0m. Integra SurveyPoint FK 1:N permitindo reprocessamentos, dispara SurveyPointProcessedEvent, participa validação DescriptiveMemorial apenas pontos precisão adequada e fornece rastreabilidade RawFilePath ReportPath auditoria futura.

---

**Última atualização:** 2026-01-12
