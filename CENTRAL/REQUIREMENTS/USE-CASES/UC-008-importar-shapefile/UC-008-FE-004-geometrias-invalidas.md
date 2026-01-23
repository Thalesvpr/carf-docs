---
id: UC-008-FE-004
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-008-FE-004: Geometrias Invalidas

Fluxo de excecao do UC-008 quando geometrias apresentam problemas topologicos.

## Condicao

Durante processamento do UC-008, sistema detecta geometrias com estrutura invalida.

## Fluxo

1. Sistema valida topologia da geometria
2. Sistema detecta problema estrutural
3. Sistema tenta correcao automatica
4. Se correcao bem-sucedida, importa com flag de revisao
5. Se correcao falha, pula registro
6. Sistema registra detalhes no log
7. Sistema continua com proximos registros

## Problemas Detectados

- Auto-intersecoes (poligono cruza a si proprio)
- Aneis nao fechados
- Vertices duplicados consecutivos
- Coordenadas corrompidas

## Comportamento

- Sistema tenta reparar automaticamente
- Geometrias reparadas marcadas para revisao
- Geometrias irrecuperaveis ignoradas
- Log inclui motivo especifico do problema

## Orientacoes ao Usuario

- Baixar log para identificar features problematicas
- Abrir Shapefile original em QGIS
- Usar ferramenta de validacao de geometrias
- Corrigir e reimportar registros afetados

## Retorno

Geometrias validas ou corrigidas importadas. Invalidas ignoradas com registro no log.
