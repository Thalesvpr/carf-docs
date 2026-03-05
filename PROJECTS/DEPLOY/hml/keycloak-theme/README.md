# Tema CARF - Keycloak

Tema customizado Keycloak implementando identidade visual CARF para páginas de autenticação login registro reset-password com layout split-screen responsivo verde institucional painel esquerdo formulário branco painel direito.

## Estrutura

```
themes/carf/
├── login/
│   ├── theme.properties     # Config parent=base styles locales
│   ├── template.ftl         # Macro registrationLayout split-screen
│   ├── login.ftl            # Página login CPF/email senha
│   ├── register.ftl         # Página cadastro usuário
│   ├── login-reset-password.ftl  # Reset senha
│   ├── error.ftl            # Página erro
│   ├── info.ftl             # Página informações
│   ├── messages/
│   │   ├── messages_pt_BR.properties  # i18n português
│   │   └── messages_en.properties     # i18n inglês
│   └── resources/
│       ├── css/login.css    # Estilos responsivos
│       ├── js/              # Validações client-side
│       └── img/             # Logo favicon
├── account/
│   ├── theme.properties
│   ├── account.ftl
│   ├── password.ftl
│   ├── messages/
│   └── resources/css/
└── email/
    ├── theme.properties
    ├── html/                # Templates HTML emails
    ├── text/                # Templates texto plain
    └── messages/
```

## Teste Local

1. Iniciar Keycloak dev mode:
```bash
docker-compose -f docker-compose.dev.yml up
```

2. Acessar Admin Console:
```
http://localhost:8080
admin / admin
```

3. Configurar tema:
```
Realm Settings > Themes > Login Theme > carf
```

4. Testar login:
```
http://localhost:8080/realms/carf/account
```

## Hot Reload

- CSS/JS: Alterações refletem automaticamente (reload página)
- Templates .ftl: Requer restart container

## Documentação

- [06-login-theme-carf.md](../../../DOCS/FEATURES/06-login-theme-carf.md) - Detalhes implementação
- [01-develop-themes.md](../../../DOCS/HOW-TO/01-develop-themes.md) - Guia desenvolvimento
- [05-theme-customization.md](../../../DOCS/FEATURES/05-theme-customization.md) - Visão geral temas

---

**Última atualização:** 2026-01-19

<!-- CARF-INDEX-START -->
## Subpastas

- [[PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/themes/carf/account/README|account]]
- [[PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/themes/carf/email/README|email]]
- [[PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/themes/carf/login/README|login]]

<!-- CARF-INDEX-END -->
