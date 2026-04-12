---
type: leaf
status: review
updated: 2026-02-08
---

# Seed Data

Documentacao dos dados iniciais (seed) necessarios para o funcionamento da GEOAPI em diferentes ambientes.

## Dados Obrigatorios (Producao)

Estes dados sao inseridos automaticamente via `HasData()` nas configuracoes do Entity Framework e estao presentes em todas as migrations iniciais. Sao necessarios para o funcionamento basico do sistema.

### Tenant Default

| Campo | Valor | Descricao |
|-------|-------|-----------|
| Id | guid fixo (seed) | Identificador do tenant interno |
| Name | CARF Internal | Tenant para testes internos e administracao |
| Slug | carf-internal | Identificador legivel |
| IsActive | true | Ativo desde a instalacao |
| CreatedAt | data da migration | Data de criacao |

### Account Super-Admin

| Campo | Valor | Descricao |
|-------|-------|-----------|
| Id | guid fixo (seed) | Identificador da conta admin |
| KeycloakId | configuravel via variavel de ambiente | ID do usuario no Keycloak |
| Name | Super Admin | Nome de exibicao |
| Email | configuravel via variavel de ambiente | Email do administrador |
| Role | SUPER_ADMIN | Role com acesso total |
| TenantId | tenant default id | Vinculado ao tenant interno |

### Community Types (Enum Values)

| Valor | Nome | Descricao |
|-------|------|-----------|
| 1 | RURAL | Comunidade em area rural |
| 2 | URBAN | Comunidade em area urbana |
| 3 | MIXED | Comunidade em area mista rural/urbana |

### Document Types (Enum Values)

| Valor | Nome | Descricao |
|-------|------|-----------|
| 1 | FACADE_PHOTO | Foto da fachada |
| 2 | INTERIOR_PHOTO | Foto interna |
| 3 | DOCUMENT_PHOTO | Foto de documento |
| 4 | PDF_DOCUMENT | Documento PDF |
| 5 | ORTHOPHOTO | Ortofoto GeoTIFF |
| 6 | REPORT | Relatorio exportado |
| 7 | CERTIFICATE | Certidao de legitimacao |

### Unit Status Values

| Valor | Nome | Descricao |
|-------|------|-----------|
| 1 | DRAFT | Rascunho — cadastro incompleto |
| 2 | IN_PROGRESS | Em andamento — coleta de dados em campo |
| 3 | PENDING_REVIEW | Aguardando revisao do coordenador |
| 4 | APPROVED | Aprovado — dados completos e validados |
| 5 | REJECTED | Rejeitado — necessita correcoes |
| 6 | ARCHIVED | Arquivado — nao mais ativo |

## Dados de Desenvolvimento (Dev/Local)

Dados inseridos apenas em ambiente de desenvolvimento para facilitar testes e exploracao da API. Podem ser inseridos via `HasData()` condicional ou script SQL.

### Resumo de Volumes

| Entidade | Quantidade Dev | Quantidade Staging | Dados |
|----------|---------------|-------------------|-------|
| Tenant | 3 | 1 (anonimizado) | Municipios ficticio: "Cidade Alfa", "Cidade Beta", "Cidade Gama" |
| Account | 10 por tenant | 5 por tenant | Mix de roles: 1 admin, 2 coordenadores, 4 cadastradores, 3 agentes |
| Community | 3 por tenant | 2 por tenant | Comunidades com boundaries GeoJSON predefinidos |
| Block | 2 por comunidade | 1 por comunidade | Quadras com poligonos simples |
| Unit | 10 por comunidade | 5 por comunidade | Mix de status: 3 DRAFT, 3 IN_PROGRESS, 2 APPROVED, 1 REJECTED, 1 ARCHIVED |
| Holder | 2-3 por unidade | 1-2 por unidade | Pessoas fisicas com CPFs validos de teste |
| Document | 1-2 por unidade | 1 por unidade | Fotos de exemplo (placeholder images) |
| Team | 1 por comunidade | 1 por comunidade | Equipe com coordenador + cadastradores |

### Tenants de Teste

| Slug | Nome | Descricao |
|------|------|-----------|
| cidade-alfa | Municipio Cidade Alfa | Municipio urbano com 3 comunidades densas |
| cidade-beta | Municipio Cidade Beta | Municipio rural com 3 comunidades esparsas |
| cidade-gama | Municipio Cidade Gama | Municipio misto para testes de borda |

### Usuarios de Teste

| Email Pattern | Role | Senha Dev | Tenant |
|---------------|------|-----------|--------|
| admin@{slug}.test | REURBMASTER | dev123!@# | Cada tenant |
| coord01@{slug}.test | COORDINATOR | dev123!@# | Cada tenant |
| coord02@{slug}.test | COORDINATOR | dev123!@# | Cada tenant |
| cad01@{slug}.test | CADASTRATOR | dev123!@# | Cada tenant |
| cad02@{slug}.test | CADASTRATOR | dev123!@# | Cada tenant |
| cad03@{slug}.test | CADASTRATOR | dev123!@# | Cada tenant |
| cad04@{slug}.test | CADASTRATOR | dev123!@# | Cada tenant |
| agent01@{slug}.test | FIELD_AGENT | dev123!@# | Cada tenant |
| agent02@{slug}.test | FIELD_AGENT | dev123!@# | Cada tenant |
| agent03@{slug}.test | FIELD_AGENT | dev123!@# | Cada tenant |

### Comunidades de Teste (Cidade Alfa)

| Nome | Tipo | Unidades | Area Aprox. |
|------|------|----------|------------|
| Comunidade Sol Nascente | URBAN | 10 | 50 ha |
| Comunidade Rio Bonito | RURAL | 10 | 200 ha |
| Comunidade Morro Verde | MIXED | 10 | 100 ha |

## Como Executar Seed

### 1. Via EF Core HasData() (Automatico)

Dados inseridos automaticamente durante a execucao de migrations. Configurados nas classes `EntityTypeConfiguration` de cada entidade.

```
// Em UnitConfiguration.cs
builder.HasData(
    new Unit { Id = Guid.Parse("..."), TenantId = ..., Status = UnitStatus.DRAFT, ... }
);
```

Vantagem: dados sempre presentes apos `dotnet ef database update`. Desvantagem: alteracoes geram novas migrations.

### 2. Via Script SQL (Manual)

Script localizado em `scripts/seed-dev-data.sql`. Executar manualmente apos criar o banco:

```
psql -h localhost -U carf -d carf_db -f scripts/seed-dev-data.sql
```

Vantagem: flexivel, facil de alterar. Desvantagem: nao versionado com migrations.

### 3. Via Endpoint Admin (Dev Only)

Endpoint disponivel apenas quando `ASPNETCORE_ENVIRONMENT=Development`:

```
POST /api/admin/seed
Authorization: Bearer {admin-token}
Content-Type: application/json

{
  "tenantCount": 3,
  "communitiesPerTenant": 3,
  "unitsPerCommunity": 10,
  "includePlaceholderPhotos": true
}
```

Resposta: 200 OK com resumo dos dados criados. Idempotente — se dados ja existem, nao duplica.

## Dados de Staging

O ambiente de staging utiliza dados anonimizados extraidos de producao. O processo de anonimizacao:

1. Dump do banco de producao
2. Script de anonimizacao substitui: nomes por nomes ficticios, CPFs por CPFs validos de teste, emails por emails @staging.test, telefones por numeros ficticios, enderecos por enderecos genericos
3. Geometrias sao mantidas (nao conteem dados pessoais)
4. Fotos e documentos sao substituidos por placeholders

Este processo e executado mensalmente pelo time de infraestrutura.