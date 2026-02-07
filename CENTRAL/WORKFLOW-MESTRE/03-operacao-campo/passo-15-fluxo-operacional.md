---
type: workflow
status: approved
updated: 2026-02-07
part: 3
step: 15
---

# Passo 15: Fluxo Operacional em Campo

Com o mapa carregado, Coordenador e Cadastrador executam operacoes no territorio.

## Atores

- **Coordenador de Campo**: executa operacoes + ve metricas
- **Cadastrador de Campo**: executa operacoes

## Sub-passos

### 15.1 Orientacao por GPS

- App obtem posicao via GPS do dispositivo
- Posicao exibida no mapa em tempo real
- Usuario se orienta para chegar ao local correto

```
┌──────────────────────┐
│   MAPA               │
│      ·───> destino   │
│     /                │
│    📍                 │
│  (sua posicao)       │
└──────────────────────┘
```

### 15.2 Visualizacao de Estruturas

- Comunidades, quadras e lotes visiveis no mapa
- Cores e icones indicam status de cada lote

### 15.3 Selecao de Quadra e Lote

- Usuario seleciona quadra de interesse
- Usuario seleciona lote especifico para operacao

```
Comunidade > Quadra A > Lote 001
```

### 15.4 Identificacao Visual de Status

Cada lote exibe status por cores e icones:

| Cor | Status | Descricao |
|-----|--------|-----------|
| 🟢 Verde | Cadastrado/Aprovado | Cadastro completo e aprovado |
| 🟡 Amarelo | Pendente | Aguardando revisao |
| 🔴 Vermelho | Rejeitado | Cadastro com problemas |
| ⚪ Cinza | Nao visitado | Sem cadastro ainda |

### 15.5 Decisao de Acao no Lote

Usuario decide acao adequada para o lote selecionado:

| Acao | Descricao | Quando usar |
|------|-----------|-------------|
| **Criacao** | Novo cadastro | Lote sem cadastro |
| **Edicao** | Atualizar dados existentes | Corrigir informacoes |
| **Movimentacao** | Ajustar posicao | Geometria incorreta |
| **Exclusao** | Remover cadastro (com justificativa) | Cadastro indevido |

## Permissoes Identicas

Tanto Coordenador quanto Cadastrador podem:
- Navegar pelo mapa
- Selecionar lotes
- Criar/editar/mover/excluir cadastros
- Visualizar status dos lotes

## Resultado

- Usuario localizado via GPS
- Lote selecionado para operacao
- Acao definida (criar/editar/mover/excluir)

## Proximo Passo

Passo 16: Pre-Formulario
