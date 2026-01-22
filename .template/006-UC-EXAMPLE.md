---
type: uc
status: approved
updated: 2026-01-22
---

# UC-001: Cadastrar Unidade Habitacional

## Atores

- Ator primario: Agente de Campo (field_agent)
- Atores secundarios: Sistema de Mapas, Servico de Armazenamento

## Pre-condicoes

- Usuario autenticado com role FIELD_AGENT ou superior
- Comunidade alvo ja cadastrada no sistema
- Dispositivo com GPS ativo (para captura de geometria)

## Fluxo Principal

1. Agente acessa modulo de cadastro de unidades
2. Sistema exibe formulario com campos obrigatorios destacados
3. Agente seleciona comunidade alvo na lista
4. Sistema carrega mapa centralizado na comunidade
5. Agente preenche dados basicos: tipo de uso, identificador
6. Agente desenha geometria do lote no mapa
7. Sistema calcula e exibe area automaticamente
8. Agente anexa foto da fachada
9. Agente confirma cadastro
10. Sistema valida dados e salva unidade com status DRAFT
11. Sistema exibe confirmacao com numero da unidade

## Fluxos Alternativos

**FA-01: Captura de geometria via GPS**
No passo 6, se agente preferir usar GPS:
1. Agente ativa modo de captura por caminhamento
2. Sistema registra pontos conforme agente percorre perimetro
3. Agente finaliza captura
4. Sistema fecha poligono e continua no passo 7

**FA-02: Geometria informada posteriormente**
No passo 6, se geometria nao disponivel:
1. Agente marca opcao "informar geometria depois"
2. Sistema permite continuar sem geometria
3. Fluxo continua no passo 8

## Pos-condicoes

- Unidade cadastrada com status DRAFT
- Geometria indexada espacialmente (se informada)
- Registro disponivel para sincronizacao
