---
type: readme
status: review
updated: 2026-01-24
---

# Conceitos

Documentacao dos conceitos fundamentais da biblioteca @carf/tscore cobrindo patterns de design, validacoes e autenticacao.

Os [value objects](./01-value-objects.md) explicam o pattern de objetos imutaveis comparados por valor. CPF, CNPJ, Email e Phone encapsulam validacao no construtor, garantindo que instancias sempre contenham dados validos. O documento detalha algoritmos de validacao brasileiros e metodos de formatacao.

A [autenticacao](./02-authentication.md) descreve integracao com Keycloak via OAuth2 Authorization Code com PKCE. KeycloakClient gerencia ciclo de vida de tokens com refresh automatico, extracao de roles do JWT e verificacao de permissoes hierarquicas. Hooks useAuth abstraem estado de autenticacao para React e Vue.

Os [tipos TypeScript](./03-typescript-types.md) documentam interfaces de dominio sincronizadas com backend .NET. Entidades Unit, Holder e Community representam dados cadastrais de regularizacao fundiaria. Enums definem estados de workflow e hierarquia de permissoes. DTOs especificam contratos de API.

A [abstracao de storage](./04-storage-abstraction.md) apresenta interface StorageAdapter para persistencia cross-platform. Permite que KeycloakClient use localStorage em web e expo-secure-store em mobile sem modificar logica OAuth2.

A [abstracao de navegacao](./05-navigation-abstraction.md) documenta interface NavigationAdapter para redirecionamentos. Suporta window.location em web e deep linking em React Native para callbacks OAuth2.

<!-- CARF-INDEX-START -->
<!-- CARF-INDEX-END -->
