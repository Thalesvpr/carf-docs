---
type: leaf
status: review
updated: 2026-02-08
---

# Setup do Ambiente de Desenvolvimento

Guia passo-a-passo para configurar o ambiente de desenvolvimento do REURBCAD React Native + Expo do zero. Ao final, o desenvolvedor tera o app rodando em um emulador Android ou simulador iOS conectado ao backend local.

## Pre-Requisitos

| Ferramenta | Versao Minima | Descricao |
|------------|---------------|-----------|
| Node.js | 20 LTS | Runtime JavaScript |
| npm ou yarn | npm 10+ / yarn 1.22+ | Gerenciador de pacotes |
| Git | 2.40+ | Controle de versao |
| Docker Desktop | 4.25+ | Container runtime para backend |
| Android Studio | Hedgehog (2023.1.1)+ | IDE e emulador Android |
| Xcode | 15+ (macOS only) | IDE e simulador iOS |
| Expo CLI | SDK 51 | Ferramenta de desenvolvimento Expo |
| VS Code | Qualquer | IDE recomendada |

### Extensoes VS Code Recomendadas

- ESLint
- Prettier
- React Native Tools
- Expo Tools
- GitLens

## Passo 1: Clonar o Repositorio

```bash
git clone https://github.com/carf-gov-br/reurbcad.git
cd reurbcad
```

## Passo 2: Instalar Dependencias

```bash
npm install
```

Se houver erros de peer dependencies, usar:

```bash
npm install --legacy-peer-deps
```

Verificar instalacao:

```bash
npx expo --version
# Deve exibir 51.x.x
```

## Passo 3: Configurar Variaveis de Ambiente

Copiar o arquivo de exemplo e preencher:

```bash
cp .env.example .env.development
```

Editar `.env.development` com os valores locais:

```env
EXPO_PUBLIC_API_URL=http://10.0.2.2:5000
EXPO_PUBLIC_KEYCLOAK_URL=http://10.0.2.2:8080
EXPO_PUBLIC_KEYCLOAK_REALM=carf
EXPO_PUBLIC_KEYCLOAK_CLIENT_ID=reurbcad
EXPO_PUBLIC_DEEP_LINK_SCHEME=carf
EXPO_PUBLIC_SENTRY_DSN=
EXPO_PUBLIC_MAP_TILE_URL=
```

**Nota importante**: `10.0.2.2` e o IP especial do emulador Android que aponta para `localhost` da maquina host. Para iOS Simulator, use `localhost` diretamente. Para dispositivo fisico na mesma rede, use o IP da maquina (ex: `192.168.1.100`).

Consulte a documentacao completa de variaveis em [Environment Variables](./05-environment-variables.md).

## Passo 4: Iniciar o Backend Local

O backend completo (GEOAPI + PostgreSQL + Keycloak + Redis) roda via Docker Compose:

```bash
# Na raiz do monorepo ou no diretorio do backend
cd ../geoapi
docker compose up -d
```

Verificar se todos os servicos estao saudaveis:

```bash
docker compose ps
```

Servicos esperados:

| Servico | Porta | Health Check |
|---------|-------|-------------|
| GEOAPI (.NET) | 5000 | `http://localhost:5000/health` |
| PostgreSQL | 5432 | `docker exec postgres pg_isready` |
| Keycloak | 8080 | `http://localhost:8080/health/ready` |
| Redis | 6379 | `docker exec redis redis-cli ping` |

Aguardar ate 2 minutos para o Keycloak inicializar completamente (importacao do realm `carf` e criacao dos clients).

### Verificar Keycloak

1. Acessar `http://localhost:8080/admin/master/console/`
2. Login: `admin` / `admin` (apenas local)
3. Trocar para realm `carf` no dropdown superior esquerdo
4. Verificar que o client `reurbcad` existe em Clients
5. Verificar que o redirect URI `carf://oauth/callback` esta configurado

## Passo 5: Criar Conta Expo (EAS)

```bash
npx expo login
# Criar conta em https://expo.dev se ainda nao tem
```

Para builds locais de desenvolvimento, a conta Expo e necessaria para o Dev Client.

## Passo 6: Configurar Emulador Android

### 6.1 Instalar Android Studio

1. Baixar em https://developer.android.com/studio
2. Instalar com componentes padrao
3. Abrir Android Studio > SDK Manager > SDK Platforms
4. Instalar **Android 14 (API 34)** com Google Play APIs

### 6.2 Criar AVD (Android Virtual Device)

1. Android Studio > Device Manager > Create Device
2. Selecionar **Pixel 7** (ou hardware similar)
3. System Image: **API 34** com **Google Play** (x86_64)
4. Configuracao AVD:
   - RAM: 4096 MB (minimo)
   - Internal Storage: 4096 MB
   - SD Card: 512 MB
