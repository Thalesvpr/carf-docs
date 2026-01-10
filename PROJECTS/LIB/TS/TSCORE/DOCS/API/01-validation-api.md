# Validation API - Referência Completa

## Visão Geral

API completa dos [Value Objects](../CONCEPTS/01-value-objects.md) de validação fornecidos pelo @carf/tscore conforme especificações de domínio em [CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS](../../../../../../CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/README.md). Todos os validadores seguem o padrão de Value Object imutável com validação no construtor.

## Import Path

```typescript
import { CPF, CNPJ, Email, PhoneNumber } from '@carf/tscore/validations'
```

## Class: CPF

Valida e manipula CPF brasileiro com dígitos verificadores.

📖 **[CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/01-cpf.md](../../../../../../CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/01-cpf.md)** - Especificação do domínio

### Constructor

```typescript
constructor(value: string)
```

Cria instância de CPF validado.

**Parâmetros:**
- `value` (string) - CPF com ou sem máscara (ex: "123.456.789-09" ou "12345678909")

**Throws:**
- `ValidationError` - Se CPF for inválido

**Exemplo:**
```typescript
const cpf = new CPF('123.456.789-09')  // ✅
const cpf2 = new CPF('12345678909')    // ✅
const cpf3 = new CPF('000.000.000-00') // ❌ Throws ValidationError
```

### Properties

#### value

```typescript
readonly value: string
```

CPF sem máscara (somente 11 dígitos numéricos).

**Exemplo:**
```typescript
const cpf = new CPF('123.456.789-09')
console.log(cpf.value) // "12345678909"
```

### Methods

#### format()

```typescript
format(): string
```

Retorna CPF formatado com máscara `###.###.###-##`.

**Returns:** CPF formatado

**Exemplo:**
```typescript
const cpf = new CPF('12345678909')
console.log(cpf.format()) // "123.456.789-09"
```

#### toString()

```typescript
toString(): string
```

Converte para string sem máscara (alias para `.value`).

**Returns:** CPF sem máscara

**Exemplo:**
```typescript
const cpf = new CPF('123.456.789-09')
console.log(cpf.toString()) // "12345678909"
console.log(`CPF: ${cpf}`)  // "CPF: 12345678909"
```

#### equals()

```typescript
equals(other: CPF): boolean
```

Compara igualdade com outro CPF.

**Parâmetros:**
- `other` (CPF) - Outro CPF para comparar

**Returns:** `true` se CPFs são iguais

**Exemplo:**
```typescript
const cpf1 = new CPF('123.456.789-09')
const cpf2 = new CPF('12345678909')
const cpf3 = new CPF('987.654.321-00')

console.log(cpf1.equals(cpf2)) // true (mesmo CPF)
console.log(cpf1.equals(cpf3)) // false
```

### Static Methods

#### isValid()

```typescript
static isValid(value: string): boolean
```

Valida CPF sem lançar exceção.

**Parâmetros:**
- `value` (string) - CPF a validar

**Returns:** `true` se válido, `false` caso contrário

**Exemplo:**
```typescript
CPF.isValid('123.456.789-09') // true
CPF.isValid('000.000.000-00') // false
CPF.isValid('abc')            // false
```

#### format()

```typescript
static format(value: string): string
```

Formata CPF sem criar instância.

**Parâmetros:**
- `value` (string) - CPF sem máscara

**Returns:** CPF formatado

**Throws:**
- `ValidationError` - Se CPF for inválido

**Exemplo:**
```typescript
CPF.format('12345678909') // "123.456.789-09"
```

#### clean()

```typescript
static clean(value: string): string
```

Remove máscara do CPF.

**Parâmetros:**
- `value` (string) - CPF com ou sem máscara

**Returns:** CPF sem máscara (11 dígitos)

**Exemplo:**
```typescript
CPF.clean('123.456.789-09') // "12345678909"
CPF.clean('12345678909')     // "12345678909"
```

### Validações Aplicadas

1. **Formato:** Exatamente 11 dígitos numéricos
2. **CPFs Conhecidos Inválidos:**
   - `00000000000`, `11111111111`, `22222222222`, ..., `99999999999`
