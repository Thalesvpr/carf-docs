---
id: UC-004-FE-003
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-004-FE-003: Bateria Baixa

Fluxo de excecao do UC-004 quando bateria atinge nivel critico.

## Condicao

Em qualquer momento do UC-004, app detecta bateria abaixo de 15%.

## Fluxo

1. Sistema detecta bateria baixa
2. Sistema exibe notificacao persistente
3. Sistema oferece ativar modo economia
4. FIELD_AGENT escolhe acao

## Modo Economia

- Desabilita GPS tracking continuo (apenas captura pontual)
- Reduz frequencia de refresh do mapa
- Desabilita sincronizacao automatica em background
- Reduz brilho da tela
- Ativa auto-save a cada mudanca de campo

## Bateria Critica (abaixo de 5%)

- Sistema forca salvamento da unidade atual
- Sistema marca unidade como incompleta se necessario
- Sistema exibe modal de emergencia
- Sistema fecha app gracefully apos salvamento

## Retorno

Modo economia ativo. FIELD_AGENT continua com limitacoes ou salva e encerra.
