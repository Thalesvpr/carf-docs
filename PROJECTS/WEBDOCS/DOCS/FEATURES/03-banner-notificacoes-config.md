---
type: leaf
status: review
updated: 2026-02-07
---

# Banner de Notificacoes - Configuracao

Schemas de collection, configuracao Decap CMS e banner de emergencia. Documento complementar a 03-banner-notificacoes.md.

## Collection Schema

Collection banners definida em src/content/config.ts como tipo data com schema Zod. Campos: title (string max 100), message (string max 500), type (enum info/warning/error/success), dismissible (boolean default true), startDate (date coerce), endDate (date coerce), e active (boolean default true).

## Decap CMS Collection

Collection banners configurada em public/admin/config.yml com pasta src/content/banners, extensao e formato JSON, create habilitado. Campos mapeiam para schema Zod: string para titulo, text para mensagem, select para tipo, boolean para dismissible e ativo, datetime para datas.

## Banner de Emergencia

Arquivo src/config/emergency-banner.json permite banners sem depender do CMS. Util para comunicar indisponibilidade do proprio CMS. Formato JSON com campos id, title, message, type, dismissible, startDate, endDate, e active. Verificado prioritariamente pelo componente Banner.astro antes da collection CMS.
