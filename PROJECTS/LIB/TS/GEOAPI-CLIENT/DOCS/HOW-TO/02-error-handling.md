---
type: leaf
status: review
updated: 2026-02-07
---

# Error Handling - Guia Pratico

Guia pratico para tratamento de erros ao usar @carf/geoapi-client.

## Hierarquia de Erros

Todos os erros da API herdam de ApiError. Os tipos especificos sao: ValidationError (400, dados invalidos), UnauthorizedError (401, nao autenticado), ForbiddenError (403, sem permissao), NotFoundError (404, nao encontrado), ConflictError (409, conflito como duplicado ou versao), TooManyRequestsError (429, rate limit), ServerError (5xx, erro do servidor), NetworkError (sem conexao) e TimeoutError (timeout excedido).

## Tratamento Basico

O padrao basico envolve try-catch com verificacao instanceof ApiError, acessando error.status (codigo HTTP), error.code (codigo do backend) e error.details (objeto com informacoes extras).

## Tratamento por Tipo

**ValidationError (400):** contem validationErrors, um mapa de campo para lista de mensagens. Uso tipico: iterar pelas entradas e exibir erros inline no formulario via setFieldError.

**UnauthorizedError (401):** indica token expirado ou invalido. Uso tipico: tentar refresh do token e refazer a requisicao; se o refresh falhar, redirecionar para login.

**ForbiddenError (403):** usuario sem permissao para a acao. Uso tipico: exibir toast informando que nao ha permissao para a operacao.

**NotFoundError (404):** recurso nao existe. Uso tipico: exibir toast e redirecionar para a listagem correspondente.

**ConflictError (409):** conflito de dados. Uso tipico: verificar error.code para distinguir entre VERSION_CONFLICT (pedir atualizacao da pagina) e DUPLICATE_CODE (exibir erro no campo do formulario).

**TooManyRequestsError (429):** rate limit atingido. Contem retryAfter indicando segundos para aguardar. Uso tipico: exibir aviso e agendar retry automatico apos o tempo indicado.

**ServerError (5xx):** erro interno do servidor. Uso tipico: exibir toast generico e logar requestId para suporte.

**NetworkError:** sem conexao com servidor. Uso tipico: exibir toast pedindo verificacao da internet.

**TimeoutError:** requisicao excedeu timeout. Uso tipico: exibir toast pedindo nova tentativa.

## Tratamento Centralizado

### Handler Global

Uma funcao handleApiError centralizada recebe o erro e despacha conforme o tipo: ValidationError nao exibe toast (erros ficam no formulario), UnauthorizedError faz logout e redireciona, ForbiddenError exibe toast de permissao, NotFoundError exibe toast de recurso nao encontrado, ConflictError pede atualizacao, TooManyRequestsError pede aguardar, ServerError e NetworkError exibem mensagens genericas, e demais erros mostram error.message.

### React Error Boundary

O componente ApiErrorBoundary (class component React) captura erros da arvore de componentes via getDerivedStateFromError e componentDidCatch, logando status, code, message e requestId para erros ApiError. Renderiza um fallback customizavel ou um DefaultErrorFallback.

### React Query

O QueryClient e configurado com retry customizado que nao retenta erros de cliente (status abaixo de 500) e retenta ate 3 vezes em outros erros. A opcao global de mutations configura onError para redirecionar ao login em caso de UnauthorizedError.

## Logging de Erros

A funcao logApiError coleta status, code, message, requestId, timestamp e URL atual. Em desenvolvimento, loga no console. Em producao, envia para servico de monitoramento (Sentry) com tags errorCode e statusCode.

## Boas Praticas

Seja especifico no tratamento, usando instanceof para distinguir tipos ao inves de tratar todos igualmente. Nunca silencie erros sem ao menos logar. Use requestId para suporte, exibindo-o ao usuario. Retente apenas em erros transientes (ServerError, NetworkError), nunca em erros de cliente.
