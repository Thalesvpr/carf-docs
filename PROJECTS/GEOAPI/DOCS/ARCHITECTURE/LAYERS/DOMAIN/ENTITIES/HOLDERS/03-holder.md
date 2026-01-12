# Holder

Entidade representando titular posseiro pessoa física vinculado unidades habitacionais através relacionamento N:N armazenando dados pessoais documentação informações socioeconômicas necessárias processos regularização fundiária. Herda de BaseEntity fornecendo auditoria soft delete. Campos principais incluem CPF validado 11 dígitos verificadores garantindo unicidade tenant, dados pessoais completos (nome RG data nascimento estado civil nacionalidade), Email e PhoneNumber contato.

Dados socioeconômicos incluem renda mensal profissão número dependentes relevantes determinação modalidade REURB-S ou REURB-E conforme faixas renda. Relacionamento N:N com Unit via UnitHolder especificando tipo vínculo (PROPRIETARIO CONJUGE MORADOR PROCURADOR HERDEIRO) permitindo múltiplos titulares unidade e múltiplas unidades titular.

Suporta validações negócio CPF único tenant, campos obrigatórios emissão certidões LegitimationCertificate e regras legitimação fundiária Lei 13465/2017, além rastreamento quando por quem dados cadastrados atualizados através timestamps herdados BaseEntity.

---

**Última atualização:** 2026-01-12
