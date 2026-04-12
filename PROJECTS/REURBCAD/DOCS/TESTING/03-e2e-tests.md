---
type: leaf
status: review
updated: 2026-02-08
---

# Testes End-to-End - REURBCAD

Testes E2E do REURBCAD usando Maestro para validar fluxos completos do aplicativo mobile, incluindo login, coleta em campo, sincronizacao e cenarios offline.

## Escolha do Maestro

O Maestro foi escolhido como framework E2E por compatibilidade nativa com Expo, sintaxe declarativa YAML sem necessidade de compilar codigo de teste e suporte a gestos mobile (swipe, scroll, long press).

| Criterio | Maestro | Detox |
|----------|---------|-------|
| Setup com Expo | Simples (APK/IPA direto) | Requer eject ou custom dev client |
| Linguagem | YAML declarativo | JavaScript/TypeScript |
| Curva de aprendizado | Baixa | Media |
| Gestos mobile | Nativo (swipe, scroll, pinch) | Via matchers |
| CI Cloud | Maestro Cloud integrado | Requer device farm externo |
| Estabilidade | Retry automatico built-in | Requer configuracao de retry |
| Screenshots | Automatico em falhas | Manual via API |

## Setup do Maestro

### Instalacao

```bash
# macOS / Linux
curl -Ls "https://get.maestro.mobile.dev" | bash

# Windows via Chocolatey
choco install maestro

# Verificar instalacao
maestro --version
```

### Estrutura de Diretorios

```
apps/reurbcad/
  .maestro/
    config.yaml
    flows/
      login.yaml
      field-collection.yaml
      holder-management.yaml
      offline-sync.yaml
      team-navigation.yaml
    utils/
      login-helper.yaml
      create-unit-helper.yaml
    data/
      test-credentials.yaml
```

### Configuracao Base

```yaml
# .maestro/config.yaml
appId: br.gov.carf.reurbcad
name: REURBCAD E2E Tests
tags:
  - reurbcad
  - mobile
  - offline-first
```

## Fluxos Criticos

### Fluxo 1: Login Completo

```yaml
# .maestro/flows/login.yaml
appId: br.gov.carf.reurbcad
name: Login com Keycloak
tags:
  - auth
  - critical

---

# Tela inicial deve mostrar botao de login
- assertVisible: "Entrar com CARF ID"

# Pressionar botao de login (abre WebView Keycloak)
- tapOn: "Entrar com CARF ID"

# Aguardar WebView do Keycloak carregar
- waitForAnimationToEnd

# Preencher credenciais na tela Keycloak
- tapOn:
    id: "username"
- inputText: "cadastrator.test@carf.dev"

- tapOn:
    id: "password"
- inputText: "Test@2026!"

# Submeter formulario
- tapOn: "Entrar"

# Aguardar redirect e processamento do token
- waitForAnimationToEnd
- extendedWaitUntil:
    visible: "Selecionar Comunidade"
    timeout: 15000

# Validar que usuario esta autenticado
- assertVisible: "Bem-vindo"
- assertVisible: "cadastrator.test"
```

### Fluxo 2: Coleta em Campo Completa

```yaml
# .maestro/flows/field-collection.yaml
appId: br.gov.carf.reurbcad
name: Coleta em Campo - Cadastro de Unidade
tags:
  - field-collection
  - critical
dependencies:
  - flows/login.yaml

---

# Pre-requisito: estar logado e com comunidade selecionada
- runFlow: utils/login-helper.yaml

# Navegar para aba de unidades
- tapOn:
    id: "tab-units"

# Iniciar nova coleta
- tapOn: "Nova Unidade"

# Step 1: Informacoes Basicas
- assertVisible: "Informacoes Basicas"
- tapOn:
    id: "input-address"
- inputText: "Rua Teste E2E, 999"

- tapOn:
    id: "input-complement"
- inputText: "Casa 1"

- tapOn: "Proximo"

# Step 2: Geolocalizacao
- assertVisible: "Geolocalizacao"
- tapOn: "Capturar Localizacao GPS"
- waitForAnimationToEnd
- assertVisible:
    id: "gps-coordinates"

# Validar que coordenadas foram capturadas
- assertVisible: "S"  # Latitude Sul
- assertVisible: "O"  # Longitude Oeste

- tapOn: "Proximo"

# Step 3: Area e Dimensoes
- assertVisible: "Area"
- tapOn:
    id: "input-area"
- inputText: "250"

- tapOn: "Proximo"

# Step 4: Fotografias
- assertVisible: "Fotografias"
- tapOn: "Tirar Foto"
- waitForAnimationToEnd

# Simular captura de foto (Maestro lida com permissoes automaticamente)
- tapOn:
    id: "camera-capture-button"
- waitForAnimationToEnd

# Confirmar foto capturada
- tapOn: "Usar Foto"
- assertVisible: "1 foto adicionada"

- tapOn: "Proximo"

# Step 5: Revisao e Salvamento
- assertVisible: "Revisao"
- assertVisible: "Rua Teste E2E, 999"
- assertVisible: "250"

- tapOn: "Salvar Unidade"

# Validar salvamento
- waitForAnimationToEnd
- assertVisible: "Unidade salva com sucesso"

# Validar que aparece na lista
- assertVisible: "Rua Teste E2E, 999"
- assertVisible: "Rascunho"
```

