---
id: UC-007-FA-002
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-007-FA-002: Exportar Selecao

Fluxo alternativo do UC-007 para exportar apenas unidades selecionadas manualmente.

## Condicao

No passo 3 do UC-007, usuario deseja exportar unidades especificas ao inves de todas filtradas.

## Fluxo

1. Usuario marca checkboxes nas unidades desejadas
2. Sistema atualiza contador de selecao
3. Botao muda para Exportar Selecionadas (N)
4. Usuario clica em Exportar Selecionadas
5. Sistema exibe modal confirmando quantidade
6. Usuario configura formato e opcoes
7. Sistema exporta apenas IDs selecionados

## Casos de Uso

- Exportar unidades problematicas para analise
- Compartilhar subset especifico com equipe externa
- Reduzir tamanho do arquivo exportado

## Retorno

Apenas unidades marcadas sao exportadas, ignorando restante dos resultados.

## Pos-condicoes

- Selecao mantida durante navegacao entre paginas
- Arquivo contem apenas registros selecionados
