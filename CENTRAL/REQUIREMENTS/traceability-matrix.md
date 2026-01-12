# Matriz de Rastreabilidade
Mapa completo mostrando dependências UC → RF → US → RNF para todos os 11 casos de uso principais do sistema CARF.
---

## UC-001: Cadastrar Unidade Habitacional
**Módulos:** GEOWEB, REURBCAD
**Épica:** security

### Requisitos Funcionais (8)
- [RF-049: Criar Unidade](./FUNCTIONAL-REQUIREMENTS/RF-049-criar-unidade.md)
- [RF-050: Editar Unidade](./FUNCTIONAL-REQUIREMENTS/RF-050-editar-unidade.md)
- [RF-054: Campos Obrigatórios de Unidade](./FUNCTIONAL-REQUIREMENTS/RF-054-campos-obrigatorios-de-unidade.md)
- [RF-055: Tipos de Unidade](./FUNCTIONAL-REQUIREMENTS/RF-055-tipos-de-unidade.md)
- [RF-056: Status de Unidade](./FUNCTIONAL-REQUIREMENTS/RF-056-status-de-unidade.md)
- [RF-066: Desenhar Unidade no Mapa](./FUNCTIONAL-REQUIREMENTS/RF-066-desenhar-unidade-no-mapa.md)
- [RF-068: Calcular Área da Unidade](./FUNCTIONAL-REQUIREMENTS/RF-068-calcular-area-da-unidade.md)
- [RF-069: Validar Sobreposição de Unidades](./FUNCTIONAL-REQUIREMENTS/RF-069-validar-sobreposicao-de-unidades.md)

### User Stories (3)
- [US-014: Criar Unidade Habitacional](./USER-STORIES/US-014-criar-unidade-habitacional.md)
- [US-019: Desenhar Geometria no Mapa](./USER-STORIES/US-019-desenhar-geometria-no-mapa.md)
- [US-021: Validar Sobreposição de Geometrias](./USER-STORIES/US-021-validar-sobreposição-de-geometrias.md)

### Implementado em

---

## UC-002: Aprovar Unidade Habitacional
**Módulos:** GEOWEB, REURBCAD
**Épica:** performance

### Requisitos Funcionais (3)
- [RF-056: Status de Unidade](./FUNCTIONAL-REQUIREMENTS/RF-056-status-de-unidade.md)
- [RF-057: Aprovar Unidade](./FUNCTIONAL-REQUIREMENTS/RF-057-aprovar-unidade.md)
- [RF-060: Timeline de Unidade](./FUNCTIONAL-REQUIREMENTS/RF-060-timeline-de-unidade.md)

### User Stories (2)
- [US-034: Aprovar Unidade](./USER-STORIES/US-034-aprovar-unidade.md)
- [US-036: Solicitar Alterações](./USER-STORIES/US-036-solicitar-alterações.md)

### Implementado em

---

## UC-003: Vincular Titular a Unidade
**Módulos:** GEOAPI, GEOWEB, REURBCAD
**Épica:** security

### Requisitos Funcionais (8)
- [RF-061: Vincular Titular a Unidade](./FUNCTIONAL-REQUIREMENTS/RF-061-vincular-titular-a-unidade.md)
- [RF-062: Múltiplos Titulares por Unidade](./FUNCTIONAL-REQUIREMENTS/RF-062-multiplos-titulares-por-unidade.md)
- [RF-084: Criar Titular](./FUNCTIONAL-REQUIREMENTS/RF-084-criar-titular.md)
- [RF-089: Campos de Pessoa Física](./FUNCTIONAL-REQUIREMENTS/RF-089-campos-de-pessoa-fisica.md)
- [RF-090: Campos de Pessoa Jurídica](./FUNCTIONAL-REQUIREMENTS/RF-090-campos-de-pessoa-juridica.md)
- [RF-091: Tipos de Relacionamento com Unidade](./FUNCTIONAL-REQUIREMENTS/RF-091-tipos-de-relacionamento-com-unidade.md)
- [RF-092: Percentual de Propriedade](./FUNCTIONAL-REQUIREMENTS/RF-092-percentual-de-propriedade.md)
- [RF-093: Titular Principal](./FUNCTIONAL-REQUIREMENTS/RF-093-titular-principal.md)

