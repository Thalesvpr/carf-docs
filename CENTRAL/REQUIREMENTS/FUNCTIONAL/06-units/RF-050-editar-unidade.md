---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-050: Editar Unidade

## Descricao

Usuarios com roles ANALYST e MANAGER podem editar dados de unidades existentes. Edicao de campos cadastrais permite atualizacao de endereco, tipo, area, nomes de titulares e documentos anexados com validacoes garantindo integridade. Edicao de geometria no mapa utilizando ferramentas interativas permitindo mover, redimensionar ou redesenhar poligono. ANALYST pode editar apenas unidades em status DRAFT ou CHANGES_REQUESTED. Log automatico de alteracoes registra todas modificacoes para auditoria.

## Criterios de Aceitacao

1. Edicao de campos alfanumericos com validacao
2. Edicao de geometria com ferramentas interativas
3. Restricao por status para role ANALYST
4. Log de auditoria com campos e valores alterados
5. Recalculo automatico de area apos modificacao geometrica

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-049, RF-056
