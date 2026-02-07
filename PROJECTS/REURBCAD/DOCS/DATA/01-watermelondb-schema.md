---
type: leaf
status: approved
updated: 2026-02-07
---

# WatermelonDB Schema

Schema completo do banco local SQLite gerenciado pelo WatermelonDB no app REURBCAD. Cada tabela espelha um subset das tabelas correspondentes no servidor PostgreSQL da GEOAPI, contendo apenas os campos necessarios para operacao em campo. O adapter SQLite e configurado com modo JSI para performance nativa, evitando o overhead da bridge JavaScript.

---

## units

Armazena unidades habitacionais coletadas ou atualizadas em campo. Espelha subset da tabela units do servidor com campos relevantes para o cadastro mobile.

| Coluna | Tipo WatermelonDB | Obrigatoria | Descricao |
|--------|-------------------|-------------|-----------|
| server_id | string | nao | ID do servidor atribuido apos primeira sincronizacao. Null para registros criados offline ainda nao sincronizados. |
| tenant_id | string | sim | Identificador do municipio. Preenchido automaticamente a partir da sessao do usuario. |
| community_id | string | sim | Comunidade vinculada. Selecionada pelo usuario ao iniciar cadastro. |
| code | string | nao | Codigo gerado pelo servidor no formato UNI-AAAA-NNNNN. Null ate primeira sync. |
| attendance_status | string | sim | Status do atendimento em campo: AUSENTE (ninguem em casa, foto fachada obrigatoria), PRESENTE (morador presente, formulario completo), NAO_QUIS (morador recusou, observacao obrigatoria), ASSINADO (formulario completo com assinatura coletada). |
| occupant_type | string | nao | POSSUIDOR ou LOCATARIO. |
| utilization_type | string | nao | RESIDENCIAL, COMERCIAL, MISTO, TERRENO_VAZIO, NAO_HABITADO. |
| unit_condition | string | nao | OCUPADA, VAZIA, EM_CONSTRUCAO, ABANDONADA. |
| address_street | string | nao | Logradouro. |
| address_number | string | nao | Numero. |
| address_complement | string | nao | Complemento. |
| address_neighborhood | string | nao | Bairro. |
| residence_time | string | nao | Declaratorio em texto livre: "5 anos", "mais de 20 anos". |
| observation | string | nao | Observacoes do agente de campo. Texto livre. |
| latitude | number | nao | Latitude GPS WGS84 do centroide ou posicao do agente. |
| longitude | number | nao | Longitude GPS WGS84. |
| gps_accuracy | number | nao | Precisao do GPS em metros no momento da captura. |
| area | number | nao | Area calculada em metros quadrados quando boundary disponivel. |
| facade_photo_path | string | nao | Caminho local da foto de fachada no filesystem do dispositivo. |
| created_by | string | sim | ID do usuario que criou o registro. |
| version | number | sim | Controle de concorrencia otimista. Comparado com servidor durante sync. |

Relacoes: tem muitos holders via tabela de juncao unit_holders (campo unit_id). Tem muitos documents via query por entity_id onde entity_type e UNIT.

---

## holders

Armazena titulares cadastrados em campo com dados pessoais e socioeconomicos completos.

| Coluna | Tipo WatermelonDB | Obrigatoria | Descricao |
|--------|-------------------|-------------|-----------|
| server_id | string | nao | ID do servidor apos sync. |
| tenant_id | string | sim | Municipio. |
| cpf | string | sim | CPF validado com 11 digitos. Validacao Mod11 executada offline antes de salvar. |
| full_name | string | sim | Nome completo com minimo de 2 palavras. |
| social_name | string | nao | Nome social quando diferente do registro civil. |
| birth_date | number | sim | Data de nascimento como timestamp Unix em milissegundos. |
| gender | string | sim | MASCULINO, FEMININO, NAO_DECLARAR, OUTROS. |
| filiation | string | nao | Campo unico opcional com 1 ou 2 nomes de filiacao. |
| marital_status | string | sim | SOLTEIRO, CASADO, DIVORCIADO, VIUVO, SEPARADO. |
| stable_union | string | nao | NAO, RECONHECIDA_CARTORIO, NAO_RECONHECIDA. |
| spouse_name | string | nao | Obrigatorio se casado ou uniao estavel reconhecida ou nao. |
| spouse_cpf | string | nao | CPF do conjuge. Obrigatorio se casado ou uniao estavel. |
| email | string | nao | Email de contato. |
| phone | string | nao | Telefone com DDD. |
| occupation | string | sim | Situacao profissional: empregado formal, autonomo, aposentado, etc. |
| profession | string | sim | Profissao conforme CBO simplificada ou texto livre com "Outros". |
| signature_path | string | nao | Caminho local do PNG da assinatura criptografado AES-256. |
| signature_timestamp | number | nao | Timestamp Unix em milissegundos do momento da assinatura. |
| signature_device_id | string | nao | Identificador unico do dispositivo que capturou a assinatura. |
| created_by | string | sim | Quem cadastrou. |
| version | number | sim | Concorrencia otimista. |

---

## unit_holders

Tabela de juncao entre units e holders armazenando o tipo de vinculo e percentual de propriedade.

