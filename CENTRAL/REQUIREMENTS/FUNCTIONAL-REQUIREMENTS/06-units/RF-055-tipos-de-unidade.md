---
modules: [GEOAPI]
epic: other
---

# RF-055: Tipos de Unidade

O sistema deve suportar a categorização de unidades habitacionais através de tipos predefinidos (RESIDENCIAL COMERCIAL MISTO INSTITUCIONAL EQUIPAMENTO_PUBLICO), onde cada tipo representa o uso predominante da edificação e influencia regras de validação e apresentação de dados. A implementação utiliza uma enumeração (enum) no backend garantindo valores consistentes e evitando erros de digitação, incluindo validação automática ao criar ou editar unidades para aceitar somente tipos válidos do conjunto predefinido. O sistema oferece filtros por tipo nas listagens e consultas de unidades, permitindo que usuários visualizem e exportem dados agrupados por categoria de uso, facilitando análises demográficas e planejamento urbano. Este requisito é essencial para GEOAPI onde os tipos de unidade são utilizados em relatórios estatísticos, mapas temáticos e regras de negócio específicas para cada categoria, garantindo que a classificação seja uniforme em toda a plataforma e compartilhada entre diferentes módulos do sistema.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
