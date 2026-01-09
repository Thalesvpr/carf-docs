---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# RF-221: Proxy de WMS/WMTS

A GEOAPI pode atuar como proxy intermediário para serviços WMS/WMTS externos através de endpoint dedicado /api/geo-services/proxy que recebe requisições do cliente frontend e as repassa para servidores WMS/WMTS de destino, solucionando problemas de CORS (Cross-Origin Resource Sharing) que impediriam navegadores de acessar diretamente serviços hospedados em domínios diferentes. O proxy implementa repasse transparente de requisições incluindo preservação de parâmetros de query como BBOX, WIDTH, HEIGHT, LAYERS e FORMAT para WMS ou TILEMATRIX, TILEROW, TILECOL para WMTS, garantindo que requisições originadas pelo cliente cheguem intactas ao serviço final e respostas sejam retornadas adequadamente. Opcionalmente, o proxy pode implementar cache de tiles em disco ou memória que armazena respostas de requisições idênticas, permitindo reutilização de tiles previamente baixados sem necessidade de requisitar novamente servidor externo, reduzindo latência percebida pelo usuário, diminuindo dependência de disponibilidade de serviços externos potencialmente instáveis, e reduzindo custos quando serviços de terceiros cobram por volume de requisições. Esta arquitetura de proxy é particularmente valiosa quando integrando múltiplos serviços WMS/WMTS de diferentes provedores com políticas variadas de CORS ou quando conectividade com servidores externos é instável, centralizando gestão de integrações externas na camada backend onde controle e observabilidade são superiores comparado a requisições diretas browser-para-servidor-externo.

---

**Última atualização:** 2025-12-30
