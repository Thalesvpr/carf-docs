---
type: leaf
status: review
updated: 2026-02-07
---

# Testing - ADMIN

## Testes E2E

Os testes end-to-end utilizam Playwright no diretorio e2e/ cobrindo fluxos criticos como login como admin, criar tenant, deletar user e visualizar audit logs. Para executar os testes, utilizar o comando de test e2e via bun que abre browser headless executando testes contra o aplicativo rodando em localhost na porta 5173. Para depuracao, existe o modo UI do Playwright que permite visualizar a execucao passo a passo. Tambem e possivel executar testes especificos passando o nome do modulo como argumento.

## Estrategia de Testes

| Aspecto | Descricao |
|---------|-----------|
| Framework | Playwright com browser headless |
| Ambiente | App local em localhost:5173 |
| Fixtures | Setup de banco em estado conhecido, reset antes de cada teste |
| RBAC | Validacao que usuario sem role ADMIN nao acessa /admin |
| CI | GitHub Actions executa testes em cada PR |

## Exemplo de Fluxo Testado

O teste de criacao de tenant segue o fluxo: o Playwright navega para a pagina de login, preenche credenciais do usuario admin, submete o formulario, navega para a secao de Tenants, clica em novo tenant, preenche o nome do municipio, clica em criar e verifica que o novo municipio aparece na listagem. Este fluxo valida a cadeia completa desde autenticacao ate a persistencia e exibicao do dado criado.

Os testes devem garantir que o banco esteja em estado conhecido usando fixtures que resetam dados antes de cada execucao, e que a validacao de RBAC impeca acesso nao autorizado as rotas administrativas.
