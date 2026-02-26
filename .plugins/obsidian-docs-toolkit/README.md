# CARF Documentation Manager

Plugin para Obsidian que gerencia documentação CARF com validação automática, gerenciamento de metadados via YAML frontmatter, e dashboard centralizado.

## Features

### Dashboard Centralizado
- Visualização de todos os documentos por status (review, approved, rejected)
- Lista de todos os problemas de validação agrupados por validator
- Filtros por severidade (errors, warnings, info)
- Click para navegar diretamente ao problema

### Metadata Estruturado (YAML Frontmatter)
```yaml
---
id: RF-001
type: RF
modules: [GEOAPI, REURBWEB]
epic: authentication
status: review
created: 2026-01-15
updated: 2026-01-19
---
```

### Validators (8 essenciais)

| Validator | Severidade | Descrição |
|-----------|------------|-----------|
| `broken-links` | ERROR | Links que apontam para arquivos inexistentes |
| `frontmatter` | ERROR | Campos obrigatórios no frontmatter |
| `orphans` | WARN | Arquivos sem nenhum link apontando para eles |
| `structure` | WARN | Seções obrigatórias por tipo |
| `title` | ERROR | H1 deve seguir padrão (# RF-001: Título) |
| `stale` | INFO | Arquivos não atualizados há >6 meses |
| `empty-folders` | WARN | Pastas com README mas sem conteúdo |
| `naming` | ERROR | Arquivos sem prefixo numérico correto |

### Commands

| Command | Hotkey | Descrição |
|---------|--------|-----------|
| `CARF: Init Metadata` | - | Cria frontmatter padrão no arquivo atual |
| `CARF: Migrate Footer` | - | Migra footer antigo para frontmatter |
| `CARF: Migrate All Footers` | - | Migra todos os footers do vault |
| `CARF: Validate File` | `Ctrl+Shift+V` | Valida arquivo atual |
| `CARF: Validate All` | - | Valida todo o vault |
| `CARF: Approve` | `Ctrl+Shift+A` | Marca como approved |
| `CARF: Reject` | `Ctrl+Shift+R` | Marca como rejected |
| `CARF: Sync Index` | - | Atualiza README da pasta atual |
| `CARF: Sync All Indexes` | - | Atualiza todos os READMEs |
| `CARF: Open Dashboard` | - | Abre o dashboard |

### Automações

- **On Save**: Atualiza timestamp `updated`, roda validação local
- **On Create**: Detecta novos arquivos CARF
- **On Rename/Delete**: Atualiza índices de README afetados
- **On Vault Open**: Roda validação global em background

### Status Bar

Mostra estatísticas rápidas: `CARF: ✓ 32 | ✗ 5 | ○ 860 | ! 47 issues`

## Instalação

### Desenvolvimento

1. Clone este repositório na pasta `.plugins` do seu vault:
   ```bash
   cd /path/to/vault/.plugins
   git clone <repo-url> obsidian-carf
   ```

2. Instale dependências:
   ```bash
   cd obsidian-carf
   npm install
   ```

3. Build:
   ```bash
   npm run build
   ```

4. Ative o plugin no Obsidian (Settings > Community Plugins)

### Build de Desenvolvimento

Para desenvolvimento com hot-reload:
```bash
npm run dev
```

## Migração do Sistema Atual

Se você já tem documentos com footer de metadata no formato antigo:

1. Instale o plugin
2. Execute o comando `CARF: Migrate All Footers`
3. Revise os arquivos migrados
4. Configure os validators nas Settings

## Configuração

Acesse Settings > CARF Plugin Settings para:

- **Paths**: Configurar caminhos CENTRAL e PROJECTS
- **Automation**: Ativar/desativar automações
- **Validators**: Habilitar/desabilitar validators específicos
- **Stale Threshold**: Configurar período para marcar documentos como stale

## Estrutura do Projeto

```
obsidian-carf/
├── manifest.json
├── main.ts                      # Entry point
├── styles.css
│
├── src/
│   ├── settings.ts              # Configurações do plugin
│   │
│   ├── models/
│   │   ├── Document.ts          # Documento parseado
│   │   ├── Issue.ts             # Problema de validação
│   │   └── types.ts             # Enums e interfaces
│   │
│   ├── services/
│   │   ├── MetadataService.ts   # CRUD de frontmatter
│   │   ├── ValidationService.ts # Orquestra validadores
│   │   ├── IndexService.ts      # Gera índices de README
│   │   └── MigrationService.ts  # Migra footer → frontmatter
│   │
│   ├── validators/
│   │   ├── Validator.ts         # Interface base
│   │   └── *.ts                 # 8 validators
│   │
│   ├── views/
│   │   └── DashboardView.ts     # Painel principal
│   │
│   └── commands/
│       └── *.ts                 # Commands
```

## Licença

MIT