### User Stories (2)
- [US-029: Vincular Titular a Unidade](./USER-STORIES/US-029-vincular-titular-a-unidade.md)
- [US-044: Cadastrar Titular no Campo](./USER-STORIES/US-044-cadastrar-titular-no-campo.md)

### Implementado em

---

## UC-004: Coletar Dados em Campo (Mobile)
**Módulos:** GEOWEB, REURBCAD
**Épica:** security

### Requisitos Funcionais (8)
- [RF-049: Criar Unidade](./FUNCTIONAL-REQUIREMENTS/RF-049-criar-unidade.md)
- [RF-063: Anexar Fotos a Unidade](./FUNCTIONAL-REQUIREMENTS/RF-063-anexar-fotos-a-unidade.md)
- [RF-064: Anexar Documentos a Unidade](./FUNCTIONAL-REQUIREMENTS/RF-064-anexar-documentos-a-unidade.md)
- [RF-122: Tirar Foto com Câmera (Mobile)](./FUNCTIONAL-REQUIREMENTS/RF-122-tirar-foto-com-câmera-mobile.md)
- [RF-123: Selecionar Foto da Galeria (Mobile)](./FUNCTIONAL-REQUIREMENTS/RF-123-selecionar-foto-da-galeria-mobile.md)
- [RF-182: Modo Offline (Mobile)](./FUNCTIONAL-REQUIREMENTS/RF-182-modo-offline-mobile.md)
- [RF-184: Criar Unidade Offline](./FUNCTIONAL-REQUIREMENTS/RF-184-criar-unidade-offline.md)
- [RF-186: Tirar Fotos Offline](./FUNCTIONAL-REQUIREMENTS/RF-186-tirar-fotos-offline.md)

### User Stories (3)
- [US-040: Cadastrar Unidade Offline](./USER-STORIES/US-040-cadastrar-unidade-offline.md)
- [US-042: Tirar Fotos com Câmera](./USER-STORIES/US-042-tirar-fotos-com-câmera.md)
- [US-044: Cadastrar Titular no Campo](./USER-STORIES/US-044-cadastrar-titular-no-campo.md)

### Implementado em

---

## UC-005: Sincronizar Dados Offline
**Módulos:** GEOAPI, GEOWEB, REURBCAD
**Épica:** security

### Requisitos Funcionais (8)
- [RF-187: Sincronização Manual](./FUNCTIONAL-REQUIREMENTS/RF-187-sincronização-manual.md)
- [RF-188: Sincronização Automática](./FUNCTIONAL-REQUIREMENTS/RF-188-sincronização-automática.md)
- [RF-189: Delta Sync (Sincronização Incremental)](./FUNCTIONAL-REQUIREMENTS/RF-189-delta-sync-sincronização-incremental.md)
- [RF-190: Detecção de Conflitos](./FUNCTIONAL-REQUIREMENTS/RF-190-detecção-de-conflitos.md)
- [RF-192: Endpoint de Pull](./FUNCTIONAL-REQUIREMENTS/RF-192-endpoint-de-pull.md)
- [RF-193: Endpoint de Push](./FUNCTIONAL-REQUIREMENTS/RF-193-endpoint-de-push.md)
- [RF-194: Limpeza de Dados Locais](./FUNCTIONAL-REQUIREMENTS/RF-194-limpeza-de-dados-locais.md)
- [RF-195: Indicador de Pendências](./FUNCTIONAL-REQUIREMENTS/RF-195-indicador-de-pendências.md)

### User Stories (3)
- [US-050: Sincronizar Manualmente](./USER-STORIES/US-050-sincronizar-manualmente.md)
- [US-051: Sincronização Automática](./USER-STORIES/US-051-sincronização-automática.md)
- [US-052: Ver Progresso de Sincronização](./USER-STORIES/US-052-ver-progresso-de-sincronização.md)

### Implementado em

---

