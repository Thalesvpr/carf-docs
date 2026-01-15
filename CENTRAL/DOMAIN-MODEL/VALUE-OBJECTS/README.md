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

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Aguardando (nova geração) index gerado por script.

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (26 arquivos)

| ID | Titulo |
|:---|:-------|
| [00-base-value-object](./00-base-value-object.md) | BaseValueObject (Value Object Base) |
| [01-cpf](./01-cpf.md) | CPF (Cadastro de Pessoa Física) |
| [02-geo-polygon](./02-geo-polygon.md) | GeoPolygon (Polígono Geográfico) |
| [03-unit-status](./03-unit-status.md) | UnitStatus (Status da Unidade) |
| [04-custom-data-schema](./04-custom-data-schema.md) | CustomData Schema (Unit.CustomData e Tenant.Settings) |
| [05-permissions-matrix](./05-permissions-matrix.md) | Permissions Matrix (Matriz de Permissões Granulares) |
| [06-spatial-overlap-matrix](./06-spatial-overlap-matrix.md) | Spatial Overlap Detection (Detecção de Sobreposição Espacial) |
| [07-geo-point](./07-geo-point.md) | GeoPoint (Ponto Geográfico) |
| [08-email](./08-email.md) | Email (Endereço de Email Validado) |
| [09-phone-number](./09-phone-number.md) | PhoneNumber (Número de Telefone Brasileiro) |
| [10-address](./10-address.md) | Address (Endereço Brasileiro Estruturado) |
| [11-community-type](./11-community-type.md) | CommunityType (Tipo de Comunidade) |
| [12-entity-type](./12-entity-type.md) | EntityType (Tipo de Entidade para Polimorfismo) |
| [13-document-type](./13-document-type.md) | DocumentType (Tipo de Documento) |
| [14-annotation-type](./14-annotation-type.md) | AnnotationType (Tipo de Anotação) |
| [15-priority](./15-priority.md) | Priority (Prioridade) |
| [16-team-role](./16-team-role.md) | TeamRole (Papel dentro de Equipe) |
| [17-sync-status](./17-sync-status.md) | SyncStatus (Status de Sincronização) |
| [18-point-type](./18-point-type.md) | PointType (Tipo de Marco Topográfico) |
| [19-point-status](./19-point-status.md) | PointStatus (Status do Ponto Topográfico) |
| [20-crea](./20-crea.md) | Crea (Registro Profissional CREA) |
| [21-api-key-value](./21-api-key-value.md) | ApiKeyValue (Valor de Chave API) |
| [22-legitimation-status](./22-legitimation-status.md) | LegitimationStatus (Status do Processo de Legitimação) |
| [23-decision](./23-decision.md) | Decision (Decisão de Análise) |
| [24-certificate-situation](./24-certificate-situation.md) | CertificateSituation (Situação do Imóvel para Certidão) |
| [25-role](./25-role.md) | Role (Papel de Usuário no Sistema) |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
