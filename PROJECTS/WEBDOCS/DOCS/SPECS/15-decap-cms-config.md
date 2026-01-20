# Configuração Decap CMS

Especificação completa da configuração do Decap CMS para edição visual de conteúdo do WEBDOCS, permitindo que equipe de documentação edite páginas sem conhecimento técnico.

## Arquivos de Configuração

O Decap CMS requer dois arquivos em public/admin/: index.html como entry point e config.yml com configuração completa.

```json
{
  "files": {
    "public/admin/index.html": "HTML mínimo que carrega Decap CMS",
    "public/admin/config.yml": "Configuração de backend, collections e fields"
  }
}
```

## Backend GitHub

Configuração do backend para integração com GitHub usando OAuth.

```yaml
backend:
  name: github
  repo: carf/carf-webdocs
  branch: main
  base_url: https://docs.carf.com.br
  auth_endpoint: /auth/cms
  commit_messages:
    create: 'docs: criar {{collection}} "{{slug}}"'
    update: 'docs: atualizar {{collection}} "{{slug}}"'
    delete: 'docs: remover {{collection}} "{{slug}}"'
    uploadMedia: 'docs: upload {{path}}'
    deleteMedia: 'docs: remover media {{path}}'
```

## Configuração de Media

Pasta para upload de imagens e arquivos.

```yaml
media_folder: public/images
public_folder: /images
media_library:
  max_file_size: 5242880  # 5MB
  allowed_extensions:
    - jpg
    - jpeg
    - png
    - gif
    - svg
    - webp
```

## Collection: Guia do Usuário

```yaml
collections:
  - name: guia
    label: Guia do Usuário
    label_singular: Página do Guia
    folder: src/content/docs/guia
    create: true
    extension: mdx
    format: frontmatter
    slug: "{{slug}}"
    preview_path: guia/{{slug}}
    fields:
      - name: title
        label: Título
        widget: string
        required: true
      - name: description
        label: Descrição
        widget: string
        required: true
        hint: "50-160 caracteres para SEO"
        pattern:
          - ".{50,160}"
          - "Descrição deve ter entre 50 e 160 caracteres"
      - name: source
        label: Arquivo Fonte
        widget: string
        required: true
        hint: "Caminho em CENTRAL ou PROJECTS"
        pattern:
          - "^(CENTRAL|PROJECTS)/.*\\.md$"
          - "Deve começar com CENTRAL/ ou PROJECTS/"
      - name: sidebar
        label: Sidebar
        widget: object
        collapsed: true
        fields:
          - name: order
            label: Ordem
            widget: number
            required: false
          - name: label
            label: Label Alternativo
            widget: string
            required: false
          - name: badge
            label: Badge
            widget: string
            required: false
            hint: "Ex: Novo, Beta"
      - name: draft
        label: Rascunho
        widget: boolean
        default: false
      - name: body
        label: Conteúdo
        widget: markdown
```

## Collection: Manuais GeoWeb

```yaml
  - name: manuais-geoweb
    label: Manuais GeoWeb
    label_singular: Manual GeoWeb
    folder: src/content/docs/manuais/geoweb
    create: true
    extension: mdx
    format: frontmatter
    slug: "{{slug}}"
    preview_path: manuais/geoweb/{{slug}}
    fields:
      - name: title
        label: Título
        widget: string
        required: true
      - name: description
        label: Descrição
        widget: string
        required: true
      - name: source
        label: Arquivo Fonte
        widget: string
        required: true
      - name: sidebar
        label: Sidebar
        widget: object
        collapsed: true
        fields:
          - name: order
            label: Ordem
            widget: number
          - name: label
            label: Label
            widget: string
          - name: badge
            label: Badge
            widget: string
      - name: draft
        label: Rascunho
        widget: boolean
        default: false
      - name: body
        label: Conteúdo
        widget: markdown
```

## Collection: Manuais REURBCAD

```yaml
  - name: manuais-reurbcad
    label: Manuais REURBCAD
    label_singular: Manual REURBCAD
    folder: src/content/docs/manuais/reurbcad
    create: true
    extension: mdx
    format: frontmatter
    slug: "{{slug}}"
    preview_path: manuais/reurbcad/{{slug}}
    fields:
      # Mesma estrutura de manuais-geoweb
```

## Collection: Manuais Admin

```yaml
  - name: manuais-admin
    label: Manuais Admin
    label_singular: Manual Admin
    folder: src/content/docs/manuais/admin
    create: true
    extension: mdx
    format: frontmatter
    slug: "{{slug}}"
    preview_path: manuais/admin/{{slug}}
    fields:
      # Mesma estrutura de manuais-geoweb
```

## Collection: Sistema CARF

```yaml
  - name: sistema
    label: O Sistema CARF
    label_singular: Página do Sistema
    folder: src/content/docs/sistema
    create: true
    extension: mdx
    format: frontmatter
    slug: "{{slug}}"
    preview_path: sistema/{{slug}}
    fields:
      # Mesma estrutura base com source obrigatório
```

## Collection: Incidentes (Status Page)

```yaml
  - name: incidents
    label: Incidentes
    label_singular: Incidente
    folder: src/content/incidents
    create: true
    extension: md
    format: frontmatter
    slug: "{{year}}-{{month}}-{{day}}-{{slug}}"
    fields:
      - name: title
        label: Título
        widget: string
      - name: date
        label: Data
        widget: datetime
      - name: status
        label: Status
        widget: select
        options:
          - { label: "Investigando", value: "investigating" }
          - { label: "Identificado", value: "identified" }
          - { label: "Monitorando", value: "monitoring" }
          - { label: "Resolvido", value: "resolved" }
      - name: services
        label: Serviços Afetados
        widget: select
        multiple: true
        options:
          - { label: "GeoAPI", value: "geoapi" }
          - { label: "Autenticação", value: "keycloak" }
          - { label: "Armazenamento", value: "minio" }
          - { label: "Banco de Dados", value: "postgres" }
      - name: body
        label: Descrição
        widget: markdown
```

## Configurações Adicionais

```yaml
# Editor
editor:
  preview: true

# Slug sanitization
slug:
  encoding: unicode
  clean_accents: true
  sanitize_replacement: "-"

# Locale
locale: pt

# Site URL para previews
site_url: https://docs.carf.com.br
display_url: https://docs.carf.com.br
```

## Autenticação OAuth

O Decap CMS usa OAuth para autenticar com GitHub. O endpoint /auth/cms no WEBDOCS funciona como proxy OAuth seguindo especificação do Decap. Usuários precisam de acesso de escrita ao repositório carf/carf-webdocs para usar o CMS.

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
