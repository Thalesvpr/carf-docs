---
id: UC-006
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-24
---

# UC-006: Gerar Relatorio de Comunidade

> **Contexto no Workflow:** UC suplementar pos-workflow. Relatorios sao gerados apos os dados terem sido coletados em campo (PARTE 3) e sincronizados. Ver [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/README.md).

## Atores

- Primario: MANAGER, ADMIN
- Secundario: Sistema de filas, Servico de notificacao

## Pre-condicoes

- Usuario autenticado com permissao para relatorios
- Comunidade selecionada possui dados cadastrados

## Fluxo Principal

1. Usuario acessa menu Relatorios
2. Sistema exibe tipos de relatorios disponiveis
3. Usuario seleciona Relatorio de Comunidade
4. Sistema exibe formulario de parametros
5. Usuario seleciona comunidade
6. Usuario define periodo de analise
7. Usuario marca secoes a incluir
8. Usuario seleciona formato de saida (PDF ou Excel)
9. Usuario clica Gerar Relatorio
10. Sistema valida parametros
11. Sistema inicia geracao assincrona
12. Sistema exibe mensagem de processamento
13. Sistema processa dados e gera arquivo
14. Sistema notifica usuario quando pronto
15. Usuario baixa arquivo gerado

## Fluxos Alternativos

- FA-001: Geracao rapida (poucos dados)
- FA-002: Agendar geracao recorrente

## Fluxos de Excecao

- FE-001: Timeout de geracao
- FE-002: Dados insuficientes
- FE-003: Erro ao gerar PDF

## Pos-condicoes

- Relatorio gerado e disponivel para download
- Arquivo armazenado temporariamente no servidor
- Notificacao enviada ao usuario
