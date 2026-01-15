---
modules: [GEOWEB]
epic: performance
---

# RF-214: Testar Conexão WMS/WMTS

O sistema implementa funcionalidade de validação que testa disponibilidade e conformidade de serviços WMS/WMTS antes de persistir configuração definitiva no catálogo de camadas, prevenindo adição de URLs inválidas, inacessíveis ou incompatíveis que resultariam em frustração dos usuários finais ao tentarem visualizar camadas não funcionais. O teste executa requisição GetCapabilities apropriada ao tipo de serviço (WMS ou WMTS) e verifica sucesso da resposta HTTP com status 200, validação de XML retornado contra schema OGC para confirmar conformidade com padrão, e presença dos elementos essenciais que permitem renderização como lista de layers disponíveis e sistemas de coordenadas suportados. Quando validação identifica problemas, o sistema apresenta feedback de erro descritivo que especifica natureza da falha incluindo mensagens como "URL não acessível: timeout após 30 segundos", "Resposta inválida: XML malformado", "Serviço não suporta projeção EPSG:4326 requerida" ou "Certificado SSL inválido ou expirado", orientando administrador sobre ação corretiva necessária. Validação bem-sucedida resulta em feedback positivo e habilitação do botão de confirmação que persiste configuração, proporcionando confiança de que camada adicionada efetivamente funcionará quando usuários tentarem visualizá-la, reduzindo chamados de suporte e frustração decorrente de funcionalidades aparentemente quebradas devido a configurações inadequadas de serviços externos.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
