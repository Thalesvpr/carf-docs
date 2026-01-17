# Conceitos: Keycloak Themes

## O que são Temas no Keycloak?

Temas no Keycloak são um mecanismo de customização visual que permite modificar a aparência de todas as interfaces de usuário fornecidas pelo servidor sem alterar o código-fonte do Keycloak.

## Tipos de Temas

### 1. Login Theme
Interface de autenticação e registro de usuários.

**Páginas incluídas:**
- Login
- Registro
- Esqueci minha senha
- Verificação de email
- Erro de autenticação
- Informações (sucesso/avisos)
- Login OTP (One-Time Password)
- WebAuthn

### 2. Account Theme
Console de autoatendimento do usuário.

**Funcionalidades:**
- Gerenciamento de perfil
- Alteração de senha
- Configuração de 2FA
- Gerenciamento de sessões ativas
- Aplicativos autorizados
- Logs de atividades

### 3. Admin Theme
Console administrativo do Keycloak (geralmente não customizado).

### 4. Email Theme
Templates de emails transacionais.

**Tipos de email:**
- Verificação de email
- Resetar senha
- Notificação de login
- Atualização de senha
- Eventos customizados

## Estrutura de um Tema

```
themes/
└── meu-tema/
    ├── login/
    │   ├── theme.properties      # Configurações
    │   ├── resources/            # Assets (CSS, JS, imagens)
    │   ├── messages/             # Traduções (i18n)
    │   └── *.ftl                 # Templates FreeMarker
    ├── account/
    ├── email/
    └── common/                   # Recursos compartilhados
```

## theme.properties

Arquivo de configuração principal do tema.

```properties
# Herança de tema pai
parent=keycloak.v2

# Estilos
styles=css/main.css css/custom.css

# Scripts
scripts=js/app.js

# Importar recursos do pai
import=common/keycloak

# Localização
locales=pt-BR,en,es
```

## Templates FreeMarker (.ftl)

Keycloak usa FreeMarker como engine de templates.

### Variáveis Disponíveis

```ftl
${realm.name}                    <!-- Nome do realm -->
${url.loginAction}               <!-- URL do action do form -->
${msg("key")}                    <!-- Mensagem internacionalizada -->
${properties.kcFormClass}        <!-- Classe CSS do tema pai -->
${login.username}                <!-- Username do login -->
${user.email}                    <!-- Email do usuário -->
${auth.attemptedUsername}        <!-- Tentativa de login -->
```

### Exemplo de Template

```ftl
<#import "template.ftl" as layout>
<@layout.registrationLayout displayMessage=true; section>
    <#if section = "header">
        ${msg("loginTitle")}
    <#elseif section = "form">
        <form action="${url.loginAction}" method="post">
            <input type="text" name="username" value="${(login.username!'')}"/>
            <input type="password" name="password"/>
            <button type="submit">${msg("doLogIn")}</button>
        </form>
    </#if>
</@layout.registrationLayout>
```

## Herança de Temas

Temas podem estender outros temas usando `parent=nome-do-tema`.

**Vantagens:**
- Reutilizar templates e estilos do tema pai
- Override seletivo apenas do necessário
- Manter compatibilidade com atualizações do Keycloak

**Exemplo:**
```properties
parent=keycloak.v2
```

Isso herda todo o tema `keycloak.v2` e você só customiza o que precisa.

## Internacionalização (i18n)

### Estrutura de Mensagens

```
themes/meu-tema/login/messages/
├── messages_en.properties
├── messages_pt_BR.properties
└── messages_es.properties
```

### messages_pt_BR.properties

```properties
loginTitle=Login no Sistema
username=Nome de usuário
password=Senha
doLogIn=Entrar
invalidUserMessage=Usuário ou senha inválidos
```

### Uso nos Templates

```ftl
<h1>${msg("loginTitle")}</h1>
<label>${msg("username")}</label>
```

## CSS e JavaScript

### CSS

```css
/* themes/meu-tema/login/resources/css/login.css */
:root {
    --primary-color: #2C5F2D;
}

body {
    font-family: Arial, sans-serif;
    background: var(--primary-color);
}

#kc-form-login {
    max-width: 400px;
    margin: 0 auto;
}
```

