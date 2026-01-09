# Extension Development - SPIs Java

## Visão Geral

Extensões Keycloak (SPIs - Service Provider Interfaces) permitem customizar comportamento server-side através de plugins Java deployados como JARs.

## Setup Maven

### Estrutura Multi-Module
```
carf-keycloak/extensions/
├── pom.xml (parent)
├── cpf-validator/
│   ├── pom.xml
│   └── src/main/java/com/carf/keycloak/
│       ├── CpfValidatorAuthenticator.java
│       └── CpfValidatorAuthenticatorFactory.java
├── tenant-audit/
│   ├── pom.xml
│   └── src/main/java/com/carf/keycloak/
│       ├── TenantAuditEventListener.java
│       └── TenantAuditEventListenerFactory.java
└── tenant-mapper/
    ├── pom.xml
    └── src/main/java/com/carf/keycloak/
        ├── TenantProtocolMapper.java
        └── TenantProtocolMapperFactory.java
```

### Parent POM
```xml
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.carf.keycloak</groupId>
    <artifactId>carf-keycloak-extensions</artifactId>
    <version>1.0.0</version>
    <packaging>pom</packaging>

    <properties>
        <keycloak.version>24.0.0</keycloak.version>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.keycloak</groupId>
                <artifactId>keycloak-server-spi</artifactId>
                <version>${keycloak.version}</version>
                <scope>provided</scope>
            </dependency>
            <dependency>
                <groupId>org.keycloak</groupId>
                <artifactId>keycloak-server-spi-private</artifactId>
                <version>${keycloak.version}</version>
                <scope>provided</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <modules>
        <module>cpf-validator</module>
        <module>tenant-audit</module>
        <module>tenant-mapper</module>
    </modules>
</project>
```

## Tipos de SPIs

### 1. Authenticator
Custom authentication logic.

```java
public class CpfValidatorAuthenticator implements Authenticator {

    @Override
    public void authenticate(AuthenticationFlowContext context) {
        String username = context.getUser().getUsername();

        // Validate CPF format
        if (!isValidCPF(username)) {
            context.failure(AuthenticationFlowError.INVALID_USER);
            return;
        }

        context.success();
    }

    private boolean isValidCPF(String cpf) {
        // CPF validation logic from @carf/tscore
        String clean = cpf.replaceAll("[^0-9]", "");
        if (clean.length() != 11) return false;

        // Check digits validation
        // ...

        return true;
    }

    @Override
    public void action(AuthenticationFlowContext context) {
        // Handle form submission if needed
    }

    @Override
    public boolean requiresUser() {
        return true;
    }

    @Override
    public boolean configuredFor(KeycloakSession session,
                                  RealmModel realm,
                                  UserModel user) {
        return true;
    }

    @Override
    public void setRequiredActions(KeycloakSession session,
                                     RealmModel realm,
                                     UserModel user) {
        // No required actions
    }

    @Override
    public void close() {
        // Cleanup if needed
    }
}
```

### Factory
```java
public class CpfValidatorAuthenticatorFactory implements AuthenticatorFactory {

    public static final String PROVIDER_ID = "carf-cpf-validator";

    @Override
    public String getDisplayType() {
        return "CARF CPF Validator";
    }

    @Override
    public String getReferenceCategory() {
        return null;
    }

    @Override
    public boolean isConfigurable() {
        return false;
    }

    @Override
    public boolean isUserSetupAllowed() {
        return false;
    }

    @Override
    public String getHelpText() {
        return "Validates username as valid CPF format";
    }

    @Override
    public List<ProviderConfigProperty> getConfigProperties() {
        return Collections.emptyList();
    }

    @Override
    public Authenticator create(KeycloakSession session) {
        return new CpfValidatorAuthenticator();
    }

    @Override
    public void init(Config.Scope config) {
    }

    @Override
    public void postInit(KeycloakSessionFactory factory) {
    }

    @Override
    public void close() {
    }

    @Override
    public String getId() {
        return PROVIDER_ID;
    }
}
```

### Service Loader Registration
`src/main/resources/META-INF/services/org.keycloak.authentication.AuthenticatorFactory`:
```
com.carf.keycloak.CpfValidatorAuthenticatorFactory
```

