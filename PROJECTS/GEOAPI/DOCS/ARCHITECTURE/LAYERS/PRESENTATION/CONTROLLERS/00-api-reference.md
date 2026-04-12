---
type: leaf
status: approved
updated: 2026-02-21
---

# API Reference

Referencia completa de todos os endpoints da GEOAPI. Cada grupo documenta as rotas em tabela, seguida de prosa descrevendo campos de request e response. Todos os endpoints requerem autenticacao via Bearer token JWT do Keycloak no header Authorization, identificacao do municipio via UUID no header X-Tenant-Id, Content-Type application/json para requests com body e Accept application/json.

---

## Units

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| POST | /api/units | Criar unidade | 201 | 400 VALIDATION_ERROR, 401 TOKEN_EXPIRED, 403 NOT_AUTHORIZED | todos autenticados |
| GET | /api/units/{id} | Obter unidade por ID | 200 | 404 | todos autenticados |
| GET | /api/units | Listar com filtros e paginacao | 200 | - | todos autenticados |
| PATCH | /api/units/{id} | Atualizar unidade | 200 | 403 UNIT_LOCKED, 404 | todos autenticados |
| DELETE | /api/units/{id} | Excluir unidade em rascunho | 204 | 400 NOT_DRAFT, 404 | todos autenticados |
| POST | /api/units/{id}/submit | Submeter para analise | 200 | 400 NO_HOLDER | todos autenticados |
| POST | /api/units/{id}/approve | Aprovar unidade | 200 | 403 NOT_AUTHORIZED | manager+ |
| POST | /api/units/{id}/reject | Rejeitar unidade | 200 | 403 NOT_AUTHORIZED | manager+ |
| GET | /api/units/geojson | Exportar como GeoJSON | 200 | - | todos autenticados |

Request de criacao (POST /api/units): body contem endereco completo com campos street, number, complement, neighborhood, city, state e zipCode todos como string. Campo communityId como UUID obrigatorio. Campo geometry como objeto contendo type "Polygon" e coordinates como array de arrays de pares de coordenadas WGS84 (longitude, latitude). Campo photos como array opcional de UUIDs referenciando documentos ja uploaded via endpoint de documents. Response retorna UnitDto com todos os campos da unidade incluindo id gerado, code automatico no formato UNI-AAAA-NNNNN, status DRAFT, timestamps e version 1.

Request de listagem (GET /api/units): query params page como inteiro (default 1), limit como inteiro (default 20, maximo 100), status como string opcional para filtrar por status, communityId como UUID opcional, search como string para busca por codigo ou endereco, sortBy aceitando code, created_at ou status, sortDir aceitando asc ou desc. Response retorna objeto paginado com campo items contendo array de UnitListItemDto (subconjunto: id, code, status, address resumido, attendance_status, created_at), campo total com contagem absoluta, page, limit e hasNext como boolean.

Request de submit (POST /api/units/{id}/submit): sem body. Pre-condicao: ao menos um titular vinculado com is_primary true. Retorna UnitDto com status atualizado para PENDING_ANALYSIS.

Request de approve (POST /api/units/{id}/approve): body contem justification como string obrigatoria com minimo 10 caracteres. Retorna UnitDto com status APPROVED.

Request de reject (POST /api/units/{id}/reject): body contem reason como string obrigatoria com minimo 50 caracteres. Retorna UnitDto com status REJECTED.

---

## Holders

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| POST | /api/holders | Criar titular | 201 | 400 CPF_INVALID, 409 CPF_EXISTS | todos autenticados |
| GET | /api/holders/{id} | Obter titular | 200 | 404 | todos autenticados |
| GET | /api/holders | Listar com paginacao | 200 | - | todos autenticados |
| PATCH | /api/holders/{id} | Atualizar titular | 200 | 404 | todos autenticados |
| DELETE | /api/holders/{id} | Excluir titular sem unidades | 204 | 400 HAS_UNITS | todos autenticados |
| GET | /api/holders/search?cpf= | Buscar por CPF | 200 | 404 | todos autenticados |
| POST | /api/holders/import | Importar planilha | 200 | 400 VALIDATION_ERROR | analyst+ |

Request de criacao (POST /api/holders): body contem cpf como string de 11 digitos sem formatacao, fullName como string com minimo 2 palavras, socialName opcional, birthDate como string ISO 8601 (AAAA-MM-DD), gender como string enum (MASCULINO, FEMININO, NAO_DECLARAR, OUTROS), filiation opcional, maritalStatus como string enum, stableUnion opcional, spouseName e spouseCpf obrigatorios quando maritalStatus e CASADO ou stableUnion diferente de NAO, email e phone opcionais, occupation e profession obrigatorios, documentType e documentNumber obrigatorios. Response retorna HolderDto com todos os campos incluindo id gerado.

