---
type: leaf
status: done
updated: 2026-02-16
---

# ADB via WiFi — Desenvolvimento sem Cabo USB

Guia para rodar o REURBCAD em device fisico sem cabo USB, usando ADB over WiFi.

## Por que usar?

- Cabo USB desconecta e atrapalha o fluxo de desenvolvimento
- Permite testar em device fisico com mais liberdade de movimento
- Funciona com dev build (sem Expo Go)

## Pre-requisitos

| Requisito | Detalhe |
|-----------|---------|
| Android SDK | `platform-tools` instalado (vem com Android Studio) |
| Device Android | Depuracao USB ativada em Opcoes do Desenvolvedor |
| Mesma rede WiFi | PC e celular devem estar na mesma sub-rede |
| Cabo USB | Apenas na primeira vez, para autorizar |

## Uso Rapido (script automatizado)

O projeto inclui um script helper que cuida de tudo:

```bash
# Conectar (primeira vez: com cabo USB plugado)
npm run adb-wifi

# Ver status da conexao
npm run adb-wifi -- --status

# Desconectar
npm run adb-wifi -- --disconnect
```

### Primeira vez

1. Conecte o device via USB
2. Rode `npm run adb-wifi`
3. Aceite o popup "Permitir depuracao USB?" no celular (marque "Sempre permitir")
4. Desplugue o cabo — pronto!

### Reconectando (sem cabo)

Se a conexao cair (celular dormiu, trocou de rede, etc.), basta rodar:

```bash
npm run adb-wifi
```

O script detecta se ja existe conexao WiFi ativa e evita duplicacao.

## Setup Manual (sem o script)

### 1. Encontrar o adb

```bash
# Windows (caminho padrao)
%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe

# macOS / Linux
~/Library/Android/sdk/platform-tools/adb
$ANDROID_HOME/platform-tools/adb
```

### 2. Com cabo USB (primeira vez)

```bash
# Verificar que o device aparece
adb devices

# Ativar modo TCP na porta 5555
adb tcpip 5555

# Pegar o IP do celular
adb shell ip addr show wlan0 | grep "inet "
# Ex: inet 192.168.1.94/24 ...

# Conectar via WiFi
adb connect 192.168.1.94:5555

# Verificar
adb devices
# Deve mostrar: 192.168.1.94:5555  device

# Pode tirar o cabo!
```

### 3. Sem cabo (Android 11+, Wireless Debugging)

Para celulares com Android 11 ou superior, nao precisa de cabo nenhum:

1. Configuracoes > Opcoes do Desenvolvedor > **Depuracao sem fio** > Ativar
2. Toque em **Parear dispositivo com codigo**
3. No terminal:
   ```bash
   adb pair 192.168.1.94:PORTA_PAREAMENTO
   # Digite o codigo de 6 digitos que apareceu no celular
   ```
4. Conecte no endereco principal (porta diferente da de pareamento):
   ```bash
   adb connect 192.168.1.94:PORTA_PRINCIPAL
   ```

## Troubleshooting

### Sub-redes diferentes (PC e celular em redes distintas)

**Sintoma**: `adb connect` falha com timeout ou connection refused.

**Causa comum**: Mesh WiFi com mesmo SSID mas o celular conectou no modem do provedor (192.168.0.x) em vez do mesh (192.168.1.x).

**Solucao**:
1. Verifique os IPs:
   - PC: `ipconfig` (Windows) ou `ip addr` (Linux/Mac)
   - Celular: Configuracoes > WiFi > detalhes da rede
2. Se estiverem em sub-redes diferentes (ex: 192.168.0.x vs 192.168.1.x):
   - Desligue e religue o WiFi do celular (pode reconectar no roteador correto)
   - Ou via adb (com cabo): `adb shell cmd connectivity airplane-mode enable` / `disable`
   - Ou desative o WiFi do modem do provedor (solucao definitiva)

### "failed to authenticate"

O celular precisa autorizar o PC. Deve aparecer um popup na tela do device — aceite e marque "Sempre permitir".

### Conexao cai ao dormir

O modo `adb tcpip` nao sobrevive a reinicializacao do device. Depois de reiniciar:
- Se tiver cabo: rode `npm run adb-wifi` de novo
- Se nao tiver: use Wireless Debugging (Android 11+) que nao precisa de cabo

### Expo nao encontra o device

Depois de conectar via WiFi, o Expo deve detectar automaticamente. Se nao detectar:

```bash
# Verificar que adb ve o device
adb devices

# Rodar o app diretamente
npx expo run:android
```

## Integracao com dev-start.js

O `npm run dev` (que roda `dev-start.js`) faz `adb reverse` automaticamente para o device USB. Com WiFi, o dev server ja e acessivel pela rede — entao `npm run dev` funciona normalmente desde que o device esteja conectado via `adb-wifi`.

Fluxo recomendado:
```bash
npm run adb-wifi     # conecta device sem fio
npm run dev          # inicia Expo + Keycloak
```
