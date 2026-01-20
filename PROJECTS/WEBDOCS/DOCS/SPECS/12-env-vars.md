# Variáveis de Ambiente

Especificação completa das variáveis de ambiente necessárias para executar o WEBDOCS em diferentes ambientes. Variáveis com prefixo PUBLIC_ são expostas ao cliente, demais são server-side only.

## Variáveis Obrigatórias

Variáveis obrigatórias devem estar definidas para o sistema funcionar corretamente. Ausência de qualquer uma causa falha no build ou runtime.

```json
{
  "required": {
    "PUBLIC_SITE_URL": {
      "example": "https://docs.carf.com.br",
      "description": "URL pública do site para links absolutos e canonical",
      "validation": "URL válida com protocolo https em produção"
    },
    "KEYCLOAK_URL": {
      "example": "https://auth.carf.com.br",
      "description": "URL base do servidor Keycloak",
      "validation": "URL válida acessível pelo servidor"
    },
    "KEYCLOAK_REALM": {
      "example": "carf",
      "description": "Nome do realm Keycloak",
      "validation": "String não vazia"
    },
    "KEYCLOAK_CLIENT_ID": {
      "example": "webdocs",
      "description": "ID do client configurado no Keycloak para WEBDOCS",
      "validation": "String não vazia correspondendo a client existente"
    },
    "KEYCLOAK_CLIENT_SECRET": {
      "example": "***",
      "description": "Secret do client para fluxo confidential",
      "validation": "String não vazia, nunca commitada em código"
    }
  }
}
```

## Variáveis Opcionais

Variáveis opcionais possuem valores padrão sensatos e podem ser omitidas em desenvolvimento.

```json
{
  "optional": {
    "GEOAPI_URL": {
      "default": "https://api.carf.com.br",
      "description": "URL base da GeoAPI para integração",
      "validation": "URL válida"
    },
    "GEOAPI_SWAGGER_PATH": {
      "default": "/swagger/v1/swagger.json",
      "description": "Path para spec OpenAPI da GeoAPI",
      "validation": "Path relativo começando com /"
    },
    "STATUS_POLL_INTERVAL_MS": {
      "default": "30000",
      "description": "Intervalo de polling da status page em milissegundos",
      "validation": "Número inteiro positivo >= 5000"
    },
    "CACHE_TTL_SECONDS": {
      "default": "300",
      "description": "TTL padrão para cache de dados externos",
      "validation": "Número inteiro positivo"
    },
    "LOG_LEVEL": {
      "default": "info",
      "description": "Nível de log (debug, info, warn, error)",
      "validation": "Enum de níveis válidos"
    }
  }
}
```

## Variáveis de Serviços para Status Page

URLs de health check dos serviços monitorados na página de status. Cada serviço pode ter URL distinta por ambiente.

```json
{
  "services": {
    "GEOAPI_HEALTH_URL": {
      "default": "https://api.carf.com.br/health",
      "description": "Endpoint de health check da GeoAPI",
      "validation": "URL válida retornando JSON com status"
    },
    "KEYCLOAK_HEALTH_URL": {
      "default": "https://auth.carf.com.br/.well-known/openid-configuration",
      "description": "Endpoint para verificar disponibilidade do Keycloak",
      "validation": "URL válida retornando JSON do OpenID Connect"
    },
    "MINIO_HEALTH_URL": {
      "default": "https://storage.carf.com.br/minio/health/live",
      "description": "Endpoint de health check do MinIO",
      "validation": "URL válida retornando 200 OK"
    },
    "POSTGRES_HEALTH_URL": {
      "default": null,
      "description": "Opcional - verificado via GeoAPI health",
      "validation": "URL válida se definida"
    }
  }
}
```

## Variáveis por Ambiente

Valores típicos para cada ambiente de deploy. Em desenvolvimento local, usar arquivo .env.local que é ignorado pelo git.

```json
{
  "environments": {
    "development": {
      "PUBLIC_SITE_URL": "http://localhost:4321",
      "KEYCLOAK_URL": "http://localhost:8080",
      "KEYCLOAK_REALM": "carf-dev",
      "GEOAPI_URL": "http://localhost:5000",
      "LOG_LEVEL": "debug"
    },
    "staging": {
      "PUBLIC_SITE_URL": "https://docs.staging.carf.com.br",
      "KEYCLOAK_URL": "https://auth.staging.carf.com.br",
      "KEYCLOAK_REALM": "carf-staging",
      "GEOAPI_URL": "https://api.staging.carf.com.br",
      "LOG_LEVEL": "info"
    },
    "production": {
      "PUBLIC_SITE_URL": "https://docs.carf.com.br",
      "KEYCLOAK_URL": "https://auth.carf.com.br",
      "KEYCLOAK_REALM": "carf",
      "GEOAPI_URL": "https://api.carf.com.br",
      "LOG_LEVEL": "warn"
    }
  }
}
```

## Validação em Runtime

O arquivo src/lib/config/env.ts deve validar variáveis obrigatórias no startup e exportar objeto tipado para uso no código. Variáveis ausentes devem causar erro fatal com mensagem clara indicando qual variável está faltando.

## Segurança

Variáveis sensíveis como KEYCLOAK_CLIENT_SECRET nunca devem ser commitadas em código ou expostas em logs. Usar secrets management do Vercel para produção e staging. Em desenvolvimento, usar arquivo .env.local ignorado pelo git.

Variáveis com prefixo PUBLIC_ são injetadas no bundle client-side e visíveis no código fonte da página. Nunca usar PUBLIC_ para valores sensíveis.

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
