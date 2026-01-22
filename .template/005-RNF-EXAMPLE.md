---
type: rnf
status: approved
updated: 2026-01-22
category: performance
---

# RNF-001: Tempo de Resposta para Endpoints de Leitura

## Descricao

Endpoints de leitura da API REST devem responder dentro de limites aceitaveis para garantir experiencia fluida do usuario e evitar timeouts em conexoes moveis instáveis. O tempo de resposta impacta diretamente a percepcao de qualidade do sistema pelos usuarios de campo que operam em areas com conectividade limitada.

## Metricas

- P95 latencia: menor que 500ms
- P99 latencia: menor que 1000ms
- Condicoes: carga normal (ate 100 usuarios simultaneos), queries sem paginacao retornando ate 100 registros

## Criterios de Aceitacao

1. 95% das requisicoes GET completam em menos de 500ms
2. 99% das requisicoes GET completam em menos de 1000ms
3. Nenhuma requisicao GET excede 3000ms (timeout)
4. Metricas medidas em ambiente de producao com monitoramento APM
5. Testes de carga validam comportamento sob 100 usuarios simultaneos
