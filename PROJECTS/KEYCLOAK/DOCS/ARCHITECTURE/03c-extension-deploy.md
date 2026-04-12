---
type: leaf
status: draft
updated: 2026-02-07
---

# Deploy e Testes de Extensoes

Processo de build, deploy via Docker e estrategia de testes para as extensoes Java do Keycloak CARF.

## Build Maven

Executar mvn clean package no diretorio extensions/. O Maven processa os tres modulos e gera JARs em cada target/: cpf-validator-1.0.0.jar, tenant-audit-1.0.0.jar e tenant-mapper-1.0.0.jar.

## Deploy via Docker

A imagem customizada usa multi-stage build. O estagio builder parte de quay.io/keycloak/keycloak:24.0.0, copia temas para /opt/keycloak/themes/carf/ e JARs para /opt/keycloak/providers/, executa kc.sh build para otimizar o runtime. O estagio final copia o resultado e define kc.sh como entrypoint.

## Ativacao no Admin Console

| Tipo de Extensao | Caminho | Procedimento |
|:-----------------|:--------|:-------------|
| Authenticator (CPF Validator) | Authentication, Flows | Copiar flow "Browser", adicionar "CPF Validator", definir Required |
| Event Listener (Tenant Audit) | Events, Config | Adicionar "tenant-audit" a lista de Event Listeners |

## Estrategia de Testes

Testes unitarios utilizam Mockito para simular AuthenticationFlowContext e UserModel. O teste do CpfValidator cria mocks, configura username como CPF formatado e verifica invocacao de context.success(). Testes de integracao utilizam Arquillian com anotacao KeycloakTest para executar fluxos contra instancia real do Keycloak validando comportamento end-to-end.

## Debug Remoto

Iniciar o container com JAVA_OPTS configurando agente JDWP na porta 8787 (suspend=n) e mapear portas 8080 e 8787. No IntelliJ IDEA criar configuracao Remote JVM Debug para localhost:8787, definir breakpoints nas SPIs e acionar o fluxo no browser.

## Referencias

- [03a-extension-structure.md](./03a-extension-structure.md) - Estrutura Maven do projeto
- [03b-extension-spis.md](./03b-extension-spis.md) - Detalhamento das SPIs
