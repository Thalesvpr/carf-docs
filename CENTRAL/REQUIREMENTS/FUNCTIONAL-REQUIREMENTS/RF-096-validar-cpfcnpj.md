---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: security
---

# RF-096: Validar CPF/CNPJ

O sistema deve implementar validação algorítmica de CPF e CNPJ através de verificação de dígitos verificadores conforme regras matemáticas oficiais estabelecidas pela Receita Federal do Brasil, onde cálculo de módulo 11 é aplicado aos dígitos base gerando e comparando dígitos verificadores esperados com os informados. A validação ocorre no backend (server-side) garantindo segurança e impossibilidade de bypass, além de replicação no frontend (client-side) oferecendo feedback imediato ao usuário durante preenchimento sem necessidade de submeter formulário para descobrir que documento é inválido. Quando CPF ou CNPJ inválido é detectado, sistema apresenta mensagem de erro clara e específica indicando que número informado não é válido matematicamente, diferenciando este erro de outros tipos de validação (campo obrigatório formato incorreto duplicidade) para orientar usuário adequadamente na correção. A validação rejeita automaticamente CPFs e CNPJs conhecidamente inválidos como sequências repetidas (111.111.111-11) ou números reservados, além de aplicar regra de cálculo de dígitos verificadores que detecta transposições, omissões ou adulterações nos números. Implementado no módulo GEOAPI com prioridade Must-have, este requisito é fundamental para integridade do cadastro garantindo que apenas documentos válidos sejam aceitos, prevenindo erros de digitação e tentativas de cadastro com documentos fictícios ou incorretos.

---

**Última atualização:** 2025-12-30
