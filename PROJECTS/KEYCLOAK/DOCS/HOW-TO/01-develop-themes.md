# Como Desenvolver Temas para Keycloak

## Pré-requisitos

- Docker instalado
- Editor de código (VS Code recomendado)
- Conhecimento básico de HTML, CSS, JavaScript
- Conhecimento básico de FreeMarker (opcional, aprende rápido)

## Setup do Ambiente de Desenvolvimento

### 1. Estrutura de Diretórios

```bash
cd PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak

# Criar estrutura do tema
mkdir -p themes/carf/login/{resources/{css,js,img},messages}
mkdir -p themes/carf/account/resources/{css,js}
mkdir -p themes/carf/email/{html,text}
```

### 2. Keycloak em Modo Desenvolvimento

Criar `docker-compose.dev.yml`:

```yaml
version: '3.8'

services:
  keycloak:
    image: quay.io/keycloak/keycloak:24.0.0
    command: start-dev
    environment:
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
      KC_HTTP_PORT: 8080
      KC_HOSTNAME_STRICT: false
    ports:
      - "8080:8080"
    volumes:
      - ./themes:/opt/keycloak/themes
      - ./realm-export.json:/opt/keycloak/data/import/realm.json:ro
    command: start-dev --import-realm
```

Iniciar Keycloak:

```bash
docker-compose -f docker-compose.dev.yml up
```

Acessar: http://localhost:8080

### 3. Configuração Inicial do Tema

Criar `themes/carf/login/theme.properties`:

```properties
parent=keycloak.v2
import=common/keycloak

styles=css/login.css
scripts=js/login.js

locales=pt-BR,en

# Meta tags
meta=viewport=width=device-width,initial-scale=1

# Favicon
favicon=img/favicon.ico
```

## Desenvolvimento do Login Theme

### Passo 1: Template Base

Criar `themes/carf/login/template.ftl`:

```ftl
<#macro registrationLayout bodyClass="" displayInfo=false displayMessage=true displayRequiredFields=false>
<!DOCTYPE html>
<html lang="${locale}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex, nofollow">

    <title>${msg("loginTitle",(realm.displayName!''))}</title>

    <#if properties.meta?has_content>
        <#list properties.meta?split(' ') as meta>
            <meta name="${meta?split('=')[0]}" content="${meta?split('=')[1]}"/>
        </#list>
    </#if>

    <link rel="icon" href="${url.resourcesPath}/img/favicon.ico">

    <#if properties.styles?has_content>
        <#list properties.styles?split(' ') as style>
            <link href="${url.resourcesPath}/${style}" rel="stylesheet" />
        </#list>
    </#if>

    <#if properties.scripts?has_content>
        <#list properties.scripts?split(' ') as script>
            <script src="${url.resourcesPath}/${script}" type="text/javascript"></script>
        </#list>
    </#if>
</head>

<body class="${properties.kcBodyClass!} ${bodyClass}">
    <div id="kc-container" class="${properties.kcContainerClass!}">
        <div id="kc-container-wrapper" class="${properties.kcContainerWrapperClass!}">

            <div id="kc-header" class="${properties.kcHeaderClass!}">
                <div id="kc-header-wrapper" class="${properties.kcHeaderWrapperClass!}">
                    <img src="${url.resourcesPath}/img/logo.svg" alt="CARF Logo" />
                    <h1>${msg("carf.title")}</h1>
                    <p>${msg("carf.subtitle")}</p>
                </div>
            </div>

            <div id="kc-content">
                <div id="kc-content-wrapper">

                    <#-- App-initiated actions should not see warning messages about the need to complete the action -->
                    <#-- during login.                                                                               -->
                    <#if displayMessage && message?has_content && (message.type != 'warning' || !isAppInitiatedAction??)>
                        <div class="alert alert-${message.type}">
                            <#if message.type = 'success'><span class="pficon pficon-ok"></span></#if>
                            <#if message.type = 'warning'><span class="pficon pficon-warning-triangle-o"></span></#if>
                            <#if message.type = 'error'><span class="pficon pficon-error-circle-o"></span></#if>
                            <#if message.type = 'info'><span class="pficon pficon-info"></span></#if>
                            <span class="kc-feedback-text">${kcSanitize(message.summary)?no_esc}</span>
                        </div>
                    </#if>

                    <#nested "header">

                    <div id="kc-form">
                        <div id="kc-form-wrapper">
                            <#nested "form">
                        </div>
                    </div>

                    <#if displayInfo>
                        <div id="kc-info" class="${properties.kcSignUpClass!}">
                            <div id="kc-info-wrapper" class="${properties.kcInfoAreaWrapperClass!}">
                                <#nested "info">
                            </div>
                        </div>
                    </#if>

                </div>
            </div>

        </div>
    </div>

    <footer id="kc-footer">
        <p>${msg("carf.footer")}</p>
    </footer>
</body>
</html>
</#macro>
```

