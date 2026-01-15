---
modules: [GEOWEB, REURBCAD]
epic: other
---

# RF-136: Atributos Customizados de Features

Este requisito especifica que cada feature deve suportar conjunto flexível de atributos customizados definidos conforme necessidades específicas de cada camada ao invés de schema rígido pré-determinado, onde propriedades são armazenadas em estrutura JSON permitindo extensibilidade sem alterações de schema de banco. O modelo de dados deve incluir campo properties do tipo JSONB no PostgreSQL armazenando objeto JSON com pares chave-valor representando atributos da feature, onde JSONB permite indexação eficiente queries sobre propriedades individuais e validação de estrutura. Cada camada deve poder definir schema de atributos configurável especificando quais campos estão disponíveis para features daquela layer incluindo nome do campo tipo de dado esperado texto número data booleano enum e se campo é obrigatório ou opcional, permitindo que administradores customizem modelo de dados conforme domínio específico sem programação. O sistema deve implementar validação de tipos ao criar ou editar features garantindo que valores fornecidos correspondem aos tipos declarados no schema da camada, onde validação rejeita submissões com tipos incorretos ou campos obrigatórios ausentes fornecendo mensagens de erro claras. A interface deve gerar formulários dinâmicos baseados no schema configurado apresentando controles apropriados para cada tipo de campo. A funcionalidade é implementada no módulo GEOAPI através de validações e modelo de dados flexível.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
