---
status: review
updated: 2026-01-21
---

# ADR-004: Decap CMS para Edição Visual

Decisão adotando Decap CMS (anteriormente Netlify CMS) como interface de edição visual justificada por permitir contribuidores não-técnicos editarem documentação sem conhecimento de Git ou Markdown via interface WYSIWYG no navegador, commits automáticos para repositório Git mantendo histórico completo e review via PR, configuração declarativa em YAML definindo collections e fields sem código backend, preview em tempo real mostrando como conteúdo aparecerá no site, e custo zero sendo projeto open source auto-hospedado.

Configuração em admin/config.yml define collections mapeando para pastas de conteúdo (guia, sistema, manuais, api, dev), fields correspondendo ao frontmatter schema Zod, e backend Git Gateway autenticando via Keycloak para edição autorizada.

Workflow de edição: contribuidor acessa /admin/, autentica via Keycloak, seleciona ou cria documento, edita via interface visual, salva criando commit no branch atual ou PR para review dependendo de configuração, preview deployment permite validação antes de merge.

Alternativas rejeitadas: edição direta no GitHub (UX ruim para não-técnicos), headless CMS pago (custo desnecessário), wiki separada (fragmentação de conteúdo).
