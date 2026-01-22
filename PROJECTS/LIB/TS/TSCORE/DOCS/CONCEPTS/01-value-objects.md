---
type: leaf
title: "Value Objects - @carf/tscore"
status: review
updated: 2026-01-21
source: "interno"
---

# Value Objects - Objetos de Valor

## Visao Geral

Value Objects sao objetos imutaveis representando conceitos do dominio definidos apenas por atributos sem identidade propria. @carf/tscore implementa Value Objects garantindo validacao consistente de dados brasileiros em todos projetos CARF.

## Conceito de Value Object

### Definicao

Um Value Object e um objeto que:
1. **Nao possui identidade** - Dois VOs com mesmos valores sao considerados iguais
2. **E imutavel** - Uma vez criado, seus valores nao podem ser alterados
3. **Encapsula validacao** - A criacao falha se os valores forem invalidos
4. **Expressa conceito de dominio** - Representa algo do mundo real (CPF, Email, Coordenadas)

### Beneficios

- **Type Safety** - TypeScript garante tipos corretos em compile-time
- **Validacao Centralizada** - Regras em um unico lugar
- **Reutilizacao** - Mesmo codigo em GEOWEB, REURBCAD, ADMIN
- **Imutabilidade** - Previne bugs de mutacao acidental
- **Semantica** - `new CPF('12345678909')` e mais expressivo que `string`

## Value Objects Disponiveis

| Value Object | Descricao | Status |
|:-------------|:----------|:-------|
| `CPF` | Cadastro de Pessoa Fisica (11 digitos) | Especificado |
| `CNPJ` | Cadastro Nacional Pessoa Juridica (14 digitos) | Especificado |
| `Email` | Endereco de email | Especificado |
| `PhoneNumber` | Telefone brasileiro (DDD + numero) | Especificado |
| `GeoPoint` | Ponto geografico (lat, lng) | Planejado |
| `GeoPolygon` | Poligono geografico | Planejado |
| `Address` | Endereco completo | Planejado |

## Value Objects Especificados

### 1. CPF (Cadastro de Pessoa Fisica)

Valida CPF brasileiro com algoritmo de digitos verificadores conforme Receita Federal.

#### Uso nas Entidades

- **Holder** - CPF obrigatorio para identificacao do posseiro
- **Account** - CPF opcional para vinculacao de usuario
- **Surveyor** - CPF obrigatorio para topografo profissional

#### Regras de Validacao

1. **Formato:** 11 dígitos numéricos (aceita máscaras `###.###.###-##`)
2. **Dígitos Verificadores:** Valida mod-11 (d1 e d2)
3. **CPFs Inválidos Conhecidos:** Rejeita `000.000.000-00`, `111.111.111-11`, etc.
4. **Unicidade:** Backend garante unicidade nacional (índice unique)

#### Implementação

```typescript
import { CPF } from '@carf/tscore/validations'

// Criação com validação automática
const cpf = new CPF('123.456.789-09') // Lança erro se inválido

// Métodos disponíveis
cpf.value // "12345678909" (sempre sem máscara)
cpf.format() // "123.456.789-09" (com máscara)
cpf.toString() // "12345678909" (sem máscara)
cpf.equals(other) // Compara igualdade entre CPFs

// Validação estática
CPF.isValid('123.456.789-09') // true/false
CPF.format('12345678909') // "123.456.789-09"
CPF.clean('123.456.789-09') // "12345678909"
```

#### Exemplos de Uso em Entidades

```typescript
import { CPF } from '@carf/tscore/validations'
import type { Holder } from '@carf/tscore/types'

// Criando Holder com CPF validado
const holder: Holder = {
 id: crypto.randomUUID(),
 cpf: new CPF('123.456.789-09').value, // Armazena sem máscara
 name: 'João da Silva',
 email: 'joao@example.com',
 // ... outros campos
}

// Validação em formulário React
function HolderForm() {
 const handleSubmit = (data: any) => {
 try {
 const cpf = new CPF(data.cpf) // Valida antes de enviar
 // Enviar para API...
 } catch (error) {
 alert('CPF inválido!')
 }
 }
}
```

#### Casos de Teste

```typescript
// Válidos
new CPF('123.456.789-09') // ✅
new CPF('12345678909') // ✅

// Inválidos
new CPF('000.000.000-00') // ❌ CPF conhecido inválido
new CPF('123.456.789-00') // ❌ Dígito verificador errado
new CPF('abc') // ❌ Formato inválido
```

### 2. CNPJ (Cadastro Nacional de Pessoa Juridica)

Valida CNPJ brasileiro com algoritmo de digitos verificadores conforme Receita Federal.

#### Uso nas Entidades

- **Holder** - CNPJ quando titular e pessoa juridica
- **Client** - CNPJ obrigatorio para instituicao cliente

#### Regras de Validacao

1. **Formato:** 14 dígitos numéricos (aceita máscaras `##.###.###/####-##`)
2. **Dígitos Verificadores:** Valida mod-11 (d1 e d2)
3. **CNPJs Inválidos Conhecidos:** Rejeita `00.000.000/0000-00`, etc.

