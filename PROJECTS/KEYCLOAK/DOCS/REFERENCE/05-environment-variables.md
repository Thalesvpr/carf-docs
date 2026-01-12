# Environment Variables

Configuração Keycloak via environment variables para containerização seguindo twelve-factor app. Admin credentials KEYCLOAK_ADMIN username admin inicial, KEYCLOAK_ADMIN_PASSWORD senha forte gerada. Database KC_DB=postgres tipo banco, KC_DB_URL=jdbc:postgresql://host:5432/keycloak connection string, KC_DB_USERNAME e KC_DB_PASSWORD credenciais, KC_DB_SCHEMA schema opcional, KC_DB_POOL_INITIAL_SIZE KC_DB_POOL_MIN_SIZE KC_DB_POOL_MAX_SIZE configuração pool conexões. Hostname KC_HOSTNAME=keycloak.carf.gov.br domínio público, KC_HOSTNAME_STRICT=true rejeita requests outros hosts, KC_HOSTNAME_STRICT_HTTPS=true força HTTPS. HTTP KC_HTTP_ENABLED=false desabilita HTTP plain, KC_HTTPS_PORT=8443 porta HTTPS, KC_HTTPS_CERTIFICATE_FILE e KC_HTTPS_CERTIFICATE_KEY_FILE paths certificado TLS. Proxy KC_PROXY=edge indica reverse proxy termina TLS, reencrypt re-encrypta, passthrough passa TLS through. Health KC_HEALTH_ENABLED=true habilita /health endpoints, KC_METRICS_ENABLED=true expõe /metrics Prometheus. Logging KC_LOG_LEVEL=info verbosidade, KC_LOG_FORMAT=json estruturado para agregadores. Cache KC_CACHE=ispn Infinispan, KC_CACHE_STACK=tcp clustering. Features KC_FEATURES=preview habilita features preview.

---

**Última atualização:** 2026-01-12