### Passo 2: Página de Login

Criar `themes/carf/login/login.ftl`:

```ftl
<#import "template.ftl" as layout>
<@layout.registrationLayout displayMessage=!messagesPerField.existsError('username','password') displayInfo=realm.password && realm.registrationAllowed && !registrationDisabled??; section>
    <#if section = "header">
        <h2 id="kc-page-title">${msg("loginAccountTitle")}</h2>
    <#elseif section = "form">
        <div id="kc-form">
            <div id="kc-form-wrapper">
                <#if realm.password>
                    <form id="kc-form-login" onsubmit="login.disabled = true; return true;" action="${url.loginAction}" method="post">
                        <div class="form-group">
                            <label for="username" class="form-label">
                                <#if !realm.loginWithEmailAllowed>${msg("username")}
                                <#elseif !realm.registrationEmailAsUsername>${msg("usernameOrEmail")}
                                <#else>${msg("email")}</#if>
                            </label>
                            <input tabindex="1" id="username" class="form-control" name="username"
                                   value="${(login.username!'')}" type="text" autofocus autocomplete="off"
                                   placeholder="${msg("username")}"
                                   aria-invalid="<#if messagesPerField.existsError('username','password')>true</#if>" />

                            <#if messagesPerField.existsError('username','password')>
                                <span id="input-error" class="error-message" aria-live="polite">
                                    ${kcSanitize(messagesPerField.getFirstError('username','password'))?no_esc}
                                </span>
                            </#if>
                        </div>

                        <div class="form-group">
                            <label for="password" class="form-label">${msg("password")}</label>
                            <input tabindex="2" id="password" class="form-control" name="password"
                                   type="password" autocomplete="off"
                                   placeholder="${msg("password")}"
                                   aria-invalid="<#if messagesPerField.existsError('username','password')>true</#if>" />
                        </div>

                        <div class="form-options">
                            <#if realm.rememberMe && !usernameEditDisabled??>
                                <div class="checkbox">
                                    <label>
                                        <#if login.rememberMe??>
                                            <input tabindex="3" id="rememberMe" name="rememberMe" type="checkbox" checked>
                                        <#else>
                                            <input tabindex="3" id="rememberMe" name="rememberMe" type="checkbox">
                                        </#if>
                                        ${msg("rememberMe")}
                                    </label>
                                </div>
                            </#if>

                            <#if realm.resetPasswordAllowed>
                                <div class="forgot-password">
                                    <a tabindex="5" href="${url.loginResetCredentialsUrl}">${msg("doForgotPassword")}</a>
                                </div>
                            </#if>
                        </div>

                        <div id="kc-form-buttons">
                            <input type="hidden" id="id-hidden-input" name="credentialId"
                                   <#if auth.selectedCredential?has_content>value="${auth.selectedCredential}"</#if> />
                            <button tabindex="4" class="btn btn-primary btn-block" name="login" id="kc-login" type="submit">
                                ${msg("doLogIn")}
                            </button>
                        </div>
                    </form>
                </#if>
            </div>
        </div>
    <#elseif section = "info" >
        <#if realm.password && realm.registrationAllowed && !registrationDisabled??>
            <div id="kc-registration-container">
                <div id="kc-registration">
                    <span>${msg("noAccount")} <a tabindex="6" href="${url.registrationUrl}">${msg("doRegister")}</a></span>
                </div>
            </div>
        </#if>
    </#if>
</@layout.registrationLayout>
```

### Passo 3: Estilos CSS

Criar `themes/carf/login/resources/css/login.css`:

