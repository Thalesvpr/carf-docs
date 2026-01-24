---
type: readme
status: review
updated: 2026-01-24
---

# Documentacao @carf/tscore

Documentacao tecnica completa da biblioteca core TypeScript compartilhada entre todos os projetos do ecossistema CARF. Esta biblioteca fornece value objects com validacoes brasileiras, tipos de dominio, cliente de autenticacao Keycloak e hooks para React e Vue.

A documentacao esta organizada em seis secoes principais. As [especificacoes tecnicas](./SPECS/README.md) detalham configuracoes de package.json, tsconfig e exports map necessarias para build e publicacao. As [decisoes arquiteturais](./ADRs/README.md) registram o historico de escolhas tecnicas fundamentais da biblioteca. A [arquitetura](./ARCHITECTURE/README.md) descreve a estrutura de modulos, subpath exports e integracao com projetos consumidores.

Os [conceitos](./CONCEPTS/README.md) explicam value objects imutaveis, sistema de autenticacao OAuth2 PKCE e tipos TypeScript compartilhados. A [referencia de API](./API/README.md) documenta todas as classes, interfaces e funcoes publicas. Os [guias praticos](./HOW-TO/README.md) orientam desenvolvedores na instalacao, uso e publicacao da biblioteca.

A biblioteca exporta quatro modulos principais via subpath exports. O modulo validations fornece CPF, CNPJ, Email e Phone como value objects. O modulo types disponibiliza interfaces Unit, Holder, Community e enums como UnitStatus e Role. O modulo auth oferece KeycloakClient com suporte a PKCE. Os modulos auth/react e auth/vue fornecem hooks especificos para cada framework.

<!-- CARF-INDEX-START -->
<!-- CARF-INDEX-END -->
