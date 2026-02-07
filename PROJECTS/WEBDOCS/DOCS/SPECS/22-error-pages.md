---
type: leaf
status: review
updated: 2026-01-21
---

# Error Pages

Templates de páginas de erro customizadas para WEBDOCS. Páginas substituem defaults do Astro/Starlight com design consistente e mensagens úteis para usuários.

## Visão Geral

```json
{
  "error_pages": {
    "404": {
      "path": "src/pages/404.astro",
      "trigger": "Página não encontrada",
      "user_action": "Buscar ou voltar para home"
    },
    "403": {
      "path": "src/pages/403.astro",
      "trigger": "Acesso negado por role",
      "user_action": "Contatar admin ou logout"
    },
    "500": {
      "path": "src/pages/500.astro",
      "trigger": "Erro interno do servidor",
      "user_action": "Tentar novamente ou reportar"
    }
  }
}
```

## Template 404 - Página Não Encontrada

```json
{
  "page_404": {
    "http_status": 404,
    "title": "Página não encontrada",
    "heading": "404",
    "subheading": "Ops! Esta página não existe",
    "message": "A página que você procura pode ter sido movida, renomeada ou não existe mais.",
    "actions": [
      {
        "label": "Voltar para Home",
        "href": "/",
        "primary": true
      },
      {
        "label": "Buscar documentação",
        "href": "/?search=",
        "primary": false
      }
    ],
    "suggestions": {
      "show": true,
      "title": "Você pode estar procurando:",
      "links": [
        { "label": "Guia do Usuário", "href": "/guia/" },
        { "label": "Manuais", "href": "/manuais/" },
        { "label": "Status dos Serviços", "href": "/status/" }
      ]
    }
  }
}
```

Estrutura Astro:

```astro
---
// src/pages/404.astro
import BaseLayout from '../layouts/BaseLayout.astro';

const suggestions = [
  { label: 'Guia do Usuário', href: '/guia/' },
  { label: 'Manuais', href: '/manuais/' },
  { label: 'Status dos Serviços', href: '/status/' }
];
---

<BaseLayout title="Página não encontrada" description="A página solicitada não foi encontrada.">
  <main class="error-page error-404">
    <div class="error-content">
      <h1 class="error-code">404</h1>
      <h2 class="error-title">Ops! Esta página não existe</h2>
      <p class="error-message">
        A página que você procura pode ter sido movida, renomeada ou não existe mais.
      </p>
      <div class="error-actions">
        <a href="/" class="btn btn-primary">Voltar para Home</a>
        <a href="/?search=" class="btn btn-secondary">Buscar documentação</a>
      </div>
      <div class="error-suggestions">
        <p>Você pode estar procurando:</p>
        <ul>
          {suggestions.map(link => (
            <li><a href={link.href}>{link.label}</a></li>
          ))}
        </ul>
      </div>
    </div>
  </main>
</BaseLayout>
```

## Template 403 - Acesso Negado

```json
{
  "page_403": {
    "http_status": 403,
    "title": "Acesso negado",
    "heading": "403",
    "subheading": "Você não tem permissão para acessar esta página",
    "message_template": "Esta seção requer uma das seguintes permissões: {allowed_roles}",
    "current_user": {
      "show": true,
      "format": "Você está autenticado como {email} com roles: {roles}"
    },
    "actions": [
      {
        "label": "Voltar para Home",
        "href": "/",
        "primary": true
      },
      {
        "label": "Fazer logout",
        "href": "/auth/logout",
        "primary": false
      }
    ],
    "contact": {
      "show": true,
      "message": "Se você acredita que deveria ter acesso, entre em contato com o administrador."
    }
  }
}
```

Estrutura Astro:

```astro
---
// src/pages/403.astro
import BaseLayout from '../layouts/BaseLayout.astro';

const { locals } = Astro;
const user = locals.user;

// Roles que permitem acesso à seção atual (passado via middleware)
const allowedRoles = locals.allowedRoles || ['admin', 'super-admin', 'dev'];

const roleLabels: Record<string, string> = {
  'user': 'Usuário',
  'field-cadastrator': 'Cadastrador de Campo',
  'field-coordinator': 'Coordenador de Campo',
  'analyst': 'Analista',
  'admin': 'Administrador',
  'super-admin': 'Super Administrador',
  'dev': 'Desenvolvedor'
};
---

<BaseLayout title="Acesso negado" description="Você não tem permissão para acessar esta página.">
  <main class="error-page error-403">
    <div class="error-content">
      <h1 class="error-code">403</h1>
      <h2 class="error-title">Você não tem permissão para acessar esta página</h2>
      <p class="error-message">
        Esta seção requer uma das seguintes permissões:
      </p>
      <ul class="allowed-roles">
        {allowedRoles.map(role => (
          <li class="role-badge">{roleLabels[role] || role}</li>
        ))}
      </ul>
      {user && (
        <div class="current-user">
          <p>
            Você está autenticado como <strong>{user.email}</strong>
          </p>
          <p>
            Suas permissões: {user.roles.map(r => roleLabels[r] || r).join(', ')}
          </p>
        </div>
      )}
      <div class="error-actions">
        <a href="/" class="btn btn-primary">Voltar para Home</a>
        <a href="/auth/logout" class="btn btn-secondary">Fazer logout</a>
      </div>
      <p class="contact-admin">
        Se você acredita que deveria ter acesso, entre em contato com o administrador do sistema.
      </p>
    </div>
  </main>
</BaseLayout>
```