## UC-006: Gerar Relatório de Comunidade
**Módulos:** GEOWEB
**Épica:** scalability

### Requisitos Funcionais (5)
- [RF-203: Relatório de Unidades por Status](./FUNCTIONAL-REQUIREMENTS/RF-203-relatório-de-unidades-por-status.md)
- [RF-204: Relatório de Titulares](./FUNCTIONAL-REQUIREMENTS/RF-204-relatório-de-titulares.md)
- [RF-205: Relatório de Progresso de Cadastramento](./FUNCTIONAL-REQUIREMENTS/RF-205-relatório-de-progresso-de-cadastramento.md)
- [RF-207: Geração Assíncrona de Relatórios](./FUNCTIONAL-REQUIREMENTS/RF-207-geração-assíncrona-de-relatórios.md)
- [RF-209: Ficha Técnica de Unidade (PDF)](./FUNCTIONAL-REQUIREMENTS/RF-209-ficha-técnica-de-unidade-pdf.md)

### User Stories (2)
- [US-074: Gerar Relatório de Comunidade](./USER-STORIES/US-074-gerar-relatório-de-comunidade.md)
- [US-075: Agendar Relatório Recorrente](./USER-STORIES/US-075-agendar-relatório-recorrente.md)

### Implementado em

---

## UC-007: Exportar Dados Geográficos
**Módulos:** GEOWEB, REURBCAD, GEOGIS
**Épica:** scalability

### Requisitos Funcionais (7)
- [RF-197: Exportar Unidades em Shapefile](./FUNCTIONAL-REQUIREMENTS/RF-197-exportar-unidades-em-shapefile.md)
- [RF-198: Exportar Unidades em KML/KMZ](./FUNCTIONAL-REQUIREMENTS/RF-198-exportar-unidades-em-kmlkmz.md)
- [RF-199: Exportar Unidades em GeoJSON](./FUNCTIONAL-REQUIREMENTS/RF-199-exportar-unidades-em-geojson.md)
- [RF-200: Exportar Unidades em CSV](./FUNCTIONAL-REQUIREMENTS/RF-200-exportar-unidades-em-csv.md)
- [RF-201: Exportar Unidades em Excel](./FUNCTIONAL-REQUIREMENTS/RF-201-exportar-unidades-em-excel.md)
- [RF-202: Exportar com Fotos/Documentos](./FUNCTIONAL-REQUIREMENTS/RF-202-exportar-com-fotosdocumentos.md)
- [RF-207: Geração Assíncrona de Relatórios](./FUNCTIONAL-REQUIREMENTS/RF-207-geração-assíncrona-de-relatórios.md)

### User Stories (2)
- [US-072: Exportar em Shapefile](./USER-STORIES/US-072-exportar-em-shapefile.md)
- [US-073: Exportar em Excel/CSV](./USER-STORIES/US-073-exportar-em-excelcsv.md)

### Implementado em

---

## UC-008: Importar Shapefile
**Módulos:** GEOWEB, REURBCAD, GEOGIS
**Épica:** scalability

### Requisitos Funcionais (4)
- [RF-040: Importar Shapefile de Comunidade](./FUNCTIONAL-REQUIREMENTS/RF-040-importar-shapefile-de-comunidade.md)
- [RF-067: Importar Unidades via Shapefile](./FUNCTIONAL-REQUIREMENTS/RF-067-importar-unidades-via-shapefile.md)
- [RF-139: Importar Shapefile em Camada](./FUNCTIONAL-REQUIREMENTS/RF-139-importar-shapefile-em-camada.md)
- [RF-140: Importar GeoJSON em Camada](./FUNCTIONAL-REQUIREMENTS/RF-140-importar-geojson-em-camada.md)

### User Stories (1)
- [US-020: Importar Unidades via Shapefile](./USER-STORIES/US-020-importar-unidades-via-shapefile.md)

### Implementado em

---

## UC-009: Gerenciar Processo de Legitimação Fundiária
**Módulos:** GEOWEB
**Épica:** scalability

