---
type: leaf
status: review
updated: 2026-02-08
---

# API de Autenticacao Nativa

Extensoes do modulo @carf/tscore/auth para suporte cross-platform em ambientes React Native, desktop e testes. Os adapters permitem que o KeycloakClient opere sem modificar a logica OAuth2 core, delegando operacoes de storage e navegacao para implementacoes especificas de cada plataforma.

## StorageAdapter

Interface para abstracao de persistencia de tokens. Todas as operacoes sao assincronas para compatibilidade com APIs mobile que usam storage criptografado nativo.

| Metodo | Parametros | Retorno | Descricao |
|:-------|:-----------|:--------|:----------|
| getItem | key: string | Promise de string ou null | Busca valor pelo key, retorna null se inexistente |
| setItem | key: string, value: string | Promise de void | Persiste par key-value de forma assincrona |
| removeItem | key: string | Promise de void | Remove item pelo key |

Keys utilizados pelo KeycloakClient: "carf_access_token" para o JWT, "carf_refresh_token" para o refresh token, "carf_id_token" para o ID token, "carf_expires_at" para timestamp de expiracao, "carf_code_verifier" para o PKCE verifier temporario durante login e "carf_state" para o state CSRF temporario durante login.

## NavigationAdapter

Interface para abstracao de redirecionamentos OAuth2. Permite que o fluxo de login funcione tanto com window.location em web quanto com deep linking em React Native.

| Metodo | Parametros | Retorno | Descricao |
|:-------|:-----------|:--------|:----------|
| redirect | url: string | Promise de void | Navega para URL de autorizacao do Keycloak |
| getCurrentUrl | | Promise de string | Retorna URL atual incluindo query params para processar callback |

## WebStorageAdapter

Classe implementando StorageAdapter usando localStorage do navegador. Construtor sem parametros. Metodos delegam diretamente para localStorage.getItem, localStorage.setItem e localStorage.removeItem, envolvendo resultado em Promise.resolve. Recomendado apenas para access_token de curta duracao; refresh_token deve preferencialmente usar HttpOnly cookies em producao conforme documentado em [02a-authentication-config](../CONCEPTS/02a-authentication-config.md).

## MobileStorageAdapter

Classe implementando StorageAdapter usando expo-secure-store para React Native. Construtor sem parametros, requer expo-secure-store como dependencia do projeto consumidor. Metodos delegam para SecureStore.getItemAsync, SecureStore.setItemAsync e SecureStore.deleteItemAsync, que utilizam keychain no iOS e encrypted shared preferences no Android. O armazenamento e criptografado nativamente pelo sistema operacional, adequado para tokens de longa duracao como o refresh_token de 30 dias do REURBCAD com scope offline_access.

## WebNavigationAdapter

Classe implementando NavigationAdapter usando window.location para aplicacoes web. Metodo redirect atribui URL a window.location.href, causando navegacao completa da pagina para o Keycloak. Metodo getCurrentUrl retorna window.location.href como Promise, permitindo extracaoo de code e state dos query params apos callback.

## MobileNavigationAdapter

Classe implementando NavigationAdapter usando expo-linking para React Native. Construtor recebe scheme (string correspondente ao registrado em app.json, por exemplo "carf") que define o prefixo do deep link. Metodo redirect abre URL via Linking.openURL, que invoca o browser do sistema para a pagina de login do Keycloak. Metodo getCurrentUrl parseia a entrada de deep link no formato carf://callback?code=xxx&state=yyy, usando Linking.getInitialURL para cold start e Linking.addEventListener para warm start. O redirectUri configurado no KeycloakClient deve ser carf://callback para corresponder ao deep link registrado.

## KeycloakClientOptions

Interface estendida de KeycloakConfig com campos opcionais para injecao de adapters.

| Propriedade | Tipo TS | Obrigatorio | Descricao |
|:------------|:--------|:------------|:----------|
| storage | StorageAdapter | nao | Adapter de storage customizado |
| navigation | NavigationAdapter | nao | Adapter de navegacao customizado |

Se nenhum adapter for fornecido, o KeycloakClient detecta o ambiente automaticamente: verifica se window e localStorage existem para usar WebStorageAdapter e WebNavigationAdapter, caso contrario tenta importar expo-secure-store e expo-linking para usar MobileStorageAdapter e MobileNavigationAdapter. Para testes unitarios, passar mocks que implementem as interfaces facilita isolamento sem dependencias de plataforma.

## Configuracao por Plataforma

Para REURBWEB e REURBMASTER (web), usa-se WebStorageAdapter com WebNavigationAdapter. O clientId e "reurbweb-client" ou "admin-client", o redirectUri e a URL do app seguida de /callback, e o scope inclui "openid profile".

Para REURBCAD (mobile), usa-se MobileStorageAdapter com MobileNavigationAdapter. O clientId e "reurbcad-client", o redirectUri e "carf://callback", e o scope inclui "openid profile offline_access" para refresh token de 30 dias que permite sessao persistente entre idas a campo.

Para GEOGIS (desktop QGIS), o plugin Python implementa seu proprio adapter de storage usando QSettings e adapter de navegacao que abre o browser padrao via webbrowser.open, consumindo a mesma logica PKCE.
