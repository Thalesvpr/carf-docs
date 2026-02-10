---
type: leaf
status: approved
updated: 2026-02-07
---

# Database Schema

Especificacao completa do schema PostgreSQL 15 com extensao PostGIS 3.4 utilizado pela GEOAPI. Todas as tabelas operam sob Row-Level Security (RLS) com isolamento por tenant_id extraido da variavel de sessao app.current_tenant definida pelo middleware de autenticacao a cada requisicao. O schema e versionado via EF Core Migrations e toda alteracao passa por migration incremental sem perda de dados.

### Status de Implementacao

Das 20 tabelas documentadas, **11 possuem entidades implementadas no codigo-fonte** (DOMAIN + INFRA com EF Core Configuration). As demais 9 estao documentadas como especificacao para implementacao futura.

| Status | Significado |
|--------|-------------|
| IMPLEMENTADA | Entidade existe no DOMAIN, Configuration no INFRA, DbSet no DbContext |
| PLANEJADA | Especificacao aprovada, sem codigo correspondente ainda |

| # | Tabela | Status |
|---|--------|--------|
| 1 | units | IMPLEMENTADA |
| 2 | holders | IMPLEMENTADA |
| 3 | unit_holders | IMPLEMENTADA |
| 4 | communities | IMPLEMENTADA |
| 5 | blocks | PLANEJADA |
| 6 | plots | PLANEJADA |
| 7 | buildings | PLANEJADA |
| 8 | documents | IMPLEMENTADA |
| 9 | teams | IMPLEMENTADA |
| 10 | team_members | IMPLEMENTADA (sem Configuration dedicada — usa convencoes EF Core) |
| 11 | community_authorizations | IMPLEMENTADA (sem Configuration dedicada — usa convencoes EF Core) |
| 12 | orthofotos | PLANEJADA |
| 13 | legitimation_requests | PLANEJADA |
| 14 | legitimation_responses | PLANEJADA |
| 15 | legitimation_certificates | PLANEJADA |
| 16 | sync_logs | IMPLEMENTADA |
| 17 | audit_logs | PLANEJADA |
| 18 | layers | PLANEJADA |
| 19 | layer_features | PLANEJADA |
| 20 | annotations | PLANEJADA |

---

## 1. units

Tabela central do sistema representando unidades habitacionais cadastradas em campo ou pelo analista. Cada unidade pertence a uma comunidade e pode opcionalmente estar vinculada a um bloco, lote e edificacao. O endereco e desnormalizado em colunas separadas para facilitar buscas textuais sem joins. A geometria e armazenada em formato PostGIS para queries espaciais. O campo version implementa controle de concorrencia otimista.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| tenant_id | uuid | nao | - | FK para tenants. Isolamento RLS. |
| community_id | uuid | nao | - | FK para communities. Comunidade a que pertence. |
| block_id | uuid | sim | null | FK para blocks. Quadra, desnormalizado para queries. |
| plot_id | uuid | sim | null | FK para plots. Lote formal quando existente. |
| building_id | uuid | sim | null | FK para buildings. Edificacao quando aplicavel. |
| code | varchar(50) | nao | - | Codigo unico por tenant. Gerado automaticamente pelo servidor no formato UNI-AAAA-NNNNN. |
| status | varchar(30) | nao | 'DRAFT' | Status atual. CHECK em DRAFT, PENDING_ANALYSIS, IN_REVIEW, APPROVED, REJECTED, REQUIRES_CHANGES. |
| address_street | varchar(200) | sim | null | Logradouro. |
| address_number | varchar(20) | sim | null | Numero. |
| address_complement | varchar(100) | sim | null | Complemento. |
| address_neighborhood | varchar(100) | sim | null | Bairro. |
| address_city | varchar(100) | sim | null | Cidade. |
| address_state | varchar(2) | sim | null | UF. |
| address_zip_code | varchar(9) | sim | null | CEP sem formatacao. |
| boundary | geometry(Polygon, 4326) | sim | null | Perimetro da unidade em WGS84. |
| centroid | geometry(Point, 4326) | sim | null | Centroide calculado a partir do boundary. |
| area | decimal(15,4) | sim | null | Area calculada via ST_Area em metros quadrados. |
| declared_area | decimal(15,4) | sim | null | Area declarada pelo titular quando diferente da calculada. |
| occupant_type | varchar(30) | sim | null | POSSUIDOR ou LOCATARIO. |
| utilization_type | varchar(30) | sim | null | RESIDENCIAL, COMERCIAL, MISTO, TERRENO_VAZIO, NAO_HABITADO. |
| unit_condition | varchar(30) | sim | null | OCUPADA, VAZIA, EM_CONSTRUCAO, ABANDONADA. |
| attendance_status | varchar(30) | sim | null | AUSENTE, PRESENTE, NAO_QUIS, ASSINADO. |
| residence_time | varchar(100) | sim | null | Tempo de moradia declaratorio em texto livre. |
| observation | text | sim | null | Observacoes do agente de campo. |
| facade_photo_path | varchar(500) | sim | null | Caminho S3 da foto de fachada principal. |
| custom_data | jsonb | sim | null | Dados especificos do tenant em formato livre. |
| created_at | timestamptz | nao | now() | Data de criacao. |
| updated_at | timestamptz | nao | now() | Ultima atualizacao. |
| created_by | uuid | nao | - | FK para account que criou. |
| updated_by | uuid | nao | - | FK para account que atualizou por ultimo. |
| deleted_at | timestamptz | sim | null | Soft delete. Null indica registro ativo. |
| version | int | nao | 1 | Controle de concorrencia otimista. Incrementado a cada update. |

