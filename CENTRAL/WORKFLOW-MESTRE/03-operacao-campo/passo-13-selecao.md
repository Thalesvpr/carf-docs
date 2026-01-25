---
type: workflow
status: approved
updated: 2026-01-25
part: 3
step: 13
---

# Passo 13: Selecao de Comunidade

Agente de Campo seleciona a comunidade para o periodo de atuacao.

## Fluxo

1. Agente de Campo visualiza lista de comunidades liberadas
2. Agente de Campo seleciona comunidade para o periodo de atuacao
3. App carrega dados especificos da comunidade selecionada

## Interface

```
┌─────────────────────────────┐
│  SELECIONAR COMUNIDADE      │
├─────────────────────────────┤
│  ○ Comunidade Vila Nova     │
│  ○ Comunidade Jardim Azul   │
│  ● Comunidade Boa Vista     │
│  ○ Comunidade Sao Jose      │
└─────────────────────────────┘
        [CONTINUAR]
```

## Dados Carregados

Ao selecionar uma comunidade, o app carrega:
- Poligono da comunidade
- Quadras dentro da comunidade
- Lotes dentro de cada quadra
- Status de cada lote
- Historico de visitas anteriores

## Resultado

- Comunidade selecionada
- Dados da comunidade carregados
- App pronto para navegacao no mapa

## Proximo Passo

Passo 14: Carregamento do Mapa