### Fluxo 3: Sincronizacao Online

```yaml
# .maestro/flows/offline-sync.yaml
appId: br.gov.carf.reurbcad
name: Sincronizacao de Dados
tags:
  - sync
  - critical
dependencies:
  - flows/field-collection.yaml

---

- runFlow: utils/login-helper.yaml
- runFlow: utils/create-unit-helper.yaml

# Verificar indicador de changes pendentes
- assertVisible: "1 alteracao pendente"

# Navegar para tela de sync
- tapOn:
    id: "tab-sync"

# Iniciar sincronizacao manual
- tapOn: "Sincronizar Agora"

# Aguardar conclusao
- extendedWaitUntil:
    visible: "Sincronizacao concluida"
    timeout: 30000

# Validar que nao ha mais pendencias
- assertVisible: "Tudo sincronizado"
- assertNotVisible: "alteracao pendente"
```

## Simulacao Offline

### Teste de Operacao sem Conexao

```yaml
# .maestro/flows/offline-operation.yaml
appId: br.gov.carf.reurbcad
name: Operacao Offline
tags:
  - offline
  - critical

---

- runFlow: utils/login-helper.yaml

# Ativar modo aviao (Android)
- runScript:
    script: |
      adb shell settings put global airplane_mode_on 1
      adb shell am broadcast -a android.intent.action.AIRPLANE_MODE

# Aguardar deteccao de offline
- extendedWaitUntil:
    visible: "Voce esta offline"
    timeout: 5000

# Criar unidade offline
- tapOn:
    id: "tab-units"
- tapOn: "Nova Unidade"
- tapOn:
    id: "input-address"
- inputText: "Rua Offline, 001"
- tapOn: "Proximo"

# Capturar GPS (usa ultimo conhecido)
- tapOn: "Usar Ultima Localizacao"
- tapOn: "Proximo"

# Preencher area
- tapOn:
    id: "input-area"
- inputText: "180"
- tapOn: "Proximo"

# Pular foto (opcional offline)
- tapOn: "Proximo"

# Salvar
- tapOn: "Salvar Unidade"
- assertVisible: "Unidade salva localmente"

# Verificar badge de pendencia
- assertVisible: "1 alteracao pendente"

# Desativar modo aviao
- runScript:
    script: |
      adb shell settings put global airplane_mode_on 0
      adb shell am broadcast -a android.intent.action.AIRPLANE_MODE

# Aguardar reconexao e sync automatico
- extendedWaitUntil:
    visible: "Sincronizacao concluida"
    timeout: 60000

- assertVisible: "Tudo sincronizado"
```

## Screenshot Comparison

### Regressao Visual

```yaml
# .maestro/flows/visual-regression.yaml
appId: br.gov.carf.reurbcad
name: Regressao Visual - Telas Principais
tags:
  - visual
  - regression

---

- runFlow: utils/login-helper.yaml

# Capturar screenshots das telas principais
- tapOn:
    id: "tab-home"
- waitForAnimationToEnd
- takeScreenshot: home-screen

- tapOn:
    id: "tab-units"
- waitForAnimationToEnd
- takeScreenshot: units-list

- tapOn:
    id: "tab-sync"
- waitForAnimationToEnd
- takeScreenshot: sync-screen

- tapOn:
    id: "tab-profile"
- waitForAnimationToEnd
- takeScreenshot: profile-screen
```

Screenshots sao comparados automaticamente pelo Maestro Cloud entre execucoes, gerando diff visual quando houver divergencia acima do threshold configurado (default 0.1% de pixels diferentes).

