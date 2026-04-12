---
type: leaf
status: review
updated: 2026-02-07
---

# Data Flow - ADMIN

## Fluxo de Dados

O fluxo de dados no ADMIN segue oito etapas sequenciais. Primeiro, a acao do usuario (por exemplo, deletar tenant) dispara um evento no React Component. O componente invoca uma mutation via TanStack Query useMutation. A mutation function chama o metodo correspondente no @carf/geoapi-client, como api.admin.tenants.delete(id). O API Client adiciona automaticamente o JWT header via interceptor e faz a requisicao HTTP para /api/admin/tenants/:id. O GEOAPI Backend valida o JWT, verifica role ADMIN ou SUPER_ADMIN, aplica RLS policy, executa a operacao no banco e chama Keycloak Admin API se necessario. A response retorna para a mutation function. O TanStack Query invalida o cache relacionado para forcar refetch. A UI re-renderiza automaticamente com dados atualizados.

## Etapas do Fluxo

| Etapa | Acao | Componente Responsavel |
|-------|------|----------------------|
| 1 | Acao do usuario (clique, submit) | React Component |
| 2 | Dispara mutation | TanStack Query useMutation |
| 3 | Chamada ao endpoint admin | @carf/geoapi-client |
| 4 | Injeta JWT e envia request HTTP | API Client interceptor |
| 5 | Valida JWT, verifica role, executa operacao | GEOAPI Backend |
| 6 | Retorna response | HTTP response |
| 7 | Invalida cache automaticamente | TanStack Query invalidateQueries |
| 8 | Re-renderiza UI com dados atualizados | React Component via refetch |

O padrao de invalidacao de cache garante que apos qualquer mutation bem-sucedida, todas as queries relacionadas sao automaticamente refetchadas, mantendo a UI sempre sincronizada com o estado atual do servidor sem necessidade de refresh manual da pagina.
