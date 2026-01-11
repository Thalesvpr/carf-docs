# DOMAIN-MODEL - Índice Completo

Índice de todas entidades value objects aggregates workflows e business rules do modelo de domínio CARF documentando arquitetura conceitual 100% technology-agnostic baseada no workflow REAL descoberto implementado pelo sistema.

## Entities (33 conceitos - 100% documentados)

### Core Domain (3)
1. **Unit** - Unidade habitacional em processo de regularização fundiária (aggregate root)
2. **Holder** - Pessoa física titular ocupante ou interessado em unidade
3. **Community** - Comunidade ou assentamento que agrupa unidades geograficamente

### Multi-Tenancy & Acesso (8)
4. **Tenant** - Cliente do sistema multi-tenant com isolamento RLS
5. **Account** - Usuário do sistema vinculado a tenant e Keycloak
6. **Team** - Equipe de trabalho agrupando usuários para atribuição de comunidades
7. **TeamMember** - Relacionamento N:N Account-Team com role
8. **CommunityAuthorization** - Autorização Team ou Account para Community com CRUD granular
9. **Block** - Quadra urbana subdividindo comunidade
10. **Plot** - Lote individual dentro de quadra
11. **Document** - Arquivo anexo polimórfico (foto PDF planta)

### Suporte (2)
12. **Annotation** - Anotação observação issue ou lembrete polimórfico
13. **UnitHolder** - Relacionamento N:N Unit-Holder com tipo e percentual de propriedade

### Topografia & Survey (6)
14. **Surveyor** - Topógrafo profissional responsável por levantamentos com licença CREA
15. **SurveyPoint** - Ponto topográfico coletado em campo com coordenadas GPS
16. **RbmcStation** - Estação RBMC do IBGE para correção GPS diferencial
17. **SurveyProcessing** - Processamento de dados GPS com precisões calculadas
18. **Monograph** - Monografia de ponto topográfico com fotos e croqui
19. **DescriptiveMemorial** - Memorial descritivo técnico com coordenadas NBR

### Legitimação Fundiária (4)
20. **LegitimationRequest** - Solicitação de legitimação fundiária para unidade (aggregate root)
21. **LegitimationResponse** - Parecer técnico de solicitação de legitimação
22. **LegitimationCertificate** - Certidão oficial de legitimação fundiária
23. **LegitimationPlan** - Planta técnica gráfica DWG/PDF

### WMS/Ortofoto (2)
24. **WmsServer** - Servidor WMS externo configurado para ortofotos de drone/aerofotogrametria
25. **WmsLayer** - Camada individual disponível em WmsServer

### GIS Customizado (2 - opcional)
26. **Layer** - Camada de mapa interna com dados vetoriais customizados
27. **LayerFeature** - Geometria individual dentro de Layer

### Security & Sessions (3)
28. **Session** - Sessão de usuário autenticado com hash de token
29. **ApiKey** - Chave de API para integrações externas (plugins GIS)
30. **Role** - Papel de permissões customizado (entity se implementado)

### Audit & Sync (3)
31. **SyncLog** - Registro de sincronização offline mobile com detecção de conflitos
32. **AuditLog** - Log de auditoria de operações CUD
33. **Permission** - Permissão individual granular (entity se implementado)

## Value Objects (25 conceitos - 100% documentados)

### Identificação & Documentos (3)
1. **Cpf** - CPF brasileiro validado com dígitos verificadores
2. **Cnpj** - CNPJ brasileiro validado com dígitos verificadores
3. **Crea** - Registro profissional CREA validado (CREA-UF NNNNNN)

### Dados Pessoais (4)
4. **Email** - Email RFC 5322 validado
5. **PhoneNumber** - Telefone brasileiro com DDD validado
6. **Address** - Endereço brasileiro completo estruturado
7. **ApiKeyValue** - Valor chave API formato geoapi_sk_xxx

### Geografia & Geometria (3)
8. **GeoPolygon** - Polígono geográfico WKT/GeoJSON
9. **GeoPoint** - Ponto geográfico lat/lng validado
10. **Coordinates** - Sistema de coordenadas SIRGAS/WGS84

### Status & Workflow (4)
11. **UnitStatus** - Status workflow unidade (DRAFT PENDING IN_REVIEW APPROVED REJECTED REQUIRES_CHANGES)
12. **LegitimationStatus** - Status processo legitimação (11 estados workflow conforme Lei 13465/2017)
13. **SyncStatus** - Status sincronização (PENDING SUCCESS CONFLICT FAILED)
14. **PointStatus** - Status ponto topográfico (COLLECTED PROCESSED APPROVED REJECTED)

### Tipos & Classificações (8)
15. **CommunityType** - Tipo comunidade (URBANA RURAL QUILOMBOLA INDIGENA RIBEIRINHA)
16. **EntityType** - Tipo entidade polimórfico (UNIT HOLDER COMMUNITY BLOCK etc)
17. **DocumentType** - Tipo documento (PHOTO_FRONT DOC_CPF PLANT_DWG MEMORIAL etc)
18. **AnnotationType** - Tipo anotação (NOTE WARNING ISSUE REMINDER)
19. **PointType** - Tipo ponto topográfico (MARCO PIQUETE NATURAL)
20. **Decision** - Decisão parecer (APPROVED REJECTED NEEDS_CORRECTION APPROVED_WITH_CONDITIONS)
21. **CertificateSituation** - Situação certidão (COVERED CONFRONTING BOTH)
22. **Priority** - Prioridade (LOW NORMAL HIGH URGENT)

