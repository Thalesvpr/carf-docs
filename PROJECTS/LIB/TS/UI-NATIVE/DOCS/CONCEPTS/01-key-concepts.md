---
type: leaf
status: review
updated: 2026-01-24
---

# Conceitos-Chave

Principios de design fundamentais da biblioteca @carf/ui-native.

## Filosofia Shadcn

Biblioteca segue abordagem shadcn onde componentes sao copiados para projeto ao inves de instalados como dependencia NPM. Desenvolvedores tem controle total sobre codigo fonte. Atualizacoes sao explícitas via copia manual. Customizacoes nao requerem overrides complexos.

## Componentes Primitivos

Elementos genericos reutilizaveis em qualquer contexto. Button fornece variantes visuais e estados de loading. Input integra com formularios via ref forwarding. Dialog implementa overlay modal com animacao. Checkbox e Switch gerenciam estado booleano. Primitivos nao conhecem dominio CARF.

## Componentes de Dominio

Elementos especificos do ecossistema CARF. StatusBadge renderiza status de unidade com cor semantica. UnitCard exibe resumo de unidade habitacional. HolderCard mostra dados de titular com CPF formatado. Componentes recebem tipos de @carf/tscore garantindo consistencia.

## NativeWind

Compilador que transforma classes Tailwind em StyleSheet nativo. Mesmas classes usadas em @carf/ui web funcionam em mobile. Dark mode via prefixo dark: em classes. Responsive design via prefixos sm:, md:, lg:. Desenvolvedores reutilizam conhecimento existente.

## Rn-Primitives

Equivalente mobile do Radix UI. Fornece primitivos acessiveis com gerenciamento de foco. Dialog, Accordion, Tooltip e DropdownMenu incluem semantica correta para leitores de tela. Componentes @carf/ui-native estendem primitivos adicionando estilizacao Tailwind.
