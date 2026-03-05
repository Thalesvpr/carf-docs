<#import "template.ftl" as layout>
<@layout.mainLayout active='account' bodyClass='user'; section>
    <div class="account-page">
        <div class="account-header">
            <h1>${msg("editAccountHtmlTitle")}</h1>
        </div>

        <#if message?has_content>
            <div class="alert alert-${message.type}">
                ${kcSanitize(message.summary)?no_esc}
            </div>
        </#if>

        <form action="${url.accountUrl}" method="post">
            <input type="hidden" id="stateChecker" name="stateChecker" value="${stateChecker}">

            <div class="form-group">
                <label for="username">${msg("username")}</label>
                <input type="text" id="username" name="username" disabled="disabled" value="${(account.username!'')}"/>
            </div>

            <div class="form-group">
                <label for="email">${msg("email")}</label>
                <input type="email" id="email" name="email" value="${(account.email!'')}" required/>
            </div>

            <div class="form-group">
                <label for="firstName">${msg("firstName")}</label>
                <input type="text" id="firstName" name="firstName" value="${(account.firstName!'')}" required/>
            </div>

            <div class="form-group">
                <label for="lastName">${msg("lastName")}</label>
                <input type="text" id="lastName" name="lastName" value="${(account.lastName!'')}" required/>
            </div>

            <div class="form-group">
                <button type="submit" class="btn btn-primary">${msg("doSave")}</button>
                <button type="button" onclick="window.location.reload()" class="btn btn-secondary">${msg("doCancel")}</button>
            </div>
        </form>
    </div>
</@layout.mainLayout>
