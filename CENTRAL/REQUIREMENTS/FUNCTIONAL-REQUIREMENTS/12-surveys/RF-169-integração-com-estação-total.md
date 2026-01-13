---
modules: [REURBCAD, GEOGIS]
epic: compatibility
---

# RF-169: Integração com Estação Total

O sistema oferece capacidade de importar dados provenientes de estações totais através de parsers especializados que interpretam formatos proprietários dos principais fabricantes de equipamentos topográficos incluindo Leica, Topcon, Trimble e South, reconhecendo estruturas específicas de codificação de medições angulares e lineares. O processo de importação extrai automaticamente coordenadas tridimensionais calculadas pelo software embarcado da estação total, além de atributos complementares como códigos de ponto, descrições de features e timestamps de coleta, transformando dados brutos de campo em informações estruturadas compatíveis com o modelo de dados geoespacial do sistema. Após extração e validação, o sistema cria features geográficas correspondentes aos pontos levantados, classificando-os automaticamente conforme códigos padronizados utilizados durante a coleta de campo e estabelecendo relacionamentos topológicos apropriados entre vértices de poligonais e elementos cadastrais. Esta funcionalidade elimina necessidade de conversões manuais ou uso de software intermediário para processamento de dados topográficos, agilizando fluxo de trabalho desde coleta em campo até disponibilização de informações georreferenciadas no sistema de gestão cadastral, reduzindo possibilidades de erro humano durante transcrição de coordenadas e garantindo rastreabilidade desde a medição original até o registro final no banco de dados.

---

**Última atualização:** 2025-12-30
