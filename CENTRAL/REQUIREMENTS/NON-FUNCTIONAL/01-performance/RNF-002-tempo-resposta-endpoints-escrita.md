---
id: RNF-002
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-002: Tempo de Resposta - Endpoints de Escrita

## Descricao

Endpoints de criacao e edicao (POST/PATCH) do GEOAPI devem responder em tempo aceitavel considerando validacoes e persistencia. Aplica-se a endpoints como POST /api/units e PATCH /api/units/{id}.

## Metricas

- Tempo de resposta: <= 1000ms no percentil 95
- Condicoes: carga normal de operacao
- Ferramenta de medicao: k6 ou Artillery

## Criterios de Aceitacao

1. 95% das requisicoes POST/PATCH completam em ate 1 segundo
2. Testes de carga validam metrica sob cenario realista
3. Monitoramento em producao confirma aderencia ao limite
