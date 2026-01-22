---
type: leaf
status: review
updated: 2026-01-21
---

# Decap CMS - Collections

Definição de todas as collections do Decap CMS para o WEBDOCS.

Arquivos relacionados:
- Visão geral: `15-decap-cms-overview.md`
- Arquivos completos: `15-decap-cms-arquivos.md`

## Collection: Guia do Usuário

```yaml
- name: guia
  label: "Guia do Usuário"
  label_singular: "Página do Guia"
  folder: src/content/docs/guia
  create: true
  delete: true
  extension: mdx
  format: frontmatter
  slug: "{{slug}}"
  preview_path: guia/{{slug}}
  sortable_fields: ['title', 'sidebar.order']
  view_filters:
    - label: "Rascunhos"
      field: draft
      pattern: true
  fields:
    - name: title
      label: "Título"
      widget: string
      required: true
      pattern:
        - ".{3,100}"
        - "Título deve ter entre 3 e 100 caracteres"
    - name: description
      label: "Descrição"
      widget: string
      required: true
      hint: "50-160 caracteres para SEO"
      pattern:
        - ".{50,160}"
        - "Descrição deve ter entre 50 e 160 caracteres"
    - name: source
      label: "Arquivo Fonte"
      widget: string
      required: true
      hint: "Caminho em CENTRAL ou PROJECTS"
      pattern:
        - "^(CENTRAL|PROJECTS)/[\\w\\-/]+\\.md$"
        - "Deve seguir padrão: CENTRAL/path/file.md"
    - name: sidebar
      label: "Sidebar"
      widget: object
      collapsed: true
      fields:
        - name: order
          label: "Ordem"
          widget: number
          required: false
        - name: label
          label: "Label Alternativo"
          widget: string
          required: false
        - name: badge
          label: "Badge"
          widget: string
          required: false
    - name: draft
      label: "Rascunho"
      widget: boolean
      default: false
    - name: body
      label: "Conteúdo"
      widget: markdown
```

## Collection: Manuais GeoWeb

```yaml
- name: manuais-geoweb
  label: "Manuais GeoWeb"
  label_singular: "Manual GeoWeb"
  description: "Manuais operacionais do GeoWeb"
  folder: src/content/docs/manuais/geoweb
  create: true
  delete: true
  extension: mdx
  format: frontmatter
  slug: "{{slug}}"
  preview_path: manuais/geoweb/{{slug}}
  fields:
    - { name: title, label: Título, widget: string, required: true }
    - name: description
      label: "Descrição"
      widget: string
      required: true
      pattern: [".{50,160}", "50-160 caracteres"]
    - name: source
      label: "Arquivo Fonte"
      widget: string
      required: true
      pattern: ["^(CENTRAL|PROJECTS)/[\\w\\-/]+\\.md$", "Formato inválido"]
    - name: sidebar
      label: "Sidebar"
      widget: object
      collapsed: true
      fields:
        - { name: order, label: Ordem, widget: number, required: false }
        - { name: label, label: Label, widget: string, required: false }
        - { name: badge, label: Badge, widget: string, required: false }
    - { name: draft, label: Rascunho, widget: boolean, default: false }
    - { name: body, label: Conteúdo, widget: markdown }
```

## Collection: Manuais REURBCAD

```yaml
- name: manuais-reurbcad
  label: "Manuais REURBCAD"
  label_singular: "Manual REURBCAD"
  description: "Manuais operacionais do REURBCAD Mobile"
  folder: src/content/docs/manuais/reurbcad
  create: true
  delete: true
  extension: mdx
  format: frontmatter
  slug: "{{slug}}"
  preview_path: manuais/reurbcad/{{slug}}
  fields:
    - { name: title, label: Título, widget: string, required: true }
    - name: description
      label: "Descrição"
      widget: string
      required: true
      pattern: [".{50,160}", "50-160 caracteres"]
    - name: source
      label: "Arquivo Fonte"
      widget: string
      required: true
      pattern: ["^(CENTRAL|PROJECTS)/[\\w\\-/]+\\.md$", "Formato inválido"]
    - name: sidebar
      label: "Sidebar"
      widget: object
      collapsed: true
      fields:
        - { name: order, label: Ordem, widget: number, required: false }
        - { name: label, label: Label, widget: string, required: false }
        - { name: badge, label: Badge, widget: string, required: false }
    - { name: draft, label: Rascunho, widget: boolean, default: false }
    - { name: body, label: Conteúdo, widget: markdown }
```

