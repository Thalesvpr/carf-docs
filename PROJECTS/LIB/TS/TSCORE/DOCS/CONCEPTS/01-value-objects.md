---
status: review
updated: 2026-01-15
---

# Value Objects - Objetos de Valor

## Visão Geral

Value Objects são objetos imutáveis representando conceitos do domínio definidos apenas por atributos sem identidade própria. @carf/tscore implementa Value Objects garantindo validação consistente de dados brasileiros em todos projetos CARF consumidos por geoapi-client para tipagem requests/responses HTTP, ui-components para validação em componentes React, e aplicações finais GEOWEB, REURBCAD e ADMIN.

## Conceito de Value Object

### Definição

Um Value Object é um objeto que:
1. **Não possui identidade** - Dois VOs com mesmos valores são considerados iguais
2. **É imutável** - Uma vez criado, seus valores não podem ser alterados
3. **Encapsula validação** - A criação falha se os valores forem inválidos
4. **Expressa conceito de domínio** - Representa algo do mundo real (CPF, Email, Coordenadas)

### Benefícios

✅ **Type Safety** - TypeScript garante tipos corretos em compile-time
✅ **Validação Centralizada** - Regras em um único lugar
✅ **Reutilização** - Mesmo código em GEOWEB, REURBCAD, ADMIN
✅ **Imutabilidade** - Previne bugs de mutação acidental
✅ **Semântica** - `new CPF('12345678909')` é mais expressivo que `string`

## Relação com CENTRAL/DOMAIN-MODEL

Os Value Objects implementados nesta biblioteca correspondem diretamente aos conceitos documentados em CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/ fornecendo índice completo de 25 Value Objects do domínio.

### Mapeamento Implementado

| Value Object @carf/tscore | Documentação CENTRAL | Status |
|---|---|---|
| `CPF` | | ✅ Implementado |
| `CNPJ` | ✅ Implementado |
| `Email` | ✅ Implementado |
| `PhoneNumber` | ✅ Implementado |
| `GeoPoint` | 🚧 Planejado |
| `GeoPolygon` | 🚧 Planejado |
| `Address` | 🚧 Planejado |

## Value Objects Implementados

### 1. CPF (Cadastro de Pessoa Física)

Valida CPF brasileiro com algoritmo de dígitos verificadores conforme Receita Federal.

#### Documentação de Domínio

📖 **** - Especificação completa do conceito CPF

#### Relacionamentos de Domínio

Este Value Object é usado nas seguintes entidades:
- **** - CPF obrigatório para identificação única nacional
- ****Account**** - CPF opcional para vinculação de usuário
- ****Surveyor**** - CPF obrigatório para topógrafo profissional

#### Regras de Validação

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

### 2. CNPJ (Cadastro Nacional de Pessoa Jurídica)

Valida CNPJ brasileiro com algoritmo de dígitos verificadores conforme Receita Federal.

#### Documentação de Domínio

📖 ****CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/02-cnpj.md**** - Especificação completa do conceito CNPJ

#### Relacionamentos de Domínio

Este Value Object é usado nas seguintes entidades:
- **** - Quando titular é pessoa jurídica
- **** - CNPJ obrigatório para instituição cliente

#### Regras de Validação

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

Valida endereços de email conforme RFC 5322 com sanitização básica.

#### Documentação de Domínio

📖 ****CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/04-email.md**** - Especificação completa do conceito Email

#### Relacionamentos de Domínio

Este Value Object é usado nas seguintes entidades:
- **** - Email para contato e notificações
- ****Account**** - Email obrigatório para autenticação

#### Regras de Validação

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

Valida telefones brasileiros com DDD e formato móvel/fixo.

#### Documentação de Domínio

📖 ****CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/05-phone-number.md**** - Especificação completa do conceito PhoneNumber

#### Relacionamentos de Domínio

Este Value Object é usado nas seguintes entidades:
- **** - Telefone para contato
- ****Account**** - Telefone opcional

#### Regras de Validação

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

## Value Objects Geograficos (Especificacao Completa)

### GeoPoint (Ponto Geografico)

Representa um ponto geografico com coordenadas latitude/longitude em sistema WGS84 (EPSG:4326).

