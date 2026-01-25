---
type: workflow
status: approved
updated: 2026-01-25
part: 3
step: 16
---

# Passo 16: Pre-Formulario

Agente define parametros iniciais antes do cadastro completo.

## Fluxo

1. Agente escolhe a acao (criar/editar/mover/excluir)
2. App exibe pre-formulario
3. Agente define unidade e status inicial
4. Validacoes basicas executadas

## Interface

```
┌─────────────────────────────┐
│  PRE-FORMULARIO             │
├─────────────────────────────┤
│  Acao: [Criar cadastro ▼]   │
│                             │
│  Tipo de Unidade:           │
│  ○ Residencial              │
│  ● Comercial                │
│  ○ Misto                    │
│  ○ Vazio                    │
│                             │
│  Status Inicial:            │
│  [Em atendimento ▼]         │
│                             │
│  [CANCELAR]  [CONTINUAR]    │
└─────────────────────────────┘
```

## Opcoes de Acao

| Acao | Descricao |
|------|-----------|
| Criar cadastro | Novo registro de lote |
| Editar cadastro | Modificar registro existente |
| Mover geometria | Ajustar posicao do lote |
| Excluir cadastro | Remover registro (requer justificativa) |

## Tipos de Unidade

| Tipo | Descricao |
|------|-----------|
| Residencial | Uso exclusivo para moradia |
| Comercial | Uso exclusivo comercial |
| Misto | Uso residencial e comercial |
| Vazio | Lote sem construcao |

## Validacoes

- Acao selecionada
- Tipo de unidade definido
- Status inicial compativel com acao

## Resultado

- Parametros iniciais definidos
- App pronto para formulario completo

## Proximo Passo

Passo 17: Formulario Completo
