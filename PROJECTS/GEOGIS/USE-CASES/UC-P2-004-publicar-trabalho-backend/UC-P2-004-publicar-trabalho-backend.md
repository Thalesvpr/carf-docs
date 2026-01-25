---
id: UC-P2-004
type: UC
modules: []
status: review
created: 2026-01-24
updated: 2026-01-24
workflow: PARTE-2
---

# UC-P2-004: Publicar Trabalho no Backend

Analista finaliza georreferenciamento e publica poligonos no backend, liberando dados para campo.

## Referencia

Este UC implementa passos 9-10 do [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/02-georreferenciamento.md).

## Atores

- Primario: Analista (Plugin QGIS)
- Secundario: Backend GEOAPI

## Pre-condicoes

- Georreferenciamento concluido (UC-P2-003 concluido)
- Poligonos validados localmente
- Conexao com backend disponivel

## Fluxo Principal

1. Analista finaliza georreferenciamento
2. Analista clica em "Publicar" no Plugin
3. Plugin valida dados localmente:
   - Geometrias validas
   - Atributos obrigatorios preenchidos
   - Topologia consistente
4. Plugin exibe resumo para confirmacao
5. Analista confirma publicacao
6. Plugin envia ao backend: `POST /api/poligonos/publicar`
7. Backend recebe dados
8. Backend valida novamente no servidor
9. Backend persiste poligonos no banco
10. Backend associa poligonos ao TENANT
11. Backend registra timestamp de publicacao
12. **REGRA CRITICA:** Backend marca dados como "liberados"
13. Plugin exibe confirmacao de sucesso
14. Agentes de Campo podem baixar pacote (PARTE 3)

## Fluxos de Excecao

- FE-001: Validacao falha no servidor
- FE-002: Conflito com dados existentes
- FE-003: Falha de conexao durante envio
- FE-004: Permissao insuficiente

## Pos-condicoes

- Poligonos armazenados no backend
- Poligonos associados ao TENANT correto
- Dados marcados como "liberados" para campo
- Agentes de Campo podem baixar pacote temporario
- PARTE 2 concluida

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| RN-01 | Publicacao e PRE-REQUISITO para acesso em campo |
| RN-02 | Dados NAO ficam disponiveis ANTES da publicacao |
| RN-03 | Timestamp de publicacao e registrado |
| RN-04 | Apenas apos publicacao, PARTE 3 pode iniciar |
