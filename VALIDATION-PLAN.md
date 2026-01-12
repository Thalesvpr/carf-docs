# Plano de Validação da Documentação CARF

Plano sistemático validação qualidade coesão consistência documentação CARF garantindo estrutura lógica rastreabilidade completa ausência contradições gaps informacionais facilitando onboarding desenvolvedores compreensão arquitetura sistema regularização fundiária urbana.

## 1. Validações Automáticas

### 1.1 Dense Paragraph Format
```bash
python .scripts/lint-dense-paragraph.py
```

**Verifica:**
- ✅ CENTRAL/ ZERO code blocks (apenas prosa densa)
- ✅ PROJECTS/FEATURES/ >= 100 palavras (não stub files)
- ✅ READMEs <= 5 links por parágrafo (evita link spam)
- ✅ Max 2 linhas vazias consecutivas (dense paragraph)

**Critérios:**
- CENTRAL deve ser 100% prosa sem exemplos código
- FEATURES devem ter conteúdo substancial (min 100 palavras)
- Parágrafos densos sem quebras excessivas

### 1.2 Arquivos Isolados
```bash
python .scripts/list-isolated-simple.py
```

**Verifica:**
- ✅ Arquivos sem links incoming/outgoing
- ✅ Documentação orfã não conectada grafo
- ✅ SRC-CODE/ ignorado (esperado isolado)

**Critérios:**
- DOCS/ deve ter ZERO arquivos isolados
- Tudo conectado via links READMEs estruturantes

### 1.3 Links Quebrados
```bash
python .scripts/check-links.py
```

**Verifica:**
- ✅ Links markdown [texto](caminho) apontam arquivos existentes
- ✅ Âncoras #secao existem nos arquivos linkados
- ✅ Caminhos relativos corretos

**Critérios:**
- ZERO links quebrados em CENTRAL/ e PROJECTS/DOCS/
- Warnings aceitáveis para links externos (HTTP)

### 1.4 Estrutura de Diretórios
```bash
find PROJECTS/*/DOCS -type d | sort
```

**Verifica:**
- ✅ Estrutura padronizada: ARCHITECTURE/ CONCEPTS/ HOW-TO/ FEATURES/
- ✅ README.md em cada diretório
- ✅ Ausência diretórios vazios ou desnecessários

**Critérios:**
- Todos projetos seguem mesma estrutura
- Exceções documentadas (LIB tem API/, KEYCLOAK tem REFERENCE/)

## 2. Validações de Consistência

### 2.1 Rastreabilidade Requirements
```bash
python .scripts/generate-traceability-matrix.py --validate
```

**Verifica:**
- ✅ UC-XXX citados em FEATURES existem em CENTRAL/REQUIREMENTS/USE-CASES/
- ✅ RF-XXX citados existem em FUNCTIONAL-REQUIREMENTS/
- ✅ US-XXX citados existem em USER-STORIES/
- ✅ Bidirecional: UC aponta RF, RF aponta implementação PROJECTS/

**Critérios:**
- ZERO referências órfãs (UC-999 inexistente)
- Rastreabilidade completa UC -> RF -> US -> Implementação

### 2.2 Nomenclatura Técnica
```bash
grep -r "REURB" CENTRAL PROJECTS --include="*.md" | grep -v "REURB-S\|REURB-E"
```

**Verifica:**
- ✅ REURB sempre qualificado -S ou -E
- ✅ PostgreSQL (não Postgres, PG, psql inconsistente)
- ✅ Keycloak (não KeyCloak, keycloak)
- ✅ React Native (não ReactNative, react-native)

**Critérios:**
- Terminologia unificada em toda documentação
- Glossário implícito consistente

### 2.3 Stack Tecnológica
```bash
grep -r "React 18" PROJECTS/*/DOCS/README.md
grep -r ".NET 9" PROJECTS/*/DOCS/README.md
```

**Verifica:**
- ✅ GEOWEB menciona React 18, Vite 5, TanStack Query v5
- ✅ REURBCAD menciona React Native 0.74, Expo 51
- ✅ GEOAPI menciona .NET 9, EF Core, PostgreSQL 16
- ✅ Versões consistentes entre ARCHITECTURE/ e FEATURES/

