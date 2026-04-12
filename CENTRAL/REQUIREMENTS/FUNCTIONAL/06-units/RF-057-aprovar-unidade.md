---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-057: Aprovar Unidade

## Descricao

Sistema deve permitir que usuarios com perfil MANAGER aprovem unidades em status PENDING_APPROVAL. Interface REURBWEB exibe botao de aprovacao visivel apenas para gestores ao visualizar detalhes de unidades pendentes. Gestor pode opcionalmente adicionar comentario explicando os motivos da aprovacao. Status alterado automaticamente para APPROVED com registro em historico de auditoria e notificacao automatica ao usuario criador.

## Criterios de Aceitacao

1. Botao de aprovacao visivel para MANAGER
2. Somente unidades PENDING podem ser aprovadas
3. Comentario opcional na aprovacao
4. Notificacao automatica ao criador
5. Log de auditoria com timestamp e usuario

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-056, RF-033
