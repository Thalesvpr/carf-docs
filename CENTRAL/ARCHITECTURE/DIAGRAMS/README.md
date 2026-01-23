---
type: readme
status: review
updated: 2026-01-22
---

# DIAGRAMS

Diagramas visuais da arquitetura do CARF em formato Mermaid (.mmd) fornecendo visualizacoes complementares a documentacao textual.

O [ecossistema](./ecosystem.mmd) apresenta visao geral de todos os sistemas e suas conexoes, mostrando como GEOAPI, GEOWEB, REURBCAD, ADMIN, GEOGIS, WEBDOCS e KEYCLOAK se relacionam. O [fluxo de dados](./data-flow.mmd) ilustra como dados fluem entre sistemas desde a coleta em campo ate a persistencia no banco, incluindo sincronizacao offline e processamento de filas. O [deployment](./deployment.mmd) mostra a topologia de implantacao em producao com containers, load balancers e servicos de infraestrutura.

Diagramas Mermaid podem ser renderizados diretamente no portal WEBDOCS ou em ferramentas como VS Code com extensao apropriada. Para exportacao em formatos estaticos como PNG ou SVG, utilize o CLI do Mermaid ou servicos online como mermaid.live.

<!-- CARF-INDEX-START -->

<!-- CARF-INDEX-END -->
