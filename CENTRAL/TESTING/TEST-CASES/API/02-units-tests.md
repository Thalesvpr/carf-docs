# Units API Tests

Casos de teste para endpoints de unidades habitacionais.

## Create Unit

### TC-UNIT-001: Criar unidade com dados válidos

```gherkin
Cenário: Cadastrar nova unidade com geometria válida
  Dado que estou autenticado como "cadastrista"
  E tenho acesso ao tenant "sp-municipio"
  Quando envio POST /api/units com:
    | address.street      | Rua das Flores |
    | address.number      | 123            |
    | address.neighborhood| Centro         |
    | address.city        | São Paulo      |
    | address.state       | SP             |
    | address.zip_code    | 01310-100      |
    | geometry            | {polygon_valido} |
  Então recebo status 201
  E a resposta contém "id"
  E a resposta contém "code" no formato "UNI-YYYY-NNNNN"
  E "status" é "Rascunho"
  E "area_m2" é calculada automaticamente
```

### TC-UNIT-002: Geometria inválida (auto-intersecção)

```gherkin
Cenário: Rejeitar polígono com auto-intersecção
  Dado que estou autenticado como "cadastrista"
  Quando envio POST /api/units com geometry auto-intersectante
  Então recebo status 400
  E a resposta contém "error" = "invalid_geometry"
  E a resposta contém "details" mencionando "self-intersection"
```

### TC-UNIT-003: Sobreposição com unidade existente

```gherkin
Cenário: Detectar sobreposição com unidade existente
  Dado que existe uma unidade com polígono em área X
  Quando envio POST /api/units com geometry sobrepondo área X
  Então recebo status 409
  E a resposta contém "error" = "geometry_overlap"
  E a resposta contém "overlapping_units" com IDs das unidades
```

## Read Unit

### TC-UNIT-010: Buscar unidade existente

```gherkin
Cenário: Buscar unidade por ID
  Dado que existe uma unidade com ID "unit-123"
  E estou autenticado no tenant correto
  Quando envio GET /api/units/unit-123
  Então recebo status 200
  E a resposta contém todos os campos da unidade
```

### TC-UNIT-011: Unidade não encontrada

```gherkin
Cenário: Buscar unidade inexistente retorna 404
  Quando envio GET /api/units/uuid-inexistente
  Então recebo status 404
```

### TC-UNIT-012: Unidade de outro tenant

```gherkin
Cenário: RLS impede acesso a unidade de outro tenant
  Dado que existe uma unidade no tenant "outro-tenant"
  E estou autenticado no tenant "meu-tenant"
  Quando envio GET /api/units/{id_unidade_outro_tenant}
  Então recebo status 404
```

## List Units

### TC-UNIT-020: Listar com paginação

```gherkin
Cenário: Listar unidades com paginação
  Dado que existem 50 unidades no tenant
  Quando envio GET /api/units?page=1&limit=20
  Então recebo status 200
  E "data" contém 20 itens
  E "pagination.total" é 50
  E "pagination.total_pages" é 3
```

### TC-UNIT-021: Filtrar por status

```gherkin
Cenário: Filtrar unidades por status
  Dado que existem 10 unidades "Aprovado" e 5 "Pendente"
  Quando envio GET /api/units?status=Aprovado
  Então recebo status 200
  E "data" contém 10 itens
  E todos os itens têm "status" = "Aprovado"
```

### TC-UNIT-022: Busca por bounding box

```gherkin
Cenário: Filtrar unidades por região geográfica
  Dado que existem unidades em diferentes locais
  Quando envio GET /api/units?bbox=-46.64,-23.55,-46.63,-23.54
  Então recebo apenas unidades cujo centroid está dentro do bbox
```

## Update Unit

### TC-UNIT-030: Atualizar endereço

```gherkin
Cenário: Atualizar endereço de unidade
  Dado que existe uma unidade com status "Rascunho"
  E estou autenticado como "cadastrista"
  Quando envio PATCH /api/units/{id} com:
    | address.number | 456 |
  Então recebo status 200
  E "address.number" é "456"
  E "updated_at" é atualizado
```

### TC-UNIT-031: Não permitir edição de unidade aprovada

```gherkin
Cenário: Bloquear edição de unidade aprovada
  Dado que existe uma unidade com status "Aprovado"
  Quando envio PATCH /api/units/{id}
  Então recebo status 403
  E a resposta contém "error" = "unit_locked"
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
