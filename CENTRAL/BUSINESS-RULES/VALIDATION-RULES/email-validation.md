# Email Validation

Regra de validação de endereço de email garantindo formato correto segundo RFC 5322 antes de armazenamento e envio de notificações onde validação inclui verificação de estrutura local@domínio, caracteres permitidos na parte local (letras números pontos hifens underscore), domínio válido com TLD reconhecido, e normalização para lowercase antes de comparação e armazenamento evitando duplicação por diferença de case. Validação estrita rejeita emails com caracteres especiais não comuns ou quoted strings para simplificar implementação e evitar problemas de compatibilidade com sistemas de email corporativos, enquanto validação permissiva aceita formatos RFC 5322 completos incluindo plus addressing (user+tag@domain) útil para organização de notificações. Email é único por tenant impedindo cadastro duplicado de mesmo titular ou conta com validação de unicidade executada em camada de application consultando repository, e verificação de domínio MX opcional para validar que domínio possui servidores de email configurados detectando typos comuns em domínios populares.

**Formato aceito:** local@domínio.tld

**Componentes:**
- **Local** (antes do @): Letras, números, ponto, hífen, underscore, plus
- **Domínio** (após o @): Letras, números, hífen, ponto separando labels
- **TLD** (extensão): Mínimo 2 caracteres, máximo razoável 10

**Regras RFC 5322 (simplificadas):**

Parte local (antes @):
- Caracteres permitidos: a-z, A-Z, 0-9, ., -, _, +
- Não pode começar ou terminar com ponto
- Não pode ter pontos consecutivos (..)
- Case insensitive (normalizar para lowercase)
- Comprimento máximo: 64 caracteres

Domínio (após @):
- Formato: label.label.tld
- Caracteres permitidos em label: a-z, A-Z, 0-9, -
- Label não pode começar ou terminar com hífen
- Cada label: 1-63 caracteres
- TLD válido: mínimo 2 caracteres (br, com, org, etc)
- Case insensitive (normalizar para lowercase)
- Comprimento máximo total: 253 caracteres

**Regex simplificado (validação básica):**

```
^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

Validação completa requer parser RFC 5322 (não apenas regex)

**Normalização:**

1. **Lowercase:** email@DOMAIN.COM → email@domain.com
2. **Trim:** " email@domain.com " → "email@domain.com"
3. **Remove dots em Gmail:** john.doe@gmail.com = johndoe@gmail.com (consideração Gmail-específica)

**Plus addressing (opcional):**

Formato: user+tag@domain.com
- Útil para organização (user+notifications@domain.com)
- Mesmo user com tags diferentes = emails distintos
- Normalização: preservar tag ou remover dependendo de contexto

**Validação de domínio MX (opcional):**

Verificar que domínio possui registro MX (Mail Exchange):
- DNS lookup: MX records para domínio
- Se não possui MX, verificar A record (alguns domínios pequenos)
- Detecta typos: gmial.com, hotmial.com, yahooo.com
- Não garante que email existe (apenas que domínio pode receber)

**Domínios comuns com typos:**

Correto → Typos detectáveis:
- gmail.com → gmial.com, gmai.com, gamil.com
- hotmail.com → hotmial.com, hotmai.com, hotmailcom
- yahoo.com → yahooo.com, yaho.com, yhoo.com
- outlook.com → outloook.com, outlok.com

Sugestão de correção: "Você quis dizer gmail.com?"

**Comprimentos máximos:**

| Componente | Máximo |
|------------|--------|
| Parte local | 64 caracteres |
| Domínio | 253 caracteres |
| Email total | 320 caracteres (64 + @ + 255) |

**Validações adicionais:**

Provedores descartáveis (opcional):
- Bloquear emails temporários: temp-mail.org, guerrillamail.com
- Lista mantida manualmente ou via API de detecção

Unicidade por tenant:
- Verificar em repository se email já existe
- Case insensitive: email@domain.com = EMAIL@domain.com
- Permitir mesmo email em tenants diferentes (multi-tenancy)

**Mensagens de erro:**
- "Email inválido: formato incorreto"
- "Email inválido: parte local excede 64 caracteres"
- "Email inválido: domínio não possui servidor de email configurado"
- "Email inválido: você quis dizer gmail.com?"
- "Email já cadastrado no sistema"
- "Email descartável não permitido (use email permanente)"

**Casos especiais:**

Emails internacionais (IDN):
- Caracteres não-ASCII em domínio (ñ, é, ç)
- Codificação Punycode: münchen.de → xn--mnchen-3ya.de
- Suporte limitado, preferir ASCII

Quoted strings (não suportado):
- "user name"@domain.com (válido RFC mas evitar)
- user@[192.168.1.1] (IP literal, não suportado)

**Armazenamento:** Lowercase normalizado sem espaços

**Exibição:** Como informado pelo usuário (preservar case original se armazenado)

**Uso em notificações:**
- Validar antes de enviar
- Capturar bounces (emails não entregues)
- Marcar email inválido após N bounces consecutivos

---

## 🔗 Relacionado

**Domain Model:**
- `../DOMAIN-MODEL/VALUE-OBJECTS/08-email.md` - Value Object implementando validação
- `../DOMAIN-MODEL/ENTITIES/08-account.md` - Entity usando email validado

**Implementações:**
- `PROJECTS/GEOAPI/LAYERS/DOMAIN/VALUE-OBJECTS/Email.cs` - Backend .NET
- `PROJECTS/GEOWEB/UTILS/validators/emailValidator.ts` - Frontend React
- `PROJECTS/REURBCAD/UTILS/emailValidator.ts` - Mobile React Native

**Referências externas:**
- RFC 5322 - Internet Message Format
- IANA - Lista de TLDs válidos

---

**Última atualização:** 2025-01-06
