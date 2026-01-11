# Value Objects - Objetos de Valor Imutáveis

Value objects são conceitos sem identidade própria definidos exclusivamente por seus atributos sendo imutáveis e intercambiáveis garantindo validação e encapsulamento de regras de negócio em estruturas de dados auto-validadas.

## Base Class

- **[00-base-value-object.md](./00-base-value-object.md)** - Classe base abstrata para todos os value objects com equals() e hashCode()

## Identificação & Documentos (3 value objects)

- **[01-cpf.md](./01-cpf.md)** - CPF brasileiro validado com dígitos verificadores
- **[02-cnpj.md](./02-geo-polygon.md)** - CNPJ brasileiro validado com dígitos verificadores
- **[20-crea.md](./20-crea.md)** - Registro profissional CREA validado (CREA-UF NNNNNN)

## Geografia & Geometria (3 value objects)

- **[03-geo-polygon.md](./02-geo-polygon.md)** - Polígono geográfico WKT/GeoJSON
- **[04-coordinates.md](./07-geo-point.md)** - Sistema de coordenadas SIRGAS/WGS84
- **[07-geo-point.md](./07-geo-point.md)** - Ponto geográfico lat/lng validado

## Status & Workflow (4 value objects)

- **[05-unit-status.md](./03-unit-status.md)** - Status workflow unidade (DRAFT PENDING IN_REVIEW APPROVED REJECTED REQUIRES_CHANGES)
- **[06-sync-status.md](./17-sync-status.md)** - Status sincronização (PENDING SUCCESS CONFLICT FAILED)
- **[19-point-status.md](./19-point-status.md)** - Status ponto topográfico (COLLECTED PROCESSED APPROVED REJECTED)
- **[21-legitimation-status.md](./22-legitimation-status.md)** - Status processo legitimação (11 estados workflow conforme Lei 13465/2017)

## Dados Pessoais (4 value objects)

- **[08-email.md](./08-email.md)** - Email RFC 5322 validado
- **[09-phone-number.md](./09-phone-number.md)** - Telefone brasileiro com DDD validado
- **[10-address.md](./10-address.md)** - Endereço brasileiro completo estruturado
- **[21-api-key-value.md](./21-api-key-value.md)** - Valor chave API formato geoapi_sk_xxx

## Tipos & Classificações (8 value objects)

- **[11-community-type.md](./11-community-type.md)** - Tipo comunidade (URBANA RURAL QUILOMBOLA INDIGENA RIBEIRINHA)
- **[12-entity-type.md](./12-entity-type.md)** - Tipo entidade polimórfico (UNIT HOLDER COMMUNITY BLOCK etc)
- **[13-document-type.md](./13-document-type.md)** - Tipo documento (PHOTO_FRONT DOC_CPF PLANT_DWG MEMORIAL etc)
- **[14-annotation-type.md](./14-annotation-type.md)** - Tipo anotação (NOTE WARNING ISSUE REMINDER)
- **[15-priority.md](./15-priority.md)** - Prioridade (LOW NORMAL HIGH URGENT)
- **[18-point-type.md](./18-point-type.md)** - Tipo ponto topográfico (MARCO PIQUETE NATURAL)
- **[22-decision.md](./23-decision.md)** - Decisão parecer (APPROVED REJECTED NEEDS_CORRECTION APPROVED_WITH_CONDITIONS)
- **[23-certificate-situation.md](./24-certificate-situation.md)** - Situação certidão (COVERED CONFRONTING BOTH)

## Roles & Permissões (2 value objects)

- **[16-team-role.md](./16-team-role.md)** - Papel em equipe (LEADER MEMBER)
- **[24-role.md](./25-role.md)** - Papel usuário sistema (SUPER_ADMIN ADMIN MANAGER ANALYST FIELD_AGENT) se implementado como VO

## Schemas & Matrices (3 value objects)

- **[04-custom-data-schema.md](./04-custom-data-schema.md)** - Schema JSON customizável para campos extras
- **[05-permissions-matrix.md](./05-permissions-matrix.md)** - Matriz de permissões CRUD por role
- **[06-spatial-overlap-matrix.md](./06-spatial-overlap-matrix.md)** - Matriz de sobreposições espaciais entre geometrias

---

**Última atualização:** 2026-01-10
