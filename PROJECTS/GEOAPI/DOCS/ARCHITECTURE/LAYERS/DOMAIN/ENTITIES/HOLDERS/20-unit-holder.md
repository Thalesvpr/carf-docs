# UnitHolder

Entidade representando relacionamento N:N entre Unit e Holder vinculando titular unidade habitacional com tipo vínculo percentual propriedade permitindo múltiplos titulares unidade e múltiplas unidades titular. Herda de BaseEntity fornecendo auditoria temporal. Campos principais incluem UnitId Guid FK, HolderId Guid FK, HolderType string (PROPRIETARIO CONJUGE MORADOR PROCURADOR HERDEIRO), OwnershipPercentage decimal nullable 0-100 aplicável apenas PROPRIETARIO permitindo copropriedade e IsPrimary bool titular principal responsável legal.

Campos auditoria incluem LinkedAt DateTime quando vínculo estabelecido e LinkedBy Guid FK Account que criou. Métodos incluem ValidateOwnership() verificando PROPRIETARIO requer OwnershipPercentage preenchido entre 0.01-100 lançando ValidationException, IsPrimaryOwner() verificando IsPrimary e PROPRIETARIO, CalculateTotalOwnership() estático validando soma não ultrapassa 100% e SetAsPrimary() desmarcando outros garantindo único primary.

Regra negócio Unit deve ter ao menos um Holder vinculado, PROPRIETARIO requer OwnershipPercentage, soma proprietários não ultrapassa 100% mas pode ser menor se parcialmente documentada. Integra Unit.LinkHolder()/UnlinkHolder() gerenciando coleção, participa validações LegitimationRequest onde apenas PROPRIETARIO contribui cálculo área legitimável e suporta transferência propriedade criando novos soft deleting antigos preservando histórico titularidade.

---

**Última atualização:** 2026-01-12
