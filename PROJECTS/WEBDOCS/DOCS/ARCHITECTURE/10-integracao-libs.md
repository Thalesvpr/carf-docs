---
type: leaf
status: review
updated: 2026-02-07
---

# Integracao com Bibliotecas

Especificacao da integracao do WEBDOCS com as bibliotecas TypeScript compartilhadas do ecossistema CARF.

## Dependencias

| Pacote | Versao | Uso | Hidratacao | Bundle |
|--------|--------|-----|------------|--------|
| @carf/tscore | workspace:* | Value Objects, validacoes, types | Nao requer | ~5kb |
| @carf/geoapi-client | workspace:* | Chamadas HTTP para GeoAPI | Nao requer (server) | ~15kb |
| @carf/ui | workspace:* | Componentes React interativos | client:idle/visible | ~40kb |

## Configuracao Astro para React

Integracao @astrojs/react necessaria para componentes @carf/ui. Configuracao Vite define ssr.noExternal com os tres pacotes CARF para bundle durante SSR. Campo optimizeDeps.include lista react e react-dom.

## Uso de @carf/tscore

Biblioteca base com Value Objects e validacoes. Usada em TypeScript server-side. Value Objects para validacao de formularios, tipagem de responses, e formatacao. Validators para validacao client-side. Types para tipagem de responses da GeoAPI.

## Uso de @carf/geoapi-client

SDK HTTP para GeoAPI usado apenas server-side. Inicializado em src/lib/services/geoapi.ts com baseUrl, timeout 10000ms, retry count 2 e delay 1000ms. Auth injection via interceptor adiciona header Authorization do cookie.

Detalhes de @carf/ui, wrapper pattern, e tree shaking em 10-integracao-libs-ui.md.
