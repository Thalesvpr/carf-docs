# Conceitos @carf/tscore

Documentação dos conceitos fundamentais da biblioteca.

## Value Objects

Value Objects são objetos imutáveis comparados por valor, não identidade. @carf/tscore implementa Value Objects para validações brasileiras:

### CPF (Cadastro de Pessoa Física)

Validação completa conforme Receita Federal:

```typescript
import { CPF } from '@carf/tscore/validations'

// Constructor valida automaticamente
const cpf = new CPF('123.456.789-09')

// Métodos
cpf.format() // "123.456.789-09"
cpf.toString() // "12345678909"
cpf.toJSON() // "12345678909"

// Validação sem instanciar
CPF.validate('123.456.789-09') // true
CPF.validate('000.000.000-00') // false (sequência rejeitada)
CPF.normalize('123.456.789-09') // "12345678909"
```

**Algoritmo mod 11:**
1. Normaliza removendo pontuação
2. Rejeita sequências conhecidas (000.000.000-00 até 999.999.999-99)
3. Calcula primeiro dígito verificador com pesos 10,9,8...2
4. Calcula segundo dígito verificador com pesos 11,10,9...2
5. Compara com dígitos fornecidos

Ver: `CENTRAL/BUSINESS-RULES/VALIDATION-RULES/cpf-validation.md`

### CNPJ (Cadastro Nacional de Pessoa Jurídica)

Validação de empresas:

```typescript
import { CNPJ } from '@carf/tscore/validations'

const cnpj = new CNPJ('11.444.777/0001-61')

cnpj.format() // "11.444.777/0001-61"
cnpj.toString() // "11444777000161"

CNPJ.validate('11.444.777/0001-61') // true
```

**Algoritmo:**
- 14 dígitos numéricos
- Pesos [5,4,3,2,9,8,7,6,5,4,3,2] para 12º dígito
- Pesos [6,5,4,3,2,9,8,7,6,5,4,3,2] para 13º dígito
- Mod 11 com resto < 2 → dígito 0, senão 11 - resto

### Email

Validação simplificada RFC 5322:

```typescript
import { Email } from '@carf/tscore/validations'

const email = new Email('user@example.com')

email.toString() // "user@example.com"

Email.validate('user@example.com') // true
Email.validate('invalid@') // false
Email.validate('user@domain') // false (precisa TLD)
```

**Regras:**
- Local part: alfanuméricos + `._%+-`
- Deve conter `@`
- Domain: alfanuméricos + `.` e `-`
- Domain deve ter pelo menos um `.` (TLD requerido)

### Phone

Formato brasileiro com DDD:

```typescript
import { Phone } from '@carf/tscore/validations'

const phone = new Phone('(11) 98765-4321')

phone.format() // "(11) 98765-4321"
phone.toString() // "11987654321"

Phone.validate('(11) 98765-4321') // true (celular 9 dígitos)
Phone.validate('(11) 3456-7890') // true (fixo 8 dígitos)
Phone.validate('(11) 1234-5678') // false (começa com 1)
```

**Regras:**
- DDD: 11-99
- Celular: 9 dígitos começando com 9
- Fixo: 8 dígitos começando com 2-5
- Formato: `(XX) XXXXX-XXXX` ou `(XX) XXXX-XXXX`

## Domain Types

Types TypeScript representando entities do domínio CARF:

### Unit (Unidade Habitacional)

```typescript
import type { Unit } from '@carf/tscore/types'
import { UnitStatus } from '@carf/tscore/types'

const unit: Unit = {
 id: string
 code: string
 status: UnitStatus
 street: string
 number?: string | null
 city: string
 state: string
 geometry?: GeoJSON.Polygon | null
 area?: number | null
 communityId: string
 createdAt: Date
 updatedAt: Date
 version: number
}
```

### Holder (Titular)

```typescript
import type { Holder } from '@carf/tscore/types'
import { EntityType } from '@carf/tscore/types'

const holder: Holder = {
 id: string
 type: EntityType
 name: string
 cpf?: string | null
 cnpj?: string | null
 email?: string | null
 phone?: string | null
 // ... outros campos
}
```

### Community (Comunidade)

```typescript
import type { Community } from '@carf/tscore/types'
import { CommunityType } from '@carf/tscore/types'

const community: Community = {
 id: string
 name: string
 type: CommunityType
 boundary?: GeoJSON.Polygon | null
 tenantId: string
 // ... outros campos
}
```

Ver todas 36+ entities em `src/types/entities/`

## Enums

### UnitStatus

Estados do workflow de aprovação:

```typescript
import { UnitStatus } from '@carf/tscore/types'

enum UnitStatus {
 DRAFT = 'DRAFT' // Rascunho
 PENDING = 'PENDING' // Aguardando análise
 IN_REVIEW = 'IN_REVIEW' // Em análise
 APPROVED = 'APPROVED' // Aprovada
 REJECTED = 'REJECTED' // Rejeitada
 REQUIRES_CHANGES = 'REQUIRES_CHANGES' // Requer alterações
}

// Transições válidas
DRAFT → PENDING
PENDING → IN_REVIEW → APPROVED
 ↓
 REJECTED ou REQUIRES_CHANGES
```

