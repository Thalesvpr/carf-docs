# Monitoramento Keycloak

## Health Check

### Endpoint de saúde

Health básico verifica disponibilidade executando curl http dois pontos barra barra localhost dois pontos oito zero oito zero barra health retornando status UP ou DOWN, health detalhado verifica prontidão executando curl endpoint barra health barra ready verificando se aplicação está pronta para receber tráfego, e liveness executando curl barra health barra live verificando se processo está respondendo útil para Kubernetes probes.

### Healthcheck automatizado

Healthcheck via script executa make health disparando verificação automatizada, healthcheck via cron agenda verificação a cada cinco minutos usando expressão asterisco barra cinco asterisco asterisco asterisco asterisco executando make health com operador OR duplo pipe para caso falha executar echo "Keycloak down!" com pipe para mail com subject Alert destinatário admin arroba carf ponto gov ponto br enviando notificação imediata se serviço cair.

## Métricas

### Endpoint de métricas

Métricas Prometheus são expostas executando curl http dois pontos barra barra localhost dois pontos oito zero oito zero barra metrics retornando formato texto Prometheus com todas métricas disponíveis incluindo contadores de sessões logins erros e histogramas de latência.

### Métricas importantes

Usuários ativos monitorados executando curl com flag silent endpoint metrics com pipe grep keycloak_sessions filtrando contador de sessões ativas, logins por segundo via grep keycloak_logins mostrando taxa de autenticações bem-sucedidas, erros de autenticação via grep keycloak_login_errors contando falhas de login tentativas inválidas, response time via grep http_request_duration exibindo histograma de latência de requisições útil para SLA.

## Prometheus

### prometheus.yml

Configuração Prometheus define scrape_configs com job_name igual keycloak, static_configs contendo targets com array keycloak dois pontos oito zero oito zero apontando para serviço Keycloak, metrics_path igual barra metrics especificando endpoint, scrape_interval igual trinta segundos definindo frequência de coleta de métricas a cada meio minuto balanceando granularidade e carga.

### ServiceMonitor (Kubernetes)

ServiceMonitor define recurso Kubernetes apiVersion monitoring ponto coreos ponto com barra v1 kind ServiceMonitor com metadata name igual keycloak, spec contendo selector com matchLabels app dois pontos keycloak selecionando pods com label correspondente, endpoints array contendo port http e path barra metrics configurando Prometheus Operator para scraping automático de métricas de pods Keycloak sem configuração manual.

## Grafana Dashboard

### Queries úteis

Taxa de logins calculada via PromQL rate parênteses keycloak_logins_total colchetes cinco m colchetes parênteses calculando média de logins por segundo nos últimos cinco minutos, taxa de falhas via rate keycloak_login_errors_total mostrando erros por segundo, sessões ativas via métrica keycloak_sessions_active retornando gauge instantâneo de sessões abertas, P95 response time via histogram_quantile parênteses zero ponto noventa e cinco vírgula rate http_request_duration_seconds_bucket calculando percentil noventa e cinco de latência significando noventa e cinco por cento das requisições são mais rápidas que valor retornado, uptime via up com label selector job igual keycloak retornando um se serviço up zero se down.

### Dashboard JSON

Dashboard Grafana estruturado em JSON com objeto raiz dashboard contendo title igual Keycloak CARF e panels array com dois painéis sendo primeiro com title Login Rate e targets array contendo objeto expr igual rate keycloak_logins_total visualizando taxa de autenticações, segundo painel title Error Rate com expr rate keycloak_login_errors_total visualizando taxa de falhas permitindo importar via Grafana UI ou API provisionando dashboard automaticamente via GitOps.

## Logs

### Centralizados

Fluent Bit configurado com seção INPUT Name forward Listen zero ponto zero ponto zero ponto zero Port vinte e quatro mil duzentos e vinte e quatro recebendo logs via protocolo forward, seção FILTER Name parser Match keycloak ponto asterisco Key_Name log Parser json parseando logs JSON de Keycloak extraindo campos estruturados, seção OUTPUT Name es Match keycloak ponto asterisco Host elasticsearch Index keycloak-logs enviando logs parseados para Elasticsearch criando índice diário com prefixo keycloak-logs permitindo busca e análise centralizada.

### Queries Elasticsearch

Query DSL estruturada com objeto query contendo bool com must array tendo dois filtros sendo primeiro match com level igual ERROR filtrando apenas logs de erro, segundo range com @timestamp gte igual now-1h filtrando última uma hora, retornando todos logs de erro recentes útil para troubleshooting incidentes identificando falhas e stack traces em janela temporal específica via Kibana ou API Elasticsearch.

## Alertas

### Prometheus Alertmanager

Alertas configurados em groups array com name keycloak contendo rules com quatro alertas sendo KeycloakDown com expr up job igual keycloak duplo igual zero for dois minutos annotations summary "Keycloak não está respondendo" disparando se serviço cair por mais de dois minutos, HighLoginErrors com expr rate keycloak_login_errors_total maior dez for cinco minutos summary "Taxa alta de erros de login" disparando se mais de dez erros por segundo sustentados, HighResponseTime com expr histogram_quantile zero ponto noventa e cinco maior dois for cinco minutos summary "Response time alto P95 maior dois segundos" alertando latência degradada, DiskSpaceHigh com expr node_filesystem_avail_bytes dividido node_filesystem_size_bytes menor zero ponto um for cinco minutos summary "Disco com menos de dez por cento disponível" prevenindo indisponibilidade por falta de espaço enviando notificações via Slack email ou PagerDuty conforme severidade.

## Eventos Keycloak

### Configurar Event Listeners
1. Admin Console → Events → Config
2. Save Events: ON
3. Saved Types: LOGIN, LOGOUT, LOGIN_ERROR, REGISTER, UPDATE_PASSWORD
4. Expiration: 7 days

### Query eventos via API

Obter token de acesso executando curl POST para endpoint realms barra master barra protocol barra openid-connect barra token passando data client_id igual admin-cli username igual admin password igual admin grant_type igual password com pipe jq extraindo access_token armazenando em variável TOKEN, consultar eventos recentes executando curl GET para admin barra realms barra carf barra events com query param max igual cem passando header Authorization Bearer interpolando TOKEN com pipe jq formatando JSON retornando últimos cem eventos do realm, filtrar LOGIN_ERROR adicionando query param type igual LOGIN_ERROR retornando apenas eventos de falha de login útil para análise de segurança detectando tentativas de invasão ou problemas de integração.

## Checklist de Monitoramento

- [ ] Health check a cada 5 minutos
- [ ] Métricas coletadas pelo Prometheus
- [ ] Dashboard Grafana configurado
- [ ] Alertas críticos ativos (down, high errors)
- [ ] Logs centralizados (Elasticsearch/CloudWatch)
- [ ] Backup diário automatizado
- [ ] Teste de restore mensal
- [ ] Revisão de eventos semanalmente
**Última atualização:** 2026-01-15
**Status do arquivo**: Review
