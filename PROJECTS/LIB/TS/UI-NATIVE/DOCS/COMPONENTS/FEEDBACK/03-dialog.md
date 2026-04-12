---
type: leaf
status: review
updated: 2026-01-24
---

# Dialog

Componente modal sobreposto para confirmacoes, formularios e conteudo complexo.

## Props

Prop open controla visibilidade em modo controlado. Prop onOpenChange recebe callback com novo estado. Prop title exibe cabecalho do dialog. Prop description exibe texto secundario abaixo do titulo.

## Estrutura

Dialog.Trigger envolve elemento que abre dialog ao pressionar. Dialog.Portal renderiza conteudo em portal separado. Dialog.Overlay exibe fundo escurecido. Dialog.Content contem titulo, descricao e children.

## Gerenciamento de Foco

Foco move para primeiro elemento focavel ao abrir. Tab navega entre elementos dentro do dialog. Focus trap impede foco sair para conteudo atras. Foco retorna para trigger ao fechar.

## Fechamento

Pressionar overlay fecha dialog por padrao. Prop closeOnOverlayPress false desabilita comportamento. Botao X no canto fornece fechamento explicito. Tecla Escape fecha em plataformas com teclado.

## Acessibilidade

Usa rn-primitives Dialog para semantica completa. AccessibilityRole dialog aplicado automaticamente. Title e description vinculados via aria-labelledby e aria-describedby. Overlay anuncia modal para leitores de tela.

## Animacao

Overlay fade in com duracao configuravel. Content scale e fade simultaneamente. Animacoes respeitam prefers-reduced-motion. Exit animation reverte entrada suavemente.
