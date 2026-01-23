---
type: leaf
status: current
updated: 2026-01-22
---

# Catalogo de Repositorios

O ecossistema CARF utiliza sete repositorios ativos organizados em arquitetura polyrepo, onde cada projeto tem deploy, versionamento e ownership independentes. Esta organizacao reflete a separacao de responsabilidades entre equipes e tecnologias distintas.

O repositorio carf-docs concentra toda documentacao central incluindo especificacoes, requisitos, arquitetura e padroes. O carf-geoapi contem o backend .NET com API REST geoespacial e integracao PostGIS. O carf-geoweb e o portal React para analistas com gestao de processos REURB. O carf-reurbcad e o aplicativo mobile React Native para coleta em campo com suporte offline-first. O carf-geogis fornece o plugin QGIS Python para analises espaciais avancadas.

Complementando o ecossistema, carf-webdocs hospeda o portal publico VitePress com documentacao tecnica e guias de usuario, enquanto carf-keycloak contem customizacoes de autenticacao incluindo temas em portugues e validacao de CPF. Dois repositorios adicionais estao planejados: carf-tscore para biblioteca TypeScript compartilhada e carf-admin para console administrativo. O backend e consumido pelos frontends via API REST, e o Keycloak fornece autenticacao OAuth2 para todos os clientes.
