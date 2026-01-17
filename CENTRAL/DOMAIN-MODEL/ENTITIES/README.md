# ENTITIES

Entidades do domínio CARF representando elementos centrais com identidade única e ciclo de vida rastreável. Cada entidade tem operações de negócio associadas e é organizada em categorias funcionais.

## Base Classes

- **[00-base-entity.md](./00-base-entity.md)** - Classe base com id, createdAt e updatedAt
- **[01-base-aggregate-root.md](./01-base-aggregate-root.md)** - Classe base para aggregates com domain events

## Core Domain

- **[02-unit.md](./02-unit.md)** - Unidade habitacional em processo de regularização
- **[03-holder.md](./03-holder.md)** - Pessoa física titular ou ocupante da unidade
- **[04-community.md](./04-community.md)** - Comunidade ou assentamento que agrupa unidades

## Multi-Tenancy e Acesso

- **[07-tenant.md](./07-tenant.md)** - Cliente do sistema com isolamento RLS
- **[08-account.md](./08-account.md)** - Usuário vinculado ao tenant via Keycloak
- **[09-team.md](./09-team.md)** - Equipe de trabalho com atribuição de comunidades
- **[10-team-member.md](./10-team-member.md)** - Relacionamento entre Account e Team
- **[11-community-authorization.md](./11-community-authorization.md)** - Autorização de acesso a comunidades
- **[12-block.md](./12-block.md)** - Quadra urbana subdividindo comunidade
- **[13-plot.md](./13-plot.md)** - Lote individual dentro da quadra
- **[14-document.md](./14-document.md)** - Arquivo anexo como foto, PDF ou planta

## Suporte

- **[06-pdf-templates.md](./06-pdf-templates.md)** - Templates PDF para memorial e certidão
- **[15-annotation.md](./15-annotation.md)** - Anotação ou observação polimórfica
- **[16-unit-holder.md](./16-unit-holder.md)** - Relacionamento Unit-Holder com percentual

## Audit e Sync

- **[17-sync-log.md](./17-sync-log.md)** - Registro de sincronização offline
- **[18-audit-log.md](./18-audit-log.md)** - Log de auditoria de operações

## Topografia

- **[19-surveyor.md](./19-surveyor.md)** - Topógrafo com licença CREA
- **[20-survey-point.md](./20-survey-point.md)** - Ponto topográfico coletado em campo
- **[21-rbmc-station.md](./21-rbmc-station.md)** - Estação RBMC IBGE para correção GPS
- **[22-survey-processing.md](./22-survey-processing.md)** - Processamento de dados GPS
- **[23-monograph.md](./23-monograph.md)** - Monografia de ponto topográfico
- **[24-descriptive-memorial.md](./24-descriptive-memorial.md)** - Memorial descritivo técnico

## Legitimação Fundiária

- **[05-contestation.md](./05-contestation.md)** - Contestação de terceiros
- **[25-legitimation-request.md](./25-legitimation-request.md)** - Solicitação de legitimação
- **[26-legitimation-response.md](./26-legitimation-response.md)** - Parecer técnico
- **[27-legitimation-certificate.md](./27-legitimation-certificate.md)** - Certidão oficial
- **[28-legitimation-plan.md](./28-legitimation-plan.md)** - Planta técnica gráfica

## WMS e Ortofoto

- **[29-wms-server.md](./29-wms-server.md)** - Servidor WMS externo
- **[30-wms-layer.md](./30-wms-layer.md)** - Camada disponível no servidor

## GIS Customizado

- **[31-layer.md](./31-layer.md)** - Camada de dados vetoriais
- **[32-layer-feature.md](./32-layer-feature.md)** - Geometria individual da camada

## Security

- **[33-session.md](./33-session.md)** - Sessão de usuário autenticado
- **[34-api-key.md](./34-api-key.md)** - Chave API para integrações

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (35 arquivos)

| ID | Titulo |
|:---|:-------|
| [00-base-entity](./00-base-entity.md) | BaseEntity (Entidade Base) |
| [01-base-aggregate-root](./01-base-aggregate-root.md) | BaseAggregateRoot (Raiz de Agregado Base) |
| [02-unit](./02-unit.md) | Unit (Unidade Habitacional) |
| [03-holder](./03-holder.md) | Holder (Titular) |
| [04-community](./04-community.md) | Community (Comunidade/Assentamento) |
| [05-contestation](./05-contestation.md) | Contestation (Contestação de Processo) |
| [06-pdf-templates](./06-pdf-templates.md) | PDF Templates (Memorial Descritivo, Planta Técnica, Certidão) |
| [07-tenant](./07-tenant.md) | Tenant (Instituição Cliente) |
| [08-account](./08-account.md) | Account (Usuário do Sistema) |
| [09-team](./09-team.md) | Team (Equipe de Trabalho) |
| [10-team-member](./10-team-member.md) | TeamMember (Membro de Equipe) |
| [11-community-authorization](./11-community-authorization.md) | CommunityAuthorization (Autorização de Acesso à Comunidade) |
| [12-block](./12-block.md) | Block (Quadra Urbana) |
| [13-plot](./13-plot.md) | Plot (Lote Individual) |
| [14-document](./14-document.md) | Document (Anexo Polimórfico) |
| [15-annotation](./15-annotation.md) | Annotation (Anotação Polimórfica) |
| [16-unit-holder](./16-unit-holder.md) | UnitHolder (Vínculo Unidade-Titular) |
| [17-sync-log](./17-sync-log.md) | SyncLog (Registro de Sincronização Offline) |
| [18-audit-log](./18-audit-log.md) | AuditLog (Log de Auditoria) |
| [19-surveyor](./19-surveyor.md) | Surveyor (Topógrafo Profissional) |
| [20-survey-point](./20-survey-point.md) | SurveyPoint (Ponto Topográfico GPS) |
| [21-rbmc-station](./21-rbmc-station.md) | RbmcStation (Estação RBMC IBGE) |
| [22-survey-processing](./22-survey-processing.md) | SurveyProcessing (Processamento de Levantamento GPS) |
| [23-monograph](./23-monograph.md) | Monograph (Monografia de Marco Topográfico) |
| [24-descriptive-memorial](./24-descriptive-memorial.md) | DescriptiveMemorial (Memorial Descritivo Técnico) |
| [25-legitimation-request](./25-legitimation-request.md) | LegitimationRequest (Processo de Legitimação Fundiária) |
| [26-legitimation-response](./26-legitimation-response.md) | LegitimationResponse (Parecer Técnico de Legitimação) |
| [27-legitimation-certificate](./27-legitimation-certificate.md) | LegitimationCertificate (Certidão de Legitimação Fundiária) |
| [28-legitimation-plan](./28-legitimation-plan.md) | LegitimationPlan (Planta Técnica de Legitimação) |
| [29-wms-server](./29-wms-server.md) | WmsServer (Servidor WMS/WMTS de Mapas) |
| [30-wms-layer](./30-wms-layer.md) | WmsLayer (Camada WMS Individual) |
| [31-layer](./31-layer.md) | Layer (Camada Vetorial Customizada) |
| [32-layer-feature](./32-layer-feature.md) | LayerFeature (Geometria Individual em Camada) |
| [33-session](./33-session.md) | Session (Sessão de Usuário Autenticado) |
| [34-api-key](./34-api-key.md) | ApiKey (Chave de API para Integrações) |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
