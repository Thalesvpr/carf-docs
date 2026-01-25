---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-077: Campos Personalizados de Unidade

## Descricao

Sistema deve permitir que usuarios ADMIN criem campos customizados por tenant estendendo modelo de unidade habitacional. Definicao de campos inclui tipo de dado (texto, numero, data, select, booleano) e configuracoes de validacao. Cada campo pode ter validacoes especificas como obrigatoriedade, valores minimos e maximos, formatos via regex e listas de opcoes para select. Interface de formulario exibe dinamicamente campos customizados renderizando controles apropriados e aplicando validacoes client-side e server-side.

## Criterios de Aceitacao

1. Criacao de campos por ADMIN
2. Tipos: texto, numero, data, select, booleano
3. Validacoes configuráveis por campo
4. Renderizacao dinamica no formulario
5. Isolamento de campos por tenant

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-049
