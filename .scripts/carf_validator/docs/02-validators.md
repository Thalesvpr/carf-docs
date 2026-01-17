# Validadores

## Validadores Locais (por arquivo)

| Nome | Descricao | Codigos |
|------|-----------|---------|
| `frontmatter` | Valida campos obrigatorios do frontmatter YAML | FRONT001-003 |
| `metadata` | Valida footer de metadata (data, status) | META001-006 |
| `structure` | Valida secoes obrigatorias por tipo | STRUCT001-002 |
| `file_size` | Valida contagem de palavras min/max | SIZE001-002 |
| `nomenclature` | Valida terminologia tecnica consistente | NOMEN001 |
| `title` | Valida padrao de titulo H1 por tipo | TITLE001-003 |
| `density` | Valida densidade de paragrafos | DENS001-004 |
| `content_bullets` | Valida bullets apenas em footer | BULLET001 |
| `prose_continuity` | Detecta quebras excessivas de prosa | PROSE001-003 |
| `readme_structure` | Valida estrutura de README | README001-007 |
| `link_format` | Valida formato de links internos | LINK001-005 |

## Validadores Globais (de grafo)

| Nome | Descricao | Codigos |
|------|-----------|---------|
| `broken_links` | Detecta links para arquivos inexistentes | BLINK001 |
| `orphans` | Detecta arquivos sem referencias | ORPHAN001 |
| `isolation` | Valida que CENTRAL nao linka PROJECTS | ISOL001-002 |
| `rf_coverage` | Verifica cobertura de RF em FEATURES | RFCOV001 |
| `uc_coverage` | Verifica cobertura de UC em modulos | UCCOV001 |
| `cross_refs` | Valida direcao de referencias | XREF001 |

## Codigos de Erro por Validador

### frontmatter

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| FRONT001 | ERROR | UC sem campo 'modules' no frontmatter |
| FRONT002 | ERROR | RF sem campo 'modules' no frontmatter |
| FRONT003 | WARNING | US sem campo 'epic' no frontmatter |

### metadata

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| META001 | ERROR | Campo 'Ultima atualizacao' ausente |
| META002 | WARNING | Documento desatualizado (>12 meses) |
| META003 | WARNING | Campo 'Status do arquivo' ausente |
| META004 | ERROR | ADR sem campo 'Data' |
| META005 | ERROR | ADR sem campo 'Status' |
| META006 | WARNING | ADR sem campo 'Decisor' |

### structure

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| STRUCT001 | ERROR | Secao obrigatoria ausente |
| STRUCT002 | WARNING | Frase obrigatoria ausente (US) |

### file_size

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| SIZE001 | WARNING | Documento muito curto |
| SIZE002 | INFO | Documento muito longo |

### nomenclature

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| NOMEN001 | WARNING | Terminologia incorreta (Postgres->PostgreSQL, etc.) |

### title

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| TITLE001 | ERROR | Documento sem titulo H1 |
| TITLE002 | ERROR | Primeira linha nao e titulo H1 |
| TITLE003 | WARNING | Titulo nao segue padrao do tipo |

### density

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| DENS001 | WARNING | Conteudo muito curto (chars) |
| DENS002 | WARNING | Muitos paragrafos |
| DENS003 | INFO | Muitas sentencas curtas |
| DENS004 | WARNING | Poucas sentencas |

### content_bullets

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| BULLET001 | WARNING | Bullet fora de secao estruturada |

### prose_continuity

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| PROSE001 | INFO | Quebras excessivas de linha |
| PROSE002 | WARNING | Paragrafo orfao (muito curto) |
| PROSE003 | INFO | Baixa densidade de virgulas |

### readme_structure

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| README001 | ERROR | Arquivo index.md nao permitido |
| README002 | ERROR | README sem titulo H1 |
| README003 | WARNING | Titulo nao comeca com maiuscula |
| README004 | INFO | Falta linha em branco apos H1 |
| README005 | WARNING | README com subpastas sem secao estrutura |
| README006 | INFO | Falta separador antes do footer |
| README007 | INFO | Links de estrutura sem negrito |

### link_format

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| LINK001 | ERROR | Path absoluto Windows |
| LINK002 | ERROR | Path absoluto Unix |
| LINK003 | WARNING | Link sem prefixo relativo ./ |
| LINK004 | INFO | Diretorio deveria ser UPPERCASE |
| LINK005 | WARNING | Link para diretorio sem README.md |

### broken_links

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| BLINK001 | ERROR | Link para arquivo inexistente |

### orphans

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| ORPHAN001 | WARNING/INFO | Documento sem referencias |

### isolation

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| ISOL001 | ERROR | CENTRAL linka para PROJECTS |
| ISOL002 | ERROR | CENTRAL referencia PROJECTS |

### rf_coverage

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| RFCOV001 | WARNING | RF sem cobertura em FEATURES |

### uc_coverage

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| UCCOV001 | INFO | UC nao mencionado em features do modulo |

### cross_refs

| Codigo | Severidade | Descricao |
|--------|------------|-----------|
| XREF001 | INFO | PROJECTS sem referencia a CENTRAL |

---

**Ultima atualizacao:** 2026-01-15
