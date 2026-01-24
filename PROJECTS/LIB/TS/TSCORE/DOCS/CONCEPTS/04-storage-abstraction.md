---
type: leaf
status: review
updated: 2026-01-24
---

# Abstracao de Storage

Interface StorageAdapter permite que KeycloakClient persista tokens em diferentes ambientes sem dependencia direta de APIs de browser.

## Motivacao

KeycloakClient original usava localStorage diretamente para armazenar tokens OAuth2. Essa abordagem funciona em browser mas impede uso em React Native onde localStorage nao existe. Mobile requer expo-secure-store para armazenamento criptografado de credenciais sensiveis. A abstracao permite mesma logica OAuth2 com backends de storage diferentes.

## Interface StorageAdapter

Interface define tres metodos para persistencia. Metodo getItem recebe key e retorna Promise com valor ou null. Metodo setItem recebe key e value persistindo de forma assincrona. Metodo removeItem recebe key e remove item correspondente. Todos metodos retornam Promise para compatibilidade com APIs assincronas de storage mobile.

## WebStorageAdapter

Implementacao para browser usando localStorage. Metodos getItem, setItem e removeItem delegam para localStorage.getItem, setItem e removeItem envolvendo em Promise.resolve para manter assinatura assincrona. Usado por padrao em GEOWEB, ADMIN e WEBDOCS.

## MobileStorageAdapter

Implementacao para React Native usando expo-secure-store. SecureStore armazena dados criptografados no Keychain iOS ou Keystore Android. Metodos delegam para SecureStore.getItemAsync, setItemAsync e deleteItemAsync. Tokens ficam protegidos mesmo se dispositivo for comprometido.

## Uso no KeycloakClient

Construtor de KeycloakClient recebe opcao storage opcional. Se nao fornecido, detecta ambiente e usa adapter apropriado. Em ambientes customizados, aplicacao passa adapter explicito. Esta inversao de dependencia permite testabilidade com mocks de storage.
