# TEST-STRATEGY

Estratégia de testes do CARF baseada na pirâmide de testes.

A [pirâmide de testes](./test-pyramid.md) define a proporção: 70% testes unitários para feedback rápido, 20% testes de integração para validar componentes juntos, e 10% testes E2E para jornadas críticas. Isso minimiza testes lentos e caros enquanto mantém cobertura adequada.

Os [coverage targets](./coverage-targets.md) definem mínimos por camada: 80% para domain layer onde está a lógica de negócio crítica, 60% para application layer com use cases, e 40% para infrastructure que testa frameworks. O pipeline CI falha se o coverage ficar abaixo desses targets.

Mutation testing opcional pode ser usado para detectar testes fracos que não validam comportamento real.

## Documentos

- **[test-pyramid.md](./test-pyramid.md)** - Proporção 70/20/10 e justificativa
- **[coverage-targets.md](./coverage-targets.md)** - Metas de coverage por camada

---

**Última atualização:** 2026-01-14
