---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# UC-010-FA-002: Proxy de WMS

Fluxo alternativo do UC-010 Configurar Camadas WMS desviando no passo 12 onde antes de salvar configuração ADMIN marca checkbox Usar Proxy (evitar CORS) ativando roteamento de requests WMS através de backend GEOAPI ao invés de chamadas diretas do navegador ao servidor externo, necessário quando servidor WMS de terceiros não possui headers CORS (Cross-Origin Resource Sharing) configurados adequadamente causando bloqueio de navegador com erro "blocked by CORS policy" impedindo carregamento de tiles cross-domain por restrições de segurança web, sistema salva flag use_proxy=true em registro geoservices marcando camada para intermediação, frontend ao renderizar camada verifica flag e ao invés de usar URL direta do servidor externo em addSource substitui por endpoint interno `/api/geoservices/{geoservice_id}/proxy?bbox={bbox}&width=256&height=256&...` passando parâmetros GetMap como query params, backend ao receber request proxy executa validação verificando geoservice_id existe e pertence ao tenant do usuário autenticado evitando uso não autorizado de proxy, constrói URL completo do servidor WMS externo substituindo placeholders com params recebidos, executa HTTP GET para servidor externo usando biblioteca axios ou node-fetch com headers corretos User-Agent Accept, recebe response binário image/png ou image/jpeg, implementa cache local usando Redis ou file system armazenando tiles com TTL 24 horas reduzindo requests repetidos ao servidor externo para mesma área economizando largura de banda e melhorando performance, retorna imagem ao frontend com headers Content-Type correto e Access-Control-Allow-Origin: * permitindo navegador aceitar response sem bloqueio CORS, frontend renderiza tile normalmente no mapa como se fosse source local transparente ao usuário final, vantagem adicional inclui possibilidade de aplicar transformações server-side como reprojeção on-the-fly ajuste de contraste ou watermarking antes de retornar ao cliente, útil para integrar WMS de órgãos governamentais antigos que não implementaram CORS ou servidores internos de rede local sem HTTPS causando mixed content warnings em aplicação servida via HTTPS.

**Ponto de Desvio:** Passo 12 do UC-010 (antes de salvar)

**Retorno:** Camada configurada com proxy, requests roteados via backend evitando CORS

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