```css
/* Variáveis CSS */
:root {
    --carf-primary: #2C5F2D;
    --carf-secondary: #97BC62;
    --carf-accent: #FFB300;
    --carf-background: #F5F5F5;
    --carf-text: #333333;
    --carf-error: #D32F2F;
    --carf-border: #E0E0E0;
    --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Reset e base */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: var(--font-family);
    background: linear-gradient(135deg, var(--carf-primary) 0%, var(--carf-secondary) 100%);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 2rem 1rem;
}

/* Container principal */
#kc-container {
    width: 100%;
    max-width: 450px;
}

#kc-container-wrapper {
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    overflow: hidden;
}

/* Header com logo */
#kc-header {
    background: linear-gradient(135deg, var(--carf-primary) 0%, #234d24 100%);
    padding: 3rem 2rem 2rem;
    text-align: center;
    color: white;
}

#kc-header img {
    max-width: 180px;
    height: auto;
    margin-bottom: 1rem;
}

#kc-header h1 {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

#kc-header p {
    font-size: 0.875rem;
    opacity: 0.9;
}

/* Content area */
#kc-content {
    padding: 2.5rem;
}

#kc-page-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--carf-text);
    margin-bottom: 2rem;
    text-align: center;
}

/* Formulário */
.form-group {
    margin-bottom: 1.5rem;
}

.form-label {
    display: block;
    font-weight: 500;
    font-size: 0.875rem;
    color: var(--carf-text);
    margin-bottom: 0.5rem;
}

.form-control {
    width: 100%;
    padding: 0.875rem 1rem;
    font-size: 1rem;
    border: 2px solid var(--carf-border);
    border-radius: 8px;
    transition: all 0.3s ease;
    font-family: inherit;
}

.form-control:focus {
    outline: none;
    border-color: var(--carf-primary);
    box-shadow: 0 0 0 3px rgba(44, 95, 45, 0.1);
}

.form-control[aria-invalid="true"] {
    border-color: var(--carf-error);
}

.error-message {
    display: block;
    margin-top: 0.5rem;
    font-size: 0.875rem;
    color: var(--carf-error);
}

/* Opções do formulário */
.form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    font-size: 0.875rem;
}

.checkbox label {
    display: flex;
    align-items: center;
    cursor: pointer;
}

.checkbox input[type="checkbox"] {
    margin-right: 0.5rem;
}

.forgot-password a {
    color: var(--carf-primary);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}

.forgot-password a:hover {
    color: var(--carf-secondary);
    text-decoration: underline;
}

/* Botões */
.btn {
    display: inline-block;
    padding: 1rem 1.5rem;
    font-size: 1rem;
    font-weight: 600;
    text-align: center;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-family: inherit;
}

.btn-primary {
    background: var(--carf-primary);
    color: white;
}

.btn-primary:hover {
    background: #234d24;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(44, 95, 45, 0.3);
}

.btn-primary:active {
    transform: translateY(0);
}

.btn-block {
    width: 100%;
}

/* Alertas */
.alert {
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
}

.alert-error {
    background: #FFEBEE;
    color: var(--carf-error);
    border-left: 4px solid var(--carf-error);
}

.alert-success {
    background: #E8F5E9;
    color: #2E7D32;
    border-left: 4px solid #2E7D32;
}

.alert-warning {
    background: #FFF3E0;
    color: #F57C00;
    border-left: 4px solid #F57C00;
}

.alert-info {
    background: #E3F2FD;
    color: #1976D2;
    border-left: 4px solid #1976D2;
}

/* Registro */
#kc-registration-container {
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid var(--carf-border);
    text-align: center;
}

#kc-registration a {
    color: var(--carf-primary);
    font-weight: 600;
    text-decoration: none;
}

#kc-registration a:hover {
    text-decoration: underline;
}

/* Footer */
#kc-footer {
    text-align: center;
    padding: 1.5rem;
    color: white;
    font-size: 0.875rem;
    opacity: 0.9;
}

/* Responsividade */
@media (max-width: 576px) {
    body {
        padding: 1rem 0.5rem;
    }

    #kc-content {
        padding: 2rem 1.5rem;
    }

    #kc-header {
        padding: 2rem 1.5rem 1.5rem;
    }

    .form-options {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.75rem;
    }
}

/* Acessibilidade */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* Dark mode (opcional) */
@media (prefers-color-scheme: dark) {
    /* Implementar se necessário */
}
```

### Passo 4: JavaScript Customizado

Criar `themes/carf/login/resources/js/login.js`:

