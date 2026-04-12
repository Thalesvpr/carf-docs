---
type: leaf
status: draft
updated: 2026-02-07
---

# Estrutura de Extensoes Keycloak

Extensoes Keycloak no projeto CARF sao implementadas como SPIs (Service Provider Interfaces) em Java 17, compiladas via Maven multi-module e deployadas como JARs no diretorio /opt/keycloak/providers/ da imagem Docker customizada. O projeto raiz reside em carf-keycloak/extensions/ com um POM parent que define a versao do Keycloak (24.0.0), configura o compilador Java 17 e gerencia dependencias compartilhadas keycloak-server-spi e keycloak-server-spi-private com scope provided.

## Modulos do Projeto

| Modulo | Descricao | Artefato |
|:-------|:----------|:---------|
| cpf-validator | Authenticator SPI que valida formato CPF no fluxo de login | cpf-validator-1.0.0.jar |
| tenant-audit | Event Listener SPI que registra eventos de usuario e admin com tenant_id | tenant-audit-1.0.0.jar |
| tenant-mapper | Protocol Mapper SPI que injeta claims de tenant no token JWT | tenant-mapper-1.0.0.jar |

Cada modulo contem seu proprio pom.xml herdando do parent, com codigo fonte em src/main/java/com/carf/keycloak/ contendo a classe de implementacao e a classe Factory correspondente. O groupId comum e com.carf.keycloak e o artifactId do parent e carf-keycloak-extensions com packaging pom.

## Dependencias Maven

As dependencias do Keycloak sao declaradas no dependencyManagement do parent POM para garantir versoes consistentes entre modulos. Ambas keycloak-server-spi e keycloak-server-spi-private usam scope provided porque o Keycloak runtime ja fornece essas bibliotecas, evitando conflitos de classloader. Cada modulo filho herda essas dependencias sem redeclarar versao.

## Service Loader

Cada SPI precisa de registro via Java Service Loader. O arquivo em src/main/resources/META-INF/services/ deve conter o nome completo da classe Factory. Para Authenticators o arquivo se chama org.keycloak.authentication.AuthenticatorFactory, para Event Listeners org.keycloak.events.EventListenerProviderFactory e para Protocol Mappers org.keycloak.protocol.ProtocolMapper. O conteudo de cada arquivo e o fully qualified name da Factory, por exemplo com.carf.keycloak.CpfValidatorAuthenticatorFactory.

## Referencias

- [03b-extension-spis.md](./03b-extension-spis.md) - Detalhamento das SPIs implementadas
- [03c-extension-deploy.md](./03c-extension-deploy.md) - Build, deploy e testes
