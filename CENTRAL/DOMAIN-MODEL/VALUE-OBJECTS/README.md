# VALUE-OBJECTS

Value objects conceitos sem identidade própria definidos exclusivamente atributos sendo imutáveis intercambiáveis garantindo validação encapsulamento regras negócio estruturas dados auto-validadas incluindo base class identificação documentos geografia geometria status workflow dados pessoais tipos classificações roles permissões schemas matrices totalizando vinte e seis value objects organizados categorias funcionais implementando validações CPF CNPJ CREA coordenadas geográficas polígonos emails telefones brasileiros status workflows legitimação fundiária tipos documentos anotações prioridades papéis equipe schemas customizáveis garantindo integridade dados camada domínio.

## Base Class

- **[00-base-value-object.md](./00-base-value-object.md)** - Classe base abstrata value objects equals hashCode

## Identificação Documentos

- **[01-cpf.md](./01-cpf.md)** - CPF brasileiro validado dígitos verificadores
- **[20-crea.md](./20-crea.md)** - Registro profissional CREA validado
- **[21-api-key-value.md](./21-api-key-value.md)** - Valor chave API formato geoapi_sk_xxx

## Geografia Geometria

- **[02-geo-polygon.md](./02-geo-polygon.md)** - Polígono geográfico WKT GeoJSON
- **[07-geo-point.md](./07-geo-point.md)** - Ponto geográfico latitude longitude validado

## Status Workflow

- **[03-unit-status.md](./03-unit-status.md)** - Status workflow unidade seis estados
- **[17-sync-status.md](./17-sync-status.md)** - Status sincronização PENDING SUCCESS CONFLICT FAILED
- **[19-point-status.md](./19-point-status.md)** - Status ponto topográfico COLLECTED PROCESSED APPROVED REJECTED
- **[22-legitimation-status.md](./22-legitimation-status.md)** - Status processo legitimação onze estados Lei 13465/2017

## Dados Pessoais

- **[08-email.md](./08-email.md)** - Email RFC 5322 validado
- **[09-phone-number.md](./09-phone-number.md)** - Telefone brasileiro DDD validado
- **[10-address.md](./10-address.md)** - Endereço brasileiro completo estruturado

## Tipos Classificações

- **[11-community-type.md](./11-community-type.md)** - Tipo comunidade URBANA RURAL QUILOMBOLA INDIGENA RIBEIRINHA
- **[12-entity-type.md](./12-entity-type.md)** - Tipo entidade polimórfico UNIT HOLDER COMMUNITY BLOCK
- **[13-document-type.md](./13-document-type.md)** - Tipo documento PHOTO_FRONT DOC_CPF PLANT_DWG MEMORIAL
- **[14-annotation-type.md](./14-annotation-type.md)** - Tipo anotação NOTE WARNING ISSUE REMINDER
- **[15-priority.md](./15-priority.md)** - Prioridade LOW NORMAL HIGH URGENT
- **[18-point-type.md](./18-point-type.md)** - Tipo ponto topográfico MARCO PIQUETE NATURAL
- **[23-decision.md](./23-decision.md)** - Decisão parecer APPROVED REJECTED NEEDS_CORRECTION
- **[24-certificate-situation.md](./24-certificate-situation.md)** - Situação certidão COVERED CONFRONTING BOTH

## Roles Permissões

- **[16-team-role.md](./16-team-role.md)** - Papel equipe LEADER MEMBER
- **[25-role.md](./25-role.md)** - Papel usuário sistema SUPER_ADMIN ADMIN MANAGER ANALYST FIELD_AGENT

## Schemas Matrices

- **[04-custom-data-schema.md](./04-custom-data-schema.md)** - Schema JSON customizável campos extras
- **[05-permissions-matrix.md](./05-permissions-matrix.md)** - Matriz permissões CRUD role
- **[06-spatial-overlap-matrix.md](./06-spatial-overlap-matrix.md)** - Matriz sobreposições espaciais geometrias

---

**Última atualização:** 2026-01-11
