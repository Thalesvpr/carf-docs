---
type: leaf
status: approved
updated: 2026-01-24
---

# Tenant

Organizacao cliente que utiliza o sistema CARF. Pode ser prefeitura municipal, orgao estadual, cartorio, ou empresa de topografia contratada para regularizacao fundiaria.

O sistema e multi-tenant - cada organizacao tem seus proprios dados completamente isolados. Usuarios de uma prefeitura nao veem dados de outra prefeitura. Comunidades, unidades e titulares pertencem sempre a um tenant especifico.

## Identificacao

Cada tenant tem um slug unico usado em URLs e login. Por exemplo, "prefeitura-rio" ou "iterj". O slug e definido na criacao e nao pode ser alterado depois.

## Personalizacao

Tenants podem customizar aparencia do sistema com logo e cores proprias. Cada organizacao ve a interface com sua identidade visual, embora o sistema seja o mesmo.

## Controle de Acesso

Administradores do tenant gerenciam seus proprios usuarios sem depender do suporte central. Podem criar contas, definir permissoes, e organizar equipes conforme estrutura interna.

## Isolamento de Dados

Todas as consultas ao banco sao automaticamente filtradas por tenant. E impossivel que consulta de um tenant retorne dados de outro - a seguranca e garantida em nivel de infraestrutura.
