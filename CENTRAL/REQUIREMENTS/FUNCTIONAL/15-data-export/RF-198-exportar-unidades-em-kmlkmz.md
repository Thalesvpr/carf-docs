---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-198: Exportar Unidades em KML/KMZ

## Descricao

Sistema deve possibilitar exportacao de unidades territoriais em formato KML (Keyhole Markup Language) ou versao compactada KMZ, padrao adotado pelo Google Earth para visualizacao tridimensional de dados geoespaciais em interface acessivel a usuarios nao tecnicos. Geracao estrutura dados conforme especificacao OGC incluindo elementos Placemark para cada unidade com geometrias em coordenadas WGS84, atributos alfanumericos em popups HTML formatados, e metadados de estilo. Sistema aplica estilos diferenciados conforme status (aprovado em verde, pendente em amarelo, rejeitado em vermelho) ou tipo de ocupacao facilitando interpretacao visual. Compactacao KMZ reduz tamanho para distribuicao via email ou internet. Dados filtrados por tenant_id do usuario.

## Criterios de Aceitacao

1. Formato KML conforme especificacao OGC
2. Opcao de compactacao KMZ
3. Coordenadas WGS84
4. Estilos diferenciados por status
5. Segregacao por tenant_id

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-044, RF-127
