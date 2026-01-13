---
modules: [GEOGIS]
epic: maintainability
---

# RF-166: Exportar Levantamento

O sistema disponibiliza funcionalidade de exportação de dados de levantamento topográfico em múltiplos formatos técnicos amplamente utilizados em engenharia e agrimensura, incluindo CSV para dados tabulares de coordenadas, DXF para intercâmbio com softwares CAD como AutoCAD e Shapefile para integração com sistemas GIS desktop. Durante o processo de exportação, o sistema inclui automaticamente metadados essenciais como sistema de coordenadas utilizado, datum de referência, data de coleta, responsável técnico pelo levantamento e identificadores do projeto, garantindo rastreabilidade e conformidade com normas técnicas de documentação geodésica. Antes da geração dos arquivos, o sistema executa rotinas de validação que verificam consistência geométrica dos dados, completude de atributos obrigatórios e integridade referencial entre pontos e features derivadas, prevenindo exportação de dados incompletos ou inconsistentes que poderiam comprometer análises posteriores ou processos de intercâmbio com órgãos reguladores. Os arquivos exportados mantêm estrutura compatível com especificações técnicas de cada formato, facilitando importação em outros sistemas sem necessidade de conversões adicionais ou ajustes manuais.

---

**Última atualização:** 2025-12-30
