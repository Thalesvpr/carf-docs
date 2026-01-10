# Contributing to @carf/geoapi-client

## Guia de Contribuição

Contribuir para @carf/geoapi-client requer fork do repositório, criar branch com nome descritivo (`feature/add-communities-api` ou `fix/retry-logic-bug`), implementar mudanças seguindo padrões existentes (cada endpoint em arquivo separado em `src/api/`, types em `src/types/`, testes em `src/__tests__/`), adicionar testes com coverage >80% usando Vitest mockando Axios com `axios-mock-adapter`, atualizar CHANGELOG.md seguindo Keep a Changelog format, rodar linters com `bun run lint` e `bun run type-check` garantindo zero erros, fazer commit seguindo Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`), push branch e abrir Pull Request com descrição clara do problema resolvido e solução implementada, aguardar code review e ajustar conforme feedback antes de merge.

## Setup para Contribuir

### 1. Fork e Clone

```bash
# Fork no GitHub
# https://github.com/Thalesvpr/carf-geoapi-client/fork

# Clonar seu fork
git clone https://github.com/SEU-USERNAME/carf-geoapi-client.git
cd carf-geoapi-client

# Adicionar upstream
git remote add upstream https://github.com/Thalesvpr/carf-geoapi-client.git
```

### 2. Instalar Dependências

```bash
bun install
```

### 3. Criar Branch

```bash
# Feature
git checkout -b feature/add-communities-endpoint

# Bug fix
git checkout -b fix/retry-logic-timeout

# Docs
git checkout -b docs/improve-readme

# Refactor
git checkout -b refactor/simplify-error-handling
```

## Estrutura do Projeto

```
src/
├── api/                    # Endpoints organizados por recurso
│   ├── units.ts           # Unit endpoints
│   ├── holders.ts         # Holder endpoints
│   ├── communities.ts     # Community endpoints
│   └── index.ts           # Exports
├── types/                  # TypeScript types
│   ├── unit.ts
│   ├── holder.ts
│   └── index.ts
├── errors/                 # Error classes
│   └── ApiError.ts
├── interceptors/           # Axios interceptors
│   ├── auth.ts
│   ├── retry.ts
│   └── error.ts
├── client.ts              # GeoApiClient class principal
└── index.ts               # Main export

__tests__/                  # Testes
├── api/
│   ├── units.test.ts
│   └── holders.test.ts
└── client.test.ts
```

## Adicionando Novo Endpoint

### 1. Criar Arquivo de Endpoint

```typescript
// src/api/communities.ts
import { AxiosInstance } from 'axios'
import { Community, CreateCommunityDto, UpdateCommunityDto } from '../types'

export function createCommunitiesApi(client: AxiosInstance) {
  return {
    /**
     * Lista todas as comunidades
     */
    async list(): Promise<Community[]> {
      const { data } = await client.get<Community[]>('/api/communities')
      return data
    },

    /**
     * Busca comunidade por ID
     */
    async getById(id: string): Promise<Community> {
      const { data } = await client.get<Community>(`/api/communities/${id}`)
      return data
    },

    /**
     * Cria nova comunidade
     */
    async create(dto: CreateCommunityDto): Promise<Community> {
      const { data } = await client.post<Community>('/api/communities', dto)
      return data
    },

    /**
     * Atualiza comunidade existente
     */
    async update(id: string, dto: UpdateCommunityDto): Promise<Community> {
      const { data } = await client.put<Community>(
        `/api/communities/${id}`,
        dto
      )
      return data
    },

    /**
     * Deleta comunidade
     */
    async delete(id: string): Promise<void> {
      await client.delete(`/api/communities/${id}`)
    },
  }
}
```

### 2. Adicionar Types

```typescript
// src/types/community.ts
export interface Community {
  id: string
  name: string
  status: 'ACTIVE' | 'INACTIVE'
  municipalityId: string
  coordinates: {
    lat: number
    lng: number
  }
  createdAt: string
  updatedAt: string
}

export interface CreateCommunityDto {
  name: string
  municipalityId: string
  coordinates: {
    lat: number
    lng: number
  }
}

export interface UpdateCommunityDto {
  name?: string
  status?: 'ACTIVE' | 'INACTIVE'
  coordinates?: {
    lat: number
    lng: number
  }
}
```

### 3. Exportar

```typescript
// src/api/index.ts
export { createCommunitiesApi } from './communities'

// src/types/index.ts
export * from './community'
```

### 4. Integrar no Client

```typescript
// src/client.ts
import { createCommunitiesApi } from './api'

export class GeoApiClient {
  public readonly communities: ReturnType<typeof createCommunitiesApi>

  constructor(config: GeoApiClientConfig) {
    // ...
    this.communities = createCommunitiesApi(this.axiosInstance)
  }
}
```

### 5. Adicionar Testes

```typescript
// __tests__/api/communities.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import MockAdapter from 'axios-mock-adapter'
import { GeoApiClient } from '../../src/client'

