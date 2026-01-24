---
type: readme
status: review
updated: 2026-01-24
---

# API Reference

Documentacao completa da API publica da biblioteca @carf/tscore cobrindo validacoes, tipos de dominio, autenticacao e extensoes para mobile.

A [API de validacoes](./01-validation-api.md) documenta os quatro value objects principais. CPF e CNPJ implementam validacao com digitos verificadores mod-11, fornecendo metodos estaticos isValid, format e clean alem de instancias imutaveis. Email valida formato RFC 5322 com normalizacao para lowercase. Phone valida telefones brasileiros com DDD, distinguindo celular de fixo.

A [API de tipos](./02-types-api.md) cobre interfaces e enums do dominio CARF. Documenta entidades Unit, Holder e Community com todos os campos e relacionamentos. Inclui enums UnitStatus, Role, LegitimationStatus e EntityType usados em todo o sistema. DTOs de criacao e atualizacao seguem convencoes de campos obrigatorios e opcionais.

A [API de autenticacao](./03-auth-api.md) descreve KeycloakClient com fluxo OAuth2 Authorization Code PKCE. Detalha metodos init, login, handleCallback, logout e getToken com refresh automatico. Documenta hooks useAuth para React e Vue com contexto de usuario, roles e permissoes hierarquicas.

A [API de autenticacao nativa](./04-auth-native-api.md) apresenta extensoes para suporte cross-platform. Interfaces StorageAdapter e NavigationAdapter permitem injecao de dependencias para ambientes mobile que requerem expo-secure-store e deep linking.

<!-- CARF-INDEX-START -->
<!-- CARF-INDEX-END -->
