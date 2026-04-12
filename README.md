---
status: review
updated: 2026-01-22
type: readme
---

# CARF - Sistema de Regularizacao Fundiaria Urbana

Sistema para gestao de processos de regularizacao fundiaria urbana conforme Lei 13.465/2017, permitindo que prefeituras gerenciem todo o ciclo desde o cadastramento de unidades habitacionais em campo ate a emissao de titulos de legitimacao.

A arquitetura e composta por [projetos independentes](./PROJECTS/README.md) que incluem o backend .NET com API REST geoespacial, portal web para analistas, app mobile para coleta em campo offline, plugin QGIS para analises espaciais, console admin para gerenciar usuarios, e bibliotecas compartilhadas entre os projetos.

A documentacao fica organizada em duas partes principais. A [documentacao central](./CENTRAL/README.md) contem a especificacao do sistema como um todo, servindo como **fonte unica de verdade** para dominio, regras de negocio, requisitos, arquitetura e padroes. Os [projetos de implementacao](./PROJECTS/README.md) contem a documentacao tecnica **especifica** de cada um, explicando como implementam o que esta especificado.

## Estrutura

| Pasta | Proposito |
|-------|-----------|
| [CENTRAL](./CENTRAL/README.md) | Especificacao compartilhada: dominio, regras, requisitos, arquitetura, design system, seguranca |
| [PROJECTS](./PROJECTS/README.md) | Implementacoes: GEOAPI, REURBWEB, REURBCAD, GEOGIS, KEYCLOAK, bibliotecas |
| [STANDARDS](./STANDARDS/README.md) | Convencoes de nomenclatura, status, conteudo, links e codigo |

## Convencoes Rapidas

Repositorio documentation-only (zero codigo). Todo .md tem frontmatter com status: `review` (rascunho ou recem-escrito), `approved` (validado por humano) ou `rejected` (erro encontrado, campo `description` obrigatorio com motivo). Antes de escrever, leia os [STANDARDS](./STANDARDS/README.md) e estude documentos vizinhos seguindo links.

Fontes de verdade que devem ser consultadas antes de qualquer escrita:

| Fonte | Caminho | Conteudo |
|-------|---------|----------|
| Schema PostgreSQL | PROJECTS/GEOAPI/DOCS/ARCHITECTURE/LAYERS/INFRA/PERSISTENCE/02-database-schema.md | Todas as tabelas, campos, tipos, constraints, indices |
| API Reference | PROJECTS/GEOAPI/DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/00-api-reference.md | Todos os endpoints, metodos, rotas, roles |
| Content Guidelines | STANDARDS/STD-005-content-guidelines.md | Limites de palavras, prosa continua, formato |
| File Status | STANDARDS/STD-001-file-status-convention.md | Regras de frontmatter e ciclo de vida |

## Para Agentes (Onboarding Rapido)

Se voce e um agente Claude trabalhando neste repositorio, siga estas regras antes de qualquer coisa:

**Ciclo de trabalho:** Leia as fontes de verdade listadas acima e pelo menos 2-3 documentos vizinhos na pasta onde vai escrever. Siga links internos encontrados nesses documentos para entender contexto. So entao escreva.

**Status de frontmatter:** Conteudo novo ou editado entra como `status: review`. Nunca use `active`, `draft`, `current` ou qualquer outro valor em documentos de CENTRAL/ e PROJECTS/. O ciclo e: `review` (agente escreve) → `approved` (humano valida) → eventual `rejected` se encontrar erro depois.

**Tracking de erros via rejected:** Se ao ler um documento voce identificar informacao incorreta, inconsistencia com o schema, campo faltando ou conflito com outra fonte de verdade, altere o frontmatter para `status: rejected` e adicione o campo `description` explicando o problema encontrado. Isso garante que o erro nao se perca e sera corrigido depois. Exemplo de frontmatter rejected:

```yaml
---
type: leaf
status: rejected
updated: 2026-02-08
description: Campo OccupantType listado como obrigatorio mas e nullable no schema PostgreSQL
---
```

**Auto-suficiencia:** Cada documento deve conter informacao suficiente para que um desenvolvedor implemente o que esta descrito sem precisar consultar outra fonte alem das referenciadas explicitamente. Se a doc nao e suficiente para implementar, ela nao esta pronta.

---

**Versao:** v1.0.0 MVP
**Licenca:** Proprietario
