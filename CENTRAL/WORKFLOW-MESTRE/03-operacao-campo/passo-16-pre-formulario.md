---
type: workflow
status: approved
updated: 2026-02-07
part: 3
step: 16
---

# Passo 16: Pre-Formulario

Coordenador ou Cadastrador define parametros iniciais antes do cadastro completo.

## Atores

- **Coordenador de Campo**: preenche pre-formulario
- **Cadastrador de Campo**: preenche pre-formulario

## Fluxo

1. Usuario escolhe a acao (criar/editar/mover/excluir)
2. App exibe pre-formulario
3. Usuario define unidade e status inicial
4. Validacoes basicas executadas

## Interface

A tela de pre-formulario exibe um dropdown para selecao de acao (Criar cadastro, Editar, Mover, Excluir), radio buttons para tipo de unidade (Residencial, Comercial, Misto, Vazio), dropdown para status inicial e botoes Cancelar e Continuar.

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
