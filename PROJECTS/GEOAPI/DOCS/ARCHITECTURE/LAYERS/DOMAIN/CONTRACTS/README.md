---
status: review
updated: 2026-01-12
---

# CONTRACTS

Interfaces definidas na camada Domain e implementadas no Infrastructure seguindo Dependency Inversion Principle da Clean Architecture, garantindo que o núcleo de negócio não depende de detalhes de implementação. Interfaces base incluem IRepository<T> para operações CRUD genéricas, IUnitOfWork para controle transacional com SaveChanges, IDateTimeProvider para fornecimento de data/hora atual testável, ITenantProvider para obtenção do tenant_id do request atual e IDomainEventDispatcher para despacho de eventos de domínio. Repositories por feature fornecem operações específicas (IUnitRepository com busca espacial e por status, IHolderRepository busca por CPF, ICommunityRepository, ITeamRepository, ICommunityAuthorizationRepository, IBlockRepository, IPlotRepository, ILayerRepository, IWmsServerRepository, IWmsLayerRepository, ISurveyorRepository, IRbmcStationRepository, ISurveyPointRepository, ISurveyProcessingRepository, IMonographRepository, ILegitimationRequestRepository, ILegitimationCertificateRepository, IDescriptiveMemorialRepository, ILegitimationPlanRepository, IAnnotationRepository, IDocumentRepository, ISyncLogRepository, IAuditLogRepository). Interfaces de serviço abstraem operações externas (ICurrentUser dados do usuário autenticado, IPermissionChecker verificação de permissões, ICommunityAccessChecker acesso a comunidade, IFileStorage upload/download, IWmsClient comunicação WMS, IGpsProcessor processamento GPS, IPdfGenerator geração de certidões e memoriais, INotificationService envio de notificações).

## Arquivos

- **[00-i-repository.md](./00-i-repository.md)** - Interface base repository operações CRUD genéricas
- **[01-i-unit-of-work.md](./01-i-unit-of-work.md)** - Unit of Work controle transacional SaveChanges
- **[02-i-date-time-provider.md](./02-i-date-time-provider.md)** - Provider data hora atual testável
- **[03-i-tenant-provider.md](./03-i-tenant-provider.md)** - Provider tenant_id request atual
- **[04-i-domain-event-dispatcher.md](./04-i-domain-event-dispatcher.md)** - Dispatcher eventos domínio
- **[05-i-current-user.md](./05-i-current-user.md)** - Interface usuário autenticado atual
- **[06-i-file-storage.md](./06-i-file-storage.md)** - Interface storage arquivos S3
- **[07-i-pdf-generator.md](./07-i-pdf-generator.md)** - Interface geração PDFs certidões memoriais

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[PROJECTS/GEOAPI/DOCS/ARCHITECTURE/LAYERS/DOMAIN/CONTRACTS/00-i-repository.md|IRepository<T>]]
- ○ [[PROJECTS/GEOAPI/DOCS/ARCHITECTURE/LAYERS/DOMAIN/CONTRACTS/01-i-unit-of-work.md|IUnitOfWork]]
- ○ [[PROJECTS/GEOAPI/DOCS/ARCHITECTURE/LAYERS/DOMAIN/CONTRACTS/02-i-date-time-provider.md|IDateTimeProvider]]
- ○ [[PROJECTS/GEOAPI/DOCS/ARCHITECTURE/LAYERS/DOMAIN/CONTRACTS/03-i-tenant-provider.md|ITenantProvider]]
- ○ [[PROJECTS/GEOAPI/DOCS/ARCHITECTURE/LAYERS/DOMAIN/CONTRACTS/04-i-domain-event-dispatcher.md|IDomainEventDispatcher]]
- ○ [[PROJECTS/GEOAPI/DOCS/ARCHITECTURE/LAYERS/DOMAIN/CONTRACTS/05-i-current-user.md|ICurrentUser]]
- ○ [[PROJECTS/GEOAPI/DOCS/ARCHITECTURE/LAYERS/DOMAIN/CONTRACTS/06-i-file-storage.md|IFileStorage]]
- ○ [[PROJECTS/GEOAPI/DOCS/ARCHITECTURE/LAYERS/DOMAIN/CONTRACTS/07-i-pdf-generator.md|IPdfGenerator]]

<!-- CARF-INDEX-END -->
