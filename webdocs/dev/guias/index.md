# Guias Técnicos

Tutoriais práticos e best practices para desenvolvimento no CARF.

## Guias Disponíveis

### Getting Started

- [Setup Ambiente Local](/dev/setup/)
- Como contribuir com código
- Padrões de código e linting
- Git workflow e branching strategy

### Backend (.NET)

- **CQRS com MediatR**: Como criar commands e queries
- **Entity Framework**: Working with migrations e DbContext
- **Testes**: Unit tests, integration tests com xUnit
- **Multi-tenancy**: Implementar RLS e tenant isolation
- **Validação**: FluentValidation patterns

### Frontend (React)

- **Feature-Sliced Design**: Organizar features e módulos
- **React Query**: Cache, mutations e optimistic updates
- **Formulários**: React Hook Form + Zod validation
- **State Management**: Zustand best practices
- **Integração API**: Axios interceptors e error handling

### Mobile (React Native)

- **Offline-First**: WatermelonDB patterns
- **Sincronização**: Incremental sync e conflict resolution
- **GPS Tracking**: Background location tracking
- **Performance**: Optimização de listas com FlashList
- **Build & Deploy**: Android/iOS release process

### Plugin QGIS

- **PyQGIS API**: Manipular layers e features
- **Exportação**: Shapefile e GeoJSON
- **Integração GEOAPI**: Autenticação e sync
- **Debugging**: Como debugar plugin QGIS

### DevOps

- **Docker**: Containerização dos serviços
- **CI/CD**: GitHub Actions workflows
- **Deployment**: Deploy em produção
- **Monitoring**: Logs e métricas

## Troubleshooting Comum

### Backend

**Erro: "Migration already applied"**

```bash
# Reverter para migration anterior
dotnet ef database update PreviousMigration --project src/Infrastructure --startup-project src/Gateway

# Remover migration
dotnet ef migrations remove --project src/Infrastructure --startup-project src/Gateway
```

**Erro: "RLS policy blocking query"**

Verifique se o tenant_id está sendo configurado corretamente:

```csharp
// Deve estar no middleware
await using var cmd = connection.CreateCommand();
cmd.CommandText = "SET app.tenant_id = @tenantId";
cmd.Parameters.AddWithValue("tenantId", tenantId);
await cmd.ExecuteNonQueryAsync();
```

### Frontend

**Erro: "CORS policy blocked"**

Configure CORS no backend:

```csharp
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.WithOrigins("http://localhost:3000")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});
```

**Erro: "Query invalidation not working"**

Force invalidation no React Query:

```typescript
await queryClient.invalidateQueries({ queryKey: ['units'] });
```

### Mobile

**Erro: "Sync conflict detected"**

Implementar three-way merge:

```typescript
const resolveConflict = (local, remote, base) => {
  // Estratégia: Last Write Wins
  return remote.updated_at > local.updated_at ? remote : local;
};
```

**Erro: "GPS permission denied"**

Solicitar permissões no Android:

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
```

## Best Practices

### Geral

- Sempre usar tipagem forte (TypeScript, C# com nullable reference types)
- Escrever testes para código crítico
- Documentar decisões arquiteturais (ADRs)
- Seguir convenções de commit (Conventional Commits)

### Backend

- Use CQRS para separar reads e writes
- Valide sempre no Application layer (FluentValidation)
- Use DTOs para contratos de API
- Nunca exponha entidades de domínio diretamente

### Frontend

- Componentes pequenos e reutilizáveis
- Use React Query para cache de servidor
- Zustand apenas para estado local/UI
- Valide formulários com Zod

### Mobile

- Sempre pensar offline-first
- Sincronizar apenas dados modificados
- Otimizar lista com virtualization
- Cachear imagens localmente

## Documentação Adicional

Ver pasta `CENTRAL/ARCHITECTURE/PATTERNS/` no carf-docs para:

- Design patterns utilizados
- Anti-patterns a evitar
- Code review checklist
- Performance guidelines

## Contribuindo

Para adicionar novos guias:

1. Crie arquivo markdown em `PROJECTS/{PROJECT}/DOCS/HOW-TO/`
2. Siga template de guia técnico
3. Adicione à navegação em `.vitepress/config.js`
4. Crie PR para revisão

## Próximos Passos

- Ver [Setup](/dev/setup/)
- Consultar [Arquitetura](/dev/arquitetura/)
- Explorar [API](/dev/api/)
