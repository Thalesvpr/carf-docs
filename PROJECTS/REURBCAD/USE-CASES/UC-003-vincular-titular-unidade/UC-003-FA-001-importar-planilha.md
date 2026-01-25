---
id: UC-003-FA-001
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-003-FA-001: Importar Titulares de Planilha

Fluxo alternativo do UC-003 para importar multiplos titulares via arquivo Excel ou CSV.

## Condicao

No passo 3 do UC-003, usuario possui lista extensa de titulares proveniente de levantamento externo.

## Fluxo

1. Usuario clica em Acoes em Lote e seleciona Importar Planilha
2. Sistema exibe modal com instrucoes e link para template
3. Usuario baixa template e preenche com dados dos titulares
4. Usuario faz upload do arquivo preenchido
5. Sistema valida estrutura e colunas obrigatorias
6. Sistema valida dados linha por linha acumulando erros
7. Sistema exibe preview com status por linha (valido, erro, duplicado)
8. Usuario revisa e corrige erros inline ou remove linhas problematicas
9. Usuario confirma importacao
10. Sistema processa em lote criando titulares e vinculos
11. Sistema registra operacao na timeline
12. Sistema exibe resumo com estatisticas

## Validacoes

- CPF/CNPJ com digitos verificadores validos
- Nome com minimo de palavras
- Tipo de relacionamento pertence ao enum permitido
- Percentual entre 0 e 100
- Duplicacao dentro da planilha e contra banco de dados

## Retorno

Lista de titulares atualizada com todos importados. Timeline registra operacao em lote.

## Pos-condicoes

- Titulares criados ou vinculados conforme planilha
- Relatorio de erros disponivel para download se houver falhas
