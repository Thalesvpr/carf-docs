---
type: leaf
status: review
updated: 2026-02-08
---

# Key Concepts

Conceitos fundamentais que sustentam a arquitetura e o design do backend GEOAPI.

## Clean Architecture

A GEOAPI segue Clean Architecture com 4 camadas concentricas onde dependencias apontam sempre para dentro. Domain e a camada mais interna contendo regras de negocio puras em C# sem dependencias externas. Application orquestra casos de uso via CQRS com Commands e Queries despachados por MediatR. Infrastructure implementa contratos do Domain com EF Core, PostgreSQL, Keycloak, S3 e Redis. Presentation e a camada mais externa expondo endpoints REST via controllers ASP.NET Core.

## Aggregates

Aggregates garantem consistencia transacional delimitando fronteiras de operacoes atomicas. UnitAggregate com Unit como root agrega UnitHolders e Documents, garantindo que unidade deve ter ao menos um titular primario antes de submissao. CommunityAggregate com Community como root agrega referencias a Units e controla boundary geografico. LegitimationRequestAggregate com LegitimationRequest como root agrega Responses e Certificates, garantindo que processo aprovado gera certidao e processo rejeitado nao pode ser editado.

## Multi-Tenancy RLS

O isolamento multi-tenant e implementado via Row-Level Security do PostgreSQL. Cada requisicao extrai tenant_id do JWT, o middleware executa SET LOCAL app.current_tenant e policies RLS filtram automaticamente todas as queries sem necessidade de filtro explicito no codigo da aplicacao. Esse mecanismo impede acesso acidental a dados de outros municipios mesmo em caso de bug no codigo.

## CQRS

Commands representam intencoes de escrita com validacao complexa retornando DTOs. Queries representam leituras sem side effects usando projecoes otimizadas e cache Redis. Ambos sao despachados via MediatR para handlers isolados e testaveis, com pipeline behaviors para validacao (FluentValidation), logging e auditoria.

## Domain Events

Eventos de dominio permitem comunicacao assincrona entre aggregates. UnitCreatedEvent notifica o hub SignalR, HolderLinkedEvent atualiza contadores, CertificateIssuedEvent dispara notificacao ao titular. Events sao despachados apos persistencia via IDomainEventDispatcher.

## Offline Sync

O protocolo delta sync conecta REURBCAD ao GEOAPI via endpoints /api/sync. Pull retorna mudancas desde timestamp, push envia batch de operacoes com deteccao de conflitos por campo usando version do registro.
