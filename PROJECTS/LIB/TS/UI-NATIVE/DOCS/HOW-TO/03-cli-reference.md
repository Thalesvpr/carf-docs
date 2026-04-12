---
type: leaf
status: active
updated: 2026-02-10
---

# CLI Reference

O CLI `@carf/ui-native` automatiza a copia de componentes para seu projeto, seguindo a filosofia shadcn: componentes copiados, nao instalados.

## Instalacao

O CLI roda diretamente sem instalacao global:

```bash
# Via npx (recomendado)
npx @carf/ui-native <command>

# Ou diretamente se clonou o repositorio
node path/to/carf-ui-native/cli/cli.mjs <command>
```

## Comandos

### `init`

Inicializa o projeto: cria configuracao, copia utilitarios base e opcionalmente o tema.

```bash
carf-ui init
```

O comando pergunta interativamente:
1. Se deseja incluir o tema (ThemeProvider, colors, presets)
2. Detecta automaticamente o package manager (bun/npm/pnpm/yarn)

Acoes executadas:
- Cria diretorios `src/components/ui/`, `src/lib/`, `src/theme/` (se tema habilitado)
- Copia `utils.ts` (cn utility) e `elevation.ts`
- Se tema: copia 5 arquivos do sistema de tema
- Grava `carf-ui.json` na raiz do projeto
- Oferece instalar dependencias npm faltantes

### `add <componente...>`

Adiciona um ou mais componentes ao projeto com resolucao automatica de dependencias internas.

```bash
# Adicionar um componente
carf-ui add button

# Adicionar multiplos
carf-ui add icon-button select dialog

# Adicionar todos os componentes de formulario
carf-ui add button input checkbox switch select
```

O comando:
1. Le `carf-ui.json` (erro se nao existe — rode `init` primeiro)
2. Resolve dependencias internas recursivamente (ex: `select` auto-adiciona `search-bar`)
3. Mostra preview dos arquivos que serao copiados e dependencias npm
4. Pede confirmacao
5. Copia arquivos criando diretorios conforme necessario
6. Oferece instalar pacotes npm faltantes

### `list`

Lista todos os componentes disponiveis com status de instalacao.

```bash
carf-ui list
```

Mostra cada componente com `[installed]` se o arquivo ja existe no diretorio destino.

## Componentes Disponiveis

### Utilitarios (Libraries)

| Nome | Descricao | Deps npm |
|------|-----------|----------|
| `cn` | Tailwind class merge (clsx + tailwind-merge) | clsx, tailwind-merge |
| `elevation` | Elevation/shadow cross-platform helper M3 | — |
| `theme` | Theme provider com presets e cores dinamicas | nativewind |

### Componentes UI

| Nome | Descricao | Deps internas | Deps npm |
|------|-----------|---------------|----------|
| `button` | M3 button com 8 variantes | cn | class-variance-authority |
| `icon-button` | Circular icon button M3 | cn, badge | class-variance-authority |
| `input` | Text input M3 outlined | cn | — |
| `checkbox` | Checkbox animado M3 | cn | lucide-react-native, react-native-reanimated |
| `switch` | Switch animado M3 | cn | react-native-reanimated |
| `avatar` | Avatar com imagem e fallback | cn | class-variance-authority |
| `badge` | Badge M3 com dot e counter | cn | class-variance-authority |
| `alert` | Alert tonal M3 | cn | class-variance-authority, lucide-react-native |
| `toast` | Snackbar M3 (3 arquivos) | cn | — |
| `dialog` | Modal dialog M3 | cn | — |
| `app-bar` | Top app bar M3, 4 variantes | cn, elevation | class-variance-authority, lucide-react-native, react-native-safe-area-context |
| `navigation-bar` | Bottom nav com pill animado | cn, elevation, badge | react-native-reanimated, react-native-safe-area-context, lucide-react-native, react-native-svg |
| `search-bar` | Search bar M3 com clear | cn | lucide-react-native, react-native-svg |
| `select` | Dropdown select com modal | cn, search-bar | lucide-react-native, react-native-svg, react-native-safe-area-context |
| `card` | Card M3, 3 variantes | cn, elevation | — |

## Arquivo de Configuracao

O `carf-ui.json` gerado pelo `init`:

```json
{
  "uiDir": "src/components/ui",
  "libDir": "src/lib",
  "themeDir": "src/theme",
  "theme": true,
  "packageManager": "bun"
}
```

| Campo | Descricao | Default |
|-------|-----------|---------|
| `uiDir` | Diretorio para componentes UI | `src/components/ui` |
| `libDir` | Diretorio para utilitarios (cn, elevation) | `src/lib` |
| `themeDir` | Diretorio para arquivos de tema | `src/theme` |
| `theme` | Se o tema foi incluido no init | `true` |
| `packageManager` | Package manager detectado | auto-detectado |

## Workflows Comuns

### Setup completo (novo projeto)

```bash
# 1. Inicializar com tema
carf-ui init
# Responder: y (incluir tema)

# 2. Adicionar componentes que precisa
carf-ui add button input icon-button dialog

# 3. Verificar o que foi instalado
carf-ui list
```

### Adicionar componente com dependencias

```bash
# select depende de search-bar, que sera adicionado automaticamente
carf-ui add select
# Output: Auto-resolved dependencies: cn, search-bar
```

### Setup sem tema

```bash
# 1. Inicializar sem tema
carf-ui init
# Responder: n (sem tema)

# 2. Adicionar componentes
carf-ui add button card
# Warning: componentes usam useThemeColors, ajustar imports manualmente
```

## Resolucao de Dependencias

O CLI resolve dependencias internas automaticamente. Ao adicionar `icon-button`, por exemplo:

1. `icon-button` depende de `cn` e `badge`
2. `badge` depende de `cn`
3. CLI adiciona: `cn` (utils.ts) + `badge` (Badge.tsx) + `icon-button` (IconButton.tsx)

Dependencias npm sao coletadas de todos os componentes resolvidos e o CLI oferece instala-las.

## Troubleshooting

**"carf-ui.json not found"**
Rode `carf-ui init` antes de usar `add`.

**"Unknown component"**
Use `carf-ui list` para ver nomes validos. Nomes usam kebab-case (ex: `icon-button`, `search-bar`, `navigation-bar`).

**Componente usa `useThemeColors` mas tema nao foi instalado**
Rode `carf-ui init` novamente com tema habilitado, ou instale o tema manualmente com `carf-ui add theme`.

**Conflito de versao em dependencia npm**
O CLI mostra versoes sugeridas mas nao forca. Ajuste versoes no package.json conforme necessidade do projeto.

**Arquivos ja existem**
O CLI mostra `[overwrite]` antes de sobrescrever e pede confirmacao. Use para atualizar componentes para versao mais recente.
