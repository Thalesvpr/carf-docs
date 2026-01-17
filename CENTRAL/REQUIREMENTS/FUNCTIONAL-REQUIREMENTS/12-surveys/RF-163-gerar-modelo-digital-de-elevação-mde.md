---
modules: [GEOGIS]
epic: compatibility
---

# RF-163: Gerar Modelo Digital de Elevação (MDE)

O sistema possibilita a geração de Modelo Digital de Elevação através da interpolação de grid regular a partir de pontos topográficos coletados, criando uma representação matricial contínua do terreno onde cada pixel armazena um valor de altitude interpolado. O processamento utiliza técnicas geoestatísticas apropriadas para distribuir espacialmente os valores conhecidos de elevação, resultando em uma superfície digital que representa fielmente a topografia da área levantada. O MDE gerado é exportado no formato GeoTIFF padrão OGC, incluindo metadados de georreferenciamento e sistema de coordenadas, garantindo interoperabilidade com softwares GIS externos e permitindo análises avançadas de terreno como cálculo de declividade, orientação de vertentes e sombreamento. Adicionalmente, o sistema permite visualizar o MDE como camada raster sobreposta ao mapa base, aplicando esquemas de cores hipsométricos que facilitam a interpretação visual do relevo, auxiliando técnicos e gestores na compreensão tridimensional do território durante processos de planejamento urbano e análise de adequabilidade de áreas para regularização fundiária.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