Request de busca por CPF (GET /api/holders/search?cpf=): param cpf como string de 11 digitos. Retorna HolderDto se encontrado, 404 se nao existe no tenant.

Request de import (POST /api/holders/import): multipart/form-data com arquivo XLSX ou CSV. Servidor processa linha a linha, valida CPF e campos obrigatorios de cada registro. Response retorna objeto com total de linhas processadas, total importadas com sucesso, total com erro e array de erros detalhados por linha (numero da linha, campo, mensagem).

---

## Unit-Holders

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| POST | /api/units/{id}/holders | Vincular titular | 201 | 400 PERCENTAGE_EXCEEDED, 400 MULTIPLE_PRIMARY, 409 DUPLICATE | todos autenticados |
| GET | /api/units/{id}/holders | Listar titulares da unidade | 200 | 404 | todos autenticados |
| PATCH | /api/units/{id}/holders/{holderId} | Atualizar vinculo | 200 | 400 PERCENTAGE_EXCEEDED, 400 MULTIPLE_PRIMARY | todos autenticados |
| DELETE | /api/units/{id}/holders/{holderId} | Desvincular titular | 204 | - | todos autenticados |

Request de vinculacao (POST /api/units/{id}/holders): body contem holderId como UUID, relationshipType como string enum (PROPRIETARIO, CONJUGE, MORADOR, PROCURADOR, HERDEIRO), ownershipPercentage como decimal entre 0 e 100 obrigatorio quando relationshipType e PROPRIETARIO, isPrimary como boolean (default false). Response retorna UnitHolderDto com todos os campos do vinculo.

---

## Communities

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| POST | /api/communities | Criar comunidade | 201 | 400 VALIDATION_ERROR | manager+ |
| GET | /api/communities/{id} | Obter comunidade | 200 | 404 | todos autenticados |
| GET | /api/communities | Listar com paginacao | 200 | - | todos autenticados |
| PATCH | /api/communities/{id} | Atualizar comunidade | 200 | 404 | manager+ |
| GET | /api/communities/{id}/units | Listar unidades da comunidade | 200 | - | todos autenticados |
| GET | /api/communities/{id}/geojson | Exportar comunidade como GeoJSON | 200 | 404 | todos autenticados |

Request de criacao (POST /api/communities): body contem code como string unica por tenant, name como string, communityType como enum (URBANA, RURAL, QUILOMBOLA, RIBEIRINHA), boundary opcional como GeoJSON Polygon, municipality e state obrigatorios, district, neighborhood e reference opcionais. Response retorna CommunityDto.

Request de listagem de unidades (GET /api/communities/{id}/units): aceita mesmos query params de paginacao e filtro da listagem de units. Response retorna PaginatedResult de UnitListItemDto filtrado pela comunidade.

Request de export GeoJSON (GET /api/communities/{id}/geojson): retorna FeatureCollection GeoJSON contendo o boundary da comunidade como Feature com properties contendo id, code e name, e todas as unidades da comunidade como Features individuais com properties contendo id, code, status e attendance_status.

---

## Documents

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| POST | /api/documents/upload | Upload documento (multipart/form-data) | 201 | 413 FILE_TOO_LARGE, 415 UNSUPPORTED_FORMAT | todos autenticados |
| GET | /api/documents/{id} | Obter metadados com URL pre-assinada | 200 | 404 | todos autenticados |
| GET | /api/documents | Listar por entidade | 200 | - | todos autenticados |
| DELETE | /api/documents/{id} | Excluir documento | 204 | 404 | todos autenticados |
| GET | /api/documents/{id}/download | Redirect para URL pre-assinada S3 | 302 | 404 | todos autenticados |

Request de upload (POST /api/documents/upload): multipart/form-data com campo file contendo o arquivo (maximo 50MB), entityType como string (UNIT, HOLDER, COMMUNITY), entityId como UUID e documentType como string enum (RG, CPF, CNH, COMPROVANTE_RESIDENCIA, FOTO_FACHADA, FOTO_DOCUMENTO, CERTIDAO, OUTRO). Tipos de arquivo aceitos: image/jpeg, image/png, image/webp, application/pdf. Response retorna DocumentDto com id, fileName, fileSize, mimeType, checksum SHA-256 calculado pelo servidor, uploadedAt e presignedUrl valida por 1 hora para acesso direto ao arquivo.

