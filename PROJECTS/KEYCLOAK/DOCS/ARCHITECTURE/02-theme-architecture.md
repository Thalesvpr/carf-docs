# Arquitetura de Temas Keycloak

## Visão Geral

Temas no Keycloak permitem customizar a aparência de todas as interfaces de usuário fornecidas pelo servidor, incluindo páginas de login, console de conta, e emails.

## Estrutura de Tema

### Hierarquia de Temas

```
themes/carf/
├── login/                    # Tema de autenticação
│   ├── theme.properties      # Configurações do tema
│   ├── resources/            # Assets estáticos
│   │   ├── css/
│   │   │   ├── login.css     # Estilos principais
│   │   │   └── styles.css    # Estilos auxiliares
│   │   ├── js/
│   │   │   └── login.js      # Scripts customizados
│   │   └── img/
│   │       ├── logo.svg      # Logo CARF
│   │       ├── favicon.ico
│   │       └── background.jpg
│   ├── login.ftl             # Template de login
│   ├── register.ftl          # Template de registro
│   ├── login-reset-password.ftl
│   ├── login-verify-email.ftl
│   ├── error.ftl
│   └── info.ftl
│
├── account/                  # Tema do console de conta
│   ├── theme.properties
│   ├── resources/
│   │   ├── css/
│   │   │   └── account.css
│   │   └── js/
│   │       └── account.js
│   └── account.ftl
│
├── email/                    # Tema de emails
│   ├── theme.properties
│   ├── html/                 # Templates HTML
│   │   ├── email-verification.ftl
│   │   ├── password-reset.ftl
│   │   ├── event-login_error.ftl
│   │   └── event-update_password.ftl
│   └── text/                 # Templates plain text
│       ├── email-verification.ftl
│       └── password-reset.ftl
│
└── admin/                    # Tema do console admin (opcional)
    ├── theme.properties
    └── resources/
```

## Login Theme - Detalhamento

### theme.properties

```properties
# Tema pai (herança)
parent=keycloak.v2

# Importar estilos do tema pai
import=common/keycloak

# Estilos customizados
styles=css/login.css css/styles.css

# Scripts customizados
scripts=js/login.js

# Meta tags customizadas
meta=viewport=width=device-width,initial-scale=1

# Favicon customizado
favicon=img/favicon.ico

# Localização
locales=pt-BR,en
```

### FreeMarker Templates

Templates utilizam FreeMarker como engine de template. Principais variáveis disponíveis:

#### login.ftl - Página de Login

```ftl
<#import "template.ftl" as layout>
<@layout.registrationLayout displayMessage=!messagesPerField.existsError('username','password'); section>
    <#if section = "header">
        ${msg("loginAccountTitle")}
    <#elseif section = "form">
        <div id="kc-form">
            <div id="kc-form-wrapper">
                <form id="kc-form-login" onsubmit="login.disabled = true; return true;" action="${url.loginAction}" method="post">
                    <div class="${properties.kcFormGroupClass!}">
                        <label for="username" class="${properties.kcLabelClass!}">
                            <#if !realm.loginWithEmailAllowed>${msg("username")}
                            <#elseif !realm.registrationEmailAsUsername>${msg("usernameOrEmail")}
                            <#else>${msg("email")}</#if>
                        </label>
                        <input tabindex="1" id="username" class="${properties.kcInputClass!}" name="username"
                               value="${(login.username!'')}" type="text" autofocus autocomplete="off"
                               aria-invalid="<#if messagesPerField.existsError('username','password')>true</#if>"/>
                    </div>

                    <div class="${properties.kcFormGroupClass!}">
                        <label for="password" class="${properties.kcLabelClass!}">${msg("password")}</label>
                        <input tabindex="2" id="password" class="${properties.kcInputClass!}" name="password"
                               type="password" autocomplete="off"
                               aria-invalid="<#if messagesPerField.existsError('username','password')>true</#if>"/>
                    </div>

                    <div class="${properties.kcFormGroupClass!} ${properties.kcFormSettingClass!}">
                        <div id="kc-form-options">
                            <#if realm.rememberMe && !usernameEditDisabled??>
                                <div class="checkbox">
                                    <label>
                                        <#if login.rememberMe??>
                                            <input tabindex="3" id="rememberMe" name="rememberMe" type="checkbox" checked> ${msg("rememberMe")}
                                        <#else>
                                            <input tabindex="3" id="rememberMe" name="rememberMe" type="checkbox"> ${msg("rememberMe")}
                                        </#if>
                                    </label>
                                </div>
                            </#if>
                        </div>
                        <div class="${properties.kcFormOptionsWrapperClass!}">
                            <#if realm.resetPasswordAllowed>
                                <span><a tabindex="5" href="${url.loginResetCredentialsUrl}">${msg("doForgotPassword")}</a></span>
                            </#if>
                        </div>
                    </div>

                    <div id="kc-form-buttons" class="${properties.kcFormGroupClass!}">
                        <input type="hidden" id="id-hidden-input" name="credentialId"
                               <#if auth.selectedCredential?has_content>value="${auth.selectedCredential}"</#if>/>
                        <input tabindex="4" class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}"
                               name="login" id="kc-login" type="submit" value="${msg("doLogIn")}"/>
                    </div>
                </form>
            </div>
        </div>
    </#if>
</@layout.registrationLayout>
```

