<#import "template.ftl" as layout>
<@layout.registrationLayout displayMessage=false; section>
    <#if section = "form">
        <div id="kc-info-message" style="text-align: center;">
            <#-- Ícone de sucesso -->
            <div style="margin-bottom: 1.5rem;">
                <svg width="56" height="56" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" stroke="var(--carf-success)" stroke-width="1.5" fill="#f0fdf4"/>
                    <path d="M9 12l2 2 4-4" stroke="var(--carf-success)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>

            <h2 class="login-title" style="margin-bottom: 12px;">${msg("infoTitle", "Informação")}</h2>

            <#-- Mensagem principal -->
            <div class="alert alert-success" style="text-align: left;">
                <p style="margin: 0; font-weight: 500;">
                    ${kcSanitize(message.summary)?no_esc}
                </p>
            </div>

            <#-- Ações pendentes (ex: verificação de email) -->
            <#if requiredActions??>
                <div class="reset-info" style="text-align: left;">
                    <strong>Próximos passos:</strong>
                    <#list requiredActions>
                        <ul style="margin: 0.5rem 0 0; padding-left: 1.5rem;">
                            <#items as reqActionItem>
                                <li>${msg("requiredAction.${reqActionItem}")}</li>
                            </#items>
                        </ul>
                    </#list>
                </div>
            </#if>

            <#-- Dica para verificação de email -->
            <#if pageRedirectUri?has_content>
                <div class="reset-info">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16">
                        <circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>
                    </svg>
                    <span>Verifique sua caixa de spam caso não encontre o e-mail na caixa de entrada.</span>
                </div>
            </#if>

            <#-- Botões de ação -->
            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 24px;">
                <#if skipLink??>
                <#else>
                    <#if pageRedirectUri?has_content>
                        <a href="${pageRedirectUri}" class="btn-submit" style="text-decoration: none; text-align: center; display: block;">
                            ${msg("backToApplication")}
                        </a>
                    <#elseif actionUri?has_content>
                        <a href="${actionUri}" class="btn-submit" style="text-decoration: none; text-align: center; display: block;">
                            ${msg("doContinue")}
                        </a>
                    <#elseif (client.baseUrl)?has_content>
                        <a href="${client.baseUrl}" class="btn-submit" style="text-decoration: none; text-align: center; display: block;">
                            ${msg("backToApplication")}
                        </a>
                    </#if>
                </#if>

                <a href="${url.loginRestartFlowUrl}" class="btn-secondary" style="text-decoration: none; text-align: center; display: block;">
                    ${msg("backToLogin")}
                </a>
            </div>
        </div>
    </#if>
</@layout.registrationLayout>
