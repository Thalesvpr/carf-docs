---
status: review
updated: 2026-01-17
---

# Setup do Projeto

Guia para configurar ambiente de desenvolvimento local do WEBDOCS permitindo executar site, editar conteúdo, e testar mudanças antes de commit.

Pré-requisitos incluem Bun 1.0+ instalado (runtime e package manager), Git para versionamento, e editor com suporte a TypeScript e Markdown (VS Code recomendado com extensões Astro e MDX).

Clonar repositório do GitHub para diretório local usando git clone seguido da URL do repositório. Navegar para pasta PROJECTS/WEBDOCS/SRC-CODE/carf-webdocs/ onde está o código fonte.

Instalar dependências executando bun install na raiz do projeto. Comando baixa pacotes definidos em package.json criando node_modules/ e bun.lockb.

Copiar arquivo .env.example para .env e preencher variáveis de ambiente. Variáveis necessárias incluem URLs do Keycloak para autenticação, client ID do client carf-webdocs, e URLs de serviços para status page. Valores de desenvolvimento disponíveis com equipe.

Executar servidor de desenvolvimento com bun run dev. Site acessível em http://localhost:4321 com hot reload automático em mudanças de código e conteúdo. Console mostra erros de build e validação.

Testar autenticação acessando /dev/ no navegador. Redirect para Keycloak indica integração funcionando. Login com credenciais de desenvolvedor para acessar seção protegida. Se auth não necessária para desenvolvimento, variável SKIP_AUTH=true desabilita verificação localmente.
