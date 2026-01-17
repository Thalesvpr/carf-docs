---
modules: [GEOWEB, REURBCAD, GEOGIS]
epic: scalability
---

# UC-007-FE-003: Erro de Reprojeção

Fluxo de exceção do UC-007 Exportar Dados Geográficos ocorrendo no passo 11.2 durante reprojeção de geometrias quando worker tenta converter coordenadas do SRID armazenado no banco (tipicamente EPSG:4326 WGS84 usado para armazenamento universal) para SRID alvo selecionado pelo usuário (ex: EPSG:31982 SIRGAS 2000 UTM 22S específico Brasil) usando função PostGIS ST_Transform(geometry, target_srid) mas operação falha lançando exceção tipicamente causada por SRID desconhecido não presente em tabela spatial_ref_sys do PostGIS (usuário selecionou EPSG customizado local não padrão), parâmetros de datum transformation ausentes para conversão específica entre datums incompatíveis, ou corrupção de metadados de projeção no banco após migração ou upgrade de PostGIS, sistema captura exceção PostgreSQL em bloco try-catch do worker logando erro completo com código SRID problemático e stack trace para investigação técnica posterior, ao invés de abortar job completamente sistema implementa fallback strategy mantendo SRID original das geometrias sem reprojetar usando ST_AsText(geometry) ou ST_AsGeoJSON(geometry) diretamente com coordenadas nativas do banco preservando dados geográficos válidos apenas em sistema de referência diferente do solicitado, adiciona campo extra no arquivo exportado se formato permitir (GeoJSON adiciona property original_srid:4326, Shapefile adiciona coluna ORIG_SRID no .dbf) documentando que reprojeção não foi aplicada permitindo usuário reprojetar manualmente em QGIS após importar usando ferramenta Reproject Layer, atualiza arquivo .prj do Shapefile ou crs do GeoJSON refletindo SRID real usado garantindo softwares GIS detectem corretamente sistema de coordenadas ao abrir arquivo evitando sobreposição incorreta com outras camadas, marca job como completed_with_warnings ao invés de failed pois exportação foi bem-sucedida apenas com limitação técnica, envia notificação ao usuário com ícone amarelo warning mensagem "Exportação concluída com ressalvas: Não foi possível reprojetar para EPSG:31982. Arquivo exportado em EPSG:4326 (original). Você pode reprojetar manualmente em seu software GIS" orientando sobre estado final e próximos passos opcionais, registra métrica de falha em dashboard de observabilidade alertando equipe técnica sobre problema recorrente que pode indicar necessidade de atualizar spatial_ref_sys com SRIDs faltantes executando script INSERT específico ou investigar configuração de PostGIS.

**Ponto de Desvio:** Passo 11.2 do UC-007 (conversão de SRID falha)

**Retorno:** SRID original mantido, arquivo gerado com warning, usuário notificado

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
