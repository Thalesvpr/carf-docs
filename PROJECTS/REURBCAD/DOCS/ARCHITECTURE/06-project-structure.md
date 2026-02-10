---
type: leaf
status: review
updated: 2026-02-08
---

# Estrutura do Projeto

Organizacao completa de diretorios, convencoes de nomenclatura, ordem de imports e descricao dos arquivos-chave do projeto REURBCAD.

## Arvore de Diretorios

```
reurbcad/
  app/                           # Expo Router - paginas e layouts
    _layout.tsx                  # RootLayout: providers globais, AuthGuard
    index.tsx                    # SplashScreen: redirect inicial
    (auth)/
      _layout.tsx                # Layout sem tabs/header
      login.tsx                  # Tela de login
    (tabs)/
      _layout.tsx                # TabsLayout: bottom navigation role-aware
      mapa/
        _layout.tsx              # Stack do mapa
        index.tsx                # Tela principal do mapa
        [unitId].tsx             # Detalhe da unidade
        nova-unidade.tsx         # Formulario nova unidade
      unidades/
        _layout.tsx
        index.tsx                # Listagem de unidades
        [unitId]/
          index.tsx
          editar.tsx
          titular/
            novo.tsx             # Novo titular
            [holderId].tsx       # Editar titular
      equipe/
        _layout.tsx
        index.tsx                # Lista de equipes
        [teamId].tsx             # Detalhe da equipe
      sync/
        _layout.tsx
        index.tsx                # Status de sincronizacao
        conflitos.tsx            # Conflitos pendentes
      perfil/
        _layout.tsx
        index.tsx                # Configuracoes
        sobre.tsx                # Sobre o app
    (modals)/
      assinatura.tsx             # Canvas de assinatura (landscape)
      foto-viewer.tsx            # Viewer de fotos
      conflito-dialog.tsx        # Resolucao de conflitos
      permissoes.tsx             # Permissoes do sistema
      preparar-regiao.tsx        # Download pacote de campo
      ocr/
        selecao.tsx
        instrucao.tsx
        camera.tsx
        revisao.tsx
        processamento.tsx
        resultado.tsx
        confirmacao.tsx
  src/
    components/                  # Componentes reutilizaveis
      ui/                        # Componentes primitivos (copiados de @carf/ui-native)
        Button.tsx
        Input.tsx
        Select.tsx
        Checkbox.tsx
        Switch.tsx
        Textarea.tsx
        Card.tsx
        Tabs.tsx
        BottomSheet.tsx
        Alert.tsx
        Toast.tsx
        Dialog.tsx
        Progress.tsx
        OfflineIndicator.tsx
      domain/                    # Componentes de dominio
        UnitCard.tsx
        HolderCard.tsx
        StatusBadge.tsx
        CommunityCard.tsx
        MapComponent.tsx
        SignatureCanvas.tsx
        CameraOverlay.tsx
        SyncStatusIndicator.tsx
      form/                      # Componentes de formulario
        FormStep1BasicInfo.tsx
        FormStep2Address.tsx
        FormStep3Area.tsx
        FormStep4Geolocation.tsx
        FormStep5Photos.tsx
        FormErrorMessage.tsx
        MaskedInput.tsx
        SearchableSelect.tsx
      errors/                    # Error Boundaries
        AppErrorBoundary.tsx
        ScreenErrorBoundary.tsx
        FormErrorBoundary.tsx
      layout/                    # Layout wrappers
        SafeScreen.tsx
        KeyboardAvoidingWrapper.tsx
        ScrollContainer.tsx
    database/                    # WatermelonDB
      index.ts                   # Instancia do database e adapter
      schema.ts                  # Schema definition (tabelas e colunas)
      migrations.ts              # Migration steps incrementais
      models/
        Unit.ts                  # Model Unit extending Model
        Holder.ts                # Model Holder
        UnitHolder.ts            # Model juncao unit_holders
        Document.ts              # Model Document (fotos e docs)
        Community.ts             # Model Community (readonly)
        Team.ts                  # Model Team (readonly)
        TeamMember.ts            # Model TeamMember (readonly)
        SyncQueue.ts             # Model SyncQueue
        SyncMetadata.ts          # Model SyncMetadata (singleton)
    services/                    # Servicos de negocio
      AuthService.ts             # Singleton OAuth2 PKCE
      SyncManager.ts             # Orquestrador de sincronizacao
      StorageService.ts          # Gerenciamento de arquivos (fotos, docs)
      LocationService.ts         # GPS e geofencing
      OcrService.ts              # OCR on-device
      NotificationService.ts     # Push notifications e toasts
    stores/                      # Zustand stores
      useAuthStore.ts
      useSyncStore.ts
      useMapStore.ts
      useFormStore.ts
    hooks/                       # Custom hooks
      useAuth.ts                 # Wrapper do useAuthStore com acoes
      useSync.ts                 # Controle de sincronizacao
      useLocation.ts             # GPS position tracking
      useForm.ts                 # Wrapper React Hook Form + Zod
      useUnit.ts                 # WatermelonDB observe unit
      useHolder.ts               # WatermelonDB observe holder
      useNetworkStatus.ts        # NetInfo wrapper
      useCameraPermission.ts     # Permissao de camera
      useDebounce.ts             # Debounce generico
      useKeyboard.ts             # Keyboard visibility e height
    utils/                       # Utilitarios puros
      validators.ts              # Validacoes CPF, CNPJ, CEP
      formatters.ts              # Formatacao de CPF, data, telefone, moeda
      date.ts                    # Helpers de data (parse, format, diff)
      crypto.ts                  # Criptografia AES-256 para assinaturas
      geojson.ts                 # Parsing e manipulacao GeoJSON
      retry.ts                   # retryWithBackoff utility
      mmkv-storage.ts            # Adapter MMKV para Zustand persist
      logger.ts                  # Logger estruturado com Sentry
    constants/                   # Constantes imutaveis
      colors.ts                  # Design tokens de cor
      spacing.ts                 # Escala de espacamento (4, 8, 12, 16, 24, 32, 48)
      typography.ts              # Fontes, tamanhos, line-heights
      api.ts                     # Base URLs e endpoints
      errors.ts                  # Codigos e mensagens de erro
      attendance-status.ts       # Enum e cores por status
      regex.ts                   # Patterns de validacao (CPF, CEP, email)
    types/                       # Tipos TypeScript
      index.ts                   # Re-export de @carf/tscore types
      navigation.ts              # Tipos de rotas e params
      forms.ts                   # Tipos de schemas de formulario
      sync.ts                    # Tipos de payload de sync
  assets/                        # Assets estaticos
    fonts/
      Inter-Regular.ttf
      Inter-Medium.ttf
      Inter-SemiBold.ttf
      Inter-Bold.ttf
    images/
      logo.png
      splash.png
      icon.png
    tiles/                       # Cache de map tiles pre-baixados
  app.json                       # Configuracao Expo
  app.config.js                  # Config dinamica (env vars)
  eas.json                       # Profiles de build EAS
  tsconfig.json                  # TypeScript config
  babel.config.js                # Babel config (reanimated plugin)
  metro.config.js                # Metro bundler config
  .env.development               # Variaveis de ambiente dev
  .env.staging                   # Variaveis de ambiente staging
  .env.production                # Variaveis de ambiente producao
```

