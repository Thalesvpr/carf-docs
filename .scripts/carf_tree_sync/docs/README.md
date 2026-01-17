# carf_tree_sync

Sistema de sincronizacao de indices para READMEs do repositorio CARF.

## Visao Geral

O `carf_tree_sync` e uma ferramenta que gera automaticamente secoes de indice em arquivos README.md, usando abordagem bottom-up para garantir que o grafo de dependencias esteja sempre resolvido.

### Abordagem Bottom-Up

```
Fase 1: FOLHAS (arquivos individuais)
    RF-001.md, UC-002.md, ADR-005.md
    -> Extrair: ID, titulo, frontmatter (epic, modules)

Fase 2: NOS INTERMEDIARIOS (subpastas)
    01-auth-security/README.md
    -> Gerar tabela de arquivos com dados da Fase 1

Fase 3: NOS RAIZ (READMEs pai)
    REQUIREMENTS/README.md
    -> Agregar contagens da Fase 2
```

## Instalacao

Nenhuma dependencia externa necessaria. Usa apenas biblioteca padrao Python 3.8+.

## Uso

### Comandos Basicos

```bash
# Sincronizar todos os READMEs
cd .scripts
python -m carf_tree_sync --root /c/DEV/CARF

# Dry-run (mostra mudancas sem aplicar)
python -m carf_tree_sync --dry-run

# Sincronizar apenas CENTRAL
python -m carf_tree_sync --path CENTRAL

# Verbose mode
python -m carf_tree_sync --verbose
```

### Opcoes

| Opcao | Descricao |
|-------|-----------|
| `--root PATH` | Diretorio raiz do repositorio (default: diretorio atual) |
| `--path SUBPATH` | Subpath especifico para sincronizar |
| `--dry-run` | Mostra mudancas sem aplicar |
| `-v, --verbose` | Mostra progresso detalhado |
| `--no-color` | Desabilita cores no output |

## Tipos de Indices

### 1. Indice de Subpastas

Para READMEs com subdiretorios que tem READMEs:

```markdown
## Indice por Dominio (221 requisitos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
| 01 | [Autenticacao e Seguranca](./01-auth-security/README.md) | 16 |
| 02 | [Gestao de Tenants](./02-tenants/README.md) | 4 |
```

### 2. Indice de Arquivos

Para READMEs com arquivos markdown:

```markdown
## Arquivos (16 requisitos)

| ID | Titulo |
|:---|:-------|
| [RF-001](./RF-001-xxx.md) | Integracao com Keycloak |
| [RF-002](./RF-002-xxx.md) | Fluxo Authorization Code |
```

## Marcadores de Geracao

O sistema usa marcadores para delimitar conteudo gerado:

```markdown
<!-- GENERATED:START - Nao edite abaixo desta linha -->
[CONTEUDO GERADO]
*Gerado automaticamente em YYYY-MM-DD HH:MM*
<!-- GENERATED:END -->
```

- Todo conteudo ACIMA de `GENERATED:START` e preservado
- Apenas a secao entre START/END e regenerada
- Se nao existir marcador, adiciona ao final do arquivo

## Arquitetura

```
carf_tree_sync/
|-- __init__.py          # Pipeline principal
|-- __main__.py          # CLI
|-- config.py            # Configuracoes
|-- scanner/
|   |-- tree.py          # Descoberta de nos
|-- parser/
|   |-- frontmatter.py   # Parse YAML
|   |-- generated.py     # Parse secoes geradas
|   |-- document.py      # Parse documentos
|-- indexer/
|   |-- base.py          # Interface
|   |-- subfolders.py    # Indice de subpastas
|   |-- files.py         # Indice de arquivos
|   |-- epic.py          # Indice por epica
|   |-- module.py        # Indice por modulo
|-- writer/
    |-- updater.py       # Atualizador de READMEs
```

## Configuracoes

Edite `config.py` para ajustar:

- `DOMAIN_NAMES`: Mapeamento de slug para nome legivel
- `REQUIREMENT_TYPES`: Tipos de requisitos e prefixos
- `MODULE_ORDER`: Ordem de exibicao dos modulos
- `EXCLUDE_DIRS`: Pastas a ignorar

## Exit Codes

| Codigo | Significado |
|--------|-------------|
| 0 | Sucesso |
| 1 | Erros durante sincronizacao |
| 2 | Erro de execucao |

---

**Ultima atualizacao:** 2026-01-15

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
