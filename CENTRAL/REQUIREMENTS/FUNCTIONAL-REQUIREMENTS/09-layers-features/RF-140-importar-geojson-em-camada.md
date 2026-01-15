---
modules: [GEOAPI]
epic: compatibility
---

# RF-140: Importar GeoJSON em Camada

Este requisito especifica que usuários autorizados devem poder importar arquivos GeoJSON em camadas existentes permitindo ingestão de dados geoespaciais a partir de fonte externa ou sistema terceiro, onde processo converte FeatureCollection do GeoJSON em features nativas do sistema. O sistema deve aceitar upload de arquivo com extensão .geojson validando que conteúdo é JSON bem-formado e estrutura corresponde à especificação GeoJSON com FeatureCollection contendo array de Features cada uma com geometria e properties. A validação de estrutura deve verificar presença de campos obrigatórios como type geometry e properties em cada feature, garantir que geometries são válidas conforme especificação GeoJSON, e confirmar que tipos de geometria das features são compatíveis com tipo configurado na camada de destino. Após validação bem-sucedida, o sistema deve processar criação de features iterando sobre array de features do GeoJSON extraindo geometria convertendo para formato PostGIS e mapeando properties para atributos customizados da feature conforme schema da camada, onde processo pode requerer transformação de nomes de campos ou tipos de dados. A importação ocorre em transação única permitindo rollback completo se qualquer feature falhar validação. O sistema deve fornecer feedback de progresso e relatório final. A funcionalidade deve estar disponível nos módulos GEOWEB e GEOAPI via endpoint de importação.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
