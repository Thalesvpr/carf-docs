---
type: workflow
status: approved
updated: 2026-02-07
part: 3
step: 14
---

# Passo 14: Carregamento do Mapa

App carrega mapa georreferenciado da area selecionada.

## Atores

- **Coordenador de Campo**: visualiza mapa da comunidade selecionada
- **Cadastrador de Campo**: visualiza mapa da regiao atribuida

## Fluxo

1. Mapa georreferenciado da area e carregado
2. Opcoes de visualizacao: usar ortofoto online (se houver conectividade) ou offline (pacote baixado)
3. Poligonos de quadras e lotes exibidos sobre a ortofoto

## Modos de Visualizacao

| Modo | Requisito | Descricao |
|------|-----------|-----------|
| ONLINE | Conectividade | Ortofoto via streaming |
| OFFLINE | Pacote baixado | Ortofoto local |

## Composicao da Tela

A tela exibe o mapa ocupando a area principal, com a ortofoto como camada base. Sobre ela, os poligonos de quadras e lotes sao renderizados (por exemplo, Quadra A com lotes L01 a L06). Na parte inferior, botoes de controle para GPS, camadas e zoom ficam disponiveis.

## Camadas do Mapa

| Camada | Conteudo |
|--------|----------|
| Base | Ortofoto georreferenciada |
| Comunidades | Poligonos de comunidades |
| Quadras | Poligonos de quadras |
| Lotes | Poligonos de lotes (com status) |
| GPS | Posicao atual do usuario |

## Diferenca por Role

| Elemento | Coordenador | Cadastrador |
|----------|-------------|-------------|
| Menu inferior | Visivel | Oculto |
| Mapa | Sim | Sim |
| Controles de mapa | Todos | Todos |

## Resultado

- Mapa carregado com ortofoto
- Poligonos visiveis sobre a ortofoto
- App pronto para navegacao e operacoes

## Proximo Passo

Passo 15: Fluxo Operacional em Campo
