---
type: leaf
status: approved
updated: 2026-01-24
---

# ADMIN

Console administrativo React SPA para gestao de tenants, usuarios e configuracoes do sistema CARF. Usado por administradores da plataforma para provisionar novos municipios, gerenciar equipes tecnicas e configurar parametros globais.

Stack compartilhada com GEOWEB usando React 18, TypeScript, Vite, TanStack Query, Zustand e shadcn/ui. Autenticacao OAuth2 PKCE via Keycloak consumindo endpoints administrativos da GEOAPI em /api/admin/*. Acesso restrito a usuarios com role de administrador de plataforma.

## Capacidades

Criacao e configuracao de tenants com parametros especificos como limites de area e camadas WMS disponiveis. Gestao de usuarios com atribuicao de roles e vinculacao a equipes. Criacao de equipes tecnicas com lideres e membros. Visualizacao de metricas de uso por tenant. Auditoria de acoes administrativas. Detalhes tecnicos no repositorio carf-admin.