5. Finalizar e iniciar o emulador

### 6.3 Configurar Variaveis de Ambiente do SDK

**Windows:**
```cmd
setx ANDROID_HOME "%LOCALAPPDATA%\Android\Sdk"
setx PATH "%PATH%;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\emulator"
```

**macOS/Linux:**
```bash
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator
# Adicionar ao ~/.zshrc ou ~/.bashrc
```

Verificar:
```bash
adb devices
# Deve listar o emulador rodando
```

## Passo 7: Configurar iOS Simulator (macOS apenas)

1. Instalar Xcode 15+ via App Store
2. Abrir Xcode > Settings > Platforms > instalar **iOS 17** runtime
3. Aceitar licenca:
   ```bash
   sudo xcodebuild -license accept
   ```
4. Instalar CocoaPods:
   ```bash
   sudo gem install cocoapods
   ```
5. Instalar dependencias iOS:
   ```bash
   cd ios && pod install && cd ..
   ```

## Passo 8: Gerar Dev Client Build

O REURBCAD usa modulos nativos (WatermelonDB JSI, expo-camera, expo-location) que exigem um Dev Client customizado ao inves do Expo Go:

```bash
# Build local para Android
npx expo run:android

# Build local para iOS (macOS apenas)
npx expo run:ios
```

Ou via EAS Build para desenvolvimento:

```bash
eas build --profile development --platform android
# Instalar o APK gerado no emulador
```

## Passo 9: Iniciar Servidor de Desenvolvimento

```bash
npx expo start --dev-client
```

Opcoes disponiveis no terminal:
- `a` - Abrir no emulador Android
- `i` - Abrir no simulador iOS
- `r` - Reload do app
- `m` - Toggle menu
- `j` - Abrir debugger

## Passo 10: Verificar Funcionamento

### Checklist de Verificacao

| Item | Como Verificar | Esperado |
|------|---------------|----------|
| App abre | Tela de splash aparece | Logo REURBCAD visivel |
| Login funciona | Tocar "Entrar" | Abre browser com Keycloak login |
| Callback OAuth | Apos login no browser | Retorna ao app autenticado |
| Mapa carrega | Tela principal apos login | MapView renderiza |
| GPS funciona | Permissao concedida | Marker na posicao atual |
| WatermelonDB | Criar uma unidade | Dados salvos localmente |
| Sync funciona | Conectado com backend | Indicador "sincronizado" |

### Teste Rapido de Fluxo

1. Abrir app no emulador
2. Tocar "Entrar"
3. Login no Keycloak com usuario de teste (cadastrator@carf.dev / test123)
4. Conceder permissoes (localizacao, camera)
5. Baixar pacote de regiao (se primeira vez)
6. Visualizar mapa com poligonos
7. Tocar botao "+" para novo cadastro
8. Preencher formulario basico e salvar
9. Verificar que unidade aparece no mapa

## Troubleshooting por Sistema Operacional

### Windows

| Problema | Solucao |
|----------|---------|
| `ANDROID_HOME not found` | Adicionar `%LOCALAPPDATA%\Android\Sdk` ao PATH do sistema |
| Metro bundler lento | Excluir pasta do projeto do Windows Defender |
| `adb not found` | Instalar platform-tools separadamente: `sdkmanager "platform-tools"` |
| Porta 8081 em uso | `netstat -ano \| findstr :8081` e matar o processo |
| `npm install` falha com node-gyp | Instalar Build Tools: `npm install -g windows-build-tools` |

### macOS

| Problema | Solucao |
|----------|---------|
| `pod install` falha | `sudo gem install ffi -- --enable-system-libffi` |
| Xcode Command Line Tools | `xcode-select --install` |
| Simulador nao aparece | Xcode > Settings > Platforms > instalar iOS runtime |
| Permissao negada em scripts | `chmod +x node_modules/.bin/*` |
| CocoaPods cache corrompido | `pod cache clean --all && pod install` |

### Linux

| Problema | Solucao |
|----------|---------|
| KVM nao disponivel (emulador lento) | `sudo apt install qemu-kvm` e habilitar virtualizacao na BIOS |
| Watchman nao instalado | Instalar via package manager do distro |
| `inotify` limit | `echo fs.inotify.max_user_watches=524288 \| sudo tee -a /etc/sysctl.conf && sudo sysctl -p` |
| Java version errada | Instalar OpenJDK 17: `sudo apt install openjdk-17-jdk` |

## Referencias

- [Environment Variables](./05-environment-variables.md)
- [Build and Release](../DEPLOYMENT/01-build-and-release.md)
- [Keycloak Setup](./01-setup-keycloak.md)
- [Troubleshooting](./06-troubleshooting.md)
- [Navigation Structure](../ARCHITECTURE/03-navigation-structure.md)
