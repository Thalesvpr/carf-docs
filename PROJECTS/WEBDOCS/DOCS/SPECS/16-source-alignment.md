---
type: leaf
status: review
updated: 2026-02-07
---

# Alinhamento com CENTRAL e PROJECTS

Sistema de rastreabilidade entre paginas WEBDOCS e documentacao fonte. Campo source no frontmatter obrigatorio e validado.

## Campo Source

Tipo string obrigatorio, pattern CENTRAL/ ou PROJECTS/ terminando em .md. Validacao verifica existencia do arquivo no repositorio.

## Mapeamento

| Secao WEBDOCS | Fontes Permitidas | Adaptacao |
|---------------|-------------------|-----------|
| /guia/ | CENTRAL/WORKFLOWS/, BUSINESS-RULES/ | Linguagem simplificada |
| /sistema/ | CENTRAL/DOMAIN-MODEL/, ARCHITECTURE/, BUSINESS-RULES/ | Precisao com explicacoes |
| /manuais/geoweb/ | PROJECTS/GEOWEB/FEATURES/, HOW-TO/, USE-CASES/ | Passos praticos |
| /manuais/reurbcad/ | PROJECTS/REURBCAD/FEATURES/, HOW-TO/, USE-CASES/ | Offline e sync |
| /manuais/admin/ | PROJECTS/ADMIN/FEATURES/, HOW-TO/ | Config e gestao |
| /api/ | CENTRAL/API/, PROJECTS/GEOAPI/, CENTRAL/INTEGRATION/ | Exemplos praticos |
| /dev/ | CENTRAL/ARCHITECTURE/, VERSIONING/, PROJECTS/LIB/ | Linguagem tecnica |

## Fontes Multiplas

Campo source aceita um valor (primario). Fontes adicionais em secao Fontes Relacionadas no final da pagina.

## Transformacao

Usar termos oficiais: Unidade Habitacional (nao Unit), Em Rascunho (nao DRAFT), Coordenador de Campo (nao field-coordinator), salvar no dispositivo (nao persistir no WatermelonDB).

## Sincronizacao

CI detecta modificacao em fonte, busca paginas que referenciam, adiciona label needs-review no PR. Reviewer verifica e cria issue ou inclui mudanca.