#### Documentacao de Dominio

📖 **CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/geo-point.md** - Especificacao do conceito

#### Relacionamentos de Dominio

- **Unit** - Ponto de referencia da unidade (centroide)
- **SurveyPoint** - Vertices do levantamento topografico
- **Community** - Ponto central da comunidade

#### Regras de Validacao

1. **Latitude:** -90 a 90 graus
2. **Longitude:** -180 a 180 graus
3. **Precisao:** Minimo 6 casas decimais recomendado (~0.1m)
4. **Sistema:** WGS84 (EPSG:4326) assumido

#### Interface

```typescript
interface GeoPoint {
  readonly latitude: number   // -90 a 90
  readonly longitude: number  // -180 a 180

  // Conversoes
  toWKT(): string             // "POINT(-46.6333 -23.5505)"
  toGeoJSON(): GeoJSONPoint   // { type: "Point", coordinates: [lng, lat] }
  toArray(): [number, number] // [longitude, latitude]

  // Operacoes
  distanceTo(other: GeoPoint): number  // Distancia em metros (Haversine)
  equals(other: GeoPoint): boolean

  // Factory methods
  static fromWKT(wkt: string): GeoPoint
  static fromGeoJSON(geojson: GeoJSONPoint): GeoPoint
  static fromArray(coords: [number, number]): GeoPoint
}

interface GeoJSONPoint {
  type: 'Point'
  coordinates: [number, number]  // [longitude, latitude]
}
```

#### Usage

```typescript
import { GeoPoint } from '@carf/tscore/geo'

// Criacao
const point = new GeoPoint(-23.5505, -46.6333)  // lat, lng
const fromWKT = GeoPoint.fromWKT('POINT(-46.6333 -23.5505)')
const fromGeoJSON = GeoPoint.fromGeoJSON({
  type: 'Point',
  coordinates: [-46.6333, -23.5505]
})

// Propriedades
point.latitude   // -23.5505
point.longitude  // -46.6333

// Conversoes
point.toWKT()      // "POINT(-46.6333 -23.5505)"
point.toGeoJSON()  // { type: "Point", coordinates: [-46.6333, -23.5505] }
point.toArray()    // [-46.6333, -23.5505]

// Operacoes
const other = new GeoPoint(-23.5600, -46.6400)
point.distanceTo(other)  // 1234.56 (metros)

// Validacao
GeoPoint.isValid(-23.5505, -46.6333)  // true
GeoPoint.isValid(91, 0)               // false (latitude invalida)
```

#### Usage em Entidades

```typescript
import type { Unit } from '@carf/tscore/types'
import { GeoPoint } from '@carf/tscore/geo'

// Unit com ponto de referencia
const unit: Unit = {
  id: '...',
  code: 'UN-001',
  referencePoint: new GeoPoint(-23.5505, -46.6333).toGeoJSON(),
  // ...
}

// Mapear para Leaflet
import L from 'leaflet'
const marker = L.marker([point.latitude, point.longitude])
```

### GeoPolygon (Poligono Geografico)

Representa um poligono geografico fechado com coordenadas em WGS84 para delimitacao de unidades habitacionais e comunidades.

#### Documentacao de Dominio

📖 **CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/geo-polygon.md** - Especificacao do conceito

#### Relacionamentos de Dominio

- **Unit** - Perimetro da unidade habitacional
- **Community** - Perimetro da comunidade
- **Block** - Delimitacao de quadra

#### Regras de Validacao

1. **Fechamento:** Primeiro e ultimo ponto devem ser iguais
2. **Minimo de Pontos:** 4 pontos (triangulo fechado)
3. **Sentido:** Counter-clockwise (CCW) para exterior
4. **Autointersecao:** Poligono nao pode se cruzar
5. **Holes:** Suporta buracos (interior em sentido horario)

#### Interface

