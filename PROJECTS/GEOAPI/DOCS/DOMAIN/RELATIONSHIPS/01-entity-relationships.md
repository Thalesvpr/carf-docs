---
type: leaf
status: review
updated: 2026-02-08
---

# Entity Relationships

Mapeamento completo de relacionamentos entre entidades do dominio especificando cardinalidades, direcoes de navegacao e regras de integridade referencial de forma agnostica a tecnologia.

## Relacionamentos Hierarquicos

| Origem | Destino | Cardinalidade | Obrigatorio | Descricao |
|--------|---------|---------------|-------------|-----------|
| Community | Unit | 1:N | sim (em Unit) | Comunidade agrupa multiplas unidades. community_id obrigatorio em units. |
| Community | Block | 1:N | sim (em Block) | Comunidade subdividida em quadras. Opcional em areas rurais. |
| Block | Plot | 1:N | sim (em Plot) | Quadra contem multiplos lotes. |
| Unit | Plot | N:1 | nao | Unidade pode estar vinculada a lote especifico. Ausente em ocupacoes informais. |
| Unit | Building | N:1 | nao | Unidade pode pertencer a edificacao (predio, vila). |
| Plot | Building | 1:N | nao | Edificacao pode existir sem lote formal (plot_id nullable). |

## Relacionamentos N:N (via tabela associativa)

| Origem | Destino | Tabela Associativa | Campos Extras | Descricao |
|--------|---------|-------------------|---------------|-----------|
| Unit | Holder | unit_holders | relationship_type, ownership_percentage, is_primary | Vinculo titular-unidade com tipo e percentual. |
| Team | Account | team_members | role (COORDINATOR, CADASTRATOR), joined_at, left_at | Membros de equipe com papel e periodo. |
| Community | Team/Account | community_authorizations | permission_level, team_id XOR account_id | Controle de acesso granular por comunidade. |

## Relacionamentos Polimorficos

| Entidade | Alvo | Campos | Descricao |
|----------|------|--------|-----------|
| Document | UNIT, HOLDER, COMMUNITY | entity_type, entity_id | Anexos vinculados a qualquer entidade. |
| Annotation | UNIT, HOLDER, COMMUNITY | entity_type, entity_id | Observacoes vinculadas a qualquer entidade. |

## Relacionamentos de Legitimacao

| Origem | Destino | Cardinalidade | Descricao |
|--------|---------|---------------|-----------|
| LegitimationRequest | Unit | N:1 | Solicitacao vinculada a unidade. UNIQUE parcial impedindo dois processos ativos para mesma unit. |
| LegitimationRequest | LegitimationResponse | 1:N | Pareceres multiplos ao longo do processo. |
| LegitimationRequest | LegitimationCertificate | 1:0..1 | Certidao emitida apos aprovacao. |
| DescriptiveMemorial | Unit | N:1 | Memorial descritivo da unidade. FK CertificateId nullable. |
| LegitimationPlan | Unit | N:1 | Planta tecnica. FKs MemorialId (obrigatorio) e CertificateId (nullable). |

## Relacionamentos de Ortofotos e Topografia

| Origem | Destino | Cardinalidade | Descricao |
|--------|---------|---------------|-----------|
| Ortofoto | Community | N:1 | Ortofoto opcional vinculada a comunidade. community_id nullable. |
| SurveyPoint | Community | N:1 | Pontos topograficos pertencem a comunidade. |

## Regras Gerais de Integridade

| Regra | Descricao |
|-------|-----------|
| FK obrigatorio | Relacionamentos N:1 obrigatorios validam existencia da FK antes de criar. |
| Soft delete preferencial | Cascade delete usa soft delete quando possivel, preservando historico. |
| Navegacao bidirecional | Navegacoes bidirecionais devem manter consistencia em ambos os lados. |
| Referencia por ID | Agregados referenciam outros agregados por ID, nao por objeto, evitando acoplamento. |
