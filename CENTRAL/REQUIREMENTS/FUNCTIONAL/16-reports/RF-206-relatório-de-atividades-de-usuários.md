---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-206: Relatorio de Atividades de Usuarios

## Descricao

Sistema deve produzir relatorio detalhado de atividades realizadas por usuario incluindo contabilizacao de operacoes de criacao e edicao discriminadas por tipo de entidade (unidades, titulares, processos, documentos), permitindo avaliacao de produtividade individual. Configuracao flexivel de periodo atraves de data inicial/final ou opcoes predefinidas (ultima semana, mes, trimestre). Relatorio em formato tabular lista cada usuario com estatisticas como unidades criadas, editadas, titulares cadastrados, fotos anexadas, documentos enviados e horas de uso calculadas via timestamps de login/logout. Exportacao em Excel e PDF permite analises adicionais e documentacao formal para prestacao de contas ou avaliacao de desempenho. Dados filtrados por tenant_id.

## Criterios de Aceitacao

1. Contabilizacao por tipo de operacao e entidade
2. Configuracao flexivel de periodo
3. Estatisticas por usuario
4. Calculo de horas de uso
5. Segregacao por tenant_id

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-030, RF-001
