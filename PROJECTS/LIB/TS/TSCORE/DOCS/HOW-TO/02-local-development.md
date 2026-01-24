---
type: leaf
status: review
updated: 2026-01-24
---

# Desenvolvimento Local

Guia para desenvolvedores que precisam modificar @carf/tscore e testar mudancas em projetos consumidores antes de publicar.

## Setup Inicial

Clonar repositorio CARF e navegar para PROJECTS/LIB/TS/TSCORE/SRC-CODE. Executar bun install para instalar dependencias. Executar bun run build para gerar dist/ inicial. Executar bun test para validar ambiente.

## Criando Link Local

Navegar para diretorio do tscore e executar npm link. Este comando registra pacote globalmente apontando para diretorio local. Link persiste ate ser removido explicitamente ou sobrescrito por nova instalacao.

## Consumindo Link em Projeto

Navegar para projeto consumidor como GEOWEB e executar npm link @carf/tscore. Imports de @carf/tscore agora resolvem para codigo local do tscore em vez de versao publicada. Mudancas no tscore refletem imediatamente apos rebuild.

## Workflow de Desenvolvimento

Manter dois terminais abertos. No tscore executar bun run build com flag --watch para recompilacao automatica. No projeto consumidor executar servidor de desenvolvimento normal. Modificar codigo do tscore e observar mudancas propagarem para consumidor apos rebuild.

## Testando Mudancas

Executar bun test no tscore apos cada mudanca significativa. Validar comportamento no projeto consumidor manualmente. Adicionar testes unitarios para novas funcionalidades. Manter coverage minimo de 80 por cento conforme verificado por bun test --coverage.

## Removendo Link

Navegar para projeto consumidor e executar npm unlink @carf/tscore. Executar bun install para reinstalar versao publicada do registry. Validar que projeto continua funcionando com versao publicada antes de criar pull request.

## Preparando Pull Request

Executar bun run build e bun test no tscore. Atualizar version em package.json seguindo semver. Documentar mudancas em CHANGELOG. Criar pull request com descricao detalhada de alteracoes. Aguardar review antes de merge e publicacao.