3. **Dígito Verificador 1 (d1):**
   - Cálculo: `d1 = 11 - ((Σ(cpf[i] * (10-i)) % 11)`
   - Se resultado >= 10, d1 = 0
4. **Dígito Verificador 2 (d2):**
   - Cálculo: `d2 = 11 - ((Σ(cpf[i] * (11-i)) % 11)`
   - Se resultado >= 10, d2 = 0

📖 **Algoritmo completo:** [CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/01-cpf.md](../../../../../../CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/01-cpf.md)

---

## Class: CNPJ

Valida e manipula CNPJ brasileiro com dígitos verificadores.

📖 ****CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/02-cnpj.md**** - Especificação do domínio

### Constructor

```typescript
constructor(value: string)
```

Cria instância de CNPJ validado.

**Parâmetros:**
- `value` (string) - CNPJ com ou sem máscara (ex: "11.444.777/0001-61" ou "11444777000161")

**Throws:**
- `ValidationError` - Se CNPJ for inválido

**Exemplo:**
```typescript
const cnpj = new CNPJ('11.444.777/0001-61')  // ✅
const cnpj2 = new CNPJ('11444777000161')      // ✅
const cnpj3 = new CNPJ('00.000.000/0000-00') // ❌ Throws ValidationError
```

### Properties

#### value

```typescript
readonly value: string
```

CNPJ sem máscara (somente 14 dígitos numéricos).

**Exemplo:**
```typescript
const cnpj = new CNPJ('11.444.777/0001-61')
console.log(cnpj.value) // "11444777000161"
```

### Methods

#### format()

```typescript
format(): string
```

Retorna CNPJ formatado com máscara `##.###.###/####-##`.

**Returns:** CNPJ formatado

**Exemplo:**
```typescript
const cnpj = new CNPJ('11444777000161')
console.log(cnpj.format()) // "11.444.777/0001-61"
```

#### toString()

```typescript
toString(): string
```

Converte para string sem máscara.

**Returns:** CNPJ sem máscara

**Exemplo:**
```typescript
const cnpj = new CNPJ('11.444.777/0001-61')
console.log(cnpj.toString()) // "11444777000161"
```

#### equals()

```typescript
equals(other: CNPJ): boolean
```

Compara igualdade com outro CNPJ.

**Parâmetros:**
- `other` (CNPJ) - Outro CNPJ para comparar

**Returns:** `true` se CNPJs são iguais

**Exemplo:**
```typescript
const cnpj1 = new CNPJ('11.444.777/0001-61')
const cnpj2 = new CNPJ('11444777000161')

console.log(cnpj1.equals(cnpj2)) // true
```

### Static Methods

#### isValid()

```typescript
static isValid(value: string): boolean
```

Valida CNPJ sem lançar exceção.

**Parâmetros:**
- `value` (string) - CNPJ a validar

**Returns:** `true` se válido, `false` caso contrário

**Exemplo:**
```typescript
CNPJ.isValid('11.444.777/0001-61') // true
CNPJ.isValid('00.000.000/0000-00') // false
```

#### format()

```typescript
static format(value: string): string
```

Formata CNPJ sem criar instância.

**Parâmetros:**
- `value` (string) - CNPJ sem máscara

**Returns:** CNPJ formatado

**Throws:**
- `ValidationError` - Se CNPJ for inválido

**Exemplo:**
```typescript
CNPJ.format('11444777000161') // "11.444.777/0001-61"
```

#### clean()

```typescript
static clean(value: string): string
```

Remove máscara do CNPJ.

**Parâmetros:**
- `value` (string) - CNPJ com ou sem máscara

**Returns:** CNPJ sem máscara (14 dígitos)

**Exemplo:**
```typescript
CNPJ.clean('11.444.777/0001-61') // "11444777000161"
CNPJ.clean('11444777000161')      // "11444777000161"
```

### Validações Aplicadas

1. **Formato:** Exatamente 14 dígitos numéricos
2. **CNPJs Conhecidos Inválidos:**
   - `00000000000000`, `11111111111111`, etc.
3. **Dígitos Verificadores:** Algoritmo mod-11 similar ao CPF

---

## Class: Email

Valida e normaliza endereços de email conforme RFC 5322.

📖 ****CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/04-email.md**** - Especificação do domínio

### Constructor

