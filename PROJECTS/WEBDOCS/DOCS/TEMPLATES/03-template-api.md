---
type: leaf
status: review
updated: 2026-01-21
---

# Template de API

Template para páginas da seção /api/ que documentam conceitos e uso da API GEOAPI de forma não-técnica complementando Swagger.

Frontmatter obrigatório define title com nome do recurso ou conceito, description com resumo de 1-2 linhas, section com valor api, e audience com valor user. Esta seção é pública diferente de Swagger interativo que requer role dev.

Introdução explica o que recurso representa no contexto de negócio, não apenas tecnicamente. Exemplo: "Unidades representam imóveis cadastrados no processo de regularização fundiária" ao invés de "endpoint /units retorna lista de unidades".

Seção de conceitos explica modelo de dados de forma simplificada. Campos principais com descrição do significado, não do tipo técnico. Relacionamentos com outros recursos explicados em termos de negócio.

Seção de operações lista ações possíveis (criar, listar, atualizar, etc) com explicação de quando usar cada uma. Não incluir detalhes técnicos de request/response que estão no Swagger. Focar em casos de uso.

Seção de permissões indica quais roles podem executar cada operação. Tabela simples com operação e roles necessárias. Link para documentação de roles para entender hierarquia.

Seção de exemplos de uso descreve cenários comuns em linguagem de negócio. Exemplo: "Para cadastrar unidade coletada em campo, primeiro valide os dados do titular, depois..."

## Template Copy-Paste

```mdx
---
title: "Nome do Recurso"
description: "Descrição do recurso em termos de negócio, não técnicos. Entre 50-160 caracteres."
source: "PROJECTS/GEOAPI/DOCS/API/nome-recurso.md"
sidebar:
  order: 1
  label: "Label Curto"
draft: false
---

import { Aside, Card, CardGrid } from '@astrojs/starlight/components';

# Nome do Recurso

Explicação do que este recurso representa no contexto da regularização fundiária.
Foco no valor de negócio, não na implementação técnica.

## O que são {Recursos}?

Descrição conceitual do recurso em linguagem acessível para usuários não-técnicos.
Relacione com o processo de trabalho real.

<Aside type="note">
  Informação contextual que ajuda a entender quando usar este recurso.
</Aside>

## Campos Principais

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| campo1 | O que significa este campo | "Valor exemplo" |
| campo2 | Para que serve | "Outro valor" |
| status | Situação atual do registro | "Ativo", "Pendente" |

## Operações Disponíveis

### Consultar {Recursos}

Quando usar: para visualizar dados existentes sem modificá-los.

Quem pode: Todos os usuários autenticados.

### Criar {Recurso}

Quando usar: ao registrar um novo item no sistema.

Quem pode: Agentes de Campo e superiores.

### Atualizar {Recurso}

Quando usar: para corrigir ou complementar informações.

Quem pode: Depende do status atual do recurso.

<Aside type="caution">
  Recursos aprovados não podem ser editados diretamente.
  É necessário solicitar alteração.
</Aside>

### Excluir {Recurso}

Quando usar: para remover registros incorretos ou duplicados.

Quem pode: Apenas Administradores e Super Admin.

## Permissões por Role

| Operação | User | Field Agent | Analyst | Admin | Super Admin |
|----------|------|-------------|---------|-------|-------------|
| Consultar | ✅ | ✅ | ✅ | ✅ | ✅ |
| Criar | ❌ | ✅ | ✅ | ✅ | ✅ |
| Atualizar | ❌ | ✅* | ✅ | ✅ | ✅ |
| Excluir | ❌ | ❌ | ❌ | ✅ | ✅ |

*Apenas recursos criados pelo próprio usuário e ainda não aprovados.

## Exemplos de Uso

### Cenário 1: Cadastrar após coleta em campo

1. Agente de campo coleta dados no app REURBCAD
2. Dados são sincronizados com servidor
3. Recurso é criado automaticamente com status "Pendente"
4. Analista revisa e aprova ou solicita correções

### Cenário 2: Atualizar dados incompletos

1. Analista identifica campos faltando
2. Solicita alterações com comentário explicativo
3. Agente de campo recebe notificação
4. Agente completa dados e reenvia

## Ver Também

<CardGrid>
  <Card title="Recurso Relacionado" icon="right-arrow">
    Descrição breve da relação.
    [Ver documentação](/api/recurso-relacionado/)
  </Card>
  <Card title="Documentação Técnica" icon="setting">
    Para desenvolvedores: Swagger interativo.
    [Abrir Swagger](/dev/api/swagger/)
  </Card>
</CardGrid>
```

## Exemplo Real: Unidades Habitacionais

```mdx
---
title: "Unidades Habitacionais"
description: "Entenda o que são unidades habitacionais no CARF e como são utilizadas no processo de regularização fundiária."
source: "PROJECTS/GEOAPI/DOCS/API/units.md"
sidebar:
  order: 3
  label: "Unidades"
draft: false
---

import { Aside, Card, CardGrid } from '@astrojs/starlight/components';

# Unidades Habitacionais

Unidades habitacionais são os imóveis cadastrados no processo de regularização fundiária.
Cada unidade representa uma moradia ou estabelecimento dentro de uma comunidade.

## O que são Unidades?

Uma unidade habitacional é o registro de um imóvel que será regularizado.
Ela contém a localização geográfica (polígono no mapa), dados do imóvel (tipo de uso, área),
e está vinculada a titulares (pessoas que ocupam ou possuem o imóvel).

<Aside type="note">
  Unidades são o elemento central do cadastro. Titulares, documentos e
  o processo de legitimação estão todos vinculados a unidades.
</Aside>

## Campos Principais

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| Identificador | Código único da unidade | "UN-2024-00123" |
| Tipo de Uso | Finalidade do imóvel | "Residencial", "Comercial" |
| Área | Tamanho em metros quadrados | "120.5 m²" |
| Status | Etapa no fluxo de trabalho | "Em Análise" |
| Comunidade | Onde a unidade está localizada | "Vila Nova Esperança" |

## Ciclo de Vida

```
Rascunho → Aguardando Aprovação → Aprovada → Em Legitimação → Legitimada
                    ↓
               Rejeitada → (correção) → Aguardando Aprovação
```

## Permissões por Role

| Operação | User | Field Agent | Analyst | Admin | Super Admin |
|----------|------|-------------|---------|-------|-------------|
| Visualizar | ✅ | ✅ | ✅ | ✅ | ✅ |
| Criar | ❌ | ✅ | ✅ | ✅ | ✅ |
| Editar | ❌ | ✅* | ✅ | ✅ | ✅ |
| Aprovar | ❌ | ❌ | ✅ | ✅ | ✅ |
| Excluir | ❌ | ❌ | ❌ | ✅ | ✅ |

## Ver Também

<CardGrid>
  <Card title="Titulares" icon="person">
    Pessoas vinculadas às unidades.
    [Ver documentação](/api/titulares/)
  </Card>
  <Card title="Fluxo de Aprovação" icon="approve-check">
    Como unidades são aprovadas.
    [Ver guia](/guia/aprovacao/)
  </Card>
</CardGrid>
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
