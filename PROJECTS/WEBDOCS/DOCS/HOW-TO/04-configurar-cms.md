---
type: leaf
status: review
updated: 2026-02-07
---

# Configurar CMS

Guia para configurar Decap CMS permitindo edicao visual de conteudo via interface web.

## Visao Geral

Arquivo de configuracao em public/admin/config.yml define backend, collections e fields. Backend especifica GitHub como storage com branch main e repo path. Collections mapeiam para pastas de conteudo definindo campos editaveis. Configuracao completa documentada em SPECS/15-decap-cms-config.md.

## Setup do GitHub OAuth

Para autenticacao do CMS via GitHub, acessar github.com/settings/developers e criar novo OAuth App. Preencher Application name como CARF WEBDOCS CMS, Homepage URL como https://docs.carf.com.br, e Authorization callback URL como https://docs.carf.com.br/api/auth/callback. Salvar Client ID e Client Secret gerados.

Configurar variaveis de ambiente GITHUB_CLIENT_ID e GITHUB_CLIENT_SECRET com valores copiados do OAuth App.

## Rota de Autenticacao

A API route em src/pages/api/auth/[...auth].ts implementa o fluxo OAuth. Quando path e "auth", redireciona para GitHub OAuth authorize com client_id, redirect_uri e scope repo user. Quando path e "callback", recebe o code, troca por access_token via POST para GitHub, e retorna HTML com script que envia token para janela do CMS via postMessage.

## Widgets Disponiveis

| Widget | Uso |
|---|---|
| string | Texto curto |
| text | Texto longo sem formatacao |
| markdown | Conteudo com editor rich text |
| datetime | Datas com picker |
| select | Lista de opcoes |
| image | Upload com preview |
| list | Campos repetiveis |

## Editorial Workflow

Habilitar publish_mode editorial_workflow em config.yml para fluxo com review. Edicoes criam branches e PRs automaticamente. Review e merge acontecem no GitHub. Desabilitar para fluxo mais simples com commits diretos.

## Checklist de Configuracao

| Item | Status |
|---|---|
| GitHub OAuth App criado | |
| GITHUB_CLIENT_ID configurado | |
| GITHUB_CLIENT_SECRET configurado | |
| public/admin/index.html existe | |
| public/admin/config.yml configurado | |
| Backend name: github | |
| Repo configurado corretamente | |
| Redirect URIs incluem localhost para dev | |
