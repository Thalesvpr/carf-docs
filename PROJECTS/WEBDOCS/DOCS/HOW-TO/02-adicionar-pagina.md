# Adicionar Página

Guia para criar novo documento no WEBDOCS com frontmatter correto e estrutura adequada para a seção destino.

Identificar seção destino (guia, sistema, manuais, api, dev, changelog) e navegar para pasta correspondente em src/content/docs/. Para manuais, navegar para subpasta da aplicação (geoweb, reurbcad, admin).

Criar arquivo Markdown com nome em kebab-case descritivo do conteúdo. Extensão .md para Markdown puro ou .mdx se precisar de componentes. Exemplo: cadastrar-unidade.md para guia de cadastro.

Adicionar frontmatter no topo do arquivo entre delimitadores de três hífens. Campos obrigatórios são title com nome da página, description com resumo de 50-160 caracteres, e section com nome da seção. Campos opcionais incluem sidebar para customizar navegação e audience para indicar público (user ou dev).

Escrever conteúdo seguindo diretrizes de content guidelines. Introdução contextualiza tema, corpo desenvolve com headings hierárquicos, conclusão sugere próximos passos. Usar callouts para destacar informações importantes.

Adicionar screenshots se necessário salvando em public/images/ na subpasta correspondente à seção. Referências de imagem usam path relativo a public/ sem a pasta public no caminho.

Validar localmente executando bun run build que verifica frontmatter contra schema Zod e valida links internos. Erros indicam campos ausentes ou links quebrados para corrigir.

Criar pull request com nova página para review. Preview deployment automático permite validar aparência antes de merge. Solicitar review de membro da equipe de documentação.

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
