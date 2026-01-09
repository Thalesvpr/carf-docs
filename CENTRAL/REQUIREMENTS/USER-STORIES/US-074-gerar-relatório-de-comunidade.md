---
modules: [GEOAPI, GEOWEB]
epic: compatibility
---

# US-074: Gerar Relatório de Comunidade

Como gestor, quero gerar relatório consolidado contendo estatísticas e indicadores de uma comunidade específica para que dashboard executivo seja apresentado a stakeholders e tomadores de decisão, onde a funcionalidade deve calcular totalizadores incluindo quantidade total de unidades titulares e área total cadastrada, garantindo geração de gráficos visuais mostrando distribuição por status (DRAFT PENDING APPROVED) e tipo de ocupação (RESIDENTIAL COMMERCIAL MIXED), permitindo exportação do relatório completo em formatos PDF para apresentações ou Excel para análises adicionais. Esta funcionalidade é implementada pelo módulo GEOWEB com interface de relatórios consumindo GEOAPI através do endpoint GET /api/reports/community-summary?communityId={id} que agrega dados estatísticos, integrada ao RF-203 (Relatórios de Comunidade) e UC-006 (Gerar Relatórios). Os critérios de aceitação incluem seleção de comunidade específica para geração do relatório através de dropdown ou busca, cálculo automático de indicadores totalizadores (total_units total_holders area_total_m2 area_average_m2), geração de gráfico de distribuição por status mostrando quantidade ou percentual em cada estado do workflow, gráfico de distribuição por tipo de ocupação (uso residencial comercial misto institucional), visualização interativa do relatório diretamente no navegador com tabelas e gráficos renderizados, opção de exportar relatório completo em formato PDF mantendo formatação visual e gráficos, opção alternativa de exportar dados brutos em Excel para análise customizada, inclusão de metadados no relatório (data de geração nome da comunidade período analisado), filtro opcional de período permitindo gerar relatório considerando apenas dados de intervalo temporal específico, e cache de relatórios gerados recentemente para agilizar acesso repetido. A rastreabilidade conecta esta user story ao RF-203 (Relatórios Gerenciais) UC-006 (Gerar Relatórios) e endpoint GET /api/reports/community-summary, garantindo visibilidade executiva sobre progresso e indicadores de cada comunidade atendida.

---

**Última atualização:** 2025-12-30
