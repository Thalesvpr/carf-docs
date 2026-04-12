---
type: standard
status: review
updated: 2026-01-22
---

# STD-007: Estilo de Codigo

## Regra

Backend .NET usa Rider/ReSharper code style com PascalCase para tipos e membros publicos, camelCase para variaveis locais. Frontend TypeScript usa Prettier e ESLint com configuracao padrao do projeto. Nomes de arquivos em kebab-case. Imports organizados alfabeticamente com separacao entre externos e internos.

## Justificativa

Formatacao consistente elimina discussoes de estilo em code review e facilita leitura de codigo por qualquer membro da equipe.

## Aplicacao

Aplica-se a todo codigo-fonte em PROJECTS/. Pre-commit hooks formatam automaticamente. CI falha se linter reportar erros. Excecao para arquivos gerados automaticamente como migrations e clients OpenAPI.
