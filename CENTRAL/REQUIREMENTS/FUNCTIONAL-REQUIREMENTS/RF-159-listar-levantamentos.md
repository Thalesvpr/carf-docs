---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: performance
---

# RF-159: Listar Levantamentos

Este requisito estabelece que o sistema deve fornecer endpoint e interface para listar levantamentos topográficos cadastrados permitindo navegação consulta e acesso a registros de trabalhos de campo realizados, onde listagem apresenta informações essenciais de cada levantamento de forma organizada e pesquisável. A interface deve implementar filtros por comunidade permitindo visualizar apenas levantamentos específicos de localidade selecionada útil em ambientes com múltiplas comunidades ou unidades territoriais onde usuário precisa focar em área geográfica particular, e filtro por data ou range de datas permitindo localizar levantamentos realizados em período específico através de seleção de data inicial e final ou presets como último mês último trimestre facilitando busca cronológica. O sistema deve implementar paginação robusta para cenários com grande volume de levantamentos registrados onde resultados são divididos em páginas de tamanho configurável tipicamente 20 a 50 registros incluindo controles de navegação e metadados de paginação como total de registros e páginas, garantindo performance adequada sem carregar dataset completo. Cada item da listagem deve exibir status do levantamento indicando se está em andamento concluído processado ou outro estado relevante através de badge ou indicador visual colorido, permitindo identificação rápida de levantamentos que requerem ação ou estão prontos para uso. A listagem deve incluir informações adicionais como data responsável comunidade e ações disponíveis. A funcionalidade deve estar disponível nos módulos GEOWEB e GEOAPI via endpoint GET.

---

**Última atualização:** 2025-12-30