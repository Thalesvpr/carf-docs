# Template Dev

Template para páginas da seção protegida /dev/ destinadas a desenvolvedores do ecossistema CARF.

Frontmatter obrigatório define title com nome técnico preciso, description com resumo técnico, section com valor dev, audience com valor dev indicando conteúdo protegido, e prerender com valor false para SSR que permite verificação de role.

Introdução assume conhecimento técnico do leitor. Pode referenciar conceitos de programação, APIs, padrões de arquitetura sem explicação. Foco em contexto específico do CARF, não em tutoriais básicos.

Corpo usa formatação técnica apropriada: code blocks com syntax highlighting para exemplos de código, inline code para nomes de funções, classes, arquivos, e variáveis. Diagramas Mermaid para fluxos e arquitetura.

Seção de configuração lista variáveis de ambiente, arquivos de config, e dependências necessárias. Formato de lista ou tabela para referência rápida.

Seção de exemplos de código mostra uso real com comentários explicando decisões não óbvias. Código deve ser copiável e funcional, não pseudo-código. Indicar arquivo onde código deve ser colocado.

Seção de troubleshooting lista erros comuns com causas e soluções. Incluir mensagens de erro exatas quando possível para facilitar busca.

Referências linkam para documentação externa relevante (libs, APIs, specs). Links para código fonte no repositório quando apropriado.

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
