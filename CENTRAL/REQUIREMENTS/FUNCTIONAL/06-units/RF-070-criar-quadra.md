---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-070: Criar Quadra

## Descricao

Sistema deve permitir criacao de quadras representando agrupamentos logicos e espaciais de unidades habitacionais. Formulario captura codigo unico, nome descritivo e comunidade a qual a quadra pertence. Geometria opcional permitindo cadastro inicial sem delimitacao espacial. Usuarios podem vincular unidades existentes a quadra estabelecendo hierarquia comunidade-quadra-unidade. Quadras funcionam como entidades intermediarias facilitando navegacao, consultas agregadas e organizacao compativel com nomenclaturas cadastrais tradicionais.

## Criterios de Aceitacao

1. Formulario com codigo, nome e comunidade
2. Geometria opcional do contorno
3. Vinculacao de unidades a quadra
4. Codigo unico por tenant
5. Hierarquia comunidade-quadra-unidade

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-034, RF-049
