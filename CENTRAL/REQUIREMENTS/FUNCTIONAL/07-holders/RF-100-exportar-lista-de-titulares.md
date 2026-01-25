---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-100: Exportar Lista de Titulares

## Descricao

Sistema deve permitir exportacao de titulares em formatos Excel e CSV respeitando filtros ativos. Exportacao inclui todos campos relevantes: nome, tipo, CPF/CNPJ, RG, nascimento, contatos, endereco e datas de criacao e atualizacao. Excel gerado com cabecalhos formatados, filtros automaticos e aba de metadados. CSV utiliza UTF-8 com BOM, delimitador adequado e escapamento correto. Viabiliza analises externas, compartilhamento e integracao com sistemas legados.

## Criterios de Aceitacao

1. Exportacao em Excel e CSV
2. Respeito aos filtros ativos
3. Todos campos relevantes incluidos
4. Excel formatado com filtros automaticos
5. CSV com UTF-8 e escapamento correto

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-087, RF-082
