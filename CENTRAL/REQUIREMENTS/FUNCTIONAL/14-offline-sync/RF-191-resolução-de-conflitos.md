---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
---

# RF-191: Resolucao de Conflitos

## Descricao

Sistema deve fornecer interface intuitiva de resolucao de conflitos apresentando tela dedicada com registros em conflito identificados durante sincronizacao. Cada conflito exibe visualizacao diff com campos modificados em cada versao utilizando cores diferenciadas para identificacao rapida de diferencas. Para cada conflito, usuario dispoe de tres opcoes: Manter local que descarta versao do servidor e persiste modificacoes locais, Manter servidor que descarta edicoes locais e aceita versao do servidor, ou Mesclar que permite combinar seletivamente atributos de ambas as versoes campo por campo. Interface de mesclagem apresenta formulario onde cada campo conflitante exibe ambos valores com opcao de selecao granular, alem de campo para justificar decisao registrada em log de auditoria. Apos resolucao, sistema marca registros como sincronizados.

## Criterios de Aceitacao

1. Visualizacao diff com cores diferenciadas
2. Opcao Manter local
3. Opcao Manter servidor
4. Opcao Mesclar campo por campo
5. Justificativa registrada em auditoria

## Rastreabilidade

- Modulos: REURBCAD
- Requisitos dependentes: RF-190
