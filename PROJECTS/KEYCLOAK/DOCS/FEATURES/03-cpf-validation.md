---
type: leaf
status: approved
updated: 2026-02-07
---

# CPF Validation

Validacao de CPF no ecossistema CARF ocorre em duas camadas complementares: client-side via JavaScript no formulario de login do Keycloak e server-side via SPI Java Authenticator. Ambas utilizam o algoritmo Mod11 compativel com a implementacao em @carf/tscore.

## Validacao Client-Side

A validacao client-side e implementada no tema FreeMarker atual via JavaScript puro nos arquivos login.js e carf-validations.js (ver [06-login-theme-carf.md](./06-login-theme-carf.md)). No contexto do tema CARF, o campo de username aceita CPF ou email. Quando o valor digitado segue padrao numerico, o script aplica automaticamente mascara XXX.XXX.XXX-XX e valida digitos verificadores em tempo real. A migracao futura para Keycloakify (conforme [ADR-001](../ADRs/ADR-001-keycloakify-adoption.md)) substituira este JavaScript por um hook React useCpfMask do pacote @carf/ui.

O algoritmo de validacao limpa caracteres nao numericos, verifica comprimento exato de 11 digitos, rejeita sequencias conhecidas como invalidas (000.000.000-00, 111.111.111-11 etc.) e calcula ambos os digitos verificadores via multiplicacao ponderada com modulo 11. Feedback visual e imediato: borda vermelha e mensagem de erro aparecem no evento blur do input, sem esperar submit do formulario. No submit, o formulario e bloqueado se o CPF for invalido, exibindo alerta de erro.

## Validacao Server-Side via SPI

O CpfValidatorAuthenticator e uma SPI Java que executa como step no authentication flow do Keycloak. No metodo authenticate, extrai o username do usuario, remove caracteres nao numericos, verifica 11 digitos e calcula digitos verificadores conforme Mod11. Se invalido, retorna AuthenticationFlowError.INVALID_USER impedindo login. Se valido, chama context.success() permitindo prosseguir para verificacao de senha. A Factory registra provider ID "carf-cpf-validator" com display type "CARF CPF Validator".

A ativacao requer copiar o flow Browser para "Browser CARF" em Authentication, Flows, adicionar execution "CARF CPF Validator" como Required e vincular ao realm como Browser Flow.

## User Profile Attributes

O campo CPF e configurado como user attribute obrigatorio no User Profile do Keycloak. A configuracao define validacao via pattern regex (11 digitos ou formato XXX.XXX.XXX-XX), mensagem de erro customizada em portugues, e permissoes onde admin pode editar e usuario pode apenas visualizar. O campo e adicionado ao grupo "Personal Information" com displayOrder apos nome e antes de email.

## Unicidade e Isolamento

A unicidade de CPF e validada no nvel de tenant: o mesmo CPF pode existir em tenants diferentes (cenarios de municipios vizinhos) mas nao dentro do mesmo tenant. O backend GEOAPI verifica unicidade via query SELECT filtrando por tenant_id antes de criar ou atualizar usuario.

## Migracao de Usuarios

Usuarios existentes sem CPF preenchido podem ser migados via Required Action UPDATE_PROFILE que forca preenchimento do perfil no proximo login, incluindo CPF como campo obrigatorio com validacao inline.
