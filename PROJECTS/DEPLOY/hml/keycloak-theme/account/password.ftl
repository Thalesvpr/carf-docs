<#import "template.ftl" as layout>
<@layout.mainLayout active='password' bodyClass='password'; section>
    <div class="account-page">
        <div class="account-header">
            <h1>${msg("changePasswordHtmlTitle")}</h1>
        </div>

        <#if message?has_content>
            <div class="alert alert-${message.type}">
                ${kcSanitize(message.summary)?no_esc}
            </div>
        </#if>

        <form action="${url.passwordUrl}" method="post">
            <input type="hidden" id="stateChecker" name="stateChecker" value="${stateChecker}">

            <#if password.passwordSet>
                <div class="form-group">
                    <label for="password">${msg("password")}</label>
                    <input type="password" id="password" name="password" autocomplete="current-password" required/>
                </div>
            </#if>

            <div class="form-group">
                <label for="password-new">${msg("passwordNew")}</label>
                <input type="password" id="password-new" name="password-new" autocomplete="new-password" required/>
            </div>

            <div class="form-group">
                <label for="password-confirm">${msg("passwordConfirm")}</label>
                <input type="password" id="password-confirm" name="password-confirm" autocomplete="new-password" required/>
            </div>

            <div class="form-group">
                <button type="submit" class="btn btn-primary">${msg("doSave")}</button>
            </div>
        </form>
    </div>
</@layout.mainLayout>
