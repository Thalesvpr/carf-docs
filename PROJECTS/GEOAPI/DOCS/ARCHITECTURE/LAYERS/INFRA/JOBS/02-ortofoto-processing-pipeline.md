---
type: leaf
status: approved
updated: 2026-02-07
---

# Ortofoto Processing Pipeline

Pipeline de processamento assincrono de ortofotos georreferenciadas executado como job Hangfire na GEOAPI. Recebe arquivos GeoTIFF uploaded pelo analista, extrai metadados espaciais, gera versao otimizada para web e produz piramide de tiles no padrao XYZ para renderizacao em mapa. Todo o processamento acontece server-side sem intervencao do usuario apos o upload.

## Biblioteca de Processamento

GDAL via binding .NET MaxRev.Gdal.Core. Esta e a unica opcao madura para processamento de GeoTIFF em ambiente server .NET, oferecendo reprojecao entre sistemas de coordenadas, extracao de metadados espaciais (SRID, bounds, resolucao, bandas), geracao de tiles via gdal2tiles e conversao entre formatos raster. O pacote NuGet inclui os binarios nativos GDAL para Linux e Windows sem necessidade de instalacao separada.

## Fluxo do Job

O job Hangfire recebe o ortofoto_id como parametro unico. O processamento segue sete etapas sequenciais.

Primeira etapa: download do arquivo original. O job busca o registro da ortofoto no banco pelo ID, extrai o original_path e baixa o arquivo GeoTIFF do bucket S3 para um diretorio temporario no servidor. Se o download falhar, o job falha imediatamente e entra na politica de retry.

Segunda etapa: extracao de metadados via GDAL. Abre o arquivo com GdalDataset e extrai o SRID do sistema de coordenadas, os limites geograficos (bounding box) como quatro coordenadas, a resolucao em pixels (largura e altura), o numero de bandas espectrais e o tamanho do pixel em unidades do sistema de coordenadas. Esses metadados sao salvos nos campos width, height, srid e bounds_geojson do registro da ortofoto.

Terceira etapa: validacao de georreferenciamento. Verifica se o arquivo possui sistema de coordenadas definido. Arquivos sem georreferenciamento sao rejeitados: o job marca status como FAILED com mensagem "Arquivo sem sistema de coordenadas definido. Verifique o georreferenciamento no QGIS antes de fazer upload." e encerra.

Quarta etapa: geracao da versao otimizada para web. Converte o GeoTIFF para JPEG com quality 85, redimensionando proporcionalmente para que o lado maior nao exceda 4096 pixels. Essa versao serve para preview rapido no GEOWEB sem carregar o arquivo original completo.

Quinta etapa: geracao da piramide de tiles. Gera tiles no padrao XYZ para zoom levels de 12 a 20, cada tile com 256 por 256 pixels em formato PNG com transparencia. Os tiles seguem a convencao z/x/y.png onde z e o nivel de zoom, x a coluna e y a linha. Tiles em areas sem dados sao omitidos para economizar espaco.

Sexta etapa: upload para S3. Faz upload da versao otimizada e de todos os tiles para o bucket S3. Os caminhos seguem a estrutura: tenant_id/orthofotos/ortofoto_id/original.tif para o arquivo original ja existente, tenant_id/orthofotos/ortofoto_id/optimized.jpg para a versao web e tenant_id/orthofotos/ortofoto_id/tiles/z/x/y.png para cada tile.

Setima etapa: atualizacao do banco. Atualiza o registro da ortofoto com optimized_path, tiles_path, metadados extraidos (width, height, srid, bounds_geojson), processing_status como COMPLETED e processed_at com o timestamp atual.

## Politica de Retry

O job executa no maximo 3 tentativas com backoff exponencial: primeira retry apos 30 segundos, segunda apos 2 minutos, terceira apos 10 minutos. Timeout maximo de 30 minutos por execucao do job. Se todas as tentativas falharem, o status da ortofoto muda para FAILED, o campo processing_error e preenchido com a mensagem de erro da ultima tentativa e o uploader recebe notificacao via NotificationHub informando a falha.

## Monitoramento

Metricas Prometheus expostas pelo job: geoapi_ortofoto_processing_duration_seconds como histograma da duracao de processamento por ortofoto, geoapi_ortofoto_processing_success_total como contador de processamentos bem-sucedidos, geoapi_ortofoto_processing_failure_total como contador de falhas e geoapi_ortofoto_queue_depth como gauge da profundidade atual da fila de processamento. Alertas configurados para fila com mais de 10 itens pendentes e taxa de falha acima de 20 porcento.

## Limpeza

Arquivos temporarios no servidor sao deletados apos upload para S3 independente do resultado (sucesso ou falha). O diretorio temporario e isolado por job para evitar conflitos entre processamentos concorrentes.
