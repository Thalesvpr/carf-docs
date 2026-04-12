---
type: leaf
status: review
updated: 2026-01-24
---

# Expo Setup

Configuracao completa de NativeWind em projeto Expo para usar @carf/ui-native.

## Instalando Dependencias

Instalar nativewind como dependencia principal do projeto. Instalar tailwindcss como dev dependency para processamento de classes. Instalar react-native-reanimated para animacoes de componentes. Verificar compatibilidade de versoes com Expo SDK.

## Inicializando Tailwind

Executar npx tailwindcss init para criar tailwind.config.js. Configurar content para incluir arquivos de componentes. Adicionar presets nativewind/preset. Estender theme com cores CARF conforme design system.

## Babel Config

Editar babel.config.js adicionando preset nativewind/babel. Manter babel-preset-expo como primeiro preset. Ordem de presets importa para transformacao correta. Reiniciar bundler apos alterar babel config.

## Metro Config

Criar ou editar metro.config.js para processar CSS. Importar withNativeWind de nativewind/metro. Envolver config existente com withNativeWind. Especificar caminho para global.css.

## Global CSS

Criar arquivo global.css na raiz do projeto. Adicionar diretivas @tailwind base, components e utilities. Importar global.css no entry point App.tsx. Verificar que nativewind processa arquivo corretamente.

## Verificacao

Criar componente teste com classes Tailwind como bg-red-500. Verificar que estilo aplica em iOS e Android. Testar dark: prefix para dark mode. Confirmar que hot reload atualiza estilos.

## Troubleshooting

Se estilos nao aplicam, limpar cache com expo start -c. Verificar ordem de presets em babel.config.js. Confirmar que content em tailwind.config.js inclui arquivos corretos. Checar console para erros de transformacao.