## Template 500 - Erro Interno

```json
{
  "page_500": {
    "http_status": 500,
    "title": "Erro interno",
    "heading": "500",
    "subheading": "Algo deu errado",
    "message": "Ocorreu um erro inesperado. Nossa equipe foi notificada e está trabalhando para resolver.",
    "actions": [
      {
        "label": "Tentar novamente",
        "onclick": "window.location.reload()",
        "primary": true
      },
      {
        "label": "Voltar para Home",
        "href": "/",
        "primary": false
      }
    ],
    "debug_info": {
      "show_in_dev": true,
      "show_in_prod": false
    },
    "report": {
      "show": true,
      "message": "Se o problema persistir, entre em contato com o suporte."
    }
  }
}
```

Estrutura Astro:

```astro
---
// src/pages/500.astro
import BaseLayout from '../layouts/BaseLayout.astro';

const isDev = import.meta.env.DEV;
const error = Astro.props.error;
---

<BaseLayout title="Erro interno" description="Ocorreu um erro inesperado no servidor.">
  <main class="error-page error-500">
    <div class="error-content">
      <h1 class="error-code">500</h1>
      <h2 class="error-title">Algo deu errado</h2>
      <p class="error-message">
        Ocorreu um erro inesperado. Nossa equipe foi notificada e está trabalhando para resolver.
      </p>
      <div class="error-actions">
        <button onclick="window.location.reload()" class="btn btn-primary">
          Tentar novamente
        </button>
        <a href="/" class="btn btn-secondary">Voltar para Home</a>
      </div>
      {isDev && error && (
        <details class="error-debug">
          <summary>Detalhes do erro (apenas em desenvolvimento)</summary>
          <pre>{error.message}</pre>
          <pre>{error.stack}</pre>
        </details>
      )}
      <p class="contact-support">
        Se o problema persistir, entre em contato com o suporte técnico.
      </p>
    </div>
  </main>
</BaseLayout>
```

## CSS Compartilhado

```json
{
  "css_location": "src/styles/error-pages.css",
  "import_in": "src/layouts/BaseLayout.astro ou astro.config.mjs customCss"
}
```

```css
/* src/styles/error-pages.css */
.error-page {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
}

.error-content {
  max-width: 500px;
}

.error-code {
  font-size: 6rem;
  font-weight: 700;
  color: var(--sl-color-accent);
  line-height: 1;
  margin: 0;
}

.error-title {
  font-size: 1.5rem;
  margin: 1rem 0;
  color: var(--sl-color-text);
}

.error-message {
  color: var(--sl-color-text-accent);
  margin-bottom: 2rem;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: var(--sl-color-accent);
  color: var(--sl-color-bg);
}

.btn-primary:hover {
  opacity: 0.9;
}

.btn-secondary {
  background: var(--sl-color-gray-6);
  color: var(--sl-color-text);
}

.btn-secondary:hover {
  background: var(--sl-color-gray-5);
}

.allowed-roles {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  flex-wrap: wrap;
  list-style: none;
  padding: 0;
  margin: 1rem 0 2rem;
}

.role-badge {
  background: var(--sl-color-gray-6);
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
}

.current-user {
  background: var(--sl-color-gray-7);
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
}

.error-suggestions ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.error-suggestions a {
  color: var(--sl-color-accent);
}

.contact-admin,
.contact-support {
  font-size: 0.875rem;
  color: var(--sl-color-text-accent);
}

.error-debug {
  text-align: left;
  background: var(--sl-color-gray-7);
  padding: 1rem;
  border-radius: 0.5rem;
  margin: 1rem 0;
}

.error-debug pre {
  overflow-x: auto;
  font-size: 0.75rem;
}
```

## Integração com Middleware

O middleware deve passar informações para a página 403:

```json
{
  "middleware_to_403": {
    "set_locals": {
      "allowedRoles": ["array de roles que permitem acesso"],
      "requestedSection": "seção que usuário tentou acessar"
    },
    "redirect_method": "Astro.rewrite('/403') ou Response.redirect"
  }
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
