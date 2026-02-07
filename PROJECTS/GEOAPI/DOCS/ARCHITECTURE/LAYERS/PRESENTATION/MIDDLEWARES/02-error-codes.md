---
type: leaf
status: approved
updated: 2026-02-07
---

# Error Codes

Catalogo completo de codigos de erro retornados pela GEOAPI. Cada erro segue o formato RFC 7807 ProblemDetails com o campo extensions.errorCode contendo o codigo maquina da tabela abaixo e extensions.fields contendo array de erros por campo quando a resposta e resultado de falha de validacao.

## Tabela de Codigos

| Codigo | HTTP | Descricao | Situacao |
|--------|------|-----------|----------|
| VALIDATION_ERROR | 400 | Campos invalidos na requisicao. | Um ou mais campos do request body falharam na validacao do FluentValidation. O campo extensions.fields contem array com objetos contendo field (nome do campo), message (mensagem legivel) e code (sub-codigo opcional). |
| CPF_INVALID | 400 | CPF com digitos verificadores incorretos. | O valor informado para CPF nao passa no algoritmo Mod11 de verificacao dos dois digitos finais. O campo deve conter exatamente 11 digitos numericos. |
| CPF_EXISTS | 409 | CPF ja cadastrado neste municipio. | Tentativa de criar holder com CPF que ja existe para o mesmo tenant_id. Violacao da constraint UNIQUE em (tenant_id, cpf). |
| UNIT_LOCKED | 403 | Unidade em status que nao permite edicao. | Tentativa de alterar campos de uma unidade cujo status e APPROVED, REJECTED, PENDING_ANALYSIS ou IN_REVIEW. Edicao so e permitida em DRAFT e REQUIRES_CHANGES. |
| NOT_DRAFT | 400 | Operacao requer que a unidade esteja em DRAFT. | Tentativa de excluir uma unidade que nao esta no status DRAFT. Exclusao so e permitida para rascunhos. |
| NO_HOLDER | 400 | Nenhum titular vinculado a unidade. | Tentativa de submeter unidade para analise (acao submit) sem ter ao menos um titular vinculado com is_primary true na tabela unit_holders. |
| PERCENTAGE_EXCEEDED | 400 | Soma de percentuais de propriedade excede 100. | Tentativa de vincular titular como PROPRIETARIO com ownership_percentage que, somado aos percentuais existentes para a mesma unidade, ultrapassa 100 porcento. |
| MULTIPLE_PRIMARY | 400 | Ja existe um titular principal para esta unidade. | Tentativa de vincular ou atualizar titular com is_primary true quando ja existe outro titular marcado como principal na mesma unidade. Apenas um titular pode ser o principal. |
| OVERLAP_DETECTED | 422 | Geometria da unidade sobrepoe outra unidade existente. | Deteccao via PostGIS ST_Intersects de que o boundary informado para a unidade se sobrepoe ao boundary de outra unidade ativa no mesmo tenant. Retornado como aviso, nao bloqueia a criacao. |
| AREA_EXCEEDED | 400 | Area calculada fora dos limites permitidos. | A area resultante do poligono informado e menor que 10 metros quadrados ou maior que 100.000 metros quadrados, indicando possivel erro de georreferenciamento. |
| GEOMETRY_INVALID | 400 | Poligono geometricamente invalido. | O boundary informado apresenta auto-intersecao, nao esta fechado (primeiro ponto diferente do ultimo) ou possui menos de 4 pontos. Validacao via PostGIS ST_IsValid. |
| OUTSIDE_BOUNDARY | 400 | Unidade fora dos limites da comunidade. | O centroide da unidade nao esta contido dentro do boundary da comunidade vinculada. Validacao via PostGIS ST_Contains. |
| NOT_AUTHORIZED | 403 | Role insuficiente para esta operacao. | O usuario autenticado nao possui a role necessaria para executar a operacao solicitada conforme a matriz de permissoes RBAC. |
| TENANT_MISMATCH | 403 | Recurso pertence a outro municipio. | Tentativa de acessar ou modificar recurso cujo tenant_id nao corresponde ao tenant do usuario autenticado. Indica possivel tentativa de bypass do isolamento RLS. |
| TOKEN_EXPIRED | 401 | Token JWT expirado. | O Bearer token enviado no header Authorization expirou conforme o claim exp do JWT Keycloak. O client deve renovar o token via refresh_token e tentar novamente. |
| SYNC_CONFLICT | 409 | Versao do registro desatualizada. | A versao enviada pelo client no campo version nao corresponde a versao atual no banco, indicando que outro usuario ou dispositivo modificou o registro desde a ultima leitura. O client deve recarregar os dados e reaplicar suas alteracoes. |
| FILE_TOO_LARGE | 413 | Arquivo excede o limite de 50MB. | O arquivo enviado no upload excede o tamanho maximo permitido de 50 megabytes. |
| UNSUPPORTED_FORMAT | 415 | Tipo de arquivo nao permitido. | O MIME type do arquivo enviado nao esta na lista de tipos aceitos: image/jpeg, image/png, image/webp, application/pdf para documentos, ou image/tiff para ortofotos. |
| PROCESSING_FAILED | 500 | Falha no processamento de ortofoto. | Erro interno durante processamento GDAL da ortofoto. O campo detail contem a mensagem de erro especifica. O usuario deve verificar o arquivo de origem e tentar novamente. |
| DUPLICATE | 409 | Vinculo duplicado entre titular e unidade. | Tentativa de criar registro em unit_holders com par (unit_id, holder_id) que ja existe. Cada titular so pode estar vinculado uma vez a cada unidade. |
| HAS_UNITS | 400 | Titular vinculado a unidades ativas. | Tentativa de excluir titular que ainda possui vinculos ativos em unit_holders. O titular deve ser desvinculado de todas as unidades antes da exclusao. |
| QUOTA_EXCEEDED | 429 | Limite de requisicoes excedido. | O numero de requisicoes por minuto excedeu o limite configurado para o usuario ou API key. O header Retry-After indica quantos segundos aguardar antes da proxima tentativa. |

## Formato de Resposta

Todas as respostas de erro seguem a especificacao RFC 7807 Problem Details for HTTP APIs. O Content-Type da resposta e application/problem+json. Os campos obrigatorios sao type contendo uma URI que identifica o tipo do erro (por exemplo /errors/cpf-invalid), title contendo uma descricao curta legivel, status contendo o codigo HTTP numerico e detail contendo uma mensagem legivel com contexto especifico da ocorrencia.

O campo extensions.errorCode contem o codigo da tabela acima, permitindo que clients implementem tratamento programatico de erros sem depender de parsing de mensagens em portugues. O campo extensions.fields e um array presente apenas quando errorCode e VALIDATION_ERROR, contendo um objeto por campo invalido com as propriedades field (caminho do campo, por exemplo "address.street"), message (mensagem legivel) e code (sub-codigo opcional como "required" ou "minLength").

## Internacionalizacao

Todas as mensagens nos campos title e detail sao retornadas em portugues brasileiro pois o sistema atende exclusivamente usuarios brasileiros. O campo errorCode e sempre em ingles maiusculo com underscores para uso programatico.
