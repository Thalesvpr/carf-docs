---
type: leaf
status: approved
updated: 2026-02-07
---

# Document

Entidade representando arquivo digital (foto, PDF) vinculado polimorficamente a qualquer entidade do sistema via EntityType e EntityId. O conteudo binario e armazenado no S3 enquanto o registro no banco contem apenas metadados e o caminho de armazenamento. Herda de BaseEntity fornecendo auditoria e soft delete.

## Papel no Dominio

Documentos sao evidencias do processo de regularizacao fundiaria: fotos de fachada comprovam a existencia e estado do imovel, copias de RG e CPF identificam o titular, comprovantes de residencia atestam moradia, certidoes formalizam decisoes. O checksum SHA-256 garante integridade do arquivo apos upload, permitindo detectar corrupcao ou adulteracao.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| TenantId | Guid | nao | Municipio. FK para Tenant. |
| EntityType | string | nao | Tipo da entidade pai. Valores: UNIT, HOLDER, COMMUNITY. |
| EntityId | Guid | nao | ID da entidade pai. Vinculo polimorfico. |
| DocumentType | string | nao | Categoria do documento. Valores: RG (carteira de identidade), CPF (cadastro de pessoa fisica), CNH (carteira de habilitacao), COMPROVANTE_RESIDENCIA (conta de agua, luz, etc), FOTO_FACHADA (foto frontal do imovel), FOTO_DOCUMENTO (foto generica de documento), CERTIDAO (certidao oficial emitida), OUTRO (documento nao categorizado). |
| FileKey | string | nao | Chave S3 do arquivo no bucket. Formato: tenant_id/entity_type/entity_id/uuid.ext. Mapeado para coluna `file_path` no banco. |
| FileName | string | nao | Nome original do arquivo preservado para referencia do usuario. |
| FileSize | long | nao | Tamanho em bytes. Limite maximo de 50MB. |
| MimeType | string | nao | Tipo MIME do arquivo. Valores aceitos: image/jpeg, image/png, image/webp, application/pdf. |
| Checksum | string | nao | Hash SHA-256 do conteudo do arquivo em hexadecimal. Calculado pelo servidor no momento do upload. |
| UploadedAt | DateTime | nao | Momento do upload. |
| UploadedBy | Guid | nao | Account que fez upload. |
| DeletedAt | DateTime | sim | Soft delete. |

## Relacionamentos

Vinculado polimorficamente a Unit, Holder ou Community via par EntityType e EntityId. Nao possui FK formal no banco pois o destino e dinamico.

## Invariantes de Negocio

FileSize nao pode exceder 50MB (52.428.800 bytes). Tentativa de upload maior retorna FILE_TOO_LARGE.

MimeType deve estar na lista de tipos aceitos. Upload com tipo diferente retorna UNSUPPORTED_FORMAT.

Checksum e calculado pelo servidor e comparado com o hash do arquivo recebido para garantir integridade da transmissao.

Fotos no contexto de sincronizacao offline seguem padrao append-only: fotos do client sempre sobem ao servidor, fotos do servidor sempre baixam ao dispositivo. Nao ha substituicao ou exclusao cruzada durante sync.

## Domain Events

DocumentUploadedEvent emitido ao concluir upload com sucesso.
