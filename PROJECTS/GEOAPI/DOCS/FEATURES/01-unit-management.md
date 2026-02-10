---
type: leaf
status: rejected
updated: 2026-02-08
description: Status era 'active' que nao e valor valido. Deve ser review, approved ou rejected conforme STD-001.
---

# Unit Management Feature

A feature de gerenciamento de unidades permite cadastrar, visualizar, editar e aprovar unidades habitacionais dentro do sistema CARF. Abrange cadastro com endereco e geometria georreferenciada, upload de fotos, vinculacao de titulares, workflow de aprovacao e visualizacao em mapa.

## User Stories

US-001 Cadastrar Unidade: o cadastrista informa endereco completo e desenha poligono no mapa ou informa coordenadas. A area e calculada automaticamente, um codigo unico no formato UNI-YYYY-NNNNN e gerado e o status inicial e Rascunho.

US-002 Visualizar no Mapa: o usuario visualiza poligonos das unidades com cores por status, clustering em zoom baixo, popup com informacoes resumidas ao clicar e filtros por status, bairro e comunidade.

US-003 Submeter para Analise: o cadastrista submete a unidade, que requer ao menos um titular vinculado. O status muda de Rascunho para Pendente, aprovadores do tenant sao notificados e o historico registra timestamp e usuario.

## Endpoints

| Metodo | Rota | Descricao |
|--------|------|-----------|
| POST | /api/units | Criar unidade |
| GET | /api/units/{id} | Obter unidade |
| GET | /api/units | Listar com filtros |
| PATCH | /api/units/{id} | Atualizar |
| DELETE | /api/units/{id} | Excluir (rascunho) |
| POST | /api/units/{id}/submit | Submeter para analise |
| POST | /api/units/{id}/approve | Aprovar |
| POST | /api/units/{id}/reject | Rejeitar |
| GET | /api/units/geojson | Exportar GeoJSON |

## Regras de Negocio

RN-001: geometria deve ser poligono valido (fechado, sem auto-interseccao). RN-002: geometria nao pode sobrepor unidade existente no mesmo tenant. RN-003: area minima 10m2, maxima 100.000m2. RN-004: coordenadas devem estar dentro do municipio do tenant. RN-005: unidades aprovadas nao podem ser editadas. RN-006: exclusao so permitida em status Rascunho.

## Diagrama de Estados

O ciclo de vida da unidade segue quatro estados. Rascunho transiciona para Pendente via submit. Pendente transiciona para Aprovado via approve ou para Rejeitado via reject.

## Permissoes

| Acao | cadastrista | analista | aprovador | admin |
|------|-------------|----------|-----------|-------|
| Criar | sim | sim | sim | sim |
| Editar | sim | sim | sim | sim |
| Visualizar | sim | sim | sim | sim |
| Submeter | sim | sim | sim | sim |
| Aprovar | nao | nao | sim | sim |
| Rejeitar | nao | nao | sim | sim |
| Excluir | sim | sim | sim | sim |
