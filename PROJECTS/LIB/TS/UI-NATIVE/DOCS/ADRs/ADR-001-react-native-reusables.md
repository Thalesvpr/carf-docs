---
type: adr
status: approved
updated: 2026-01-24
---

# ADR-001: React Native Reusables com NativeWind

## Contexto

Biblioteca @carf/ui usa Radix UI e Tailwind CSS, tecnologias exclusivas de web. Aplicativo REURBCAD mobile reimplementava componentes sem padronizacao, duplicando esforco e criando inconsistencias visuais. Equipe precisava reutilizar conhecimento existente de Tailwind mantendo consistencia visual com versao web.

## Decisao

Criar @carf/ui-native baseada em react-native-reusables seguindo filosofia shadcn de copiar componentes para o projeto. Usar NativeWind para manter mesmas classes Tailwind do web. Usar rn-primitives como equivalente acessivel do Radix UI fornecendo primitivos como Dialog, Tooltip e Accordion com gerenciamento de foco e acessibilidade.

## Consequencias

Consistencia visual entre web e mobile atraves de classes Tailwind compartilhadas. Desenvolvedores reutilizam conhecimento existente sem reaprendizado. Componentes de dominio como StatusBadge e UnitCard compartilham tipos do tscore. Configuracao inicial requer setup de NativeWind no Expo com babel preset e tailwind.config.js.

## Alternativas Rejeitadas

Tamagui e gluestack-ui tem APIs diferentes do shadcn, exigindo reaprendizado de patterns de estilizacao. StyleSheet puro do React Native nao reutiliza classes Tailwind ja conhecidas pela equipe e causaria divergencia visual entre plataformas.
