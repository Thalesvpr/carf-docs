---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: security
---

# RF-012: Controle de Acesso por Recurso

Sistema deve verificar permissões específicas para cada operação CRUD (Create Read Update Delete) em recursos protegidos onde verificação de permissão ocorre antes de executar qualquer operação validando que usuário autenticado possui role adequada e permissões específicas para recurso solicitado baseando decisão em claims roles e tenant_id presentes no JWT, retorno de HTTP 403 Forbidden deve ocorrer quando usuário autenticado tenta acessar recurso para qual não possui permissão adequada incluindo corpo de resposta JSON com mensagem descritiva (ex: "Usuário não possui permissão para deletar unidades" "Acesso negado: role insuficiente") permitindo cliente exibir feedback apropriado, logs de tentativas negadas devem ser registrados em sistema de auditoria incluindo timestamp identificador de usuário recurso tentado operação solicitada IP de origem e razão da negação permitindo análise de segurança detecção de tentativas de acesso não autorizado e compliance com requisitos regulatórios, implementação em módulo GEOAPI utilizando middleware ou decorators que interceptam requisições HTTP e aplicam lógica de autorização antes de delegar para controllers de negócio.

---

**Última atualização:** 2025-12-30
