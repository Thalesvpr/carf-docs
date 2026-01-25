---
id: UC-006-FA-001
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-006-FA-001: Geracao Rapida (Poucos Dados)

Fluxo alternativo do UC-006 para geracao sincrona quando comunidade possui poucos dados.

## Condicao

No passo 11 do UC-006, sistema detecta que comunidade possui menos de 100 unidades.

## Fluxo

1. Sistema verifica quantidade de unidades
2. Sistema detecta volume pequeno (menos de 100)
3. Sistema executa geracao sincrona no mesmo request
4. Sistema processa dados e gera arquivo
5. Sistema retorna arquivo diretamente no response
6. Download inicia automaticamente no navegador

## Vantagens

- Resposta imediata sem aguardar notificacao
- Nao utiliza fila de processamento
- Permite iteracao rapida ajustando parametros

## Retorno

Arquivo retornado diretamente. Download inicia imediatamente apos clique.

## Pos-condicoes

- Relatorio gerado e baixado em operacao unica
- Sem armazenamento em servidor (arquivo temporario)