### CSS Customizado

#### login.css - Identidade Visual CARF

```css
/* Variáveis CSS para identidade visual */
:root {
    --carf-primary: #2C5F2D;      /* Verde institucional */
    --carf-secondary: #97BC62;    /* Verde claro */
    --carf-accent: #FFB300;       /* Amarelo destaque */
    --carf-background: #F5F5F5;
    --carf-text: #333333;
    --carf-error: #D32F2F;
}

/* Background da página de login */
body {
    background: linear-gradient(135deg, var(--carf-primary) 0%, var(--carf-secondary) 100%);
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Container principal */
#kc-container {
    max-width: 450px;
    margin: 0 auto;
    padding: 2rem;
}

/* Card de login */
#kc-form-wrapper {
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    padding: 3rem;
}

/* Logo CARF */
#kc-header-wrapper {
    text-align: center;
    margin-bottom: 2rem;
}

#kc-header-wrapper img {
    max-width: 200px;
    height: auto;
}

/* Campos de formulário */
.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: var(--carf-text);
    font-weight: 500;
    font-size: 0.875rem;
}

.form-group input[type="text"],
.form-group input[type="password"],
.form-group input[type="email"] {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.form-group input:focus {
    outline: none;
    border-color: var(--carf-primary);
    box-shadow: 0 0 0 3px rgba(44, 95, 45, 0.1);
}

/* Botão de login */
#kc-login {
    width: 100%;
    padding: 1rem;
    background: var(--carf-primary);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

#kc-login:hover {
    background: #234d24;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(44, 95, 45, 0.3);
}

#kc-login:active {
    transform: translateY(0);
}

/* Link "Esqueci minha senha" */
#kc-form-options a {
    color: var(--carf-primary);
    text-decoration: none;
    font-size: 0.875rem;
    transition: color 0.3s ease;
}

#kc-form-options a:hover {
    color: var(--carf-secondary);
    text-decoration: underline;
}

/* Mensagens de erro */
.alert-error {
    background: #FFEBEE;
    border-left: 4px solid var(--carf-error);
    padding: 1rem;
    margin-bottom: 1.5rem;
    border-radius: 4px;
    color: var(--carf-error);
}

/* Checkbox "Lembrar-me" */
.checkbox label {
    display: flex;
    align-items: center;
    font-size: 0.875rem;
}

.checkbox input[type="checkbox"] {
    margin-right: 0.5rem;
}

/* Responsividade */
@media (max-width: 768px) {
    #kc-container {
        padding: 1rem;
    }

    #kc-form-wrapper {
        padding: 2rem 1.5rem;
    }
}
```

