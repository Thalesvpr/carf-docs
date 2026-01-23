---
id: UC-004-FE-002
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-004-FE-002: Memoria Cheia

Fluxo de excecao do UC-004 quando armazenamento do dispositivo esta insuficiente.

## Condicao

No passo 9 do UC-004, app detecta espaco insuficiente para salvar novas fotos.

## Fluxo

1. Sistema detecta armazenamento insuficiente
2. Sistema exibe modal de alerta com espaco disponivel
3. Sistema oferece opcoes para liberar espaco
4. FIELD_AGENT escolhe acao

## Acoes Disponiveis

- **Sincronizar Pendencias**: Envia dados para servidor e libera espaco local
- **Gerenciar Fotos**: Abre listagem para deletar fotos desnecessarias
- **Limpar Cache**: Remove tiles de mapa e arquivos temporarios
- **Cancelar**: Impede novas fotos mas permite salvar unidade sem fotos adicionais

## Retorno

Apos liberar espaco, FIELD_AGENT pode continuar tirando fotos.

## Pos-condicoes

- Espaco de armazenamento liberado
- Warning preventivo exibido quando uso acima de 80%
