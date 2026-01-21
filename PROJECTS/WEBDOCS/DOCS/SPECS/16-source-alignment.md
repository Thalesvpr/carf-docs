---
id: ""
type: ARCH
modules: []
epic: ""
status: review
created: 2026-01-21
updated: 2026-01-21
---

# Alinhamento com CENTRAL e PROJECTS

Especificação do sistema de alinhamento que garante rastreabilidade entre páginas WEBDOCS e documentação fonte em CENTRAL e PROJECTS. O campo source no frontmatter é obrigatório e validado automaticamente.

## Campo Source Obrigatório

Toda página de conteúdo em WEBDOCS deve declarar sua fonte através do campo source no frontmatter. Este campo garante que a documentação do usuário final sempre tenha referência para a documentação técnica oficial.

```json
{
  "source": {
    "required": true,
    "type": "string",
    "pattern": "^(CENTRAL|PROJECTS)/.*\\.md$",
    "description": "Caminho relativo para arquivo fonte no repositório carf-docs",
    "examples": [
      "CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/01-auth-security/RF-001-integracao-com-keycloak.md",
      "CENTRAL/WORKFLOWS/02-field-data-collection-workflow.md",
      "PROJECTS/GEOWEB/DOCS/FEATURES/01-map-navigation.md",
      "CENTRAL/DOMAIN-MODEL/ENTITIES/02-unit.md"
    ],
    "validation": "Arquivo referenciado deve existir no repositório"
  }
}
```

## Mapeamento Seção WEBDOCS para Fonte

Cada seção do WEBDOCS tem fontes permitidas em CENTRAL e PROJECTS. O validador verifica se o source declarado é compatível com a seção da página.

```json
{
  "mapping": {
    "/guia/": {
      "allowed_sources": [
        "CENTRAL/WORKFLOWS/",
        "CENTRAL/BUSINESS-RULES/"
      ],
      "description": "Guias do usuário derivados de workflows e regras de negócio",
      "content_adaptation": "Simplificar linguagem técnica para usuário final"
    },
    "/sistema/": {
      "allowed_sources": [
        "CENTRAL/DOMAIN-MODEL/",
        "CENTRAL/ARCHITECTURE/",
        "CENTRAL/BUSINESS-RULES/"
      ],
      "description": "Explicações do sistema derivadas do modelo de domínio e arquitetura",
      "content_adaptation": "Manter precisão técnica com explicações acessíveis"
    },
    "/manuais/geoweb/": {
      "allowed_sources": [
        "PROJECTS/GEOWEB/DOCS/FEATURES/",
        "PROJECTS/GEOWEB/DOCS/HOW-TO/",
        "CENTRAL/REQUIREMENTS/USE-CASES/"
      ],
      "description": "Manuais GeoWeb derivados de features e casos de uso",
      "content_adaptation": "Foco em passos práticos com screenshots"
    },
    "/manuais/reurbcad/": {
      "allowed_sources": [
        "PROJECTS/REURBCAD/DOCS/FEATURES/",
        "PROJECTS/REURBCAD/DOCS/HOW-TO/",
        "CENTRAL/REQUIREMENTS/USE-CASES/"
      ],
      "description": "Manuais REURBCAD derivados de features e casos de uso",
      "content_adaptation": "Foco em uso offline e sincronização"
    },
    "/manuais/admin/": {
      "allowed_sources": [
        "PROJECTS/ADMIN/DOCS/FEATURES/",
        "PROJECTS/ADMIN/DOCS/HOW-TO/"
      ],
      "description": "Manuais do painel administrativo",
      "content_adaptation": "Foco em configuração e gestão"
    },
    "/api/": {
      "allowed_sources": [
        "CENTRAL/API/",
        "PROJECTS/GEOAPI/DOCS/",
        "CENTRAL/INTEGRATION/"
      ],
      "description": "Documentação de API derivada das specs técnicas",
      "content_adaptation": "Exemplos práticos de uso"
    },
    "/dev/": {
      "allowed_sources": [
        "CENTRAL/ARCHITECTURE/",
        "CENTRAL/VERSIONING/",
        "PROJECTS/*/DOCS/ARCHITECTURE/",
        "PROJECTS/LIB/"
      ],
      "description": "Documentação técnica para desenvolvedores",
      "content_adaptation": "Manter linguagem técnica, adicionar exemplos de código"
    }
  }
}
```

## Fontes Múltiplas

Uma página WEBDOCS pode consolidar múltiplas fontes. O campo source aceita apenas um valor, mas seção "Fontes Relacionadas" no final da página pode listar fontes adicionais.

```json
{
  "multiple_sources": {
    "primary": "Campo source no frontmatter (obrigatório)",
    "related": "Seção ## Fontes Relacionadas no conteúdo (opcional)",
    "format": "Lista de links para arquivos em CENTRAL/PROJECTS"
  }
}
```

## Transformação de Conteúdo

Conteúdo em WEBDOCS não é cópia direta da fonte. A documentação é adaptada para o público alvo (usuários finais vs desenvolvedores) mantendo alinhamento conceitual com a fonte.

```json
{
  "adaptation_guidelines": {
    "terminology": {
      "rule": "Usar termos definidos em CENTRAL/DOMAIN-MODEL/ENTITIES/",
      "example": "Usar 'Unidade Habitacional' não 'Unit'"
    },
    "status_values": {
      "rule": "Usar valores de CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/03-unit-status.md",
      "example": "Usar 'Em Análise' não 'UNDER_REVIEW'"
    },
    "role_names": {
      "rule": "Usar nomes de PROJECTS/KEYCLOAK/DOCS/INTEGRATION/RBAC/",
      "example": "Usar 'Agente de Campo' não 'field-agent'"
    },
    "simplification": {
      "rule": "Simplificar linguagem técnica para usuários",
      "example": "Usar 'salvar no dispositivo' não 'persistir no WatermelonDB'"
    }
  }
}
```

## Sincronização

Quando a fonte é atualizada em CENTRAL ou PROJECTS, a página correspondente em WEBDOCS deve ser revisada. O sistema de validação detecta arquivos fonte modificados e alerta sobre páginas WEBDOCS que podem precisar de atualização.

```json
{
  "sync_workflow": {
    "1": "CI detecta modificação em arquivo CENTRAL/PROJECTS",
    "2": "Busca páginas WEBDOCS que referenciam o arquivo",
    "3": "Adiciona label 'needs-review' no PR",
    "4": "Reviewer verifica se WEBDOCS precisa atualização",
    "5": "Se precisar, cria issue ou inclui mudança no PR"
  }
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
