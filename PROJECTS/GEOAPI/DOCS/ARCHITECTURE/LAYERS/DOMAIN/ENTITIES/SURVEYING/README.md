# SURVEYING

Entities topografia levantamento campo do GEOAPI gerenciando coleta processamento dados geodésicos GNSS para geração coordenadas precisas Units. Surveyor representa topógrafo profissional responsável levantamento com Name CPF CREA value object validando registro profissional CAU licença ativa e Equipment lista receptores GNSS utilizados rastreabilidade calibração. RbmcStation registra estações IBGE Rede Brasileira Monitoramento Contínuo fornecendo correção diferencial pós-processamento com StationCode identificador IBGE, Location GeoPoint coordenadas oficiais precisas e RinexUrl endpoint download arquivos observação RINEX formato padrão. SurveyPoint representa ponto coletado campo com PointType enum (BOUNDARY/CORNER/REFERENCE) classificando, RawCoordinates GeoPoint capturadas receptor, ProcessedCoordinates GeoPoint após correção diferencial RBMC, Accuracy metros HDOP horizontal dilution precision indicando confiabilidade, Timestamp UTC coleta e SurveyorId rastreando responsável. SurveyProcessing documenta job pós-processamento com InputPoints collection SurveyPoints raw, RbmcStationId base utilizada correção, ProcessingMethod enum (RTK/PPK/DGPS), OutputGeometry GeoPolygon resultante após ajuste rede e QualityMetrics JSON contendo RMS residuals fechamento linear angular compliance NBR 13133. Monograph entity armazena monografia marco geodésico com Description localização, Coordinates precisas, Photos croqui acesso e InstallationDate rastreando implantação RN reference network controle qualidade futuras medições garantindo repeatability surveys independentes.

## Arquivos

- **[12-surveyor.md](./12-surveyor.md)** - Topógrafo profissional responsável levantamento
- **[13-survey-point.md](./13-survey-point.md)** - Ponto geodésico coletado campo GNSS
- **[25-rbmc-station.md](./25-rbmc-station.md)** - Estação IBGE RBMC correção diferencial
- **[26-survey-processing.md](./26-survey-processing.md)** - Job pós-processamento GNSS PPK
- **[27-monograph.md](./27-monograph.md)** - Monografia marco geodésico implantado

---

**Última atualização:** 2026-01-12
