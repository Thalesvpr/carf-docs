---
type: leaf
status: current
updated: 2026-01-23
---

# Estrategia de Seguranca

O CARF implementa defesa em profundidade com multiplas camadas de protecao para o Keycloak como identity provider centralizado e para os dados sensiveis de regularizacao fundiaria.

A protecao contra brute force bloqueia contas apos 5 tentativas falhas por 15 minutos, com bloqueio permanente apos 30 falhas exigindo intervencao administrativa. Rate limiting no Ingress NGINX limita endpoints de autenticacao a 10 requisicoes por segundo, bloqueando IPs abusivos por 1 hora. A politica de senha exige minimo 12 caracteres com maiusculas, minusculas, numeros e simbolos, proibindo reutilizacao das 5 senhas anteriores.

O Admin Console do Keycloak e acessivel apenas via VPN ou kubectl port-forward, nunca exposto publicamente. MFA via TOTP e obrigatorio para roles admin e super-admin. Toda comunicacao usa TLS 1.3 com certificados renovados automaticamente via cert-manager. Tokens JWT usam RS256 com chaves RSA 2048-bit rotacionadas anualmente.

Audit logging registra todos eventos de autenticacao com retencao de 90 dias, e acoes administrativas por 1 ano. Logs sao exportados para SIEM via syslog com alertas configurados para anomalias como multiplas falhas de login ou acesso fora de horario comercial. Headers de seguranca incluem HSTS, X-Frame-Options DENY e Content-Security-Policy restritiva.
