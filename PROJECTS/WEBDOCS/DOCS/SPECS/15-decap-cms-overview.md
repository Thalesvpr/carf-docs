---
type: leaf
status: review
updated: 2026-01-21
---

# Decap CMS - Visão Geral

Especificação da configuração do Decap CMS para edição visual de conteúdo do WEBDOCS.

Arquivos relacionados:
- Collections detalhadas: `15-decap-cms-collections.md`
- Arquivos completos: `15-decap-cms-arquivos.md`

## Arquivos de Configuração

O Decap CMS requer dois arquivos em public/admin/:

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

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
