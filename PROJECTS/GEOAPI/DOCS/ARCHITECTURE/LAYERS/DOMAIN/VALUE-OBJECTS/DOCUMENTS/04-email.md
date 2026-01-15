# Email

Value object imutável herdando de BaseValueObject representando endereço de email válido com validação de formato RFC 5322 simplificado, garantindo que apenas emails bem-formados sejam armazenados no sistema. Validações incluem verificação de formato básico "local@domain" com local-part contendo caracteres alfanuméricos, pontos, hífens e underscores, símbolo @ obrigatório único, domain com pelo menos um ponto, e TLD (top-level domain) com mínimo 2 caracteres.

Métodos principais incluem construtor recebendo string e validando formato, propriedade Value read-only retornando email normalizado em lowercase para comparações case-insensitive, ToString() retornando valor formatado, Domain() extraindo parte após @ para validações de domínio corporativo, e operadores de igualdade comparando valores normalizados.

Usado em Account para email do usuário vinculado ao Keycloak garantindo unicidade de login, Holder para contato opcional do titular, envio de notificações e recuperação de senha, e validação de domínios permitidos em configurações de Tenant (ex: apenas emails @prefeitura.gov.br podem criar contas).

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
