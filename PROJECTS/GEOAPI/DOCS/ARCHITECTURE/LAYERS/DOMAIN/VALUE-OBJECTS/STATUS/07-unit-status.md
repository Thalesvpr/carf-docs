---
type: leaf
status: review
updated: 2026-02-08
---

# UnitStatus

Value object enum representando os estados do workflow de cadastro e aprovacao de unidades habitacionais, controlando transicoes validas de status e permissoes de edicao em cada estagio do processo de regularizacao. No banco de dados, corresponde ao campo units.status (varchar(30)) com CHECK constraint.

As transicoes seguem fluxo definido onde cada estado determina quais operacoes sao permitidas e quais papeis (Role) podem executar acoes naquele estagio.

## Valores Permitidos

| Valor | Descricao |
| --- | --- |
| DRAFT | Rascunho inicial criado por tecnico de campo. Editavel livremente. |
| PENDING_ANALYSIS | Submetido para analise tecnica. Nao editavel por campo. |
| IN_REVIEW | Em revisao por analista. Pode solicitar correcoes. |
| APPROVED | Aprovado para emissao de certidao. Imutavel exceto por administradores. |
| REJECTED | Rejeitado com justificativa. Retorna para DRAFT para correcao. |
| REQUIRES_CHANGES | Analista solicitou mudancas especificas antes de prosseguir. |

## Transicoes Validas

| De | Para | Condicao |
| --- | --- | --- |
| DRAFT | PENDING_ANALYSIS | Documentacao minima preenchida. |
| PENDING_ANALYSIS | IN_REVIEW | Analista assumiu a analise. |
| IN_REVIEW | APPROVED | Parecer tecnico favoravel. |
| IN_REVIEW | REJECTED | Parecer tecnico desfavoravel com justificativa. |
| IN_REVIEW | REQUIRES_CHANGES | Correcoes necessarias identificadas. |
| REJECTED | DRAFT | Apos correcao pelo requerente. |
| REQUIRES_CHANGES | DRAFT | Apos correcao pelo requerente. |

## Metodos Principais

| Metodo | Retorno | Descricao |
| --- | --- | --- |
| CanEdit() | bool | Verifica se status permite edicao. |
| CanSubmit() | bool | Verifica se pode avancar para analise. |
| CanApprove() | bool | Verifica se esta em estado aprovavel. |
| ValidateTransition(UnitStatus) | void | Lanca exception se transicao invalida. |

Usado em Unit para controlar workflow com domain event UnitStatusChangedEvent disparado em cada transicao, integrando com sistema de permissoes via Role (COORDINATOR e CADASTRATOR editam DRAFT, ANALYST analisa PENDING_ANALYSIS).
