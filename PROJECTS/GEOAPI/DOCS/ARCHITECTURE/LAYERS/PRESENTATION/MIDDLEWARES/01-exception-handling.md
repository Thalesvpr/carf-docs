---
type: leaf
status: active
updated: 2026-02-07
---

# Exception Handling Middleware

O ExceptionHandlingMiddleware intercepta todas as excecoes nao tratadas na pipeline HTTP da GEOAPI e as converte em respostas padronizadas no formato ProblemDetails (RFC 7807) com content type application/problem+json.

## Mapeamento de Excecoes

O middleware utiliza pattern matching para mapear cada tipo de excecao ao status HTTP correspondente.

| Tipo de Excecao | Status HTTP | Titulo |
|----------------|-------------|--------|
| ValidationException | 400 Bad Request | Validation Error |
| DomainException | 400 Bad Request | Domain Error |
| NotFoundException | 404 Not Found | Not Found |
| UnauthorizedException | 401 Unauthorized | Unauthorized |
| ForbiddenException | 403 Forbidden | Forbidden |
| ConflictException | 409 Conflict | Conflict |
| Qualquer outra | 500 Internal Server Error | Internal Server Error |

## Comportamento

O metodo InvokeAsync envolve a chamada ao proximo middleware em um bloco try-catch. Quando uma excecao e capturada, o metodo HandleExceptionAsync extrai o correlationId do TraceIdentifier da requisicao. Erros com status 500 ou acima sao logados como Error com a excecao completa. Erros abaixo de 500 sao logados como Warning apenas com a mensagem. O correlationId e adicionado as extensions do ProblemDetails para rastreabilidade. Para ValidationException, os erros de campo sao incluidos na extensao "errors" do ProblemDetails. Mensagens internas de erro nunca sao expostas em respostas 500, que sempre retornam "An unexpected error occurred".

## Registro

O middleware e o primeiro componente do pipeline HTTP, registrado em Program.cs via UseMiddleware antes de Swagger, CORS e autenticacao.
