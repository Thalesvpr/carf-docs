---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
---

# RF-194: Limpeza de Dados Locais

## Descricao

Sistema deve oferecer funcionalidade de limpeza de cache permitindo ao usuario liberar espaco de armazenamento do dispositivo removendo dados sincronizados que nao precisam mais estar disponiveis offline, especialmente util quando tecnico conclui trabalho em uma comunidade e prepara dispositivo para outra localidade. Logica inteligente preserva automaticamente dados nao sincronizados, garantindo que trabalho pendente nunca seja perdido inadvertidamente. Dialogo de confirmacao obrigatoria alerta sobre acao irreversivel listando quantidade de registros a serem removidos e espaco a ser liberado, incluindo advertencia sobre necessidade de sincronizacao previa. Apos confirmacao, dados sincronizados removidos do SQLite e arquivos de midia deletados do sistema de arquivos liberando espaco para novo download de tenant.

## Criterios de Aceitacao

1. Funcao de limpeza de cache
2. Preservacao automatica de dados nao sincronizados
3. Dialogo de confirmacao obrigatoria
4. Listagem de registros e espaco a liberar
5. Remocao de SQLite e arquivos de midia

## Rastreabilidade

- Modulos: REURBCAD
- Requisitos dependentes: RF-182, RF-183
