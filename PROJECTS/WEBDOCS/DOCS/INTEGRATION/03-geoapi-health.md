# Integração com GEOAPI Health

Status page do WEBDOCS consome endpoints /health dos serviços CARF para exibir disponibilidade em tempo real. Integração via fetch server-side durante SSR garante que informações são atuais sem expor URLs internas ao cliente.

Endpoint /health da GEOAPI retorna JSON com status (healthy, degraded, unhealthy), checks individuais (database, keycloak, minio), e timestamp. Response inclui latência de cada dependência permitindo identificar gargalos específicos.

Componente StatusPage.astro executa fetch para cada serviço configurado em src/config/services.ts durante renderização server-side. Timeout de 5 segundos previne que serviço lento bloqueie renderização. Serviços que não respondem são marcados como unknown com mensagem explicativa.

Serviços monitorados incluem GEOAPI verificando endpoint /health que testa conexão PostgreSQL e dependências, Keycloak verificando /.well-known/openid-configuration indicando que realm está operacional, e MinIO verificando endpoint /minio/health/live para storage de arquivos.

Client-side polling opcional via script que executa fetch a cada 30 segundos atualizando indicadores visuais sem reload da página. Polling desabilitado por padrão para economizar recursos, habilitado quando usuário clica em "atualização automática".

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