Indices: composto em (tenant_id, community_id) para queries de listagem de unidades por comunidade. GiST em boundary para queries espaciais como ST_Contains e ST_Intersects. UNIQUE em (tenant_id, code) garantindo codigo unico por municipio. Composto em (tenant_id, status) para filtros de listagem por status. Parcial em deleted_at IS NULL para excluir soft-deleted das queries padrao.

RLS Policy tenant_isolation: filtra automaticamente todas as queries por tenant_id igual a current_setting('app.current_tenant')::uuid.

---

## 2. holders

Titular ou posseiro pessoa fisica vinculado a uma ou mais unidades. Armazena todos os dados pessoais, documentais e socioeconomicos necessarios para o processo de legitimacao fundiaria. O CPF e o identificador natural do titular dentro de cada tenant.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| tenant_id | uuid | nao | - | FK para tenants. |
| cpf | varchar(11) | nao | - | CPF sem formatacao. Validado via algoritmo Mod11. |
| cnpj | varchar(14) | sim | null | CNPJ para pessoa juridica. Mutuamente exclusivo com CPF em contexto de legitimacao. |
| full_name | varchar(200) | nao | - | Nome completo. Minimo 2 palavras. |
| social_name | varchar(200) | sim | null | Nome social quando diferente do nome de registro. |
| birth_date | date | nao | - | Data de nascimento. |
| gender | varchar(30) | nao | - | MASCULINO, FEMININO, NAO_DECLARAR, OUTROS. |
| filiation | varchar(400) | sim | null | Campo unico opcional com 1 ou 2 nomes de filiacao. |
| marital_status | varchar(30) | nao | - | SOLTEIRO, CASADO, DIVORCIADO, VIUVO, SEPARADO. |
| stable_union | varchar(30) | sim | null | NAO, RECONHECIDA_CARTORIO, NAO_RECONHECIDA. |
| spouse_name | varchar(200) | sim | null | Obrigatorio se marital_status CASADO ou stable_union diferente de NAO. |
| spouse_cpf | varchar(11) | sim | null | CPF do conjuge. Obrigatorio se casado ou uniao estavel. |
| email | varchar(200) | sim | null | Email de contato. |
| phone | varchar(20) | sim | null | Telefone com DDD. |
| occupation | varchar(100) | nao | - | Situacao profissional: empregado formal, autonomo, aposentado, etc. |
| profession | varchar(100) | nao | - | Profissao conforme CBO simplificada. |
| education_level | varchar(50) | sim | null | Nivel de escolaridade. |
| monthly_income | decimal(12,2) | sim | null | Renda mensal declarada em reais. Relevante para REURB-S vs REURB-E. |
| dependents_count | int | sim | null | Numero de dependentes. |
| nationality | varchar(50) | nao | 'BRASILEIRA' | Nacionalidade. |
| document_type | varchar(30) | nao | - | RG, CNH, CIN, PASSAPORTE, CTPS. |
| document_number | varchar(30) | nao | - | Numero do documento de identificacao. |
| signature_path | varchar(500) | sim | null | Caminho S3 do PNG da assinatura digital criptografado AES-256. |
| signature_timestamp | timestamptz | sim | null | Momento exato da captura da assinatura. |
| signature_device_id | varchar(100) | sim | null | Identificador do dispositivo usado para assinatura. |
| created_at | timestamptz | nao | now() | Data de criacao. |
| updated_at | timestamptz | nao | now() | Ultima atualizacao. |
| created_by | uuid | nao | - | Quem cadastrou. |
| updated_by | uuid | nao | - | Quem atualizou por ultimo. |
| version | int | nao | 1 | Controle de concorrencia otimista para sincronizacao mobile. Incrementado a cada atualizacao. |
| deleted_at | timestamptz | sim | null | Soft delete. |

