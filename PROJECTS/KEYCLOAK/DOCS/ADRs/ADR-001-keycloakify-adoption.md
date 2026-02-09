---
type: adr
status: accepted
updated: 2026-02-07
description: "Decisao de adotar Keycloakify para temas Keycloak no projeto CARF."
---

# ADR-001: Adocao de Keycloakify para Temas Keycloak

## Contexto

O CARF requer customizacao visual das interfaces de autenticacao Keycloak. A abordagem tradicional usa templates FreeMarker com HTML e JavaScript vanilla. O projeto ja possui a biblioteca de componentes carf/ui construida sobre React, Radix UI e Tailwind CSS, utilizada em GEOWEB, ADMIN e WebDocs. Manter consistencia visual entre aplicacoes e telas de autenticacao e requisito do design system. A implementacao FreeMarker atual duplica estilos e logica de validacao CPF que ja existem em carf/ui.

## Decisao

Adotar Keycloakify como ferramenta padrao para desenvolvimento de temas Keycloak. Keycloakify permite criar temas usando React e TypeScript, possibilitando importacao direta dos componentes carf/ui nas telas de login, registro e recuperacao de senha. A escolha prioriza reutilizacao sobre tamanho de bundle. REURBCAD fica fora do escopo por utilizar design system mobile separado.

## Consequencias

Reutilizacao direta de componentes elimina duplicacao de estilos e comportamentos entre carf/ui e o tema Keycloak. Mudancas no design system propagam automaticamente para autenticacao. Desenvolvedores trabalham com stack familiar incluindo autocomplete, type checking e hot reload. Paginas de login ganham testabilidade unitaria e de integracao. Em contrapartida, o pipeline de CI/CD ganha complexidade com o build step do Keycloakify CLI. O bundle do tema cresce de aproximadamente cinquenta para cento e cinquenta kilobytes comprimidos. Atualizacoes do Keycloak podem exigir atualizacoes correspondentes no Keycloakify.

## Alternativas Rejeitadas

FreeMarker puro foi rejeitado por impossibilitar reutilizacao de carf/ui, forcando manutencao duplicada de estilos e componentes. Web Components adicionariam complexidade de compilacao sem ganho significativo sobre Keycloakify. Iframe embedding introduziria problemas de UX e seguranca com CSP e cross-origin.
