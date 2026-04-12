---
type: leaf
status: review
updated: 2026-01-24
---

# Integracao

Como consumir biblioteca @carf/ui-native em aplicativos Expo existentes.

## Copiando Componentes

Seguindo filosofia shadcn, componentes sao copiados para diretorio do projeto. Diretorio components/ui recebe primitivos como Button e Input. Diretorio components/domain recebe StatusBadge, UnitCard e HolderCard. Atualizacoes requerem copia manual de novos arquivos.

## Configurando Tema

Arquivo tailwind.config.js estende tema base com cores do CARF. Definir primary, secondary, destructive, muted, accent e background. Dark mode usa prefixo dark: em classes. ThemeProvider opcional gerencia preferencia do usuario.

## Usando Primitivos

Importar componentes de diretorio local. Button aceita variant como default, outline, ghost ou destructive. Input integra com react-hook-form via ref forwarding. Dialog usa rn-primitives para overlay e animacao.

## Usando Componentes de Dominio

StatusBadge recebe status do tipo UnitStatus de @carf/tscore e renderiza badge colorido. UnitCard recebe objeto Unit e exibe resumo com codigo, endereco e status. HolderCard recebe Holder e exibe nome, CPF formatado e contato.

## Testando Integracao

Verificar que componentes renderizam corretamente em iOS e Android. Testar dark mode alternando tema. Validar acessibilidade com VoiceOver e TalkBack. Confirmar que tipos TypeScript inferem props corretamente.
