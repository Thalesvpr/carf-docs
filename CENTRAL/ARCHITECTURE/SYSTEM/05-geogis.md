---
type: leaf
status: approved
updated: 2026-01-24
---

# GEOGIS

Plugin QGIS em Python para georreferenciamento de poligonos e publicacao de dados integrando com ortofotos do CARF. Usado por Analistas GIS designados a um tenant para acessar ortofotos, desenhar comunidades, quadras e lotes, e publicar o trabalho no backend liberando dados para operacao em campo.

Stack com QGIS 3.28+, Python 3.9, PyQGIS para acesso a funcionalidades do QGIS, GDAL para processamento raster, Shapely para geometrias e PyProj para reprojecoes. Autenticacao em duas etapas: login via Keycloak OAuth2 PKCE com desktop flow usando servidor HTTP local temporario, seguido de AUTHENTICATION KEY (chave adicional que vincula sessao do plugin ao backend e habilita acesso as ortofotos do tenant).

## Capacidades

Acesso automatico as ortofotos do tenant designado apos autenticacao. Ferramentas de desenho para criar poligonos de comunidades, quadras e lotes sobre a ortofoto. Validacao topologica identificando sobreposicoes e gaps. Atribuicao de metadados aos poligonos. Publicacao do trabalho no backend que libera os dados para download pelos Agentes de Campo. Detalhes tecnicos no repositorio carf-geogis.
