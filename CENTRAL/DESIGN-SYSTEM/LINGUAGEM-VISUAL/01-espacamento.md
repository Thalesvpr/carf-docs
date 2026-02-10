---
type: leaf
status: approved
updated: 2026-02-07
---

# Espacamento

Espaco nao e ausencia - e organizacao. O espacamento no CARF cria agrupamentos logicos, estabelece hierarquia e da respiro visual para que informacoes nao se atropelem.

Elementos relacionados ficam proximos. Um label e seu campo sao um grupo. Um titulo e seu conteudo sao um grupo. A proximidade comunica relacao sem necessidade de linhas ou caixas. Quando voce olha para a tela, os grupos devem ser obvios.

Elementos nao relacionados ficam distantes. Secoes diferentes tem espaco generoso entre si. Acoes primarias tem espaco ao redor para nao serem clicadas por acidente. O usuario nunca deveria confundir a qual grupo um elemento pertence.

## Respiro

Telas lotadas intimidam e confundem. Mesmo quando ha muita informacao para mostrar, o espacamento cria pausas visuais que permitem processar uma coisa de cada vez. Scroll e preferivel a densidade excessiva - o usuario pode rolar, mas nao pode desembaralhar uma tela apertada.

Em dispositivos moveis, espacamento generoso tambem significa alvos de toque seguros. Dedos sao imprecisos, especialmente sob estresse ou em movimento. Espaco entre elementos interativos previne toques acidentais.

## Escala de Tokens

A escala de espacamento usa base 4px, alinhada com Tailwind CSS defaults e as especificacoes do REURBCAD.

| Token | Valor | Tailwind | Uso |
|:------|:------|:---------|:----|
| space-1 | 4px | p-1 / gap-1 | Padding inline minimo, gap entre icone e texto |
| space-2 | 8px | p-2 / gap-2 | Gap entre elementos relacionados, padding de badges |
| space-3 | 12px | p-3 / gap-3 | Padding de componentes compactos, gap em listas densas |
| space-4 | 16px | p-4 / gap-4 | Padding padrao de cards e inputs, gap entre campos de form |
| space-6 | 24px | p-6 / gap-6 | Gap entre secoes dentro de um card, padding de dialogs |
| space-8 | 32px | p-8 / gap-8 | Margem entre blocos de conteudo, padding de paginas web |
| space-12 | 48px | p-12 / gap-12 | Espacamento entre secoes maiores, margem de pagina mobile |

Na pratica, use space-2 para micro-espacamento (dentro de componentes), space-4 como padrao (entre componentes), e space-8 para macro-espacamento (entre secoes). Em mobile, alvos de toque devem ter no minimo 44px de altura com space-2 entre eles.
