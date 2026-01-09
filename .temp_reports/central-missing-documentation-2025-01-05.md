# CENTRAL/ - Documentação Faltante
**Data:** 2025-01-05
**Status:** Análise de gaps de conteúdo (pós-agnosticismo)

---

## 🚨 GAPS CRÍTICOS ENCONTRADOS

### Resumo Executivo

| Tipo | Esperado | Documentado | Faltando | % Completo |
|------|----------|-------------|----------|------------|
| **Entidades** | 33 | 5 | **28** | 15% ❌ |
| **Value Objects** | 23 | 6 | **17** | 26% ❌ |
| **Aggregates** | 3 | 1 | **2** | 33% ❌ |
| **Workflows** | ~10-15 | 1 | **~9-14** | <10% ❌ |

**CONCLUSÃO:** CENTRAL/TECHNICAL/DOMAIN-MODEL está apenas **~20% completo**! 🔴

---

## 📋 ENTIDADES FALTANTES (28 de 33)

### ✅ Documentadas (5)
1. Unit
2. Holder
3. Community
4. Contestation
5. PdfTemplates

### ❌ FALTANDO - Prioridade CRÍTICA (Core Domain - 8)
- **Team** - Equipe de trabalho agrupando usuários
- **Account** - Usuário do sistema vinculado a tenant
- **Tenant** - Cliente multi-tenant com isolamento RLS
- **Block** - Quadra urbana subdividindo comunidade
- **Plot** - Lote individual dentro de quadra
- **Document** - Arquivo anexo polimórfico
- **Annotation** - Anotação/observação/issue polimórfico
- **UnitHolder** - Relacionamento N:N Unit-Holder

### ❌ FALTANDO - Prioridade ALTA (Legitimação - 5)
- **LegitimationRequest** - Solicitação legitimação
- **LegitimationResponse** - Parecer técnico
- **LegitimationCertificate** - Certidão oficial
- **DescriptiveMemorial** - Memorial descritivo técnico
- **LegitimationPlan** - Planta técnica gráfica

### ❌ FALTANDO - Prioridade ALTA (Topografia - 5)
- **Surveyor** - Topógrafo profissional
- **SurveyPoint** - Ponto topográfico GPS
- **RbmcStation** - Estação RBMC IBGE
- **SurveyProcessing** - Processamento dados GPS
- **Monograph** - Monografia ponto topográfico

### ❌ FALTANDO - Prioridade MÉDIA (Auth/Mobile - 6)
- **Session** - Sessão usuário autenticado
- **ApiKey** - Chave API integrações
- **TeamMember** - Relacionamento Account-Team
- **CommunityAuthorization** - Autorização Team/Account-Community
- **Role** - Papel de permissões customizado
- **Permission** - Permissão individual granular
- **SyncLog** - Registro sincronização offline

### ❌ FALTANDO - Prioridade BAIXA (GIS/Auditoria - 5)
- **Layer** - Camada mapa customizada
- **LayerFeature** - Geometria individual em Layer
- **WmsServer** - Servidor WMS externo
- **WmsLayer** - Camada WMS
- **AuditLog** - Log de auditoria operações CUD

---

## 📋 VALUE OBJECTS FALTANTES (17 de 23)

### ✅ Documentados (6)
1. Cpf
2. GeoPolygon
3. UnitStatus
4. CustomDataSchema
5. PermissionsMatrix
6. SpatialOverlapMatrix

### ❌ FALTANDO - Prioridade CRÍTICA (4)
- **GeoPoint** - Ponto geográfico lat/lng validado
- **Email** - Email RFC 5322 validado
- **Address** - Endereço brasileiro completo
- **PhoneNumber** - Telefone brasileiro com DDD

### ❌ FALTANDO - Prioridade ALTA (6)
- **CommunityType** - URBANA RURAL QUILOMBOLA RIBEIRINHA
- **SyncStatus** - PENDING SUCCESS CONFLICT FAILED
- **TeamRole** - LEADER MEMBER
- **DocumentType** - PHOTO_FRONT DOC_CPF PLANT MEMORIAL
- **LegitimationStatus** - 11 estados workflow legitimação
- **Decision** - APPROVED REJECTED NEEDS_CORRECTION

### ❌ FALTANDO - Prioridade MÉDIA (7)
- **PointType** - MARCO PIQUETE NATURAL
- **PointStatus** - COLLECTED PROCESSED APPROVED REJECTED
- **CertificateSituation** - COVERED CONFRONTING BOTH
- **Crea** - Registro profissional CREA validado
- **ApiKeyValue** - Formato geoapi_sk_xxx
- **Priority** - LOW NORMAL HIGH URGENT
- **AnnotationType** - NOTE WARNING ISSUE REMINDER
- **Role** - SUPER_ADMIN ADMIN MANAGER ANALYST FIELD_AGENT
- **EntityType** - UNIT HOLDER COMMUNITY (polimórfico)

---

## 📋 AGGREGATES FALTANTES (2 de 3)

### ✅ Documentados (1)
1. Unit Aggregate

### ❌ FALTANDO (2)
- **Community Aggregate** - Community + Blocks + CommunityAuthorizations
- **LegitimationRequest Aggregate** - Request + Responses + Certificate + Memorial + Plan

---

## 🎯 PLANO DE AÇÃO PRIORIZADO

### FASE 1: CORE DOMAIN (Prioridade CRÍTICA) - ~20 arquivos
**Entidades (8):** Team, Account, Tenant, Block, Plot, Document, Annotation, UnitHolder
**Value Objects (4):** GeoPoint, Email, Address, PhoneNumber
**Workflows (3):** Cadastro Unidade, Sincronização Offline, Processo Legitimação

### FASE 2: LEGITIMAÇÃO (Prioridade ALTA) - ~8 arquivos
**Entidades (5):** LegitimationRequest, LegitimationResponse, LegitimationCertificate, DescriptiveMemorial, LegitimationPlan
**Value Objects (2):** LegitimationStatus, Decision
**Aggregate (1):** LegitimationRequest Aggregate

### FASE 3: TOPOGRAFIA (Prioridade ALTA) - ~9 arquivos
**Entidades (5):** Surveyor, SurveyPoint, RbmcStation, SurveyProcessing, Monograph
**Value Objects (3):** PointType, PointStatus, CertificateSituation
**Workflows (1):** Coleta Topográfica

### FASE 4: AUTH/MOBILE (Prioridade MÉDIA) - ~16 arquivos
**Entidades (7):** Session, ApiKey, TeamMember, CommunityAuthorization, Role, Permission, SyncLog
**Value Objects (8):** CommunityType, SyncStatus, TeamRole, DocumentType, ApiKeyValue, AnnotationType, Priority, Role, EntityType
**Aggregate (1):** Community Aggregate

### FASE 5: GIS/AUDITORIA (Prioridade BAIXA) - ~6 arquivos
**Entidades (5):** Layer, LayerFeature, WmsServer, WmsLayer, AuditLog
**Workflows (1):** Geração Relatórios

---

## 📊 TOTAL ESTIMADO: ~54-59 arquivos faltantes

---

## 💡 CONCLUSÃO

**Você estava CERTO:** CENTRAL/ está apenas ~20% completo!

**Faltam ~54-59 arquivos** de documentação conceitual.

**Próximo passo:** Começar FASE 1 (Core Domain) - 20 arquivos mais críticos.

---

**Gerado:** 2025-01-05
