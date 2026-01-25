---
type: workflow
status: approved
updated: 2026-01-25
part: 2
step: 9
---

# Passo 9: Publicacao no Backend

Analista publica o trabalho de georreferenciamento no backend.

## Fluxo

1. Analista finaliza georreferenciamento
2. Analista clica em "Publicar" no Plugin
3. Plugin valida dados localmente:
   - Geometrias validas
   - Atributos obrigatorios preenchidos
   - Topologia consistente
4. Plugin envia ao backend: `POST /api/poligonos/publicar`
5. Backend recebe e persiste poligonos
6. Backend associa poligonos ao TENANT
7. Backend registra timestamp de publicacao
8. Plugin exibe confirmacao de sucesso

## API Request

```http
POST /api/poligonos/publicar
Authorization: Bearer {jwt_token}
X-Auth-Key: {authentication_key}
Content-Type: application/json

{
  "tenant_id": "uuid",
  "ortofoto_id": "uuid",
  "poligonos": [
    {
      "tipo": "comunidade",
      "nome": "Comunidade X",
      "geometria": { "type": "Polygon", "coordinates": [...] },
      "atributos": { ... }
    },
    {
      "tipo": "quadra",
      "nome": "Quadra A",
      "comunidade_id": "uuid",
      "geometria": { "type": "Polygon", "coordinates": [...] }
    },
    {
      "tipo": "lote",
      "codigo": "001",
      "quadra_id": "uuid",
      "geometria": { "type": "Polygon", "coordinates": [...] }
    }
  ]
}
```

## Validacoes do Plugin

| Validacao | Descricao |
|-----------|-----------|
| Geometria valida | Poligono fechado, sem auto-intersecao |
| Atributos obrigatorios | Nome, tipo, codigo preenchidos |
| Topologia | Sem sobreposicoes, sem gaps |
| Hierarquia | Lote dentro de quadra, quadra dentro de comunidade |

## Resultado

- Poligonos persistidos no banco de dados
- Associacao com TENANT registrada
- Timestamp de publicacao salvo
- **REGRA CRITICA:** Dados agora disponiveis para PARTE 3

## Proximo Passo

Passo 10: Dados Liberados para Campo
