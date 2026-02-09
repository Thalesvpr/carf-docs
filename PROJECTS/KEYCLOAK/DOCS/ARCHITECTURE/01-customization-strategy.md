---
type: leaf
status: review
updated: 2026-02-07
---

# Estratégia de Customização do Keycloak

O projeto CARF customiza o Keycloak em três níveis complementares: temas visuais via Keycloakify, extensões funcionais via SPIs Java e configuração declarativa de realm via JSON. Cada nível tem escopo, complexidade e tecnologia distintos, e juntos cobrem todas as necessidades de identidade do sistema.

## Temas — Customização Visual via Keycloakify

A customização visual utiliza Keycloakify (ADR-001) para desenvolver temas em React e TypeScript, consumindo componentes da biblioteca @carf/ui (Button, Input, FormField, Alert, Card). O resultado do build é um JAR que o Keycloak serve exatamente como um tema FreeMarker tradicional, sem diferença funcional na implantação.

Três tipos de tema são customizados: o tema de login (páginas de autenticação, registro, recuperação de senha, verificação de email e erro), o tema de account (console de gerenciamento de conta do usuário com perfil, sessões e 2FA) e o tema de email (templates de email transacionais para verificação, reset de senha e notificações).

O uso de @carf/ui garante consistência visual absoluta entre as telas de autenticação e as aplicações GEOWEB, ADMIN e WebDocs que consomem a mesma biblioteca. Mudanças no Design System propagam automaticamente para o tema Keycloak. O hook useCpfMask de @carf/ui aplica máscara e validação de CPF diretamente no formulário de login, eliminando a necessidade de reimplementar essa lógica em JavaScript vanilla.

O código fonte do tema fica em PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak-theme/ com estrutura padrão Keycloakify: entry point KcApp.tsx, páginas React em src/login/pages/ (Login.tsx, Register.tsx, ResetPassword.tsx), traduções em i18n.ts, e configuração em keycloakify.config.ts e vite.config.ts.

A abordagem FreeMarker tradicional foi rejeitada por impossibilitar reutilização de @carf/ui e forçar manutenção duplicada de estilos e validações. A documentação FreeMarker existente permanece válida como referência interna de como temas funcionam mas está marcada como legacy.

## Extensions (SPIs) — Customização Funcional

Extensões Java via Keycloak SPI adicionam lógica de negócio ao servidor de autenticação. As extensões planejadas para o CARF são implementadas em Java 17 e empacotadas como JARs copiados para /opt/keycloak/providers/.

O **CPF Authenticator** valida formato e dígitos verificadores de CPF durante o fluxo de autenticação, rejeitando documentos inválidos antes de consultar o banco. O **Tenant Claims Mapper** é um protocol mapper customizado que extrai os atributos de usuário current_tenant, tenants e community_ids e os injeta como claims no JWT dentro do scope carf-tenant. Na prática o realm-export.json já configura protocol mappers nativos (User Attribute → Token Claim) que resolvem esse mapeamento sem código Java, mas o SPI customizado permite lógica adicional como validação de tenant ativo contra a lista de tenants permitidos.

**Event Listeners** customizados capturam eventos de autenticação (login, logout, falha) e administração (criação de usuário, alteração de role) para integração com sistema de logs centralizado e notificações para administradores.

A estrutura do projeto segue o padrão Maven com pacotes organizados em com.carf.keycloak.authenticators, com.carf.keycloak.listeners e com.carf.keycloak.mappers. Testes utilizam JUnit e Keycloak Testcontainers para integração.

## Configuração de Realm — Customização Declarativa

A configuração de realm via realm-export.json (fonte da verdade em CENTRAL/INTEGRATION/KEYCLOAK/realm-export.json) define de forma declarativa todas as entidades do provedor de identidade sem código customizado.

Roles e permissões CARF compreendem seis roles de realm em hierarquia de árvore: field-cadastrator, field-coordinator (herda field-cadastrator), analyst (ramo separado), manager (herda field-coordinator e analyst), admin (herda manager) e super-admin (herda admin). O scope OAuth2 customizado carf-tenant contém os protocol mappers que injetam claims de multi-tenancy no JWT.

A política de senha exige mínimo 8 caracteres (length(8)). Tokens têm vida curta: access token 5 minutos, SSO idle 30 minutos, SSO max 10 horas. Multi-tenancy funciona via atributos de usuário (tenants, current_tenant, community_ids) mapeados para claims JWT por protocol mappers nativos.

O realm-export.json é importado na primeira inicialização do Keycloak e versionado no Git. Alterações feitas via Admin Console devem ser re-exportadas para manter o JSON atualizado.

## Estratégia de Deploy

Em desenvolvimento, o Keycloak roda via Docker Compose (docker-compose.dev.yml) com PostgreSQL 16. O tema Keycloakify é desenvolvido com hot reload via Vite (pnpm dev) e testado conectando ao Keycloak local. Extensions são compiladas com Maven e copiadas manualmente para providers/.

Em staging e produção, uma imagem Docker customizada embute tema JAR e extensions JAR sobre a imagem base quay.io/keycloak/keycloak:24.0.0. O build executa /opt/keycloak/bin/kc.sh build para otimizar providers. Deploy via Kubernetes com configuração por Kustomize overlays.

Versionamento segue: temas e realm config versionados no Git junto com a documentação, extensions com versionamento semântico, e imagem Docker tagged com versão do projeto.