```javascript
// Aguardar carregamento do DOM
document.addEventListener('DOMContentLoaded', function() {
    console.log('Tema CARF carregado');

    // Máscara de CPF para campo username
    const usernameField = document.getElementById('username');
    if (usernameField) {
        // Detectar se é CPF (11 dígitos)
        usernameField.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');

            // Se tem 11 dígitos, aplicar máscara de CPF
            if (value.length <= 11) {
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
                e.target.value = value;
            } else {
                // Truncar se passar de 11
                e.target.value = value.substring(0, 11);
            }
        });
    }

    // Validação básica de formulário
    const loginForm = document.getElementById('kc-form-login');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;

            if (!username || !password) {
                e.preventDefault();
                alert('Por favor, preencha todos os campos.');
                return false;
            }
        });
    }

    // Auto-focus no campo de username
    if (usernameField && !usernameField.value) {
        usernameField.focus();
    }
});
```

### Passo 5: Internacionalização

Criar `themes/carf/login/messages/messages_pt_BR.properties`:

```properties
# Título e cabeçalho
loginAccountTitle=Entre com sua conta
carf.title=Sistema CARF
carf.subtitle=Regularização Fundiária Urbana
carf.footer=© 2025 CARF - Todos os direitos reservados

# Campos
username=CPF
usernameOrEmail=CPF ou Email
email=Email
password=Senha
rememberMe=Lembrar-me neste dispositivo
doForgotPassword=Esqueci minha senha

# Botões
doLogIn=Entrar
doRegister=Criar uma conta
doCancel=Cancelar
doSubmit=Enviar

# Registro
noAccount=Não tem uma conta?
registerTitle=Criar Conta

# Mensagens de erro
invalidUserMessage=CPF ou senha inválidos
loginTimeout=Sua sessão expirou. Por favor, faça login novamente.
accountDisabledMessage=Sua conta está desabilitada. Entre em contato com o suporte.
accountTemporarilyDisabledMessage=Sua conta está temporariamente bloqueada devido a muitas tentativas de login. Tente novamente mais tarde.
invalidPasswordExistingMessage=Senha inválida.
invalidPasswordMinLengthMessage=Senha inválida: tamanho mínimo {0}.

# Mensagens de sucesso
emailVerifyInstruction1=Um email de verificação foi enviado para {0}.
emailVerifyInstruction2=Não recebeu o código? Clique <a href="{0}">aqui</a> para reenviar.

# LGPD
termsTitle=Termos de Uso e Política de Privacidade
termsText=Ao se cadastrar, você concorda com nossos Termos de Uso e Política de Privacidade conforme a LGPD.
termsAccept=Li e aceito os termos
```

## Teste do Tema

### 1. Ativar o Tema

Acessar Admin Console: http://localhost:8080

1. Login com `admin/admin`
2. Selecionar realm `carf`
3. Realm Settings → Themes
4. Login Theme: `carf`
5. Salvar

### 2. Testar Páginas

- **Login:** http://localhost:8080/realms/carf/account
- **Registro:** Ativar em Realm Settings → Login → User Registration
- **Esqueci senha:** Clicar no link na página de login

### 3. Hot Reload

Mudanças em CSS/JS são recarregadas automaticamente.
Templates (.ftl) podem precisar de refresh do cache:
```bash
docker-compose -f docker-compose.dev.yml restart
```

## Debugging

### Browser DevTools

1. F12 para abrir DevTools
2. Inspector para verificar HTML/CSS
3. Console para ver erros JavaScript
4. Network para verificar carregamento de recursos

### Logs do Keycloak

```bash
docker-compose -f docker-compose.dev.yml logs -f keycloak
```

### Verificar Template Errors

Templates FreeMarker com erros mostram stack trace no navegador (em modo dev).

## Build para Produção

### 1. Minificar CSS/JS

```bash
# Instalar minificadores
npm install -g csso-cli uglify-js

# Minificar
csso themes/carf/login/resources/css/login.css -o themes/carf/login/resources/css/login.min.css
uglifyjs themes/carf/login/resources/js/login.js -o themes/carf/login/resources/js/login.min.js
```

### 2. Atualizar theme.properties

```properties
styles=css/login.min.css
scripts=js/login.min.js
```

### 3. Build da Imagem Docker

```bash
docker build -t carf-keycloak:latest -f docker/Dockerfile.custom .
```

## Próximos Passos

1. [ ] Desenvolver tema de Account
2. [ ] Desenvolver tema de Email
3. [ ] Adicionar mais páginas (register.ftl, error.ftl)
4. [ ] Implementar testes automatizados
5. [ ] Documentar guia de contribuição

## Referências

- [Keycloak Theme SPI](https://www.keycloak.org/docs/latest/server_development/#_themes)
- [FreeMarker Documentation](https://freemarker.apache.org/docs/)
- [CSS Variables (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
