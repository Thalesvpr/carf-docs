---
type: leaf
status: review
updated: 2026-01-24
---

# API de Tipos

Documentacao das interfaces e enums de dominio exportados pelo modulo @carf/tscore/types. Todos os tipos espelham modelos do backend .NET para consistencia entre frontend e API.

## Entidades Principais

A interface Unit representa unidade habitacional com campos id, code, status, endereco completo, geometry como GeoJSON Polygon, area, communityId e metadados de auditoria. A interface Holder representa titular com campos para pessoa fisica ou juridica incluindo cpf, cnpj, dados pessoais e endereco. A interface Community representa comunidade com name, code, type, boundary como poligono delimitador, area total e tenantId para isolamento multi-tenant.

## Enums de Status

UnitStatus define estados do workflow de aprovacao: DRAFT para rascunho inicial, PENDING_ANALYSIS aguardando analise, IN_REVIEW em revisao tecnica, APPROVED para aprovadas, REJECTED para rejeitadas e REQUIRES_CHANGES quando precisa correcoes. LegitimationStatus define onze estados do processo REURB legal desde DRAFT ate CERTIFICATE_ISSUED conforme Lei 13.465/2017.

## Enum de Roles

Role define hierarquia de permissoes com seis niveis: SUPER_ADMIN com acesso total, ADMIN para administradores de tenant, MANAGER para gestores, ANALYST para analistas tecnicos, FIELD_COORDINATOR para coordenadores de campo com menu mobile completo e supervisao de equipe, e FIELD_CADASTRATOR para cadastradores de campo com acesso restrito a mapa e formularios. A funcao hasRolePermission compara niveis hierarquicos permitindo verificacao de autorizacao.

## Enums Auxiliares

EntityType distingue PESSOA_FISICA, PESSOA_JURIDICA, GOVERNMENT, NGO e OTHER para classificacao de titulares. CommunityType categoriza comunidades como URBAN_SLUM, RURAL_SETTLEMENT, INDIGENOUS_LAND, QUILOMBOLA, FISHING_COMMUNITY ou OTHER.

## DTOs

Interfaces CreateUnitDto e UpdateUnitDto definem contratos para criacao e atualizacao via API. Create requer campos obrigatorios como code, street, city, state e communityId. Update torna todos campos opcionais para PATCH parcial. PaginatedResponse encapsula listas com total, page, limit e flags hasNext e hasPrevious.
