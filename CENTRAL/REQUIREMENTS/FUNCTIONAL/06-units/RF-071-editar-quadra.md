---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-071: Editar Quadra

## Descricao

Sistema deve permitir edicao de dados cadastrais de quadras existentes. Interface oferece atualizacao de campos alfanumericos (codigo, nome, comunidade) via formulario padrao e edicao de geometria espacial via ferramentas interativas de mapa. Edicao de geometria permite ajuste de vertices do poligono delimitador incluindo adicionar, mover ou remover vertices. Todas alteracoes registradas em log de auditoria com timestamp, usuario, campos modificados e valores anteriores e novos. Validacoes incluem unicidade de codigo e integridade geometrica.

## Criterios de Aceitacao

1. Edicao de campos alfanumericos
2. Edicao de geometria via mapa interativo
3. Ajuste de vertices do poligono
4. Log de auditoria com valores anteriores
5. Validacao de unicidade de codigo

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-070
