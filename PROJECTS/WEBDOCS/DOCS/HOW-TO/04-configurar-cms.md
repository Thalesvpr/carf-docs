---
status: review
updated: 2026-01-17
---

# Configurar CMS

Guia para configurar Decap CMS permitindo edição visual de conteúdo via interface web.

Arquivo de configuração em public/admin/config.yml define backend, collections e fields. Backend especifica GitHub como storage com branch main e repo path. Collections mapeiam para pastas de conteúdo definindo campos editáveis.

Configurar autenticação editando backend section para usar OAuth via Keycloak. Adicionar base_url apontando para endpoint OAuth, auth_endpoint para /authorize, e token_endpoint para /token. App ID é client ID do Keycloak.

Testar CMS acessando /admin/ no navegador. Tela de login deve aparecer redirecionando para Keycloak. Após autenticação, interface do CMS deve carregar mostrando collections configuradas.

Adicionar nova collection para seção de conteúdo editando config.yml. Definir name único, label para exibição, folder apontando para pasta de conteúdo, create true para permitir novos documentos, e fields listando campos do frontmatter com tipo de widget apropriado.

Widgets disponíveis incluem string para texto curto, text para texto longo sem formatação, markdown para conteúdo com editor rich text, datetime para datas com picker, select para lista de opções, image para upload com preview, e list para campos repetíveis.

Configurar preview templates opcionalmente para ver como conteúdo aparecerá no site durante edição. Arquivo de preview em public/admin/preview.js define template usando React que renderiza frontmatter e body.

Testar editorial workflow habilitando publish_mode editorial_workflow em config.yml. Edições criam branches e PRs automaticamente. Review e merge acontecem no GitHub. Desabilitar para fluxo mais simples com commits diretos.