## Localização (i18n)

### messages_pt_BR.properties

```properties
# Login
loginAccountTitle=Login - CARF
usernameOrEmail=CPF ou Email
username=CPF
password=Senha
doLogIn=Entrar
rememberMe=Lembrar-me
doForgotPassword=Esqueci minha senha

# Registro
registerTitle=Cadastro - CARF
firstName=Nome
lastName=Sobrenome
email=Email
doRegister=Cadastrar
backToLogin=Voltar ao login

# Erros
invalidUserMessage=CPF ou senha inválidos
accountDisabledMessage=Conta desabilitada. Entre em contato com o administrador.
emailVerifyInstruction1=Um email com instruções foi enviado para {0}.

# Custom messages CARF
carf.welcome=Bem-vindo ao Sistema CARF
carf.description=Sistema de Regularização Fundiária Urbana
carf.support=Suporte: suporte@carf.gov.br
```

## JavaScript Customizado

### login.js

```javascript
// Validação de CPF no cliente
document.addEventListener('DOMContentLoaded', function() {
    const usernameField = document.getElementById('username');

    if (usernameField) {
        usernameField.addEventListener('blur', function() {
            const cpf = this.value.replace(/\D/g, '');

            if (cpf.length === 11) {
                if (!validarCPF(cpf)) {
                    this.classList.add('error');
                    mostrarErro('CPF inválido');
                } else {
                    this.classList.remove('error');
                    esconderErro();
                }
            }
        });

        // Máscara de CPF
        usernameField.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length <= 11) {
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
                this.value = value;
            }
        });
    }
});

function validarCPF(cpf) {
    // Implementação de validação de CPF
    // (pode importar do @carf/tscore)
    // ...
}

function mostrarErro(mensagem) {
    // Implementação de exibição de erro
}

function esconderErro() {
    // Implementação de ocultação de erro
}
```

## Email Theme

### email-verification.ftl

```ftl
<#ftl output_format="HTML">
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #2C5F2D 0%, #97BC62 100%);
            padding: 2rem;
            text-align: center;
        }
        .header img {
            max-width: 180px;
        }
        .content {
            padding: 2rem;
            color: #333;
        }
        .button {
            display: inline-block;
            padding: 1rem 2rem;
            background: #2C5F2D;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            margin: 1.5rem 0;
        }
        .footer {
            background: #f5f5f5;
            padding: 1.5rem;
            text-align: center;
            font-size: 0.875rem;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="${properties.logo!}" alt="CARF Logo">
        </div>
        <div class="content">
            <h2>Verifique seu email</h2>
            <p>Olá,</p>
            <p>Alguém criou uma conta ${realmName} com este endereço de email. Se foi você, clique no link abaixo para verificar seu email:</p>
            <a href="${link}" class="button">Verificar Email</a>
            <p>Este link expira em ${linkExpiration} minutos.</p>
            <p>Se você não criou esta conta, ignore este email.</p>
        </div>
        <div class="footer">
            <p>Sistema CARF - Regularização Fundiária Urbana</p>
            <p>suporte@carf.gov.br</p>
        </div>
    </div>
</body>
</html>
```

## Boas Práticas

1. **Herança de Temas:** Sempre estender temas base (`parent=keycloak.v2`) para aproveitar melhorias do Keycloak
2. **Acessibilidade:** Garantir ARIA labels, contraste adequado, navegação por teclado
3. **Responsividade:** Mobile-first design com breakpoints adequados
4. **Performance:** Minificar CSS/JS, otimizar imagens, lazy loading
5. **i18n:** Sempre usar chaves de mensagem (`${msg("key")}`) ao invés de texto hardcoded
6. **Versionamento:** Manter temas versionados no Git junto com o código

## Referências

- [Keycloak Theme Documentation](https://www.keycloak.org/docs/latest/server_development/#_themes)
- [FreeMarker Documentation](https://freemarker.apache.org/docs/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
