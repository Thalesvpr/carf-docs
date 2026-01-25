---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
  - GEOAPI
---

# RF-190: Deteccao de Conflitos

## Descricao

Sistema deve implementar mecanismo robusto de deteccao de conflitos que identifica situacoes onde mesmo registro foi editado simultaneamente no servidor central e localmente no dispositivo offline, cenario comum em projetos colaborativos com multiplas equipes. Deteccao utiliza comparacao de timestamps updated_at mantidos no registro local e no servidor, onde conflito e identificado quando timestamp do servidor e posterior ao timestamp da ultima sincronizacao mas registro tambem possui modificacoes locais nao sincronizadas. Ao detectar conflito, sistema nao sobrescreve automaticamente nenhuma versao para prevenir perda de dados, mas marca registro como em conflito e interrompe sincronizacao daquele item, permitindo que outros registros sejam processados normalmente. Interface dedicada exibe ambas as versoes lado a lado destacando campos divergentes.

## Criterios de Aceitacao

1. Comparacao de timestamps updated_at
2. Identificacao de edicoes concorrentes
3. Nao sobrescrever versoes automaticamente
4. Marcacao de registro em conflito
5. Exibicao de versoes lado a lado

## Rastreabilidade

- Modulos: REURBCAD, GEOAPI
- Requisitos dependentes: RF-185, RF-193