Indices: UNIQUE em (tenant_id, cpf) garantindo um unico titular por CPF por municipio. Composto em (tenant_id, full_name) para busca por nome. Parcial em deleted_at IS NULL.

---

## 3. unit_holders

Tabela de juncao N:N entre unidades e titulares. Cada registro representa o vinculo de um titular com uma unidade, especificando o tipo de relacionamento e o percentual de propriedade quando aplicavel.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| unit_id | uuid | nao | - | FK para units. ON DELETE CASCADE. |
| holder_id | uuid | nao | - | FK para holders. ON DELETE RESTRICT. |
| relationship_type | varchar(30) | nao | - | CHECK em PROPRIETARIO, CONJUGE, MORADOR, PROCURADOR, HERDEIRO. |
| ownership_percentage | decimal(5,2) | sim | null | Percentual de propriedade. CHECK entre 0 e 100. Obrigatorio para PROPRIETARIO. |
| is_primary | boolean | nao | false | Titular principal responsavel legal pela unidade. |
| created_at | timestamptz | nao | now() | Quando o vinculo foi criado. |
| created_by | uuid | nao | - | Quem criou o vinculo. |

Constraints: UNIQUE em (unit_id, holder_id) impedindo vinculo duplicado do mesmo titular na mesma unidade. CHECK constraint validando que a soma de ownership_percentage por unit_id nao excede 100, implementada via trigger. CHECK constraint garantindo exatamente um is_primary true por unit_id, implementada via trigger after insert/update.

---

## 4. communities

Comunidade ou assentamento que agrupa unidades habitacionais em um contexto geografico e social especifico. Serve como unidade organizacional principal para os processos de regularizacao fundiaria e como escopo de autorizacao de acesso para equipes de campo.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| tenant_id | uuid | nao | - | FK para tenants. |
| code | varchar(50) | nao | - | Codigo unico por tenant. |
| name | varchar(200) | nao | - | Nome da comunidade. |
| community_type | varchar(30) | nao | - | CHECK em URBANA, RURAL, QUILOMBOLA, RIBEIRINHA. |
| boundary | geometry(Polygon, 4326) | sim | null | Perimetro da comunidade em WGS84. |
| area | decimal(15,4) | sim | null | Area em metros quadrados. |
| municipality | varchar(100) | nao | - | Municipio. |
| state | varchar(2) | nao | - | UF. |
| district | varchar(100) | sim | null | Distrito. |
| neighborhood | varchar(100) | sim | null | Bairro. |
| reference | text | sim | null | Ponto de referencia. |
| status | varchar(30) | nao | 'ACTIVE' | Status da comunidade. |
| created_at | timestamptz | nao | now() | Data de criacao. |
| updated_at | timestamptz | nao | now() | Ultima atualizacao. |
| created_by | uuid | nao | - | Quem criou. |
| updated_by | uuid | nao | - | Quem atualizou. |
| deleted_at | timestamptz | sim | null | Soft delete. |

Indices: UNIQUE em (tenant_id, code). GiST em boundary para queries espaciais. Composto em (tenant_id, status).

---

## 5. blocks — PLANEJADA

