---
status: rejected
description: "Incompleto. Standards devem ter regras claras e validaveis, nao apenas diretrizes vagas. Contem blocos de codigo."
updated: 2026-01-21
---

# STD-004: Tipos de Documento

Todo documento no repositorio CARF possui um tipo que define sua estrutura e regras de validacao. O tipo pode ser declarado explicitamente no frontmatter ou inferido pelo nome do arquivo.

## Frontmatter de Tipo

O campo `type` no frontmatter define o tipo do documento. Se omitido, o tipo e inferido pelo nome do arquivo.

```yaml
---
type: adr
status: rejected
description: "Incompleto. Standards devem ter regras claras e validaveis, nao apenas diretrizes vagas. Contem blocos de codigo."
updated: 2026-01-21
---
```

## Tipos Disponiveis

| Tipo | Descricao | Padrao de Nome |
|------|-----------|----------------|
| `template` | Arquivo template com regras de validacao | `*-000-template.md` |
| `adr` | Architecture Decision Record | `ADR-XXX-*.md` |
| `rf` | Requisito Funcional | `RF-XXX-*.md` |
| `rnf` | Requisito Nao Funcional | `RNF-XXX-*.md` |
| `uc` | Caso de Uso | `UC-XXX-*.md` ou `XX-UC-XXX-*.md` |
| `us` | User Story | `US-XXX-*.md` |
| `readme` | Arquivo indice de pasta | `README.md` |
| `doc` | Documento generico | Qualquer outro `.md` |

## Templates

Templates definem regras de validacao para documentos do mesmo tipo na pasta. Um template e identificado por `type: template` no frontmatter e deve declarar `template_for` indicando qual tipo ele valida.

```yaml
---
type: template
template_for: adr
status: rejected
description: "Incompleto. Standards devem ter regras claras e validaveis, nao apenas diretrizes vagas. Contem blocos de codigo."
updated: 2026-01-21
validation:
  max_words: 300
  max_words_per_section: 80
  required_sections:
    - Contexto
    - Decisao
    - Consequencias
    - Alternativas Rejeitadas
  forbidden:
    - "```"
    - "http"
    - "|--|"
  title_pattern: "^ADR-\\d{3}:"
  filename_pattern: "^ADR-\\d{3}-.+\\.md$"
---
```

## Regras de Validacao

Templates podem definir as seguintes regras no campo `validation`:

| Regra | Tipo | Descricao |
|-------|------|-----------|
| `max_words` | number | Maximo de palavras no documento |
| `max_words_per_section` | number | Maximo de palavras por secao |
| `required_sections` | string[] | Lista de secoes H2 obrigatorias |
| `forbidden` | string[] | Padroes proibidos no conteudo |
| `title_pattern` | string | Regex para validar titulo H1 |
| `filename_pattern` | string | Regex para validar nome do arquivo |

## Inferencia de Tipo

Se o campo `type` nao estiver presente no frontmatter, o tipo e inferido pelo nome do arquivo seguindo estas regras em ordem:

1. Nome contem `-000-template` → `template`
2. Nome comeca com `ADR-` → `adr`
3. Nome comeca com `RF-` → `rf`
4. Nome comeca com `RNF-` → `rnf`
5. Nome comeca com `UC-` ou `XX-UC-` → `uc`
6. Nome comeca com `US-` → `us`
7. Nome e `README.md` → `readme`
8. Qualquer outro → `doc`

## Heranca de Templates

O validador busca templates na pasta do documento e em pastas ancestrais. Isso permite definir um template em uma pasta pai que se aplica a todos os documentos do tipo nas subpastas.

## Validacao Automatica

O plugin Obsidian Docs Toolkit valida automaticamente documentos conforme suas regras de template. Erros e avisos aparecem no painel de issues. Documentos sem template correspondente nao sao validados por regras de template, apenas por regras globais como frontmatter e links.
