---
modules: [GEOAPI, REURBCAD]
epic: performance
---

# US-028: Buscar Titular por CPF

Como analista, quero buscar titular por CPF para que eu evite duplicatas, onde o sistema fornece busca rápida e eficiente permitindo localizar titulares existentes através de CPF ou CNPJ antes de criar novos registros, garantindo que não sejam criadas entradas duplicadas para mesma pessoa e facilitando reuso de cadastros existentes. O cenário principal de uso ocorre quando analista está prestes a cadastrar novo titular e primeiro utiliza campo de busca para verificar se pessoa já está registrada digitando CPF ou CNPJ, permitindo que sistema retorne resultados instantaneamente mostrando titulares existentes com documento correspondente e oferecendo opção de vincular titular existente ao invés de criar duplicata. Os critérios de aceitação incluem campo de search que aceita busca por CPF ou CNPJ com ou sem formatação permitindo entrada flexível como 12345678900 ou 123.456.789-00, resultado instantâneo com tempo de resposta inferior a 300ms mesmo em base com milhares de titulares através de índices otimizados no banco de dados, listagem de holders existentes que possuem CPF ou CNPJ correspondente à busca mostrando nome completo e informações básicas para confirmação, e sugestão explícita de vincular titular existente quando busca retorna resultados evitando criação de duplicata e mantendo integridade dos dados. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint GET /api/holders?search={cpf} com query otimizada usando índices em campos de documento) e GEOWEB (componente de busca de titular com autocomplete e ações contextuais), garantindo rastreabilidade com RF-095 (Busca de Titulares por Documento) e UC-003 (Caso de Uso de Gestão de Titulares), onde busca normaliza entrada removendo formatação antes de comparar e considera apenas titulares ativos do mesmo tenant, incluindo destacamento visual de resultados exatos versus parciais e opções de criar novo titular quando busca não retorna resultados.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Review
