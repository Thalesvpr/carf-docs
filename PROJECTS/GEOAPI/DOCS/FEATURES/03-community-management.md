---
type: leaf
status: review
updated: 2026-02-08
---

# Community Management Feature

A feature de gerenciamento de comunidades permite criar, consultar e editar assentamentos que agrupam unidades habitacionais em um contexto geografico e social. Comunidades sao a unidade organizacional principal para processos de regularizacao fundiaria e servem como escopo de autorizacao de acesso para equipes de campo, determinando quais unidades cada equipe pode cadastrar e editar.

## User Stories

US-020 Criar Comunidade: o gestor informa codigo unico, nome, tipo (URBANA, RURAL, QUILOMBOLA, RIBEIRINHA), municipio, estado e opcionalmente boundary como poligono GeoJSON. O sistema valida unicidade do codigo por tenant e persiste o registro.

US-021 Visualizar Comunidade no Mapa: o usuario visualiza o boundary da comunidade sobreposto ao mapa base com unidades internas renderizadas como poligonos coloridos por status. A exportacao GeoJSON retorna FeatureCollection com boundary e todas as unidades como Features individuais.

US-022 Editar Boundary: o gestor atualiza o perimetro da comunidade. O sistema valida o poligono via PostGIS ST_IsValid e recalcula a area via ST_Area. A alteracao do boundary nao afeta unidades ja cadastradas dentro do perimetro anterior.

## Endpoints

| Metodo | Rota | Descricao |
|--------|------|-----------|
| POST | /api/communities | Criar comunidade |
| GET | /api/communities/{id} | Obter comunidade |
| GET | /api/communities | Listar com paginacao |
| PATCH | /api/communities/{id} | Atualizar comunidade |
| GET | /api/communities/{id}/units | Listar unidades da comunidade |
| GET | /api/communities/{id}/geojson | Exportar como GeoJSON |

## Regras de Negocio

RN-020: codigo da comunidade deve ser unico por tenant, constraint UNIQUE em (tenant_id, code). RN-021: boundary quando informado deve ser poligono valido conforme PostGIS ST_IsValid, fechado e sem auto-interseccao. RN-022: area da comunidade e calculada automaticamente via ST_Area quando boundary e informado. RN-023: tipo de comunidade aceita apenas valores URBANA, RURAL, QUILOMBOLA e RIBEIRINHA. RN-024: municipio e estado sao obrigatorios pois determinam o contexto jurisdicional do processo de regularizacao.

## Permissoes

| Acao | field-cadastrator | field-coordinator | analyst | manager | admin | super-admin |
|------|-------------------|-------------------|---------|---------|-------|-------------|
| Criar | nao | nao | nao | sim | sim | sim |
| Editar | nao | nao | nao | sim | sim | sim |
| Visualizar | sim | sim | sim | sim | sim | sim |
| Listar unidades | sim | sim | sim | sim | sim | sim |
| Exportar GeoJSON | sim | sim | sim | sim | sim | sim |
