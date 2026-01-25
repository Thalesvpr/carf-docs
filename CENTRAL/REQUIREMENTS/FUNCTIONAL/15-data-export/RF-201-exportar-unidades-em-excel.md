---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-201: Exportar Unidades em Excel

## Descricao

Sistema deve oferecer exportacao de unidades em formato Excel (.xlsx) nativo do Microsoft Office produzindo planilha com multiplas abas organizadas logicamente: aba principal com dados de unidades, aba adicional com titulares vinculados, e opcionalmente abas com documentos anexados, fotos e estatisticas agregadas. Geracao aplica formatacao profissional incluindo cabecalhos com fundo colorido, colunas com larguras ajustadas automaticamente, formatacao numerica apropriada para valores monetarios e percentuais, e formatacao de data no padrao brasileiro. Filtros automaticos ativados na linha de cabecalho permitem analises exploratories interativas. Exportacao valiosa para gestores familiarizados com ambiente Office que necessitam criar graficos e tabelas dinamicas.

## Criterios de Aceitacao

1. Formato .xlsx nativo
2. Multiplas abas organizadas
3. Formatacao profissional de celulas
4. Filtros automaticos na linha de cabecalho
5. Segregacao por tenant_id

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-044, RF-074
