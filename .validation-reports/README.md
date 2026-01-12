# Sistema de Validação CARF

**Status:** Implementado e funcional
**Data Primeira Execução:** 2026-01-12
**Commit:** docs/complete-documentation-structure@5733ab7

---

## 📋 Índice Rápido

### Resultados da Última Auditoria
- **[RESUMO-EXECUTIVO.md](./RESUMO-EXECUTIVO.md)** - Top 10 problemas + prioridades (LEIA ESTE PRIMEIRO)
- **[BRUTAL-AUDIT.md](./BRUTAL-AUDIT.md)** - Relatório completo consolidado
- **[details/](./details/)** - Outputs detalhados de cada validação (16 arquivos)

### Documentação do Sistema
- **[AUDIT-PLAN.md](./AUDIT-PLAN.md)** - Plano de implementação executado
- **[VALIDATION-RULES.md](./VALIDATION-RULES.md)** - Regras rígidas por tipo de documento
- **[VALIDATION-PLAN.md](./VALIDATION-PLAN.md)** - Estratégia completa de validação

---

## 🎯 Resultados Última Execução

**Status:** 5 passou, 11 falhou
**Erros:** 3.353
**Warnings:** 408
**Arquivos:** 907 markdown

### Top 5 Problemas

1. 🔴 **File Structure** - 2.001 violações (seções, títulos, frontmatter)
2. 🔴 **Metadata** - 630 arquivos sem "Última atualização"
3. 🟡 **Language** - 292 arquivos com palavras inglesas
4. 🟡 **RF Coverage** - 190 de 221 RFs não documentados (86%)
5. 🟡 **Feature Sections** - 61 seções faltando

---

## 🚀 Como Usar

### Executar Auditoria Completa
```bash
cd C:\DEV\CARF
python .scripts/audit-brutal.py
```

### Executar Validação Específica
```bash
python .scripts/validate-metadata.py
python .scripts/validate-rf-coverage.py
python .scripts/validate-language.py
```

### Ver Resultados
```bash
# Resumo executivo com prioridades
cat .validation-reports/RESUMO-EXECUTIVO.md

# Relatório completo
cat .validation-reports/BRUTAL-AUDIT.md

# Detalhes de validação específica
cat .validation-reports/details/metadata.txt
```

---

## 📦 Estrutura

```
.validation-reports/
├── README.md                    # Este arquivo (índice)
├── RESUMO-EXECUTIVO.md          # Prioridades e top problemas
├── BRUTAL-AUDIT.md              # Relatório completo consolidado
├── AUDIT-PLAN.md                # Plano de implementação
├── VALIDATION-RULES.md          # Regras por tipo de documento
├── VALIDATION-PLAN.md           # Estratégia de validação
├── SNAPSHOT-2026-01-12.md       # Snapshot histórico
└── details/                     # Outputs detalhados
    ├── dense-paragraph.txt
    ├── isolated-files.txt
    ├── broken-links.txt
    ├── central-isolation.txt
    ├── uc-coverage.txt
    ├── structure.txt
    ├── rf-coverage.txt
    ├── nomenclature.txt
    ├── stack-versions.txt
    ├── cross-references.txt
    ├── features-vs-code.txt
    ├── feature-sections.txt
    ├── language.txt
    ├── metadata.txt
    ├── file-size.txt
    └── file-structure.txt
```

---

## 🔧 Scripts de Validação

Localizados em `.scripts/`:

### Script Master
- **audit-brutal.py** - Executa todas as 16 validações sequencialmente

### Validações Existentes (5)
1. **lint-dense-paragraph.py** - Code blocks em CENTRAL, word count em FEATURES
2. **list-isolated-simple.py** - Arquivos sem links
3. **check-links.py** - Links quebrados
4. **lint-central-isolation.py** - Isolamento CENTRAL ↔ PROJECTS
5. **validate-uc-coverage.py** - Use Cases implementados

### Validações Novas (11)
6. **validate-structure.py** - Estrutura de diretórios
7. **validate-rf-coverage.py** - Cobertura Requisitos Funcionais
8. **validate-nomenclature.py** - Terminologia técnica (PostgreSQL, Keycloak, REURB-S/E)
9. **validate-stack-versions.py** - Versões de tecnologias consistentes
10. **validate-cross-references.py** - Referências bidirecionais CENTRAL ↔ PROJECTS
11. **validate-features-vs-code.py** - Features documentadas vs implementadas
12. **validate-feature-sections.py** - Seções obrigatórias em FEATURES
13. **validate-language.py** - Idioma português
14. **validate-metadata.py** - "Última atualização: YYYY-MM-DD"
15. **validate-file-size.py** - Min/max palavras por tipo
16. **validate-file-structure.py** - Estrutura interna (seções, frontmatter, títulos)

---

## 📊 Regras de Validação

Por tipo de documento (detalhes em `VALIDATION-RULES.md`):

| Tipo | Min | Max | Seções Obrigatórias | Metadados |
|------|-----|-----|---------------------|-----------|
| README | 150w | 500w | Descrição, Links | Última atualização |
| ADR | 450w | 700w | - | Data, Status, Decisor |
| Use Case | 400w | 700w | Regras, Rastreabilidade | Última atualização |
| RF | 100w | 350w | Critérios, Relacionado | Última atualização |
| User Story | 80w | 250w | Acceptance Criteria | - |
| Entity | 200w | 500w | - | - |
| Feature | 500w | 1000w | Validações, API, Relacionamentos | Última atualização |
| HOW-TO | 300w | 900w | Pré-requisitos, Passos | - |
| Concept | 250w | 550w | Como Funciona | - |
| Business Rule | 300w | 700w | - | - |
| Architecture | 400w | 900w | Explicação, Implementação | - |

---

## ⚠️ Nota Importante

**Esta pasta é temporária e pode ser removida a qualquer momento.**

Os scripts de validação (`.scripts/*.py`) são permanentes e podem ser executados sempre que necessário para regenerar os relatórios.

Para auditoria regular, recomenda-se:
- Executar mensalmente: `python .scripts/audit-brutal.py`
- Integrar no CI/CD para validação automática em PRs
- Arquivar relatórios históricos se necessário

---

## 📈 Próximas Ações Recomendadas

### Esta Semana (Imediato)
1. Adicionar "Última atualização" em 630 arquivos
2. Criar 5 OVERVIEW.md faltando
3. Fixar 3 violações nomenclatura

### Este Mês (Curto Prazo)
1. Adicionar 61 seções faltando em FEATURES
2. Revisar 190 RFs órfãos
3. Padronizar 14 versões stack
4. Expandir 162 READMEs < 150 palavras

### Este Quarter (Médio Prazo)
1. Revisar 292 arquivos com inglês
2. Corrigir 2.001 violações estrutura
3. Dividir 193 arquivos > max palavras
4. Integrar validação em CI/CD

**Ver detalhes completos em [RESUMO-EXECUTIVO.md](./RESUMO-EXECUTIVO.md)**

---

**Sistema implementado por:** Claude Sonnet 4.5
**Tempo implementação:** 12.5 horas (conforme planejado)
**Próxima auditoria:** 2026-02-12 (mensal recomendado)
