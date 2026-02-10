---
type: leaf
status: review
updated: 2026-02-07
---

# Wizard

Componente stepper multi-step para formularios complexos com validacao por etapa.

## Props

Prop steps array de objetos com label, content e isValid opcional definindo cada etapa. Prop activeStep indice da etapa ativa atualmente. Prop onStepChange callback invocado com novo indice ao navegar entre etapas. Prop onComplete callback invocado ao confirmar ultima etapa do wizard. Prop allowBack boolean controla se navegacao para etapas anteriores e permitida.

## Progress Bar

Barra de progresso horizontal exibe indicadores circulares para cada etapa. Etapa completa exibe check icon com bg-primary indicando conclusao. Etapa ativa exibe numero com ring primaria indicando posicao atual. Etapa futura exibe numero com estilo mutado indicando pendencia. Linhas conectam indicadores mostrando fluxo sequencial.

## Navegacao

Botao proximo avanca para etapa seguinte quando isValid da etapa atual retorna true. Botao anterior retorna para etapa precedente quando allowBack habilitado. Botao concluir substitui proximo na ultima etapa invocando onComplete. Validacao por step impede avanco quando dados incompletos.

## Conteudo

Content de cada step renderiza como children no painel principal abaixo da progress bar. Apenas conteudo da etapa ativa renderiza para performance. Transicao entre etapas usa animacao de fade para suavidade. Scroll automatico para topo ao mudar de etapa.

## Acessibilidade

Progress bar recebe role progressbar com aria-valuenow e aria-valuemax. Cada step indicator recebe aria-label com nome e status da etapa. Botoes de navegacao recebem labels descritivos da acao. Foco move para conteudo da etapa ao navegar.

## Estilizacao

Progress bar usa flex horizontal com items-center e gap entre indicadores. Indicadores usam rounded-full com w-8 h-8 para formato circular. Linhas conectoras usam h-0.5 bg-border entre indicadores. Conteudo usa p-6 com max-w para legibilidade.
