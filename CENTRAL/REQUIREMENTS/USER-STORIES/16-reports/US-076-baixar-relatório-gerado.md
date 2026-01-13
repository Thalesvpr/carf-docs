---
modules: [GEOAPI, GEOWEB, GEOGIS]
epic: compatibility
---

# US-076: Baixar Relatório Gerado

Como gestor, quero acessar e baixar relatórios previamente gerados seja manualmente ou via agendamento automático para que acesso histórico a análises passadas seja fácil sem necessidade de regerar dados, onde a funcionalidade deve exibir lista de relatórios disponíveis organizados cronologicamente, garantindo filtros por tipo de relatório e intervalo de datas para localizar rapidamente relatório desejado, permitindo download direto de arquivo gerado com um click mantendo formato original (PDF Excel Shapefile). Esta funcionalidade é implementada pelo módulo GEOWEB com interface de biblioteca de relatórios consumindo GEOAPI através dos endpoints GET /api/reports para listar e GET /api/reports/{id}/download para obter arquivo, integrada ao UC-006 (Gerar Relatórios) para gestão de histórico de relatórios. Os critérios de aceitação incluem exibição de lista de relatórios gerados anteriormente ordenados por data de geração descendente (mais recentes primeiro), informações visíveis para cada relatório incluindo tipo nome da comunidade formato data_geração tamanho_arquivo e usuário_gerador, filtro por tipo de relatório permitindo mostrar apenas relatórios de comunidade exportações ou dashboards, filtro por intervalo de datas permitindo localizar relatórios gerados em período específico, indicação visual do formato de cada relatório através de ícone (PDF Excel Shapefile CSV), click direto em relatório ou botão "Download" iniciando download imediato do arquivo original, preview opcional de relatórios PDF diretamente no navegador antes de baixar, paginação ou scroll infinito para navegação eficiente em histórico extenso de relatórios, retenção configurável de relatórios com limpeza automática de arquivos antigos após período (exemplo 90 dias), e opção de excluir relatório manualmente se não for mais necessário. A rastreabilidade conecta esta user story ao UC-006 (Gerar Relatórios) e aos endpoints GET /api/reports e GET /api/reports/{id}/download, garantindo acesso conveniente a histórico completo de análises e exportações realizadas.

---

**Última atualização:** 2025-12-30
