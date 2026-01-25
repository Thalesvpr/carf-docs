---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-215: Listar Camadas WMS/WMTS

## Descricao

Sistema deve fornecer interface administrativa de listagem exibindo todos os servicos WMS/WMTS configurados em tabela com colunas URL do servidor, nome amigavel, tipo de servico (WMS ou WMTS), layers consumidos, status (ativo/inativo) e data de ultima validacao. Edicao inline permite modificar atributos simples como nome ou opacidade diretamente na tabela. Toggle switch de ativacao/desativacao controla visibilidade para usuarios finais sem excluir configuracao. Interface oferece filtragem por tipo de servico ou status, busca textual por nome ou URL, e ordenacao por qualquer coluna, facilitando gestao de catalogos extensos de multiplas fontes externas.

## Criterios de Aceitacao

1. Tabela com URL, nome, tipo e status
2. Edicao inline de atributos simples
3. Toggle de ativacao/desativacao
4. Filtros e busca textual
5. Ordenacao por qualquer coluna

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-212, RF-213
