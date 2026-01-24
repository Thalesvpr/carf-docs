---
type: leaf
status: review
updated: 2026-01-24
---

# API de Autenticacao Nativa

Extensoes do modulo @carf/tscore/auth para suporte cross-platform em ambientes React Native.

## StorageAdapter

Interface para abstracao de persistencia de tokens. Metodo getItem recebe key string e retorna Promise de string ou null. Metodo setItem recebe key e value strings persistindo de forma assincrona. Metodo removeItem recebe key string e deleta item. Todas operacoes sao assincronas para compatibilidade com APIs mobile.

## NavigationAdapter

Interface para abstracao de redirecionamentos OAuth2. Metodo redirect recebe URL string e navega para destino. Metodo getCurrentUrl retorna Promise de string com URL atual incluindo query parameters. Usado para processar callback do servidor de autorizacao.

## WebStorageAdapter

Classe implementando StorageAdapter usando localStorage. Construtor nao recebe parametros. Metodos delegam para localStorage envolvendo resultado em Promise. Exportada para uso explicito em ambiente web quando necessario.

## MobileStorageAdapter

Classe implementando StorageAdapter usando expo-secure-store. Construtor nao recebe parametros. Requer expo-secure-store instalado como dependencia. Metodos delegam para SecureStore com armazenamento criptografado nativo.

## WebNavigationAdapter

Classe implementando NavigationAdapter usando window.location. Metodo redirect atribui a window.location.href. Metodo getCurrentUrl retorna window.location.href como Promise.

## MobileNavigationAdapter

Classe implementando NavigationAdapter usando expo-linking. Construtor recebe scheme string correspondente ao registrado em app.json. Metodo redirect abre URL via Linking.openURL. Metodo getCurrentUrl parseia entrada de deep link.

## KeycloakClientOptions

Interface estendida com campos opcionais storage e navigation. Ambos recebem implementacoes de adapter. Se nao fornecidos, KeycloakClient detecta ambiente automaticamente instanciando adapters apropriados. Para ambientes customizados ou testes, passar adapters explicitos ou mocks.
