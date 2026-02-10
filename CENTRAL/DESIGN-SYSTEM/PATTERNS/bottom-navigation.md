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

| Label | Destino | Descricao |
|-------|---------|-----------|
| Home | Dashboard | Metricas e visao geral |
| Mapa | Mapa | Navegacao geografica |
| Equipe | Lista membros | Gerenciamento de equipe |
| Perfil | Configuracoes | Dados do usuario |

## Interface - Coordenador

A tela do Coordenador exibe o conteudo principal na area central e, na parte inferior, uma barra fixa de navegacao com quatro abas: Home, Mapa, Equipe e Perfil.

## Interface - Cadastrador

O Cadastrador abre o app e vai direto para o mapa da regiao atribuida. Nao ha menu inferior. O mapa e a tela inicial e unica navegacao principal.

## Funcionalidades por Aba

**Home (Coordenador):** Metricas de produtividade da equipe, cadastros realizados hoje/semana/mes, lotes pendentes na regiao, alertas e notificacoes.

**Mapa (Ambos):** Visualizacao geografica da regiao, selecao de lotes para cadastro, status visual por cores.

**Equipe (Coordenador):** Lista de membros da equipe, produtividade individual de cada cadastrador, status de cada membro (online/offline), contato direto com membros.

**Perfil (Coordenador):** Dados do usuario, configuracoes do app, logout.

## Justificativa

A diferenciacao de interface entre Coordenador e Cadastrador segue o principio de interface minimalista. Coordenador precisa de visao gerencial, metricas e acesso a equipe. Cadastrador tem foco exclusivo na execucao de cadastros, sem distracao.

## Logica de Exibicao

O Bottom Navigation e exibido condicionalmente com base na role do usuario. Se a role for field-coordinator, o menu inferior fica visivel e a tela inicial e Home. Se a role for field-cadastrator, o menu inferior fica oculto e a tela inicial e o Mapa.

## Referencia

- Roles: CENTRAL/DOMAIN-RULES/WORKFLOWS/03-role-permissions.md
- Atores: CENTRAL/WORKFLOW-MESTRE/05-conceitos-glossario/atores.md
- Passo 13 (selecao): CENTRAL/WORKFLOW-MESTRE/03-operacao-campo/passo-13-selecao.md
