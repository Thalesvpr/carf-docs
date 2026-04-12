---
type: readme
status: review
updated: 2026-02-07
---

# API Reference

Documentacao completa da API publica da biblioteca tscore cobrindo validacoes, tipos de dominio, autenticacao e extensoes para mobile.

A [API de validacoes](./01-validation-api.md) documenta os quatro value objects principais. CPF e CNPJ implementam validacao com digitos verificadores mod-11, fornecendo metodos estaticos isValid, format e clean alem de instancias imutaveis. Email valida formato RFC 5322 com normalizacao para lowercase. Phone valida telefones brasileiros com DDD, distinguindo celular de fixo.

A [API de tipos](./02-types-api.md) serve como indice para a documentacao de interfaces e enums do dominio CARF, organizada em quatro sub-documentos. A secao de [entidades](./02-types-entities.md) cobre Unit, Holder, Community, Team, Account, Tenant, Block, Plot, Building e Document. A secao de [relacionamentos](./03-types-relationships.md) descreve juncoes, legitimacao, GIS, autenticacao e infraestrutura. A secao de [enums](./04-types-enums.md) documenta UnitStatus, Role, LegitimationStatus e todos os demais enums de classificacao. A secao de [DTOs](./05-types-dtos.md) apresenta contratos de criacao e atualizacao com tabela de versionamento.

A [API de autenticacao](./06-auth-api.md) descreve KeycloakClient com fluxo OAuth2 Authorization Code PKCE. Detalha metodos init, login, handleCallback, logout e getToken com refresh automatico. Documenta hooks useAuth para React e Vue com contexto de usuario, roles e permissoes hierarquicas.

A [API de autenticacao nativa](./07-auth-native-api.md) apresenta extensoes para suporte cross-platform. Interfaces StorageAdapter e NavigationAdapter permitem injecao de dependencias para ambientes mobile que requerem expo-secure-store e deep linking.

<!-- CARF-INDEX-START -->
<!-- CARF-INDEX-END -->
