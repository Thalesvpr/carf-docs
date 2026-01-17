# Referencia de Regras

## Regras de Titulo por Tipo

| Tipo | Padrao | Exemplo |
|------|--------|---------|
| ADR | `# ADR-NNN:` | `# ADR-001: Usar PostgreSQL` |
| UC | `# UC-NNN:` | `# UC-001: Cadastrar Unidade` |
| RF | `# RF-NNN:` | `# RF-001: Sistema deve...` |
| RNF | `# RNF-NNN:` | `# RNF-001: Tempo de resposta` |
| US | `# US-NNN:` | `# US-001: Como usuario...` |
| README | `# UPPERCASE` ou `# Nome - Desc` | `# GEOAPI` ou `# GEOAPI - API REST` |

## Regras de Estrutura por Tipo

### Use Case (UC)

Secoes obrigatorias:
- `## Regras de Negocio`
- `## Rastreabilidade`

### Requisito Funcional (RF)

Secoes obrigatorias:
- `## Criterios de Aceitacao`

### User Story (US)

Frases obrigatorias (case-insensitive):
- "Como "
- "quero "
- "para que "

### Feature

Secoes obrigatorias (uma das opcoes):
- `## Validacoes` ou `## Validation`
- `## API Integration` ou `## Integracao API`
- `## Relacionamentos` ou `## Domain Model`

### How-To

Secoes obrigatorias:
- `## Pre-requisitos`
- `## Passos`

## Regras de Tamanho (palavras)

| Tipo | Minimo | Maximo |
|------|--------|--------|
| README | 50 | 500 |
| ADR | 200 | 800 |
| UC | 150 | 800 |
| RF | 80 | 400 |
| RNF | 60 | 350 |
| US | 60 | 300 |
| ENTITY | 150 | 600 |
| FEATURE | 200 | 1000 |
| HOW_TO | 150 | 900 |
| CONCEPT | 100 | 600 |
| BUSINESS_RULE | 100 | 800 |
| WORKFLOW | 150 | 1000 |
| PATTERN | 200 | 900 |

## Regras de Densidade

| Tipo | Min Chars | Max Paragrafos | Palavras/Sentenca |
|------|-----------|----------------|-------------------|
| RF | 800 | 2 | 20-50 |
| US | 1000 | 2 | 25-60 |
| ENTITY | 1500 | 2 | 35-100 |
| BUSINESS_RULE | 800 | 3 | 15-45 |
| UC | 600 | 3 | 20-50 |

## Regras de Nomenclatura

Termos que devem seguir grafia correta:

| Incorreto | Correto |
|-----------|---------|
| REURB (sem qualificador) | REURB-S ou REURB-E |
| Postgres | PostgreSQL |
| KeyCloak | Keycloak |
| react-native (em prosa) | React Native |
| DotNet | .NET |
| Nodejs | Node.js |
| Typescript | TypeScript |
| Javascript | JavaScript |
| Postgis | PostGIS |

## Regras de Metadata Footer

### Documentos Gerais

Campos obrigatorios:
```markdown
---

**Ultima atualizacao:** YYYY-MM-DD
```

### README

Campos obrigatorios:
```markdown
---

**Ultima atualizacao:** YYYY-MM-DD
**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
```

### ADR

Campos obrigatorios:
```markdown
**Data:** YYYY-MM-DD
**Status:** Aprovado e Implementado
**Decisor:** Nome/Equipe
```

## Regras de Links

### Formato

- Paths relativos obrigatorios: `./pasta/arquivo.md`
- Sem paths absolutos Windows: `C:\...`
- Sem paths absolutos Unix: `/...`

### Diretorios

- Diretorios em CENTRAL devem ser UPPERCASE: `./DOMAIN-MODEL/`
- Links para diretorios devem apontar para README: `./PASTA/README.md`

### Isolamento

- CENTRAL nao pode linkar para PROJECTS
- PROJECTS pode (e deve) linkar para CENTRAL

## Regras de README

1. Titulo H1 na primeira linha (apos frontmatter)
2. Linha em branco apos H1
3. Nao usar `index.md` - sempre `README.md`
4. Separador `---` antes do footer
5. Se tiver subpastas, incluir secao de estrutura

### Secoes de Estrutura Validas

- `## Estrutura`
- `## Aplicacoes`
- `## Bibliotecas`
- `## Dominios`
- `## Indice`
- `## Arquivos`

### Formato de Links em Listas

Preferencial (com negrito):
```markdown
- **[NOME/](./NOME/README.md)** - Descricao curta
```

## Secoes que Permitem Bullets

Bullets (listas) sao permitidos APENAS nestas secoes:

- Fluxos Alternativos
- Fluxos de Excecao
- Regras de Negocio
- Rastreabilidade
- Criterios de Aceitacao
- Relacionamentos
- Modulos
- Pre-condicoes
- Pos-condicoes
- Atores
- Referencias
- Ver tambem
- Dependencias
- Estrutura
- Aplicacoes
- Bibliotecas
- Dominios

No corpo do documento, usar prosa continua.

---

**Ultima atualizacao:** 2026-01-15
