---
type: leaf
status: review
updated: 2026-02-07
---

# Decap CMS - Arquivos

Descricao dos arquivos de configuracao prontos para o Decap CMS. Arquivos relacionados: 15-decap-cms-overview.md e 15-decap-cms-collections.md.

## config.yml

Arquivo principal em public/admin/config.yml. A secao backend configura integracao com GitHub no repositorio carf/carf-webdocs na branch main, com base_url apontando para https://docs.carf.com.br e auth_endpoint /api/auth/cms. Commit messages seguem padrao convencional com prefixo docs e placeholder de collection e slug.

Secao media configura media_folder como public/images, public_folder como /images, com limite de 5MB e suporte a subpastas. Secao site configura URL, display URL, logo e locale pt. Secao editor habilita preview. Secao slug configura encoding unicode, clean_accents true e sanitize_replacement com hifen.

Secao collections define seis collections: guia para Guia do Usuario em src/content/docs/guia com extensao mdx, manuais-reurbweb em src/content/docs/manuais/reurbweb, manuais-reurbcad em src/content/docs/manuais/reurbcad, manuais-admin em src/content/docs/manuais/admin, incidents para Incidentes em src/content/incidents com extensao md e slug com data, e banners em src/content/banners com extensao e formato yaml. Detalhes dos campos em 15-decap-cms-collections.md.

## index.html do Admin

Arquivo minimo em public/admin/index.html com charset utf-8, viewport responsivo, meta robots noindex, titulo CARF Docs CMS, favicon SVG e script carregando Decap CMS versao 3 do unpkg CDN.

## Preview Templates

O arquivo public/admin/preview-styles.js registra CSS customizado para preview com CMS.registerPreviewStyle apontando para /styles/custom.css. Registra preview template para collection guia que exibe titulo, descricao, badge de rascunho quando draft e true, e corpo do conteudo em estrutura de artigo com classe content.
