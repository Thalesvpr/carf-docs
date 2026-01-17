# INFRA

Camada de infraestrutura do GEOAPI implementando todas interfaces definidas no Domain seguindo Dependency Inversion Principle sem que o núcleo de negócio dependa de detalhes técnicos. PERSISTENCE contém implementações EF Core com DbContext, repositories concretos, migrations, configurations de mapeamento OR/M e seeders de dados iniciais para desenvolvimento e testes. INTEGRATIONS agrupa integrações com sistemas externos como Keycloak para autenticação OAuth2/OIDC, APIs de validação de CPF/CNPJ da Receita Federal, serviços de geocoding e validação de endereços, e consumo de APIs de órgãos públicos. STORAGE implementa IFileStorage para upload/download de documentos usando S3-compatible storage (MinIO em dev, AWS S3 em prod) com suporte a URLs pré-assinadas e streaming de arquivos grandes. CACHE fornece implementações de caching distribuído via Redis para queries frequentes, cache de sessões e invalidação coordenada entre instâncias. JOBS contém background jobs Hangfire para processos assíncronos como envio de notificações, geração de relatórios, sincronização com sistemas legados e limpeza de dados temporários.

## Subpastas

- **[PERSISTENCE/](./PERSISTENCE/README.md)** - EF Core DbContext, repositories, migrations, seeders
- **[INTEGRATIONS/](./INTEGRATIONS/README.md)** - Integrações externas (Keycloak, APIs validação, etc)
- **[STORAGE/](./STORAGE/README.md)** - File storage S3-compatible (MinIO/AWS S3)
- **[CACHE/](./CACHE/README.md)** - Redis distributed cache
- **[JOBS/](./JOBS/README.md)** - Hangfire background jobs

---

**Última atualização:** 2026-01-12

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (0 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Cache](./CACHE/README.md) | 0 |
|  | [Integrations](./INTEGRATIONS/README.md) | 0 |
|  | [Jobs](./JOBS/README.md) | 0 |
|  | [Persistence](./PERSISTENCE/README.md) | 0 |
|  | [Storage](./STORAGE/README.md) | 0 |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Pronto
