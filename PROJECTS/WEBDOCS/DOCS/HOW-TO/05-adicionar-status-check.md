---
type: leaf
status: review
updated: 2026-02-07
---

# Adicionar Status Check

Guia para incluir novo servico na status page permitindo monitorar disponibilidade.

## Estrutura de Configuracao

O arquivo src/config/services.ts define array de servicos monitorados. Cada servico e representado pela interface Service com as seguintes propriedades:

| Propriedade | Tipo | Descricao |
|---|---|---|
| id | string | Identificador unico em kebab-case |
| name | string | Nome para exibicao na interface |
| description | string | Descricao breve do servico |
| healthEndpoint | string ou null | URL do endpoint de health (null se checado via outro servico) |
| timeout | number | Timeout em milissegundos (padrao 5000) |
| critical | boolean | Se true, sistema depende deste servico |
| category | enum | Categoria: api, database, auth, ou external |
| expectedResponse.status | number | Codigo HTTP esperado (opcional) |
| expectedResponse.bodyContains | string | Texto esperado no body (opcional) |

## Servicos Pre-configurados

| ID | Nome | Endpoint | Critico |
|---|---|---|---|
| geoapi | GeoAPI | GEOAPI_URL + /health | Sim |
| keycloak | Keycloak | KEYCLOAK_URL + /health/ready | Sim |
| postgres | PostgreSQL | null (checado via GeoAPI) | Sim |

## Adicionar Novo Servico

Para adicionar um servico, editar src/config/services.ts e incluir nova entrada no array services. Definir id descritivo em kebab-case, name legivel para usuarios, healthEndpoint com URL completa (usar import.meta.env para variaveis de ambiente), timeout apropriado, critical conforme dependencia do sistema, e category correspondente.

Se URL diferir entre ambientes, adicionar variavel de ambiente em .env e .env.example. Para servicos que requerem autenticacao, incluir propriedade headers com token Bearer lido de variavel de ambiente. Status page executa fetch server-side entao token nao e exposto ao cliente.

## Teste e Validacao

Testar localmente executando bun run dev e acessando /status/. Novo servico deve aparecer na lista com indicador de status. Verificar que status reflete corretamente disponibilidade do servico. Commit e push da mudanca para pipeline de CI validar build e preview deployment.

## Checklist

| Item |
|---|
| Identificar endpoint de health do servico |
| Testar endpoint manualmente via browser ou ferramenta HTTP |
| Adicionar entrada em src/config/services.ts |
| Definir timeout apropriado |
| Marcar critical conforme dependencia |
| Adicionar variavel de ambiente se URL varia por ambiente |
| Testar localmente em /status/ |
| Verificar preview deployment |
