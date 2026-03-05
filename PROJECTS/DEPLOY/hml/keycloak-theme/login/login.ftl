<#import "template.ftl" as layout>
<@layout.registrationLayout displayInfo=realm.password && realm.registrationAllowed && !registrationDisabled??; section>
    <#if section = "form">
        <#--
            Mapeamento clientId -> displayName
            Fonte canônica: CENTRAL/ECOSYSTEM/applications.json
            Manter sincronizado com o registro de aplicações do ecossistema.
        -->
        <#assign clientDisplayNames = {
            "reurbweb":        "REURBWEB",
            "reurbmaster":     "REURBMASTER",
            "geoweb":          "GeoWeb",
            "reurbcad":        "REURBCAD Mobile",
            "geoapi":          "GeoAPI",
            "geogis":          "GeoGIS",
            "webdocs":         "WebDocs",
            "admin":           "Painel Admin",
            "account":         "Account Console",
            "account-console": "Account Console",
            "admin-cli":       "Admin CLI"
        }>

        <h2 class="login-title">Entrar no CARF</h2>
        <#if client?? && client.clientId?has_content>
            <#assign displayName = clientDisplayNames[client.clientId]!client.clientId>
            <p class="login-subtitle">Para acessar <strong>${displayName}</strong></p>
        <#else>
            <p class="login-subtitle">Acesse sua conta</p>
        </#if>

        <#if message?has_content && (message.type != 'warning' || !isAppInitiatedAction??)>
            <div class="alert alert-${message.type}">${kcSanitize(message.summary)?no_esc}</div>
        </#if>

        <form action="${url.loginAction}" method="post">
            <div class="field">
                <label for="username">E-mail ou Usuário</label>
                <input type="text" id="username" name="username" value="${(login.username!'')}"
                       placeholder="Digite seu e-mail ou usuário" autofocus autocomplete="username">
            </div>

            <div class="field">
                <label for="password">Senha</label>
                <div class="password-wrapper">
                    <input type="password" id="password" name="password"
                           placeholder="Digite sua senha" autocomplete="current-password">
                    <button type="button" class="password-toggle" aria-label="Mostrar senha" tabindex="-1">
                        <svg class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                            <circle cx="12" cy="12" r="3"/>
                        </svg>
                        <svg class="eye-off-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none">
                            <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
                            <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
                            <path d="M14.12 14.12a3 3 0 1 1-4.24-4.24"/>
                            <line x1="1" y1="1" x2="23" y2="23"/>
                        </svg>
                    </button>
                </div>
            </div>

            <div class="options">
                <#if realm.rememberMe && !usernameHidden??>
                    <label class="remember">
                        <input type="checkbox" name="rememberMe" <#if login.rememberMe??>checked</#if>>
                        <span>Lembrar-me</span>
                    </label>
                </#if>
                <#if realm.resetPasswordAllowed>
                    <a href="${url.loginResetCredentialsUrl}" class="forgot">Esqueceu a senha?</a>
                </#if>
            </div>

            <button type="submit" class="btn-submit">Entrar</button>
        </form>

        <#if realm.password && realm.registrationAllowed && !registrationDisabled??>
            <p class="register">Não tem uma conta? <a href="${url.registrationUrl}">Criar conta</a></p>
        </#if>

    <#elseif section = "info">
    </#if>
</@layout.registrationLayout>
