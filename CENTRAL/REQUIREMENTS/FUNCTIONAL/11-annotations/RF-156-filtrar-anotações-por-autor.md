---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-156: Filtrar Anotacoes por Autor

## Descricao

Sistema deve permitir filtrar visualizacao de anotacoes no mapa e listagens baseado em autoria, permitindo ver apenas proprias anotacoes ou todas de todos usuarios conforme preferencia. Interface fornece toggle ou selector com opcoes "Minhas anotacoes" e "Todas" para alternar rapidamente entre modos, onde "Minhas" filtra para exibir apenas anotacoes criadas pelo usuario logado (identificado por user_id). Filtro implementado no backend via query parameter comparando campo author_id de cada anotacao com identificador do usuario logado. Exibicao condicional aplica filtro tanto na renderizacao de marcadores no mapa quanto em listagens em paineis, mantendo consistencia entre interfaces. Estado do filtro persistido na sessao mantendo preferencia entre navegacoes.

## Criterios de Aceitacao

1. Toggle "Minhas anotacoes" / "Todas"
2. Filtro por user_id no backend
3. Consistencia entre mapa e listagens
4. Persistencia de preferencia na sessao
5. Filtragem dentro do escopo do tenant

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-153, RF-017