Subdivisao espacial de uma comunidade representando uma quadra urbana. Organiza o territorio em areas menores contendo multiplos lotes. Opcional: comunidades rurais ou assentamentos informais podem nao ter blocos.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| community_id | uuid | nao | - | FK para communities. |
| code | varchar(50) | nao | - | Codigo unico dentro da comunidade. |
| name | varchar(100) | sim | null | Nome descritivo opcional. |
| boundary | geometry(Polygon, 4326) | sim | null | Perimetro da quadra. |
| area | decimal(15,4) | sim | null | Area em metros quadrados. |
| created_at | timestamptz | nao | now() | Data de criacao. |
| updated_at | timestamptz | nao | now() | Ultima atualizacao. |
| deleted_at | timestamptz | sim | null | Soft delete. |

Indices: UNIQUE em (community_id, code). GiST em boundary.

---

## 6. plots — PLANEJADA

Lote individual dentro de um bloco representando a parcela cadastral minima. Pode ou nao estar vinculado a uma unidade, permitindo representar lotes vagos.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| block_id | uuid | nao | - | FK para blocks. |
| code | varchar(50) | nao | - | Codigo unico dentro do bloco. |
| boundary | geometry(Polygon, 4326) | sim | null | Perimetro do lote. |
| area | decimal(15,4) | sim | null | Area em metros quadrados. |
| created_at | timestamptz | nao | now() | Data de criacao. |
| updated_at | timestamptz | nao | now() | Ultima atualizacao. |
| deleted_at | timestamptz | sim | null | Soft delete. |

Indices: UNIQUE em (block_id, code). GiST em boundary.

---

## 7. buildings — PLANEJADA

Edificacao dentro de um lote que pode conter multiplas unidades habitacionais. Util para predios, vilas e conjuntos habitacionais onde um unico lote tem varias unidades.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| plot_id | uuid | sim | null | FK para plots. Nullable pois edificacao pode existir sem lote formal. |
| unit_count | int | nao | 1 | Numero de unidades na edificacao. |
| building_type | varchar(50) | nao | - | CASA, APARTAMENTO, COMERCIAL, MISTO. |
| floors_count | int | sim | null | Numero de andares. |
| created_at | timestamptz | nao | now() | Data de criacao. |
| updated_at | timestamptz | nao | now() | Ultima atualizacao. |
| deleted_at | timestamptz | sim | null | Soft delete. |

---

## 8. documents

Documentos e fotos vinculados a qualquer entidade do sistema via relacionamento polimorfico. Cada registro armazena metadados do arquivo enquanto o conteudo binario fica no S3. O checksum SHA-256 garante integridade do arquivo apos upload.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| tenant_id | uuid | nao | - | FK para tenants. |
| entity_type | varchar(30) | nao | - | Tipo da entidade pai: UNIT, HOLDER, COMMUNITY. |
| entity_id | uuid | nao | - | ID da entidade pai. |
| document_type | varchar(50) | nao | - | CHECK em RG, CPF, CNH, COMPROVANTE_RESIDENCIA, FOTO_FACHADA, FOTO_DOCUMENTO, CERTIDAO, OUTRO. |
| file_path | varchar(500) | nao | - | Caminho completo no S3. |
| file_name | varchar(200) | nao | - | Nome original do arquivo preservado. |
| file_size | bigint | nao | - | Tamanho em bytes. |
| mime_type | varchar(100) | nao | - | Tipo MIME: image/jpeg, image/png, image/webp, application/pdf. |
| checksum | varchar(64) | nao | - | Hash SHA-256 do conteudo do arquivo. |
| uploaded_at | timestamptz | nao | now() | Momento do upload. |
| uploaded_by | uuid | nao | - | Quem fez upload. |
| deleted_at | timestamptz | sim | null | Soft delete. |

Indices: composto em (entity_type, entity_id) para listar documentos de uma entidade. Composto em (tenant_id, document_type) para relatorios.

---

## 9. teams

