---
type: leaf
status: review
updated: 2026-02-07
---

# Decap CMS - Visao Geral

Especificacao da configuracao do Decap CMS para edicao visual de conteudo do WEBDOCS. Arquivos relacionados: 15-decap-cms-collections.md e 15-decap-cms-arquivos.md.

## Arquivos de Configuracao

O Decap CMS requer dois arquivos na pasta public/admin/. O arquivo index.html e HTML minimo que carrega Decap CMS via script. O arquivo config.yml contem configuracao de backend, collections e fields.

## Backend GitHub

| Propriedade | Valor | Descricao |
|-------------|-------|-----------|
| name | github | Provider de backend |
| repo | carf/carf-webdocs | Repositorio alvo |
| branch | main | Branch de publicacao |
| base_url | https://docs.carf.com.br | URL base para OAuth |
| auth_endpoint | /auth/cms | Endpoint de autenticacao |

Commit messages seguem padrao convencional com prefixo docs: seguido da acao (criar, atualizar, remover) e nome do collection/slug.

## Configuracao de Media

Pasta para upload e public/images com folder publico /images. Tamanho maximo de arquivo e 5MB. Extensoes permitidas sao jpg, jpeg, png, gif, svg e webp.

## Configuracoes Adicionais

| Propriedade | Valor | Descricao |
|-------------|-------|-----------|
| editor.preview | true | Habilita pre-visualizacao |
| slug.encoding | unicode | Suporte a caracteres unicode |
| slug.clean_accents | true | Remove acentos de slugs |
| slug.sanitize_replacement | - | Substitui caracteres invalidos por hifen |
| locale | pt | Idioma portugues |
| site_url | https://docs.carf.com.br | URL para previews |

## Autenticacao OAuth

O Decap CMS usa OAuth para autenticar com GitHub. O endpoint /auth/cms no WEBDOCS funciona como proxy OAuth seguindo especificacao do Decap. Usuarios precisam de acesso de escrita ao repositorio carf/carf-webdocs para usar o CMS.
