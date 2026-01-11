# Topography Workflow

Workflow de levantamento topográfico profissional via receptores GNSS RTK coletando coordenadas geodésicas de alta precisão (centímetros) para unidades críticas em comunidades onde GPS consumer mobile conforme [field data collection workflow](./01-field-data-collection-workflow.md) apresenta imprecisão inaceitável (3-10m typical) para processos judiciais de regularização fundiária, utilizando equipamento geodésico Trimble/Leica com pós-processamento de observáveis via estações de referência RBMC IBGE conforme normas técnicas INCRA gerando memorial descritivo com azimutes distâncias confrontantes e monografia técnica contendo método coleta datum projeção precisões atingidas assinado por responsável técnico (Engenheiro Agrimensor com CREA ativo) validando juridicamente limites de cada Unit para emissão de certidões de legitimação conforme legitimation workflow implementado em backend GEOAPI persistindo pontos levantados em SurveyPoint linked to Surveyor professional via SurveyProcessing session conectando RbmcStation post-processing e gerando DescriptiveMemorial com Monograph técnica conforme UC-topography use cases e regras de negócio em survey-validation.

## Atores

**Topógrafo/Agrimensor (Professional Surveyor):** Engenheiro Agrimensor ou Técnico em Geodésia com registro CREA ativo operando equipamento GNSS geodésico realizando levantamento em campo com precisão centimétrica, responsável técnico assinando memorial descritivo e monografia, cadastrado como Surveyor entity vinculado a Team com registro profissional CREA number validado.

**Analista GIS (GIS Analyst):** Técnico GIS desktop processando dados brutos GNSS via software Trimble Business Center ou Leica Geo Office importando observáveis de estações RBMC IBGE calculando coordenadas ajustadas gerando relatórios precisão validando quality control conforme workflow [analyst validation](./02-analyst-validation-workflow.md).

**Gestor Técnico (Technical Manager):** Coordenador aprovando memoriais descritivos e monografias verificando conformidade com normas INCRA NBR 13133 antes de submeter processos de legitimação conforme legitimation workflow.

## Steps do Workflow

### 1. Identificação de Unidades Críticas (Planning Phase)

**Critérios para levantamento topográfico profissional:**
1. **Unidades de alto valor:** Área >200m² ou valor venal elevado justificando investimento
2. **Contestações de limites:** Confrontantes disputando divisa entre units requer precisão judicial
3. **Áreas públicas adjacentes:** Limites com ruas praças áreas verdes exigem demarcação oficial
4. **Imprecisão GPS excessiva:** Units coletadas em [field data collection](./01-field-data-collection-workflow.md) com HDOP >5 ou multipath severo indicando coordenadas não confiáveis
5. **Requisito legal cartório:** Cartório de Registro de Imóveis exige memorial descritivo assinado por responsável técnico para matrícula

**Analista em GEOWEB marca units:**
- Status transitions APPROVED → REQUIRES_SURVEY via command handler RequestSurveyCommand conforme [unit-status-transitions](../BUSINESS-RULES/WORKFLOW-RULES/unit-status-transitions.md)
- Adiciona Annotation type SURVEY_REQUEST justificando: "Contestação de limite com vizinho - necessário levantamento GNSS"
- Sistema cria SurveyRequest entity linked to Unit com status PENDING

### 2. Preparação de Campo (Equipment Setup)

**Topógrafo em escritório antes de campo:**

#### 2.1 Seleção de Estações RBMC
1. Acessa portal IBGE RBMC https://www.ibge.gov.br/geociencias/informacoes-sobre-posicionamento-geodesico/rede-geodesica/16258-rede-brasileira-de-monitoramento-continuo-dos-sistemas-gnss-rbmc.html
2. Identifica estações de referência próximas à Community alvo (ideal <30km para baseline curta minimizando erros atmosféricos)
3. Cadastra stations como RbmcStation entities em GEOAPI:
   - Station code (exemplo: PARA - Curitiba/PR)
   - GeoPoint coordenadas geodésicas WGS84 homologadas IBGE
   - Antenna type, receiver model
   - Data availability period
