---
type: leaf
status: review
updated: 2026-01-24
---

# Configuracao NativeWind

Setup necessario para usar NativeWind em projetos Expo com @carf/ui-native.

## Dependencias

Instalar nativewind como dependencia principal e tailwindcss como dev dependency. Instalar expo-constants e react-native-reanimated para animacoes. Instalar rn-primitives para primitivos acessiveis usados por componentes complexos.

## Babel Config

Arquivo babel.config.js deve incluir preset nativewind/babel. Este preset transforma classes Tailwind em chamadas StyleSheet. Ordem de presets importa, nativewind deve vir apos babel-preset-expo.

## Tailwind Config

Arquivo tailwind.config.js na raiz do projeto define content apontando para arquivos de componentes. Estender tema com cores CARF, spacing customizado e breakpoints para diferentes tamanhos de tela mobile. Importar preset de nativewind para tipos.

## Global CSS

Arquivo global.css importa diretivas @tailwind base, components e utilities. Configurar metro.config.js para processar CSS via withNativeWind. Importar global.css no entry point do app.

## Verificacao

Apos configuracao, classes Tailwind devem funcionar em componentes React Native. Verificar que dark mode alterna corretamente. Testar em iOS e Android para garantir consistencia de estilizacao.
