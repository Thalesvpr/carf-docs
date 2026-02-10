---
type: leaf
status: review
updated: 2026-02-07
---

# Navegacao do Sidebar

Estrutura de navegacao do sidebar do WEBDOCS com hierarquia, labels e badges.

## Secoes

| Secao | Collapsed | Roles |
|-------|-----------|-------|
| Guia do Usuario | nao | todos autenticados |
| O Sistema CARF | nao | analyst, admin, super-admin, dev |
| Manuais | por subsecao | field-cadastrator+, analyst+, admin+, dev |
| API (badge Dev) | nao | super-admin, dev |
| Desenvolvedores (badge Dev) | nao | dev |
| Status | - | admin, super-admin, dev |
| Changelog | - | admin, super-admin, dev |

## Itens

Guia: Bem-vindo, Primeiros Passos, Conceitos, Glossario, FAQ. Sistema: Visao Geral, Lei 13.465/2017, Fluxo, Papeis, Entidades. Manuais GeoWeb: Introducao, Mapa, Unidades, Titulares, Analise, Relatorios. REURBCAD: Introducao, Coleta, Geometrias, Fotos, Sync. Admin: Introducao, Usuarios, Equipes, Config, Relatorios. API: Visao Geral, Autenticacao, Recursos, Erros, Swagger. Dev: Getting Started, Arquitetura, Bibliotecas, Componentes UI (Acoes, Inputs, Feedback, Overlays, Layout, Data Display), Contribuindo, Debug.

## Filtragem por Role

Starlight nao suporta filtragem nativa. Componente SidebarNav le Astro.locals.user.roles e filtra items. Sem autenticacao mostra apenas secoes publicas.

## Badges e Responsividade

Badges: note (azul), tip (verde), caution (amarelo para Dev/Beta), danger (vermelho), success (verde para Novo). Top-level expanded, subsecoes collapsed exceto ativa. Persiste em localStorage. Desktop: sidebar fixo. Tablet: colapsavel. Mobile: drawer overlay.
