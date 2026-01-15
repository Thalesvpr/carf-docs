# VALUE-OBJECTS

Value objects são conceitos sem identidade própria, definidos exclusivamente por seus atributos. São imutáveis e encapsulam validações e regras de negócio, garantindo integridade na camada de domínio.

## Base Class

- **[00-base-value-object.md](./00-base-value-object.md)** - Classe base com equals e hashCode

## Identificação e Documentos

- **[01-cpf.md](./01-cpf.md)** - CPF brasileiro com validação de dígitos
- **[20-crea.md](./20-crea.md)** - Registro profissional CREA
- **[21-api-key-value.md](./21-api-key-value.md)** - Valor de chave API

## Geografia e Geometria

- **[02-geo-polygon.md](./02-geo-polygon.md)** - Polígono geográfico WKT/GeoJSON
- **[07-geo-point.md](./07-geo-point.md)** - Ponto com latitude e longitude

## Status e Workflow

- **[03-unit-status.md](./03-unit-status.md)** - Status da unidade em seis estados
- **[17-sync-status.md](./17-sync-status.md)** - Status de sincronização
- **[19-point-status.md](./19-point-status.md)** - Status do ponto topográfico
- **[22-legitimation-status.md](./22-legitimation-status.md)** - Status do processo em onze estados

## Dados Pessoais

- **[08-email.md](./08-email.md)** - Email validado conforme RFC 5322
- **[09-phone-number.md](./09-phone-number.md)** - Telefone brasileiro com DDD
- **[10-address.md](./10-address.md)** - Endereço brasileiro estruturado

## Tipos e Classificações

- **[11-community-type.md](./11-community-type.md)** - Tipo de comunidade
- **[12-entity-type.md](./12-entity-type.md)** - Tipo de entidade polimórfico
- **[13-document-type.md](./13-document-type.md)** - Tipo de documento
- **[14-annotation-type.md](./14-annotation-type.md)** - Tipo de anotação
- **[15-priority.md](./15-priority.md)** - Prioridade LOW a URGENT
- **[18-point-type.md](./18-point-type.md)** - Tipo de ponto topográfico
- **[23-decision.md](./23-decision.md)** - Decisão de parecer
- **[24-certificate-situation.md](./24-certificate-situation.md)** - Situação da certidão

## Roles e Permissões

- **[16-team-role.md](./16-team-role.md)** - Papel na equipe
- **[25-role.md](./25-role.md)** - Papel do usuário no sistema

## Schemas e Matrizes

- **[04-custom-data-schema.md](./04-custom-data-schema.md)** - Schema JSON customizável
- **[05-permissions-matrix.md](./05-permissions-matrix.md)** - Matriz de permissões CRUD
- **[06-spatial-overlap-matrix.md](./06-spatial-overlap-matrix.md)** - Matriz de sobreposições espaciais

---

**Última atualização:** 2026-01-14