| Coluna | Tipo WatermelonDB | Obrigatoria | Descricao |
|--------|-------------------|-------------|-----------|
| server_id | string | nao | ID do servidor apos sync. |
| unit_id | string | sim | Referencia para unit local. |
| holder_id | string | sim | Referencia para holder local. |
| relationship_type | string | sim | PROPRIETARIO, CONJUGE, MORADOR, PROCURADOR, HERDEIRO. |
| ownership_percentage | number | nao | Percentual de propriedade entre 0 e 100. Obrigatorio para PROPRIETARIO. |
| is_primary | boolean | sim | Titular principal da unidade. Exatamente um por unidade. |

---

## documents

Metadados de documentos e fotos capturados ou baixados. O arquivo binario fica no filesystem local.

| Coluna | Tipo WatermelonDB | Obrigatoria | Descricao |
|--------|-------------------|-------------|-----------|
| server_id | string | nao | ID do servidor apos sync. |
| tenant_id | string | sim | Municipio. |
| entity_type | string | sim | UNIT ou HOLDER. |
| entity_id | string | sim | ID local da entidade vinculada. |
| document_type | string | sim | RG, CPF, CNH, COMPROVANTE_RESIDENCIA, FOTO_FACHADA, FOTO_DOCUMENTO, CERTIDAO, OUTRO. |
| file_path | string | sim | Caminho local do arquivo no dispositivo. |
| file_name | string | sim | Nome original do arquivo. |
| file_size | number | sim | Tamanho em bytes. |
| mime_type | string | sim | Tipo MIME: image/jpeg, image/png, application/pdf. |
| uploaded | boolean | sim | Se ja foi enviado ao servidor. Default false. |

---

## sync_queue

Fila persistente de operacoes pendentes de sincronizacao. Operacoes ficam na fila ate serem enviadas com sucesso ao servidor ou ate falharem definitivamente apos todas as tentativas de retry.

| Coluna | Tipo WatermelonDB | Obrigatoria | Descricao |
|--------|-------------------|-------------|-----------|
| entity_type | string | sim | Tipo da entidade: UNIT, HOLDER, UNIT_HOLDER, DOCUMENT. |
| entity_id | string | sim | ID local da entidade. |
| operation | string | sim | CREATE, UPDATE ou DELETE. |
| payload | string | sim | Dados completos da operacao serializados como texto JSON. |
| retry_count | number | sim | Numero de tentativas ja realizadas. Default 0. Maximo 5. |
| status | string | sim | PENDING (aguardando envio), PROCESSING (sendo enviada), FAILED (falhou apos todas tentativas). |
| created_at | number | sim | Timestamp de criacao da operacao. |

Fila ordenada por prioridade implicita: documents com entity_type UNIT e document_type FOTO_FACHADA tem prioridade sobre outros documentos. Operacoes CREATE tem prioridade sobre UPDATE. DELETE tem prioridade mais baixa.

---

## communities

Comunidades baixadas do servidor durante o download do pacote de campo. Somente leitura no dispositivo: nunca editadas localmente, apenas consumidas para exibicao no mapa e vinculacao com unidades.

| Coluna | Tipo WatermelonDB | Obrigatoria | Descricao |
|--------|-------------------|-------------|-----------|
| server_id | string | sim | ID do servidor. Sempre preenchido pois vem do pull. |
| tenant_id | string | sim | Municipio. |
| code | string | sim | Codigo da comunidade. |
| name | string | sim | Nome da comunidade. |
| community_type | string | sim | URBANA, RURAL, QUILOMBOLA, RIBEIRINHA. |
| boundary_geojson | string | nao | Perimetro em formato GeoJSON serializado como texto. |
| municipality | string | sim | Municipio. |
| state | string | sim | UF. |

---

## teams

Equipes baixadas do servidor. Somente leitura no dispositivo.

| Coluna | Tipo WatermelonDB | Obrigatoria | Descricao |
|--------|-------------------|-------------|-----------|
| server_id | string | sim | ID do servidor. |
| tenant_id | string | sim | Municipio. |
| name | string | sim | Nome da equipe. |

---

## team_members

Membros de equipe baixados do servidor. Somente leitura.

| Coluna | Tipo WatermelonDB | Obrigatoria | Descricao |
|--------|-------------------|-------------|-----------|
| server_id | string | sim | ID do servidor. |
| team_id | string | sim | Referencia para team local. |
| account_id | string | sim | UUID do usuario no Keycloak. |
| role | string | sim | COORDINATOR ou CADASTRATOR. |

---

## Estrategia de Migration

O schema do WatermelonDB e versionado de forma incremental. Cada migration step descreve a alteracao: adicao de coluna, criacao de tabela nova ou renomeacao. O adapter SQLite executa as migrations automaticamente ao detectar que a versao do schema no dispositivo e menor que a versao definida no codigo. Migrations sao irreversiveis: nao ha rollback. Se uma migration falhar, o app exibe mensagem solicitando reinstalacao.

O adapter SQLite e configurado com JSI habilitado para acesso sincrono ao banco sem overhead da bridge JavaScript, WAL mode para melhor concorrencia entre leitura e escrita, e batch size padrao para operacoes em lote.

Retention policy: registros locais mais antigos que 6 meses e ja sincronizados com sucesso sao elegíveis para limpeza automatica, mantendo o banco compacto. Registros nao sincronizados nunca sao limpos independente da idade.
