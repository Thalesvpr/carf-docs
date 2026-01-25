---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-221: Proxy de WMS/WMTS

## Descricao

GEOAPI deve atuar como proxy intermediario para servicos WMS/WMTS externos atraves de endpoint GET /api/geo-services/proxy que recebe requisicoes do cliente frontend e repassa para servidores de destino, solucionando problemas de CORS que impediriam navegadores de acessar diretamente servicos em dominios diferentes. Proxy implementa repasse transparente de requisicoes preservando parametros como BBOX, WIDTH, HEIGHT, LAYERS para WMS ou TILEMATRIX, TILEROW, TILECOL para WMTS. Opcionalmente implementa cache de tiles em disco ou memoria armazenando respostas de requisicoes identicas, reduzindo latencia e dependencia de servicos externos potencialmente instaveis.

## Criterios de Aceitacao

1. Endpoint GET /api/geo-services/proxy
2. Resolucao de problemas de CORS
3. Repasse transparente de parametros
4. Cache de tiles opcional
5. Reducao de latencia e dependencia externa

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-212, RF-213