## Proposito de Cada Diretorio

| Diretorio | Proposito | Regras |
|-----------|-----------|--------|
| `app/` | Rotas e layouts do Expo Router | Apenas logica de roteamento e composicao de componentes. Sem logica de negocio. |
| `src/components/ui/` | Componentes primitivos de UI | Copiados de `@carf/ui-native`. Sem logica de dominio. Apenas props de apresentacao. |
| `src/components/domain/` | Componentes de dominio | Conhecem tipos do `@carf/tscore`. Podem acessar stores e hooks. |
| `src/components/form/` | Steps do wizard de formulario | Usam React Hook Form + Zod. Um componente por step. |
| `src/components/errors/` | Error Boundaries | Componentes de classe React para captura de erros. |
| `src/database/` | WatermelonDB completo | Schema, migrations, models. Fonte de verdade para dados locais. |
| `src/database/models/` | Classes de Model WatermelonDB | Extending `Model` com decorators `@field`, `@relation`, `@date`. |
| `src/services/` | Servicos singleton | Classes com logica de negocio complexa. AuthService, SyncManager, etc. |
| `src/stores/` | Zustand stores | Uma store por dominio. Sem efeitos colaterais diretos (delegam para services). |
| `src/hooks/` | Custom React hooks | Wrappers de stores, WatermelonDB observables, permissoes, GPS. |
| `src/utils/` | Funcoes puras utilitarias | Sem dependencia de React ou estado. Testavel unitariamente. |
| `src/constants/` | Constantes imutaveis | Design tokens, URLs, codigos de erro. Exportam objetos `as const`. |
| `src/types/` | Tipos TypeScript | Re-exports de `@carf/tscore` e tipos locais do app. |
| `assets/` | Assets estaticos | Fontes, imagens, icones. Referenciados via `require()` ou `expo-asset`. |

