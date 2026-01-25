---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-076: Numeracao Automatica de Unidades

## Descricao

Sistema deve oferecer geracao automatica de codigos identificadores para unidades seguindo padrao configuravel por tenant. Template de numeracao pode incluir prefixos, codigos hierarquicos (comunidade-quadra-unidade) e contadores sequenciais resultando em codigos como C001-Q01-U001. Geracao utiliza sequencias de banco de dados garantindo unicidade em cenarios de cadastramento concorrente. Usuarios mantem opcao de override manual para especificacao de codigo customizado quando necessario.

## Criterios de Aceitacao

1. Template configuravel por tenant
2. Codigos hierarquicos com prefixos
3. Sequencias atomicas para unicidade
4. Override manual permitido
5. Incremento sequencial automatico

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-049, RF-054
