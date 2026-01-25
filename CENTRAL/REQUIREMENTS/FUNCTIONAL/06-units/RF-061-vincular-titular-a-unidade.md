---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - REURBCAD
  - GEOAPI
---

# RF-061: Vincular Titular a Unidade

## Descricao

Sistema deve permitir que usuarios vinculem titulares a unidades habitacionais. Processo oferece duas modalidades: busca de titulares existentes por CPF ou nome, ou criacao inline de novo titular sem sair do formulario da unidade. Usuario deve especificar tipo de relacionamento obrigatorio (PROPRIETARIO, POSSUIDOR, USUFRUTUARIO, LOCATARIO, COMODATARIO, OUTRO). Busca oferece autocompletar com feedback quando titular com mesmo CPF ja existe. Opcao de marcar titular como principal para identificacao prioritaria.

## Criterios de Aceitacao

1. Busca de titulares existentes com autocompletar
2. Criacao inline de novo titular
3. Tipo de relacionamento obrigatorio
4. Opcao de marcar titular principal
5. Validacao de CPF duplicado com feedback

## Rastreabilidade

- Modulos: GEOWEB, REURBCAD, GEOAPI
- Requisitos dependentes: RF-049, RF-062