```typescript
constructor(value: string)
```

Cria instância de Email validado e normalizado.

**Parâmetros:**
- `value` (string) - Endereço de email

**Throws:**
- `ValidationError` - Se email for inválido

**Exemplo:**
```typescript
const email = new Email('user@example.com')     // ✅
const email2 = new Email('USER@EXAMPLE.COM')    // ✅ (normalizado para lowercase)
const email3 = new Email('invalid-email')       // ❌ Throws ValidationError
```

### Properties

#### value

```typescript
readonly value: string
```

Email normalizado (lowercase).

**Exemplo:**
```typescript
const email = new Email('USER@EXAMPLE.COM')
console.log(email.value) // "user@example.com"
```

#### local

```typescript
readonly local: string
```

Parte local do email (antes do @).

**Exemplo:**
```typescript
const email = new Email('user@example.com')
console.log(email.local) // "user"
```

#### domain

```typescript
readonly domain: string
```

Domínio do email (depois do @).

**Exemplo:**
```typescript
const email = new Email('user@example.com')
console.log(email.domain) // "example.com"
```

### Methods

#### toString()

```typescript
toString(): string
```

Converte para string (alias para `.value`).

**Returns:** Email normalizado

**Exemplo:**
```typescript
const email = new Email('USER@EXAMPLE.COM')
console.log(email.toString()) // "user@example.com"
```

#### equals()

```typescript
equals(other: Email): boolean
```

Compara igualdade com outro Email.

**Parâmetros:**
- `other` (Email) - Outro Email para comparar

**Returns:** `true` se emails são iguais (case-insensitive)

**Exemplo:**
```typescript
const email1 = new Email('user@example.com')
const email2 = new Email('USER@EXAMPLE.COM')
const email3 = new Email('other@example.com')

console.log(email1.equals(email2)) // true
console.log(email1.equals(email3)) // false
```

### Static Methods

#### isValid()

```typescript
static isValid(value: string): boolean
```

Valida email sem lançar exceção.

**Parâmetros:**
- `value` (string) - Email a validar

**Returns:** `true` se válido, `false` caso contrário

**Exemplo:**
```typescript
Email.isValid('user@example.com') // true
Email.isValid('invalid-email')    // false
Email.isValid('@example.com')     // false
```

#### normalize()

```typescript
static normalize(value: string): string
```

Normaliza email para lowercase.

**Parâmetros:**
- `value` (string) - Email a normalizar

**Returns:** Email normalizado

**Exemplo:**
```typescript
Email.normalize('USER@EXAMPLE.COM') // "user@example.com"
```

### Validações Aplicadas

1. **Formato RFC 5322:** `local-part@domain`
2. **Parte local:** Não vazia, caracteres válidos
3. **Domínio:** Contém TLD válido (`.com`, `.br`, etc.)
4. **Normalização:** Converte para lowercase

---

## Class: PhoneNumber

Valida e formata telefones brasileiros com DDD.

📖 ****CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/05-phone-number.md**** - Especificação do domínio

### Constructor

```typescript
constructor(value: string)
```

Cria instância de PhoneNumber validado.

**Parâmetros:**
- `value` (string) - Telefone com ou sem máscara (ex: "(11) 98765-4321" ou "11987654321")

**Throws:**
- `ValidationError` - Se telefone for inválido

**Exemplo:**
```typescript
const phone = new PhoneNumber('(11) 98765-4321')  // ✅ Móvel
const phone2 = new PhoneNumber('11987654321')      // ✅
const phone3 = new PhoneNumber('(11) 3456-7890')  // ✅ Fixo
const phone4 = new PhoneNumber('123')             // ❌ Throws ValidationError
```

### Properties

#### value

```typescript
readonly value: string
```

Telefone sem máscara (DDD + número, 10 ou 11 dígitos).

**Exemplo:**
```typescript
const phone = new PhoneNumber('(11) 98765-4321')
console.log(phone.value) // "11987654321"
```

#### ddd

```typescript
readonly ddd: string
```

Código DDD (2 dígitos).

**Exemplo:**
```typescript
const phone = new PhoneNumber('(11) 98765-4321')
console.log(phone.ddd) // "11"
```

#### number

```typescript
readonly number: string
```

