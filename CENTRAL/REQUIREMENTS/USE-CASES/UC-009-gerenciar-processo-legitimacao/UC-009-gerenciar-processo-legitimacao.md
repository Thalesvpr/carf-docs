---
id: UC-009
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-009: Gerenciar Processo de Legitimacao Fundiaria

## Atores

- Primario: ANALYST, MANAGER
- Secundario: Sistema de notificacao, Servico de geracao de documentos

## Pre-condicoes

- Usuario autenticado com permissao de legitimacao
- Unidade com status Approved
- Titular principal vinculado a unidade

## Fluxo Principal

1. Usuario acessa detalhes da unidade
2. Sistema exibe secao Legitimacao Fundiaria
3. Usuario clica em Iniciar Processo de Legitimacao
4. Sistema exibe formulario com campos do processo
5. Usuario preenche numero do processo, tipo e modalidade
6. Usuario seleciona beneficiario principal dentre titulares
7. Usuario informa data de protocolo e orgao responsavel
8. Usuario clica Criar Processo
9. Sistema valida dados e cria processo com status Em Analise
10. Sistema exibe checklist de documentos obrigatorios
11. Usuario faz upload dos documentos necessarios
12. Sistema valida e marca itens como concluidos
13. Usuario clica Submeter para Aprovacao
14. Sistema atualiza status e notifica MANAGER
15. MANAGER acessa lista de processos pendentes
16. MANAGER revisa documentacao e dados do processo
17. MANAGER decide aprovar, solicitar correcoes ou indeferir
18. Se aprovado, sistema habilita geracao do Termo
19. Usuario gera PDF do Termo de Legitimacao
20. Usuario baixa termo para impressao e registro

## Fluxos Alternativos

- FA-001: Processo coletivo (multiplas unidades)
- FA-002: Assinatura digital do termo

## Fluxos de Excecao

- FE-001: Unidade sem titular principal
- FE-002: Documentacao incompleta
- FE-003: Processo indeferido

## Pos-condicoes

- Processo de legitimacao criado e acompanhado
- Documentacao anexada e validada
- Termo gerado apos aprovacao