**Critérios:**
- Versões tecnologias corretas em todos lugares
- Sem contradições "React 17" num lugar "React 18" outro

### 2.4 Referências Cruzadas CENTRAL <-> PROJECTS
```bash
grep -r "CENTRAL/" PROJECTS/*/DOCS --include="*.md" | wc -l
grep -r "PROJECTS/" CENTRAL --include="*.md" | wc -l
```

**Verifica:**
- ✅ PROJECTS/FEATURES/ linkam CENTRAL/REQUIREMENTS/USE-CASES/
- ✅ CENTRAL/DOMAIN-MODEL/ referencia implementações PROJECTS/
- ✅ Bidirecionalidade referências

**Critérios:**
- Interconexão clara CENTRAL (especificação) e PROJECTS (implementação)
- Nenhum projeto documenta features sem ligar requisitos CENTRAL

## 3. Validações de Completude

### 3.1 Estrutura Projetos Completa
```bash
for proj in ADMIN GEOAPI GEOGIS GEOWEB KEYCLOAK REURBCAD WEBDOCS; do
  echo "=== $proj ==="
  ls -d PROJECTS/$proj/DOCS/*/ 2>/dev/null || echo "MISSING DIRS"
done
```

**Verifica:**
- ✅ Todos projetos tem ARCHITECTURE/ CONCEPTS/ HOW-TO/
- ✅ Projetos aplicação (não lib) tem FEATURES/
- ✅ Cada diretório tem README.md

**Critérios:**
- Estrutura mínima completa
- Exceções justificadas (WEBDOCS sem FEATURES ok)

### 3.2 Casos de Uso Implementados
```bash
python .scripts/validate-uc-coverage.py
```

**Verifica:**
- ✅ UC-001 a UC-011 existem CENTRAL/REQUIREMENTS/USE-CASES/
- ✅ Cada UC tem pelo menos 1 feature PROJECTS/ implementando
- ✅ Features órfãs (não implementam nenhum UC) identificadas

**Critérios:**
- Todos UCs principais implementados
- Features documentadas rastreiam UCs

### 3.3 Requisitos Funcionais Cobertos
```bash
python .scripts/validate-rf-coverage.py
```

**Verifica:**
- ✅ RF-001 a RF-221 existem CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/
- ✅ Cada RF citado em FEATURES existe
- ✅ RFs críticos (autenticação, multi-tenancy) implementados

**Critérios:**
- RFs core sistema todos cobertos
- RFs secundários podem ter implementação futura

### 3.4 Features Documentadas vs Implementadas
```bash
ls PROJECTS/*/DOCS/FEATURES/*.md | wc -l
find PROJECTS/*/SRC-CODE -name "*.tsx" -o -name "*.ts" -o -name "*.cs" | wc -l
```

**Verifica:**
- ✅ Features DOCS correspondem features SRC-CODE
- ✅ Código sem documentação identificado (grep TODOs)
- ✅ Documentação sem código identificado

**Critérios:**
- Proporção razoável docs:code
- Features principais todas documentadas

## 4. Validações de Qualidade Textual

### 4.1 Seções Padronizadas Features
```bash
for f in PROJECTS/*/DOCS/FEATURES/*.md; do
  grep -q "## Validações" "$f" && echo "$f OK" || echo "$f MISSING Validações"
  grep -q "## API Integration\|## Integração API" "$f" && echo "$f OK" || echo "$f MISSING API"
  grep -q "## Relacionamentos\|## Domain Model" "$f" && echo "$f OK" || echo "$f MISSING Relacionamentos"
done
```

**Verifica:**
- ✅ FEATURES tem seções consistentes: Validações, API Integration, Domain Model/Relacionamentos
- ✅ Padrão seguido em todos arquivos

**Critérios:**
- Estrutura interna features padronizada
- Leitores sabem onde encontrar informações (validações sempre seção 2, API sempre seção 3)

### 4.2 Idioma Português
```bash
grep -r "the\|and\|for\|with" CENTRAL --include="*.md" | grep -v "ARCHITECTURE/ADRs" | head -20
```

**Verifica:**
- ✅ Prosa em português (exceto termos técnicos inglês)
- ✅ ADRs podem ter inglês (padrão internacional)
- ✅ Code snippets inglês ok

