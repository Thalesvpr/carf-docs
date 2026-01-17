---
modules: [GEOAPI, GEOGIS]
epic: maintainability
---

# UC-010-FE-002: XML Inválido

Fluxo de exceção do UC-010 Configurar Camadas WMS ocorrendo no passo 7 quando sistema recebe response HTTP 200 do GetCapabilities mas não consegue parsear XML retornado tipicamente causado por response não sendo XML válido (servidor retornou HTML de erro página de login ou JSON ao invés de XML esperado), XML malformado com tags não fechadas ou aninhamento incorreto violando sintaxe XML básica, namespace declarations faltando impedindo parser resolver prefixos como wms:Layer, encoding incorreto com caracteres especiais corrompidos (UTF-8 declarado mas bytes em ISO-8859-1 causando � replacement chars), ou response vazia sem conteúdo body apesar de status 200, sistema tenta parsear usando xml2js ou DOMParser capturando exception SyntaxError ou ParseError lançada ao encontrar estrutura inválida, loga erro incluindo primeiros 500 caracteres do response body para debug mostrando o que servidor realmente retornou, exibe modal amarelo warning com título "Resposta Inválida do Servidor WMS" mensagem "O servidor retornou uma resposta que não é um documento XML válido. Verifique se URL é realmente de serviço WMS/WMTS compatível com padrão OGC" orientando sobre possível causa, inclui seção expansível Detalhes Técnicos mostrando preview do response truncado permitindo ADMIN identificar visualmente problema como `<html><head><title>404 Not Found</title>` indicando página erro ao invés de XML WMS ou `{"error": "API key required"}` indicando endpoint JSON incorreto, oferece botões Ver Response Completo abrindo modal com textarea readonly contendo response body inteiro permitindo análise completa ou copiar para consulta com suporte, Copiar URL copiando URL testada para clipboard facilitando teste externo em navegador ou cliente WMS desktop (QGIS), Tentar Novamente fechando modal, ADMIN verifica URL consultando documentação oficial da fonte garantindo endpoint correto usualmente terminando em /wms ou /geoserver/wms com query params corretos, testa URL isoladamente em navegador verificando se retorna XML começando com `<?xml version="1.0"?><WMS_Capabilities>` confirmando validade.

**Ponto de Desvio:** Passo 7 do UC-010 (parsing do XML)

**Retorno:** Erro exibido, ADMIN verifica se URL é realmente WMS/WMTS válido

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
