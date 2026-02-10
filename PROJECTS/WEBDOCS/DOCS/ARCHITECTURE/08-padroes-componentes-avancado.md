---
type: leaf
status: review
updated: 2026-02-07
---

# Padroes de Componentes - Avancado

Diretivas de hidratacao, uso de React via @carf/ui, e requisitos de acessibilidade. Documento complementar a 08-padroes-componentes.md.

## Diretivas de Hidratacao

Componentes Astro sao estaticos por padrao. Para interatividade client-side, usar diretivas com componentes React.

| Diretiva | Quando usar | Impacto no bundle |
|----------|-------------|-------------------|
| nenhuma | Maioria dos componentes Astro | Zero JavaScript |
| client:load | EVITAR, raramente necessario | JS com a pagina |
| client:idle | PREFERIR para interatividade nao-critica | JS apos interacao |
| client:visible | Componentes abaixo do fold ou pesados | JS sob demanda |
| client:only | Libs que nao suportam SSR | Sem SSR, JS obrigatorio |

## Uso de Componentes React (@carf/ui)

Componentes React da biblioteca @carf/ui sao importados e usados com diretivas de hidratacao. Sempre usar diretiva, preferir client:idle ou client:visible. Passar props como atributos e handlers como funcoes inline ou importadas.

## Componentes Astro vs React

Usar Astro para conteudo estatico, layout e estrutura, wrapper de componentes React, e qualquer coisa sem interatividade. Usar React para interatividade complexa (drag-drop), estado client-side, componentes @carf/ui, e integracoes com libs React.

## Acessibilidade

Usar elementos semanticos (button, nav, main). Adicionar aria-label quando necessario. Garantir ordem de foco logica. Todos elementos interativos acessiveis via teclado. Seguir WCAG 2.1 AA com contraste 4.5:1 para texto.
