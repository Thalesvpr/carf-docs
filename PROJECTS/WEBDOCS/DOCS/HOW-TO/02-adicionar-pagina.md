---
type: leaf
status: review
updated: 2026-01-21
---

# Adicionar Página

Guia para criar novo documento no WEBDOCS com frontmatter correto e estrutura adequada para a seção destino.

Identificar seção destino (guia, sistema, manuais, api, dev, changelog) e navegar para pasta correspondente em src/content/docs/. Para manuais, navegar para subpasta da aplicação (geoweb, reurbcad, admin).

Criar arquivo Markdown com nome em kebab-case descritivo do conteúdo. Extensão .md para Markdown puro ou .mdx se precisar de componentes. Exemplo: cadastrar-unidade.md para guia de cadastro.

Adicionar frontmatter no topo do arquivo entre delimitadores de três hífens. Campos obrigatórios são title com nome da página, description com resumo de 50-160 caracteres, e section com nome da seção. Campos opcionais incluem sidebar para customizar navegação e audience para indicar público (user ou dev).

Escrever conteúdo seguindo diretrizes de content guidelines. Introdução contextualiza tema, corpo desenvolve com headings hierárquicos, conclusão sugere próximos passos. Usar callouts para destacar informações importantes.

Adicionar screenshots se necessário salvando em public/images/ na subpasta correspondente à seção. Referências de imagem usam path relativo a public/ sem a pasta public no caminho.

Validar localmente executando bun run build que verifica frontmatter contra schema Zod e valida links internos. Erros indicam campos ausentes ou links quebrados para corrigir.

Criar pull request com nova página para review. Preview deployment automático permite validar aparência antes de merge. Solicitar review de membro da equipe de documentação.

## Frontmatter Completo

Template copy-paste para nova página:

```yaml
---
title: "Título da Página"
source: "CENTRAL/WORKFLOWS/02-field-data-collection-workflow.md"
sidebar:
  order: 1
  label: "Label Curto"
  badge: "Novo"
draft: false
---
```

## Estrutura de Pastas

```json
{
  "content_structure": {
    "src/content/docs/": {
      "guia/": "Conceitos e workflows - para todos usuários",
      "sistema/": "Visão geral do CARF - para analistas+",
      "manuais/": {
        "geoweb/": "Manual do GeoWeb - analistas",
        "reurbcad/": "Manual do REURBCAD - agentes de campo",
        "admin/": "Manual Admin - administradores"
      },
      "api/": "Documentação da API - desenvolvedores",
      "status/": "Página de status - todos"
    }
  }
}
```

## Exemplo de Página MDX

```mdx
---
title: "Cadastrar Unidade Habitacional"
description: "Guia passo a passo para cadastrar uma nova unidade habitacional no sistema CARF usando GeoWeb ou REURBCAD."
source: "CENTRAL/REQUIREMENTS/USE-CASES/UC-001-cadastrar-unidade-habitacional/UC-001-cadastrar-unidade-habitacional.md"
sidebar:
  order: 3
  badge: "Atualizado"
---

import { Aside, Steps, Card, CardGrid } from '@astrojs/starlight/components';

# Cadastrar Unidade Habitacional

Neste guia você aprenderá a cadastrar uma nova unidade habitacional no sistema CARF.

<Aside type="note">
  Este processo pode ser realizado via GeoWeb (desktop) ou REURBCAD (mobile).
</Aside>

## Pré-requisitos

- Acesso ao sistema com role **Agente de Campo** ou superior
- Comunidade já cadastrada no sistema
- Dispositivo com GPS (para REURBCAD)

## Passo a Passo

<Steps>
1. Acesse a comunidade desejada
2. Clique em "Nova Unidade"
3. Desenhe o polígono da unidade no mapa
4. Preencha os dados obrigatórios
5. Salve e envie para aprovação
</Steps>

## Opções de Cadastro

<CardGrid>
  <Card title="Via GeoWeb" icon="laptop">
    Ideal para cadastro em escritório com imagens de satélite.
    [Ir para manual GeoWeb](/manuais/geoweb/)
  </Card>
  <Card title="Via REURBCAD" icon="phone">
    Ideal para cadastro em campo com GPS.
    [Ir para manual REURBCAD](/manuais/reurbcad/)
  </Card>
</CardGrid>

## Próximos Passos

Após cadastrar a unidade:
- [Vincular titular à unidade](/guia/vincular-titular/)
- [Enviar para aprovação](/guia/aprovar-unidade/)
```

## Convenção de Nomes

```json
{
  "naming_conventions": {
    "file_name": {
      "format": "kebab-case.mdx",
      "examples": ["cadastrar-unidade.mdx", "vincular-titular.mdx"]
    },
    "title": {
      "format": "Title Case em português",
      "examples": ["Cadastrar Unidade Habitacional", "Vincular Titular à Unidade"]
    },
    "source": {
      "format": "Caminho exato no carf-docs",
      "examples": ["CENTRAL/WORKFLOWS/02-field-data-collection-workflow.md"]
    }
  }
}
```

## Validação Local

```bash
# Verificar se frontmatter está correto
bun run astro check

# Build completo com validação
bun run build

# Validar apenas sources
bun run validate:sources
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
