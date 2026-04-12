---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-216: Editar Camada WMS/WMTS

## Descricao

Sistema deve possibilitar edicao de configuracoes de servicos WMS/WMTS previamente cadastrados atraves de formulario dedicado permitindo atualizacao de URL quando endpoint sofre mudancas, modificacao de layers consumidos, ajuste de estilos de renderizacao, e alteracao de parametros como opacidade, ordem e nome. Modificacoes passam por validacao automatica testando conectividade e verificando disponibilidade dos layers via GetCapabilities. Sistema mantem log detalhado de alteracoes com timestamp, administrador responsavel, campos alterados com valores anteriores e novos, proporcionando trilha de auditoria para troubleshooting e conformidade.

## Criterios de Aceitacao

1. Formulario de edicao completo
2. Validacao automatica de mudancas
3. GetCapabilities para verificar layers
4. Log de alteracoes com valores antes/depois
5. Identificacao de administrador responsavel

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-212, RF-214
