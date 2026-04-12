---
type: leaf
status: approved
updated: 2026-01-24
---

# Processamento de Levantamento

Job de pos-processamento diferencial que corrige coordenadas GPS brutas usando dados de estacao RBMC. Transforma precisao de metros em centimetros.

O processamento e etapa obrigatoria para levantamentos oficiais. Coordenadas coletadas diretamente do GPS nao tem precisao suficiente para documentacao tecnica de registro em cartorio.
[[06-pdf-templates]]
## Entradas

Arquivo bruto de observacoes do receptor GPS usado em campo, no formato RINEX. Arquivo de observacoes da estacao RBMC para o mesmo periodo de coleta.

## Processamento

Software especializado combina as duas fontes de dados. Resolve ambiguidades de fase de portadora e calcula vetor preciso entre estacao de referencia e ponto coletado.

## Saidas

Coordenadas corrigidas com precisao centimetrica. Relatorio tecnico com estatisticas de qualidade - numero de satelites, diluicao de precisao, erro estimado.

## Status

Processamento pode ter sucesso com precisao adequada, sucesso parcial requerendo revisao, ou falha por dados insuficientes. Topografo valida resultados antes de aprovar.
