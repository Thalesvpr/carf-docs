---
status: approved
updated: 2026-01-20
---

# Mapeamento Tela-Componentes

Documentacao de quais componentes @carf/ui sao usados em cada tela das aplicacoes CARF.

## GEOWEB

### Tela: Dashboard

**Rota:** `/dashboard`

| Componente | Uso | Quantidade |
|:-----------|:----|:-----------|
| Card | Metricas (unidades, posseiros, pendentes) | 4 |
| Badge | Contadores em cards | 4 |
| Button | Acoes rapidas | 2-3 |

### Tela: Listagem de Unidades

**Rota:** `/units`

| Componente | Uso | Quantidade |
|:-----------|:----|:-----------|
| Table | Listagem principal | 1 |
| Input | Busca por codigo/endereco | 1 |
| Select | Filtro de status | 1 |
| Select | Filtro de comunidade | 1 |
| Button | Nova Unidade | 1 |
| StatusBadge | Status em cada linha | N |
| DropdownMenu | Acoes por linha | N |
| Dialog | Confirmacao de exclusao | 1 |
| Toast | Feedback de acoes | - |

### Tela: Cadastro/Edicao de Unidade

**Rota:** `/units/new`, `/units/:id/edit`

| Componente | Uso | Quantidade |
|:-----------|:----|:-----------|
| Card | Container do formulario | 1 |
| Input | Codigo, endereco, area | 3+ |
| Label | Labels dos campos | N |
| Select | Comunidade, status | 2 |
| Textarea | Observacoes | 1 |
| Button | Salvar, Cancelar | 2 |
| Tabs | Dados, Posseiros, Documentos | 1 |
| HolderCard | Lista de posseiros vinculados | N |
| Dialog | Vincular posseiro | 1 |
| Toast | Feedback de salvamento | - |

### Tela: Detalhe de Unidade

**Rota:** `/units/:id`

| Componente | Uso | Quantidade |
|:-----------|:----|:-----------|
| Card | Container principal | 1 |
| Tabs | Dados, Posseiros, Documentos, Historico | 1 |
| StatusBadge | Status atual | 1 |
| HolderCard | Posseiros vinculados | N |
| Button | Editar, Excluir | 2 |
| Badge | Tags/categorias | N |
| Accordion | Historico de alteracoes | 1 |

### Tela: Listagem de Posseiros

**Rota:** `/holders`

| Componente | Uso | Quantidade |
|:-----------|:----|:-----------|
| Table | Listagem principal | 1 |
| Input | Busca por nome/CPF | 1 |
| Button | Novo Posseiro | 1 |
| DropdownMenu | Acoes por linha | N |
| Dialog | Confirmacao de exclusao | 1 |

### Tela: Cadastro/Edicao de Posseiro

**Rota:** `/holders/new`, `/holders/:id/edit`

| Componente | Uso | Quantidade |
|:-----------|:----|:-----------|
| Card | Container do formulario | 1 |
| Input | Nome, CPF, email, telefone | 4+ |
| Label | Labels dos campos | N |
| Checkbox | Pessoa juridica? | 1 |
| Button | Salvar, Cancelar | 2 |
| UnitCard | Unidades vinculadas | N |
| Toast | Feedback | - |

### Tela: Comunidades

**Rota:** `/communities`

| Componente | Uso | Quantidade |
|:-----------|:----|:-----------|
| CommunityCard | Cards de comunidades | N |
| Input | Busca | 1 |
| Button | Nova Comunidade | 1 |
| Select | Filtro de status | 1 |

## ADMIN

### Tela: Dashboard Administrativo

**Rota:** `/admin/dashboard`

| Componente | Uso | Quantidade |
|:-----------|:----|:-----------|
| Card | Metricas do sistema | 4-6 |
| Progress | Uso de recursos | 2-3 |

### Tela: Gestao de Usuarios

**Rota:** `/admin/users`

| Componente | Uso | Quantidade |
|:-----------|:----|:-----------|
| Table | Lista de usuarios | 1 |
| Input | Busca | 1 |
| Button | Novo Usuario | 1 |
| Badge | Roles do usuario | N |
| Dialog | Edicao de usuario | 1 |
| Checkbox | Permissoes | N |
| AlertDialog | Desativar usuario | 1 |

### Tela: Gestao de Comunidades

**Rota:** `/admin/communities`

| Componente | Uso | Quantidade |
|:-----------|:----|:-----------|
| Table | Lista de comunidades | 1 |
| CommunityCard | Preview em modal | 1 |
| Dialog | CRUD comunidade | 1 |
| Input | Nome, cidade | 2+ |
| Select | Estado, status | 2 |
| Switch | Status ativo | 1 |

### Tela: Configuracoes

**Rota:** `/admin/settings`

| Componente | Uso | Quantidade |
|:-----------|:----|:-----------|
| Tabs | Categorias de config | 1 |
| Card | Grupos de configuracao | N |
| Switch | Toggles de features | N |
| Input | Valores de config | N |
| Button | Salvar | 1 |
| Toast | Feedback | - |

## Keycloak Theme

### Tela: Login

**Rota:** `/realms/{realm}/account`

| Componente | Uso | Quantidade |
|:-----------|:----|:-----------|
| Card | Container do form | 1 |
| Input | Usuario/Email | 1 |
| Input | Senha | 1 |
| Label | Labels dos campos | 2 |
| Checkbox | Lembrar-me | 1 |
| Button | Entrar | 1 |
| Alert | Mensagens de erro | 0-1 |

### Tela: Registro

**Rota:** `/realms/{realm}/protocol/openid-connect/registrations`

| Componente | Uso | Quantidade |
|:-----------|:----|:-----------|
| Card | Container | 1 |
| Input | Nome, Email, Senha, Confirmar | 4 |
| Label | Labels | 4 |
| Checkbox | Aceito termos | 1 |
| Button | Registrar | 1 |
| Alert | Erros de validacao | 0-1 |

### Tela: Recuperar Senha

**Rota:** `/realms/{realm}/login-actions/reset-credentials`

| Componente | Uso | Quantidade |
|:-----------|:----|:-----------|
| Card | Container | 1 |
| Input | Email | 1 |
| Label | Label | 1 |
| Button | Enviar | 1 |
| Alert | Feedback | 0-1 |

## Resumo de Uso

| Componente | GEOWEB | ADMIN | Keycloak | Total Telas |
|:-----------|:------:|:-----:|:--------:|:-----------:|
| Button | 10 | 6 | 3 | 19 |
| Input | 8 | 5 | 6 | 19 |
| Card | 6 | 5 | 3 | 14 |
| Table | 3 | 2 | 0 | 5 |
| Select | 5 | 2 | 0 | 7 |
| Dialog | 4 | 2 | 0 | 6 |
| Toast | 5 | 3 | 0 | 8 |
| StatusBadge | 4 | 0 | 0 | 4 |
| Tabs | 3 | 2 | 0 | 5 |
| Label | 3 | 2 | 7 | 12 |
| Badge | 3 | 2 | 0 | 5 |
| UnitCard | 2 | 0 | 0 | 2 |
| HolderCard | 2 | 0 | 0 | 2 |
| CommunityCard | 1 | 2 | 0 | 3 |
| Checkbox | 1 | 2 | 2 | 5 |
| Alert | 0 | 0 | 3 | 3 |
