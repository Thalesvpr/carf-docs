# Plano: Auditoria Brutal Completa da Documentação CARF

## Resumo Executivo

Sistema validação automática completa **907 arquivos markdown** com **16 scripts** detectando TODOS problemas:
- 5 scripts existentes (dense paragraph, isolated files, links quebrados, UC coverage, central isolation)
- 11 scripts novos (estrutura, RF coverage, nomenclatura, stack versions, cross-refs, features vs código, seções padronizadas, idioma, metadados, tamanho, estrutura interna)

**Estimativa:** 12.5 horas implementação

## Problemas Conhecidos

- TESTING/TEST-CASES/: Apenas stubs, sem docs reais
- OPERATIONS/: READMEs < 100 palavras
- 15 arquivos com TODO/FIXME
- 1 monolito: index-by-module.md (7.503 palavras)
- 3 diretórios sem README

## Fases Implementação

### Fase 1: Regras Rígidas (2h)
Criar VALIDATION-RULES.md definindo min/max palavras, seções obrigatórias, metadados, padrões nomenclatura para cada tipo:
- READMEs: 150-500 palavras
- ADRs: 450-700 palavras
- Use Cases: 400-700 palavras
- FEATURES: 500-1000 palavras
- Entities: 200-500 palavras
- (+ 6 tipos adicionais)

### Fase 2: Scripts Validação (8h)
Implementar 11 scripts Python:
1. validate-structure.py - Estrutura diretórios padronizada
2. validate-rf-coverage.py - RF coverage
3. validate-nomenclature.py - REURB-S/E, PostgreSQL, Keycloak
4. validate-stack-versions.py - .NET 9, React 18 consistency
5. validate-cross-references.py - CENTRAL ↔ PROJECTS refs
6. validate-features-vs-code.py - Docs vs implementação
7. validate-feature-sections.py - Seções obrigatórias
8. validate-language.py - Português (exceto termos técnicos)
9. validate-metadata.py - "Última atualização"
10. validate-file-size.py - Min/max palavras
11. validate-file-structure.py - Seções obrigatórias

### Fase 3: Script Master (1h)
audit-brutal.py executa todos 16 scripts sequencialmente gerando relatório consolidado

### Fase 4: Execução (30min)
Rodar auditoria completa gerando BRUTAL-AUDIT.md

### Fase 5: Relatório (1h)
Template relatório com:
- Resumo executivo (erros/warnings)
- Problemas por severidade (Crítico/Importante/Menor)
- Diretórios incompletos detalhados
- Arquivos muito pequenos/grandes
- Seções/metadados faltando
- Rastreabilidade UC/RF/US
- Recomendações priorizadas
- Estatísticas qualidade

## Arquivos Criados

1. VALIDATION-RULES.md - Regras qualidade
2-12. .scripts/validate-*.py - 11 scripts validação
13. .scripts/audit-brutal.py - Script master
14. validation-reports/BRUTAL-AUDIT.md - Relatório final

## Verificação

```bash
cd C:\DEV\CARF
python .scripts/audit-brutal.py
```

Saída esperada:
- ✓ PASSED (validações ok)
- ✗ FAILED (com count erros)
- Relatório consolidado validation-reports/BRUTAL-AUDIT.md

## Plano Detalhado

Ver arquivo completo em `.claude/plans/cuddly-squishing-wilkinson.md` (fora repo) contendo:
- Regras YAML detalhadas por tipo
- Pseudocódigo completo cada script
- Template relatório final
- Riscos e mitigações
- Notas implementação técnicas

---

**Criado:** 2026-01-12
**Status:** Aprovado
**Próximos Passos:** Fase 1 - Criar VALIDATION-RULES.md
