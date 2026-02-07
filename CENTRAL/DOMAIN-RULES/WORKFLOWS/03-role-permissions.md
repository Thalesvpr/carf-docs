---
type: leaf
status: approved
updated: 2026-02-07
---

# Role Permissions

Sistema RBAC com seis niveis hierarquicos de autorizacao, alinhado com Keycloak realm CARF.

## Hierarquia de Papeis

| Role | Keycloak Name | Nivel | Descricao |
|------|---------------|-------|-----------|
| SUPER_ADMIN | super-admin | 6 | Acesso irrestrito incluindo todos os tenants |
| ADMIN | admin | 5 | Gerencia usuarios, times e configuracoes do tenant |
| MANAGER | manager | 4 | Aprova unidades, gerencia processos de legitimacao |
| ANALYST | analyst | 3 | Revisa e recomenda aprovacao |
| FIELD_COORDINATOR | field-coordinator | 2 | Coordenador de equipe de campo |
| FIELD_CADASTRATOR | field-cadastrator | 1 | Cadastrador de campo |

## Composicao de Roles (Keycloak)

```
super-admin
  └── admin
       └── manager
            ├── analyst
            └── field-coordinator
                 └── field-cadastrator
```

Cada role inclui permissoes de todos os roles abaixo na hierarquia.

## Papeis de Campo - Mobile (REURBCAD)

**field-coordinator**: Coordenador de equipe de campo.
- Selecao de regiao de trabalho
- Visualizacao de metricas da equipe
- Acesso a lista de membros
- Dashboard de produtividade individual por cadastrador
- Contato com membros da equipe
- Visualizacao de lotes pendentes
- Interface com menu inferior completo

**field-cadastrator**: Cadastrador de campo.
- Visualizacao do mapa da regiao atribuida
- Criacao de pings em lotes
- Preenchimento de formularios de unidade e titular
- Captura de fotos e assinatura
- Interface simplificada SEM menu inferior
- Nao visualiza metricas de colegas
- Nao seleciona regiao

## Segregacao de Responsabilidades

Decisoes criticas requerem dupla verificacao:
- Analyst revisa, Manager aprova
- Emissao de certidao requer: units.approve + legitimation.approve + documents.generate

## Politicas de Atribuicao

| Promocao | Requisitos |
|----------|------------|
| field-cadastrator → field-coordinator | Aprovacao do manager |
| field-coordinator → analyst | Capacitacao em analise tecnica |
| analyst → manager | 6 meses + taxa aprovacao > 95% |
| manager → admin | Funcionario efetivo do orgao |
| admin → super-admin | Equipe tecnica de infraestrutura |

## Auditoria

Todas as acoes sensiveis sao registradas com: usuario, IP, timestamp, parametros, resultado.
Tentativas de acesso negado geram alertas de seguranca.

## Referencia

- Keycloak realm: `CENTRAL/INTEGRATION/KEYCLOAK/realm-export.json`
- TypeScript enum: `@carf/tscore` → `Role`
