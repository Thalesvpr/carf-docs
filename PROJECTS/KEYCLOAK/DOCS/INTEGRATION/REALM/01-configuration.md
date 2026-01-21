---
status: review
updated: 2026-01-19
---

# Configuração do Realm

Realm "carf" configurado com seis clients distintos para as aplicações do ecossistema CARF. Configurações de sessão definem SSO Session Idle timeout de 30 minutos (1800 segundos) e SSO Session Max de 10 horas (36000 segundos), com Remember Me habilitado estendendo idle para 24 horas quando usuário marca checkbox no login.

Password policy enforça comprimento mínimo de 8 caracteres incluindo pelo menos um dígito, um caractere lowercase, um uppercase, um caractere especial, e proíbe uso do username como senha seguindo OWASP guidelines. Brute force protection configurado com máximo de 5 tentativas permitidas seguidas de bloqueio de 15 minutos prevenindo ataques de força bruta.

Refresh tokens configurados com max reuse zero garantindo uso único onde cada refresh invalida token anterior e emite novo prevenindo replay attacks. Access tokens com lifetime de 5 minutos (300 segundos) forçando refresh frequente reduzindo janela de exposição em caso de vazamento.

Redirect URIs configurados para cada client incluindo localhost para desenvolvimento e domínios de produção. Web Origins configurados como "+" indicando auto-fill baseado em redirect URIs permitindo requisições CORS apenas de origens registradas prevenindo XSS attacks.
