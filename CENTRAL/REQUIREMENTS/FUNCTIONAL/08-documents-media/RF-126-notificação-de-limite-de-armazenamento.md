---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-126: Notificacao de Limite de Armazenamento

## Descricao

Sistema deve notificar administradores de tenant proativamente quando uso de storage atinge 80% da quota configurada, permitindo acao preventiva antes de uploads bloqueados. Monitoramento implementado via job agendado que verifica periodicamente consumo de cada tenant comparando com quota, calculando percentual utilizado e identificando tenants que ultrapassaram threshold de alerta. Quando threshold atingido, sistema envia email de alerta para administradores do tenant com informacoes sobre uso atual, quota total, percentual consumido e orientacoes sobre como liberar espaco ou solicitar aumento. Painel administrativo exibe metricas de storage visualmente atraves de grafico ou barra de progresso com indicadores amarelo proximo do limite e vermelho quando excedido. Sistema registra envio de notificacoes para evitar spam, enviando maximo uma vez por periodo configurado.

## Criterios de Aceitacao

1. Alerta automatico ao atingir 80% da quota
2. Email para administradores do tenant
3. Painel visual de uso de storage
4. Indicadores visuais de alerta
5. Controle de frequencia de notificacoes

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-125, RF-017
