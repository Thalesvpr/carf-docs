---
type: readme
status: review
updated: 2026-01-24
---

# Arquitetura

Documentacao arquitetural da biblioteca @carf/tscore descrevendo estrutura de modulos, patterns de design e integracao com projetos consumidores.

A [estrutura de pacote](./01-package-structure.md) apresenta a organizacao interna da biblioteca. O diretorio src/ contem quatro modulos principais: validations com value objects, types com interfaces de dominio, auth com cliente Keycloak e adapters para React e Vue. Cada modulo exporta via subpath exports permitindo importacoes granulares.

A arquitetura segue principios de biblioteca compartilhada publicada via npm. Value objects sao imutaveis com validacao no construtor, garantindo que instancias sempre representam dados validos. Tipos TypeScript espelham modelos do backend .NET para consistencia entre frontend e API. O cliente de autenticacao abstrai OAuth2 PKCE com storage configuravel.

Projetos REURBWEB, REURBCAD, REURBMASTER e WEBDOCS consomem a biblioteca via GitHub Packages. Cada projeto configura .npmrc com registry @carf e instala com bun add @carf/tscore. Desenvolvimento local usa npm link para testar mudancas antes de publicar.

A biblioteca nao possui dependencias de runtime exceto Zod para schemas. React e Vue sao peer dependencies opcionais carregadas apenas quando auth/react ou auth/vue sao importados. Esta abordagem minimiza bundle size e evita conflitos de versao.

<!-- CARF-INDEX-START -->
<!-- CARF-INDEX-END -->
