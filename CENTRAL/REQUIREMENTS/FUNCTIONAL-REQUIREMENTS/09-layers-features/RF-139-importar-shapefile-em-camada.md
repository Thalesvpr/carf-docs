---
modules: [GEOWEB, GEOGIS]
epic: compatibility
---

# RF-139: Importar Shapefile em Camada

Este requisito estabelece que usuários autorizados devem poder importar shapefiles ESRI em camadas existentes criando features automaticamente a partir dos dados geoespaciais contidos no arquivo, onde processo converte geometrias e atributos do shapefile para modelo de dados do sistema. O sistema deve aceitar upload de arquivo ZIP contendo componentes obrigatórios do shapefile incluindo .shp .shx .dbf e opcionalmente .prj para definição de sistema de coordenadas, onde validação garante que todos arquivos necessários estão presentes antes de processar importação. A interface deve fornecer funcionalidade de mapeamento de atributos permitindo que usuário especifique correspondência entre campos do DBF do shapefile e schema de atributos customizados da camada de destino, onde mapeamento pode incluir renomeação conversão de tipos e omissão de campos não relevantes. O processo de importação deve ocorrer em lote criando múltiplas features de uma só vez através de transação única, onde sistema lê geometrias e atributos do shapefile valida cada feature conforme tipo de geometria da camada e insere registros correspondentes no banco de dados, fornecendo feedback de progresso durante processamento e relatório final indicando quantas features foram importadas com sucesso e eventuais erros. O sistema deve reprojetar geometrias se necessário convertendo do sistema de coordenadas do shapefile para SRID configurado no sistema. A funcionalidade deve estar disponível nos módulos GEOWEB e GEOAPI.

---

**Última atualização:** 2025-12-30