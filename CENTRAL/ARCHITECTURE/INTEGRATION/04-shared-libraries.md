---
type: leaf
status: review
updated: 2026-01-22
---

# Shared Libraries

Bibliotecas compartilhadas entre projetos frontend para reuso de codigo e consistencia. Pacotes publicados em registry npm privado e versionados semanticamente com changelog documentado.

O pacote @carf/tscore contem utilitarios TypeScript como validadores de CPF/CNPJ, formatadores de data/moeda, tipos compartilhados e helpers de geometria. O pacote @carf/ui implementa design system com componentes React usando shadcn/ui como base, tokens de design e temas claro/escuro.

## Clientes de API

O pacote geoapi-client fornece cliente TypeScript tipado para GEOAPI gerado automaticamente a partir do OpenAPI spec. Inclui interceptors para autenticacao, retry, e tratamento de erros. Usado por GEOWEB, ADMIN e REURBCAD garantindo consistencia na comunicacao com backend e tipagem forte de payloads.
