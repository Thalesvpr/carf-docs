---
type: leaf
status: review
updated: 2026-01-24
---

# Tipos TypeScript

Interfaces e enums de dominio CARF sincronizados com modelos do backend .NET. Garantem type safety e autocomplete em todo frontend.

## Sincronizacao com Backend

Cada interface TypeScript espelha classe C# correspondente. Campos obrigatorios e opcionais correspondem a nullable annotations do .NET. Tipos de data usam Date no frontend mapeando para DateTime do backend. GeoJSON types alinham com NetTopologySuite. Processo de sincronizacao requer atualizacao manual quando backend modifica modelos, com possibilidade futura de geracao automatica via NSwag.

## Entidades de Dominio

Unit representa unidade habitacional no processo REURB. Contem identificacao com id e code, status do workflow, endereco completo, geometria como poligono GeoJSON, areas em metros quadrados, referencia a Community e metadados de auditoria com createdAt, updatedAt e version para optimistic locking.

Holder representa titular de direito sobre unidade. Pode ser pessoa fisica com CPF ou juridica com CNPJ. Inclui dados pessoais como nome, data nascimento, nacionalidade, estado civil e profissao. Contem contato com email e telefone. Endereco pode diferir da unidade.

Community agrupa unidades em area geografica. Define name, code opcional, type categorizando natureza da ocupacao, boundary como poligono delimitador, area total e tenantId para isolamento multi-tenant.

## Enums de Workflow

UnitStatus define seis estados do ciclo de aprovacao de unidades. LegitimationStatus define onze estados do processo REURB legal conforme Lei 13.465/2017. EntityType classifica titulares como pessoa fisica ou juridica. CommunityType categoriza ocupacoes. Role hierarquiza permissoes de usuarios em cinco niveis.

## DTOs de API

CreateUnitDto e UpdateUnitDto definem payloads de requisicao. Create inclui campos obrigatorios para POST. Update torna campos opcionais para PATCH parcial. Pattern se repete para Holder e Community. PaginatedResponse encapsula listas com metadados de paginacao.