4. Download observáveis RINEX das stations para janela temporal do levantamento planejado

#### 2.2 Configuração Equipamento GNSS
**Receptor Trimble R10 ou Leica GS18 com configurações:**
- **Modo operação:** RTK (Real-Time Kinematic) se celular 4G disponível com correção NTRIP, ou Static pós-processado se área sem sinal
- **Taxa coleta:** 1Hz (1 epoch/segundo) para static, 5Hz para RTK
- **Máscara elevação:** 15° eliminando satélites baixos no horizonte com multipath
- **GNSS systems:** GPS + GLONASS + Galileo + BeiDou (multi-constellation aumenta disponibilidade satélites)
- **Datum:** SIRGAS 2000 (oficial Brasil conforme IBGE)
- **Projeção:** UTM zona 22S ou 23S conforme longitude local

#### 2.3 Validação Equipamento
1. Verificação certificado calibração receptor (válido <2 anos)
2. Teste antenna cable resistance
3. Carga bateria interna (autonomia 8h) + bateria externa backup
4. Tablet controller com software Trimble Access instalado offline
5. Tripé, bastão com nível bolha, prisma refletor

### 3. Levantamento em Campo (Data Collection Phase)

**Topógrafo visita comunidade com equipamento GNSS:**

#### 3.1 Materialização de Marcos Geodésicos
1. Identifica pontos estratégicos estáveis para instalar marcos de referência (RN - Referência de Nível):
   - Cantos de construções permanentes (postes concreto, muros alvenaria)
   - Evita pontos móveis (portões, árvores, estruturas madeira)
2. Instala pinos metálicos ou marca tinta permanente identificando RN-001, RN-002, etc
3. Cria SurveyPoint type REFERENCE_BENCHMARK para cada RN
4. Fotografa marco com contexto identificável para relocação futura

#### 3.2 Coleta Estática GNSS (Static Survey)
**Para cada marco RN:**
1. Monta receptor GNSS sobre tripé nivelado com prumo laser centralizando antenna sobre marco
2. Mede altura instrumental (HI) do marco até phase center antenna com trena milimétrica (ex: 1.847m)
3. Configura coleta estática 60min minimum (ideal 120min para baseline >20km)
4. Receptor grava observáveis raw (carrier phase L1/L2, pseudorange C/A) em arquivo RINEX local
5. Anota metadados em caderneta campo:
   - RN ID, timestamp início/fim
   - Altura instrumental
   - Condições atmosféricas (temperatura, pressão, nuvens)
   - Obstruções (árvores, prédios próximos)
   - Número satélites visíveis, PDOP, HDOP
6. Repete para 3-4 marcos RN estabelecendo rede geodésica local densificada

#### 3.3 Levantamento RTK dos Vértices das Unidades
**Com rede local estabelecida, coleta vértices units:**
1. Topógrafo caminha perímetro de cada Unit marcada REQUIRES_SURVEY
2. Posiciona bastão GNSS em modo RTK sobre cada vértice (canto da construção, limite cerca)
3. Aguarda fixed solution (RTK FIXED com precisão <2cm horizontal)
4. Registra ponto no controller Trimble Access:
   - Point ID: UNIT-123-V1, UNIT-123-V2, etc (V = vértice)
   - Código feature: BUILDING_CORNER, FENCE_POST, SIDEWALK_EDGE
   - Attributes: Unit ID vinculado
5. Repete para todos vértices polígono unit (típico 4-8 vértices por unit retangular/irregular)
6. Valida closure error: distância entre primeiro e último vértice deve ser <5cm para polígono fechado
7. Fotografa cada vértice com contexto mostrando relação com construção

