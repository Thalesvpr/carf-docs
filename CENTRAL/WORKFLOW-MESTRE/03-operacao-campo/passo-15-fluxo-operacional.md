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

O app obtem posicao via GPS do dispositivo. A posicao e exibida no mapa em tempo real, e o usuario se orienta para chegar ao lote de destino.

### 15.2 Visualizacao de Estruturas

Comunidades, quadras e lotes ficam visiveis no mapa. Cores e icones indicam status de cada lote.

### 15.3 Selecao de Quadra e Lote

O usuario seleciona a quadra de interesse e depois o lote especifico, seguindo a hierarquia Comunidade, Quadra, Lote.

### 15.4 Identificacao Visual de Status

Cada lote exibe status por cores e icones:

| Cor | Status | Descricao |
|-----|--------|-----------|
| Verde | Cadastrado/Aprovado | Cadastro completo e aprovado |
| Amarelo | Pendente | Aguardando revisao |
| Vermelho | Rejeitado | Cadastro com problemas |
| Cinza | Nao visitado | Sem cadastro ainda |

### 15.5 Decisao de Acao no Lote

Usuario decide acao adequada para o lote selecionado:

| Acao | Descricao | Quando usar |
|------|-----------|-------------|
| Criacao | Novo cadastro | Lote sem cadastro |
| Edicao | Atualizar dados existentes | Corrigir informacoes |
| Movimentacao | Ajustar posicao | Geometria incorreta |
| Exclusao | Remover cadastro (com justificativa) | Cadastro indevido |

## Permissoes Identicas

Tanto Coordenador quanto Cadastrador podem navegar pelo mapa, selecionar lotes, criar/editar/mover/excluir cadastros e visualizar status dos lotes.

## Resultado

- Usuario localizado via GPS
- Lote selecionado para operacao
- Acao definida (criar/editar/mover/excluir)

## Proximo Passo

Passo 16: Pre-Formulario
