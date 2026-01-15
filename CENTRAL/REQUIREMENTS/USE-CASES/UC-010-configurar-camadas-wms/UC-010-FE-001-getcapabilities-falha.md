---
modules: [GEOAPI, GEOWEB]
epic: security
---

# UC-010-FE-001: GetCapabilities Falha

Fluxo de exceção do UC-010 Configurar Camadas WMS ocorrendo no passo 6 quando sistema executa request HTTP GET para URL GetCapabilities mas operação falha retornando erro ao invés de XML válido tipicamente causado por timeout (servidor externo lento ou fora do ar não respondendo dentro de 10 segundos configurados), HTTP 404 Not Found (URL incorreta ou endpoint mudou sem documentação atualizada), HTTP 500 Internal Server Error (servidor externo com problema técnico falha de banco de dados ou configuração), DNS resolution failure (domínio não existe ou não resolve para IP válido), SSL certificate error (certificado expirado auto-assinado ou hostname mismatch em URLs HTTPS), ou network unreachable (firewall bloqueando saída do servidor GEOAPI para domínios externos), sistema captura exceção em bloco try-catch logando erro completo com stack trace URL tentada HTTP status code e response body se disponível facilitando troubleshooting, exibe modal vermelho erro com ícone de alerta título "Falha ao Conectar ao Servidor WMS" e mensagem específica transcrevendo erro técnico como "Timeout após 10s - servidor não respondeu" ou "HTTP 404 - endpoint não encontrado" ou "SSL certificate expired" orientando ADMIN sobre natureza do problema, inclui sugestões de ações corretivas em bullets como "Verifique se URL está correta e completa incluindo protocolo https://", "Teste URL diretamente no navegador verificando se retorna XML", "Confirme que servidor está online e acessível", "Verifique se firewall permite saída do servidor para domínio externo", botão Tentar Novamente fecha modal mantendo formulário preenchido permitindo ADMIN ajustar URL corrigindo typo ou consultando documentação atualizada da fonte, opcionalmente pode incluir botão Testar no Navegador abrindo nova aba com URL GetCapabilities permitindo ADMIN ver resposta diretamente e diagnosticar se problema é com URL ou com conectividade do servidor backend GEOAPI especificamente.

**Ponto de Desvio:** Passo 6 do UC-010 (request GetCapabilities)

**Retorno:** Erro exibido, ADMIN corrige URL e retenta teste

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