Equipe de campo que agrupa usuarios para atribuicao coletiva de acesso a comunidades. Cada equipe tem um coordenador e um ou mais cadastradores.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| tenant_id | uuid | nao | - | FK para tenants. |
| name | varchar(100) | nao | - | Nome da equipe. |
| description | text | sim | null | Descricao opcional. |
| created_at | timestamptz | nao | now() | Data de criacao. |
| updated_at | timestamptz | nao | now() | Ultima atualizacao. |
| deleted_at | timestamptz | sim | null | Soft delete. |

Indices: composto em (tenant_id, name).

---

## 10. team_members

Membros de uma equipe de campo com papel especifico. O papel define as permissoes do membro dentro do app mobile REURBCAD.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| team_id | uuid | nao | - | FK para teams. |
| account_id | uuid | nao | - | UUID do usuario no Keycloak. |
| role | varchar(30) | nao | - | COORDINATOR ou CADASTRATOR. |
| joined_at | timestamptz | nao | now() | Data de entrada na equipe. |
| left_at | timestamptz | sim | null | Data de saida. Null indica membro ativo. |

Indices: UNIQUE em (team_id, account_id) impedindo membro duplicado na mesma equipe.

---

## 11. community_authorizations

Controle de acesso granular por comunidade, podendo ser atribuido a uma equipe inteira ou a um usuario individual. Quando atribuido a uma equipe, todos os membros ativos herdam a autorizacao.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| community_id | uuid | nao | - | FK para communities. |
| team_id | uuid | sim | null | FK para teams. Mutuamente exclusivo com account_id. |
| account_id | uuid | sim | null | UUID do usuario. Mutuamente exclusivo com team_id. |
| permission_level | varchar(30) | nao | - | READ, WRITE ou ADMIN. |
| granted_at | timestamptz | nao | now() | Quando a autorizacao foi concedida. |
| granted_by | uuid | nao | - | Quem concedeu. |

Constraints: CHECK garantindo que exatamente um entre team_id e account_id esta preenchido (XOR).

---

## 12. orthofotos — PLANEJADA

Ortofotos de drone vinculadas opcionalmente a uma comunidade. Armazena metadados do arquivo original e das versoes processadas (otimizada para web e tiles para o mapa). O processamento e assincrono via Hangfire.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| tenant_id | uuid | nao | - | FK para tenants. |
| community_id | uuid | sim | null | FK para communities. Nullable se ortofoto cobre area sem comunidade cadastrada. |
| original_path | varchar(500) | nao | - | Caminho S3 do arquivo GeoTIFF original. |
| optimized_path | varchar(500) | sim | null | Caminho S3 da versao JPEG otimizada para web. Preenchido apos processamento. |
| tiles_path | varchar(500) | sim | null | Caminho base S3 dos tiles XYZ. Preenchido apos processamento. |
| file_size | bigint | nao | - | Tamanho do arquivo original em bytes. |
| width | int | sim | null | Largura em pixels. Extraido via GDAL apos processamento. |
| height | int | sim | null | Altura em pixels. |
| srid | int | sim | null | Sistema de referencia espacial. Esperado 4326 ou equivalente. |
| bounds_geojson | jsonb | sim | null | Limites geograficos da ortofoto em formato GeoJSON Polygon. |
| capture_date | date | sim | null | Data do voo de captura. |
| processing_status | varchar(30) | nao | 'PENDING' | CHECK em PENDING, PROCESSING, COMPLETED, FAILED. |
| processing_error | text | sim | null | Mensagem de erro quando status FAILED. |
| uploaded_at | timestamptz | nao | now() | Momento do upload. |
| uploaded_by | uuid | nao | - | Quem fez upload. |
| processed_at | timestamptz | sim | null | Quando o processamento concluiu. |

Indices: composto em (tenant_id). Composto em (processing_status) para fila de processamento.

---

## 13. legitimation_requests — PLANEJADA