### Roles & Permissões (3)
23. **TeamRole** - Papel em equipe (LEADER MEMBER)
24. **Role** - Papel usuário sistema (SUPER_ADMIN ADMIN MANAGER ANALYST FIELD_AGENT) se implementado como VO
25. **SyncDirection** - Direção sync (PULL PUSH BIDIRECTIONAL) se implementado

## Aggregates (3 principais - 100% documentados)

1. **Unit Aggregate** - Unit raiz + UnitHolder + Documents + Annotations + SurveyPoints
2. **Community Aggregate** - Community raiz + Blocks + CommunityAuthorizations + Documents
3. **LegitimationRequest Aggregate** - Request raiz + Responses + Certificate + Memorial + Plan + Contestations

## Workflows (5 principais - 100% documentados)

1. **field-data-collection-workflow** - Coleta offline mobile com sync pull/push e conflict resolution
2. **analyst-validation-workflow** - Correção em massa QGIS usando ortofoto WMS como referência
3. **topography-workflow** - Levantamento GNSS profissional com pós-processamento RBMC
4. **legitimation-workflow** - Processo completo 11 estados conforme Lei 13465/2017
5. **wms-integration-workflow** - Configuração e consumo de ortofotos drone via WMS/WMTS OGC

## Business Rules (7 principais - 100% documentados)

### VALIDATION-RULES (2)
1. **holder-validation** - Validação de Holder (CPF/CNPJ, unicidade, LGPD, UnitHolder)
2. **unit-validation** - Validação de Unit (code, geometria, área, spatial overlap)

### WORKFLOW-RULES (2)
3. **unit-status-transitions** - State machine Unit (6 estados + transições permitidas)
4. **legitimation-status-transitions** - State machine LegitimationRequest (11 estados Lei 13465/2017)

### LEGITIMATION-RULES (3)
5. **reurb-s-requirements** - Requisitos REURB-S (interesse social: ≤250sqm, gratuito)
6. **reurb-e-requirements** - Requisitos REURB-E (interesse específico: ≤500sqm, taxa)
7. **contestation-rules** - Regras contestações administrativas (30 dias, análise, recursos)

## Workflow REAL Documentado

Documentação baseada no workflow REAL descoberto via exploração do codebase:

**1. Drone/Aerofotogrametria →** Levantamento aéreo gera ortofoto + pontos de controle GPS
**2. WMS/WMTS →** Ortofoto publicada via servidor OGC (NÃO armazenada no sistema)
**3. Campo Mobile →** Equipe visita casas coletando dados offline (Unit + Holder + fotos)
**4. QGIS Desktop →** Analistas corrigem geometrias EM MASSA usando ortofoto como base
**5. Topografia RBMC →** Topógrafo processa GPS com estações IBGE melhorando acurácia metros→centímetros
**6. Legitimação →** Gestor conduz workflow 11 estados até emissão de certidão

## Isolamento de Dados (Multi-Tenancy + Município)

**Tenant (Instituição):** ITERJ, Prefeitura, empresa topografia - isolamento via RLS
**Community (com campo municipio):** Isolamento geográfico estruturado
**Team + CommunityAuthorization:** Controle operacional de acesso (quem edita qual comunidade)
**Mobile Offline Sync:** Baixa SOMENTE comunidades autorizadas para Team do usuário

## Technology-Agnostic Principle

**CRITICAL:** CENTRAL/TECHNICAL/ NÃO menciona implementações específicas:

**Proibido mencionar:**
- ❌ PostgreSQL, WatermelonDB, SQLite (usar: "banco de dados relacional", "banco local embarcado")
- ❌ React Native, React, .NET, FastAPI (usar: "aplicação mobile", "backend API")
- ❌ QGIS especificamente (usar: "ferramenta GIS desktop com plugin")
- ❌ NetTopologySuite, Turf.js (usar: "biblioteca geometria computacional")
- ❌ Keycloak especificamente (usar: "provedor de identidade OAuth2/OIDC")

**Detalhes de implementação pertencem a:** (detalhes de implementação em cada projeto)

## Implementações por Projeto

Cada conceito documentado tem implementação específica em:
- **Backend .NET:** (detalhes de implementação em cada projeto) (entities, VOs, aggregates, workflows, rules)
- **Frontend React:** (detalhes de implementação em cada projeto) (interfaces TypeScript, validations)
- **Mobile React Native:** (detalhes de implementação em cada projeto) (entities com banco local, sync offline)
- **Plugin GIS Python:** (detalhes de implementação em cada projeto) (classes Python, bulk operations)

## Status de Completude

✅ **ENTITIES:** 33/33 (100%)
✅ **VALUE OBJECTS:** 25/25 (100%)
✅ **AGGREGATES:** 3/3 (100%)
✅ **WORKFLOWS:** 5/5 (100%)
✅ **BUSINESS RULES:** 7/7 (100%)

**CENTRAL/TECHNICAL/DOMAIN-MODEL: 100% COMPLETO**

Total de arquivos documentados: ~70 arquivos markdown

---

**Última atualização:** 2025-01-05
