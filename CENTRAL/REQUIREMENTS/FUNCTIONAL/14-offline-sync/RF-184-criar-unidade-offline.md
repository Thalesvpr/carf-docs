---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
---

# RF-184: Criar Unidade Offline

## Descricao

Sistema deve permitir criacao completa de unidades territoriais no aplicativo mobile sem conexao com internet. Formulario totalmente funcional offline captura todos os atributos obrigatorios incluindo identificacao, tipo de ocupacao, geometria espacial desenhada no mapa e vinculacao com titulares. Sistema gera automaticamente UUID localmente no dispositivo para identificar univocamente a unidade, garantindo que multiplos dispositivos operando simultaneamente offline nao gerem conflitos de identificacao ao sincronizar. Unidade criada recebe flag de "pendente sincronizacao" com icone distintivo indicando que registro foi criado localmente e ainda nao foi persistido no banco central. Validacoes de negocio executadas localmente incluindo campos obrigatorios, formatos e consistencia de dados.

## Criterios de Aceitacao

1. Formulario completo funcional offline
2. Geracao de UUID local automatico
3. Flag visual de pendente sincronizacao
4. Validacoes de negocio locais
5. Vinculacao com titulares offline

## Rastreabilidade

- Modulos: REURBCAD
- Requisitos dependentes: RF-044, RF-182
