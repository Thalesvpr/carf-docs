---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-072: Listar Quadras

## Descricao

Sistema deve oferecer listagem de quadras com filtragem por comunidade permitindo visualizacao segmentada do cadastro territorial. Interface apresenta codigo, nome, comunidade e total de unidades vinculadas a cada quadra. Total de unidades por quadra facilita compreensao da densidade de ocupacao e completude do cadastramento. Listagem implementa paginacao automatica garantindo performance com grandes volumes de dados. Controles de navegacao permitem acesso rapido a diferentes paginas de resultados.

## Criterios de Aceitacao

1. Listagem com codigo, nome e comunidade
2. Filtro por comunidade
3. Contagem de unidades por quadra
4. Paginacao automatica
5. Ordenacao por diferentes campos

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-070
