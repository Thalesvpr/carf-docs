---
type: leaf
status: review
updated: 2026-01-24
---

# Abstracao de Navegacao

Interface NavigationAdapter permite que KeycloakClient redirecione usuarios em diferentes ambientes sem dependencia direta de window.location.

## Motivacao

Fluxo OAuth2 requer redirecionamento para servidor de autorizacao e retorno para aplicacao. Em browser, KeycloakClient usava window.location.href diretamente. React Native nao tem window.location, exigindo expo-linking para deep links. A abstracao permite mesma logica OAuth2 com mecanismos de navegacao diferentes.

## Interface NavigationAdapter

Interface define dois metodos para navegacao. Metodo redirect recebe URL e navega para destino de forma adequada ao ambiente. Metodo getCurrentUrl retorna URL atual para processamento de callback OAuth2. Ambos metodos retornam Promise para compatibilidade com APIs assincronas.

## WebNavigationAdapter

Implementacao para browser usando window.location. Metodo redirect atribui URL a window.location.href causando navegacao completa. Metodo getCurrentUrl retorna window.location.href incluindo query parameters do callback OAuth2. Usado em GEOWEB, ADMIN e WEBDOCS.

## MobileNavigationAdapter

Implementacao para React Native usando expo-linking. Metodo redirect chama Linking.openURL para abrir navegador externo ou processar deep link. Metodo getCurrentUrl parseia URL de entrada registrada no app.json como scheme. Callback OAuth2 retorna via deep link configurado como redirect_uri.

## Configuracao de Deep Link

Aplicacao mobile configura scheme no app.json como reurbcad://callback. Keycloak client registra essa URL como redirect_uri valida. Apos autenticacao, Keycloak redireciona para deep link que reativa app mobile com code e state nos query parameters para troca por tokens.
