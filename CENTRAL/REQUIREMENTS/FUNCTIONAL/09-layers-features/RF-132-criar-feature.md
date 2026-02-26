---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-132: Criar Feature

## Descricao

Sistema deve permitir criacao de features geograficas (pontos, linhas, poligonos) dentro de camadas GIS existentes para registrar elementos espaciais e atributos associados. Interface fornece ferramentas de desenho no mapa para tracar geometria diretamente sobre visualizacao cartografica. Ferramenta apropriada e ativada conforme tipo de geometria da camada: single-click para pontos, multiplos cliques conectados para linhas, sequencia fechada para poligonos. Durante ou apos desenho, formulario de atributos customizados permite preenchimento de propriedades definidas no schema da layer. Sistema valida geometria criada garantindo ausencia de auto-intersecoes, fechamento adequado de aneis e conformidade com tipo esperado. Feature persistida no PostGIS com atributos em campo JSONB, renderizada imediatamente com estilo da camada.

## Criterios de Aceitacao

1. Ferramentas de desenho no mapa
2. Formulario de atributos customizados
3. Validacao de geometria
4. Persistencia em PostGIS com JSONB
5. Renderizacao imediata apos criacao

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-131, RF-136
