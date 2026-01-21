---
status: rejected
description: "Conteudo operacional. Git workflows pertencem a .github ou CONTRIBUTING."
updated: 2026-01-20
---

# Matriz de Compatibilidade

Tabela de versões compatíveis entre repositórios do CARF, atualizada a cada release coordenada. Consulte esta matriz antes de deployments para garantir combinações testadas e funcionais.

## Matriz Atual

| Release | carf-geoapi | carf-geoweb | carf-reurbcad | carf-keycloak | carf-geogis | carf-webdocs |
|---------|-------------|-------------|---------------|---------------|-------------|--------------|
| MVP 1.0 | v1.0.x | v1.0.x | v1.0.x | v1.0.x | v1.0.x | v1.0.x |

## Dependências Críticas

Algumas combinações de versões têm dependências críticas que devem ser respeitadas. carf-geoweb e carf-reurbcad dependem de endpoints específicos do carf-geoapi, portanto versões de frontend devem ser compatíveis com a versão de API deployada. Todos os frontends dependem de carf-keycloak para autenticação OAuth2, portanto mudanças em realm configuration ou client settings requerem atualização coordenada.

## Regras de Compatibilidade

Para carf-geoapi, versões PATCH (v1.0.1, v1.0.2) são sempre compatíveis com frontends da mesma MINOR. Versões MINOR (v1.1.0) adicionam endpoints mas mantêm compatibilidade. Versões MAJOR (v2.0.0) podem quebrar contratos e requerem atualização de frontends.

Para carf-keycloak, mudanças em temas são sempre compatíveis. Mudanças em realm configuration podem afetar claims JWT. Mudanças em client configuration afetam autenticação de aplicações específicas.

Para carf-tscore (quando publicado), versões são especificadas em package.json dos consumidores. Range ^ permite updates MINOR e PATCH automáticos. Range ~ permite apenas PATCH. Versões fixas garantem reprodutibilidade mas requerem updates manuais.

## Como Usar Esta Matriz

Antes de deploy, verificar se combinação de versões está documentada como compatível. Se deploying versão não listada, executar testes de integração completos em staging. Após validação de nova combinação, atualizar esta matriz com linha adicional.

## Histórico de Releases

| Data | Release | Notas |
|------|---------|-------|
| 2026-01-20 | MVP 1.0 | Release inicial do sistema |

## Incompatibilidades Conhecidas

Esta seção documenta combinações de versões conhecidas como incompatíveis para evitar deployments problemáticos.

| Combinação | Problema | Solução |
|------------|----------|---------|
| - | - | Nenhuma incompatibilidade documentada ainda |
