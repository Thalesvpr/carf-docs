---
type: leaf
status: approved
updated: 2026-02-24
---

# Regiao

Unidade estrategica operacional definida pelo Tenant para organizar sua atuacao. Nao e um conceito geografico fixo — e um agrupamento logico cujo significado e escopo sao determinados pela empresa conforme sua necessidade de fluxo.

Uma regiao pode representar um bairro, uma cidade, um conjunto de CEPs, uma macrorregiao, ou qualquer recorte que faca sentido para o processo operacional do Tenant. O sistema nao impoe semantica territorial — aceita qualquer definicao que a empresa adote.

## Papel no Dominio

Regiao e um **container de atuacao**: organiza Comunidades, equipes e responsabilidades sem assumir hierarquia geografica rigida. Cada Tenant define suas regioes conforme sua estrutura interna.

Exemplos de uso real:
- Prefeitura pequena: uma unica regiao = toda a cidade
- Prefeitura grande: regioes por zona (Norte, Sul, Centro, Rural)
- Empresa de topografia: regioes por contrato ou lote de municipios
- Orgao estadual: regioes por conjunto de municipios ou bacias hidrograficas

## Principios de Modelagem

1. **Operacional, nao cartografico** — Regiao nao e um dado do mapa, e uma decisao de negocio
2. **Configuravel por Tenant** — Cada empresa define o que "regiao" significa para si
3. **Escopo variavel** — Pode ser granular (bairro) ou amplo (estado inteiro)
4. **Geometria opcional** — O perimetro e informativo, nao definitivo. A regiao existe mesmo sem boundary
5. **Sem hierarquia geografica imposta** — O sistema nao assume pais > estado > cidade > bairro
6. **Expansivel sem refatoracao** — Futuramente pode suportar multi-nivel, sobreposicao territorial ou sub-regioes, sem quebrar o modelo atual

## Propriedades

| Propriedade | Tipo       | Descricao                                                    |
|-------------|------------|--------------------------------------------------------------|
| nome        | string     | Nome identificador da regiao (definido pelo Tenant)          |
| descricao   | string?    | Descricao livre do escopo/abrangencia                        |
| scopeType   | enum?      | Tipo de escopo indicativo: `custom`, `neighborhood`, `city`, `state`, `macro_region` |
| boundary    | geometry?  | Perimetro indicativo (opcional, informativo)                 |
| metadata    | jsonb?     | Dados complementares livres (CEPs, codigos IBGE, tags, etc.) |
| tenantId    | UUID       | Referencia ao Tenant proprietario                            |
| status      | enum       | Estado da regiao: `active` ou `inactive`                     |

### Sobre `scopeType`

O campo `scopeType` e **indicativo**, nao restritivo. Serve para dar contexto ao sistema e a interface sobre a granularidade da regiao, mas nao impoe regras. Um Tenant pode ter regioes com scopeTypes diferentes coexistindo.

### Sobre `metadata`

Campo JSONB flexivel para dados que variam conforme o uso. Exemplos:
- `{ "ceps": ["20000-000", "20999-999"] }` — para regioes definidas por faixa de CEP
- `{ "ibgeCodes": ["3304557"] }` — para regioes vinculadas a municipios IBGE
- `{ "tags": ["contrato-2026-A", "lote-3"] }` — para regioes logicas de contrato

## Relacionamentos

- Pertence a um **Tenant** (N:1)
- Contem zero ou mais **Comunidades** (1:N)
- Equipes podem ser designadas por Regiao
- Upload links podem ser vinculados a uma Regiao

## O que Regiao NAO e

- Nao e um nivel fixo de hierarquia geografica
- Nao e um substituto para endereco ou localizacao
- Nao e um conceito imutavel — pode ser redefinida pelo Tenant a qualquer momento
- Nao assume que toda Comunidade deve pertencer a uma Regiao (associacao pode ser opcional inicialmente)

## Evolucao Futura

O modelo atual e flat (Tenant > Regioes). Evolucoes possiveis sem refatoracao:
- **Sub-regioes**: adicionar `parentId` opcional para criar arvore de regioes
- **Sobreposicao**: permitir que uma Comunidade pertenca a mais de uma Regiao (via tabela de juncao)
- **Multi-nivel nomeado**: o Tenant define seus proprios niveis (ex: "Diretoria > Gerencia > Setor")

Essas evolucoes devem ser naturais, nao impostas prematuramente.

## Referencia

- Ver [07-tenant.md](./07-tenant.md)
- Ver [04-community.md](./04-community.md)
