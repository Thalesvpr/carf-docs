---
status: review
updated: 2026-01-21
---

# Regras de Validação

Regras de validação automática que garantem qualidade e alinhamento da documentação WEBDOCS.

Arquivos relacionados:
- Scripts de implementação: `17-validation-scripts.md`
- Integração CI: `17-validation-ci.md`

## Validação de Fonte (SOURCE)

```json
{
  "source_rules": [
    {
      "id": "SRC001",
      "name": "Source Required",
      "description": "Campo source é obrigatório no frontmatter de toda página de conteúdo",
      "severity": "ERROR",
      "applies_to": "src/content/docs/**/*.mdx",
      "excludes": ["index.mdx", "_*.mdx"]
    },
    {
      "id": "SRC002",
      "name": "Source Exists",
      "description": "Arquivo referenciado no campo source deve existir no repositório",
      "severity": "ERROR",
      "check": "Verificar se path existe em carf-docs"
    },
    {
      "id": "SRC003",
      "name": "Source Section Match",
      "description": "Source deve ser compatível com a seção da página conforme mapeamento",
      "severity": "WARNING",
      "reference": "SPECS/16-source-alignment.md"
    },
    {
      "id": "SRC004",
      "name": "Source Format",
      "description": "Source deve seguir pattern ^(CENTRAL|PROJECTS)/.*\\.md$",
      "severity": "ERROR",
      "pattern": "^(CENTRAL|PROJECTS)/.*\\.md$"
    }
  ]
}
```

## Validação de Cobertura (COVERAGE)

```json
{
  "coverage_rules": [
    {
      "id": "COV001",
      "name": "RF Coverage",
      "description": "Todo Requisito Funcional deve ter pelo menos uma página WEBDOCS referenciando-o",
      "source_pattern": "CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/**/RF-*.md",
      "severity": "WARNING",
      "exception": "RFs marcados como internal=true são isentos"
    },
    {
      "id": "COV002",
      "name": "UC Coverage",
      "description": "Todo Caso de Uso deve ter manual correspondente em WEBDOCS",
      "source_pattern": "CENTRAL/REQUIREMENTS/USE-CASES/**/UC-*.md",
      "severity": "WARNING",
      "exception": "UCs técnicos sem interface de usuário são isentos"
    },
    {
      "id": "COV003",
      "name": "Workflow Coverage",
      "description": "Todo workflow operacional deve ter guia em /guia/",
      "source_pattern": "CENTRAL/WORKFLOWS/*.md",
      "severity": "INFO"
    },
    {
      "id": "COV004",
      "name": "Feature Coverage",
      "description": "Toda feature de PROJECTS deve ter manual correspondente",
      "source_pattern": "PROJECTS/*/DOCS/FEATURES/*.md",
      "severity": "WARNING"
    }
  ]
}
```

## Validação de Termos (TERMS)

```json
{
  "term_rules": [
    {
      "id": "TERM001",
      "name": "Entity Names",
      "description": "Nomes de entidades devem usar grafia oficial",
      "terms_source": "CENTRAL/DOMAIN-MODEL/ENTITIES/README.md",
      "severity": "WARNING",
      "examples": {
        "correct": ["Unidade Habitacional", "Titular", "Comunidade"],
        "incorrect": ["Unit", "Holder", "Community", "unidade"]
      }
    },
    {
      "id": "TERM002",
      "name": "Status Values",
      "description": "Valores de status devem usar labels oficiais",
      "terms_source": "CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/03-unit-status.md",
      "severity": "WARNING",
      "examples": {
        "correct": ["Em Rascunho", "Aguardando Aprovação", "Aprovada"],
        "incorrect": ["DRAFT", "PENDING", "APPROVED", "draft"]
      }
    },
    {
      "id": "TERM003",
      "name": "Role Names",
      "description": "Nomes de roles devem usar labels oficiais",
      "severity": "ERROR",
      "examples": {
        "correct": ["Agente de Campo", "Analista", "Administrador"],
        "incorrect": ["field-agent", "analyst", "admin"]
      }
    },
    {
      "id": "TERM004",
      "name": "Product Names",
      "description": "Nomes de produtos devem usar grafia oficial",
      "severity": "WARNING",
      "terms": {
        "GeoWeb": ["geoweb", "Geoweb", "GEOWEB"],
        "REURBCAD": ["Reurbcad", "ReurbCAD", "reurbcad"],
        "GeoAPI": ["geoapi", "Geoapi", "GEOAPI"]
      }
    }
  ]
}
```

## Validação de Conteúdo (CONTENT)

```json
{
  "content_rules": [
    {
      "id": "CONT001",
      "name": "Description Length",
      "description": "Campo description deve ter entre 50 e 160 caracteres",
      "severity": "ERROR",
      "min": 50,
      "max": 160
    },
    {
      "id": "CONT002",
      "name": "Title Present",
      "description": "Campo title é obrigatório e não pode ser vazio",
      "severity": "ERROR"
    },
    {
      "id": "CONT003",
      "name": "No Broken Links",
      "description": "Links internos devem apontar para páginas existentes",
      "severity": "ERROR"
    },
    {
      "id": "CONT004",
      "name": "No Dead Images",
      "description": "Imagens referenciadas devem existir em public/images/",
      "severity": "ERROR"
    },
    {
      "id": "CONT005",
      "name": "Alt Text Required",
      "description": "Todas imagens devem ter atributo alt para acessibilidade",
      "severity": "WARNING"
    }
  ]
}
```

## Execução dos Validadores

```json
{
  "commands": {
    "all": "bun run validate",
    "sources": "bun run validate:sources",
    "coverage": "bun run validate:coverage",
    "terms": "bun run validate:terms",
    "content": "bun run validate:content"
  },
  "ci_integration": {
    "trigger": "Pull requests e push para main",
    "block_merge": "Erros com severity ERROR bloqueiam merge",
    "warnings": "Warnings são reportados mas não bloqueiam"
  },
  "output": {
    "format": "JSON com lista de violações",
    "fields": ["rule_id", "severity", "file", "line", "message", "suggestion"]
  }
}
```

## Ignorando Regras

Em casos excepcionais, regras podem ser ignoradas:

```json
{
  "ignore_syntax": {
    "frontmatter": "validate-ignore: [RULE_ID, RULE_ID]",
    "example": "validate-ignore: [COV001, TERM002]",
    "requirement": "Comentário explicando motivo da exceção"
  }
}
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