### Requisitos Funcionais (8)
- [RF-172: Criar Processo de Legitimação](./FUNCTIONAL-REQUIREMENTS/RF-172-criar-processo-de-legitimação.md)
- [RF-173: Editar Processo](./FUNCTIONAL-REQUIREMENTS/RF-173-editar-processo.md)
- [RF-174: Listar Processos](./FUNCTIONAL-REQUIREMENTS/RF-174-listar-processos.md)
- [RF-175: Status de Processo](./FUNCTIONAL-REQUIREMENTS/RF-175-status-de-processo.md)
- [RF-176: Anexar Documentos ao Processo](./FUNCTIONAL-REQUIREMENTS/RF-176-anexar-documentos-ao-processo.md)
- [RF-177: Gerar Termo de Legitimação](./FUNCTIONAL-REQUIREMENTS/RF-177-gerar-termo-de-legitimação.md)
- [RF-179: Timeline de Processo](./FUNCTIONAL-REQUIREMENTS/RF-179-timeline-de-processo.md)
- [RF-180: Notificação de Mudança de Status](./FUNCTIONAL-REQUIREMENTS/RF-180-notificação-de-mudança-de-status.md)

### User Stories (3)
- [US-078: Criar Processo de Legitimação](./USER-STORIES/US-078-criar-processo-de-legitimação.md)
- [US-080: Aprovar ou Rejeitar Processo](./USER-STORIES/US-080-aprovarrejeitar-processo.md)
- [US-081: Gerar Termo de Legitimação (PDF)](./USER-STORIES/US-081-gerar-termo-de-legitimação-pdf.md)

### Implementado em

---

## UC-010: Configurar Camadas WMS/WMTS
**Módulos:** GEOAPI, GEOWEB, REURBCAD
**Épica:** performance

### Requisitos Funcionais (6)
- [RF-212: Adicionar Camada WMS](./FUNCTIONAL-REQUIREMENTS/RF-212-adicionar-camada-wms.md)
- [RF-213: Adicionar Camada WMTS](./FUNCTIONAL-REQUIREMENTS/RF-213-adicionar-camada-wmts.md)
- [RF-214: Testar Conexão WMS/WMTS](./FUNCTIONAL-REQUIREMENTS/RF-214-testar-conexão-wmswmts.md)
- [RF-215: Listar Camadas WMS/WMTS](./FUNCTIONAL-REQUIREMENTS/RF-215-listar-camadas-wmswmts.md)
- [RF-216: Editar Camada WMS/WMTS](./FUNCTIONAL-REQUIREMENTS/RF-216-editar-camada-wmswmts.md)
- [RF-221: Proxy de WMS/WMTS](./FUNCTIONAL-REQUIREMENTS/RF-221-proxy-de-wmswmts.md)

### User Stories (2)
- [US-064: Adicionar Camadas WMS](./USER-STORIES/US-064-adicionar-camadas-wms.md)
- [US-119: Gerenciar Serviços WMS/WMTS](./USER-STORIES/US-119-gerenciar-servicos-wmswmts.md)

### Implementado em

---

## UC-011: Gerenciar Equipes Técnicas
**Módulos:** GEOWEB, REURBCAD
**Épica:** security

### Requisitos Funcionais (3)
- [RF-024: Listar Usuários](./FUNCTIONAL-REQUIREMENTS/RF-024-listar-usuários.md)
- [RF-026: Criar Equipe (Team)](./FUNCTIONAL-REQUIREMENTS/RF-026-criar-equipe-team.md)
- [RF-050: Editar Unidade](./FUNCTIONAL-REQUIREMENTS/RF-050-editar-unidade.md)

### User Stories (1)
- [US-030: Gerenciar Equipes Técnicas](./USER-STORIES/US-030-gerenciar-equipes-técnicas.md)

### Implementado em

---

## Estatísticas
- **Total de UCs:** 11
- **Total de RFs referenciados:** 68
- **Total de USs referenciados:** 24
- **Total de RNFs referenciados:** 0
- **Média de RFs por UC:** 6.2
- **Média de USs por UC:** 2.2

---
**Última atualização:** 2026-01-10