**Critérios:**
- Documentação narrativa português
- Termos técnicos inglês aceitáveis (OAuth2, JWT, PostGIS)

### 4.3 Metadados Atualizados
```bash
grep "Última atualização: 202" PROJECTS/*/DOCS/README.md
```

**Verifica:**
- ✅ Footer "Última atualização: YYYY-MM-DD" presente
- ✅ Datas recentes (não 2020, 2021 desatualizados)

**Critérios:**
- READMEs principais tem data atualização
- Indicador manutenção ativa

## 5. Validações Manuais (Checklist Humano)

### 5.1 Flow de Leitura Arquitetura
**Tarefa:** Ler sequência documentos como novo desenvolvedor

1. Iniciar CENTRAL/README.md
2. Navegar CENTRAL/ARCHITECTURE/README.md
3. Ler 3 ADRs principais (ADR-001, ADR-003, ADR-008)
4. Navegar CENTRAL/DOMAIN-MODEL/README.md
5. Escolher 1 projeto (ex: GEOWEB)
6. Ler PROJECTS/GEOWEB/DOCS/README.md
7. Ler ARCHITECTURE/01-overview.md
8. Ler 1 FEATURE (ex: unit-management.md)

**Checklist:**
- [ ] Fluxo lógico? Informações aparecem em ordem compreensível?
- [ ] Consegue entender stack tecnológica completa?
- [ ] Consegue localizar onde está implementado UC-001?
- [ ] Terminologia consistente ao longo leitura?
- [ ] Links funcionam e levam lugares esperados?

### 5.2 Contradições Stack Tecnológica
**Tarefa:** Comparar stack docs diferentes

1. Ler CENTRAL/ARCHITECTURE/ADRs/ADR-001-dotnet-9-backend.md
2. Ler PROJECTS/GEOAPI/DOCS/ARCHITECTURE/01-overview.md
3. Comparar versões .NET mencionadas

**Checklist:**
- [ ] Versões .NET consistentes?
- [ ] Versões PostgreSQL/PostGIS consistentes?
- [ ] Bibliotecas principais mencionadas mesmas?
- [ ] Decisões ADRs refletidas em implementação docs?

### 5.3 Gaps de Informação
**Tarefa:** Identificar perguntas sem resposta

Tentar responder via documentação:
1. Como configurar ambiente dev GEOAPI?
2. Como autenticação funciona end-to-end?
3. Como field collector sincroniza offline?
4. Quais validações CPF executadas?
5. Como multi-tenancy RLS implementado?

**Checklist:**
- [ ] Todas perguntas respondíveis navegando docs?
- [ ] Informações estão locais previsíveis (setup em HOW-TO, conceitos em CONCEPTS)?
- [ ] Cross-referências ajudam encontrar info relacionada?

### 5.4 Redundância Desnecessária
**Tarefa:** Identificar duplicação sem valor

Comparar:
1. CENTRAL/API/AUTHENTICATION/ vs PROJECTS/GEOAPI/DOCS/CONCEPTS/01-authentication.md
2. CENTRAL/WORKFLOWS/02-field-data-collection-workflow.md vs PROJECTS/REURBCAD/DOCS/FEATURES/

**Checklist:**
- [ ] Duplicação justificada? (CENTRAL especifica, PROJECTS implementa)
- [ ] Ou duplicação desnecessária? (copy-paste mesmo conteúdo)
- [ ] Informação CENTRAL mais abstrata, PROJECTS mais concreta?

### 5.5 Cobertura Features vs Requirements
**Tarefa:** Validar implementação requisitos

1. Pegar UC-001 (cadastrar unidade habitacional)
2. Identificar RFs relacionados (RF-049 a RF-069)
3. Encontrar features implementando (GEOWEB unit-management, REURBCAD field-collection)
4. Verificar se features cobrem todos RFs

**Checklist:**
- [ ] UC -> RF mapeamento claro?
- [ ] RF -> Feature mapeamento explícito?
- [ ] RFs críticos todos implementados?
- [ ] Features órfãs (não implementam requirements) justificadas?

## 6. Métricas de Qualidade

