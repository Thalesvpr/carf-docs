---
type: readme
status: review
updated: 2026-02-07
---

# Especificacoes Tecnicas - @carf/ui

Documentacao tecnica detalhada das configuracoes de projeto necessarias para build, desenvolvimento e publicacao da biblioteca de componentes.

## Documentos

| ID | Titulo | Descricao |
|:---|:-------|:----------|
| 01-package-json | Package.json | Dependencias, exports e configuracao npm |
| 02-tailwind-config | Tailwind Config | Configuracao Tailwind com tema CARF |
| 03-globals-css | Globals CSS | CSS variables e tema base |
| 04-storybook-config | Storybook | Configuracao do Storybook |

## Visao Geral

O @carf/ui e configurado para build via Vite com TypeScript, styling via Tailwind CSS com CSS Variables, componentes base via shadcn/ui e Radix UI, documentacao via Storybook e publicacao via GitHub Packages sob o scope @carf.

## Requisitos de Ambiente

As versoes minimas necessarias sao Node.js 18.0.0 ou superior e Bun 1.0.0 ou superior.

## Comandos Principais

Para instalar dependencias, usar bun install. Para build da biblioteca, bun run build. Para iniciar Storybook em modo de desenvolvimento, bun run storybook. Para executar testes, bun test. Para verificacao de tipos, tsc --noEmit.

<!-- CARF-INDEX-START -->
## Documentos

| ID | Titulo |
|:---|:-------|
| [01-package-json](./01-package-json.md) | Package.json |
| [02-tailwind-config](./02-tailwind-config.md) | Tailwind Config |
| [03-globals-css](./03-globals-css.md) | Globals CSS |
| [04-storybook-config](./04-storybook-config.md) | Storybook Config |

<!-- CARF-INDEX-END -->
