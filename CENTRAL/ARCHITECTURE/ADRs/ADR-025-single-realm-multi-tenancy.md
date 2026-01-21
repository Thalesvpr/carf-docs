---
status: rejected
updated: 2026-01-21
description: "Sobreposicao com ADR-005 (RLS). Formato incorreto com secao Implementacao, codigo, diagramas. Consolidar e remover implementacao. Contem blocos de codigo."
---

# ADR-025: Single-Realm Multi-Tenancy Strategy

## Contexto

O sistema CARF atende múltiplos municípios (prefeituras) como clientes, cada um constituindo um tenant isolado. Três abordagens principais existem para multi-tenancy no Keycloak: realm por tenant, database/schema separation, e single-realm com user attributes. A escolha impacta diretamente escalabilidade, isolamento de dados, complexidade operacional e experiência do usuário.

Requisitos específicos do CARF incluem: consultores que acessam múltiplos municípios simultaneamente, SSO unificado entre todas aplicações do ecossistema, e projeção de 50+ municípios atendidos até 2027.

## Decisao

Adotar estrategia **single-realm multi-tenancy** utilizando user attributes para controle de acesso a tenants.

### Implementacao

Cada usuario possui dois atributos no Keycloak:

| Atributo | Tipo | Descricao | Exemplo |
|:---------|:-----|:----------|:--------|
| `tenants` | multi-valued array | Tenants aos quais usuario tem acesso | `["prefeitura-sjc", "prefeitura-taubate"]` |
| `current_tenant` | string | Tenant ativo na sessao atual | `"prefeitura-sjc"` |

Protocol mappers convertem atributos para JWT claims:
- `tenant_id` = current_tenant (claim principal usado pelo backend)
- `allowed_tenants` = tenants array (usado pelo frontend para tenant switcher)

### Fluxo de Tenant Switching

1. Frontend exibe dropdown com tenants de `allowed_tenants`
2. Usuario seleciona novo tenant
3. Frontend chama `POST /api/auth/switch-tenant` com novo tenant_id
4. Backend valida que tenant está em allowed_tenants do usuario
5. Backend atualiza `current_tenant` via Keycloak Admin API
6. Frontend forca refresh do token via `keycloak.updateToken(-1)`
7. Novo access token contem `tenant_id` atualizado

### Isolamento de Dados

Row Level Security (RLS) no PostgreSQL garante isolamento:

```sql
-- Middleware .NET configura variavel de sessao
SET LOCAL app.tenant_id = '{tenant_id_from_jwt}';

-- Policy aplicada a todas tabelas
CREATE POLICY tenant_isolation ON units
  USING (tenant_id = current_setting('app.tenant_id')::uuid)
  WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
```

Queries SELECT/UPDATE/DELETE automaticamente filtradas pelo tenant ativo, sem necessidade de WHERE explicito em cada query.

## Consequencias

### Positivas

**SSO verdadeiro**: Usuario autentica uma vez e acessa qualquer aplicacao (GEOWEB, REURBCAD, ADMIN) sem reautenticar, independente do tenant ativo.

**Multi-tenant users**: Consultores externos podem ter acesso a multiplos municipios simultaneamente, alternando via dropdown sem logout/login.

**Escalabilidade operacional**: Adicionar novo municipio requer apenas criar registros de tenant e atribuir usuarios, sem provisionar novo realm ou infraestrutura.

**Backups simplificados**: Single database com todas as tabelas permite backups atomicos e restore consistente.

**Cross-tenant analytics**: Super-admins podem executar queries agregadas atraves de SET SESSION privilegiado para dashboards corporativos.

### Negativas

**Complexidade de RLS**: Todas tabelas devem ter policies configuradas corretamente; falha em uma tabela compromete isolamento.

**Admin API calls**: Troca de tenant requer chamada para Keycloak Admin API, adicionando latencia (mitigado por cache).

**Tenant offboarding**: Remover municipio requer DELETE CASCADE manual com auditoria para compliance LGPD.

### Neutras

**Performance RLS**: Overhead de RLS e negligenciavel (<1ms por query) em benchmarks com 100+ tenants.

## Alternativas Rejeitadas

### Realm por Tenant

Criar realm separado para cada municipio.

**Motivo da rejeicao**: Nao escala para 50+ municipios (cada realm consome recursos significativos), impossibilita SSO entre tenants, consultores multi-tenant precisariam de contas separadas em cada realm, e administracao operacional (backups, upgrades, monitoring) cresce linearmente.

### Grupos Keycloak

Usar grupos hierarquicos para representar tenants.

**Motivo da rejeicao**: Usuario pode pertencer a apenas um grupo leaf na hierarquia do Keycloak, impossibilitando consultores multi-tenant. Workarounds com multiplos grupos complicam queries de membership.

### Database-per-Tenant

Criar database PostgreSQL separado para cada municipio.

**Motivo da rejeicao**: Complica migrations (N databases para atualizar), impossibilita cross-tenant queries para analytics, e aumenta custo de infraestrutura (conexoes, backups).

## Metricas de Sucesso

- [ ] 100% das tabelas com RLS policies configuradas e testadas
- [ ] Tempo de tenant switch < 500ms (incluindo refresh token)
- [ ] Zero incidentes de vazamento de dados entre tenants
- [ ] Suporte a 50+ tenants sem degradacao de performance

## Referencias

- [PostgreSQL Row Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [ADR-003: Keycloak Autenticacao](./ADR-003-keycloak-autenticacao.md)
- [Multi-tenancy Implementation](../../PROJECTS/KEYCLOAK/DOCS/INTEGRATION/REALM/01-configuration.md)
