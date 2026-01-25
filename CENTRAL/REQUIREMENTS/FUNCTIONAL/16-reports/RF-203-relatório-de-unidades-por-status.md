---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-203: Relatorio de Unidades por Status

## Descricao

Sistema deve gerar relatorio consolidado que agrega unidades territoriais por status de aprovacao, apresentando visao quantitativa da distribuicao cadastral atraves de contagens e percentuais de unidades classificadas como Rascunho (DRAFT), Pendente de Analise (PENDING), Aprovada (APPROVED), Rejeitada (REJECTED) e outros estados do workflow. Filtros configuraveis permitem segmentar por periodo de cadastramento, comunidade especifica ou equipe responsavel. Relatorio apresenta graficos visuais (pizza, barras) ilustrando proporcoes entre status, alem de tabelas detalhadas com contagens absolutas e percentuais. Exportacao disponivel em PDF com layout profissional incluindo cabecalhos institucionais, e Excel para analises adicionais. Dados filtrados por tenant_id do usuario autenticado.

## Criterios de Aceitacao

1. Agregacao por status do workflow
2. Filtros por periodo, comunidade e equipe
3. Graficos de pizza e barras
4. Exportacao em PDF e Excel
5. Segregacao por tenant_id

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-044, RF-049
