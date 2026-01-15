# Design Principles - ADMIN

## Princípios

**(1) Security-First** - assume que toda entrada é maliciosa, valida TUDO no backend, rate limiting em endpoints admin, sanitiza outputs para prevenir XSS, client_secret NUNCA no frontend, **(2) Principle of Least Privilege** - usuários têm apenas permissões mínimas necessárias, roles segregadas (ADMIN gerencia próprio tenant, SUPER_ADMIN gerencia todos), **(3) Explicit Over Implicit** - preferir mutations explícitas a automáticas, verbose error messages para admins debugarem, **(4) Idempotency** - operações podem ser retried sem side effects duplicados (ex: delete tenant verificando se existe antes), **(5) Audit Everything** - log TODAS mutations administrativas para compliance, **(6) Fail Securely** - em caso de erro, negar acesso ao invés de permitir, mostrar erro genérico para users mas logar detalhes completos.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
