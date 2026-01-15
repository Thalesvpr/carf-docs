# TEST-STRATEGY

Estratégia de testes do CARF baseada na pirâmide de testes.

A [pirâmide de testes](./02-test-pyramid.md) define a proporção: 70% testes unitários para feedback rápido, 20% testes de integração para validar componentes juntos, e 10% testes E2E para jornadas críticas. Isso minimiza testes lentos e caros enquanto mantém cobertura adequada.

Os [coverage targets](./01-coverage-targets.md) definem mínimos por camada: 80% para domain layer onde está a lógica de negócio crítica, 60% para application layer com use cases, e 40% para infrastructure que testa frameworks. O pipeline CI falha se o coverage ficar abaixo desses targets.

Mutation testing opcional pode ser usado para detectar testes fracos que não validam comportamento real.

---

**Última atualização:** 2026-01-14

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (2 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-coverage-targets](./01-coverage-targets.md) | METAS DE COBERTURA |
| [02-test-pyramid](./02-test-pyramid.md) | PIRÂMIDE DE TESTES |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
