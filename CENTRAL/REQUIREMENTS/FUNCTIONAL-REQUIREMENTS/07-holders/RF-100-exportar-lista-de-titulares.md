---
modules: [GEOWEB]
epic: reliability
---

# RF-100: Exportar Lista de Titulares

O sistema deve permitir exportação de titulares cadastrados em formatos Excel e CSV facilitando análises externas, compartilhamento de dados com stakeholders e backup descentralizado de informações, onde exportação respeita filtros ativos na interface incluindo no arquivo apenas titulares visíveis conforme critérios de busca e filtragem aplicados. A exportação inclui todos os campos relevantes do cadastro de titulares como nome completo ou razão social, tipo (pessoa física ou jurídica), CPF ou CNPJ, RG, data de nascimento, contatos (telefone email), endereço completo e datas de criação e última atualização do registro, garantindo completude informacional do arquivo exportado. Para Excel, sistema gera planilha formatada com cabeçalhos em negrito, filtros automáticos habilitados e larguras de coluna ajustadas ao conteúdo facilitando manipulação imediata sem necessidade de formatação manual, além de incluir aba adicional com metadados da exportação (data filtros aplicados total de registros). Para CSV, utiliza codificação UTF-8 com BOM garantindo compatibilidade com Excel e sistemas diversos, aplicando delimitador apropriado (vírgula ou ponto-e-vírgula conforme locale) e escapamento correto de aspas e quebras de linha em campos de texto. Implementado nos módulos GEOWEB e GEOAPI com prioridade Should-have, este recurso viabiliza workflows externos que requeiram processamento de dados de titulares em ferramentas especializadas de análise ou integração com sistemas legados.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
