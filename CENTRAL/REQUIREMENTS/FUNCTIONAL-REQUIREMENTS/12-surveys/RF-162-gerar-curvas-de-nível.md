---
modules: [GEOGIS]
epic: other
---

# RF-162: Gerar Curvas de Nível

O sistema oferece capacidade de gerar curvas de nível a partir de pontos topográficos previamente importados, aplicando algoritmos de interpolação espacial como TIN (Triangulated Irregular Network) ou IDW (Inverse Distance Weighting) para estimar valores de elevação em toda a área de interesse e derivar isolinhas altimétricas. O usuário pode configurar o parâmetro de equidistância vertical entre as curvas conforme as necessidades técnicas do projeto, permitindo representações mais detalhadas com equidistâncias menores para projetos de precisão ou representações mais generalizadas para análises de contexto regional. As curvas resultantes são criadas como features do tipo LineString no banco geoespacial, preservando a conectividade topológica e permitindo análises de relevo e visualização tridimensional do terreno. Esta funcionalidade é particularmente útil em projetos de regularização fundiária em áreas de topografia acidentada, onde a representação altimétrica auxilia na identificação de áreas de risco geotécnico, planejamento de drenagem e validação de limites de unidades territoriais em conformidade com características do relevo natural.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
