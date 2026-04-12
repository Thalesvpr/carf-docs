---
id: UC-007-FA-001
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-007-FA-001: Exportacao Rapida (Poucos Dados)

Fluxo alternativo do UC-007 para exportacao sincrona quando ha poucos registros.

## Condicao

No passo 10 do UC-007, sistema detecta menos de 100 registros a exportar.

## Fluxo

1. Sistema verifica quantidade de registros
2. Sistema detecta volume pequeno (menos de 100)
3. Sistema executa exportacao sincrona no mesmo request
4. Sistema processa dados e gera arquivo
5. Sistema retorna arquivo diretamente no response
6. Download inicia automaticamente no navegador

## Vantagens

- Resposta imediata sem aguardar notificacao
- Nao utiliza fila de processamento
- Permite iteracao rapida para validacao em QGIS

## Retorno

Arquivo retornado diretamente. Download inicia imediatamente apos clique.

## Pos-condicoes

- Arquivo exportado e baixado em operacao unica
- Sem armazenamento em servidor
