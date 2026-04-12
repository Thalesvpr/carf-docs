---
type: leaf
status: review
updated: 2026-02-07
---

# File Upload - Guia Pratico

Guia para upload de arquivos usando a Documents API do @carf/geoapi-client.

## Upload Basico

O upload utiliza api.documents.upload passando o arquivo, um objeto de metadados com type (tipo do documento, por exemplo ID_DOCUMENT), entityType (HOLDER, UNIT ou COMMUNITY) e entityId (UUID da entidade associada). O retorno contem o id do documento criado.

## Upload com Progresso

O terceiro parametro de api.documents.upload aceita um callback onProgress que recebe um objeto com percentage (0 a 100), loaded (bytes enviados) e total (bytes totais). Uso tipico: atualizar uma barra de progresso na interface.

## Componente de Upload Simples

Um componente React de upload mantem estados de uploading (boolean), progress (numero de 0 a 100) e error (string ou null). Ao selecionar arquivo via input file, reseta os estados, marca uploading como verdadeiro, chama api.documents.upload com o callback de progresso e trata erros. O input aceita extensoes .pdf, .jpg, .jpeg e .png e fica desabilitado durante upload. Uma barra de progresso aparece durante o envio e mensagens de erro sao exibidas quando ocorrem.

As props do componente sao:

| Prop | Tipo | Descricao |
|:-----|:-----|:----------|
| entityType | UNIT ou HOLDER ou COMMUNITY | Tipo da entidade associada |
| entityId | string | UUID da entidade |
| documentType | DocumentType | Tipo do documento |
| onSuccess | funcao opcional | Callback com o documento criado |

## Upload com Drag and Drop

O componente de drag-and-drop usa a biblioteca react-dropzone com useDropzone. Mantem uma lista de UploadFile, cada um com file, id (UUID gerado), status (pending, uploading, success ou error), progress e opcionalmente error e document. Ao soltar arquivos, adiciona-os a lista e inicia upload individual de cada um. A area de drop aceita image/* (.jpg, .jpeg, .png) e application/pdf (.pdf) com tamanho maximo de 10 MB. Uma lista abaixo da area mostra o status de cada arquivo com barra de progresso durante envio.

## Upload com Cancelamento

O cancelamento usa CancelToken do geoapi-client. Cria-se um CancelToken.source, passa-se o token como opcao do upload e chama-se source.cancel quando o usuario solicita cancelamento. Erros de cancelamento sao detectados via CancelToken.isCancel e tratados silenciosamente. O botao de cancelar fica habilitado apenas durante o upload.

## Validacao de Arquivos

A validacao client-side verifica tres criterios antes do envio: tamanho maximo de 10 MB, tipo MIME permitido (image/jpeg, image/png, application/pdf) e extensao permitida (.jpg, .jpeg, .png, .pdf). A funcao de validacao retorna null se o arquivo e valido ou uma string de erro descritiva.

## Compressao de Imagens

Para imagens maiores que 1 MB, a biblioteca browser-image-compression comprime antes do envio, configurada com maxSizeMB de 1, maxWidthOrHeight de 1920 pixels e useWebWorker ativado.

## Multiplos Arquivos

O upload de multiplos arquivos usa Promise.allSettled para enviar todos em paralelo, separando os resultados entre fulfilled (sucesso) e rejected (falha) para exibir contagem de enviados e falhados.

## Tratamento de Erros

Erros de upload incluem: ValidationError (arquivo invalido), status 413 (payload too large, exibir limite de 10 MB), status 415 (unsupported media type) e NetworkError (erro de conexao).
