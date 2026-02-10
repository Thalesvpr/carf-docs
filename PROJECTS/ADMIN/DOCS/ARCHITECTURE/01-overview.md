---
type: leaf
status: review
updated: 2026-02-07
---

# Overview da Arquitetura - ADMIN

## Visao Geral

ADMIN e o console administrativo React SPA construido com Vite 5 e shadcn/ui, fornecendo interface para operacoes privilegiadas restrito a usuarios com role ADMIN ou SUPER_ADMIN autenticados via Keycloak PKCE flow. O sistema comunica-se com GEOAPI atraves dos endpoints /api/admin/ que fazem proxy seguro para Keycloak Admin API mantendo client_secret no backend. Utiliza TanStack Query para server state, Zustand para client state, @carf/tscore para auth e validacoes, e deploy para Vercel como static SPA com React Router v6.

## Camadas da Arquitetura

O usuario acessa admin.carf.gov.br via HTTPS com JWT. A Vercel CDN serve arquivos estaticos do SPA. A Presentation Layer renderiza componentes React. A State Management Layer usa TanStack Query e Zustand. A API Client Layer via @carf/geoapi-client injeta JWT automaticamente. As requisicoes chegam ao GEOAPI Backend .NET 9 nos endpoints /api/admin/ que validam JWT e verificam role antes de fazer proxy para a Keycloak Admin API.

## Funcionalidades Principais

| Modulo | Descricao |
|--------|-----------|
| Gerenciamento de Usuarios | Listar, criar, editar, desabilitar, resetar senha, atribuir roles |
| Gerenciamento de Tenants | Listar, criar, editar, visualizar estatisticas, deletar com validacao |
| Audit Logs | Timeline com filtros, exportacao CSV/PDF, busca por entity_id |
| Configuracoes do Sistema | Feature flags, rate limiting, timeout de sessoes |
| Operacoes Batch | Importar usuarios CSV, scripts de manutencao, relatorios |

## Seguranca

A autenticacao utiliza JWT via Keycloak com refresh automatico. A autorizacao segue RBAC com dois niveis: ADMIN gerencia o proprio tenant enquanto SUPER_ADMIN gerencia todos. Todas as operacoes sao logadas em audit trail imutavel registrando quem, quando, o que e o tenant_id.
