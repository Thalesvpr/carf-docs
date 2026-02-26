---
type: readme
status: approved
updated: 2026-01-24
---

# SYSTEM

Documentacao dos sistemas que compoem o ecossistema CARF descrevendo proposito, usuarios-alvo, capacidades principais e dependencias de cada um. Fornece visao conceitual de alto nivel sem entrar em detalhes de implementacao.

O ecossistema CARF e composto por sete sistemas integrados que atendem diferentes perfis de usuario e contextos de uso. O [GEOAPI](./01-geoapi.md) e o backend central que recebe ortofotos, processa dados geoespaciais e orquestra regras de negocio. O [REURBWEB](./02-reurbweb.md) e o portal web usado por analistas para gestao de unidades, aprovacoes e geracao de relatorios. O [REURBCAD](./03-reurbcad.md) e o aplicativo mobile offline-first usado por equipes de campo para operacao apos publicacao do Analista.

O [ADMIN](./04-reurbmaster.md) e o console administrativo para gestao de tenants, usuarios e configuracoes do sistema. O [GEOGIS](./05-geogis.md) e o plugin QGIS para georreferenciamento de poligonos e publicacao de dados para campo. O [WEBDOCS](./06-webdocs.md) e o portal de documentacao tecnica construido com Astro/Starlight. O [KEYCLOAK](./07-keycloak.md) e o identity provider que centraliza autenticacao OAuth2/OIDC para todos os sistemas. O [catalogo de repositorios](./08-repository-catalog.md) documenta a estrutura polyrepo com os repositorios independentes e suas responsabilidades.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (8)

| Documento | Status |
|-----------|--------|
| [GEOAPI](./01-geoapi.md) | ⚠ |
| [REURBWEB](./02-reurbweb.md) | ⚠ |
| [REURBCAD](./03-reurbcad.md) | ⚠ |
| [ADMIN](./04-reurbmaster.md) | ⚠ |
| [GEOGIS](./05-geogis.md) | ⚠ |
| [WEBDOCS](./06-webdocs.md) | ⚠ |
| [KEYCLOAK](./07-keycloak.md) | ⚠ |
| [Catalogo de Repositorios](./08-repository-catalog.md) | ⚠ |

<!-- CARF-INDEX-END -->
