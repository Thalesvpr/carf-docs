---
id: UC-008-FE-002
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-008-FE-002: SRID Desconhecido

Fluxo de excecao do UC-008 quando sistema de coordenadas nao pode ser identificado.

## Condicao

Durante processamento do UC-008, sistema nao consegue detectar SRID do arquivo.

## Fluxo

1. Sistema tenta identificar sistema de coordenadas
2. Sistema detecta falha (arquivo .prj ausente ou invalido)
3. Sistema aplica fallback assumindo SRID padrao
4. Sistema preserva geometrias sem reprojecao
5. Sistema registra warning no log
6. Sistema continua processamento
7. Sistema notifica usuario sobre ressalva

## Causas Comuns

- Arquivo .prj ausente no ZIP
- Arquivo .prj corrompido ou vazio
- Projecao customizada desconhecida
- Sintaxe WKT incompativel

## Orientacoes ao Usuario

- Verificar geometrias no mapa apos importacao
- Se posicionamento incorreto, reverter importacao
- Adicionar .prj correto ao Shapefile
- Reexportar do QGIS com opcao de salvar CRS

## Retorno

Importacao continua com SRID padrao assumido. Warning exibido na notificacao final.