### 2. Event Listener
Audit and logging.

```java
public class TenantAuditEventListener implements EventListenerProvider {

    private static final Logger log = Logger.getLogger(TenantAuditEventListener.class);

    @Override
    public void onEvent(Event event) {
        // User events (LOGIN, LOGOUT, REGISTER, etc.)
        String tenantId = extractTenantId(event);

        log.infof("Event: %s, User: %s, Tenant: %s, IP: %s",
            event.getType(),
            event.getUserId(),
            tenantId,
            event.getIpAddress());

        // Save to external DB, Kafka, etc.
        saveAuditLog(event, tenantId);
    }

    @Override
    public void onEvent(AdminEvent event, boolean includeRepresentation) {
        // Admin events (CREATE_USER, UPDATE_CLIENT, etc.)
        log.infof("Admin Event: %s, Resource: %s, Operator: %s",
            event.getOperationType(),
            event.getResourcePath(),
            event.getAuthDetails().getUserId());

        saveAdminAuditLog(event);
    }

    private String extractTenantId(Event event) {
        // Extract from user attributes
        if (event.getUserId() != null) {
            // Query user and get tenant_id attribute
        }
        return null;
    }

    private void saveAuditLog(Event event, String tenantId) {
        // Implement persistence (DB, Kafka, S3, etc.)
    }

    private void saveAdminAuditLog(AdminEvent event) {
        // Implement admin audit persistence
    }

    @Override
    public void close() {
    }
}
```

## Build e Deploy

### Build
```bash
cd extensions
mvn clean package

# JARs gerados em:
# cpf-validator/target/cpf-validator-1.0.0.jar
# tenant-audit/target/tenant-audit-1.0.0.jar
```

### Deploy no Dockerfile
```dockerfile
FROM quay.io/keycloak/keycloak:24.0.0 AS builder

# Copy themes
COPY themes/carf /opt/keycloak/themes/carf

# Copy extensions
COPY extensions/cpf-validator/target/cpf-validator-1.0.0.jar /opt/keycloak/providers/
COPY extensions/tenant-audit/target/tenant-audit-1.0.0.jar /opt/keycloak/providers/

# Build
RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:24.0.0
COPY --from=builder /opt/keycloak/ /opt/keycloak/

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
```

### Ativar Extension

#### Authenticator
1. Admin Console → Authentication → Flows
2. Copy "Browser" flow
3. Add execution → CPF Validator
4. Set Required

#### Event Listener
1. Admin Console → Events → Config
2. Event Listeners → Add "tenant-audit"
3. Save

## Testing

### Unit Tests (Mockito)
```java
@Test
public void testValidCPF() {
    CpfValidatorAuthenticator authenticator = new CpfValidatorAuthenticator();

    AuthenticationFlowContext context = mock(AuthenticationFlowContext.class);
    UserModel user = mock(UserModel.class);

    when(context.getUser()).thenReturn(user);
    when(user.getUsername()).thenReturn("123.456.789-00");

    authenticator.authenticate(context);

    verify(context).success();
}
```

### Integration Tests (Arquillian)
```java
@RunWith(Arquillian.class)
@KeycloakTest
public class CpfValidatorIT {

    @Test
    public void testCpfValidationInRealFlow() {
        // Test with real Keycloak instance
        // ...
    }
}
```

## Debug Remoto

### Habilitar Debug
```bash
docker run -e JAVA_OPTS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8787" \
    -p 8080:8080 -p 8787:8787 \
    carf/keycloak:latest start-dev
```

### IntelliJ IDEA
1. Run → Edit Configurations
2. Add New → Remote JVM Debug
3. Host: localhost, Port: 8787
4. Start Debug
5. Set breakpoints em SPIs
6. Trigger flow no browser

## Referências

- [Keycloak SPI Documentation](https://www.keycloak.org/docs/latest/server_development/#_providers)
- [Authenticator SPI](https://www.keycloak.org/docs/latest/server_development/#_auth_spi)
- [Event Listener SPI](https://www.keycloak.org/docs/latest/server_development/#_events_spi)
- [Protocol Mapper SPI](https://www.keycloak.org/docs/latest/server_development/#_protocol_mappers)
