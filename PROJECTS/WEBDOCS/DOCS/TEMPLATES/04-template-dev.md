---
type: leaf
status: review
updated: 2026-02-07
---

# Template Dev

Template para paginas da secao protegida /dev/ destinadas a desenvolvedores do ecossistema CARF.

Frontmatter obrigatorio define title com nome tecnico preciso, description com resumo tecnico, source apontando para doc em PROJECTS, sidebar com order, label, e badge Dev, prerender false para SSR, e draft false.

## Estrutura do Frontmatter

| Campo | Obrigatorio | Descricao | Exemplo |
|-------|-------------|-----------|---------|
| title | Sim | Nome tecnico preciso | JWT Validation Service |
| description | Sim | Resumo tecnico conciso | Servico de validacao JWT com cache JWKS |
| source | Sim | Path doc em PROJECTS | PROJECTS/WEBDOCS/DOCS/ARCHITECTURE/03-autenticacao.md |
| sidebar.order | Sim | Posicao na navegacao | 2 |
| sidebar.label | Sim | Label curto | JWT Validation |
| sidebar.badge | Sim | Badge visual | Dev |
| prerender | Sim | false para SSR com auth | false |
| draft | Sim | false para publicar | false |

## Estrutura do Conteudo

Introducao assume conhecimento tecnico. Pode referenciar APIs, padroes de arquitetura sem explicacao basica. Imports incluem Aside, Code, Tabs, TabItem do Starlight.

Secao de arquitetura descreve estrutura do componente. Diagramas Mermaid para fluxos. Secao de configuracao lista variaveis de ambiente em tabela e dependencias em tabela.

Detalhes de secoes de implementacao, testes e troubleshooting em 04-template-dev-secoes.md.
