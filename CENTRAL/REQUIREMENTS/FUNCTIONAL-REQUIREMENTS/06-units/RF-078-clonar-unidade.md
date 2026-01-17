---
modules: [GEOWEB]
epic: units
---

# RF-078: Clonar Unidade

O sistema deve permitir que usuários clonem unidades habitacionais existentes criando cópia com todos os campos alfanuméricos e relacionamentos (exceto código identificador que deve ser único), onde geometria clonada é automaticamente deslocada 5 metros em direção nordeste evitando sobreposição exata com unidade original. A funcionalidade gera novo código único automaticamente seguindo padrão configurado para o tenant ou incrementando sequencialmente código da unidade original, garantindo que clone possua identificador válido e único sem intervenção manual do usuário. O clone herda tipo de unidade, comunidade, quadra, lote (se aplicável), campos customizados e valores de todos os atributos exceto campos de auditoria (created_at updated_at created_by) que refletem criação do clone como novo registro independente. Implementado nos módulos GEOWEB e GEOAPI com prioridade Could-have, este recurso otimiza cadastramento de edificações similares ou geminadas onde múltiplas unidades compartilham características comuns, permitindo duplicação rápida e ajuste incremental ao invés de preenchimento completo de formulário repetidas vezes, aumentando produtividade especialmente em contextos de conjuntos habitacionais padronizados ou vilas com características uniformes.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
