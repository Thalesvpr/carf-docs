---
type: readme
status: current
updated: 2026-01-22
---

# ARCHITECTURE

Documentacao da arquitetura sistemica do CARF definindo sistemas, integracoes, decisoes tecnicas e padroes obrigatorios para todos os projetos do ecossistema.

A pasta [SYSTEM](./SYSTEM/README.md) documenta cada sistema do ecossistema CARF incluindo GEOAPI, GEOWEB, REURBCAD, ADMIN, GEOGIS, WEBDOCS e KEYCLOAK, descrevendo proposito, usuarios-alvo, capacidades e dependencias de cada um sem entrar em detalhes de implementacao. A pasta [INTEGRATION](./INTEGRATION/README.md) explica como os sistemas se comunicam cobrindo autenticacao OAuth2/OIDC, comunicacao via API REST, sincronizacao offline do mobile, bibliotecas compartilhadas e camada de dados PostgreSQL/PostGIS.

A pasta [DECISIONS](./DECISIONS/README.md) contem Architecture Decision Records documentando escolhas arquiteturais significativas como multi-tenancy via RLS, offline-first com WatermelonDB, Keycloak como identity provider, e stack tecnologico de backend e frontend. A pasta [STANDARDS](./STANDARDS/README.md) define padroes obrigatorios para documentacao, codigo, commits e design de API que todos os projetos devem seguir. A pasta [DIAGRAMS](./DIAGRAMS/README.md) fornece visualizacoes Mermaid do ecossistema, fluxo de dados e topologia de deployment.

Para implementacao tecnica especifica de cada projeto incluindo arquitetura de codigo, configuracoes, guias de desenvolvimento e estrategias de deployment, consulte a documentacao em PROJECTS/*/DOCS/.

<!-- CARF-INDEX-START -->
> **Indice gerado automaticamente.** Nao edite manualmente.

<!-- CARF-INDEX-END -->
