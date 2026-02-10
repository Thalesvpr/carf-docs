---
type: leaf
status: review
updated: 2026-02-07
---

# Legitimation API - Criacao e Workflow

## Metodo create

Cria novo processo de legitimacao. Recebe um objeto CreateLegitimationDTO e retorna o Legitimation criado.

### Parametros de Criacao

| Campo | Tipo | Obrigatorio | Descricao |
|:------|:-----|:------------|:----------|
| unitId | string | Sim | UUID da unidade a legitimar |
| holderId | string | Sim | UUID do posseiro principal |
| reurbType | string | Sim | REURB_S ou REURB_E |
| requestDate | Date | Nao | Data do requerimento |
| protocolNumber | string | Nao | Numero do protocolo |
| observations | string | Nao | Observacoes gerais |
| documents | array | Nao | Documentos iniciais com type e fileId |

### Regras de Validacao

A unidade informada em unitId deve existir e nao pode ter outro processo ativo. O posseiro em holderId deve estar vinculado a unidade. O campo reurbType deve ser compativel com o tipo da comunidade a que pertence a unidade.

## Metodo executeAction

Executa acao de workflow no processo. Recebe o ID do processo e um objeto WorkflowActionDTO contendo a acao, observacoes opcionais e documentos opcionais com type e fileId.

### Acoes Disponiveis

| Acao | Descricao |
|:-----|:----------|
| SUBMIT | Submeter para analise |
| APPROVE | Aprovar o processo |
| REJECT | Rejeitar o processo |
| REQUEST_DOCS | Solicitar documentos adicionais |
| RETURN | Devolver para correcao |
| CANCEL | Cancelar o processo |
| REOPEN | Reabrir processo cancelado ou rejeitado |

### Fluxo de Status

O processo inicia em DRAFT. Ao executar SUBMIT, transiciona para PENDING_ANALYSIS. A partir de PENDING_ANALYSIS, tres caminhos sao possiveis: APPROVE leva a APPROVED, REQUEST_DOCS leva a PENDING_DOCUMENTS e REJECT leva a REJECTED. Quando em PENDING_DOCUMENTS, executar SUBMIT retorna o processo para PENDING_ANALYSIS. As acoes CANCEL e REOPEN permitem cancelar e reabrir processos respectivamente. A cada execucao de acao, o sistema registra automaticamente o historico com usuario, data, status anterior e novo status.
