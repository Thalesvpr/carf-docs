---
type: leaf
status: review
updated: 2026-02-07
---

# Setup Dev Environment - ADMIN

## Setup

O setup do ambiente de desenvolvimento requer Node.js 18 ou superior, ou Bun 1.0 ou superior. Primeiro, clonar o repositorio do ADMIN para o diretorio PROJECTS/ADMIN/SRC-CODE. Em seguida, instalar as dependencias com o gerenciador de pacotes bun. Configurar o arquivo de variaveis de ambiente local (.env.local) definindo VITE_API_URL apontando para localhost na porta 7001 e VITE_KEYCLOAK_URL apontando para localhost na porta 8080. Subir as dependencias de infraestrutura (GEOAPI, Keycloak e PostgreSQL) utilizando docker-compose com o perfil de desenvolvimento na raiz do projeto CARF. Finalmente, iniciar o dev server com bun que abre o aplicativo em localhost na porta 5173 com hot reload habilitado. Apos o servidor iniciar, fazer login com o usuario admin configurado no Keycloak realm e acessar o dashboard em /admin.

## Variaveis de Ambiente

| Variavel | Valor Local | Descricao |
|----------|-------------|-----------|
| VITE_API_URL | http://localhost:7001 | Endereco do GEOAPI local |
| VITE_KEYCLOAK_URL | http://localhost:8080 | Endereco do Keycloak local |

## Dependencias de Infraestrutura

| Servico | Porta | Descricao |
|---------|-------|-----------|
| GEOAPI | 7001 | Backend .NET 9 |
| Keycloak | 8080 | Servidor de autenticacao |
| PostgreSQL | 5432 | Banco de dados |

Todas as dependencias de infraestrutura sao gerenciadas via docker-compose na raiz do projeto CARF, garantindo que o ambiente local replique as condicoes de producao.
