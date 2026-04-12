---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-054: Campos Obrigatorios de Unidade

## Descricao

Sistema deve validar obrigatoriamente os campos essenciais ao cadastrar ou editar unidade habitacional: codigo unico de identificacao, endereco completo, comunidade a qual pertence, geometria espacial (coordenadas geograficas) e tipo de uso da unidade. Validacao ocorre tanto no momento do preenchimento quanto antes do salvamento, apresentando mensagens de erro claras para cada campo invalido ou ausente. Campos problematicos destacados visualmente.

## Criterios de Aceitacao

1. Validacao de codigo, endereco, comunidade e geometria
2. Validacao no preenchimento e antes de salvar
3. Mensagens de erro claras e especificas
4. Destaque visual de campos invalidos
5. Bloqueio de salvamento ate correcao

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-049
