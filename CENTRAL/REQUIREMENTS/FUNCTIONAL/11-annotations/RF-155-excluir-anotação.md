---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-155: Excluir Anotacao

## Descricao

Sistema deve permitir exclusao de anotacoes atraves de processo controlado que previne remocoes acidentais, implementado via soft delete preservando dados para auditoria. Soft delete marca anotacao como excluida atraves de campo deleted_at ao inves de remover registro do banco, permitindo rastreabilidade e possivel recuperacao. Antes de executar exclusao, sistema exige confirmacao explicita via dialogo que apresenta resumo da anotacao sendo removida (texto e autor), evitando delecoes acidentais. Apos confirmacao, anotacao e removida imediatamente do mapa e listagens padrao, mas permanece acessivel via interfaces administrativas ou queries de auditoria. Exclusao registrada no log incluindo usuario executor, timestamp, identificador da anotacao e conteudo removido.

## Criterios de Aceitacao

1. Soft delete com campo deleted_at
2. Confirmacao explicita antes de excluir
3. Remocao imediata do mapa e listagens
4. Dados preservados para auditoria
5. Registro em log de auditoria

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-153, RF-134