## Collection: Manuais Admin

```yaml
- name: manuais-admin
  label: "Manuais Admin"
  label_singular: "Manual Admin"
  description: "Manuais para administradores"
  folder: src/content/docs/manuais/admin
  create: true
  delete: true
  extension: mdx
  format: frontmatter
  slug: "{{slug}}"
  preview_path: manuais/admin/{{slug}}
  fields:
    - { name: title, label: Título, widget: string, required: true }
    - name: description
      label: "Descrição"
      widget: string
      required: true
      pattern: [".{50,160}", "50-160 caracteres"]
    - name: source
      label: "Arquivo Fonte"
      widget: string
      required: true
      pattern: ["^(CENTRAL|PROJECTS)/[\\w\\-/]+\\.md$", "Formato inválido"]
    - name: sidebar
      label: "Sidebar"
      widget: object
      collapsed: true
      fields:
        - { name: order, label: Ordem, widget: number, required: false }
        - { name: label, label: Label, widget: string, required: false }
        - { name: badge, label: Badge, widget: string, required: false }
    - { name: draft, label: Rascunho, widget: boolean, default: false }
    - { name: body, label: Conteúdo, widget: markdown }
```

## Collection: Incidentes (Status Page)

```yaml
- name: incidents
  label: "Incidentes"
  label_singular: "Incidente"
  description: "Registro de incidentes para a página de status"
  folder: src/content/incidents
  create: true
  delete: true
  extension: md
  format: frontmatter
  slug: "{{year}}-{{month}}-{{day}}-{{slug}}"
  fields:
    - name: title
      label: "Título"
      widget: string
      required: true
      hint: "Descrição curta do incidente"
    - name: date
      label: "Data/Hora"
      widget: datetime
      required: true
      format: "YYYY-MM-DDTHH:mm:ssZ"
    - name: status
      label: "Status"
      widget: select
      required: true
      options:
        - { label: "Investigando", value: "investigating" }
        - { label: "Identificado", value: "identified" }
        - { label: "Monitorando", value: "monitoring" }
        - { label: "Resolvido", value: "resolved" }
    - name: services
      label: "Serviços Afetados"
      widget: select
      multiple: true
      required: true
      options:
        - { label: "GeoAPI", value: "geoapi" }
        - { label: "Autenticação (Keycloak)", value: "keycloak" }
        - { label: "Armazenamento (MinIO)", value: "minio" }
        - { label: "Banco de Dados (PostgreSQL)", value: "postgres" }
    - name: severity
      label: "Severidade"
      widget: select
      required: true
      options:
        - { label: "Menor - Impacto limitado", value: "minor" }
        - { label: "Maior - Funcionalidade afetada", value: "major" }
        - { label: "Crítico - Sistema indisponível", value: "critical" }
    - name: body
      label: "Descrição e Atualizações"
      widget: markdown
```

## Collection: Banners

```yaml
- name: banners
  label: "Banners"
  label_singular: "Banner"
  description: "Notificações exibidas no topo das páginas"
  folder: src/content/banners
  create: true
  delete: true
  extension: yaml
  format: yaml
  identifier_field: id
  fields:
    - name: id
      label: "ID"
      widget: string
      required: true
      hint: "Identificador único (lowercase, hífens)"
      pattern:
        - "^[a-z0-9-]+$"
        - "Apenas letras minúsculas, números e hífens"
    - name: content
      label: "Conteúdo"
      widget: string
      required: true
      hint: "Mensagem do banner (máx. 200 caracteres)"
      pattern:
        - ".{10,200}"
        - "Entre 10 e 200 caracteres"
    - name: variant
      label: "Tipo"
      widget: select
      required: true
      default: "note"
      options:
        - { label: "Informação", value: "note" }
        - { label: "Dica", value: "tip" }
        - { label: "Atenção", value: "caution" }
        - { label: "Perigo", value: "danger" }
        - { label: "Sucesso", value: "success" }
    - name: dismissible
      label: "Pode ser fechado"
      widget: boolean
      default: true
    - name: startDate
      label: "Data Início"
      widget: datetime
      required: false
    - name: endDate
      label: "Data Fim"
      widget: datetime
      required: false
    - name: priority
      label: "Prioridade"
      widget: number
      required: false
      default: 50
      min: 0
      max: 100
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