```typescript
interface GeoPolygon {
  readonly coordinates: GeoPoint[]
  readonly holes?: GeoPoint[][]

  // Propriedades
  area(): number           // Area em m² (WGS84 projection)
  perimeter(): number      // Perimetro em metros
  centroid(): GeoPoint     // Ponto central
  bounds(): GeoBounds      // Bounding box

  // Conversoes
  toWKT(): string
  toGeoJSON(): GeoJSONPolygon

  // Validacao
  isValid(): boolean
  contains(point: GeoPoint): boolean
  intersects(other: GeoPolygon): boolean

  // Factory methods
  static fromWKT(wkt: string): GeoPolygon
  static fromGeoJSON(geojson: GeoJSONPolygon): GeoPolygon
  static fromCoordinates(coords: Array<[number, number]>): GeoPolygon
}

interface GeoJSONPolygon {
  type: 'Polygon'
  coordinates: Array<Array<[number, number]>>  // [exterior, ...holes]
}

interface GeoBounds {
  north: number  // max latitude
  south: number  // min latitude
  east: number   // max longitude
  west: number   // min longitude
}
```

#### Usage

```typescript
import { GeoPolygon, GeoPoint } from '@carf/tscore/geo'

// Criacao a partir de WKT (comum em PostGIS)
const polygon = GeoPolygon.fromWKT(
  'POLYGON((-46.634 -23.550, -46.633 -23.550, -46.633 -23.551, -46.634 -23.551, -46.634 -23.550))'
)

// Criacao a partir de coordenadas
const coords: Array<[number, number]> = [
  [-46.634, -23.550],
  [-46.633, -23.550],
  [-46.633, -23.551],
  [-46.634, -23.551],
  [-46.634, -23.550]  // Fechamento
]
const fromCoords = GeoPolygon.fromCoordinates(coords)

// Propriedades geometricas
polygon.area()       // 250.5 (m²)
polygon.perimeter()  // 64.2 (metros)
polygon.centroid()   // GeoPoint do centro

// Bounding box
const bounds = polygon.bounds()
// { north: -23.550, south: -23.551, east: -46.633, west: -46.634 }

// Operacoes espaciais
const point = new GeoPoint(-23.5505, -46.6335)
polygon.contains(point)  // true/false

// Conversoes
polygon.toWKT()      // "POLYGON((...))
polygon.toGeoJSON()  // { type: "Polygon", coordinates: [...] }

// Validacao
GeoPolygon.isValid(coords)       // true/false
polygon.isValid()                // true se geometria valida
```

#### Usage em Unidades

```typescript
import type { Unit } from '@carf/tscore/types'
import { GeoPolygon } from '@carf/tscore/geo'

// Criar unidade com geometria
const polygon = GeoPolygon.fromWKT(wktFromGIS)

const unit: Unit = {
  id: '...',
  code: 'UN-001',
  geometry: polygon.toWKT(),         // Armazenar como WKT
  area: polygon.area(),              // Calcular area automaticamente
  // ...
}

// Exibir em Leaflet
import L from 'leaflet'
const geoJsonLayer = L.geoJSON(polygon.toGeoJSON())
geoJsonLayer.addTo(map)
```

### Address (Endereco Brasileiro)

Representa endereco completo seguindo padroes brasileiros.

#### Interface

```typescript
interface Address {
  street: string           // Logradouro (obrigatorio)
  number?: string          // Numero
  complement?: string      // Complemento
  neighborhood?: string    // Bairro
  city: string             // Municipio (obrigatorio)
  state: string            // UF 2 letras (obrigatorio)
  zipCode?: string         // CEP 8 digitos

  // Formatacao
  format(): string         // "Rua X, 123 - Bairro, Cidade/UF"
  formatShort(): string    // "Rua X, 123"

  // Validacao
  static isValidZipCode(cep: string): boolean
  static isValidState(uf: string): boolean
}
```

#### Usage

```typescript
import { Address } from '@carf/tscore/validations'

const address = new Address({
  street: 'Rua das Flores',
  number: '123',
  complement: 'Apto 45',
  neighborhood: 'Centro',
  city: 'Sao Paulo',
  state: 'SP',
  zipCode: '01310100'
})

address.format()      // "Rua das Flores, 123, Apto 45 - Centro, Sao Paulo/SP"
address.formatShort() // "Rua das Flores, 123"

// Validacoes
Address.isValidZipCode('01310-100')  // true
Address.isValidState('SP')           // true
Address.isValidState('XX')           // false
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
