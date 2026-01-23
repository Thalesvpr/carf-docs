---
id: UC-004-FE-001
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-004-FE-001: GPS Nao Disponivel

Fluxo de excecao do UC-004 quando GPS esta desabilitado ou sem permissao.

## Condicao

No passo 5 do UC-004, app detecta que GPS esta desabilitado ou permissao foi negada.

## Fluxo

1. Sistema detecta GPS indisponivel
2. Sistema exibe modal de alerta
3. Sistema oferece opcoes ao usuario
4. FIELD_AGENT escolhe acao

## Acoes Disponiveis

- **Habilitar GPS**: Abre configuracoes do sistema para ativar GPS
- **Continuar Sem GPS**: Prossegue com limitacoes (desenho manual obrigatorio)
- **Cancelar**: Aborta criacao da unidade

## Limitacoes Sem GPS

- Localizacao aproximada baseada em ultimo ponto conhecido
- Opcao Caminhar Perimetro desabilitada
- Unidade marcada com flag de baixa precisao
- Observacao automatica para revisao posterior

## Retorno

Se habilitar GPS, retorna ao passo 5. Se continuar sem, prossegue com limitacoes.