#### 3.4 Levantamento de Confrontantes e Referências
**Coleta pontos adicionais contexto:**
- Limites lote oficial (se existir demarcação física)
- Meio-fio ruas adjacentes definindo alinhamento
- Árvores significativas, postes de iluminação como pontos de amarração
- Construções vizinhas para verificar confrontações

**Todos pontos salvos em SurveyPoint com types:**
- UNIT_VERTEX: vértice unidade habitacional
- STREET_CURB: meio-fio rua
- REFERENCE_TREE: árvore referência
- NEIGHBOR_CORNER: canto construção vizinha

### 4. Pós-Processamento GNSS (Post-Processing Phase)

**Analista GIS em escritório com software Trimble Business Center:**

#### 4.1 Importação Dados Brutos
1. Download observáveis RINEX do receptor GNSS via USB ou WiFi sync
2. Download observáveis RINEX das estações RBMC IBGE para mesmo período temporal
3. Importa arquivos para projeto TBC creating SurveyProcessing session

#### 4.2 Processamento Baseline Diferencial
1. Software calcula baselines (vetores 3D) entre estação RBMC conhecida e cada RN coletado:
   - Resolve ambiguidades integer carrier phase L1/L2
   - Aplica correções atmosféricas (ionosfera, troposfera) modelando delay
   - Computa least squares adjustment propagando precisões
2. Output: Coordenadas geodésicas ajustadas WGS84/SIRGAS2000 para cada RN com precisões:
   - Horizontal (σH): <1cm typical para baseline <20km
   - Vertical (σV): <2cm typical
3. Valida quality indicators:
   - Ratio test >3.0 (ambiguity resolution confidence)
   - RMS residuals <1cm
   - Loop closure error <1:50000 (para rede com múltiplos RNs)

#### 4.3 Ajustamento de Rede Local
1. Com RNs ajustados como fixed control points, processa levantamento RTK dos vértices units
2. Transforma coordenadas WGS84 → SIRGAS2000 → UTM zona local via parâmetros IBGE
3. Calcula coordenadas planas E, N (metros) para cada vértice conforme Coordinates Value Object
4. Persiste SurveyPoint com coordenadas ajustadas e precisões em GEOAPI via POST /api/survey/points

#### 4.4 Reconstrução de Polígonos Units
1. Query vértices agrupados por Unit ID: `SELECT * FROM survey_points WHERE unit_id = 'X' ORDER BY point_id`
2. Constrói GeoPolygon WKT com coordenadas ajustadas substituindo geometria GPS imprecisa original
3. Valida topology PostGIS conforme [ADR-002: PostGIS](../../ARCHITECTURE/ADRs/ADR-002-postgresql-postgis.md):
   - ST_IsValid: polígono fechado sem self-intersections
   - ST_Area: área m² dentro de range esperado
   - ST_Overlaps: nenhum overlap com units vizinhas
4. PATCH /api/units/{id} atualizando geometry com polígono ajustado
5. Status transitions REQUIRES_SURVEY → SURVEYED via command handler CompleteSurveyCommand

### 5. Geração de Memorial Descritivo (Legal Documentation)

**Analista GIS gera DescriptiveMemorial para cada Unit:**

