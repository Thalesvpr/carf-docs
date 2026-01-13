---
modules: [GEOWEB]
epic: performance
---

# RF-088: Tipos de Titular

O sistema deve suportar categorização de titulares em tipos predefinidos (PESSOA_FISICA PESSOA_JURIDICA) através de enumeração que garante valores consistentes e possibilita renderização condicional de campos específicos conforme tipo selecionado. Quando tipo é PESSOA_FISICA, formulário exibe e requer campos como CPF, RG, data de nascimento, gênero e estado civil, ocultando campos específicos de pessoa jurídica que não se aplicam a indivíduos. Quando tipo é PESSOA_JURIDICA, formulário apresenta campos como CNPJ, inscrição estadual, razão social, nome fantasia e representante legal, escondendo campos exclusivos de pessoa física para manter interface limpa e relevante ao contexto. A validação de documento (CPF ou CNPJ) é aplicada condicionalmente baseada no tipo selecionado, onde algoritmo correto de verificação de dígitos é utilizado conforme natureza do documento garantindo que pessoas físicas não possam ser cadastradas com CNPJ e vice-versa. Implementado no módulo GEOAPI com prioridade Must-have, este requisito é essencial para modelagem adequada de diferentes naturezas jurídicas de titulares, onde empresas, associações e pessoas físicas coexistem como responsáveis por unidades em contextos diversos de regularização fundiária e cadastramento territorial.

---

**Última atualização:** 2025-12-30
