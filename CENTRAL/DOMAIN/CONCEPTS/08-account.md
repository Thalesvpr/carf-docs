---
type: leaf
status: review
updated: 2026-01-22
---

# Usuario

Pessoa com acesso ao sistema dentro de um tenant especifico. Pode ser funcionario da prefeitura, tecnico de campo, analista, ou gestor responsavel por aprovar processos.

Usuarios nao tem senha no sistema - a autenticacao e feita via Keycloak (login unico). O sistema apenas registra quem e o usuario e qual seu nivel de permissao.

## Papeis

Existem cinco niveis de acesso. Super Admin e exclusivo da equipe interna e acessa todos os tenants. Admin gerencia usuarios e configuracoes do tenant. Manager aprova processos e supervisiona equipes. Analyst faz analises documentais e tecnicas. Field Agent e o tecnico de campo que cadastra unidades e titulares.

## Atribuicao a Equipes

Usuarios sao organizados em equipes de trabalho. Um tecnico de campo pode pertencer a equipe Zona Norte, por exemplo. A equipe determina quais comunidades o usuario pode acessar.

## Autorizacoes Especificas

Alem da equipe, usuarios podem ter autorizacoes individuais para comunidades especificas. Isso permite flexibilidade quando alguem precisa acessar dados fora de sua equipe regular.

## Rastreabilidade

Toda acao no sistema registra qual usuario a executou. Isso permite auditoria completa de quem criou, modificou ou aprovou cada registro.
