---
type: workflow
status: approved
updated: 2026-02-07
part: 2
step: 9
---

# Passo 9: Publicacao no Backend

Analista publica o trabalho de georreferenciamento no backend.

## Fluxo

1. Analista finaliza georreferenciamento
2. Analista clica em "Publicar" no Plugin
3. Plugin valida dados localmente: geometrias validas, atributos obrigatorios preenchidos, topologia consistente
4. Plugin envia ao backend via requisicao POST para /api/poligonos/publicar, autenticado com Bearer token e AUTHENTICATION KEY
5. Backend recebe e persiste poligonos
6. Backend associa poligonos ao TENANT
7. Backend registra timestamp de publicacao
8. Plugin exibe confirmacao de sucesso

## Corpo da Requisicao

A requisicao de publicacao envia os seguintes dados:

| Campo | Descricao |
|-------|-----------|
| tenant_id | UUID do tenant |
| ortofoto_id | UUID da ortofoto de referencia |
| poligonos | Lista de poligonos com tipo (comunidade, quadra, lote), nome ou codigo, geometria GeoJSON Polygon e atributos |

Cada poligono de tipo quadra inclui comunidade_id e cada lote inclui quadra_id, estabelecendo a hierarquia.

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
