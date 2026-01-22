---
type: adr
status: rejected
updated: 2026-01-21
description: "Escopo muito amplo. Mistura 7 decisoes diferentes (brute force, rate limit, senha, admin, TLS, audit, headers). Separar ou mover para SECURITY. Contem blocos de codigo."
---

# ADR-029: Estrategia de Seguranca Keycloak

## Contexto

Keycloak como identity provider centralizado do CARF e alvo de alto valor para atacantes. Comprometimento do Keycloak significa acesso potencial a todas aplicacoes e dados de todos tenants. Estrategia de seguranca deve cobrir: protecao contra ataques de autenticacao, politicas de credenciais, isolamento administrativo, e auditoria.

O sistema atende prefeituras municipais com dados sensiveis de regularizacao fundiaria, exigindo conformidade com LGPD e melhores praticas de seguranca do setor publico.

## Decisao

Implementar **estrategia de seguranca em camadas** cobrindo infraestrutura, aplicacao, credenciais e monitoramento.

### 1. Protecao Contra Brute Force

| Configuracao | Valor | Motivo |
|:-------------|:------|:-------|
| Falhas para bloqueio temporario | 5 | Previne adivinhacao de senha |
| Duracao bloqueio temporario | 15 minutos | Tempo para atacante desistir |
| Falhas para bloqueio permanente | 30 | Conta comprometida requer intervencao |
| Reset de contador | Apos login bem-sucedido | Usuario legitimo nao acumula falhas |

### 2. Rate Limiting (Ingress NGINX)

| Endpoint | Limite | Burst |
|:---------|:-------|:------|
| `/realms/*/protocol/openid-connect/token` | 10 req/s | 20 |
| `/realms/*/protocol/openid-connect/auth` | 10 req/s | 20 |
| Demais endpoints | 100 req/s | 200 |

IPs que excedem limites repetidamente bloqueados por 1 hora.

### 3. Politica de Senha

| Requisito | Valor |
|:----------|:------|
| Comprimento minimo | 12 caracteres |
| Maiusculas | 1+ |
| Minusculas | 1+ |
| Numeros | 1+ |
| Caracteres especiais | 1+ |
| Historico bloqueado | 5 senhas anteriores |
| Expiracao | Desabilitada* |

*Expiracao de senha desabilitada para evitar fadiga de seguranca. Compensado por monitoramento de credenciais vazadas (Have I Been Pwned integration).

### 4. Isolamento Admin Console

| Controle | Implementacao |
|:---------|:--------------|
| Exposicao | Apenas rede interna (VPN) |
| Ingress | Separado, sem exposicao publica |
| Acesso emergencial | kubectl port-forward |
| Rotacao de credenciais | Trimestral |
| Armazenamento secrets | HashiCorp Vault |

### 5. Criptografia e Transporte

| Aspecto | Configuracao |
|:--------|:-------------|
| TLS | Obrigatorio (`KC_HOSTNAME_STRICT_HTTPS=true`) |
| Certificados | cert-manager com renovacao automatica 30 dias |
| Algoritmo JWT | RS256 com chaves RSA 2048-bit |
| Rotacao de chaves | Anual (ou imediata se comprometida) |
| HSTS | Enabled via Ingress |

### 6. Audit Logging

| Evento | Logging | Retencao |
|:-------|:--------|:---------|
| Login sucesso/falha | Habilitado | 90 dias |
| Logout | Habilitado | 90 dias |
| Admin actions | Habilitado | 1 ano |
| Token issuance | Habilitado | 90 dias |
| Exportacao | SIEM via syslog | Conforme SIEM |

### 7. Headers de Seguranca

```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; frame-ancestors 'none'
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

## Consequencias

### Positivas

**Defesa em profundidade**: Multiplas camadas de protecao garantem que falha em uma nao compromete sistema inteiro.

**Compliance LGPD**: Audit logging de 90 dias e controles de acesso atendem requisitos de rastreabilidade.

**Deteccao rapida**: Monitoramento de anomalias no SIEM permite resposta a incidentes em tempo habil.

**Resiliencia a brute force**: Combinacao de bloqueio de conta e rate limiting torna ataques de forca bruta ineficazes.

### Negativas

**UX impactada por bloqueio**: Usuarios legitimos que esquecem senha podem ser bloqueados temporariamente.

**Overhead de auditoria**: Logging de todos eventos aumenta volume de dados e custo de storage.

**Complexidade operacional**: Acesso admin via VPN adiciona fricao para operacoes legitimas.

### Neutras

**CAPTCHA condicional**: reCAPTCHA v3 habilitado apenas quando detectada atividade suspeita, nao em todos os logins.

## Alternativas Rejeitadas

### Expiracao de Senha Periodica

Forcar troca de senha a cada 90 dias.

**Motivo da rejeicao**: Pesquisas demonstram que expiracao periodica leva usuarios a escolher senhas mais fracas e previsiveis (Senha1!, Senha2!). Monitoramento de vazamentos e mais eficaz.

### WAF Completo

Implementar Web Application Firewall dedicado.

**Motivo da rejeicao**: Rate limiting no Ingress NGINX e protecoes nativas do Keycloak sao suficientes para o perfil de risco atual. WAF pode ser adicionado se necessario futuramente.

### MFA Obrigatorio para Todos

Exigir segundo fator para todos usuarios.

**Motivo da rejeicao**: Agentes de campo em areas remotas podem nao ter acesso a celular para OTP. MFA habilitado para roles admin e super-admin; opcional para demais.

## Implementacao

### Keycloak Realm Configuration

```json
{
  "bruteForceProtected": true,
  "failureFactor": 5,
  "waitIncrementSeconds": 900,
  "maxFailureWaitSeconds": 900,
  "maxDeltaTimeSeconds": 43200,
  "passwordPolicy": "length(12) and upperCase(1) and lowerCase(1) and digits(1) and specialChars(1) and passwordHistory(5)",
  "eventsEnabled": true,
  "eventsExpiration": 7776000,
  "adminEventsEnabled": true,
  "adminEventsDetailsEnabled": true
}
```

### Alertas SIEM

Configurar alertas para:
- 10+ falhas de login do mesmo IP em 5 minutos
- Login de IP em pais diferente do habitual
- Admin login fora de horario comercial
- Volume anormal de token refreshes
- Tentativas de acesso a admin console de IP externo

## Metricas de Sucesso

- [ ] Zero comprometimentos de conta admin
- [ ] Tempo de deteccao de incidente < 15 minutos
- [ ] 100% de logins via HTTPS
- [ ] Audit logs disponiveis para 100% dos eventos de seguranca
- [ ] Taxa de bloqueio por brute force < 0.1% dos usuarios

## Referencias

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [NIST SP 800-63B Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [Keycloak Security Best Practices](https://www.keycloak.org/docs/latest/server_admin/#_security_defenses)
- [Security Implementation](../../PROJECTS/KEYCLOAK/DOCS/INTEGRATION/SECURITY/)
