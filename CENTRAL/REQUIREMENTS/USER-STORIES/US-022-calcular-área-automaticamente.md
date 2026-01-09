---
modules: [GEOAPI, REURBCAD]
epic: units
---

# US-022: Calcular Área Automaticamente

Como sistema, quero calcular área da geometria automaticamente para que usuário não precise informar manualmente, onde o cálculo é executado de forma transparente sempre que uma geometria é criada ou modificada, garantindo precisão e consistência dos valores de área sem depender de entrada manual propensa a erros. O cenário principal de uso ocorre internamente no backend sempre que um endpoint de criação ou atualização de unidade recebe uma geometria, permitindo que antes de persistir o registro no banco de dados o sistema execute função espacial PostGIS para calcular a área real da geometria fornecida em metros quadrados e armazene este valor calculado no campo area da tabela de unidades. Os critérios de aceitação incluem execução automática da função ST_Area(geometry) do PostGIS sobre a geometria fornecida calculando área geodésica precisa, armazenamento do resultado em metros quadrados no campo area da entidade Unit garantindo que valor é sempre derivado da geometria real e não de entrada manual, e recálculo automático da área sempre que a geometria de uma unidade é editada mantendo sincronização perfeita entre geometria e área armazenada. Esta funcionalidade é implementada pelos módulos GEOAPI (trigger de banco de dados ou lógica de aplicação no repositório de unidades que invoca ST_Area antes de INSERT/UPDATE) e é transparente para GEOWEB que simplesmente exibe o valor calculado sem necessidade de entrada manual, garantindo rastreabilidade com RF-068 (Cálculo Automático de Área) e UC-001 (Caso de Uso de Gestão de Unidades), onde cálculos consideram projeção apropriada para medições precisas e valores são sempre consistentes com a geometria armazenada, incluindo validações que rejeitam geometrias com área zero ou negativa indicando problemas topológicos.

---

**Última atualização:** 2025-12-30