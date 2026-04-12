---
type: leaf
status: approved
updated: 2026-02-07
---

# Keycloak SPIs

Service Provider Interfaces (SPIs) do Keycloak sao pontos de extensao server-side que permitem customizar comportamento core do servidor de autenticacao. Implementadas como JARs Java, as SPIs sao colocadas em /opt/keycloak/providers/ e descobertas automaticamente durante o boot via Java Service Loader.

## Tipos de SPI Relevantes para o CARF

O tipo **Authenticator** permite criar steps customizados em authentication flows. A interface define metodos authenticate (logica principal de validacao), action (processar formulario submetido), requiresUser (se precisa usuario carregado) e configuredFor (se step esta configurado para o usuario). O contexto AuthenticationFlowContext fornece acesso ao usuario, sessao e mecanismos de resposta como success, failure e challenge. No CARF, o CpfValidatorAuthenticator valida formato e digitos verificadores de CPF antes da verificacao de senha.

O tipo **EventListenerProvider** intercepta eventos do ciclo de vida do Keycloak. O metodo onEvent(Event) captura eventos de usuario como LOGIN, LOGOUT, REGISTER e UPDATE_PROFILE. O metodo onEvent(AdminEvent) captura eventos administrativos como CREATE_USER, UPDATE_CLIENT e alteracoes de roles. No CARF, o TenantAuditEventListener enriquece cada evento com tenant_id extraido dos atributos do usuario, persistindo em storage externo para auditoria multi-tenant.

O tipo **ProtocolMapper** permite adicionar ou modificar claims no JWT. O metodo transformAccessToken recebe o token, modelo do mapper, sessao e contexto do client, retornando o token modificado com claims adicionais. No CARF, o TenantProtocolMapper injeta claims tenant_id, allowed_tenants e community_ids extraidos de user attributes, embora na pratica o realm-export.json use protocol mappers nativos oidc-usermodel-attribute-mapper para este mapeamento.

O tipo **RequiredActionProvider** forca acoes obrigatorias como verificar email, atualizar senha ou aceitar termos de uso. Define metodos evaluateTriggers para condicoes de ativacao, requiredActionChallenge para apresentar o desafio e processAction para validar a resposta do usuario.

O tipo **UserStorageProvider** integra fontes externas de usuarios como LDAP, Active Directory ou banco de dados legado. Implementa metodos getUserByUsername, getUserById, searchForUser e validateCredentials, permitindo SSO com sistemas preexistentes sem migrar usuarios.

## Registro e Descoberta

Cada SPI exige registro via Java Service Loader. O arquivo em src/main/resources/META-INF/services/ deve conter o fully qualified name da classe Factory correspondente. Para Authenticators, o arquivo chama-se org.keycloak.authentication.AuthenticatorFactory. Para Event Listeners, org.keycloak.events.EventListenerProviderFactory. Para Protocol Mappers, org.keycloak.protocol.ProtocolMapper. Todas as factories implementam ProviderFactory com metodos getId, init, postInit e close.

## Build e Dependencias

SPIs sao buildadas via Maven com keycloak-server-spi e keycloak-server-spi-private como dependencias provided, pois o runtime do Keycloak ja fornece essas bibliotecas. O JAR resultante deve ser uber JAR contendo dependencias externas mas excluindo as APIs do Keycloak para evitar conflitos de classloader. Em modo dev, SPIs sao hot-reloadable, mas em producao exigem restart do Keycloak apos deploy.

## Configuracao e Ativacao

Authenticators sao ativados em Authentication, Flows no Admin Console, copiando o flow Browser e adicionando o step customizado. Event Listeners sao ativados em Realm Settings, Events, Config adicionando o provider ID na lista. Protocol Mappers sao configurados em Client Scopes, selecionando o scope e adicionando o mapper.

## Testes e Debug

Testes unitarios utilizam Mockito para simular AuthenticationFlowContext, UserModel e KeycloakSession. Testes de integracao usam Keycloak Testcontainers para executar fluxos contra instancia real em container. Debug remoto requer iniciar o container com JAVA_OPTS configurando agente JDWP na porta 8787 (suspend=n) e conectar o debugger do IntelliJ IDEA ou Eclipse. O codigo fonte das SPIs CARF reside em PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/extensions/ estruturado como Maven multi-module.
