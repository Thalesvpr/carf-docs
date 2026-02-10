---
type: leaf
status: review
updated: 2026-02-07
---

# Integracao com Bibliotecas - UI Components

Detalhes de uso de @carf/ui, padrao de wrapper, e tree shaking. Documento complementar a 10-integracao-libs.md.

## Uso de @carf/ui

Componentes React para interatividade requerendo hidratacao client-side.

| Componente | Uso | Hidratacao | Nota |
|------------|-----|------------|------|
| Toast | Notificacoes sucesso/erro | client:idle | Criar ToastProvider.astro |
| Dialog | Modais de confirmacao | client:idle | Interatividade obrigatoria |
| DropdownMenu | Menu do usuario no header | client:idle | Interatividade obrigatoria |
| Button | Botoes com handlers complexos | client:idle | Opcional, pode usar Astro nativo |
| Input | Busca avancada com validacao | client:idle | Quando validacao real-time necessaria |

Evitar Table (Starlight ja tem tabelas otimizadas) e Card (usar Astro nativo para cards estaticos).

## Padrao de Wrapper Astro para React

Para usar React em paginas Astro, criar wrapper components. Componente Astro importa React component, define props no frontmatter, e renderiza com diretiva de hidratacao. Exemplo: UserMenuWrapper.astro importa DropdownMenu de @carf/ui, recebe prop user, renderiza com client:idle.

## Tree Shaking e Versioning

Bibliotecas CARF sao tree-shakeable. Importar seletivamente via import { Button, Dialog } from '@carf/ui', nunca via wildcard, permitindo bundler remover codigo nao usado.

Versioning usa workspace protocol (workspace:*) significando sempre versao local do workspace, resolvendo para versao especifica ao publicar.
