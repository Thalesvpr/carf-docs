---
type: leaf
status: review
updated: 2026-02-07
---

# Banner de Notificacoes

Banner no topo do site exibe avisos importantes como manutencoes programadas, alertas de seguranca, ou anuncios de novas funcionalidades. Conteudo editavel via Decap CMS permite equipe nao-tecnica publicar avisos sem deploy.

Configuracao em collection banners do CMS define campos title, message, type (info, warning, error, success), startDate, endDate, e dismissible. Datas controlam periodo de exibicao automatico.

Componente Banner.astro renderizado no layout base consulta collection de banners ativos filtrando por data atual entre startDate e endDate. Multiplos banners sao empilhados. Banner dismissible salva estado em localStorage.

## Tipos de Banner

| Tipo | Cor fundo | Uso |
|------|-----------|-----|
| info | Azul claro | Informacoes gerais, anuncios |
| warning | Amarelo claro | Manutencoes programadas |
| error | Vermelho claro | Indisponibilidade, problemas criticos |
| success | Verde claro | Novas versoes, resolucoes |

## Componente Banner.astro

Componente em src/components/Banner.astro verifica primeiro banner de emergencia via import de src/config/emergency-banner.json. Se active, usa como prioritario. Senao, busca da collection CMS filtrando por datas.

Script client-side verifica banners dismissiveis: se localStorage contem chave banner-dismissed-{id}, remove elemento. Botao de fechar salva chave e remove do DOM.

Detalhes de schemas, CMS e emergencia em 03-banner-notificacoes-config.md.
