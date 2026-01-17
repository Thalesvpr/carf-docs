---
modules: [GEOWEB]
epic: units
---

# RF-099: Listar Unidades de um Titular

O sistema deve apresentar lista completa de todas as unidades habitacionais vinculadas a um titular específico, onde visualização mostra código da unidade, endereço, comunidade, tipo de relacionamento do titular com a unidade (proprietário possuidor locatário etc) e status atual da unidade (draft pending approved rejected). A listagem permite identificação rápida de titulares com múltiplas propriedades ou posses facilitando análises de concentração fundiária, detecção de possíveis irregularidades como mesmo titular em unidades distantes geograficamente sugerindo cadastros duplicados, ou simplesmente navegação entre propriedades de mesma pessoa durante processos de regularização. A interface oferece filtros por tipo de relacionamento e status permitindo segmentação como "mostrar apenas unidades onde titular é proprietário e status é aprovado" focalizando análise em subconjunto específico de vínculos relevantes ao contexto. Cada item da lista é clicável navegando diretamente para visualização detalhada da unidade correspondente, criando navegação fluida entre cadastro de titular e unidades associadas através de links bidirecionais que facilitam exploração relacional da base de dados. Implementado nos módulos GEOWEB e GEOAPI com prioridade Should-have, este recurso é essencial para compreensão completa do portfolio de cada titular e detecção de padrões que possam indicar necessidade de intervenções específicas ou validações adicionais.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