Processo de legitimacao fundiaria conforme Lei 13.465/2017. Cada registro representa um requerimento de legitimacao vinculado a uma unidade, acompanhando todo o ciclo de vida desde a submissao ate o registro em cartorio.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| tenant_id | uuid | nao | - | FK para tenants. |
| unit_id | uuid | nao | - | FK para units. Unidade objeto da legitimacao. |
| status | varchar(30) | nao | 'DRAFT' | CHECK em DRAFT, SUBMITTED, UNDER_ANALYSIS, NOTIFICATION_PUBLISHED, CONTESTATION_PERIOD, CONTESTATION_RECEIVED, DECISION_PENDING, APPROVED, REJECTED, TITLE_ISSUED, REGISTERED. |
| requested_at | timestamptz | nao | now() | Data de protocolo. |
| requested_by | uuid | nao | - | Quem iniciou o processo. |
| analyst_id | uuid | sim | null | Analyst responsavel pela analise. |
| manager_id | uuid | sim | null | Manager responsavel pela decisao. |
| decision | varchar(30) | sim | null | APPROVED ou REJECTED. |
| decision_reason | text | sim | null | Justificativa da decisao. |
| decision_at | timestamptz | sim | null | Quando a decisao foi tomada. |
| deadline | date | sim | null | Prazo para decisao (120 dias apos fechamento de contestacao). |
| contestation_deadline | date | sim | null | Prazo final para contestacoes (30 dias apos publicacao). |
| created_at | timestamptz | nao | now() | Data de criacao. |
| updated_at | timestamptz | nao | now() | Ultima atualizacao. |
| deleted_at | timestamptz | sim | null | Soft delete. |

Indices: composto em (tenant_id, status). UNIQUE em (unit_id) impedindo dois processos ativos para a mesma unidade (parcial onde deleted_at IS NULL e status NOT IN ('REJECTED')).

---

## 14. legitimation_responses — PLANEJADA

Respostas e pareceres vinculados a um processo de legitimacao. Inclui pareceres tecnicos de analistas, decisoes de managers e contestacoes de terceiros.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| request_id | uuid | nao | - | FK para legitimation_requests. |
| responder_id | uuid | nao | - | UUID do responsavel pela resposta. |
| response_type | varchar(30) | nao | - | PARECER_TECNICO, DECISAO, CONTESTACAO, CORRECAO. |
| content | text | nao | - | Texto completo da resposta. |
| responded_at | timestamptz | nao | now() | Quando a resposta foi registrada. |

---

## 15. legitimation_certificates — PLANEJADA

Certidoes de legitimacao fundiaria emitidas apos aprovacao do processo. Cada certidao tem numero unico sequencial e gera um PDF oficial armazenado no S3.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| request_id | uuid | nao | - | FK para legitimation_requests. |
| certificate_number | varchar(50) | nao | - | Numero unico sequencial no formato CERT-AAAA-NNNNN. |
| situation | varchar(30) | nao | - | COVERED, CONFRONTING, BOTH. |
| issued_at | timestamptz | nao | now() | Data de emissao. |
| issued_by | uuid | nao | - | Quem emitiu. |
| pdf_path | varchar(500) | nao | - | Caminho S3 do PDF da certidao. |

Constraints: UNIQUE em certificate_number globalmente.

---

## 16. sync_logs

Registro de cada operacao de sincronizacao entre o app mobile REURBCAD e o servidor GEOAPI. Usado para rastreabilidade, deteccao de conflitos e depuracao de problemas de sincronizacao.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| tenant_id | uuid | nao | - | FK para tenants. |
| user_id | uuid | nao | - | UUID do usuario que sincronizou. |
| entity_type | varchar(30) | nao | - | Tipo da entidade: UNIT, HOLDER, DOCUMENT, etc. |
| entity_id | uuid | nao | - | ID da entidade sincronizada. |
| operation | varchar(10) | nao | - | CREATE, UPDATE ou DELETE. |
| payload | jsonb | nao | - | Dados completos da operacao em formato JSON. |
| synced_at | timestamptz | nao | now() | Quando a sync foi processada no servidor. |
| client_timestamp | timestamptz | nao | - | Timestamp do client no momento da operacao local. |
| server_timestamp | timestamptz | nao | now() | Timestamp do servidor ao processar. |
| conflict_resolved | boolean | nao | false | Se houve conflito e foi resolvido. |

Indices: composto em (tenant_id, user_id). Composto em (entity_type, entity_id).

---

## 17. audit_logs — PLANEJADA

