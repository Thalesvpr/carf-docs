---
type: leaf
status: review
updated: 2026-02-07
---

# Troubleshooting - ADMIN

## Problemas Comuns

Esta secao documenta os problemas mais frequentes encontrados durante desenvolvimento e operacao do REURBMASTER, com diagnostico e solucao para cada caso.

## Tabela de Problemas e Solucoes

| Problema | Diagnostico | Solucao |
|----------|-------------|---------|
| 401 Unauthorized ao acessar /admin | JWT nao contem role ADMIN ou SUPER_ADMIN, ou VITE_KEYCLOAK_URL incorreto | Verificar roles do usuario no Keycloak, validar variavel de ambiente, limpar localStorage e refazer login |
| API calls falhando | Erro CORS indica VITE_API_URL incorreto; timeout indica GEOAPI lento | Verificar VITE_API_URL no console do navegador, confirmar que aponta para GEOAPI na porta correta |
| Estilos nao carregando | Build nao incluiu classes Tailwind do shadcn/ui | Executar build completo via bun, limpar cache do navegador |
| Nao consegue deletar tenant | Tenant possui dependencias como unidades ou usuarios | GEOAPI retorna erro detalhado na response com lista de dependencias que devem ser removidas primeiro |
| Protected routes nao funcionando | React Router ou middleware de validacao de role com configuracao incorreta | Verificar configuracao do React Router e que o middleware de role esta sendo executado corretamente |

## Resolucao de Erro 401

Para resolver o erro 401, limpar todos os tokens armazenados no localStorage do navegador, recarregar a pagina e fazer login novamente. Se o problema persistir, verificar no Keycloak que o usuario possui a role ADMIN ou SUPER_ADMIN atribuida corretamente.

## Resolucao de Erro CORS

Para diagnosticar erros CORS, inspecionar o console do navegador e verificar se a variavel VITE_API_URL aponta corretamente para o endereco do GEOAPI, como por exemplo localhost na porta 7001 para ambiente de desenvolvimento.
