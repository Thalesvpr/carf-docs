---
status: review
updated: 2026-01-21
---

# Setup do Projeto

Guia para configurar ambiente de desenvolvimento local do WEBDOCS permitindo executar site, editar conteúdo, e testar mudanças antes de commit.

Pré-requisitos incluem Bun 1.0+ instalado (runtime e package manager), Git para versionamento, e editor com suporte a TypeScript e Markdown (VS Code recomendado com extensões Astro e MDX).

Clonar repositório do GitHub para diretório local usando git clone seguido da URL do repositório. Navegar para pasta PROJECTS/WEBDOCS/SRC-CODE/carf-webdocs/ onde está o código fonte.

Instalar dependências executando bun install na raiz do projeto. Comando baixa pacotes definidos em package.json criando node_modules/ e bun.lockb.

Copiar arquivo .env.example para .env e preencher variáveis de ambiente. Variáveis necessárias incluem URLs do Keycloak para autenticação, client ID do client carf-webdocs, e URLs de serviços para status page. Valores de desenvolvimento disponíveis com equipe.

Executar servidor de desenvolvimento com bun run dev. Site acessível em http://localhost:4321 com hot reload automático em mudanças de código e conteúdo. Console mostra erros de build e validação.

Testar autenticação acessando /dev/ no navegador. Redirect para Keycloak indica integração funcionando. Login com credenciais de desenvolvedor para acessar seção protegida. Se auth não necessária para desenvolvimento, variável SKIP_AUTH=true desabilita verificação localmente.

## Pré-requisitos Detalhados

```json
{
  "prerequisites": {
    "bun": {
      "version": ">=1.0.0",
      "check": "bun --version",
      "install": "curl -fsSL https://bun.sh/install | bash"
    },
    "node": {
      "version": ">=20.0.0",
      "note": "Opcional - Bun inclui runtime próprio, mas alguns scripts podem usar Node"
    },
    "git": {
      "version": ">=2.30",
      "check": "git --version"
    },
    "vscode_extensions": [
      "astro-build.astro-vscode",
      "unifiedjs.vscode-mdx",
      "dbaeumer.vscode-eslint",
      "esbenp.prettier-vscode"
    ]
  }
}
```

## Comandos de Setup

```bash
# 1. Clonar repositório
git clone https://github.com/carf/carf-webdocs.git
cd carf-webdocs

# 2. Instalar dependências
bun install

# 3. Copiar variáveis de ambiente
cp .env.example .env.local

# 4. Editar .env.local com seus valores
# (ver SPECS/12-env-vars.md para detalhes)

# 5. Iniciar servidor de desenvolvimento
bun run dev

# 6. Verificar no navegador
# http://localhost:4321
```

## Verificação de Funcionamento

```json
{
  "verification_checklist": [
    {
      "test": "Home page carrega",
      "url": "http://localhost:4321",
      "expected": "Página inicial com sidebar"
    },
    {
      "test": "Hot reload funciona",
      "action": "Editar qualquer arquivo .mdx",
      "expected": "Browser atualiza automaticamente"
    },
    {
      "test": "Build passa",
      "command": "bun run build",
      "expected": "Sem erros, dist/ gerado"
    },
    {
      "test": "Validação passa",
      "command": "bun run validate",
      "expected": "Sem erros de frontmatter"
    }
  ]
}
```

## Problemas Comuns

```json
{
  "common_issues": {
    "port_in_use": {
      "error": "Port 4321 is already in use",
      "fix": "Matar processo: kill $(lsof -t -i:4321) ou usar PORT=4322 bun run dev"
    },
    "bun_not_found": {
      "error": "command not found: bun",
      "fix": "Reinstalar Bun ou adicionar ~/.bun/bin ao PATH"
    },
    "env_missing": {
      "error": "Variáveis de ambiente inválidas",
      "fix": "Verificar .env.local está configurado conforme .env.example"
    },
    "node_modules_corrupted": {
      "error": "Erros de import ou módulos não encontrados",
      "fix": "rm -rf node_modules bun.lockb && bun install"
    }
  }
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
