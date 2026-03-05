<#import "template.ftl" as layout>
<@layout.registrationLayout displayInfo=false; section>
    <#if section = "form">
        <h2 class="login-title">Esqueceu sua senha?</h2>
        <p class="login-subtitle">Digite seu e-mail para receber instruções</p>

        <#if message?has_content && (message.type != 'warning' || !isAppInitiatedAction??)>
            <div class="alert alert-${message.type}">${kcSanitize(message.summary)?no_esc}</div>
        </#if>

        <form id="kc-reset-password-form" action="${url.loginAction}" method="post">
            <div class="field">
                <label for="username">
                    <#if !realm.loginWithEmailAllowed>${msg("username")}<#elseif !realm.registrationEmailAsUsername>${msg("usernameOrEmail")}<#else>${msg("email")}</#if>
                </label>
                <input type="text" id="username" name="username" autofocus
                       value="${(auth.attemptedUsername!'')}"
                       placeholder="${msg("usernamePlaceholder")}"
                       autocomplete="username"
                       aria-invalid="<#if messagesPerField.existsError('username')>true</#if>"
                />
                <#if messagesPerField.existsError('username')>
                    <span class="field-error" aria-live="polite">
                        ${kcSanitize(messagesPerField.get('username'))?no_esc}
                    </span>
                </#if>
            </div>

            <div class="reset-info">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16">
                    <circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>
                </svg>
                <span>Enviaremos um e-mail com instruções para criar uma nova senha.</span>
            </div>

            <button type="submit" class="btn-submit">Enviar</button>

            <p class="back-to-login">
                <a href="${url.loginUrl}">&laquo; Voltar para o login</a>
            </p>
        </form>

    <#elseif section = "info">
    </#if>
</@layout.registrationLayout>
