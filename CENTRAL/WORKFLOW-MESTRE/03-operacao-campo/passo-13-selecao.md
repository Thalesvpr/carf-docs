---
type: workflow
status: approved
updated: 2026-02-07
part: 3
step: 13
---

# Passo 13: Selecao de Comunidade

**SOMENTE Coordenador de Campo** seleciona a comunidade para o periodo de atuacao.

## Regra Critica

| Role | Comportamento |
|------|---------------|
| **Coordenador (field-coordinator)** | Seleciona comunidade no app |
| **Cadastrador (field-cadastrator)** | NAO seleciona - recebe atribuicao do Admin/Manager via backend |

## Fluxo - Coordenador

1. Coordenador visualiza lista de comunidades liberadas
2. Coordenador seleciona comunidade para o periodo de atuacao
3. App carrega dados especificos da comunidade selecionada

## Fluxo - Cadastrador

1. Cadastrador abre o app
2. App carrega automaticamente a regiao atribuida pelo Admin/Manager
3. NAO ha tela de selecao - vai direto pro mapa

## Interface

A tela do Coordenador exibe uma lista de comunidades disponiveis (como Vila Nova, Jardim Azul, Boa Vista, Sao Jose) com selecao por radio button e botao Continuar. O Cadastrador nao ve essa tela e abre diretamente o mapa da regiao atribuida pelo Admin.

## Diferenca de UI

| Elemento | Coordenador | Cadastrador |
|----------|-------------|-------------|
| Tela inicial | Lista de comunidades | Mapa direto |
| Bottom Navigation | SIM | NAO |
| Selecao de regiao | SIM | NAO |

## Dados Carregados

Ao acessar uma comunidade (por selecao ou atribuicao), o app carrega:
- Poligono da comunidade
- Quadras dentro da comunidade
- Lotes dentro de cada quadra
- Status de cada lote
- Historico de visitas anteriores

## Resultado

- Comunidade ativa definida
- Dados da comunidade carregados
- App pronto para navegacao no mapa

## Proximo Passo

Passo 14: Carregamento do Mapa
