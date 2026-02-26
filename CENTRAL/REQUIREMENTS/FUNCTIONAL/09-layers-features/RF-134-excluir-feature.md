---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-134: Excluir Feature

## Descricao

Sistema deve permitir exclusao de features geograficas atraves de processo controlado que previne remocoes acidentais e mantem rastreabilidade, implementado via soft delete. Soft delete marca feature como excluida atraves de campo deleted_at ao inves de remover registro fisicamente, permitindo auditoria futura e recuperacao se necessario. Antes de executar exclusao, sistema exige confirmacao explicita via dialogo que previne delecoes acidentais, incluindo descricao da feature sendo removida. Apos confirmacao, feature e removida imediatamente da renderizacao no mapa e de listagens padrao, mas dados permanecem acessiveis via queries administrativas ou de auditoria. Operacao registrada no log incluindo usuario executor, timestamp, identificador da feature e contexto.

## Criterios de Aceitacao

1. Soft delete com campo deleted_at
2. Confirmacao explicita antes de excluir
3. Remocao imediata da renderizacao
4. Dados preservados para auditoria
5. Registro em log de auditoria

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-132, RF-127
