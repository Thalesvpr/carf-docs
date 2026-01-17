# Data Flow - ADMIN

## Fluxo de Dados

Data flow: **(1) User action** (ex: delete tenant) → **(2) React Component** chama mutation via TanStack Query `useMutation()` → **(3) Mutation function** chama `api.admin.tenants.delete(id)` via @carf/geoapi-client → **(4) API Client** adiciona JWT header automaticamente via interceptor, faz DELETE request para `/api/admin/tenants/:id` → **(5) GEOAPI Backend** valida JWT, verifica role ADMIN/SUPER_ADMIN, valida RLS policy, executa delete no banco, chama Keycloak Admin API se necessário → **(6) Response** volta para mutation function → **(7) TanStack Query** invalida cache com `queryClient.invalidateQueries(['tenants'])` → **(8) UI** re-renderiza automaticamente com dados atualizados via refetch automático.

## Exemplo Prático

```typescript
// 1. Component
function TenantManagementPage() {
  // 2. Mutation hook
  const deleteMutation = useMutation({
    mutationFn: (id: string) => api.admin.tenants.delete(id),
    onSuccess: () => {
      // 7. Invalidar cache
      queryClient.invalidateQueries(['tenants'])
      toast.success('Tenant deleted')
    },
  })

  return (
    <Button onClick={() => deleteMutation.mutate(tenantId)}>
      Delete
    </Button>
  )
}

// 3-6. Fluxo automático via @carf/geoapi-client
// 8. UI atualiza automaticamente
```

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Contém code blocks - considerar converter para prosa.
