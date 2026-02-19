---
type: leaf
status: approved
updated: 2026-01-28
---

# Ping de Registro

Coordenada GPS capturada no momento em que o agente de campo inicia a coleta de dados de uma unidade. Serve como ancora geografica para todo o conteudo associado aquele trabalho.

O ping nao valida nem corrige a unidade selecionada. Ele apenas documenta o local real onde a coleta aconteceu. Todo o material coletado - formulario, fotos, croquis, assinaturas - fica vinculado a esse ponto.

## Funcionamento

Quando o agente seleciona uma unidade e inicia o trabalho, o sistema registra latitude e longitude do dispositivo naquele instante. Esse ponto e preservado integralmente, sem ajustes automaticos.

## Inconsistencia Geografica

Se o ping cair fisicamente mais proximo de outra unidade, o sistema nao corrige automaticamente. A divergencia e marcada como inconsistencia geografica, calculada pela distancia entre o ponto coletado e a localizacao esperada da unidade cadastrada.

Essa marcacao nao bloqueia o trabalho em campo nem invalida o registro. Apenas sinaliza para o analista que existe divergencia entre local esperado e local efetivo. O analista decide se valida, corrige ou invalida em etapa posterior.

## Justificativa

Inconsistencias de campo sao informacao, nao erro. Um agente pode estar no formulario da unidade B1 mas fisicamente mais proximo da A1 por diversos motivos legitimos. Preservar essa informacao garante rastreabilidade e permite decisoes conscientes de validacao.