Número sem DDD (8 ou 9 dígitos).

**Exemplo:**
```typescript
const phone = new PhoneNumber('(11) 98765-4321')
console.log(phone.number) // "987654321"
```

### Methods

#### format()

```typescript
format(): string
```

Retorna telefone formatado com máscara.

**Returns:**
- Móvel: `(##) #####-####`
- Fixo: `(##) ####-####`

**Exemplo:**
```typescript
const mobile = new PhoneNumber('11987654321')
console.log(mobile.format()) // "(11) 98765-4321"

const landline = new PhoneNumber('1134567890')
console.log(landline.format()) // "(11) 3456-7890"
```

#### toString()

```typescript
toString(): string
```

Converte para string sem máscara.

**Returns:** Telefone sem máscara

**Exemplo:**
```typescript
const phone = new PhoneNumber('(11) 98765-4321')
console.log(phone.toString()) // "11987654321"
```

#### isMobile()

```typescript
isMobile(): boolean
```

Verifica se é telefone móvel (9 dígitos, inicia com 9).

**Returns:** `true` se móvel

**Exemplo:**
```typescript
const mobile = new PhoneNumber('(11) 98765-4321')
console.log(mobile.isMobile()) // true

const landline = new PhoneNumber('(11) 3456-7890')
console.log(landline.isMobile()) // false
```

#### isLandline()

```typescript
isLandline(): boolean
```

Verifica se é telefone fixo (8 dígitos).

**Returns:** `true` se fixo

**Exemplo:**
```typescript
const landline = new PhoneNumber('(11) 3456-7890')
console.log(landline.isLandline()) // true

const mobile = new PhoneNumber('(11) 98765-4321')
console.log(mobile.isLandline()) // false
```

#### equals()

```typescript
equals(other: PhoneNumber): boolean
```

Compara igualdade com outro PhoneNumber.

**Parâmetros:**
- `other` (PhoneNumber) - Outro telefone para comparar

**Returns:** `true` se telefones são iguais

**Exemplo:**
```typescript
const phone1 = new PhoneNumber('(11) 98765-4321')
const phone2 = new PhoneNumber('11987654321')

console.log(phone1.equals(phone2)) // true
```

### Static Methods

#### isValid()

```typescript
static isValid(value: string): boolean
```

Valida telefone sem lançar exceção.

**Parâmetros:**
- `value` (string) - Telefone a validar

**Returns:** `true` se válido, `false` caso contrário

**Exemplo:**
```typescript
PhoneNumber.isValid('(11) 98765-4321') // true
PhoneNumber.isValid('123')             // false
```

#### format()

```typescript
static format(value: string): string
```

Formata telefone sem criar instância.

**Parâmetros:**
- `value` (string) - Telefone sem máscara

**Returns:** Telefone formatado

**Throws:**
- `ValidationError` - Se telefone for inválido

**Exemplo:**
```typescript
PhoneNumber.format('11987654321') // "(11) 98765-4321"
PhoneNumber.format('1134567890')  // "(11) 3456-7890"
```

#### clean()

```typescript
static clean(value: string): string
```

Remove máscara do telefone.

**Parâmetros:**
- `value` (string) - Telefone com ou sem máscara

**Returns:** Telefone sem máscara

**Exemplo:**
```typescript
PhoneNumber.clean('(11) 98765-4321') // "11987654321"
PhoneNumber.clean('11987654321')      // "11987654321"
```

### Validações Aplicadas

1. **DDD:** 2 dígitos entre 11-99
2. **Número Móvel:** 9 dígitos, primeiro dígito = 9
3. **Número Fixo:** 8 dígitos
4. **Formato:** Aceita com ou sem máscara

---

## Errors

### ValidationError

Exceção lançada quando validação falha.

```typescript
class ValidationError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'ValidationError'
  }
}
```

**Exemplo de tratamento:**

```typescript
import { CPF, ValidationError } from '@carf/tscore/validations'

try {
  const cpf = new CPF(userInput)
  console.log('CPF válido:', cpf.format())
} catch (error) {
  if (error instanceof ValidationError) {
    console.error('Validação falhou:', error.message)
    // Mostrar mensagem para usuário
  } else {
    throw error // Re-lança erros desconhecidos
  }
}
```
