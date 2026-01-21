---
status: review
updated: 2026-01-21
---

# Validação de Conteúdo

Checks automáticos validam integridade do conteúdo antes de deploy garantindo que links funcionam, frontmatter está correto, e estrutura segue padrões.

Validação de links usa astro check junto com plugin de link checking que verifica links internos apontando para páginas existentes, links externos retornando HTTP 200, e âncoras referenciando headings válidos. Links quebrados falham o build com lista de erros.

Validação de frontmatter verifica schema Zod definido em src/content/config.ts. Campos obrigatórios ausentes, tipos incorretos, e valores fora do enum permitido geram erros de build. Mensagens indicam arquivo e campo problemático.

Validação de estrutura verifica que arquivos estão em pastas corretas para sua seção, nomes seguem convenção kebab-case, e hierarquia de headings é válida (h1 único, sem pulos de nível). Implementada via script customizado em scripts/validate-structure.ts.

Validação de imagens verifica que referências de imagem apontam para arquivos existentes em public/images/, alt text está presente em todas imagens, e dimensões width/height estão definidas para prevenir layout shift.

Execução local via comando npm run validate executa todos checks de conteúdo. Útil para validar antes de commit. Pre-commit hook opcional pode executar validação automaticamente impedindo commits com erros.

Erros de validação são reportados com path do arquivo, linha quando possível, e descrição do problema. Exit code não-zero falha CI impedindo deploy de conteúdo inválido.
