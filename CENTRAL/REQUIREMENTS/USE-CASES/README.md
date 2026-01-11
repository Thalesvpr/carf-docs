# USE-CASES

Casos de uso cross-cutting do CARF documentando fluxos de negócio que atravessam múltiplos projetos. Cada UC segue nomenclatura UC-NNN-titulo-descritivo.md, possui metadados YAML, atores (Administrador, Técnico, Fiscal, Cidadão, Sistema), objetivo claro, pré-condições que devem estar satisfeitas, fluxo principal passo-a-passo, fluxos alternativos para variações do cenário, fluxos de exceção para erros e validações, pós-condições garantidas após execução bem-sucedida, e rastreabilidade para RFs implementados e USs derivadas. Exemplos incluem cadastrar unidade habitacional (GEOWEB cadastra → GEOAPI valida → REURBCAD sincroniza → GEOGIS visualiza), gerenciar usuários sistema (autenticação Keycloak cross-project), e gerar relatório comunidade (agregação de dados multi-fonte). UCs específicos de cada projeto ficam em PROJECTS/*/REQUIREMENTS/USE-CASES/.

## Navegação

**[index-by-epic.md](./index-by-epic.md)** - Índice de todos os 11 Use Cases organizados por épica (security, performance, scalability)

Documentação complementar de requirements inclui [overview completo](../README.md) apresentando estrutura hierárquica de 11 UCs 221 RFs 140 USs e 85 RNFs com estatísticas de cobertura por módulo e épica, [índice por módulo](../index-by-module.md) organizando requirements conforme projetos implementadores GEOWEB REURBCAD GEOAPI GEOGIS facilitando descoberta de features por equipe de desenvolvimento, e [matriz de rastreabilidade](../traceability-matrix.md) mapeando relacionamentos bidirecionais UC→RF→US→RNF estabelecendo conexões explícitas entre casos de uso requisitos funcionais user stories e requisitos não-funcionais.

---

**Última atualização:** 2026-01-10