Request de listagem (GET /api/documents): query params entityType e entityId obrigatorios para filtrar documentos de uma entidade especifica. Aceita paginacao padrao. Response retorna PaginatedResult de DocumentListItemDto.

Request de download (GET /api/documents/{id}/download): retorna HTTP 302 com Location apontando para URL pre-assinada do S3 valida por 15 minutos. O client segue o redirect para baixar o arquivo diretamente do S3.

---

## Orthofotos

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| POST | /api/orthofotos/upload | Upload ortofoto (multipart) | 202 Accepted | 413 FILE_TOO_LARGE, 415 UNSUPPORTED_FORMAT | drone-operator, analyst+ |
| GET | /api/orthofotos/{id} | Obter metadados | 200 | 404 | todos autenticados |
| GET | /api/orthofotos | Listar ortofotos do tenant | 200 | - | todos autenticados |
| GET | /api/orthofotos/jobs/{jobId} | Status do processamento | 200 | 404 | drone-operator, analyst+ |

Request de upload (POST /api/orthofotos/upload): multipart/form-data com campo file contendo arquivo GeoTIFF, communityId como UUID opcional e captureDate como string ISO 8601 opcional. Tipo aceito: image/tiff. Tamanho maximo: 500MB para ortofotos. Response retorna HTTP 202 Accepted com body contendo ortofotoId (UUID do registro criado) e jobId (UUID do job Hangfire para acompanhamento). O processamento e assincrono.

Request de status do job (GET /api/orthofotos/jobs/{jobId}): retorna objeto com status (PENDING, PROCESSING, COMPLETED, FAILED), progress como percentual estimado, error como string nullable com mensagem de erro quando FAILED e ortofotoId para referencia cruzada.

---

## Sync

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| GET | /api/sync/changes?since= | Pull mudancas desde timestamp | 200 | 401 | field-coordinator, field-cadastrator |
| POST | /api/sync/push | Push batch de operacoes locais | 200 | 401, 409 SYNC_CONFLICT | field-coordinator, field-cadastrator |
| GET | /api/sync/status | Status da ultima sync | 200 | - | field-coordinator, field-cadastrator |

Request de pull (GET /api/sync/changes?since=): param since como timestamp ISO 8601 da ultima sincronizacao bem-sucedida. Response retorna objeto com tres colecoes (units, holders, communities), cada uma subdividida em created (array de registros novos), updated (array de registros modificados) e deleted (array de UUIDs removidos). Inclui serverTimestamp para uso como since no proximo pull e hasMore como boolean indicando se existem mais mudancas para paginar.

Request de push (POST /api/sync/push): body contem array operations, cada operacao com entityType (UNIT, HOLDER, DOCUMENT), localId como string (ID local do WatermelonDB), operation como enum (CREATE, UPDATE, DELETE), payload como objeto com os dados da entidade e clientTimestamp como ISO 8601. O servidor processa sequencialmente, valida regras de negocio e retorna array results, cada resultado com localId, status (SUCCESS ou CONFLICT ou ERROR), serverId como UUID atribuido pelo servidor quando CREATE, e conflictData como objeto nullable contendo serverVersion e clientVersion dos campos divergentes quando CONFLICT.

Request de status (GET /api/sync/status): retorna objeto com lastSyncAt como timestamp da ultima sync bem-sucedida, pendingConflicts como inteiro com contagem de conflitos aguardando resolucao e pendingOperations como inteiro com operacoes na fila do servidor.

---

## Field Packages

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| GET | /api/packages/field | Metadados do pacote | 200 | 403 | field-coordinator, field-cadastrator |
| GET | /api/packages/field/{id}/download | Download binario do pacote | 200 | 404 | field-coordinator, field-cadastrator |

Request de metadados (GET /api/packages/field): retorna objeto com packageId como UUID, sizeBytes com tamanho estimado, communities como array de nomes das comunidades incluidas, createdAt com timestamp de criacao do pacote e downloadUrl como URL pre-assinada do S3 valida para download unico. O pacote contem: versao otimizada de ortofoto para as comunidades autorizadas do usuario, poligonos GeoJSON de unidades e comunidades e metadados pre-cadastrados de comunidades e unidades existentes.

Request de download (GET /api/packages/field/{id}/download): retorna binario do pacote compactado em formato ZIP com Content-Type application/zip. A URL pre-assinada expira apos primeiro uso para evitar compartilhamento indevido.

---

