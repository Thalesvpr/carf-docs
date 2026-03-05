<#macro registrationLayout bodyClass="" displayInfo=false displayMessage=true displayRequiredFields=false>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex, nofollow">
    <title>${msg("loginTitle",(realm.displayName!''))}</title>
    <link rel="icon" href="${url.resourcesPath}/img/favicon.ico">
    <link rel="stylesheet" href="${url.resourcesPath}/css/login.css">
</head>
<body>
    <div class="login-container">
        <!-- Painel Esquerdo - Branding -->
        <div class="login-brand">
            <div class="brand-content">
                <img src="${url.resourcesPath}/img/carf-logo.svg" alt="CARF" class="brand-logo-img">
                <h1 class="brand-logo">CARF</h1>
                <p class="brand-subtitle">Sistema de Regularização<br>Fundiária Urbana</p>
            </div>
        </div>

        <!-- Painel Direito - Formulário -->
        <div class="login-main">
            <div class="login-card">
                <#nested "form">

                <#if displayInfo>
                    <div class="login-info">
                        <#nested "info">
                    </div>
                </#if>
            </div>
        </div>
    </div>
    <script src="${url.resourcesPath}/js/login.js"></script>
</body>
</html>
</#macro>
