---
type: leaf
status: review
updated: 2026-02-07
---

# Reports API - Status, Download e Formatos

## Estrutura do ReportJob

O objeto ReportJob e retornado por todos os metodos de solicitacao de exportacao e pelo metodo getStatus.

| Campo | Tipo | Descricao |
|:------|:-----|:----------|
| id | string | UUID do job para consultas |
| status | ReportJobStatus | PENDING, PROCESSING, COMPLETED ou FAILED |
| format | ReportFormat | excel, pdf ou csv |
| createdAt | Date | Data de criacao do job |
| completedAt | Date (opcional) | Data de conclusao |
| downloadUrl | string (opcional) | Disponivel quando status e COMPLETED |
| error | string (opcional) | Mensagem de erro quando status e FAILED |
| progress | number (opcional) | Percentual de progresso de 0 a 100 |

## Metodo getStatus

Verifica o status de um job de geracao de relatorio. Recebe o jobId como string e retorna o objeto ReportJob atualizado. O cliente deve fazer polling deste metodo ate que o status seja COMPLETED ou FAILED.

## Metodo download

Faz download do relatorio gerado. Recebe o jobId e opcoes opcionais de progresso e cancelamento. Retorna um Blob com o conteudo do arquivo. Lanca NotFoundError (404) se o job nao existe e BadRequestError (400) se o job ainda nao completou.

## Helper waitForCompletion

Aguarda conclusao do job com polling automatico. Recebe o jobId e opcoes opcionais.

| Opcao | Tipo | Padrao | Descricao |
|:------|:-----|:-------|:----------|
| pollingInterval | number | 2000 | Intervalo entre consultas em milissegundos |
| timeout | number | 300000 | Timeout total em milissegundos (5 minutos) |
| onProgress | funcao | nenhum | Callback chamado a cada verificacao com o ReportJob |

Este helper encapsula o loop de polling, retornando o ReportJob quando atingir COMPLETED ou lancando erro em caso de FAILED ou timeout.

## Helper exportAndDownload

Combina solicitacao, aguardo e download em uma unica chamada. Recebe o tipo de relatorio (units, holders ou communityStats), os parametros de filtro, o formato desejado e opcoes opcionais. Retorna diretamente o Blob do arquivo gerado, simplificando o fluxo para o consumidor.

## Formatos de Saida

| Formato | Extensao | Caracteristicas |
|:--------|:---------|:----------------|
| Excel | .xlsx | Formatacao automatica de colunas, headers em negrito, tabela filtrada, multiplas abas quando aplicavel |
| PDF | .pdf | Cabecalho com logo e data, tabelas formatadas, graficos para estatisticas, paginacao automatica |
| CSV | .csv | UTF-8 com BOM para compatibilidade com Excel, separador ponto-e-virgula, ideal para importacao em outros sistemas |
