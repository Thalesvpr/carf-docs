# Boas Práticas

HTTPS obrigatório em produção configurado via KC_HOSTNAME_STRICT_HTTPS=true. Certificados TLS gerenciados por cert-manager com renovação automática 30 dias antes da expiração. Headers de segurança (HSTS, X-Frame-Options, X-Content-Type-Options) configurados no Ingress NGINX.

Admin Console restrito a rede interna via Ingress separado sem exposição pública. Acesso administrativo apenas via VPN ou kubectl port-forward para troubleshooting. Credenciais admin rotacionadas trimestralmente com histórico em vault corporativo.

Política de senha configurada em Realm Settings > Authentication > Password Policy. Mínimo 12 caracteres, pelo menos 1 maiúscula, 1 minúscula, 1 número e 1 caractere especial. Histórico de 5 senhas anteriores bloqueado para reuso. Expiração de senha desabilitada para evitar fadiga de segurança, compensada por monitoramento de credenciais vazadas.

Tokens com vida curta: access token 5 minutos, refresh token 30 minutos idle e 8 horas máximo. Refresh token rotation ativado invalida token anterior após cada uso. Algoritmo RS256 para assinatura com chaves RSA de 2048 bits rotacionadas anualmente.

Audit logging habilitado para todos os eventos de autenticação e administração. Logs exportados para SIEM corporativo via syslog ou integração direta. Retenção de 90 dias para compliance e investigação de incidentes.

---

**Status:** Review
**Atualizado:** 2026-01-19
**Descrição:** 
