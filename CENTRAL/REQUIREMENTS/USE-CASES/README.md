# USE-CASES

Casos de uso cross-cutting do CARF documentando fluxos de negócio que atravessam múltiplos projetos. Cada UC segue nomenclatura UC-NNN-titulo-descritivo.md, possui metadados YAML, atores (Administrador, Técnico, Fiscal, Cidadão, Sistema), objetivo claro, pré-condições que devem estar satisfeitas, fluxo principal passo-a-passo, fluxos alternativos para variações do cenário, fluxos de exceção para erros e validações, pós-condições garantidas após execução bem-sucedida, e rastreabilidade para RFs implementados e USs derivadas. Exemplos incluem cadastrar unidade habitacional (GEOWEB cadastra → GEOAPI valida → REURBCAD sincroniza → GEOGIS visualiza), gerenciar usuários sistema (autenticação Keycloak cross-project), e gerar relatório comunidade (agregação de dados multi-fonte). UCs específicos de cada projeto ficam em PROJECTS/*/REQUIREMENTS/USE-CASES/.

---

**Última atualização:** 2025-12-29
