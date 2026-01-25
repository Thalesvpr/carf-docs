---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
---

# RF-185: Editar Unidade Offline

## Descricao

Sistema deve permitir edicao de unidades territoriais existentes no modo offline, possibilitando que tecnicos em campo atualizem informacoes cadastrais, corrijam dados imprecisos, complementem atributos incompletos ou ajustem geometrias espaciais conforme verificacoes in loco. Edicoes persistidas imediatamente no banco SQLite local e unidade modificada recebe marcacao automatica de alteracao com flag e timestamp registrando momento da edicao. Sistema implementa mecanismo de deteccao de conflitos comparando timestamp de ultima atualizacao local com servidor durante sincronizacao subsequente, identificando edicoes simultaneas em diferentes dispositivos. Versao editada offline permanece disponivel localmente com indicacao visual de pendencia de sincronizacao.

## Criterios de Aceitacao

1. Edicao de todos os campos offline
2. Persistencia imediata em SQLite
3. Flag e timestamp de modificacao
4. Indicador visual de pendencia
5. Deteccao de conflitos por timestamp

## Rastreabilidade

- Modulos: REURBCAD
- Requisitos dependentes: RF-044, RF-184
