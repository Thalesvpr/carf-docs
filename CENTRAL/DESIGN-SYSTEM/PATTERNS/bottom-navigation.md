---
type: pattern
status: approved
updated: 2026-02-07
platform: mobile
---

# Bottom Navigation

Menu de navegacao inferior presente apenas para Coordenadores de Campo no app REURBCAD.

## Definicao

O Bottom Navigation e um padrao de navegacao mobile que exibe um menu fixo na parte inferior da tela, permitindo acesso rapido as principais areas do aplicativo.

## Regra de Exibicao

| Role | Bottom Navigation |
|------|-------------------|
| **Coordenador (field-coordinator)** | VISIVEL |
| **Cadastrador (field-cadastrator)** | OCULTO |

## Itens do Menu

| Icone | Label | Destino | Descricao |
|-------|-------|---------|-----------|
| 🏠 | Home | Dashboard | Metricas e visao geral |
| 🗺️ | Mapa | Mapa | Navegacao geografica |
| 👥 | Equipe | Lista membros | Gerenciamento de equipe |
| ⚙️ | Perfil | Configuracoes | Dados do usuario |

## Interface - Coordenador

```
┌─────────────────────────────────────┐
│                                     │
│           CONTEUDO DA TELA          │
│                                     │
│                                     │
├─────────────────────────────────────┤
│  🏠      🗺️       👥       ⚙️        │
│ Home    Mapa   Equipe   Perfil     │
└─────────────────────────────────────┘
```

## Interface - Cadastrador

```
┌─────────────────────────────────────┐
│                                     │
│           MAPA                      │
│     (tela inicial e unica          │
│      navegacao principal)           │
│                                     │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

O Cadastrador abre o app e vai **direto para o mapa** da regiao atribuida. Nao ha menu inferior.

## Funcionalidades por Aba

### Home (Coordenador)

- Metricas de produtividade da equipe
- Cadastros realizados hoje/semana/mes
- Lotes pendentes na regiao
- Alertas e notificacoes

### Mapa (Ambos)

- Visualizacao geografica da regiao
- Selecao de lotes para cadastro
- Status visual por cores

### Equipe (Coordenador)

- Lista de membros da equipe
- Produtividade individual de cada cadastrador
- Status de cada membro (online/offline)
- Contato direto com membros

### Perfil (Coordenador)

- Dados do usuario
- Configuracoes do app
- Logout

## Justificativa

A diferenciacao de interface entre Coordenador e Cadastrador segue o principio de **interface minimalista**:

- **Coordenador**: Precisa de visao gerencial, metricas e acesso a equipe
- **Cadastrador**: Foco exclusivo na execucao de cadastros, sem distracao

## Implementacao

```typescript
// Verificar role para exibir Bottom Navigation
const showBottomNav = user.role === 'field-coordinator';

// Tela inicial por role
const initialScreen = user.role === 'field-coordinator'
  ? 'Home'
  : 'Map';
```

## Referencia

- Roles: `CENTRAL/DOMAIN-RULES/WORKFLOWS/03-role-permissions.md`
- Atores: `CENTRAL/WORKFLOW-MESTRE/05-conceitos-glossario/atores.md`
- Passo 13 (selecao): `CENTRAL/WORKFLOW-MESTRE/03-operacao-campo/passo-13-selecao.md`