## Convencoes de Nomenclatura

| Tipo | Convencao | Exemplo |
|------|-----------|---------|
| Componentes React | PascalCase | `UnitCard.tsx`, `FormStep1BasicInfo.tsx` |
| Custom hooks | camelCase com prefixo `use` | `useAuth.ts`, `useNetworkStatus.ts` |
| Servicos | PascalCase com sufixo `Service` ou `Manager` | `AuthService.ts`, `SyncManager.ts` |
| Zustand stores | camelCase com prefixo `use` e sufixo `Store` | `useAuthStore.ts`, `useMapStore.ts` |
| Utilitarios | camelCase | `validators.ts`, `formatters.ts` |
| Constantes | camelCase (arquivo), UPPER_SNAKE_CASE (valores) | `colors.ts` com `PRIMARY_BLUE` |
| WatermelonDB models | PascalCase singular | `Unit.ts`, `Holder.ts` |
| Tipos TypeScript | PascalCase para interfaces/types | `FormDraft`, `SyncConflict` |
| Arquivos de rota Expo | kebab-case | `nova-unidade.tsx`, `foto-viewer.tsx` |
| Parametros dinamicos | camelCase entre colchetes | `[unitId].tsx`, `[holderId].tsx` |

## Ordem de Imports

Todos os arquivos seguem a mesma ordem de imports, separados por linha em branco:

```typescript
// 1. Modulos do React e React Native
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Pressable } from 'react-native';

// 2. Bibliotecas externas
import { useQuery } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

// 3. Bibliotecas internas (@carf/*)
import { Unit, UnitStatus } from '@carf/tscore';
import { geoApiClient } from '@carf/geoapi-client';

// 4. Servicos e stores
import { AuthService } from '@/services/AuthService';
import { useAuthStore } from '@/stores/useAuthStore';

// 5. Hooks customizados
import { useUnit } from '@/hooks/useUnit';
import { useNetworkStatus } from '@/hooks/useNetworkStatus';

// 6. Componentes internos
import { Button } from '@/components/ui/Button';
import { UnitCard } from '@/components/domain/UnitCard';

// 7. Utilitarios e constantes
import { formatCpf } from '@/utils/formatters';
import { COLORS } from '@/constants/colors';

// 8. Tipos (se type-only import)
import type { FormDraft } from '@/types/forms';
```

## Tabela de Arquivos-Chave

| Arquivo | Proposito | Dependencias Principais |
|---------|-----------|------------------------|
| `app/_layout.tsx` | Provider tree, AuthGuard, routing raiz | Zustand stores, WatermelonDB, QueryClient |
| `src/database/index.ts` | Cria instancia do Database com adapter SQLite JSI | schema, migrations |
| `src/database/schema.ts` | Define todas as tabelas e colunas | Nenhuma (declarativo) |
| `src/services/AuthService.ts` | Singleton OAuth2 PKCE login/logout/refresh | expo-secure-store, expo-auth-session |
| `src/services/SyncManager.ts` | Orquestra pull/push/conflict resolution | WatermelonDB, geoapi-client, AuthService |
| `src/stores/useAuthStore.ts` | Estado de autenticacao global | AuthService, MMKV |
| `src/stores/useSyncStore.ts` | Estado de sync e conflitos | WatermelonDB sync_queue |
| `src/hooks/useLocation.ts` | GPS tracking com Expo Location | expo-location |
| `src/utils/validators.ts` | Validacao CPF Mod11, CNPJ | @carf/tscore/validations |
| `app.config.js` | Config dinamica lendo EXPO_PUBLIC_* | dotenv |
| `eas.json` | Build profiles (dev, preview, production) | Nenhuma |

## Alias de Path

O `tsconfig.json` configura aliases para evitar imports relativos longos:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/components/*": ["src/components/*"],
      "@/database/*": ["src/database/*"],
      "@/services/*": ["src/services/*"],
      "@/stores/*": ["src/stores/*"],
      "@/hooks/*": ["src/hooks/*"],
      "@/utils/*": ["src/utils/*"],
      "@/constants/*": ["src/constants/*"],
      "@/types/*": ["src/types/*"]
    }
  }
}
```

## Referencias

- [Navigation Structure](./03-navigation-structure.md)
- [State Management](./04-state-management.md)
- [WatermelonDB Schema](../DATA/01-watermelondb-schema.md)
- [Lib Integration](./02-lib-integration.md)
- [Build and Release](../DEPLOYMENT/01-build-and-release.md)
