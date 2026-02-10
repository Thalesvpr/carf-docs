---
type: leaf
status: active
updated: 2026-02-07
---

# File Storage

A GEOAPI utiliza armazenamento compativel com S3 para persistir documentos e fotos. Em producao, conecta ao AWS S3 na regiao sa-east-1. Em desenvolvimento, utiliza MinIO com ForcePathStyle habilitado.

## Interface IFileStorage

| Metodo | Parametros | Retorno | Descricao |
|--------|-----------|---------|-----------|
| UploadAsync | stream, fileName, contentType, ct | string (key) | Faz upload do arquivo e retorna a chave gerada |
| DownloadAsync | key, ct | Stream | Baixa o arquivo pelo key |
| DeleteAsync | key, ct | void | Remove o arquivo |
| GetPresignedUrlAsync | key, expiration, ct | string (URL) | Gera URL temporaria com validade configuravel |

## Implementacao S3FileStorage

A classe S3FileStorage implementa IFileStorage utilizando o SDK da AWS. Cada upload adiciona o metadata "tenant-id" com o id do tenant atual para rastreabilidade. A chave do arquivo segue o formato "{tenantId}/{ano}/{mes}/{guid}.{extensao}", organizando os objetos em hierarquia por tenant e data.

## Configuracao

| Propriedade | Producao | Desenvolvimento |
|-------------|----------|-----------------|
| Provider | S3 | MinIO |
| BucketName | carf-documents | carf-documents |
| Region | sa-east-1 | - |
| Endpoint | https://s3.sa-east-1.amazonaws.com | http://localhost:9000 |

O cliente AmazonS3 e registrado como Singleton no DI. Quando o provider e MinIO, ForcePathStyle e habilitado para compatibilidade.

## Servico de Upload de Fotos

A classe PhotoService encapsula o upload de fotos de unidades com validacao de tipo e tamanho. Verifica se o content type esta na lista de tipos permitidos e se o tamanho nao excede o limite maximo. Gera um thumbnail via ImageProcessor e faz upload de ambos os arquivos (original e thumbnail com prefixo "thumb_"), retornando as duas chaves em um PhotoDto.

## Limites por Tipo de Arquivo

| Tipo | DocumentType | Max Tamanho | Content-Types Permitidos | Descricao |
|------|-------------|-------------|-------------------------|-----------|
| FOTO_FACHADA | FACADE_PHOTO | 10 MB | image/jpeg, image/png | Foto da fachada da unidade |
| FOTO_INTERNA | INTERIOR_PHOTO | 10 MB | image/jpeg, image/png | Foto interna da unidade |
| FOTO_DOCUMENTO | DOCUMENT_PHOTO | 10 MB | image/jpeg, image/png | Foto de documento do titular |
| DOCUMENTO_PDF | PDF_DOCUMENT | 50 MB | application/pdf | Documentos em PDF (escritura, contrato) |
| ORTOFOTO | ORTHOPHOTO | 500 MB | image/tiff, image/geotiff | GeoTIFF para processamento |
| RELATORIO | REPORT | 100 MB | application/pdf, text/csv, application/zip | Relatorios exportados |
| CERTIDAO | CERTIFICATE | 10 MB | application/pdf | Certidao de legitimacao |

### Validacao de Upload

Toda requisicao de upload passa por validacao antes de aceitar o arquivo:

1. **Content-Type**: verificado contra a lista de tipos permitidos para o DocumentType informado
2. **Tamanho**: verificado contra o limite maximo do DocumentType. Requisicoes acima do limite retornam 413 Payload Too Large
3. **Extensao**: deve corresponder ao Content-Type informado (ex: `.jpg` para `image/jpeg`)
4. **Antivirus**: em producao, o arquivo e escaneado antes de gravar no S3 (futuro — fase 2)

## Convencao de Path S3

Pattern geral: `{tenant_id}/{entity_type}/{entity_id}/{uuid}.{ext}`

