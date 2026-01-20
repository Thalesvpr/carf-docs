---
status: review
updated: 2026-01-20
---

# Coordenação de Releases

Processo de coordenação de releases entre os repositórios do CARF garantindo compatibilidade, qualidade e deployments sem downtime.

## Processo de Release

O processo de release segue etapas sequenciais começando por preparação onde cada repositório cria branch release/vX.Y.Z a partir de main com features planejadas para a versão. Na fase de atualização, changelogs são atualizados seguindo categorias Added, Changed, Deprecated, Removed, Fixed e Security, e versões são incrementadas em package.json ou csproj conforme SemVer. Tags são criadas no formato vX.Y.Z após aprovação dos PRs de release. Deploy para staging acontece em todos os repositórios permitindo testes de integração end-to-end. Após validação, deploy para produção segue ordem específica garantindo dependências disponíveis antes de consumidores.

## Ordem de Deploy

A ordem de deploy respeita dependências entre projetos. Primeiro deploy do carf-keycloak garantindo autenticação disponível. Segundo deploy do carf-geoapi disponibilizando API backend. Terceiro deploy de frontends carf-geoweb, carf-reurbcad e carf-webdocs que consomem a API. Por último deploy do carf-geogis que pode depender de dados via API. Esta ordem minimiza janelas onde componentes ficam incompatíveis.

## Smoke Tests

Após cada deploy em staging e produção, smoke tests validam funcionamento básico. Para carf-keycloak verificar endpoint de health e obtenção de token. Para carf-geoapi verificar health check e endpoint público de versão. Para carf-geoweb verificar carregamento da aplicação e autenticação. Para carf-reurbcad verificar build e login em ambiente de teste. Falha em smoke test bloqueia progressão do deploy.

## Breaking Changes

Mudanças incompatíveis requerem comunicação antecipada. Deprecation warnings são adicionados uma release antes da remoção efetiva. Migration guides documentam passos necessários para consumidores se adequarem. Período de suporte para versões anteriores é definido conforme impacto da mudança. Coordenação com times consumidores garante que todos estejam preparados antes do deploy.

## Rollback

Em caso de problemas após deploy em produção, procedimento de rollback reverte para versão anterior. Tags anteriores identificam versões estáveis conhecidas. Deploy da tag anterior restaura estado funcional. Investigação de root cause acontece em paralelo sem pressão de produção instável. Postmortem documenta causa, impacto e ações preventivas.

## Release Notes

Cada release produz release notes agregadas documentando mudanças em todos os repositórios afetados. O documento especifica versões de cada componente, features adicionadas, bugs corrigidos e breaking changes. Release notes são publicadas no carf-webdocs e comunicadas aos stakeholders.

## Matriz de Compatibilidade

Consulte 03-compatibility-matrix.md para tabela detalhada de versões compatíveis entre repositórios, atualizada a cada release coordenada.
