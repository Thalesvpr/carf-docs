---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-073: Exportar em Excel/CSV

Como gestor, quero exportar dados tabulares de unidades em formatos Excel (XLSX) ou CSV para que análise externa em ferramentas de planilha como Microsoft Excel Google Sheets ou scripts de processamento seja possível, onde a funcionalidade deve suportar ambos formatos XLSX e CSV com seleção pelo usuário, garantindo configuração de colunas exportadas permitindo escolher quais atributos incluir, permitindo aplicação de filtros ativos no momento da exportação e limitação de máximo 10.000 linhas por arquivo para controle de tamanho e performance. Esta funcionalidade é implementada pelo módulo GEOWEB com interface de exportação consumindo GEOAPI através do endpoint POST /api/exports?format=xlsx ou format=csv utilizando bibliotecas de geração de planilhas (EPPlus ClosedXML ou similar), integrada ao RF-199 (Exportação Excel/CSV) e UC-007 (Exportar Dados). Os critérios de aceitação incluem suporte a exportação em formato XLSX (Excel moderno) e CSV (texto delimitado por vírgula ou ponto-e-vírgula), interface de seleção de colunas permitindo marcar/desmarcar atributos específicos a incluir na exportação, aplicação automática de filtros e ordenação ativos no momento da exportação garantindo consistência com visualização atual, limite de 10.000 linhas por arquivo com alerta ao usuário se dataset completo exceder limite, formatação adequada de tipos de dados em Excel (números como numéricos datas como formato de data textos como texto), inclusão de cabeçalhos descritivos na primeira linha com nomes amigáveis das colunas, opção de escolher delimitador em CSV (vírgula ponto-e-vírgula tab) conforme padrão regional, encoding UTF-8 com BOM para garantir compatibilidade de caracteres especiais em Excel, geração assíncrona para datasets grandes com notificação quando arquivo estiver pronto, e download automático de arquivo gerado ou disponibilização de link temporário. A rastreabilidade conecta esta user story ao RF-199 (Exportação Tabular) UC-007 (Exportar Dados) e endpoint POST /api/exports com parâmetros de formato, garantindo interoperabilidade com ferramentas de análise tabular amplamente utilizadas.

---

**Última atualização:** 2025-12-30
