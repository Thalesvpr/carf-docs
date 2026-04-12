---
type: leaf
status: review
updated: 2026-02-07
---

# Legitimation API - Historico e Documentos

## Metodo getHistory

Obtem o historico de acoes executadas em um processo de legitimacao. Recebe o ID do processo e retorna um array de LegitimationHistory.

### Estrutura de LegitimationHistory

| Campo | Tipo | Descricao |
|:------|:-----|:----------|
| id | string | UUID do registro |
| legitimationId | string | UUID do processo |
| action | WorkflowAction | Acao executada |
| fromStatus | LegitimationStatus | Status anterior |
| toStatus | LegitimationStatus | Novo status |
| observations | string (opcional) | Observacoes da acao |
| performedBy | objeto | Contem id e name do usuario |
| performedAt | Date | Data e hora da execucao |
| documents | array (opcional) | Documentos anexados na acao |

O historico permite rastrear todas as transicoes de status do processo, incluindo quem executou cada acao e quando. Cada entrada registra o status de origem e destino da transicao.

## Metodo getDocuments

Lista todos os documentos anexados ao processo de legitimacao. Recebe o ID do processo e retorna um array de Document.

## Metodo addDocument

Anexa um novo documento ao processo. Recebe o ID do processo e um objeto com os campos type, fileId e description opcional. O fileId referencia um arquivo previamente enviado via Documents API.

### Tipos de Documento

| Tipo | Descricao |
|:-----|:----------|
| ID_DOCUMENT | RG ou CNH |
| CPF | Cadastro de Pessoa Fisica |
| PROOF_OF_RESIDENCE | Comprovante de residencia |
| MARRIAGE_CERTIFICATE | Certidao de casamento |
| PROPERTY_TAX | IPTU |
| POWER_OF_ATTORNEY | Procuracao |
| TECHNICAL_REPORT | Laudo tecnico |
| PLANT | Planta ou croqui |
| AERIAL_PHOTO | Foto aerea |
| OTHER | Outro tipo |

## Metodo downloadCertificate

Faz download do certificado de legitimacao emitido. Recebe o ID do processo e retorna um Blob com o arquivo PDF. O endpoint correspondente e GET /api/legitimation/{id}/certificate. Lanca NotFoundError (404) se o processo nao existe ou o certificado ainda nao foi emitido, e ForbiddenError (403) se o usuario nao tem permissao.
