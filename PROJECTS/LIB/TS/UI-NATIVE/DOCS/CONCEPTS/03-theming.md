---
type: leaf
status: review
updated: 2026-01-24
---

# Theming

Sistema de temas customizaveis da biblioteca @carf/ui-native.

## Variaveis de Tema

Tailwind config define cores via variaveis CSS customizadas. Primary, secondary, destructive, muted, accent e background sao cores principais. Cada cor tem variante foreground para texto sobre fundo. Variaveis sao referencias em classes como bg-primary e text-primary-foreground.

## Dark Mode

NativeWind suporta dark mode via prefixo dark: em classes. Classe dark:bg-background aplica cor diferente em modo escuro. Sistema detecta preferencia via useColorScheme hook. ThemeProvider opcional permite override manual pelo usuario.

## Customizacao por Tenant

Tenants podem definir cores proprias via tailwind.config.js. Override de variaveis CSS customiza aparencia sem modificar componentes. Cores institucionais de prefeituras aplicam-se automaticamente. Schema de cores valida contraste minimo.

## Persistencia

AsyncStorage persiste preferencia de tema do usuario. Valor null usa preferencia do sistema. Valor light ou dark forca modo especifico. App inicializa com ultimo valor persistido antes de renderizar.

## Componentes de Tema

ThemeProvider envolve app fornecendo contexto de tema. useTheme hook retorna tema atual e funcao toggle. ThemeToggle componente renderiza switch para alternar modos. Componentes reagem automaticamente a mudancas de tema.

## Migracao de Cores

Ao atualizar cores do design system, alterar tailwind.config.js. Todas instancias de classes afetadas atualizam automaticamente. Verificar contraste apos mudancas. Testar em ambos modos claro e escuro.
