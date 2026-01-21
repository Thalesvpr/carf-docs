---
status: review
updated: 2026-01-21
---

# Template de Guia

Template para páginas da seção /guia/ que explicam como usar a documentação e conceitos do sistema CARF.

Frontmatter obrigatório define title com nome descritivo da página, description com resumo de 1-2 linhas para SEO, section com valor guia, e audience com valor user indicando conteúdo público. Campo sidebar opcional define label e order para navegação.

Introdução no primeiro parágrafo contextualiza o conteúdo explicando o que leitor aprenderá e por que é relevante. Máximo de 3-4 linhas focando no benefício para o leitor, não na estrutura do documento.

Corpo divide conteúdo em seções com headings h2 para tópicos principais e h3 para subtópicos. Cada seção aborda um aspecto do tema com explicação clara e exemplos quando aplicável. Callouts destacam informações importantes.

Conclusão sugere próximos passos com links para páginas relacionadas em seção "Ver também" ou "Próximos passos". Links para aprofundamento do tema ou páginas complementares.

Exemplo de frontmatter completo para página de guia sobre navegação: title como Navegando pela Documentação, description como Aprenda a usar a busca sidebar e atalhos de teclado para encontrar informações rapidamente, section como guia, audience como user, sidebar com label Navegação e order 2.

## Template Copy-Paste

```mdx
---
title: "Título do Guia"
source: "CENTRAL/WORKFLOWS/nome-do-workflow.md"
sidebar:
  order: 1
  label: "Label Curto"
draft: false
---

import { Aside, Steps, Card, CardGrid, Tabs, TabItem } from '@astrojs/starlight/components';

# Título do Guia

Introdução contextualiza o conteúdo explicando o que o leitor aprenderá e por que é relevante.
Máximo de 3-4 linhas focando no benefício para o leitor.

## Conceito Principal

Explicação clara do conceito principal com exemplos quando aplicável.

<Aside type="note">
  Informação adicional que ajuda a entender melhor o conceito.
</Aside>

### Subtópico 1

Detalhamento do primeiro aspecto do tema.

### Subtópico 2

Detalhamento do segundo aspecto do tema.

<Aside type="tip">
  Dica prática para aplicar o conhecimento.
</Aside>

## Aplicação Prática

Como aplicar o conceito no dia-a-dia do trabalho com CARF.

<Steps>
1. Primeiro passo com descrição clara
2. Segundo passo com resultado esperado
3. Terceiro passo finalizando o processo
</Steps>

<Aside type="caution">
  Atenção para situações que requerem cuidado especial.
</Aside>

## Próximos Passos

Agora que você entende {conceito}, pode:

<CardGrid>
  <Card title="Próximo Guia" icon="right-arrow">
    Descrição breve do próximo passo recomendado.
    [Ir para próximo guia](/guia/proximo/)
  </Card>
  <Card title="Manual Relacionado" icon="document">
    Manual que complementa este guia.
    [Ver manual](/manuais/aplicacao/funcionalidade/)
  </Card>
</CardGrid>

## Ver Também

- [Link para página relacionada 1](/guia/relacionado-1/)
- [Link para página relacionada 2](/guia/relacionado-2/)
```

## Exemplo Real Completo

```mdx
---
title: "Fluxo de Aprovação de Unidades"
description: "Entenda como funciona o processo de aprovação de unidades habitacionais no CARF, desde a coleta até a validação final."
source: "CENTRAL/WORKFLOWS/04-analyst-validation-workflow.md"
sidebar:
  order: 4
  label: "Aprovação"
draft: false
---

import { Aside, Steps, Card, CardGrid } from '@astrojs/starlight/components';

# Fluxo de Aprovação de Unidades

O processo de aprovação garante que todas as unidades cadastradas atendem aos requisitos
da Lei 13.465/2017 antes de serem consideradas válidas para legitimação fundiária.

## Visão Geral do Fluxo

O fluxo de aprovação envolve três etapas principais:

<Steps>
1. **Coleta**: Agente de campo cadastra unidade via REURBCAD ou GeoWeb
2. **Análise**: Analista verifica dados e documentação
3. **Aprovação/Rejeição**: Decisão final com justificativa
</Steps>

<Aside type="note">
  Apenas usuários com role **Analista** ou superior podem aprovar unidades.
</Aside>

## Status da Unidade

Uma unidade passa pelos seguintes status durante o fluxo:

| Status | Descrição | Próximas Ações |
|--------|-----------|----------------|
| Em Rascunho | Cadastro iniciado, não enviado | Completar e enviar |
| Aguardando Aprovação | Enviada para análise | Aprovar ou Rejeitar |
| Aprovada | Validada pelo analista | Vincular titular |
| Rejeitada | Problemas identificados | Corrigir e reenviar |

<Aside type="tip">
  Unidades rejeitadas podem ser corrigidas pelo agente de campo e reenviadas para análise.
</Aside>

## Critérios de Aprovação

Para ser aprovada, uma unidade deve atender:

- Geometria válida e sem sobreposição
- Todos campos obrigatórios preenchidos
- Documentação comprobatória anexada
- Localização dentro da comunidade

<Aside type="caution">
  Unidades com sobreposição de mais de 5% são automaticamente rejeitadas e requerem
  revisão da geometria.
</Aside>

## Próximos Passos

<CardGrid>
  <Card title="Manual de Aprovação" icon="document">
    Passo a passo detalhado para analistas.
    [Ver manual](/manuais/geoweb/analise/)
  </Card>
  <Card title="Vincular Titular" icon="person">
    Próxima etapa após aprovação.
    [Ver guia](/guia/vincular-titular/)
  </Card>
</CardGrid>

## Ver Também

- [Cadastrar Unidade](/guia/cadastrar-unidade/)
- [Papéis e Permissões](/sistema/papeis/)
- [Contestação de Decisões](/guia/contestacao/)
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
