<#import "template.ftl" as layout>
<@layout.registrationLayout displayMessage=false; section>
    <#if section = "form">
        <div style="text-align: center;">
            <#-- Error icon -->
            <div style="margin-bottom: 1.5rem;">
                <svg width="56" height="56" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" stroke="var(--color-error)" stroke-width="1.5" fill="#fef2f2"/>
                    <path d="M12 8v4" stroke="var(--color-error)" stroke-width="2" stroke-linecap="round"/>
                    <circle cx="12" cy="16" r="1" fill="var(--color-error)"/>
                </svg>
            </div>

            <h2 class="login-title" style="margin-bottom: 12px;">Falha na autenticação</h2>

            <#-- Error message -->
            <div class="alert alert-error" style="text-align: left; margin-bottom: 24px;">
                ${kcSanitize(message.summary)?no_esc}
            </div>

            <p class="login-subtitle" style="margin-bottom: 32px;">
                Verifique suas credenciais e tente novamente.<br>
                Se o problema persistir, entre em contato com o suporte.
            </p>

            <#-- Action buttons -->
            <div style="display: flex; flex-direction: column; gap: 12px;">
                <a href="${url.loginRestartFlowUrl}" class="btn-submit" style="text-decoration: none; text-align: center; display: block;">
                    Tentar novamente
                </a>

                <#if client?? && client.baseUrl?has_content>
                    <a href="${client.baseUrl}" class="btn-secondary" style="text-decoration: none; text-align: center; display: block;">
                        Voltar para a aplicação
                    </a>
                </#if>
            </div>
        </div>
    </#if>
</@layout.registrationLayout>
