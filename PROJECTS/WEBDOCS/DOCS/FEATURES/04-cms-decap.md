---
status: review
updated: 2026-01-17
---

# CMS Decap

Decap CMS fornece interface visual em /admin/ para editar conteúdo do WEBDOCS sem conhecimento de Git ou Markdown. Edições são commitadas diretamente no repositório mantendo histórico completo e permitindo review via pull requests.

Configuração em admin/config.yml define backend GitHub com branch main, collections mapeando para pastas de conteúdo, e fields especificando widgets de edição. Cada collection corresponde a uma seção do portal (guia, sistema, manuais, api, status, changelog, banners).

Autenticação via Keycloak garante que apenas usuários autorizados acessam CMS. Custom auth provider em admin/index.html configura OAuth2 PKCE flow redirecionando para Keycloak ao invés de GitHub nativo. Token obtido é usado para autenticar chamadas à GitHub API.

Widgets disponíveis incluem string para títulos, text para descrições curtas, markdown para conteúdo principal com preview, datetime para datas com picker, select para campos de escolha, image para upload com preview, e list para campos repetíveis como tags.

Editorial workflow habilitado cria branch e PR automaticamente para cada edição. Coluna kanban mostra drafts, in review, e ready. Aprovação no GitHub merge o PR publicando conteúdo. Workflow é opcional e pode ser desabilitado para edições diretas no branch principal.

Preview em tempo real mostra como conteúdo aparecerá no site durante edição. Configuração de preview em config.yml define template Astro a usar para renderização. Útil para validar formatação antes de salvar.
