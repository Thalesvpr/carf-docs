# Client REURBCAD

App mobile React Native para coleta em campo configurado como public client com PKCE S256 e deep links para callback OAuth em ambiente mobile.

Redirect URIs incluem carf://callback e carf://oauth/callback como custom scheme para capturar callback OAuth após login no browser do dispositivo, e exp://localhost:19000/* para desenvolvimento com Expo. Deep links configurados no app via react-native-app-auth para interceptar redirecionamentos e extrair authorization code.

Armazenamento seguro de tokens utiliza react-native-keychain no iOS (Keychain Services criptografado por hardware) e EncryptedSharedPreferences no Android para refresh_token. Access token mantido em memória volátil nunca persistido em storage acessível.

Modo offline: app armazena dados localmente em SQLite/WatermelonDB, verifica conectividade antes de refresh token, se offline usa token cacheado até expirar (máximo 24h com Remember Me), ao voltar online tenta refresh e sincroniza dados pendentes. Se refresh falha por token expirado, redireciona para login.

---

**Status:** Review
**Atualizado:** 2026-01-19
**Descrição:** 
