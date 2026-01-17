# RbmcStation

Entidade representando estação Rede Brasileira Monitoramento Contínuo GNSS operada IBGE fornecendo dados correção diferencial processamento pontos topográficos coletados campo elevando precisão GPS comum nível geodésico. Herda de BaseEntity fornecendo auditoria temporal. Campos principais incluem Code string código oficial IBGE 4 caracteres (RIOD PARA RECF) único nacionalmente, Name string nome completo estação, GeoPoint Location coordenadas geodésicas precisas antena precisão milimétrica e Altitude decimal ortométrica metros nível mar.

Campos controle incluem IsActive bool estação operacional recebendo dados continuamente, Region string nullable região geográfica (Sudeste Norte) busca e DataUrl string nullable URL download arquivos RINEX FTP IBGE. Métodos incluem CalculateDistance(GeoPoint targetPoint) distância geodésica km escolher estação mais próxima, IsWithinRange(point maxDistanceKm) verificando raio aceitável 100km PPP 30km RTK, GetRinexUrl(DateTime date) construindo URL RINEX data específica e FindNearestStations(point count) estático retornando N estações mais próximas ordenadas.

Regra negócio processamento SurveyPoint deve usar RBMC dentro raio adequado preferindo mais próxima ativa. Integra SurveyProcessing através FKs RbmcStation1Id RbmcStation2Id permitindo uma ou duas estações base, participa cálculo precisão distância afeta diretamente resultado, fornece dados RINEX software RTKLIB IBGE-PPP e suporta sincronização API oficial IBGE background job Hangfire atualizando estações ativas.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
