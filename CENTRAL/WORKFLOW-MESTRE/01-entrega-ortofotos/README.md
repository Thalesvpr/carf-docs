---
type: workflow
status: approved
updated: 2026-01-25
part: 1
---

# PARTE 1: Entrega e Processamento de Ortofotos

Fluxo de entrega de ortofotos desde o Analista de Drone ate o armazenamento em bucket segregado por TENANT.

## Atores

| Ator | Papel |
|------|-------|
| Analista de Drone | Responsavel por publicar/entregar ortofotos prontas |
| Backend (GEOAPI) | Recebe, processa e armazena ortofotos |
| Keycloak | Autentica o Analista de Drone |
| Bucket (S3/MinIO) | Armazena ortofotos originais e versoes reduzidas |

## Pre-condicoes

- Analista de Drone possui credenciais validas no Keycloak
- Analista de Drone esta designado a um TENANT
- Ortofoto esta pronta para envio (mosaico gerado a partir de imagens de drone)
- Backend esta operacional e conectado ao bucket

## Passos

| Passo | Descricao | Documento |
|-------|-----------|-----------|
| 1 | Autenticacao | [passo-01-autenticacao.md](./passo-01-autenticacao.md) |
| 2 | Upload da Ortofoto | [passo-02-upload.md](./passo-02-upload.md) |
| 3 | Processamento pelo Backend | [passo-03-processamento.md](./passo-03-processamento.md) |
| 4 | Armazenamento em Bucket | [passo-04-armazenamento.md](./passo-04-armazenamento.md) |

## Pos-condicoes

- Ortofoto original armazenada no bucket
- Versao reduzida/otimizada disponivel
- Metadados registrados no banco de dados
- Ortofoto associada ao TENANT correto
- Analistas do mesmo TENANT podem acessar a ortofoto (PARTE 2)

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| RN-01 | Autenticacao via Keycloak e OBRIGATORIA |
| RN-02 | Backend SEMPRE reduz tamanho da ortofoto |
| RN-03 | Ortofoto SEMPRE e salva em bucket (S3/MinIO) |
| RN-04 | Ortofoto SEMPRE e associada ao TENANT do analista |
| RN-05 | Apenas usuarios do mesmo TENANT podem acessar a ortofoto |

## Integracao com Sistemas

| Sistema | Responsabilidade |
|---------|------------------|
| Portal Upload | Interface para envio de ortofotos |
| Keycloak | Autenticacao OAuth2/OIDC |
| GEOAPI | Processamento e registro |
| S3/MinIO | Armazenamento de objetos |

## Proxima Parte

Apos o armazenamento, a ortofoto fica disponivel para o Analista (Plugin QGIS) na PARTE 2: Georreferenciamento.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (4)

| Documento | Status |
|-----------|--------|
| [Passo 1: Autenticacao](./passo-01-autenticacao.md) | ⚠ |
| [Passo 2: Upload da Ortofoto](./passo-02-upload.md) | ⚠ |
| [Passo 3: Processamento pelo Backend](./passo-03-processamento.md) | ⚠ |
| [Passo 4: Armazenamento em Bucket por TENANT](./passo-04-armazenamento.md) | ⚠ |

<!-- CARF-INDEX-END -->