## CI Setup para E2E

### GitHub Actions com Maestro Cloud

```yaml
name: REURBCAD E2E Nightly
on:
  schedule:
    - cron: '0 3 * * *'
  workflow_dispatch:

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - uses: actions/setup-java@v4
        with:
          java-version: 17
          distribution: temurin

      - run: yarn install --frozen-lockfile

      - name: Build APK de teste
        run: |
          cd apps/reurbcad
          npx expo prebuild --platform android --clean
          cd android
          ./gradlew assembleDebug

      - name: Upload para Maestro Cloud
        uses: mobile-dev-inc/action-maestro-cloud@v1
        with:
          api-key: ${{ secrets.MAESTRO_CLOUD_KEY }}
          app-file: apps/reurbcad/android/app/build/outputs/apk/debug/app-debug.apk
          workspace: apps/reurbcad/.maestro
          include-tags: critical
          env: |
            TEST_USER=cadastrator.test@carf.dev
            TEST_PASS=${{ secrets.E2E_TEST_PASSWORD }}
            API_URL=https://staging.api.carf.dev

  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - run: yarn install --frozen-lockfile

      - name: Build simulador iOS
        run: |
          cd apps/reurbcad
          npx expo prebuild --platform ios --clean
          cd ios
          xcodebuild -workspace ReurbCad.xcworkspace \
            -scheme ReurbCad \
            -sdk iphonesimulator \
            -configuration Debug \
            -derivedDataPath build

      - name: Upload para Maestro Cloud
        uses: mobile-dev-inc/action-maestro-cloud@v1
        with:
          api-key: ${{ secrets.MAESTRO_CLOUD_KEY }}
          app-file: apps/reurbcad/ios/build/Build/Products/Debug-iphonesimulator/ReurbCad.app
          workspace: apps/reurbcad/.maestro
          include-tags: critical
```

## Fluxos Criticos a Cobrir

| Fluxo | Prioridade | Tags | Tempo Estimado |
|-------|-----------|------|----------------|
| Login com Keycloak | P0 | `auth, critical` | 30s |
| Coleta completa (wizard 5 steps) | P0 | `field-collection, critical` | 90s |
| Sincronizacao manual | P0 | `sync, critical` | 45s |
| Operacao offline + reconexao | P0 | `offline, critical` | 120s |
| Gestao de titulares (CRUD) | P1 | `holders` | 60s |
| Navegacao entre comunidades | P1 | `navigation` | 30s |
| Captura de fotos com metadados GPS | P1 | `camera, geo` | 45s |
| Visualizacao de equipes | P2 | `teams` | 20s |
| Importacao de shapefile | P2 | `shapefile` | 60s |
| Logout e limpeza de sessao | P1 | `auth` | 15s |

### Tempo Total Estimado

- **P0 (critical):** ~285s (~5 min) - executados em todo PR
- **P0 + P1:** ~455s (~8 min) - executados diariamente
- **Todos:** ~515s (~9 min) - executados semanalmente

## Boas Praticas E2E

| Pratica | Descricao |
|---------|-----------|
| Dados isolados | Cada fluxo cria seus proprios dados, nao depende de estado pre-existente |
| Cleanup | Fluxos limpam dados criados ao final (ou usar tenant de teste isolado) |
| Timeouts generosos | Mobile e mais lento; usar `extendedWaitUntil` com timeout adequado |
| Tags para filtragem | Categorizar fluxos por area (`auth`, `sync`, `field-collection`) |
| Helper flows | Extrair acoes repetidas (login, criar unidade) em flows reutilizaveis |
| Evitar sleep fixo | Usar `waitForAnimationToEnd` e `extendedWaitUntil` em vez de delay fixo |
| Ambiente staging | E2E sempre contra ambiente staging, nunca producao |
| Credenciais seguras | Senhas via secrets do CI, nunca hardcoded nos YAML |

## Referencias

- [00-testing-strategy.md](./00-testing-strategy.md) - Estrategia geral
- [01-unit-tests.md](./01-unit-tests.md) - Testes unitarios
- [02-component-tests.md](./02-component-tests.md) - Testes de componentes
- [FEATURES/03-offline-sync.md](../FEATURES/03-offline-sync.md) - Funcionalidade de sync
- [CONCEPTS/01-authentication.md](../CONCEPTS/01-authentication.md) - Fluxo de login
