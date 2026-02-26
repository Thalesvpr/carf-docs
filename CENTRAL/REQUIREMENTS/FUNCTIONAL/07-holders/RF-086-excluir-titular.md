---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-086: Excluir Titular

## Descricao

Sistema deve permitir que usuarios ADMIN excluam titulares utilizando soft delete que marca registro como inativo sem remocao fisica. Antes de permitir exclusao, sistema verifica vinculos ativos com unidades alertando quando titular possui relacionamentos que precisam ser removidos ou transferidos. Interface apresenta modal de confirmacao obrigatoria com aviso sobre consequencias e contagem de vinculos afetados. Soft delete preserva historico para auditorias e possibilita restauracao.

## Criterios de Aceitacao

1. Soft delete mantendo registro inativo
2. Verificacao de vinculos ativos antes de excluir
3. Modal de confirmacao obrigatoria
4. Restrito a perfil ADMIN
5. Possibilidade de restauracao

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-084, RF-061