### Role

Hierarquia de permissões:

```typescript
import { Role, hasRolePermission } from '@carf/tscore/types'

enum Role {
 SUPER_ADMIN = 'SUPER_ADMIN' // Nível 5
 ADMIN = 'ADMIN' // Nível 4
 MANAGER = 'MANAGER' // Nível 3
 ANALYST = 'ANALYST' // Nível 2
 FIELD_AGENT = 'FIELD_AGENT' // Nível 1
}

// Verificação hierárquica
hasRolePermission(Role.MANAGER, Role.ANALYST) // true
hasRolePermission(Role.ANALYST, Role.MANAGER) // false
```

### LegitimationStatus

Estados do processo REURB Lei 13.465/2017:

```typescript
import { LegitimationStatus } from '@carf/tscore/types'

enum LegitimationStatus {
 DRAFT = 'DRAFT'
 SUBMITTED = 'SUBMITTED'
 UNDER_REVIEW = 'UNDER_REVIEW'
 AWAITING_DOCUMENTATION = 'AWAITING_DOCUMENTATION'
 PUBLIC_NOTICE = 'PUBLIC_NOTICE'
 CONTESTED = 'CONTESTED'
 ANALYZING_CONTESTATION = 'ANALYZING_CONTESTATION'
 APPROVED = 'APPROVED'
 REJECTED = 'REJECTED'
 CERTIFICATE_ISSUED = 'CERTIFICATE_ISSUED'
 ARCHIVED = 'ARCHIVED'
}
```

## Autenticação

### KeycloakClient

Cliente OAuth2/OIDC para Keycloak:

```typescript
import { KeycloakClient } from '@carf/tscore/auth'

const client = new KeycloakClient({
 url: 'http://localhost:8080',
 realm: 'carf',
 clientId: 'geoweb'
})

// Inicializar (carrega tokens de localStorage)
await client.init()

// Login (redireciona para Keycloak)
client.login()

// Obter token (refresh automático se expirado)
const token = await client.getToken()

// Verificar role
client.hasRole(Role.ADMIN)

// Verificar permissão hierárquica
client.hasRolePermission(Role.ANALYST)

// Logout
await client.logout()
```

**Funcionalidades:**
- Authorization Code + PKCE flow
- Token refresh automático (60s antes expiry)
- Role extraction de JWT claims
- Storage em localStorage
- CSRF protection via state parameter

### React Hooks

```typescript
import { useAuth } from '@carf/tscore/auth/react'
import { Role } from '@carf/tscore/types'

function Component() {
 const {
 user, // User | null
 isLoading, // boolean
 isAuthenticated, // boolean
 login, // () => void
 logout, // () => Promise<void>
 hasRole, // (role: Role) => boolean
 hasPermission, // (role: Role) => boolean
 getToken // () => Promise<string>
 } = useAuth()

 if (isLoading) return <Loading />
 if (!isAuthenticated) return <Login />

 return (
 <div>
 <p>Olá, {user.name}</p>
 {hasRole(Role.ADMIN) && <AdminPanel />}
 </div>
 )
}
```

### Vue Composables

```typescript
<script setup lang="ts">
import { useAuth } from '@carf/tscore/auth/vue'
import { Role } from '@carf/tscore/types'

const {
 user, // Ref<User | null>
 isLoading, // Ref<boolean>
 isAuthenticated, // Ref<boolean>
 login, // () => void
 logout, // () => Promise<void>
 hasRole, // (role: Role) => boolean
 hasPermission, // (role: Role) => boolean
 getToken // () => Promise<string>
} = useAuth()
</script>
```

## DTOs (Data Transfer Objects)

Types para comunicação API:

```typescript
import type { CreateUnitDto, UpdateUnitDto } from '@carf/tscore/types'

// POST /api/units
const createDto: CreateUnitDto = {
 code: 'UN-001',
 street: 'Rua Example',
 city: 'São Paulo',
 state: 'SP',
 communityId: 'uuid'
 // Campos obrigatórios apenas
}

// PATCH /api/units/:id
const updateDto: UpdateUnitDto = {
 street?: 'Nova Rua',
 number?: '123'
 // Todos campos opcionais
}
```

**Variants:**
- `Create*Dto` - Campos requeridos para POST
- `Update*Dto` - Campos opcionais para PATCH
- `*WithRelations` - Entity + related entities
- `*WithStats` - Entity + computed statistics

## Ver também

- [Value Objects Detalhados](./01-value-objects.md) - Implementações completas de CPF, CNPJ, Email, Phone
- [Autenticação Keycloak](./02-authentication.md) - OAuth2/OIDC integration
- [TypeScript Types](./03-typescript-types.md) - Entities, Enums, DTOs do domínio CARF

---

**Última atualização:** 2026-01-09

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (3 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-value-objects](./01-value-objects.md) | Value Objects - Objetos de Valor |
| [02-authentication](./02-authentication.md) | Authentication - Autenticação com Keycloak |
| [03-typescript-types](./03-typescript-types.md) | TypeScript Types - Tipos Compartilhados |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Incompleto
Descrição: Muitas listas com bullets (24) antes do rodapé - considerar converter para parágrafo denso; Contém code blocks - considerar converter para prosa.
