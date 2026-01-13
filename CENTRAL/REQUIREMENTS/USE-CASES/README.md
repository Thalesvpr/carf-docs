# USE-CASES

Casos de uso cross-cutting do CARF documentando fluxos de negócio que atravessam múltiplos projetos. Cada UC segue nomenclatura UC-NNN-titulo-descritivo.md, possui metadados YAML, atores (Administrador, Técnico, Fiscal, Cidadão, Sistema), objetivo claro, pré-condições que devem estar satisfeitas, fluxo principal passo-a-passo, fluxos alternativos para variações do cenário, fluxos de exceção para erros e validações, pós-condições garantidas após execução bem-sucedida, e rastreabilidade para RFs implementados e USs derivadas. Exemplos incluem cadastrar unidade habitacional (GEOWEB cadastra → GEOAPI valida → REURBCAD sincroniza → GEOGIS visualiza), gerenciar usuários sistema (autenticação Keycloak cross-project), e gerar relatório comunidade (agregação de dados multi-fonte). UCs específicos de cada projeto ficam em PROJECTS/*/REQUIREMENTS/USE-CASES/.

## Navegação

Documentação complementar de requirements inclui [overview completo](../README.md) apresentando estrutura hierárquica de 11 UCs 221 RFs 140 USs e 85 RNFs com estatísticas de cobertura por módulo e épica organizando requirements conforme projetos implementadores GEOWEB REURBCAD GEOAPI GEOGIS facilitando descoberta de features por equipe de desenvolvimento estabelecendo conexões explícitas entre casos de uso requisitos funcionais user stories e requisitos não-funcionais.

---

**Última atualização:** 2026-01-10

---

<!-- GENERATED:START - Não edite abaixo desta linha -->
## Índice por Domínio (66 requisitos)

| # | Domínio | Arquivos |
|:--|:--------|:--------:|
|  | [UC-001-cadastrar-unidade-habitacional](./UC-001-cadastrar-unidade-habitacional/README.md) | 6 |
|  | [UC-002-aprovar-unidade-habitacional](./UC-002-aprovar-unidade-habitacional/README.md) | 4 |
|  | [UC-003-vincular-titular-unidade](./UC-003-vincular-titular-unidade/README.md) | 6 |
|  | [UC-004-coletar-dados-campo-mobile](./UC-004-coletar-dados-campo-mobile/README.md) | 7 |
|  | [UC-005-sincronizar-dados-offline](./UC-005-sincronizar-dados-offline/README.md) | 7 |
|  | [UC-006-gerar-relatorio-comunidade](./UC-006-gerar-relatorio-comunidade/README.md) | 6 |
|  | [UC-007-exportar-dados-geograficos](./UC-007-exportar-dados-geograficos/README.md) | 6 |
|  | [UC-008-importar-shapefile](./UC-008-importar-shapefile/README.md) | 6 |
|  | [UC-009-gerenciar-processo-legitimacao](./UC-009-gerenciar-processo-legitimacao/README.md) | 6 |
|  | [UC-010-configurar-camadas-wms](./UC-010-configurar-camadas-wms/README.md) | 7 |
|  | [UC-011-gerenciar-equipes-tecnicas](./UC-011-gerenciar-equipes-tecnicas/README.md) | 5 |

*Gerado automaticamente em 2026-01-13 19:11*
<!-- GENERATED:END -->
