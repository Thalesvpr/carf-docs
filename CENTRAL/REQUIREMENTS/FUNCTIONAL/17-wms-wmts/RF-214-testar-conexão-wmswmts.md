---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-214: Testar Conexao WMS/WMTS

## Descricao

Sistema deve implementar validacao que testa disponibilidade e conformidade de servicos WMS/WMTS antes de persistir configuracao, prevenindo adicao de URLs invalidas ou inacessiveis. Teste executa requisicao GetCapabilities e verifica sucesso HTTP 200, valida XML retornado contra schema OGC, e confirma presenca de elementos essenciais como lista de layers e sistemas de coordenadas. Quando validacao identifica problemas, sistema apresenta feedback de erro descritivo especificando falha como "URL nao acessivel: timeout", "XML malformado" ou "Certificado SSL invalido". Validacao bem-sucedida habilita botao de confirmacao proporcionando confianca de que camada funcionara corretamente.

## Criterios de Aceitacao

1. Requisicao GetCapabilities automatica
2. Validacao contra schema OGC
3. Feedback de erro descritivo
4. Verificacao de certificado SSL
5. Botao de confirmacao habilitado apos sucesso

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-212, RF-213
