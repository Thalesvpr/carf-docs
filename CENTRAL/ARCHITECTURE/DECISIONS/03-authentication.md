---
type: adr
status: approved
updated: 2026-01-24
---

# ADR-003: Keycloak como Identity Provider

## Contexto

Sistema CARF requer autenticacao unificada para web, mobile e desktop com suporte a single sign-on. Prefeituras podem querer integracao com Active Directory existente. Gestao de usuarios e roles deve ser centralizada. Decisao impacta seguranca, experiencia de login e integracao com sistemas municipais.

## Decisao

Adotamos Keycloak como identity provider centralizado implementando OAuth2 e OpenID Connect. Single realm CARF com todos os usuarios e clients. Multi-tenancy via atributo customizado tenant_id incluido como claim no token. Temas customizados com Keycloakify para consistencia visual com demais aplicacoes. O Plugin QGIS (GEOGIS) exige autenticacao em duas etapas: login via Keycloak OAuth2 seguido de AUTHENTICATION KEY (chave adicional que vincula sessao do plugin ao backend e habilita acesso as ortofotos do tenant).

## Consequencias

Single sign-on funcional entre todas as aplicacoes. Federation com LDAP e Active Directory disponivel para prefeituras que desejarem. Infraestrutura adicional para hospedar Keycloak com alta disponibilidade. Complexidade de configuracao inicial compensada por flexibilidade de customizacao.

## Alternativas Rejeitadas

Auth0 foi descartado por custo em escala com milhares de usuarios e lock-in em servico cloud. Firebase Auth foi rejeitado por limitacoes de customizacao e dependencia de ecossistema Google. Implementacao propria foi descartada por complexidade de manter seguranca em protocolo OAuth2.
