---
type: leaf
status: review
updated: 2026-01-19
---

# Role Dev

Role dev destina-se a desenvolvedores que precisam acessar ferramentas técnicas do ecossistema CARF. Diferente das roles operacionais que seguem hierarquia super-admin > admin > analyst > field-collector, a role dev é transversal e pode ser combinada com qualquer outra role sem relação de herança.

Usuários com role dev têm acesso à seção /dev/ do WebDocs que inclui Swagger interativo com try-it-out para testar endpoints da GEOAPI usando token real do desenvolvedor, documentação técnica interna sobre arquitetura e padrões de código, métricas e logs de debug dos serviços em ambiente de desenvolvimento, e guias de contribuição com git workflow e code review. Esta seção não é visível para usuários sem role dev mesmo que possuam roles superiores como admin ou super-admin.

Role dev não concede permissões operacionais no sistema CARF. Um desenvolvedor que precisa também operar o sistema cadastrando unidades ou gerenciando usuários deve receber role adicional como analyst ou admin conforme necessidade. A separação garante que acesso a ferramentas de desenvolvimento seja explicitamente concedido e não implícito em outras roles.

No Keycloak a role dev é realm role simples sem composite roles associadas. Deve ser atribuída manualmente a usuários da equipe de desenvolvimento. Token JWT inclui dev no array de roles quando presente permitindo middleware do WebDocs validar acesso às rotas protegidas.
