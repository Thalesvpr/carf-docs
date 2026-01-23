---
type: leaf
status: review
updated: 2026-01-22
---

# Estacao RBMC

Estacao de referencia da Rede Brasileira de Monitoramento Continuo operada pelo IBGE. Fornece dados de correcao para pos-processamento de levantamentos GPS.

A RBMC e infraestrutura nacional de geodesia. Estacoes distribuidas pelo pais coletam observacoes GPS continuamente, disponibilizando dados que permitem corrigir coordenadas brutas.

## Funcionamento

Receptor GPS permanente com coordenadas conhecidas com precisao milimetrica. Observacoes sao publicadas em arquivos RINEX diarios. Topografos baixam dados do mesmo periodo de sua coleta.

## Pos-Processamento

Software de processamento diferencial compara observacoes do receptor de campo com as da estacao RBMC. A diferenca permite calcular correcoes, melhorando precisao de metros para centimetros.

## Distancia

Ideal que estacao RBMC esteja a menos de 300km do levantamento. Distancias maiores degradam qualidade da correcao atmosferica, reduzindo precisao final.

## Selecao Automatica

Sistema seleciona automaticamente a estacao mais proxima dos pontos coletados, baixa arquivos necessarios, e processa os dados sem intervencao manual do topografo.
