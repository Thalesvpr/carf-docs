---
type: leaf
status: review
updated: 2026-01-24
---

# Getting Started

Como comecar a usar componentes @carf/ui-native em projeto Expo existente.

## Pre-requisitos

Projeto Expo SDK 50 ou superior com TypeScript configurado. React Native 0.73 ou superior. NativeWind configurado conforme guia expo-setup. Dependencia @carf/tscore instalada para componentes de dominio.

## Estrutura de Diretorios

Criar diretorio components/ui na raiz do projeto para primitivos. Criar diretorio components/domain para componentes CARF. Manter estrutura plana sem subdiretorios excessivos. Um arquivo por componente seguindo convencao do React Native.

## Copiando Componentes

Copiar arquivos de componentes desejados para diretorio local. Button.tsx vai para components/ui/Button.tsx. StatusBadge.tsx vai para components/domain/StatusBadge.tsx. Ajustar imports relativos conforme estrutura local.

## Instalando Dependencias

Componentes usam rn-primitives para primitivos acessiveis. Instalar pacotes conforme componentes copiados. Dialog requer @rn-primitives/dialog. Checkbox requer @rn-primitives/checkbox. Instalar react-native-reanimated para animacoes.

## Primeiro Componente

Importar Button de components/ui/Button. Usar em tela existente com props variant e onPress. Verificar que estilos NativeWind aplicam corretamente. Testar em iOS e Android para consistencia.

## Proximos Passos

Copiar componentes adicionais conforme necessidade. Configurar tema customizado em tailwind.config.js. Adicionar componentes de dominio apos instalar @carf/tscore. Consultar documentacao de cada componente para props e variantes.