#### 5.1 Cálculo de Elementos Geométricos
**Software TBC ou QGIS calcula automaticamente:**
- **Perímetro total:** Soma de distâncias entre vértices consecutivos (ex: 42.87m)
- **Área:** Cálculo planar em m² (ex: 127.34m²)
- **Azimutes:** Ângulo horizontal de cada lado medido de Norte (ex: lado AB azimute 45°32'15")
- **Distâncias:** Comprimento horizontal de cada lado (ex: lado AB = 10.25m)
- **Vértices:** Coordenadas E, N de cada vértice numeradas sequencialmente

#### 5.2 Identificação de Confrontantes
**Analista documenta limites com base em observação campo e cadastro:**
- **Norte:** Rua João Silva (via pública)
- **Sul:** Lote de Maria Santos CPF 123.456.789-00 (Unit ID 456)
- **Leste:** Área verde pública (reserva)
- **Oeste:** Lote de José Oliveira CPF 987.654.321-00 (Unit ID 457)

#### 5.3 Redação Textual Memorial
**Formato legal padronizado:**

Memorial descritivo inicia com cabeçalho MEMORIAL DESCRITIVO seguido por parágrafo de localização descrevendo Imóvel situado na Rua Exemplo número cento e vinte e três Bairro Centro Município de Curitiba Estado do Paraná, seguido por seção DESCRIÇÃO GEOMÉTRICA iniciando descrição no vértice V1 de coordenadas E igual quinhentos mil metros N igual sete milhões e duzentos mil metros referência SIRGAS2000 UTM fuso vinte e dois sul, deste segue por linha reta com azimute quarenta e cinco graus trinta e dois minutos quinze segundos e distância dez vírgula vinte e cinco metros até vértice V2 coordenadas E quinhentos mil e sete vírgula vinte e quatro N sete milhões duzentos mil e sete vírgula vinte e sete confrontando neste lado com Rua João Silva via pública, deste segue linha reta azimute cento e trinta e cinco graus quarenta e cinco minutos trinta segundos distância doze vírgula quarenta e três metros até vértice V3 coordenadas E quinhentos mil quinze vírgula noventa e oito N sete milhões cento e noventa e nove mil novecentos e noventa e oito vírgula quarenta e cinco confrontando com lote de propriedade Maria Santos CPF cento e vinte e três ponto quatrocentos e cinquenta e seis ponto setecentos e oitenta e nove traço zero zero descrevendo perímetro completo com azimutes distâncias coordenadas e confrontantes conforme padrão legal cartorário.

[... continua para todos os lados fechando polígono ...]

encerrando o polígono no vértice V1, ponto inicial desta descrição.

ÁREA TOTAL: 127,34 m² (cento e vinte e sete metros quadrados e trinta e quatro decímetros quadrados)

PERÍMETRO: 42,87 m (quarenta e dois metros e oitenta e sete centímetros)

#### 5.4 Persistência em Banco
1. Memorial salvo como DescriptiveMemorial entity linked to Unit
2. Campos estruturados:
   - Unit ID foreign key
   - Full text memorial (markdown ou plain text)
   - Area m² calculated
   - Perimeter m calculated
   - Vertices JSON array com coordenadas
   - Confrontantes structured (norte, sul, leste, oeste)
   - Generated by user ID (analista)
   - Generated at timestamp
3. PDF gerado via template com brasão município, cabeçalho oficial, texto formatado
4. PDF armazenado como Document type DESCRIPTIVE_MEMORIAL linked to Unit

### 6. Geração de Monografia Técnica (Technical Report)

**Topógrafo responsável elabora Monograph para Unit:**

#### 6.1 Conteúdo Obrigatório Monografia
**Documento técnico conforme NBR 13133 contendo:**

1. **Identificação:**
   - Título: "Monografia de Levantamento Topográfico - Unidade 123"
   - Contratante: Prefeitura Municipal
   - Responsável técnico: Eng. João Silva CREA-PR 12345
   - Data levantamento: 2026-01-10

2. **Objetivo:**
   - "Levantamento geodésico de precisão para regularização fundiária conforme Lei 13.465/2017"

3. **Localização:**
   - Município, bairro, endereço aproximado
   - Coordenadas geográficas aproximadas
   - Mapa de situação

4. **Método de Levantamento:**
   - Equipamento utilizado: Trimble R10 GNSS RTK SN: 123456
   - Certificado calibração nº XYZ válido até 2027-05
   - Datum: SIRGAS2000
   - Projeção: UTM Zona 22 Sul
   - Modo: Static + RTK
   - Estações RBMC utilizadas: PARA, CUAB (distâncias: 15km, 28km)
   - Tempo ocupação estática: 90min per benchmark
   - Software pós-processamento: Trimble Business Center v5.0

5. **Precisões Atingidas:**
   - Horizontal (σH): 0.008m (8mm)
   - Vertical (σV): 0.015m (15mm)
   - Precisão relativa: 1:75000

6. **Marcos Geodésicos Implantados:**
   - RN-001: Pino metálico instalado em poste concreto E=500.000,00m N=7.200.000,00m H=900,234m
   - RN-002: Marca tinta em muro alvenaria E=500.050,12m N=7.200.045,87m H=899,987m
   - Croquis localização + fotos

7. **Observações:**
   - Condições climáticas: Céu claro, temperatura 25°C
   - Obstruções: Nenhuma significativa, skyview >80%
   - Multipath: Mínimo devido a área aberta

8. **Considerações Finais:**
   - Levantamento atende requisitos precisão para fins de regularização fundiária
   - Coordenadas atendem normas INCRA para georreferenciamento

9. **Assinatura Digital:**
   - Engenheiro Agrimensor João Silva
   - CREA-PR 12345
   - ART (Anotação Responsabilidade Técnica) nº 987654

#### 6.2 Persistência Monografia
1. Monografia redigida em Word/LibreOffice seguindo template padrão
2. Exportada para PDF assinado digitalmente com certificado A1/A3 do responsável técnico
3. Salva como Monograph entity em GEOAPI:
   - Unit ID foreign key
   - Surveyor ID foreign key (responsável técnico)
   - CREA registration number
   - Survey date
   - Equipment used
   - RBMC stations used
   - Achieved precision horizontal/vertical
   - Full text content (markdown)
   - PDF document as Document type MONOGRAPH
4. Status Unit transitions SURVEYED → SURVEY_APPROVED após gestor revisar e aprovar

### 7. Validação Técnica e Aprovação

**Gestor Técnico em GEOWEB revisa:**

#### 7.1 Checklist Validação
- [ ] Memorial descritivo texto correto, sem ambiguidades
- [ ] Área calculada conforme polígono ajustado
- [ ] Confrontantes identificados corretamente
- [ ] Monografia contém todos elementos obrigatórios NBR 13133
- [ ] Responsável técnico com CREA ativo (consulta web CREA)
- [ ] Precisões atingidas adequadas para finalidade (σH <2cm)
- [ ] Polígono não overlaps units vizinhas (validação PostGIS)
- [ ] PDF memorial e monografia assinados digitalmente

#### 7.2 Aprovação
1. Se conforme: Command handler ApproveSurveyCommand executa:
   - Status Unit transitions SURVEY_APPROVED → APPROVED
   - Annotation adicionada: "Levantamento topográfico aprovado - precisão 8mm horizontal"
   - Domain event SurveyApprovedEvent disparado conforme [ADR-010: Event-Driven](../../ARCHITECTURE/ADRs/ADR-010-event-driven-architecture.md)
2. Unit elegível para próximo workflow legitimation

#### 7.3 Rejeição
1. Se não conforme: Command handler RejectSurveyCommand executa:
   - Status transitions SURVEY_APPROVED → REQUIRES_SURVEY
   - Annotation com motivo: "Precisão insuficiente lado Norte - refazer coleta"
   - Notificação enviada topógrafo responsável para correção

### 8. Integração com Processo de Legitimação

**Units com survey aprovado:**
1. Memorial descritivo e monografia anexados ao processo administrativo de legitimação conforme legitimation workflow
2. Documentação técnica enviada para cartório de Registro de Imóveis juntamente com certidões
3. Coordenadas geodésicas SIRGAS2000 incluídas na matrícula do imóvel conforme Lei 10.267/2001 (georreferenciamento de imóveis rurais, aplicável analogicamente para REURB urbana)
4. Polígono ajustado exportado para Shapefile via [UC-007: Exportar Dados Geográficos](../../REQUIREMENTS/USE-CASES/UC-007-exportar-dados-geograficos.md) para envio a órgãos fiscalizadores

## Aggregates & Entities Envolvidas

**Survey Domain:**
- SurveyRequest entity requesting survey for unit
- Surveyor entity professional with CREA registration
- SurveyPoint entity cada ponto GNSS coletado
- RbmcStation entity estação referência IBGE
- SurveyProcessing entity session pós-processamento
- DescriptiveMemorial entity memorial descritivo legal
- Monograph entity relatório técnico NBR 13133

**Core Domain:**
- [UnitAggregate](../AGGREGATES/01-unit-aggregate.md) root coordenando survey entities
- Community agrupamento geográfico
- Document storing PDFs memorial/monograph
- Annotation justificativas survey requests/approvals

## Value Objects Utilizados

- Coordinates coordenadas geodésicas SIRGAS2000 + UTM planas
- GeoPolygon geometria unit ajustada com vértices precisos
- GeoPoint cada survey point WGS84/SIRGAS2000
- UnitStatus state machine REQUIRES_SURVEY → SURVEYED → SURVEY_APPROVED

## Business Rules Aplicadas

- survey-validation precisão mínima σH <2cm, CREA ativo, polígono fechado
- [unit-status-transitions](../BUSINESS-RULES/WORKFLOW-RULES/unit-status-transitions.md) transições APPROVED → REQUIRES_SURVEY → SURVEYED → SURVEY_APPROVED
- memorial-generation-rules formato legal memorial descritivo conforme NBR 13133

## Implementação

**Backend:** GEOAPI implementa survey domain com CQRS handlers RequestSurveyCommand CreateSurveyPointCommand CompleteSurveyCommand ApproveSurveyCommand validando server-side conforme [Clean Architecture](../../ARCHITECTURE/PATTERNS/01-clean-architecture.md), persistindo survey points em PostgreSQL+PostGIS via [ADR-002](../../ARCHITECTURE/ADRs/ADR-002-postgresql-postgis.md) armazenando coordenadas geodésicas com spatial indexes para queries eficientes, gerando PDFs memorial/monograph via template engine com assinatura digital certificado A1.

**Portal Web:** GEOWEB fornece interface para analistas e gestores revisarem survey data, visualizarem polígonos ajustados overlayed em mapa com ortofotos conforme WMS workflow, aprovarem/rejeitarem surveys com justificativas via forms validados client-side usando @carf/tscore, e exportarem relatórios consolidados multiple units usando @carf/geoapi-client consumindo API endpoints.

**Software Externo:** Trimble Business Center ou Leica Geo Office para pós-processamento GNSS não integrado diretamente com CARF, analista importa coordenadas ajustadas via CSV upload ou API batch POST /api/survey/points/batch endpoint processando até 1000 pontos por request.

## Métricas

- **Custo:** R$ 500-1500 per unit dependendo área complexidade (equipamento GNSS ~R$ 80k amortizado em 1000 levantamentos)
- **Tempo levantamento:** 2-4h campo per unit (inclui deslocamento, setup, coleta RNs + vértices)
- **Tempo pós-processamento:** 1-2h escritório per unit (processamento, ajustamento, geração memorial)
- **Precisão típica:** σH = 0.5-1.5cm (horizontal), σV = 1.0-3.0cm (vertical) para baseline <30km
- **Taxa aprovação:** ~98% surveys aprovados na primeira submissão quando seguem protocolo
- **% Units requerendo survey:** ~5-10% total units em community (somente críticas conforme critérios)

## Conformidade Normativa

**Normas técnicas aplicáveis:**
- **NBR 13133:1994** - Execução de levantamento topográfico
- **NBR 14166:1998** - Rede de referência cadastral municipal
- **Lei 10.267/2001** - Georreferenciamento de imóveis rurais (aplicável analogicamente)
- **Norma Técnica INCRA 2ª Edição** - Georreferenciamento de imóveis rurais
- **Lei 13.465/2017 Art. 11 §2º** - Memorial descritivo como documento obrigatório REURB

---

**Última atualização:** 2026-01-10
