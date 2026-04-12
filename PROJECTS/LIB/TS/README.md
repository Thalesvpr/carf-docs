---
type: readme
status: review
updated: 2026-01-24
---

# Bibliotecas TypeScript

Bibliotecas TypeScript compartilhadas entre aplicacoes do ecossistema CARF publicadas no GitHub Packages.

A biblioteca [TSCORE](./TSCORE/README.md) publica como @carf/tscore fornece value objects com validacoes brasileiras para CPF, CNPJ, Email e Phone. Inclui tipos de dominio sincronizados com backend .NET e cliente de autenticacao Keycloak com hooks para React e Vue. Suporta ambiente mobile via adapters de storage e navegacao.

A biblioteca [GEOAPI-CLIENT](./GEOAPI-CLIENT/README.md) publica como @carf/geoapi-client oferece HTTP client tipado para comunicacao com backend GEOAPI. Integra autenticacao automatica e tipos de request e response.

A biblioteca [UI-COMPONENTS](./UI-COMPONENTS/README.md) publica como @carf/ui disponibiliza componentes React baseados em shadcn/ui e Tailwind CSS para aplicacoes web REURBWEB, REURBMASTER e WEBDOCS. Inclui componentes de dominio CARF como StatusBadge e UnitCard.

A biblioteca [UI-NATIVE](./UI-NATIVE/README.md) publica como @carf/ui-native fornece componentes React Native baseados em react-native-reusables e NativeWind para o aplicativo REURBCAD mobile. Mantem consistencia visual com @carf/ui atraves de classes Tailwind compartilhadas.

Todas bibliotecas dependem de @carf/tscore para tipos. As bibliotecas de UI dependem de tipos para componentes de dominio. A biblioteca @carf/geoapi-client e consumida por REURBWEB e REURBCAD para comunicacao com backend. A biblioteca @carf/ui e exclusiva para web enquanto @carf/ui-native e exclusiva para mobile.

<!-- CARF-INDEX-START -->
<!-- CARF-INDEX-END -->
