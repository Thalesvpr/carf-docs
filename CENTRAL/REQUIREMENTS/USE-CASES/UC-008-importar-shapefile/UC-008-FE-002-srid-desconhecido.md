---
modules: [GEOWEB, REURBCAD, GEOGIS]
epic: scalability
---

# UC-008-FE-002: SRID Desconhecido

Fluxo de exceção do UC-008 Importar Shapefile ocorrendo no passo 10.3 durante reprojeção quando worker tenta detectar sistema de coordenadas original do Shapefile para converter geometrias para EPSG:4326 padrão de armazenamento mas não consegue identificar SRID por uma das condições: arquivo .prj ausente do ZIP (componente opcional contendo definição WKT da projeção não incluído no upload), .prj presente mas vazio ou corrompido com conteúdo inválido não parseável como WKT, .prj contém WKT com AUTHORITY desconhecido não presente em tabela spatial_ref_sys do PostGIS (projeção customizada local ou datum muito específico), ou .prj usa sintaxe WKT antiga incompatível com parser moderno esperando WKT2 especificação ISO 19162, sistema tenta parser usando biblioteca proj4js ou similar detectando falha ao converter WKT para código EPSG retornando null ou exception, ao invés de abortar importação completa falhando job e perdendo trabalho de upload e mapeamento já realizado, sistema implementa fallback strategy assumindo SRID padrão EPSG:4326 WGS84 usado por GPS e web mapping tratando coordenadas do Shapefile como já estando em lat/lon sem reprojetar aplicando ST_SetSRID(geometry, 4326) ao invés de ST_Transform preservando valores numéricos originais apenas atribuindo metadado de projeção, adiciona warning em import_errors table com severity=WARNING ao invés de ERROR registrando "SRID não identificado. Assumido EPSG:4326. Verifique se geometrias estão corretas no mapa" orientando usuário sobre decisão tomada, worker continua processamento normalmente criando unidades com geometrias preservadas, ao concluir job notificação exibe ícone amarelo warning mensagem "Importação concluída com ressalvas: Sistema de coordenadas não identificado. Verifique se geometrias aparecem corretamente no mapa" com link Ver no Mapa abrindo visualização das unidades importadas permitindo inspeção visual, se geometrias aparecem em localização incorreta (ex: valores UTM interpretados como lat/lon resultando em coordenadas absurdas fora do Brasil ou oceano) usuário pode deletar importação usando ação Reverter Importação disponível em relatório que executa DELETE FROM units WHERE import_job_id = $id desfazendo criações em lote, corrigir Shapefile adicionando .prj correto exportando novamente de QGIS com opção Save CRS to file marcada, e reimportar garantindo reprojeção adequada, caso comum em levantamentos de campo usando GPS que já grava em WGS84 onde assumir EPSG:4326 é correto e sistema funciona perfeitamente, ou Shapefiles baixados de fontes governamentais brasileiras tipicamente em SIRGAS 2000 UTM onde falta de .prj causa posicionamento incorreto exigindo correção manual.

**Ponto de Desvio:** Passo 10.3 do UC-008 (falha ao detectar SRID)

**Retorno:** EPSG:4326 assumido, geometrias preservadas sem reprojeção, warning registrado

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
