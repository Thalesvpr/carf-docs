---
type: leaf
status: review
updated: 2026-02-08
---

# Troubleshooting

Guia de resolucao de problemas comuns durante desenvolvimento e uso do REURBCAD, organizado por categoria com sintoma, causa provavel e solucao.

## Build e Compilacao

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| `Build failed: Could not resolve dependency` | Conflito de versoes entre pacotes npm | Executar `npm install --legacy-peer-deps`. Se persistir, deletar `node_modules` e `package-lock.json`, depois `npm install` novamente. |
| `Android build fails: SDK not found` | Variavel `ANDROID_HOME` nao configurada | Configurar `ANDROID_HOME` apontando para o SDK Android. No Windows: `setx ANDROID_HOME "%LOCALAPPDATA%\Android\Sdk"`. No macOS/Linux: `export ANDROID_HOME=$HOME/Library/Android/sdk`. |
| `iOS build fails: pod install error` | CocoaPods desatualizado ou cache corrompido | Executar `cd ios && pod deintegrate && pod cache clean --all && pod install && cd ..`. Se necessario, instalar versao mais recente: `sudo gem install cocoapods`. |
| `EAS build fails: credentials error` | Keystore Android ou provisioning iOS nao configurados | Para Android: `eas credentials --platform android`. Para iOS: `eas credentials --platform ios`. Seguir wizard de configuracao. |
| `EAS build fails: missing env vars` | Variaveis de ambiente nao definidas no profile EAS | Verificar `eas.json` e garantir que o profile tem todas as `EXPO_PUBLIC_*` necessarias. Consultar [Environment Variables](./05-environment-variables.md). |
| `TypeScript error: Cannot find module '@carf/tscore'` | Workspace links nao resolvidos | Executar `npm link @carf/tscore @carf/geoapi-client` ou verificar paths em `tsconfig.json`. |
| `Gradle build failed: Java version` | Versao do Java incompativel com Gradle | Instalar OpenJDK 17. Configurar `JAVA_HOME`. Verificar com `java -version`. |

## Metro Bundler e Dev Server

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Metro bundler lento (>30s para bundle) | Cache corrompido ou muitos watchers | Limpar cache: `npx expo start --clear`. No Windows, adicionar pasta do projeto as exclusoes do antivirus. |
| `Error: ENOSPC: System limit for file watchers reached` (Linux) | Limite de inotify watchers atingido | Aumentar limite: `echo fs.inotify.max_user_watches=524288 \| sudo tee -a /etc/sysctl.conf && sudo sysctl -p`. |
| `Port 8081 already in use` | Outro processo Metro rodando | Matar processo: Windows `netstat -ano \| findstr :8081` depois `taskkill /PID <pid> /F`. macOS/Linux: `lsof -i :8081` depois `kill -9 <pid>`. |
| Hot reload nao funciona | Fast Refresh desconectado | Pressionar `r` no terminal do Metro. Se persistir, fechar e reabrir o app no emulador. |
| `Unable to resolve module` apos instalar pacote | Metro cache desatualizado | Parar Metro, executar `npx expo start --clear` para limpar cache do bundler. |

## Deep Link e Autenticacao

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Deep link nao retorna ao app apos login no Keycloak | Scheme nao configurado ou redirect URI errado | Verificar que `app.json` tem `"scheme": "carf"`. Verificar no Keycloak que o client `reurbcad` tem redirect URI `carf://oauth/callback`. No Android, verificar `intentFilters` no `app.json`. |
| Login abre mas retorna erro `invalid_redirect_uri` | Redirect URI no Keycloak nao bate com o app | No Keycloak Admin > Clients > reurbcad > Valid Redirect URIs, adicionar `carf://oauth/callback`. Salvar. |
| Token refresh loop (app faz login, expira, login, expira...) | Access token lifetime muito curto no Keycloak | Verificar Keycloak > Realm Settings > Tokens > Access Token Lifespan. Deve ser 5 minutos (300 segundos) minimo. O app faz refresh 60 segundos antes de expirar. |
| Login funciona no emulador mas nao no device fisico | URL do Keycloak usando localhost | Trocar `EXPO_PUBLIC_KEYCLOAK_URL` para IP da maquina na rede local (ex: `http://192.168.1.100:8080`). Garantir que firewall permite conexao na porta. |
| `SecureStore error: Could not encrypt` | SecureStore nao disponivel no emulador sem Google Play | Usar emulador com Google Play APIs. AVD deve usar system image com `Google Play`. |

## WatermelonDB e Dados Locais

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| `WatermelonDB migration error` ao abrir app | Schema version do codigo maior que do banco local sem migration correspondente | Adicionar migration step em `src/database/migrations.ts` para a nova versao. Cada alteracao de schema exige uma migration. Se em dev, pode resetar: `database.write(async () => await database.unsafeResetDatabase())`. |
| `Cannot read property of undefined` ao acessar relacao | Registro relacionado nao existe localmente | Verificar se o pull de sync trouxe o registro. Usar `.observe()` com null check no componente. Exibir placeholder se registro nao encontrado. |
| Dados nao aparecem apos sync | Query filtrando por tenant_id errado | Verificar `useAuthStore().tenant.id`. Garantir que dados no servidor pertencem ao tenant do usuario logado. |
| `Database disk image is malformed` | Corrupcao do SQLite (crash durante escrita) | Forcar reset do database: desinstalar e reinstalar o app. Dados nao sincronizados serao perdidos. Reportar como bug. |
| App crash ao abrir com muitos registros | WatermelonDB tentando carregar muitos registros de uma vez | Usar paginacao nas queries: `.query(Q.take(50), Q.skip(offset))`. Implementar FlatList com `onEndReached` para lazy loading. |

