<#import "template.ftl" as layout>
<@layout.registrationLayout displayMessage=!messagesPerField.existsError('firstName','lastName','email','username','password','password-confirm'); section>
    <#if section = "header">
        <div class="kc-logo">
            <img src="${url.resourcesPath}/img/logo.svg" alt="${msg("logoAlt", "CARF")}" />
        </div>
        ${msg("registerTitle")}
    <#elseif section = "form">
        <form id="kc-register-form" class="${properties.kcFormClass!}" action="${url.registrationAction}" method="post">

            <#-- Nome -->
            <div class="form-group">
                <label for="firstName" class="${properties.kcLabelClass!}">${msg("firstName")}</label>
                <input type="text" id="firstName" class="${properties.kcInputClass!}" name="firstName"
                       value="${(register.formData.firstName!'')}"
                       autocomplete="given-name"
                       placeholder="${msg("firstNamePlaceholder")}"
                       aria-invalid="<#if messagesPerField.existsError('firstName')>true</#if>"
                />
                <#if messagesPerField.existsError('firstName')>
                    <span id="input-error-firstname" class="${properties.kcInputErrorMessageClass!}" aria-live="polite">
                        ${kcSanitize(messagesPerField.get('firstName'))?no_esc}
                    </span>
                </#if>
            </div>

            <#-- Sobrenome -->
            <div class="form-group">
                <label for="lastName" class="${properties.kcLabelClass!}">${msg("lastName")}</label>
                <input type="text" id="lastName" class="${properties.kcInputClass!}" name="lastName"
                       value="${(register.formData.lastName!'')}"
                       autocomplete="family-name"
                       placeholder="${msg("lastNamePlaceholder")}"
                       aria-invalid="<#if messagesPerField.existsError('lastName')>true</#if>"
                />
                <#if messagesPerField.existsError('lastName')>
                    <span id="input-error-lastname" class="${properties.kcInputErrorMessageClass!}" aria-live="polite">
                        ${kcSanitize(messagesPerField.get('lastName'))?no_esc}
                    </span>
                </#if>
            </div>

            <#-- Email -->
            <div class="form-group">
                <label for="email" class="${properties.kcLabelClass!}">${msg("email")}</label>
                <input type="email" id="email" class="${properties.kcInputClass!}" name="email"
                       value="${(register.formData.email!'')}"
                       autocomplete="email"
                       placeholder="${msg("emailPlaceholder")}"
                       aria-invalid="<#if messagesPerField.existsError('email')>true</#if>"
                />
                <#if messagesPerField.existsError('email')>
                    <span id="input-error-email" class="${properties.kcInputErrorMessageClass!}" aria-live="polite">
                        ${kcSanitize(messagesPerField.get('email'))?no_esc}
                    </span>
                </#if>
            </div>

            <#-- Username (CPF ou username) -->
            <#if !realm.registrationEmailAsUsername>
                <div class="form-group">
                    <label for="username" class="${properties.kcLabelClass!}">${msg("username")}</label>
                    <input type="text" id="username" class="${properties.kcInputClass!}" name="username"
                           value="${(register.formData.username!'')}"
                           autocomplete="username"
                           placeholder="${msg("usernamePlaceholder")}"
                           aria-invalid="<#if messagesPerField.existsError('username')>true</#if>"
                    />
                    <#if messagesPerField.existsError('username')>
                        <span id="input-error-username" class="${properties.kcInputErrorMessageClass!}" aria-live="polite">
                            ${kcSanitize(messagesPerField.get('username'))?no_esc}
                        </span>
                    </#if>
                </div>
            </#if>

            <#-- Senha -->
            <#if passwordRequired??>
                <div class="form-group">
                    <label for="password" class="${properties.kcLabelClass!}">${msg("password")}</label>
                    <div class="password-wrapper">
                        <input type="password" id="password" class="${properties.kcInputClass!}" name="password"
                               autocomplete="new-password"
                               placeholder="${msg("passwordNewPlaceholder")}"
                               aria-invalid="<#if messagesPerField.existsError('password','password-confirm')>true</#if>"
                        />
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
                    <#if messagesPerField.existsError('password')>
                        <span id="input-error-password" class="${properties.kcInputErrorMessageClass!}" aria-live="polite">
                            ${kcSanitize(messagesPerField.get('password'))?no_esc}
                        </span>
                    </#if>
                </div>

                <#-- Confirmar Senha -->
                <div class="form-group">
                    <label for="password-confirm" class="${properties.kcLabelClass!}">${msg("passwordConfirm")}</label>
                    <div class="password-wrapper">
                        <input type="password" id="password-confirm" class="${properties.kcInputClass!}" name="password-confirm"
                               autocomplete="new-password"
                               placeholder="${msg("passwordConfirmPlaceholder")}"
                               aria-invalid="<#if messagesPerField.existsError('password-confirm')>true</#if>"
                        />
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
                    <#if messagesPerField.existsError('password-confirm')>
                        <span id="input-error-password-confirm" class="${properties.kcInputErrorMessageClass!}" aria-live="polite">
                            ${kcSanitize(messagesPerField.get('password-confirm'))?no_esc}
                        </span>
                    </#if>
                </div>
            </#if>

            <#-- Recaptcha -->
            <#if recaptchaRequired??>
                <div class="form-group">
                    <div class="g-recaptcha" data-sitekey="${recaptchaSiteKey}" data-size="compact"></div>
                </div>
            </#if>

            <#-- Botão de Registro -->
            <div id="kc-form-buttons" class="form-group">
                <input class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}" type="submit" value="${msg("doRegister")}"/>
            </div>

        </form>
    <#elseif section = "info">
        <#-- Link para login -->
        <div id="kc-registration">
            <span>${msg("alreadyHaveAccount")} <a href="${url.loginUrl}">${msg("doLogIn")}</a></span>
        </div>
    </#if>
</@layout.registrationLayout>
