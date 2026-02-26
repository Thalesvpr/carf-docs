---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-200: Exportar Unidades em CSV

## Descricao

Sistema deve possibilitar exportacao de dados tabulares de unidades em formato CSV (Comma-Separated Values) que omite geometrias espaciais mas preserva todos os atributos alfanumericos, ideal para analises estatisticas e importacao em planilhas eletronicas como Excel ou Google Sheets. Exportacao inclui colunas relevantes como identificador, codigo cadastral, tipo de ocupacao, area, status, datas de cadastramento e atualizacao, nomes de titulares e endereco. Arquivo utiliza encoding UTF-8 com BOM garantindo correta visualizacao de caracteres acentuados. Sistema permite configuracao do separador (virgula, ponto-e-virgula ou tabulacao) adaptando a requisitos regionais de formatacao. Dados filtrados por tenant_id do usuario autenticado.

## Criterios de Aceitacao

1. Exportacao de todos os atributos alfanumericos
2. Encoding UTF-8 com BOM
3. Separador configuravel
4. Colunas de titulares vinculados
5. Segregacao por tenant_id

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-044, RF-074