#### Implementação

```typescript
import { CNPJ } from '@carf/tscore/validations'

// Criação com validação automática
const cnpj = new CNPJ('11.444.777/0001-61')

// Métodos disponíveis
cnpj.value // "11444777000161" (sem máscara)
cnpj.format() // "11.444.777/0001-61" (com máscara)
cnpj.toString() // "11444777000161"
cnpj.equals(other) // Compara igualdade

// Validação estática
CNPJ.isValid('11.444.777/0001-61')
CNPJ.format('11444777000161')
CNPJ.clean('11.444.777/0001-61')
```

### 3. Email

Valida enderecos de email conforme RFC 5322 com sanitizacao basica.

#### Uso nas Entidades

- **Holder** - Email para contato e notificacoes
- **Account** - Email obrigatorio para autenticacao

#### Regras de Validacao

1. **Formato RFC 5322:** `local-part@domain`
2. **Normalização:** Converte para lowercase
3. **Sanitização:** Remove espaços e caracteres inválidos
4. **Domínio:** Valida presença de TLD válido

#### Implementação

```typescript
import { Email } from '@carf/tscore/validations'

// Criação com validação automática
const email = new Email('user@example.com')

// Métodos disponíveis
email.value // "user@example.com" (normalizado lowercase)
email.local // "user" (parte local)
email.domain // "example.com"
email.toString() // "user@example.com"
email.equals(other) // Compara igualdade

// Validação estática
Email.isValid('user@example.com') // true/false
Email.normalize('USER@EXAMPLE.COM') // "user@example.com"
```

#### Exemplos de Uso

```typescript
import { Email } from '@carf/tscore/validations'
import type { Holder } from '@carf/tscore/types'

// Criando Holder com Email validado
const holder: Holder = {
 id: crypto.randomUUID(),
 cpf: '12345678909',
 name: 'Maria Santos',
 email: new Email('maria@example.com').value,
 // ... outros campos
}

// Hook React para validação
import { useState } from 'react'

function useEmailValidation() {
 const [error, setError] = useState<string | null>(null)

 const validate = (value: string) => {
 try {
 new Email(value)
 setError(null)
 return true
 } catch (err) {
 setError('Email inválido')
 return false
 }
 }

 return { validate, error }
}
```

### 4. PhoneNumber (Telefone Brasileiro)

Valida telefones brasileiros com DDD e formato movel/fixo.

#### Uso nas Entidades

- **Holder** - Telefone para contato
- **Account** - Telefone opcional

#### Regras de Validacao

1. **DDD:** 2 dígitos (11-99)
2. **Número Móvel:** 9 dígitos iniciando com 9 (ex: 98765-4321)
3. **Número Fixo:** 8 dígitos (ex: 3456-7890)
4. **Formato:** Aceita `(##) #####-####` ou `(##) ####-####`

#### Implementação

```typescript
import { PhoneNumber } from '@carf/tscore/validations'

// Criação com validação automática
const phone = new PhoneNumber('(11) 98765-4321')

// Métodos disponíveis
phone.value // "11987654321" (sem máscara)
phone.ddd // "11"
phone.number // "987654321"
phone.format() // "(11) 98765-4321"
phone.toString() // "11987654321"
phone.isMobile() // true
phone.isLandline() // false

// Validação estática
PhoneNumber.isValid('(11) 98765-4321')
PhoneNumber.format('11987654321')
PhoneNumber.clean('(11) 98765-4321')
```

## Padrões de Implementação

### Estrutura Base de Value Object

```typescript
// src/validations/value-object.base.ts
export abstract class ValueObject<T> {
 protected readonly _value: T

 constructor(value: T) {
 this.validate(value)
 this._value = value
 }

 protected abstract validate(value: T): void

 public get value(): T {
 return this._value
 }

 public equals(other: ValueObject<T>): boolean {
 return this._value === other._value
 }

 public toString(): string {
 return String(this._value)
 }
}
```

### Padrão de Uso

```typescript
// 1. Importar Value Object
import { CPF, Email, PhoneNumber } from '@carf/tscore/validations'

// 2. Criar instância (lança erro se inválido)
try {
 const cpf = new CPF(userInput)
 const email = new Email(userInput)
 const phone = new PhoneNumber(userInput)
} catch (error) {
 console.error('Validação falhou:', error.message)
}

// 3. Usar em tipos
import type { Holder } from '@carf/tscore/types'

const holder: Holder = {
 cpf: new CPF('123.456.789-09').value,
 email: new Email('user@example.com').value,
 phone: new PhoneNumber('(11) 98765-4321').value,
 // ...
}
```

## Testes

Todos os Value Objects têm cobertura de testes >= 95%:

```bash
cd PROJECTS/LIB/TS/TSCORE/SRC-CODE
bun test src/validations/
```

Ver especificações de teste:
- `src/validations/__tests__/cpf.spec.ts`
- `src/validations/__tests__/cnpj.spec.ts`
- `src/validations/__tests__/email.spec.ts`
- `src/validations/__tests__/phone.spec.ts`
