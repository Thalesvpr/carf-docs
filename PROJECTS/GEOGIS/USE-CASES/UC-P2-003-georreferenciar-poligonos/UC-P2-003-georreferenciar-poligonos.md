---
id: UC-P2-003
type: UC
modules: []
status: review
created: 2026-01-24
updated: 2026-01-24
workflow: PARTE-2
---

# UC-P2-003: Georreferenciar Poligonos

Analista usa ferramentas do QGIS para desenhar poligonos de comunidades, quadras e lotes.

## Referencia

Este UC implementa passo 8 do [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/02-georreferenciamento.md).

## Atores

- Primario: Analista (Plugin QGIS)
- Secundario: QGIS (ferramentas nativas)

## Pre-condicoes

- Ortofoto carregada no QGIS (UC-P2-002 concluido)
- Ferramentas de edicao do QGIS disponiveis

## Fluxo Principal

1. Analista utiliza ortofoto como referencia visual
2. Analista ativa modo de edicao no QGIS
3. Analista desenha poligonos de comunidades (limites da area)
4. Analista desenha poligonos de quadras (divisoes internas)
5. Analista desenha poligonos de lotes (unidades individuais)
6. Analista preenche atributos de cada poligono:
   - Identificador unico
   - Tipo (comunidade/quadra/lote)
   - Metadados adicionais
7. Analista usa snapping para precisao
8. Analista valida topologia:
   - Sem sobreposicoes entre poligonos
   - Sem gaps entre poligonos adjacentes
   - Hierarquia consistente (lote dentro de quadra, quadra dentro de comunidade)
9. Plugin valida regras de negocio
10. Trabalho salvo localmente durante edicao

## Fluxos Alternativos

- FA-001: Importar poligonos existentes de shapefile
- FA-002: Usar ferramenta de auto-deteccao de bordas

## Fluxos de Excecao

- FE-001: Topologia invalida (sobreposicao)
- FE-002: Atributos obrigatorios faltando
- FE-003: Hierarquia inconsistente

## Pos-condicoes

- Poligonos desenhados e validados
- Atributos preenchidos
- Topologia consistente
- Trabalho pronto para publicacao (UC-P2-004)

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| RN-01 | Poligonos NAO podem se sobrepor |
| RN-02 | Lotes DEVEM estar dentro de quadras |
| RN-03 | Quadras DEVEM estar dentro de comunidades |
| RN-04 | Atributos obrigatorios DEVEM ser preenchidos |