## Teams

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| GET | /api/teams | Listar equipes do tenant | 200 | - | manager+ |
| GET | /api/teams/{id} | Obter equipe com membros | 200 | 404 | manager+, coordinator (propria equipe) |
| GET | /api/teams/{id}/metrics | Metricas de produtividade | 200 | 404 | manager+, coordinator (propria equipe) |
| GET | /api/teams/{id}/communities | Comunidades autorizadas | 200 | 404 | todos da equipe |

Request de metricas (GET /api/teams/{id}/metrics): query param period como enum (TODAY, WEEK, MONTH, ALL) com default WEEK. Response retorna objeto com totalUnits (total de unidades cadastradas pela equipe no periodo), byStatus como objeto com contagem por cada attendance_status, byMember como array de objetos contendo memberId, memberName, unitsCount e completionPercentage, e dailyProgress como array de objetos com date e count para grafico de evolucao.

Request de comunidades (GET /api/teams/{id}/communities): retorna array de CommunityListItemDto contendo apenas as comunidades para as quais a equipe tem autorizacao, com campos id, code, name, communityType e permissionLevel.

---

## Legitimation

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| POST | /api/legitimation | Iniciar processo | 201 | 400 VALIDATION_ERROR | analyst+ |
| GET | /api/legitimation/{id} | Obter processo | 200 | 404 | analyst+ |
| GET | /api/legitimation | Listar processos com paginacao | 200 | - | analyst+ |
| POST | /api/legitimation/{id}/approve | Aprovar processo | 200 | 403 NOT_AUTHORIZED | manager+ |
| POST | /api/legitimation/{id}/reject | Rejeitar processo | 200 | 403 NOT_AUTHORIZED | manager+ |
| GET | /api/legitimation/{id}/certificate | Download PDF da certidao | 200 | 404 | analyst+ |

Request de criacao (POST /api/legitimation): body contem unitId como UUID obrigatorio. Pre-condicao: unidade com status APPROVED e ao menos um titular PROPRIETARIO vinculado. Response retorna LegitimationRequestDto com status DRAFT.

Request de approve (POST /api/legitimation/{id}/approve): body contem justification como string obrigatoria. Retorna LegitimationRequestDto com status APPROVED.

Request de reject (POST /api/legitimation/{id}/reject): body contem reason como string obrigatoria com minimo 100 caracteres citando fundamento legal. Retorna LegitimationRequestDto com status REJECTED.

Request de certificado (GET /api/legitimation/{id}/certificate): retorna arquivo PDF com Content-Type application/pdf e Content-Disposition attachment. Disponivel apenas para processos com status TITLE_ISSUED ou REGISTERED.

---

## Auth Keys

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| POST | /api/auth-keys | Gerar chave de API | 201 | 401 | analyst+ |
| GET | /api/auth-keys | Listar chaves ativas | 200 | - | analyst+ |
| DELETE | /api/auth-keys/{id} | Revogar chave | 204 | 404 | analyst+ |

Request de criacao (POST /api/auth-keys): body contem name como string descritiva (por exemplo "QGIS Desktop"). Response retorna objeto com id, name, key (UUID v4 exibido uma unica vez), expiresAt (30 dias a partir da criacao) e createdAt. O campo key nunca mais sera retornado apos esta response.

Request de listagem (GET /api/auth-keys): retorna array de objetos com id, name, createdAt, expiresAt e lastUsedAt. O campo key nunca e incluido na listagem.

---

## Headers Obrigatorios

Todas as requisicoes devem incluir os seguintes headers. Authorization com valor Bearer seguido do token JWT obtido do Keycloak. X-Tenant-Id com UUID do municipio do usuario. Content-Type com application/json para requests com body. Accept com application/json para responses.

O header X-Tenant-Id e validado contra o claim tenant_id do JWT. Se nao corresponderem, a API retorna erro TENANT_MISMATCH com HTTP 403.

---

## Formato de Erro Padrao

Todas as respostas de erro seguem RFC 7807 ProblemDetails. Campos: type como URI do tipo de erro, title como descricao curta, status como codigo HTTP, detail como mensagem legivel com contexto. Campo extensions.errorCode contem o codigo maquina conforme tabela documentada em 02-error-codes.md. Campo extensions.fields contem array de erros por campo quando aplicavel (validacao).

---

## Paginacao Padrao

Listas paginadas recebem query params page (inteiro, default 1) e limit (inteiro, default 20, maximo 100). Response inclui campos items (array de resultados), total (contagem absoluta de registros), page (pagina atual), limit (tamanho da pagina) e hasNext (boolean indicando se existe proxima pagina).
