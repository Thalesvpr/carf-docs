# Estratégia de Customização do Keycloak

## Visão Geral

O projeto CARF utiliza Keycloak como provedor de identidade centralizado (IdP) com customizações específicas para atender aos requisitos de UX e funcionalidades especializadas para o domínio de regularização fundiária urbana.

## Níveis de Customização

### 1. Temas (Themes) - Customização Visual

**Escopo:** Interface do usuário
**Complexidade:** Baixa
**Tecnologias:** HTML, CSS, JavaScript, FreeMarker

Customizações de tema incluem:

#### Login Theme
- Página de login com identidade visual CARF
- Formulários de registro
- Páginas de erro
- Recuperação de senha
- Verificação de email

#### Account Theme
- Console de gerenciamento de conta do usuário
- Página de perfil
- Gerenciamento de sessões
- Autenticação de dois fatores (2FA)

#### Email Theme
- Templates de email transacionais
- Email de boas-vindas
- Notificações de alteração de senha
- Verificação de email

**Arquivos customizados:**
```
themes/carf/
├── login/
│   ├── theme.properties
│   ├── resources/
│   │   ├── css/
│   │   │   └── login.css
│   │   ├── js/
│   │   │   └── login.js
│   │   └── img/
│   │       └── logo.svg
│   └── login.ftl
├── account/
│   ├── theme.properties
│   └── resources/
└── email/
    ├── theme.properties
    └── html/
        ├── email-verification.ftl
        └── password-reset.ftl
```

### 2. Extensions (SPIs) - Customização Funcional

**Escopo:** Lógica de negócio
**Complexidade:** Média/Alta
**Tecnologias:** Java 17, Keycloak SPI

Extensões potenciais para CARF:

#### Custom Authenticators
- Validação de CPF durante registro
- Integração com sistemas externos de validação de identidade
- Autenticação baseada em geolocalização (para fiscais de campo)

#### Event Listeners
- Auditoria customizada de eventos
- Integração com sistema de logs centralizado
- Notificações para administradores

#### User Storage SPI
- Federação com sistemas legados de usuários
- Importação de usuários de sistemas municipais existentes

#### Protocol Mappers
- Claims customizados no JWT (tenant_id, roles específicas REURB)
- Mapeamento de atributos específicos do domínio

**Estrutura de extension:**
```
extensions/
├── pom.xml
└── src/
    └── main/
        └── java/
            └── com/
                └── carf/
                    └── keycloak/
                        ├── authenticators/
                        ├── listeners/
                        └── mappers/
```

### 3. Configuração de Realm

**Escopo:** Configuração declarativa
**Complexidade:** Baixa
**Tecnologias:** JSON (realm export/import)

Customizações de realm:

- Roles e permissões CARF (ADMIN, ANALYST, FIELD_AGENT, MUNICIPALITY_MANAGER, PUBLIC)
- Scopes OAuth2 customizados (carf-tenant, reurb-permissions)
- Políticas de senha conforme LGPD
- Configuração de sessões e tokens
- Multi-tenancy via atributos de usuário

**Arquivo:** `realm-export.json` (em CENTRAL/INTEGRATION/KEYCLOAK/)

## Estratégia de Desenvolvimento

### Ambiente de Desenvolvimento

1. **Keycloak local com hot-reload de temas:**
   ```bash
   docker run -p 8080:8080 \
     -e KEYCLOAK_ADMIN=admin \
     -e KEYCLOAK_ADMIN_PASSWORD=admin \
     -v ./themes:/opt/keycloak/themes \
     quay.io/keycloak/keycloak:24.0.0 start-dev
   ```

2. **Build de extensions:**
   ```bash
   cd extensions
   mvn clean package
   cp target/carf-keycloak-extensions.jar /opt/keycloak/providers/
   ```

### Estratégia de Deployment

#### Development
- Keycloak standalone com Docker Compose
- Temas montados via volume
- Extensions copiados manualmente

#### Staging/Production
- Imagem Docker customizada com temas e extensions embutidos
- Deployment via Kubernetes
- Configuração via Kustomize overlays

**Dockerfile customizado:**
```dockerfile
FROM quay.io/keycloak/keycloak:24.0.0

# Copiar temas customizados
COPY themes/carf /opt/keycloak/themes/carf

# Copiar extensions
COPY extensions/target/*.jar /opt/keycloak/providers/

# Rebuild do Keycloak com extensions
RUN /opt/keycloak/bin/kc.sh build

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
```

## Versionamento

- **Temas:** Versionados junto com o código (Git)
- **Extensions:** Versionamento semântico (MAJOR.MINOR.PATCH)
- **Realm configuration:** Exportado e versionado no Git
- **Imagem Docker:** Tagged com versão do projeto (ex: `carf-keycloak:1.2.0`)

## Testes

### Temas
- Testes manuais de UI/UX
- Testes de responsividade (mobile, desktop)
- Validação de acessibilidade (WCAG 2.1)

### Extensions
- Unit tests (JUnit)
- Integration tests com Keycloak Testcontainers
- Testes de performance para authenticators customizados

### Realm Configuration
- Testes de importação/exportação
- Validação de roles e permissões
- Testes de fluxos OAuth2/OIDC

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Muitas listas com bullets (47) antes do rodapé - considerar converter para parágrafo denso; Contém code blocks - considerar converter para prosa.
