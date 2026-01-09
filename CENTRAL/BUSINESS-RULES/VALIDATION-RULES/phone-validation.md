# Phone Validation

Regra de validação de número de telefone brasileiro garantindo formato correto com DDD código de área válido e número com quantidade correta de dígitos onde validação inclui verificação de código país (55 para Brasil), DDD válido (11 a 99 conforme Anatel), distinção entre telefone fixo (8 dígitos) e móvel (9 dígitos iniciando com 9), e normalização para formato canônico apenas dígitos antes de armazenamento facilitando comparação e queries. Telefone pode ser fornecido formatado com parênteses espaços e hífens (exemplo: (11) 98765-4321 ou +55 11 3456-7890) sendo normalizado removendo caracteres não numéricos antes de validação, e armazenamento inclui código país facilitando integração com sistemas de SMS e chamadas internacionais. Validação de DDD utiliza lista oficial Anatel com códigos atribuídos por estado onde códigos 11-19 são São Paulo, 21-28 Rio de Janeiro e Espírito Santo, 31-38 Minas Gerais, 41-49 Paraná e Santa Catarina, 51-55 Rio Grande do Sul, 61-69 Centro-Oeste e Norte, 71-79 Nordeste, 81-89 Pernambuco Paraíba Alagoas, 91-99 Pará e Amazonas permitindo validar que DDD corresponde a região esperada do usuário.

**Formato aceito:** +55 (DD) NNNNN-NNNN ou variações normalizadas

**Componentes:**
- **Código país:** +55 (Brasil, opcional na entrada mas obrigatório no armazenamento)
- **DDD:** 2 dígitos (11-99 conforme Anatel)
- **Número:** 8 dígitos (fixo) ou 9 dígitos (móvel começando com 9)

**Estrutura:**

Telefone móvel: +55 11 98765-4321
- Código país: 55
- DDD: 11 (São Paulo)
- Número: 98765-4321 (9 dígitos, inicia com 9)

Telefone fixo: +55 11 3456-7890
- Código país: 55
- DDD: 11 (São Paulo)
- Número: 3456-7890 (8 dígitos, inicia com 2-5)

**DDDs válidos por região (Anatel):**

| Região | DDDs | Estados |
|--------|------|---------|
| São Paulo | 11-19 | SP |
| Rio de Janeiro | 21-24, 22 | RJ |
| Espírito Santo | 27-28 | ES |
| Minas Gerais | 31-38 | MG |
| Paraná | 41-46 | PR |
| Santa Catarina | 47-49 | SC |
| Rio Grande do Sul | 51-55 | RS |
| Distrito Federal | 61 | DF |
| Goiás | 62, 64 | GO |
| Tocantins | 63 | TO |
| Mato Grosso | 65, 66 | MT |
| Mato Grosso do Sul | 67 | MS |
| Acre | 68 | AC |
| Rondônia | 69 | RO |
| Bahia | 71, 73-75, 77 | BA |
| Sergipe | 79 | SE |
| Pernambuco | 81, 87 | PE |
| Alagoas | 82 | AL |
| Paraíba | 83 | PB |
| Rio Grande do Norte | 84 | RN |
| Ceará | 85, 88 | CE |
| Piauí | 86, 89 | PI |
| Pará | 91, 93, 94 | PA |
| Amazonas | 92, 97 | AM |
| Amapá | 96 | AP |
| Roraima | 95 | RR |
| Maranhão | 98, 99 | MA |

**Validações aplicadas:**

1. **DDD válido:**
   - DDD entre 11 e 99
   - DDD existe na lista Anatel
   - Validação estrita: verificar tabela completa

2. **Número de dígitos:**
   - Móvel: 9 dígitos, primeiro dígito = 9
   - Fixo: 8 dígitos, primeiro dígito = 2-5
   - Rejeitar se não corresponde ao padrão

3. **Formato numérico:**
   - Apenas dígitos após normalização
   - Comprimento total: 10-11 dígitos (DDD + número)

**Normalização:**

Entrada: "(11) 98765-4321" ou "+55 11 98765-4321" ou "11987654321"

Normalizado: 5511987654321 (código país + DDD + número)

Passos:
1. Remover caracteres não numéricos: ( ) - espaço +
2. Se inicia com 0 (DDD com zero à esquerda): remover primeiro 0
3. Se não inicia com 55: adicionar código país 55
4. Validar comprimento: 12-13 dígitos (55 + DDD 2 dígitos + número 8-9 dígitos)

**Armazenamento:** 5511987654321 (string 12-13 dígitos)

**Exibição:**
- Nacional: (11) 98765-4321
- Internacional: +55 11 98765-4321
- Compacto: 11987654321

**Validações adicionais:**

Distinguir móvel vs fixo:
- Móvel: 9 dígitos iniciando com 9
- Fixo: 8 dígitos iniciando com 2-5
- Útil para escolher canal de notificação (SMS apenas móvel)

Validar região:
- Se conhecido estado do usuário, validar DDD corresponde
- Alertar se DDD de região diferente (possível erro)

Números especiais (não validar):
- 0800 (gratuito)
- 0300 (custo compartilhado)
- 190, 192, 193 (emergência e serviços)

**Mensagens de erro:**
- "Telefone inválido: DDD não reconhecido"
- "Telefone inválido: número de dígitos incorreto"
- "Telefone inválido: móvel deve iniciar com 9"
- "Telefone inválido: fixo deve ter 8 dígitos"
- "Telefone já cadastrado no sistema"

**Casos especiais:**

Telefones antigos (pré-2017):
- Móveis SP e RJ tinham 8 dígitos
- Desde 2017 todos móveis Brasil têm 9 dígitos
- Aceitar apenas formato atual (9 dígitos)

Números estrangeiros:
- Não validar como brasileiro
- Aceitar formato internacional genérico
- Regex: ^\+\d{1,3}\s?\d{6,14}$

**Regex validação (após normalização):**

Móvel brasileiro:
```
^55[1-9]{2}9[0-9]{8}$
```

Fixo brasileiro:
```
^55[1-9]{2}[2-5][0-9]{7}$
```

**Uso em notificações SMS:**
- Validar antes de enviar
- Capturar status de entrega
- Marcar inválido após N falhas consecutivas
- Preferir SMS para números móveis verificados

---

## 🔗 Relacionado

**Domain Model:**
- `../DOMAIN-MODEL/VALUE-OBJECTS/09-phone-number.md` - Value Object implementando validação
- `../DOMAIN-MODEL/ENTITIES/02-holder.md` - Entity usando telefone validado

**Anatel:**
- Tabela oficial de DDDs por região
- Plano de numeração brasileiro

**Implementações:**
- `PROJECTS/GEOAPI/LAYERS/DOMAIN/VALUE-OBJECTS/PhoneNumber.cs` - Backend .NET
- `PROJECTS/GEOWEB/UTILS/validators/phoneValidator.ts` - Frontend React
- `PROJECTS/REURBCAD/UTILS/phoneValidator.ts` - Mobile React Native

---

**Última atualização:** 2025-01-06
