---
status: review
updated: 2026-01-20
---

# Status Page

Página /status/ exibe disponibilidade em tempo real dos serviços CARF permitindo usuários verificarem se sistema está operacional antes de reportar problemas. Implementação combina checks server-side durante SSR com polling opcional client-side.

Layout apresenta card para cada serviço com indicador visual de status (verde para healthy, amarelo para degraded, vermelho para unhealthy, cinza para unknown), nome do serviço, latência do último check, e timestamp da verificação. Seção inferior mostra histórico de incidentes recentes ordenados por data.

## Configuração de Serviços

Serviços monitorados são configurados em formato JSON permitindo adicionar novos serviços sem modificar componentes. Configuração usa variáveis de ambiente para URLs, permitindo valores distintos por ambiente.

```json
{
  "services": [
    {
      "id": "geoapi",
      "name": "GeoAPI",
      "description": "API principal do sistema CARF",
      "healthEndpoint": "${GEOAPI_HEALTH_URL}",
      "timeout": 5000,
      "critical": true,
      "expectedResponse": {
        "status": 200,
        "body": { "status": "healthy" }
      }
    },
    {
      "id": "keycloak",
      "name": "Autenticação",
      "description": "Servidor de identidade Keycloak",
      "healthEndpoint": "${KEYCLOAK_HEALTH_URL}",
      "timeout": 5000,
      "critical": true,
      "expectedResponse": {
        "status": 200,
        "body": "JSON com issuer"
      }
    },
    {
      "id": "minio",
      "name": "Armazenamento",
      "description": "Armazenamento de arquivos e documentos",
      "healthEndpoint": "${MINIO_HEALTH_URL}",
      "timeout": 5000,
      "critical": false,
      "expectedResponse": {
        "status": 200
      }
    },
    {
      "id": "postgres",
      "name": "Banco de Dados",
      "description": "PostgreSQL com PostGIS",
      "healthEndpoint": null,
      "checkVia": "geoapi",
      "critical": true,
      "note": "Verificado indiretamente via health da GeoAPI"
    }
  ]
}
```

## Configuração de Polling

```json
{
  "polling": {
    "interval": 30000,
    "retries": 2,
    "retryDelay": 1000,
    "enabled": true,
    "userToggle": true
  }
}
```

## Estados de Status

```json
{
  "states": {
    "online": {
      "condition": "Response 200 dentro do timeout",
      "color": "#22c55e",
      "icon": "check-circle",
      "label": "Operacional"
    },
    "degraded": {
      "condition": "Response 200 mas latência > 2000ms",
      "color": "#eab308",
      "icon": "alert-triangle",
      "label": "Degradado"
    },
    "offline": {
      "condition": "Response != 200 ou timeout",
      "color": "#ef4444",
      "icon": "x-circle",
      "label": "Indisponível"
    },
    "unknown": {
      "condition": "Erro de rede ou primeira verificação",
      "color": "#6b7280",
      "icon": "help-circle",
      "label": "Desconhecido"
    }
  }
}
```

Health check executa durante SSR garantindo que página carrega com dados atuais. Componente StatusGrid.astro itera sobre serviços configurados executando fetch paralelo com Promise.allSettled para não bloquear em caso de timeout. Resultados são passados para componentes visuais conforme SPECS/13-componentes.md.

Histórico de incidentes mantido em collection do Decap CMS permite equipe de operações documentar manutenções programadas e falhas passadas via interface visual. Frontmatter inclui data, serviços afetados, descrição, e status (investigating, identified, monitoring, resolved). Configuração da collection em SPECS/15-decap-cms-config.md.

Polling client-side habilitado via checkbox "atualização automática" executa fetch a cada 30 segundos atualizando indicadores sem reload. Implementado com setInterval e fetch para endpoint API interno /api/health que retorna JSON com status atual de todos serviços.

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