Trilha de auditoria imutavel registrando todas as operacoes de escrita no sistema. Append-only: registros nunca sao atualizados ou deletados. Retencao minima de 7 anos conforme LGPD para dados pessoais.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| tenant_id | uuid | nao | - | FK para tenants. |
| user_id | uuid | sim | null | UUID do usuario. Null se operacao automatica. |
| action | varchar(30) | nao | - | CREATE, UPDATE, DELETE, LOGIN, LOGOUT, STATUS_CHANGE. |
| entity_type | varchar(30) | nao | - | Tipo da entidade afetada. |
| entity_id | uuid | nao | - | ID da entidade afetada. |
| old_values | jsonb | sim | null | Valores anteriores. Null em CREATE. |
| new_values | jsonb | sim | null | Novos valores. Null em DELETE. |
| ip_address | varchar(45) | sim | null | IP de origem da requisicao. IPv4 ou IPv6. |
| user_agent | varchar(500) | sim | null | User-Agent do cliente HTTP. |
| timestamp | timestamptz | nao | now() | Momento da operacao. |

Indices: composto em (tenant_id, entity_type, entity_id) para historico de uma entidade. Composto em (tenant_id, user_id, timestamp) para auditoria por usuario. Particionamento por mes recomendado para tabelas com alto volume.

---

## 18. layers — PLANEJADA

Camadas GIS customizaveis por tenant para visualizacao de dados espaciais adicionais ao dominio principal de unidades e comunidades. Exemplos: areas de risco, rede de agua, perimetros de preservacao.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| tenant_id | uuid | nao | - | FK para tenants. |
| name | varchar(200) | nao | - | Nome da camada. |
| layer_type | varchar(30) | nao | - | POINT, LINESTRING, POLYGON. |
| source_url | varchar(500) | sim | null | URL de origem se importada de servico externo. |
| visible | boolean | nao | true | Visivel por padrao. |
| opacity | decimal(3,2) | nao | 1.00 | Opacidade de 0 a 1. |
| z_index | int | nao | 0 | Ordem de empilhamento. Maior fica por cima. |
| created_at | timestamptz | nao | now() | Data de criacao. |
| updated_at | timestamptz | nao | now() | Ultima atualizacao. |
| deleted_at | timestamptz | sim | null | Soft delete. |

Indices: composto em (tenant_id, z_index).

---

## 19. layer_features — PLANEJADA

Features individuais de uma camada, cada uma com geometria propria e atributos descritivos em formato JSONB extensivel. Permite armazenar qualquer dado espacial customizado sem alteracao de schema.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| layer_id | uuid | nao | - | FK para layers. |
| geometry | geometry | nao | - | Geometria PostGIS. Tipo deve corresponder ao layer_type da camada pai. |
| properties | jsonb | sim | null | Atributos descritivos em formato livre. |
| created_at | timestamptz | nao | now() | Data de criacao. |
| updated_at | timestamptz | nao | now() | Ultima atualizacao. |
| deleted_at | timestamptz | sim | null | Soft delete. |

Indices: GiST em geometry para queries espaciais. Composto em (layer_id). GIN em properties para queries JSONB.

---

## 20. annotations — PLANEJADA

Anotacoes e observacoes vinculadas a qualquer entidade do sistema via relacionamento polimorfico. Permite registrar notas, alertas, problemas e lembretes com rastreamento de resolucao.

| Coluna | Tipo PostgreSQL | Nullable | Default | Descricao |
|--------|----------------|----------|---------|-----------|
| id | uuid | nao | gen_random_uuid() | Chave primaria. |
| tenant_id | uuid | nao | - | FK para tenants. |
| entity_type | varchar(30) | nao | - | Tipo da entidade anotada. |
| entity_id | uuid | nao | - | ID da entidade. |
| annotation_type | varchar(30) | nao | - | NOTE, WARNING, ISSUE, REMINDER. |
| content | text | nao | - | Texto da anotacao. |
| priority | varchar(10) | sim | null | LOW, NORMAL, HIGH, URGENT. Obrigatorio para ISSUE e REMINDER. |
| created_at | timestamptz | nao | now() | Data de criacao. |
| created_by | uuid | nao | - | Quem criou. |
| deleted_at | timestamptz | sim | null | Soft delete. |

Indices: composto em (entity_type, entity_id) para listar anotacoes de uma entidade. Composto em (tenant_id, annotation_type) para dashboards.