### Exemplos de Paths

| Cenario | Path Completo |
|---------|--------------|
| Foto de unidade (original) | `abc123/units/unit-456/img-789.jpg` |
| Foto de unidade (thumbnail) | `abc123/units/unit-456/thumb_img-789.jpg` |
| Documento de titular | `abc123/holders/holder-789/doc-012.pdf` |
| Ortofoto original | `abc123/orthofotos/orto-345/original.tiff` |
| Ortofoto processada (tiles) | `abc123/orthofotos/orto-345/tiles/{z}/{x}/{y}.png` |
| Ortofoto thumbnail | `abc123/orthofotos/orto-345/thumb.png` |
| Relatorio exportado | `abc123/reports/report-678/export.pdf` |
| Certidao de legitimacao | `abc123/legitimation/leg-901/certidao.pdf` |
| Memorial descritivo | `abc123/legitimation/leg-901/memorial.pdf` |
| Planta de legitimacao | `abc123/legitimation/leg-901/planta.pdf` |

### Organizacao por Tenant

Cada tenant possui seu proprio "diretorio virtual" no bucket. Isso permite:

- **Isolamento**: listagem de objetos filtrada por prefix `{tenant_id}/`
- **Limpeza**: remocao de todos os dados de um tenant via delete por prefix
- **Auditoria**: identificacao rapida de qual tenant possui qual arquivo
- **Cotas**: medicao de uso de storage por tenant via S3 inventory

## Presigned URLs

| Operacao | TTL | Uso | Metodo HTTP |
|----------|-----|-----|-------------|
| Upload | 1 hora | Cliente envia arquivo direto pro S3 | PUT |
| Download | 15 minutos | Cliente baixa arquivo | GET |
| Thumbnail | 1 hora | Exibicao em listas (cacheable) | GET |

### Fluxo de Upload via Presigned URL

1. Cliente solicita presigned URL: `POST /api/documents/presigned-upload` com fileName, contentType, documentType
2. API valida permissoes, gera UUID para o arquivo, cria presigned PUT URL com TTL de 1 hora
3. API retorna `{ uploadUrl, fileKey, expiresAt }`
4. Cliente faz PUT diretamente no S3 usando a URL recebida
5. Cliente confirma upload: `POST /api/documents/confirm-upload` com fileKey
6. API verifica existencia do objeto no S3, cria registro na tabela documents, retorna DocumentDto

### Fluxo de Download via Presigned URL

1. Cliente solicita download: `GET /api/documents/{id}/download`
2. API verifica permissoes (usuario deve ter acesso ao tenant e a comunidade)
3. API gera presigned GET URL com TTL de 15 minutos
4. API retorna redirect 302 para a presigned URL (ou retorna a URL no body, conforme header Accept)

## Cleanup de Arquivos Orfaos

O job semanal **CleanupOrphanedFiles** (executado domingos as 5h UTC) realiza a limpeza de arquivos sem referencia no banco de dados.

### Algoritmo

1. Lista todos os objects no bucket com prefix `{tenant_id}/` para cada tenant ativo
2. Para cada object, extrai o `file_key` do path
3. Consulta a tabela `documents` para verificar se existe registro com aquele `file_key`
4. Se nao existe registro, marca o object para remocao
5. Antes de remover, grava log estruturado com nivel Warning contendo: tenant_id, file_key, tamanho, data de criacao do object
6. Remove o object do S3
7. Ao final, publica metrica `orphaned_files_removed_total` com label tenant_id

### Salvaguardas

- **Grace period**: arquivos criados ha menos de 48 horas sao ignorados (podem estar em processo de confirmacao de upload)
- **Dry run**: flag de configuracao `FileStorage:CleanupDryRun` permite listar sem remover
- **Limite por execucao**: maximo de 1000 arquivos removidos por execucao para evitar impacto no S3
- **Log de auditoria**: todos os arquivos removidos sao registrados em tabela `file_cleanup_log` para rastreabilidade
