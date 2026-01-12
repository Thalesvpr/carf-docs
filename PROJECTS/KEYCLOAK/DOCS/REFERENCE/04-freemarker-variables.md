# FreeMarker Variables

Templates FreeMarker .ftl têm acesso a variáveis context injetadas pelo Keycloak para renderização dinâmica. Objeto realm fornece realm.name identificador, realm.displayName nome amigável, realm.internationalizationEnabled boolean i18n. Objeto url contém URLs dinâmicas url.loginAction form action, url.loginUrl página login, url.registrationUrl registro, url.loginResetCredentialsUrl reset senha, url.resourcesPath caminho assets theme. Função msg("key") retorna mensagem localizada do messages properties atual, msg("key", param1, param2) com interpolação. Objeto properties acessa variáveis theme.properties como properties.kcFormClass classes CSS. Objeto login em páginas login contém login.username valor preenchido, login.rememberMe checkbox state. Objeto user quando autenticado fornece user.username, user.email, user.firstName, user.lastName, user.attributes map custom. Objeto auth em fluxos auth contém auth.attemptedUsername tentativa falha, auth.showUsername boolean. Objeto client identifica client atual client.clientId, client.name. Array social.providers lista identity providers configurados para social login buttons. Objeto message para feedback message.summary texto, message.type enum success error warning info para styling condicional.

---

**Última atualização:** 2026-01-12
