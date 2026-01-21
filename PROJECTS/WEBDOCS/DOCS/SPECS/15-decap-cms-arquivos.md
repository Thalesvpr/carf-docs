---
status: review
updated: 2026-01-21
---

# Decap CMS - Arquivos Completos

Arquivos de configuração completos prontos para copiar.

Arquivos relacionados:
- Visão geral: `15-decap-cms-overview.md`
- Collections: `15-decap-cms-collections.md`

## config.yml Completo

```yaml
# public/admin/config.yml
# Decap CMS Configuration for CARF WEBDOCS

# ===========================================
# BACKEND CONFIGURATION
# ===========================================
backend:
  name: github
  repo: carf/carf-webdocs
  branch: main
  base_url: https://docs.carf.com.br
  auth_endpoint: /api/auth/cms
  commit_messages:
    create: 'docs: criar {{collection}} "{{slug}}"'
    update: 'docs: atualizar {{collection}} "{{slug}}"'
    delete: 'docs: remover {{collection}} "{{slug}}"'
    uploadMedia: 'docs: upload {{path}}'
    deleteMedia: 'docs: remover media {{path}}'

# ===========================================
# MEDIA CONFIGURATION
# ===========================================
media_folder: public/images
public_folder: /images
media_library:
  max_file_size: 5242880
  folder_support: true

# ===========================================
# SITE CONFIGURATION
# ===========================================
site_url: https://docs.carf.com.br
display_url: https://docs.carf.com.br
logo_url: /logo.svg
locale: pt

# ===========================================
# EDITOR CONFIGURATION
# ===========================================
editor:
  preview: true

slug:
  encoding: unicode
  clean_accents: true
  sanitize_replacement: "-"

# ===========================================
# COLLECTIONS
# ===========================================
collections:
  # GUIA DO USUÁRIO
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
    fields:
      - { name: title, label: Título, widget: string, required: true }
      - { name: description, label: Descrição, widget: string, required: true }
      - { name: source, label: Arquivo Fonte, widget: string, required: true }
      - name: sidebar
        label: Sidebar
        widget: object
        collapsed: true
        fields:
          - { name: order, label: Ordem, widget: number, required: false }
          - { name: label, label: Label, widget: string, required: false }
          - { name: badge, label: Badge, widget: string, required: false }
      - { name: draft, label: Rascunho, widget: boolean, default: false }
      - { name: body, label: Conteúdo, widget: markdown }

  # MANUAIS GEOWEB
  - name: manuais-geoweb
    label: "Manuais GeoWeb"
    folder: src/content/docs/manuais/geoweb
    create: true
    extension: mdx
    fields:
      - { name: title, label: Título, widget: string, required: true }
      - { name: description, label: Descrição, widget: string, required: true }
      - { name: source, label: Arquivo Fonte, widget: string, required: true }
      - { name: draft, label: Rascunho, widget: boolean, default: false }
      - { name: body, label: Conteúdo, widget: markdown }

  # MANUAIS REURBCAD
  - name: manuais-reurbcad
    label: "Manuais REURBCAD"
    folder: src/content/docs/manuais/reurbcad
    create: true
    extension: mdx
    fields:
      - { name: title, label: Título, widget: string, required: true }
      - { name: description, label: Descrição, widget: string, required: true }
      - { name: source, label: Arquivo Fonte, widget: string, required: true }
      - { name: draft, label: Rascunho, widget: boolean, default: false }
      - { name: body, label: Conteúdo, widget: markdown }

  # MANUAIS ADMIN
  - name: manuais-admin
    label: "Manuais Admin"
    folder: src/content/docs/manuais/admin
    create: true
    extension: mdx
    fields:
      - { name: title, label: Título, widget: string, required: true }
      - { name: description, label: Descrição, widget: string, required: true }
      - { name: source, label: Arquivo Fonte, widget: string, required: true }
      - { name: draft, label: Rascunho, widget: boolean, default: false }
      - { name: body, label: Conteúdo, widget: markdown }

  # INCIDENTES
  - name: incidents
    label: "Incidentes"
    folder: src/content/incidents
    create: true
    extension: md
    slug: "{{year}}-{{month}}-{{day}}-{{slug}}"
    fields:
      - { name: title, label: Título, widget: string }
      - { name: date, label: Data, widget: datetime }
      - name: status
        label: Status
        widget: select
        options: [investigating, identified, monitoring, resolved]
      - name: services
        label: Serviços
        widget: select
        multiple: true
        options: [geoapi, keycloak, minio, postgres]
      - { name: body, label: Descrição, widget: markdown }

  # BANNERS
  - name: banners
    label: "Banners"
    folder: src/content/banners
    create: true
    extension: yaml
    format: yaml
    fields:
      - { name: id, label: ID, widget: string }
      - { name: content, label: Conteúdo, widget: string }
      - name: variant
        label: Tipo
        widget: select
        options: [note, tip, caution, danger, success]
      - { name: dismissible, label: Pode fechar, widget: boolean, default: true }
      - { name: startDate, label: Início, widget: datetime, required: false }
      - { name: endDate, label: Fim, widget: datetime, required: false }
```

## index.html do Admin

```html
<!-- public/admin/index.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex" />
  <title>CARF Docs - CMS</title>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
</head>
<body>
  <script src="https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js"></script>
</body>
</html>
```

## Preview Templates

```javascript
// public/admin/preview-styles.js
// Registrar CSS para preview
CMS.registerPreviewStyle('/styles/custom.css');

// Preview template para páginas de guia
CMS.registerPreviewTemplate('guia', ({ entry, widgetFor }) => {
  const title = entry.getIn(['data', 'title']);
  const description = entry.getIn(['data', 'description']);
  const draft = entry.getIn(['data', 'draft']);

  return h('article', { className: 'content' },
    draft && h('div', { className: 'draft-badge' }, 'RASCUNHO'),
    h('h1', {}, title),
    h('p', { className: 'description' }, description),
    h('hr'),
    widgetFor('body')
  );
});
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
