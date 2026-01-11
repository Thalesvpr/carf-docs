# Entities - Entidades do Modelo de Domínio

Entidades são conceitos com identidade única persistida ao longo do tempo representando elementos centrais do domínio de regularização fundiária urbana com ciclo de vida rastreável e operações de negócio associadas.

## Base Classes

- **[00-base-entity.md](./00-base-entity.md)** - Classe base abstrata para todas as entidades com id, createdAt, updatedAt
- **[01-base-aggregate-root.md](./01-base-aggregate-root.md)** - Classe base para aggregates com domain events

## Core Domain (3 entidades)

- **[02-unit.md](./02-unit.md)** - Unidade habitacional em processo de regularização fundiária (aggregate root)
- **[03-holder.md](./03-holder.md)** - Pessoa física titular ocupante ou interessado em unidade
- **[04-community.md](./04-community.md)** - Comunidade ou assentamento que agrupa unidades geograficamente

## Multi-Tenancy & Acesso (8 entidades)

- **[07-tenant.md](./07-tenant.md)** - Cliente do sistema multi-tenant com isolamento RLS
- **[08-account.md](./08-account.md)** - Usuário do sistema vinculado a tenant e Keycloak
- **[09-team.md](./09-team.md)** - Equipe de trabalho agrupando usuários para atribuição de comunidades
- **[10-team-member.md](./10-team-member.md)** - Relacionamento N:N Account-Team com role
- **[11-community-authorization.md](./11-community-authorization.md)** - Autorização Team ou Account para Community com CRUD granular
- **[12-block.md](./12-block.md)** - Quadra urbana subdividindo comunidade
- **[13-plot.md](./13-plot.md)** - Lote individual dentro de quadra
- **[14-document.md](./14-document.md)** - Arquivo anexo polimórfico (foto PDF planta)

## Suporte (2 entidades)

- **[15-annotation.md](./15-annotation.md)** - Anotação observação issue ou lembrete polimórfico
- **[16-unit-holder.md](./16-unit-holder.md)** - Relacionamento N:N Unit-Holder com tipo e percentual de propriedade

## Audit & Sync (2 entidades)

- **[17-sync-log.md](./17-sync-log.md)** - Registro de sincronização offline mobile com detecção de conflitos
- **[18-audit-log.md](./18-audit-log.md)** - Log de auditoria de operações CUD

## Topografia & Survey (6 entidades)

- **[19-surveyor.md](./19-surveyor.md)** - Topógrafo profissional responsável por levantamentos com licença CREA
- **[20-survey-point.md](./20-survey-point.md)** - Ponto topográfico coletado em campo com coordenadas GPS
- **[21-rbmc-station.md](./21-rbmc-station.md)** - Estação RBMC do IBGE para correção GPS diferencial
- **[22-survey-processing.md](./22-survey-processing.md)** - Processamento de dados GPS com precisões calculadas
- **[23-monograph.md](./23-monograph.md)** - Monografia de ponto topográfico com fotos e croqui
- **[24-descriptive-memorial.md](./24-descriptive-memorial.md)** - Memorial descritivo técnico com coordenadas NBR

## Legitimação Fundiária (5 entidades)

- **[05-contestation.md](./05-contestation.md)** - Contestação de terceiros sobre legitimação fundiária
- **[25-legitimation-request.md](./25-legitimation-request.md)** - Solicitação de legitimação fundiária para unidade (aggregate root)
- **[26-legitimation-response.md](./26-legitimation-response.md)** - Parecer técnico de solicitação de legitimação
- **[27-legitimation-certificate.md](./27-legitimation-certificate.md)** - Certidão oficial de legitimação fundiária
- **[28-legitimation-plan.md](./28-legitimation-plan.md)** - Planta técnica gráfica DWG/PDF

## WMS/Ortofoto (2 entidades)

- **[29-wms-server.md](./29-wms-server.md)** - Servidor WMS externo configurado para ortofotos de drone
- **[30-wms-layer.md](./30-wms-layer.md)** - Camada individual disponível em WmsServer

## GIS Customizado (2 entidades - opcional)

- **[31-layer.md](./31-layer.md)** - Camada de mapa interna com dados vetoriais customizados
- **[32-layer-feature.md](./32-layer-feature.md)** - Geometria individual dentro de Layer

## Security & Sessions (2 entidades)

- **[33-session.md](./33-session.md)** - Sessão de usuário autenticado com hash de token
- **[34-api-key.md](./34-api-key.md)** - Chave de API para integrações externas (plugins GIS)

---

**Última atualização:** 2026-01-10
