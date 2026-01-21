---
status: review
updated: 2026-01-21
---

# Configurar CMS

Guia para configurar Decap CMS permitindo edição visual de conteúdo via interface web.

Arquivo de configuração em public/admin/config.yml define backend, collections e fields. Backend especifica GitHub como storage com branch main e repo path. Collections mapeiam para pastas de conteúdo definindo campos editáveis.

Configurar autenticação editando backend section para usar OAuth via Keycloak. Adicionar base_url apontando para endpoint OAuth, auth_endpoint para /authorize, e token_endpoint para /token. App ID é client ID do Keycloak.

Testar CMS acessando /admin/ no navegador. Tela de login deve aparecer redirecionando para Keycloak. Após autenticação, interface do CMS deve carregar mostrando collections configuradas.

Adicionar nova collection para seção de conteúdo editando config.yml. Definir name único, label para exibição, folder apontando para pasta de conteúdo, create true para permitir novos documentos, e fields listando campos do frontmatter com tipo de widget apropriado.

Widgets disponíveis incluem string para texto curto, text para texto longo sem formatação, markdown para conteúdo com editor rich text, datetime para datas com picker, select para lista de opções, image para upload com preview, e list para campos repetíveis.

Configurar preview templates opcionalmente para ver como conteúdo aparecerá no site durante edição. Arquivo de preview em public/admin/preview.js define template usando React que renderiza frontmatter e body.

Testar editorial workflow habilitando publish_mode editorial_workflow em config.yml. Edições criam branches e PRs automaticamente. Review e merge acontecem no GitHub. Desabilitar para fluxo mais simples com commits diretos.

## Configuração Completa

A configuração completa do CMS está documentada em **SPECS/15-decap-cms-config.md** incluindo:
- config.yml completo com todas collections
- Configuração de backend GitHub
- Widgets disponíveis
- Preview templates

## Setup do GitHub OAuth

```json
{
  "github_oauth_setup": {
    "steps": [
      "1. Acessar https://github.com/settings/developers",
      "2. Criar novo OAuth App",
      "3. Preencher Application name: CARF WEBDOCS CMS",
      "4. Homepage URL: https://docs.carf.com.br",
      "5. Authorization callback URL: https://docs.carf.com.br/api/auth/callback",
      "6. Salvar Client ID e Client Secret"
    ],
    "env_vars": {
      "GITHUB_CLIENT_ID": "Copiar do GitHub OAuth App",
      "GITHUB_CLIENT_SECRET": "Copiar do GitHub OAuth App"
    }
  }
}
```

## API de Autenticação

```typescript
// src/pages/api/auth/[...auth].ts
import type { APIRoute } from 'astro';

const GITHUB_CLIENT_ID = import.meta.env.GITHUB_CLIENT_ID;
const GITHUB_CLIENT_SECRET = import.meta.env.GITHUB_CLIENT_SECRET;

export const GET: APIRoute = async ({ params, redirect, url }) => {
  const path = params.auth;

  if (path === 'auth') {
    // Redirect to GitHub OAuth
    const authUrl = new URL('https://github.com/login/oauth/authorize');
    authUrl.searchParams.set('client_id', GITHUB_CLIENT_ID);
    authUrl.searchParams.set('redirect_uri', `${url.origin}/api/auth/callback`);
    authUrl.searchParams.set('scope', 'repo user');
    return redirect(authUrl.toString());
  }

  if (path === 'callback') {
    const code = url.searchParams.get('code');

    const tokenRes = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        client_id: GITHUB_CLIENT_ID,
        client_secret: GITHUB_CLIENT_SECRET,
        code
      })
    });

    const { access_token } = await tokenRes.json();

    // Return HTML that posts token to CMS
    return new Response(`
      <script>
        (function() {
          window.opener.postMessage(
            'authorization:github:success:${JSON.stringify({ token: access_token })}',
            window.location.origin
          );
          window.close();
        })()
      </script>
    `, { headers: { 'Content-Type': 'text/html' } });
  }

  return new Response('Not found', { status: 404 });
};
```

## Checklist de Configuração

```json
{
  "checklist": [
    "[ ] GitHub OAuth App criado",
    "[ ] GITHUB_CLIENT_ID configurado",
    "[ ] GITHUB_CLIENT_SECRET configurado",
    "[ ] public/admin/index.html existe",
    "[ ] public/admin/config.yml configurado",
    "[ ] Backend name: github",
    "[ ] Repo configurado corretamente",
    "[ ] Redirect URIs incluem localhost para dev"
  ]
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
