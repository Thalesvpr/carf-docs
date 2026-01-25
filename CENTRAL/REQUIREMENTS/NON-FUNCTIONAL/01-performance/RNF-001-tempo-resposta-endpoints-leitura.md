---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-001: Tempo de Resposta - Endpoints de Leitura

## Descricao

Endpoints de consulta (GET) do GEOAPI devem responder rapidamente para garantir experiencia fluida aos usuarios. Aplica-se a endpoints como GET /api/units, GET /api/holders e GET /api/communities.

## Metricas

- Tempo de resposta: <= 500ms no percentil 95
- Condicoes: carga normal de operacao
- Ferramenta de medicao: k6 ou Artillery

## Criterios de Aceitacao

1. 95% das requisicoes GET completam em ate 500ms
2. Testes de carga validam metrica sob cenario realista
3. Monitoramento em producao confirma aderencia ao limite
