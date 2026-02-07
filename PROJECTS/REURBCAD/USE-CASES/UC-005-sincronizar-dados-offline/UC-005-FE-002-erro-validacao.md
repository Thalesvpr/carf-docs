---
id: UC-005-FE-002
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-005-FE-002: Erro de Validacao no Servidor

Fluxo de excecao do UC-005 quando servidor rejeita dados por erro de validacao.

## Condicao

Na fase PUSH do UC-005, servidor detecta violacao de regras de negocio nos dados enviados.

## Fluxo

1. Servidor valida dados recebidos
2. Servidor detecta erro de validacao
3. Servidor retorna erro com detalhes
4. App exibe modal com lista de erros
5. App destaca campos problematicos
6. Usuario de campo (FIELD_COORDINATOR ou FIELD_CADASTRATOR) edita e corrige dados
7. Usuario de campo retenta sincronizacao

## Validacoes que Podem Falhar

- CPF/CNPJ invalido
- Geometria invalida
- Soma de percentuais excede 100%
- Campos obrigatorios vazios

## Retorno

Dados permanecem pendentes. Usuario de campo (FIELD_COORDINATOR ou FIELD_CADASTRATOR) corrige e retenta sincronizacao.

## Pos-condicoes

- Erros exibidos com mensagens claras
- Formulario de edicao pre-carregado para correcao
