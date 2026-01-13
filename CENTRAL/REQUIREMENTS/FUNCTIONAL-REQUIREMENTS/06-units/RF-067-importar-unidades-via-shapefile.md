---
modules: [GEOWEB, GEOGIS]
epic: compatibility
---

# RF-067: Importar Unidades via Shapefile

O sistema deve permitir que usuários com perfil ADMIN importem múltiplas unidades simultaneamente através de upload de arquivo shapefile (.zip contendo .shp .shx .dbf .prj), onde a interface GEOWEB oferece wizard guiando o processo de importação em etapas sequenciais. Após upload, o sistema exibe wizard de mapeamento de campos permitindo que administrador associe colunas do shapefile (nome técnico da camada) aos campos do modelo de unidade do sistema (código endereço tipo comunidade), incluindo sugestões automáticas baseadas em nomes similares e prévia dos dados para validação visual. Antes de executar a importação definitiva, o sistema apresenta preview mostrando quantas unidades serão criadas, estatísticas de preenchimento de campos e alertas sobre possíveis problemas (geometrias inválidas, códigos duplicados, tipos não reconhecidos), permitindo ajustes no mapeamento ou correção do shapefile antes do commit. A importação em lote processa todas as unidades válidas transacionalmente, onde sucesso completo resulta em criação de todas as unidades e falhas acionam rollback completo, garantindo consistência e evitando importações parciais que comprometam integridade da base de dados.

---

**Última atualização:** 2025-12-30
