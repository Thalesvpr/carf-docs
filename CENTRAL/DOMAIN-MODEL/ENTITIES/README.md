# ENTITIES

Entidades conceitos identidade única persistida longo tempo representando elementos centrais domínio regularização fundiária urbana ciclo vida rastreável operações negócio associadas incluindo base classes abstratas agregados principais core domain multi-tenancy acesso suporte audit sync topografia survey legitimação fundiária WMS ortofoto GIS customizado security sessions totalizando trinta e cinco entidades organizadas categorias funcionais garantindo modelagem completa processos regularização desde cadastramento campo até emissão certidão oficial.

## Base Classes

- **[00-base-entity.md](./00-base-entity.md)** - Classe base abstrata entidades id createdAt updatedAt
- **[01-base-aggregate-root.md](./01-base-aggregate-root.md)** - Classe base aggregates domain events

## Core Domain

- **[02-unit.md](./02-unit.md)** - Unidade habitacional processo regularização aggregate root
- **[03-holder.md](./03-holder.md)** - Pessoa física titular ocupante interessado unidade
- **[04-community.md](./04-community.md)** - Comunidade assentamento agrupa unidades geograficamente

## Multi-Tenancy Acesso

- **[07-tenant.md](./07-tenant.md)** - Cliente sistema multi-tenant isolamento RLS
- **[08-account.md](./08-account.md)** - Usuário sistema vinculado tenant Keycloak
- **[09-team.md](./09-team.md)** - Equipe trabalho agrupando usuários atribuição comunidades
- **[10-team-member.md](./10-team-member.md)** - Relacionamento Account Team role
- **[11-community-authorization.md](./11-community-authorization.md)** - Autorização Team Account Community CRUD granular
- **[12-block.md](./12-block.md)** - Quadra urbana subdividindo comunidade
- **[13-plot.md](./13-plot.md)** - Lote individual quadra
- **[14-document.md](./14-document.md)** - Arquivo anexo polimórfico foto PDF planta

## Suporte

- **[06-pdf-templates.md](./06-pdf-templates.md)** - Templates PDF Memorial Descritivo Planta Técnica Certidão
- **[15-annotation.md](./15-annotation.md)** - Anotação observação issue lembrete polimórfico
- **[16-unit-holder.md](./16-unit-holder.md)** - Relacionamento Unit Holder tipo percentual propriedade

## Audit Sync

- **[17-sync-log.md](./17-sync-log.md)** - Registro sincronização offline mobile detecção conflitos
- **[18-audit-log.md](./18-audit-log.md)** - Log auditoria operações CUD

## Topografia Survey

- **[19-surveyor.md](./19-surveyor.md)** - Topógrafo profissional levantamentos licença CREA
- **[20-survey-point.md](./20-survey-point.md)** - Ponto topográfico coletado campo coordenadas GPS
- **[21-rbmc-station.md](./21-rbmc-station.md)** - Estação RBMC IBGE correção GPS diferencial
- **[22-survey-processing.md](./22-survey-processing.md)** - Processamento dados GPS precisões calculadas
- **[23-monograph.md](./23-monograph.md)** - Monografia ponto topográfico fotos croqui
- **[24-descriptive-memorial.md](./24-descriptive-memorial.md)** - Memorial descritivo técnico coordenadas NBR

## Legitimação Fundiária

- **[05-contestation.md](./05-contestation.md)** - Contestação terceiros legitimação fundiária
- **[25-legitimation-request.md](./25-legitimation-request.md)** - Solicitação legitimação fundiária unidade aggregate root
- **[26-legitimation-response.md](./26-legitimation-response.md)** - Parecer técnico solicitação legitimação
- **[27-legitimation-certificate.md](./27-legitimation-certificate.md)** - Certidão oficial legitimação fundiária
- **[28-legitimation-plan.md](./28-legitimation-plan.md)** - Planta técnica gráfica DWG PDF

## WMS Ortofoto

- **[29-wms-server.md](./29-wms-server.md)** - Servidor WMS externo configurado ortofotos drone
- **[30-wms-layer.md](./30-wms-layer.md)** - Camada individual disponível WmsServer

## GIS Customizado

- **[31-layer.md](./31-layer.md)** - Camada mapa interna dados vetoriais customizados
- **[32-layer-feature.md](./32-layer-feature.md)** - Geometria individual Layer

## Security Sessions

- **[33-session.md](./33-session.md)** - Sessão usuário autenticado hash token
- **[34-api-key.md](./34-api-key.md)** - Chave API integrações externas plugins GIS

---

**Última atualização:** 2026-01-11
