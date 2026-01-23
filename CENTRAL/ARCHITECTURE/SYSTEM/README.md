---
type: readme
status: current
updated: 2026-01-22
---

# SYSTEM

Documentacao dos sistemas que compoem o ecossistema CARF descrevendo proposito, usuarios-alvo, capacidades principais e dependencias de cada um. Fornece visao conceitual de alto nivel sem entrar em detalhes de implementacao.

O ecossistema CARF e composto por sete sistemas integrados que atendem diferentes perfis de usuario e contextos de uso. O [GEOAPI](./01-geoapi.md) e o backend central que expoe API REST para todos os clientes, processando dados geoespaciais e orquestrando regras de negocio. O [GEOWEB](./02-geoweb.md) e o portal web usado por analistas para gestao de unidades, aprovacoes e geracao de relatorios. O [REURBCAD](./03-reurbcad.md) e o aplicativo mobile offline-first usado por equipes de campo para coleta de dados cadastrais in loco.

O [ADMIN](./04-admin.md) e o console administrativo para gestao de tenants, usuarios e configuracoes do sistema. O [GEOGIS](./05-geogis.md) e um plugin QGIS para analises espaciais avancadas e geoprocessamento batch. O [WEBDOCS](./06-webdocs.md) e o portal de documentacao tecnica construido com Astro/Starlight. O [KEYCLOAK](./07-keycloak.md) e o identity provider que centraliza autenticacao OAuth2/OIDC para todos os sistemas. O [catalogo de repositorios](./08-repository-catalog.md) documenta a estrutura polyrepo com os sete repositorios independentes e suas responsabilidades.

Para detalhes tecnicos de implementacao de cada sistema consulte a documentacao especifica em PROJECTS/*/DOCS/.

<!-- CARF-INDEX-START -->

<!-- CARF-INDEX-END -->
