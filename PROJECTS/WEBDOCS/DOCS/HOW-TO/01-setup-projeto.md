---
type: leaf
status: review
updated: 2026-02-07
---

# Setup do Projeto

Guia para configurar ambiente de desenvolvimento local do WEBDOCS permitindo executar site, editar conteudo, e testar mudancas antes de commit.

## Pre-requisitos

| Ferramenta | Versao Minima | Verificacao |
|---|---|---|
| Bun | 1.0.0 | Executar bun --version no terminal |
| Node (opcional) | 20.0.0 | Bun inclui runtime proprio mas alguns scripts podem usar Node |
| Git | 2.30 | Executar git --version no terminal |

Extensoes recomendadas para VS Code: astro-build.astro-vscode, unifiedjs.vscode-mdx, dbaeumer.vscode-eslint, e esbenp.prettier-vscode.

## Passos de Configuracao

Clonar repositorio do GitHub executando git clone com URL do repositorio. Navegar para pasta PROJECTS/WEBDOCS/SRC-CODE/carf-webdocs/ onde esta o codigo fonte.

Instalar dependencias executando bun install na raiz do projeto. Comando baixa pacotes definidos em package.json criando node_modules/ e bun.lockb.

Copiar arquivo .env.example para .env.local e preencher variaveis de ambiente. Variaveis necessarias incluem URLs do Keycloak, client ID do client carf-webdocs, e URLs de servicos para status page. Valores de desenvolvimento disponiveis com equipe. Detalhes em SPECS/12-env-vars.md.

Executar servidor de desenvolvimento com bun run dev. Site acessivel em http://localhost:4321 com hot reload automatico. Para pular autenticacao local, configurar variavel SKIP_AUTH=true.

## Verificacao de Funcionamento

| Teste | Acao | Resultado Esperado |
|---|---|---|
| Home page carrega | Acessar http://localhost:4321 | Pagina inicial com sidebar |
| Hot reload funciona | Editar qualquer arquivo .mdx | Browser atualiza automaticamente |
| Build passa | Executar bun run build | Sem erros, dist/ gerado |
| Validacao passa | Executar bun run validate | Sem erros de frontmatter |

## Problemas Comuns

| Erro | Causa | Solucao |
|---|---|---|
| Port 4321 is already in use | Porta ocupada | Matar processo na porta ou usar PORT=4322 bun run dev |
| command not found: bun | Bun nao instalado | Reinstalar Bun ou adicionar ~/.bun/bin ao PATH |
| Variaveis de ambiente invalidas | .env.local ausente | Verificar .env.local configurado conforme .env.example |
| Erros de import ou modulos nao encontrados | node_modules corrompido | Remover node_modules e bun.lockb, executar bun install novamente |
