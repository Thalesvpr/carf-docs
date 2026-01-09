# Value Objects - Objetos de Valor Imutáveis

Value objects são conceitos sem identidade própria definidos exclusivamente por seus atributos sendo imutáveis e intercambiáveis garantindo validação e encapsulamento de regras de negócio em estruturas de dados auto-validadas.

## Identificação & Documentos (3 value objects)

- **01-cpf.md** - CPF brasileiro validado com dígitos verificadores
- **02-cnpj.md** - CNPJ brasileiro validado com dígitos verificadores
- **20-crea.md** - Registro profissional CREA validado (CREA-UF NNNNNN)

## Dados Pessoais (4 value objects)

- **08-email.md** - Email RFC 5322 validado
- **09-phone-number.md** - Telefone brasileiro com DDD validado
- **10-address.md** - Endereço brasileiro completo estruturado
- **21-api-key-value.md** - Valor chave API formato geoapi_sk_xxx

## Geografia & Geometria (3 value objects)

- **03-geo-polygon.md** - Polígono geográfico WKT/GeoJSON
- **07-geo-point.md** - Ponto geográfico lat/lng validado
- **04-coordinates.md** - Sistema de coordenadas SIRGAS/WGS84

## Status & Workflow (4 value objects)

- **05-unit-status.md** - Status workflow unidade (DRAFT PENDING IN_REVIEW APPROVED REJECTED REQUIRES_CHANGES)
- **21-legitimation-status.md** - Status processo legitimação (11 estados workflow conforme Lei 13465/2017)
- **06-sync-status.md** - Status sincronização (PENDING SUCCESS CONFLICT FAILED)
- **19-point-status.md** - Status ponto topográfico (COLLECTED PROCESSED APPROVED REJECTED)

## Tipos & Classificações (7 value objects)

- **11-community-type.md** - Tipo comunidade (URBANA RURAL QUILOMBOLA INDIGENA RIBEIRINHA)
- **12-entity-type.md** - Tipo entidade polimórfico (UNIT HOLDER COMMUNITY BLOCK etc)
- **13-document-type.md** - Tipo documento (PHOTO_FRONT DOC_CPF PLANT_DWG MEMORIAL etc)
- **14-annotation-type.md** - Tipo anotação (NOTE WARNING ISSUE REMINDER)
- **18-point-type.md** - Tipo ponto topográfico (MARCO PIQUETE NATURAL)
- **22-decision.md** - Decisão parecer (APPROVED REJECTED NEEDS_CORRECTION APPROVED_WITH_CONDITIONS)
- **23-certificate-situation.md** - Situação certidão (COVERED CONFRONTING BOTH)

## Roles & Permissões (3 value objects)

- **16-team-role.md** - Papel em equipe (LEADER MEMBER)
- **24-role.md** - Papel usuário sistema (SUPER_ADMIN ADMIN MANAGER ANALYST FIELD_AGENT) se implementado como VO
- **15-priority.md** - Prioridade (LOW NORMAL HIGH URGENT)

## Implementações

Cada value object documentado aqui tem implementação específica em:
- **Backend .NET**: `PROJECTS/GEOAPI/LAYERS/DOMAIN/VALUE-OBJECTS/` (records C# imutáveis)
- **Frontend React**: `PROJECTS/GEOWEB/UTILS/value-objects/` (classes TypeScript ou funções validação)
- **Mobile React Native**: `PROJECTS/REURBCAD/UTILS/` (classes JavaScript com validação)
- **Plugin GIS Python**: `PROJECTS/GEOGIS/utils/` (dataclasses ou namedtuples)

**Princípios de Value Objects:**
- Imutabilidade: Uma vez criado, não pode ser alterado
- Igualdade por valor: Dois VOs com mesmos atributos são considerados iguais
- Auto-validação: Construtor valida e lança exceção se dados inválidos
- Sem identidade: Não têm ID único, definidos apenas por atributos

Ver também:
- **CENTRAL/DOMAIN-MODEL/ENTITIES/** - Entidades com identidade única
- **CENTRAL/DOMAIN-MODEL/AGGREGATES/** - Fronteiras de consistência
- **CENTRAL/DOMAIN-MODEL/00-INDEX.md** - Índice completo do modelo de domínio

---

**Última atualização:** 2025-01-08
