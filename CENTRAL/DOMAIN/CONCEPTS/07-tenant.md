---
type: leaf
status: approved
updated: 2026-02-21
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

## Organizacao Operacional

Um Tenant pode definir **Regioes** para organizar sua atuacao. Regioes sao unidades estrategicas — nao niveis geograficos fixos. Cada Tenant decide o que "regiao" significa para seu contexto (pode ser bairro, cidade, macrorregiao, contrato, etc.).

Comunidades podem ser associadas a Regioes, mas a associacao e flexivel e configuravel pelo Tenant. Nao ha hierarquia geografica rigida imposta pelo sistema.

Estrutura tipica: Tenant > Regioes (opcionais) > Comunidades

### Referencia

- Ver [39-regiao.md](./39-regiao.md)
- Ver [04-community.md](./04-community.md)