### 6.1 Cobertura Documentação
```bash
# Total arquivos markdown
find CENTRAL PROJECTS/*/DOCS -name "*.md" | wc -l

# Arquivos READMEs estruturantes
find CENTRAL PROJECTS/*/DOCS -name "README.md" | wc -l

# Arquivos features documentados
find PROJECTS/*/DOCS/FEATURES -name "*.md" ! -name "README.md" | wc -l

# Use cases documentados
find CENTRAL/REQUIREMENTS/USE-CASES -name "UC-*.md" | wc -l

# Requisitos funcionais
find CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS -name "RF-*.md" | wc -l
```

**Metas:**
- [x] >= 800 arquivos markdown total
- [x] >= 30 features documentados
- [x] >= 11 use cases principais (UC-001 a UC-011)
- [x] >= 200 requisitos funcionais (RF-001 a RF-221)

### 6.2 Densidade Informacional
```bash
# Palavras por arquivo feature (deve ser >= 100)
for f in PROJECTS/*/DOCS/FEATURES/*.md; do
  wc -w "$f"
done | awk '{sum+=$1; count++} END {print "Média:", sum/count, "palavras/feature"}'
```

**Meta:**
- [x] Média >= 150 palavras por feature (mínimo 100)

### 6.3 Interconexão Grafo
```bash
# Links totais documentação
grep -r "\[.*\](\..*\.md)" CENTRAL PROJECTS/*/DOCS | wc -l

# Densidade links (links / arquivos)
# Meta: >= 3 links por arquivo (bem conectado)
```

**Meta:**
- [x] >= 3 links médios por arquivo markdown

## 7. Plano Execução Validação

### Fase 1: Automáticas (1 hora)
```bash
# 1. Dense paragraph
python .scripts/lint-dense-paragraph.py > validation-reports/01-dense-paragraph.txt

# 2. Isolated files
python .scripts/list-isolated-simple.py > validation-reports/02-isolated-files.txt

# 3. Links quebrados
python .scripts/check-links.py > validation-reports/03-broken-links.txt

# 4. Rastreabilidade
python .scripts/generate-traceability-matrix.py --validate > validation-reports/04-traceability.txt
```

### Fase 2: Consistência (2 horas)
```bash
# 1. Nomenclatura
grep -r "REURB[^-SE]" CENTRAL PROJECTS --include="*.md" > validation-reports/05-nomenclature.txt

# 2. Stack tech
grep -r "React [0-9]" PROJECTS/GEOWEB PROJECTS/REURBCAD --include="*.md" > validation-reports/06-stack-versions.txt

# 3. Estrutura projetos
bash .scripts/validate-project-structure.sh > validation-reports/07-structure.txt
```

### Fase 3: Manuais (4 horas)
```bash
# Executar checklist 5.1 a 5.5
# Documentar achados em validation-reports/08-manual-review.md
```

### Fase 4: Relatório Final (1 hora)
```bash
# Consolidar todos reports
python .scripts/generate-validation-report.py --input validation-reports/ --output VALIDATION-REPORT.md
```

## 8. Critérios Aprovação

### Must Have (Bloqueantes)
- [ ] ZERO arquivos isolados em DOCS/
- [ ] ZERO links quebrados em CENTRAL/
- [ ] ZERO code blocks em CENTRAL/ (exceto tabelas)
- [ ] Rastreabilidade UC -> RF completa
- [ ] Estrutura projetos padronizada

### Should Have (Warnings)
- [ ] Nomenclatura 100% consistente
- [ ] Todas features >= 100 palavras
- [ ] Stack tech consistente entre docs
- [ ] Metadados atualizados (datas recentes)

### Nice to Have (Melhorias Futuras)
- [ ] Diagramas arquitetura mermaid
- [ ] Exemplos código em PROJECTS/CONCEPTS/
- [ ] Vídeos tutoriais setup
- [ ] API reference completo OpenAPI

## 9. Manutenção Contínua

### Weekly
- Rodar lint-dense-paragraph.py
- Rodar list-isolated-simple.py
- Verificar links quebrados

### Monthly
- Revisar rastreabilidade requirements
- Atualizar metadados datas
- Adicionar features novas desenvolvidas

### Quarterly
- Validação manual completa (checklist 5.1-5.5)
- Atualizar stack tech se mudanças
- Review arquitetura ADRs novos

---

**Criado:** 2026-01-12
**Responsável:** Tech Lead / Arquiteto
**Revisão:** Quarterly
