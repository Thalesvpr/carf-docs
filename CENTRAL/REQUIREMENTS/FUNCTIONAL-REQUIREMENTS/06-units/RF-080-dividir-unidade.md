---
modules: [GEOWEB]
epic: units
---

# RF-080: Dividir Unidade

O sistema deve permitir que administradores (perfil ADMIN) dividam uma unidade habitacional em múltiplas unidades através de desenho de linha divisória diretamente no mapa, onde ferramenta de split possibilita criação de polígonos resultantes a partir de partição geométrica da unidade original. A interface oferece ferramenta de desenho de linha onde usuário clica sequencialmente vértices definindo trajetória de corte que intersecta polígono da unidade original, aplicando operação de split geométrico (ST_Split) que resulta em dois ou mais polígonos correspondentes às novas unidades. Para cada polígono resultante, sistema cria automaticamente novo registro de unidade herdando atributos básicos da unidade original (tipo comunidade quadra) mas requerendo especificação de códigos únicos identificadores para cada nova unidade criada. Titulares da unidade original podem ser distribuídos entre novas unidades através de interface que permite seleção de quais titulares devem ser vinculados a cada unidade resultante, ou duplicação de todos os titulares em todas as novas unidades quando divisão física não implica divisão de responsabilidade, garantindo flexibilidade para diferentes cenários de subdivisão territorial ou regularização de ocupações que evoluíram de unidade única para múltiplas moradias.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
