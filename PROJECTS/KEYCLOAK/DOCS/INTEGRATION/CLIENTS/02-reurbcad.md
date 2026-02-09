---
type: leaf
status: review
updated: 2026-01-19
---

# Client REURBCAD

App mobile React Native para coleta em campo configurado como public client com PKCE S256 e deep links para callback OAuth em ambiente mobile.

Redirect URIs incluem carf://callback e carf://oauth/callback como custom scheme para capturar callback OAuth após login no browser do dispositivo, exp://localhost:19000/* e exp://192.168.*.*:*/* para desenvolvimento com Expo em rede local, e http://localhost:19006/* para Expo web. Deep links configurados no app via react-native-app-auth para interceptar redirecionamentos e extrair authorization code.

Armazenamento seguro de tokens utiliza react-native-keychain no iOS (Keychain Services criptografado por hardware) e EncryptedSharedPreferences no Android para refresh_token. Access token mantido em memória volátil nunca persistido em storage acessível.

Modo offline: app armazena dados localmente em WatermelonDB, verifica conectividade antes de refresh token. Para offline real deve solicitar scope offline_access obtendo offline refresh token com idle timeout de 30 dias (offlineSessionIdleTimeout: 2592000). Sem offline_access, Remember Me estende sessão para idle 1 dia / max 7 dias. Ao voltar online tenta refresh e sincroniza dados pendentes. Se refresh falha por token expirado, redireciona para login.