### JavaScript

```javascript
// themes/meu-tema/login/resources/js/login.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('Tema CARF carregado');

    // Custom validation
    const form = document.getElementById('kc-form-login');
    form.addEventListener('submit', function(e) {
        // Validações customizadas
    });
});
```

## Recursos Estáticos

### Imagens

```
themes/meu-tema/login/resources/img/
├── logo.svg
├── background.jpg
└── favicon.ico
```

### Referência nos Templates

```ftl
<img src="${url.resourcesPath}/img/logo.svg" alt="Logo">
```

### CSS

```css
background-image: url('../img/background.jpg');
```

## Email Templates

### Estrutura

```
themes/meu-tema/email/
├── html/
│   ├── email-verification.ftl
│   ├── password-reset.ftl
│   └── event-login_error.ftl
└── text/
    ├── email-verification.ftl
    └── password-reset.ftl
```

### Variáveis Disponíveis em Emails

```ftl
${user.username}              <!-- Username do destinatário -->
${user.email}                 <!-- Email do destinatário -->
${realmName}                  <!-- Nome do realm -->
${link}                       <!-- Link de ação -->
${linkExpiration}             <!-- Tempo de expiração do link -->
${event.type}                 <!-- Tipo de evento -->
```

## Deployment de Temas

### Desenvolvimento

```bash
# Copiar tema para diretório do Keycloak
cp -r themes/carf /opt/keycloak/themes/

# Hot reload (modo dev)
docker run -v ./themes:/opt/keycloak/themes quay.io/keycloak/keycloak:24.0.0 start-dev
```

### Produção

```dockerfile
FROM quay.io/keycloak/keycloak:24.0.0
COPY themes/carf /opt/keycloak/themes/carf
```

### Ativação do Tema

Via Admin Console:
1. Realm Settings → Themes
2. Login Theme: `carf`
3. Account Theme: `carf`
4. Email Theme: `carf`

Via realm export:
```json
{
  "loginTheme": "carf",
  "accountTheme": "carf",
  "emailTheme": "carf"
}
```

## Boas Práticas

### 1. Sempre Usar Herança
```properties
parent=keycloak.v2
```
Aproveita melhorias e correções do tema base.

### 2. Manter i18n Consistente
Todas as strings devem estar em `messages_*.properties`.

### 3. Acessibilidade
- ARIA labels
- Contraste adequado (WCAG 2.1 AA)
- Navegação por teclado
- Screen reader friendly

### 4. Responsividade
```css
@media (max-width: 768px) {
    #kc-container {
        padding: 1rem;
    }
}
```

### 5. Performance
- Minificar CSS/JS
- Otimizar imagens (WebP, compressão)
- Lazy loading quando possível

### 6. Versionamento
Manter temas no Git junto com o código.

### 7. Testes
- Testar todos os fluxos (login, registro, reset password)
- Testar em diferentes browsers
- Testar mobile e desktop
- Testar dark mode (se aplicável)

## Limitações

1. **Não pode alterar lógica do servidor** - Temas são apenas para UI
2. **Templates FreeMarker fixos** - Estrutura de variáveis é definida pelo Keycloak
3. **Cache agressivo** - Pode precisar limpar cache do browser durante desenvolvimento
4. **Compatibilidade** - Temas podem quebrar em major updates do Keycloak

## Troubleshooting

### Tema não aparece
- Verificar nome do diretório
- Verificar permissões de arquivo
- Limpar cache do Keycloak: `rm -rf standalone/data/cache`

### CSS não carrega
- Verificar `styles=` em `theme.properties`
- Verificar caminho dos arquivos CSS
- Inspecionar console do browser

### Mensagens não traduzidas
- Verificar `messages_*.properties` existe
- Verificar `locales=` em `theme.properties`
- Verificar uso de `${msg("key")}` nos templates

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Muitas listas com bullets (42) antes do rodapé - considerar converter para parágrafo denso; Contém code blocks - considerar converter para prosa.
