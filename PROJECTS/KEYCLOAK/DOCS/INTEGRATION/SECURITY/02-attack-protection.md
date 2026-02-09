---
type: leaf
status: review
updated: 2026-02-07
---

# Proteção Contra Ataques

Brute force protection habilitado em Realm Settings > Security Defenses > Brute Force Detection. Configuração bloqueia usuário após 5 tentativas falhas (failureFactor: 5) com wait máximo de 15 minutos (maxFailureWaitSeconds: 900). Contador de falhas reseta após 12 horas de inatividade (maxDeltaTimeSeconds: 43200), não sendo bloqueio permanente.

Rate limiting adicional via Ingress NGINX limita requisições por IP: 10 req/s para endpoints de autenticação, 100 req/s para demais endpoints. Burst de 20 requisições permitido antes de throttling. IPs que excedem limites repetidamente bloqueados por 1 hora.

CAPTCHA opcional integrado via Google reCAPTCHA v3. Habilitado dinamicamente quando detecção de brute force identifica atividade suspeita de IP específico. Configuração em Authentication > Flows > Browser com execução condicional baseada em risco.

Proteção contra CSRF via token state em todos os fluxos OAuth. Keycloak valida que state enviado no redirect corresponde ao gerado na requisição inicial. Aplicações devem sempre gerar state único e verificar no callback.

Content Security Policy configurado para prevenir XSS em páginas do Keycloak. Diretiva script-src permite apenas scripts inline necessários para funcionamento do formulário de login. Frame-ancestors restringe embedding apenas para domínios autorizados.

Monitoramento de anomalias via alertas no SIEM para padrões suspeitos: múltiplos logins de geografias distantes, tentativas de login fora do horário comercial para contas administrativas, volume anormal de refresh tokens.
