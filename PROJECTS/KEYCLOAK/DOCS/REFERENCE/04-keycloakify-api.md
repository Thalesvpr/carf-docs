---
type: leaf
status: rejected
description: "REFERENCE usa tabelas extensivas para APIs - formato referencia incompativel com prosa densa"
updated: 2026-01-22
---

# Keycloakify API Reference

Referência das APIs, tipos e configurações disponíveis no Keycloakify para desenvolvimento de temas Keycloak com React.

## KcContext

O KcContext é o objeto central que contém todos os dados fornecidos pelo Keycloak para renderização das páginas. É o equivalente React das variáveis FreeMarker.

### Estrutura Base

Todas as páginas recebem um KcContext com propriedades comuns.

| Propriedade | Tipo | Descrição |
|:------------|:-----|:----------|
| pageId | string | Identificador da página atual (login.ftl, register.ftl, etc.) |
| realm | RealmContext | Informações do realm |
| url | UrlContext | URLs de ação e recursos |
| locale | LocaleContext | Informações de internacionalização |
| auth | AuthContext | Estado da autenticação |
| message | MessageContext | Mensagem de feedback (erro/sucesso) |
| messagesPerField | MessagesPerField | Validação por campo |
| properties | Record<string, string> | Propriedades do theme.properties |
| scripts | string[] | Scripts a carregar |
| isAppInitiatedAction | boolean | Se ação foi iniciada pela aplicação |

### RealmContext

Informações sobre o realm Keycloak atual.

| Propriedade | Tipo | Descrição |
|:------------|:-----|:----------|
| name | string | Nome do realm |
| displayName | string | Nome para exibição |
| displayNameHtml | string | Nome com HTML permitido |
| internationalizationEnabled | boolean | Se i18n está ativo |
| registrationAllowed | boolean | Se auto-registro está permitido |
| registrationEmailAsUsername | boolean | Se email é usado como username |
| loginWithEmailAllowed | boolean | Se login com email é permitido |
| resetPasswordAllowed | boolean | Se recuperação de senha está ativa |
| rememberMe | boolean | Se "lembrar-me" está habilitado |
| password | boolean | Se autenticação por senha está ativa |

### UrlContext

URLs dinâmicas para formulários e recursos.

| Propriedade | Tipo | Descrição |
|:------------|:-----|:----------|
| loginAction | string | Action URL do form de login |
| loginUrl | string | URL da página de login |
| loginResetCredentialsUrl | string | URL de recuperação de senha |
| registrationAction | string | Action URL do form de registro |
| registrationUrl | string | URL da página de registro |
| resourcesPath | string | Caminho base para assets do tema |
| resourcesCommonPath | string | Caminho para recursos compartilhados |
| logoutUrl | string | URL de logout |
| oauthAction | string | Action URL para OAuth |

### LocaleContext

Informações de localização e idiomas disponíveis.

| Propriedade | Tipo | Descrição |
|:------------|:-----|:----------|
| currentLanguageTag | string | Tag do idioma atual (pt-BR, en, etc.) |
| supported | SupportedLocale[] | Lista de idiomas suportados |

Cada SupportedLocale contém label (nome do idioma), languageTag (código) e url (link para trocar idioma).

### AuthContext

Estado do fluxo de autenticação.

| Propriedade | Tipo | Descrição |
|:------------|:-----|:----------|
| attemptedUsername | string | Username da tentativa falha |
| showUsername | boolean | Se deve mostrar username |
| showResetCredentials | boolean | Se deve mostrar link de reset |
| showTryAnotherWayLink | boolean | Se deve mostrar alternativas |

### MessageContext

Mensagem de feedback para o usuário.

| Propriedade | Tipo | Descrição |
|:------------|:-----|:----------|
| type | string | Tipo: success, warning, error, info |
| summary | string | Texto da mensagem |

## Contextos por Página

Cada tipo de página tem propriedades específicas além das comuns.

### Login (login.ftl)

| Propriedade | Tipo | Descrição |
|:------------|:-----|:----------|
| login.username | string | Username preenchido anteriormente |
| login.rememberMe | boolean | Estado do checkbox lembrar-me |
| social.providers | SocialProvider[] | Identity providers disponíveis |
| usernameEditDisabled | boolean | Se edição do username está bloqueada |

### Register (register.ftl)

| Propriedade | Tipo | Descrição |
|:------------|:-----|:----------|
| register.formData | FormData | Dados do formulário preenchidos |
| recaptchaRequired | boolean | Se reCAPTCHA é obrigatório |
| recaptchaSiteKey | string | Chave do reCAPTCHA |
| passwordRequired | boolean | Se senha é obrigatória |
| termsAcceptanceRequired | boolean | Se termos devem ser aceitos |

### Login Reset Password (login-reset-password.ftl)

| Propriedade | Tipo | Descrição |
|:------------|:-----|:----------|
| auth.attemptedUsername | string | Username/email informado |

### Login Update Password (login-update-password.ftl)

| Propriedade | Tipo | Descrição |
|:------------|:-----|:----------|
| isAppInitiatedAction | boolean | Se foi iniciado pela aplicação |
| username | string | Username do usuário |

### Error (error.ftl)

| Propriedade | Tipo | Descrição |
|:------------|:-----|:----------|
| message.summary | string | Mensagem de erro |
| client | ClientContext | Informações do client (se disponível) |
| skipLink | boolean | Se deve esconder link de skip |

### Info (info.ftl)

