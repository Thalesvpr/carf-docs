---
type: adr
status: approved
updated: 2026-01-24
---

# ADR-002: Abstracao de Storage e Navegacao para Auth

## Contexto

KeycloakClient dependia diretamente de localStorage, sessionStorage e window.location, APIs exclusivas de browser. React Native com Expo requer expo-secure-store para armazenamento seguro de tokens e deep linking para callbacks OAuth2. Essa dependencia impedia reutilizacao da logica OAuth2 PKCE em aplicativos mobile.

## Decisao

Abstrair storage e navegacao via interfaces injetadas no construtor do KeycloakClient. Interface StorageAdapter define metodos getItem, setItem e removeItem para persistencia. Interface NavigationAdapter define metodo redirect para redirecionamentos. Criar WebStorageAdapter usando localStorage e WebNavigationAdapter usando window.location. Criar MobileStorageAdapter usando expo-secure-store e MobileNavigationAdapter usando expo-linking para deep links.

## Consequencias

Logica OAuth2 PKCE permanece compartilhada entre plataformas sem duplicacao. Cada plataforma implementa apenas adapters especificos. Testes unitarios usam mocks dos adapters sem dependencias de browser. Tokens em mobile ficam armazenados com seguranca nativa. Configuracao inicial requer instanciacao explicita dos adapters adequados.

## Alternativas Rejeitadas

Criar KeycloakClientNative separado duplicaria toda logica OAuth2 complexa com PKCE, refresh e extracao de roles. Usar biblioteca terceira como react-native-app-auth perderia integracao com tipos do tscore e exigiria mapeamento manual de dados.
