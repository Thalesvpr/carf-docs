---
id: UC-005-FE-004
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-005-FE-004: Espaco Insuficiente (Pull)

Fluxo de excecao do UC-005 quando nao ha espaco para baixar atualizacoes do servidor.

## Condicao

Na fase PULL do UC-005, app detecta espaco insuficiente para armazenar dados baixados.

## Fluxo

1. App recebe tamanho estimado dos dados a baixar
2. App verifica espaco disponivel no dispositivo
3. App detecta espaco insuficiente
4. App exibe modal com opcoes

## Acoes Disponiveis

- **Liberar Espaco**: Abre gerenciador de armazenamento do sistema
- **Sincronizar Apenas Enviar**: Executa apenas PUSH enviando dados locais
- **Limpar Cache**: Remove tiles de mapa e arquivos temporarios
- **Cancelar**: Aborta sincronizacao

## Retorno

Apos liberar espaco, FIELD_AGENT retenta e PULL completa normalmente.

## Pos-condicoes

- Espaco liberado por uma das acoes
- Sincronizacao pode ser retomada
