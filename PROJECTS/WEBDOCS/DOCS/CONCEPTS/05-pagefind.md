---
status: review
updated: 2026-01-17
---

# Pagefind

Pagefind é engine de busca estática que indexa conteúdo no build time e executa queries inteiramente no cliente sem necessidade de servidor de busca. Índice comprimido é carregado sob demanda resultando em busca instantânea com bundle size mínimo.

Indexação acontece como passo pós-build executando pagefind --site dist que escaneia HTML gerado extraindo texto, headings, e metadados. Índice é fragmentado em chunks pequenos carregados conforme usuário digita minimizando transferência inicial.

Integração com Starlight é built-in configurada automaticamente. Componente de busca no header usa Pagefind UI renderizando input com autocomplete, resultados com preview de snippet, e navegação por teclado. Configuração em astro.config.mjs permite customizar placeholder, atalhos de teclado, e traduções.

Atributos data-pagefind controlam indexação granular. data-pagefind-body marca região principal de conteúdo ignorando navegação e footer. data-pagefind-ignore exclui seções específicas como código ou elementos decorativos. data-pagefind-meta adiciona metadados customizados aos resultados.

Vantagens sobre Algolia DocSearch incluem custo zero (Algolia é pago para sites não open source), privacidade (queries não saem do navegador), e controle total sobre indexação. Limitações incluem ausência de analytics de busca e necessidade de rebuild para atualizar índice.
