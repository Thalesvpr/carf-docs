---
type: leaf
status: review
updated: 2026-01-24
---

# Usando Tipos

Guia para consumir @carf/tscore em projetos do ecossistema CARF cobrindo instalacao, configuracao e exemplos de uso.

## Configuracao do Registry

Projetos devem configurar arquivo .npmrc na raiz com linha @carf:registry=https://npm.pkg.github.com para direcionar pacotes @carf para GitHub Packages. Autenticacao usa GITHUB_TOKEN do ambiente definido em .env ou CI secrets.

## Instalacao

Executar bun add @carf/tscore instala biblioteca e dependencias. React ou Vue sao peer dependencies opcionais instaladas apenas se projeto ja usa esses frameworks. Zod e unica dependencia runtime sempre instalada.

## Importando Validacoes

Importar CPF, CNPJ, Email ou Phone de @carf/tscore/validations. Usar construtor para criar instancia validada que lanca erro se invalida. Usar metodo estatico isValid para validar sem lancar excecao. Integrar com react-hook-form via funcao validate customizada que retorna mensagem de erro ou true.

## Importando Tipos

Importar interfaces usando type keyword como Unit, Holder e Community de @carf/tscore/types. Importar enums como UnitStatus e Role diretamente para uso em comparacoes. Usar tipos em definicoes de estado React, props de componentes e retornos de queries TanStack Query. Tipos garantem autocomplete e previnem erros de digitacao.

## Integracao com REURBWEB

REURBWEB importa tipos para TanStack Query tipando retornos de API. Validacoes integram com formularios react-hook-form. AuthProvider envolve App com KeycloakClient configurado. useAuth fornece estado de autenticacao em componentes.

## Integracao com REURBCAD

REURBCAD usa tipos para modelos WatermelonDB mantendo consistencia com API. Validacoes executam offline antes de sincronizar. Adapter de storage usa expo-secure-store para tokens em vez de localStorage. NavigationAdapter usa deep linking para callbacks OAuth2.

## Integracao com ADMIN e WEBDOCS

ADMIN usa Next.js com AuthProvider em client component separado. WEBDOCS usa VitePress com initAuth em configuracao de theme. Ambos consomem mesma biblioteca com integracao especifica de framework.