## Camera e Permissoes

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Camera permission denied | Usuario negou permissao ou permissao revogada | Exibir tela explicativa com botao "Abrir Configuracoes" que chama `Linking.openSettings()`. Usuario deve conceder manualmente em Configuracoes > Apps > REURBCAD > Permissoes. |
| Foto salva mas aparece preta ou corrompida | Problema de compressao ou path incorreto | Verificar que `expo-image-manipulator` usa quality entre 0.7 e 0.9. Verificar que o path retornado e acessivel via `FileSystem.getInfoAsync()`. |
| Camera travando no emulador | Emulador sem suporte a camera | Usar webcam do host: AVD > Advanced Settings > Camera > Front/Back > Webcam. Ou testar em dispositivo fisico. |
| Permissao de localizacao negada permanentemente | Usuario selecionou "Nao perguntar novamente" | Unica opcao e direcionar para configuracoes do sistema: `Linking.openSettings()`. Exibir mensagem explicando que GPS e obrigatorio. |

## Sincronizacao

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Sync trava / timeout apos varios minutos | Payload muito grande ou conexao lenta | Verificar `pendingCount` na sync store. Se > 500, pode ser lento. O app envia em batches de 50. Verificar conexao e tentar com WiFi. |
| Sync retorna 401 | Token expirado e refresh falhou | Verificar se offline token ainda valido (< 30 dias). Se expirado, fazer logout e login novamente. |
| Sync retorna 409 em todos os registros | `version` local muito antiga | Pode indicar que outro dispositivo atualizou massivamente. Resolver conflitos manualmente na tela de conflitos ou forcar pull completo. |
| Sync retorna 422 em registros especificos | Dados invalidos rejeitados pelo servidor | Verificar os registros marcados como FAILED na sync_queue. Corrigir dados (CPF invalido, campos obrigatorios vazios) e re-tentar. |
| Indicador de sync mostra "erro" permanente | Erro nao recuperavel na sync | Checar logs: `useSyncStore().errorMessage`. Causas comuns: schema incompativel (atualizar app), tenant invalido (contatar admin). |
| Sync em background nao executa | Background Fetch nao registrado ou sistema matou task | Verificar `EXPO_PUBLIC_BACKGROUND_SYNC=true`. No Android, desabilitar otimizacao de bateria para o app. No iOS, background fetch tem frequencia minima controlada pelo OS. |

## Mapa

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Map tiles nao carregam offline | Tiles nao foram pre-baixados | Executar download do pacote de regiao em E4 (Preparar Regiao) antes de ir a campo. Verificar espaco disponivel no dispositivo. |
| Poligonos nao aparecem no mapa | Dados GeoJSON nao baixados ou community sem boundary | Verificar que a community selecionada tem `boundary_geojson` preenchido. Executar sync para baixar dados atualizados. |
| Mapa lento com muitos poligonos | Renderizacao de centenas de poligonos simultaneos | Habilitar clustering: o app agrupa poligonos em zoom < 16. Verificar que `visibleLayers` nao tem layers desnecessarios ativos. |
| GPS mostra posicao errada no emulador | Emulador usando posicao padrao (Googleplex) | No emulador Android: Extended Controls > Location > definir lat/long manualmente. Ou usar arquivo GPX para simular rota. |
| Erro `MapView requires mapbox token` | Configuracao de provider de mapa incorreta | REURBCAD usa `react-native-maps` com provider Google Maps. Verificar que Google Maps API key esta configurada no `app.json` em `android.config.googleMaps.apiKey`. |

## Emulador e Performance

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Emulador Android extremamente lento | Virtualizacao nao habilitada (HAXM/KVM) | **Windows**: habilitar Hyper-V ou HAXM no BIOS. **Linux**: `sudo apt install qemu-kvm`. Verificar com `emulator -accel-check`. |
| App fecha sozinho (crash silencioso) | Out of memory no emulador | Aumentar RAM do AVD para 4096 MB. Reduzir numero de apps abertos no emulador. |
| Teclado cobre inputs no formulario | `KeyboardAvoidingView` nao configurado | Usar componente `KeyboardAvoidingWrapper` em todos os formularios. Verificar `behavior` prop: `padding` no iOS, `height` no Android. |
| ScrollView nao rola suavemente | Renderizacao pesada dentro do scroll | Usar `FlatList` ao inves de `ScrollView` para listas longas. Memorizar componentes pesados com `React.memo()`. |

## Dicas Gerais

1. **Sempre limpar cache do Metro primeiro**: `npx expo start --clear` resolve 60% dos problemas de desenvolvimento.
2. **Verificar logs do dispositivo**: `adb logcat *:E` (Android) ou Console do Xcode (iOS) para erros nativos nao visiveis no Metro.
3. **Reinstalar app no emulador**: Desinstalar completamente e instalar novo build resolve problemas de estado corrompido.
4. **Verificar versao do Expo SDK**: Garantir que todas as libs `expo-*` estao na versao compativel com o SDK 51. Usar `npx expo install --fix` para alinhar versoes.
5. **Consultar logs de sync**: A tela de sync (E11) mostra historico de tentativas de sincronizacao com timestamps e erros detalhados.

## Referencias

- [Setup Dev Environment](./04-setup-dev-environment.md)
- [Environment Variables](./05-environment-variables.md)
- [Error Handling](../ARCHITECTURE/05-error-handling.md)
- [WatermelonDB Schema](../DATA/01-watermelondb-schema.md)
- [Offline Sync](../FEATURES/03-offline-sync.md)
- [Keycloak Integration](../ARCHITECTURE/01-keycloak-integration.md)
