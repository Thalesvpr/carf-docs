---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-101: Mesclar Titulares Duplicados

## Descricao

Sistema deve permitir que usuarios ADMIN mesclem titulares duplicados consolidando em unico registro. Interface oferece selecao de multiplos titulares suspeitos via checkboxes ou ferramenta de deteccao de duplicatas por similaridade. Wizard apresenta comparacao lado-a-lado para escolha de valores por campo. Vinculacoes com unidades transferidas automaticamente para titular consolidado com deduplicacao de vinculos redundantes. Duplicados originais inativados via soft delete preservando rastreabilidade.

## Criterios de Aceitacao

1. Selecao de multiplos titulares para mesclar
2. Wizard de comparacao lado-a-lado
3. Transferencia automatica de vinculos
4. Soft delete dos duplicados originais
5. Restrito a perfil ADMIN

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-084, RF-079
