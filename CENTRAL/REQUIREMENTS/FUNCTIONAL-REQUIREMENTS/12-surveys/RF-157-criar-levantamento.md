---
modules: [GEOWEB, REURBCAD]
epic: reliability
---

# RF-157: Criar Levantamento

Este requisito estabelece que usuários autorizados devem poder criar registros de levantamento topográfico no sistema documentando trabalhos de campo e medições realizadas incluindo metadados descritivos e arquivos brutos de dados coletados, onde levantamentos são entidades que organizam informação sobre atividades de mapeamento e coleta de dados geoespaciais. O sistema deve fornecer formulário de criação com campos para data de realização do levantamento permitindo registro cronológico preciso, responsável técnico identificando profissional que conduziu trabalho para rastreabilidade e responsabilização, e equipamento utilizado documentando instrumentos de medição como estação total GPS RTK ou drone para contexto sobre precisão e metodologia empregada. O formulário deve permitir vinculação do levantamento a comunidade ou unidade territorial específica estabelecendo escopo geográfico e contexto administrativo do trabalho realizado, onde associação facilita organização e recuperação de levantamentos por localidade. O sistema deve suportar upload de arquivo bruto contendo dados coletados em campo em formatos diversos como .raw .txt .csv ou outros formatos proprietários de equipamentos topográficos, onde arquivo é armazenado em object storage vinculado ao registro de levantamento permitindo acesso posterior para processamento análise ou auditoria. Os metadados e arquivo devem ser validados durante criação e registro completo persistido no banco. A funcionalidade deve estar disponível nos módulos GEOWEB para entrada de dados, REURBCAD para criação mobile em campo, e GEOAPI para persistência.

---

**Última atualização:** 2025-12-30