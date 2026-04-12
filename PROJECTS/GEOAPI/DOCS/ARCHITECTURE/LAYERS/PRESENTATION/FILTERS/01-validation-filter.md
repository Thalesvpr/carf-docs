---
type: leaf
status: active
updated: 2026-02-07
---

# Validation Filter

A GEOAPI utiliza duas camadas de validacao: um action filter para ModelState e um pipeline behavior do MediatR para validacao de commands.

## ValidationFilter

A classe ValidationFilter implementa IAsyncActionFilter e intercepta todas as requisicoes antes da execucao do action method. Se o ModelState estiver invalido, o filtro monta um ValidationProblemDetails com titulo "Validation Failed", status 400 e a lista de erros agrupados por campo. A resposta e retornada como BadRequest sem executar o controller. Se o ModelState for valido, a execucao prossegue normalmente.

## Registro Global

O filtro e adicionado globalmente na configuracao de controllers em Program.cs. A validacao automatica do ASP.NET e desabilitada via ApiBehaviorOptions com SuppressModelStateInvalidFilter configurado como verdadeiro, delegando todo o controle ao filtro customizado.

## Integracao com FluentValidation

Os validators do FluentValidation sao registrados automaticamente por assembly scanning a partir do CreateUnitRequestValidator. A classe ValidationBehavior implementa IPipelineBehavior do MediatR, servindo como segundo nivel de validacao. Para cada request que chega ao pipeline, o behavior executa todos os validators registrados para aquele tipo, coleta as falhas e, se houver alguma, lanca ValidationException antes de o handler ser invocado.

| Camada | Componente | Momento | Alvo |
|--------|-----------|---------|------|
| HTTP | ValidationFilter | Antes do controller | ModelState (DTOs de request) |
| MediatR | ValidationBehavior | Antes do handler | Commands e Queries |