| Propriedade | Tipo | Descrição |
|:------------|:-----|:----------|
| message.summary | string | Mensagem informativa |
| messageHeader | string | Cabeçalho da mensagem |
| requiredActions | string[] | Ações requeridas pendentes |
| skipLink | boolean | Se deve esconder link de skip |
| pageRedirectUri | string | URI de redirecionamento |
| actionUri | string | URI de ação |

## Funções de i18n

O Keycloakify fornece funções para acessar mensagens internacionalizadas.

### msg(key)

Retorna a mensagem traduzida para a chave especificada no idioma atual do usuário.

| Parâmetro | Tipo | Descrição |
|:----------|:-----|:----------|
| key | string | Chave da mensagem |
| ...args | string[] | Argumentos para interpolação |

A função busca primeiro em mensagens customizadas do tema, depois nas mensagens padrão do Keycloak.

### advancedMsg(key)

Similar a msg(), mas permite HTML na mensagem retornada. Use com cuidado para evitar XSS, aplicando sanitização adequada.

### msgStr(key)

Retorna a mensagem como string pura, útil para contextos onde React escapa HTML automaticamente.

## Hooks

Hooks React disponibilizados pelo Keycloakify para funcionalidades comuns.

### useGetClassName

Hook para obter classes CSS combinando classes do tema base com customizações.

Recebe um objeto com doUseDefaultCss (boolean para incluir classes padrão) e classes (objeto mapeando slots para classes customizadas).

Retorna função getClassName(slot) que retorna a string de classes para o slot especificado.

Slots disponíveis incluem kcHtmlClass, kcBodyClass, kcHeaderClass, kcFormClass, kcInputClass, kcButtonClass entre outros documentados em theme.properties.

### useFormValidation

Hook para validação de formulários integrada com messagesPerField do Keycloak.

Retorna objeto com existsError(fieldName) que verifica se campo tem erro, getFirstError(fieldName) que retorna primeira mensagem de erro, e getErrors(fieldName) que retorna todas as mensagens.

### useDownloadTerms

Hook para download e exibição de termos de uso quando termsAcceptanceRequired é true.

Retorna objeto com termsMarkdown (conteúdo dos termos), isLoading (estado de carregamento), e error (erro se houver).

## Configuração

O arquivo keycloakify.config.ts configura o comportamento do build.

### Opções de Configuração

| Opção | Tipo | Descrição |
|:------|:-----|:----------|
| themeName | string | Nome do tema no Keycloak |
| themeVersion | string | Versão do tema |
| extraThemeProperties | string[] | Properties adicionais para theme.properties |
| keycloakVersionTargets | object | Versões Keycloak suportadas |
| groupId | string | Group ID Maven para o JAR |
| artifactId | string | Artifact ID Maven para o JAR |
| doCreateJar | boolean | Se deve gerar JAR (default: true) |
| startKeycloakOptions | object | Opções para modo desenvolvimento |

### extraThemeProperties

Array de strings no formato chave=valor que serão incluídas no theme.properties gerado.

Propriedades comuns incluem parent (tema pai para herança), styles (arquivos CSS), scripts (arquivos JS), locales (idiomas suportados), e propriedades customizadas acessíveis via kcContext.properties.

### keycloakVersionTargets

Objeto especificando compatibilidade com versões Keycloak.

| Propriedade | Tipo | Descrição |
|:------------|:-----|:----------|
| hasAccountTheme | boolean | Se inclui tema de Account |
| hasAdminTheme | boolean | Se inclui tema Admin |
| loginThemeResourcesFromKeycloakVersion | string | Versão KC para recursos |

## Componentes Base

Keycloakify fornece componentes base que podem ser estendidos ou substituídos.

### Template

Componente de template padrão que renderiza a estrutura HTML base da página.

Props incluem kcContext (contexto da página), doUseDefaultCss (se usa CSS padrão), classes (classes customizadas), e children (conteúdo da página).

### UserProfileFormFields

Componente que renderiza campos de formulário baseados no User Profile configurado no Keycloak.

Props incluem kcContext, onIsFormSubmittable (callback de validação), e BeforeField/AfterField (componentes para inserir conteúdo antes/depois de campos).

### PasswordWrapper

Componente que encapsula campo de senha com toggle de visibilidade.

Props incluem kcContext, passwordInputId (id do input), e children (input de senha).

## Mapeamento FreeMarker

Para referência, esta tabela mapeia variáveis FreeMarker comuns para suas equivalentes no KcContext.

| FreeMarker | KcContext |
|:-----------|:----------|
| ${realm.name} | kcContext.realm.name |
| ${realm.displayName} | kcContext.realm.displayName |
| ${url.loginAction} | kcContext.url.loginAction |
| ${url.resourcesPath} | kcContext.url.resourcesPath |
| ${login.username} | kcContext.login.username |
| ${message.summary} | kcContext.message.summary |
| ${message.type} | kcContext.message.type |
| ${msg("key")} | msg("key") via hook |
| ${properties.custom} | kcContext.properties.custom |
| ${locale.currentLanguageTag} | kcContext.locale.currentLanguageTag |

Consulte REFERENCE/04-freemarker-variables.md para lista completa de variáveis FreeMarker e seus usos.

## Referências

A documentação oficial do Keycloakify em keycloakify.dev/docs contém referência completa de tipos gerados e APIs avançadas.

O repositório de exemplos em github.com/keycloakify/keycloakify-starter demonstra implementações de referência para todos os tipos de página.
