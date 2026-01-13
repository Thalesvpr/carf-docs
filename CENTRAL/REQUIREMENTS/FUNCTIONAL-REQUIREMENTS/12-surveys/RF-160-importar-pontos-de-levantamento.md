---
modules: [REURBCAD, GEOGIS]
epic: compatibility
---

# RF-160: Importar Pontos de Levantamento

O sistema permite a importação de coordenadas de pontos topográficos através de arquivos nos formatos CSV ou TXT, onde o usuário realiza o upload do arquivo contendo os dados geodésicos coletados em campo, incluindo coordenadas X Y Z e códigos de identificação dos pontos. A funcionalidade implementa um mecanismo de mapeamento de colunas que permite ao usuário correlacionar os campos do arquivo importado com os atributos esperados pelo sistema, garantindo flexibilidade no tratamento de diferentes estruturas de dados topográficos provenientes de equipamentos diversos. Após o processamento do arquivo, o sistema cria automaticamente features do tipo Point no banco de dados geoespacial, permitindo a visualização e análise posterior dos pontos levantados no contexto do projeto cadastral, incluindo sua integração com unidades territoriais e comunidades existentes. Esta funcionalidade é essencial para projetos de regularização fundiária que demandam levantamentos topográficos de precisão, facilitando a transição dos dados coletados em campo para o ambiente digital de gestão territorial.

---

**Última atualização:** 2025-12-30
