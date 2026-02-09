---
type: leaf
status: review
updated: 2026-02-07
---

# Boas Práticas

HTTPS obrigatório em produção configurado via KC_HOSTNAME_STRICT_HTTPS=true. Certificados TLS gerenciados por cert-manager com renovação automática 30 dias antes da expiração. Headers de segurança (HSTS, X-Frame-Options, X-Content-Type-Options) configurados no Ingress NGINX.

Admin Console restrito a rede interna via Ingress separado sem exposição pública. Acesso administrativo apenas via VPN ou kubectl port-forward para troubleshooting. Credenciais admin rotacionadas trimestralmente com histórico em vault corporativo.

Política de senha configurada em Realm Settings > Authentication > Password Policy. Mínimo 8 caracteres (length(8) no realm-export.json). Expiração de senha desabilitada para evitar fadiga de segurança, compensada por monitoramento de credenciais vazadas.

Tokens com vida curta: access token 5 minutos, SSO session idle 30 minutos e SSO session max 10 horas. Refresh token rotation atualmente desligada no realm-export.json (revokeRefreshToken: false), ADR-003 recomenda ativar em producao. Algoritmo RS256 para assinatura com chaves RSA de 2048 bits rotacionadas anualmente.

Audit logging habilitado para todos os eventos de autenticação e administração. Logs exportados para SIEM corporativo via syslog ou integração direta. Retenção de 90 dias para compliance e investigação de incidentes.
