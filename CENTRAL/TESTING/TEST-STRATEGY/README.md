# TEST-STRATEGY

Estratégia de testes CARF. test-pyramid.md defende proporção 70 porcento unit / 20 porcento integration / 10 porcento e2e minimizando testes lentos caros. coverage-targets.md define mínimo 80 porcento coverage domain layer (business logic crítica), 60 porcento application (use cases), 40 porcento infrastructure (acceptable pois testa frameworks). Ferramentas: framework de testes unitários backend com asserções fluentes, framework de testes frontend com biblioteca de testes de componentes, framework de testes E2E mobile. CI pipeline falha se coverage abaixo targets. Mutation testing opcional via ferramenta de análise de mutações detectando dead code.

---

**Última atualização:** 2025-01-05
