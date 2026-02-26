---
type: leaf
status: approved
updated: 2026-01-24
---

# Catalogo de Repositorios

O ecossistema CARF utiliza sete repositorios ativos organizados em arquitetura polyrepo, onde cada projeto tem deploy, versionamento e ownership independentes. Esta organizacao reflete a separacao de responsabilidades entre equipes e tecnologias distintas.

O repositorio carf-docs concentra toda documentacao central incluindo especificacoes, requisitos, arquitetura e padroes. O carf-geoapi contem o backend .NET com API REST geoespacial e integracao PostGIS. O carf-reurbweb e o portal React para analistas com gestao de processos REURB. O carf-reurbcad e o aplicativo mobile React Native para coleta em campo com suporte offline-first. O carf-geogis fornece o plugin QGIS Python para georreferenciamento de poligonos e publicacao de dados.

Complementando o ecossistema, carf-webdocs hospeda o portal publico VitePress com documentacao tecnica e guias de usuario, enquanto carf-keycloak contem customizacoes de autenticacao incluindo temas em portugues e validacao de CPF. Dois repositorios adicionais estao planejados: carf-tscore para biblioteca TypeScript compartilhada e carf-reurbmaster para console administrativo. O backend e consumido pelos frontends via API REST, e o Keycloak fornece autenticacao OAuth2 para todos os clientes.

## URLs dos Repositorios

| Repositorio | URL | Stack |
|---|---|---|
| carf-docs | https://github.com/Thalesvpr/carf-docs | Obsidian/Markdown |
| carf-geoapi | https://github.com/Thalesvpr/carf-geoapi | .NET 9 / PostGIS |
| carf-reurbweb | https://github.com/Thalesvpr/carf-reurbweb | React |
| carf-reurbcad | https://github.com/Thalesvpr/carf-reurbcad | React Native/Expo |
| carf-geogis | https://github.com/Thalesvpr/carf-geogis | QGIS/Python |
| carf-webdocs | https://github.com/Thalesvpr/carf-webdocs | VitePress |
| carf-keycloak | https://github.com/Thalesvpr/carf-keycloak | Keycloakify |
