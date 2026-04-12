---
type: leaf
status: review
updated: 2026-01-24
---

# Publicacao

Guia para publicar novas versoes de @carf/tscore no GitHub Packages cobrindo versionamento, tagging e verificacao.

## Versionamento Semantico

Biblioteca segue semver onde MAJOR indica breaking changes, MINOR adiciona funcionalidades compativeis e PATCH corrige bugs. Enquanto em versao 0.x.y, MINOR pode conter breaking changes. Atualizar campo version em package.json antes de publicar.

## Preparando Release

Garantir que main branch esta atualizado com todas mudancas via git pull. Executar bun test para validar suite de testes. Executar bun run build para gerar artefatos de distribuicao. Revisar CHANGELOG com descricao de mudancas desde ultima versao.

## Criando Tag

Executar npm version patch, minor ou major conforme natureza das mudancas. Comando atualiza package.json, cria commit e tag automaticamente. Executar git push origin main --follow-tags para enviar commit e tag ao remote.

## Pipeline Automatizado

GitHub Actions workflow .github/workflows/publish.yml detecta push de tag v*. Pipeline executa checkout, setup de Bun, install, test, lint, type-check e build. Se testes passam, configura .npmrc e executa npm publish com GITHUB_TOKEN do secrets. Pacote aparece em github.com/CARF/packages.

## Verificando Publicacao

Navegar para pagina de packages do repositorio no GitHub. Verificar que nova versao aparece na lista. Em projeto consumidor executar bun update @carf/tscore para obter nova versao. Validar que imports funcionam corretamente.

## Troubleshooting

Se publicacao falha por autenticacao com erro 401, verificar que GITHUB_TOKEN tem permissao write:packages. Se falha por versao duplicada com erro 409, incrementar version em package.json. Se consumidor nao encontra versao, verificar .npmrc aponta para registry correto e limpar cache com bun cache clean. Se erro 403 Forbidden, verificar permissoes de packages na organizacao.
