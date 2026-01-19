# Decap CMS

Decap CMS (anteriormente Netlify CMS) é sistema de gerenciamento de conteúdo Git-based que fornece interface visual para editar arquivos Markdown sem conhecimento técnico de Git. Edições são commitadas diretamente no repositório mantendo histórico completo e permitindo review via pull requests.

Arquitetura client-side significa que não há backend separado. Single page application em /admin/ carrega configuração de admin/config.yml e comunica diretamente com API do GitHub (ou GitLab, Bitbucket) para ler e escrever arquivos. Autenticação via OAuth garante que apenas usuários autorizados podem editar.

Configuração em config.yml define backend (GitHub com branch), collections mapeando para pastas de conteúdo, e fields especificando widgets de edição para cada campo do frontmatter. Widgets disponíveis incluem string, text, markdown, datetime, select, image, e list para campos repetíveis.

Editorial Workflow opcional habilita estados draft, in review, e ready adicionando coluna kanban na interface. Edições criam branch e PR automaticamente, review acontece no GitHub, e merge publica o conteúdo. Útil para equipes que precisam de aprovação antes de publicar.

Integração com Keycloak no WEBDOCS usa custom auth provider configurando Decap para autenticar via OAuth2 do Keycloak ao invés de GitHub direto garantindo que apenas usuários com role apropriada podem acessar CMS.

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