describe('CommunitiesApi', () => {
  let client: GeoApiClient
  let mock: MockAdapter

  beforeEach(() => {
    client = new GeoApiClient({
      baseURL: 'http://localhost:7001',
    })
    mock = new MockAdapter(client['axiosInstance'])
  })

  it('list() should return communities', async () => {
    const mockCommunities = [
      { id: '1', name: 'Community A', status: 'ACTIVE' },
      { id: '2', name: 'Community B', status: 'INACTIVE' },
    ]

    mock.onGet('/api/communities').reply(200, mockCommunities)

    const communities = await client.communities.list()

    expect(communities).toEqual(mockCommunities)
    expect(mock.history.get.length).toBe(1)
  })

  it('getById() should return community', async () => {
    const mockCommunity = {
      id: '1',
      name: 'Community A',
      status: 'ACTIVE',
    }

    mock.onGet('/api/communities/1').reply(200, mockCommunity)

    const community = await client.communities.getById('1')

    expect(community).toEqual(mockCommunity)
  })

  it('create() should create community', async () => {
    const dto = {
      name: 'New Community',
      municipalityId: 'mun-1',
      coordinates: { lat: -23.5505, lng: -46.6333 },
    }

    const mockResponse = { id: '3', ...dto, status: 'ACTIVE' }

    mock.onPost('/api/communities').reply(201, mockResponse)

    const community = await client.communities.create(dto)

    expect(community).toEqual(mockResponse)
    expect(mock.history.post[0].data).toBe(JSON.stringify(dto))
  })
})
```

### 6. Atualizar CHANGELOG

```markdown
# Changelog

## [Unreleased]

### Added
- Communities API endpoints (list, getById, create, update, delete)
- Community type definitions
```

### 7. Rodar Validações

```bash
# Testes
bun test

# Coverage
bun test --coverage

# Lint
bun run lint

# Type check
bun run type-check
```

## Conventional Commits

Seguir o padrão [Conventional Commits](https://www.conventionalcommits.org/):

### Tipos

- **feat:** Nova feature
- **fix:** Bug fix
- **docs:** Mudanças em documentação
- **style:** Formatação (não afeta código)
- **refactor:** Refatoração (não adiciona feature nem fix bug)
- **test:** Adicionar/modificar testes
- **chore:** Mudanças de build, CI, dependencies

### Exemplos

```bash
# Feature
git commit -m "feat: add communities API endpoints"

# Bug fix
git commit -m "fix: retry logic not working for network errors"

# Docs
git commit -m "docs: improve authentication flow documentation"

# Breaking change
git commit -m "feat!: change error response format

BREAKING CHANGE: ApiError.details is now Record<string, any> instead of string"

# Multiple changes
git commit -m "feat: add communities API

- Add list, getById, create, update, delete endpoints
- Add Community type definitions
- Add comprehensive tests with >80% coverage"
```

## Code Style

### TypeScript

```typescript
// ✅ CORRETO
export interface Community {
  id: string
  name: string
}

// ❌ INCORRETO
export interface community {  // PascalCase para types
  ID: string  // camelCase para fields
  NAME: string
}
```

### Async/Await

```typescript
// ✅ CORRETO - async/await
async function loadData() {
  try {
    const data = await api.units.list()
    return data
  } catch (error) {
    console.error(error)
  }
}

// ❌ INCORRETO - promises sem await
function loadData() {
  return api.units.list().then((data) => {
    return data
  })
}
```

### Error Handling

```typescript
// ✅ CORRETO - throw ApiError tipado
if (response.status === 404) {
  throw new ApiError(404, 'UNIT_NOT_FOUND', 'Unidade não encontrada')
}

// ❌ INCORRETO - throw string
if (response.status === 404) {
  throw 'Unit not found'
}
```

## Testes

### Coverage Mínimo

- **Lines:** 80%
- **Functions:** 80%
- **Branches:** 80%
- **Statements:** 80%

### Estrutura de Teste

```typescript
describe('FeatureName', () => {
  // Setup comum
  beforeEach(() => {
    // ...
  })

  // Happy path
  it('should succeed when valid input', async () => {
    // ...
  })

  // Error cases
  it('should throw ApiError when not found', async () => {
    // ...
  })

  it('should retry on network error', async () => {
    // ...
  })
})
```

## Pull Request

### Checklist

Antes de abrir PR, garantir:

- [ ] Testes passando (`bun test`)
- [ ] Coverage >80% (`bun test --coverage`)
- [ ] Lint sem erros (`bun run lint`)
- [ ] Types corretos (`bun run type-check`)
- [ ] CHANGELOG.md atualizado
- [ ] Commits seguem Conventional Commits
- [ ] Branch atualizada com `main` (`git rebase upstream/main`)

### Template de PR

```markdown
## Descrição

[Descreva as mudanças de forma clara]

## Tipo de Mudança

- [ ] Bug fix (non-breaking change)
- [ ] Nova feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentação

## Como Testar

1. Clone o PR
2. Rode `bun install`
3. Execute `bun test`
4. Teste manualmente com...

## Screenshots (se aplicável)

[Adicione screenshots]

## Checklist

- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] CHANGELOG.md atualizado
- [ ] Sem breaking changes OU breaking changes documentadas
```

## Code Review

### O que esperamos

- **Código limpo:** Fácil de ler e entender
- **Testes completos:** Cenários happy path + edge cases
- **Documentação:** JSDoc em funções públicas
- **Performance:** Não adicionar latência desnecessária
- **Segurança:** Não expor tokens, validar inputs

### Feedback

- Code review é colaborativo, não crítico
- Perguntas são bem-vindas
- Se discordar, discuta educadamente
- Aceite feedback construtivo

## Publicação

Apenas maintainers podem publicar novas versões:

```bash
# Incrementar versão
npm version patch  # 0.1.0 → 0.1.1
npm version minor  # 0.1.0 → 0.2.0
npm version major  # 0.1.0 → 1.0.0

# Push tag
git push --follow-tags

# CI/CD publica automaticamente
```

## Referências

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Vitest](https://vitest.dev/)
- [axios-mock-adapter](https://github.com/ctimmerm/axios-mock-adapter)
