---
status: review
updated: 2026-01-17
---

# Seção Manuais

Seção /manuais/ documenta uso das três aplicações do ecossistema: GEOWEB (portal web), REURBCAD (app de campo), e ADMIN (console administrativo). Maior volume de conteúdo do portal.

Estrutura de pastas em src/content/docs/manuais/ subdivide em geoweb/, reurbcad/, e admin/. Cada subpasta contém index.mdx como landing e páginas por funcionalidade. Campo subsection no frontmatter identifica aplicação.

Conteúdo de GEOWEB documenta funcionalidades para analistas: dashboard com métricas, listagem e busca de unidades, visualização de detalhes com mapa, fluxo de aprovação e rejeição, geração de relatórios, e exportação de dados. Uma página por funcionalidade principal.

Conteúdo de REURBCAD documenta funcionalidades para agentes de campo: configuração inicial e login, navegação pelo mapa com camadas, cadastro de nova unidade com formulário, captura de fotos e documentos, modo offline e sincronização, e troubleshooting de problemas comuns em campo.

Conteúdo de ADMIN documenta funcionalidades para gestores: gestão de usuários (criar, editar, desativar), atribuição de roles e permissões, configuração de tenant (nome, CNPJ), visualização de audit logs, e gerenciamento de equipes.

Tom de escrita é prático e direto focado em "como fazer". Instruções passo-a-passo com screenshots. Callouts para dicas, warnings para ações destrutivas, e troubleshooting para problemas comuns.

Frontmatter define section como manuais, subsection como aplicação específica, audience como user. Screenshots organizados em public/images/manuais/{subsection}/.
