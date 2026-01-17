---
modules: [GEOAPI, GEOWEB, GEOGIS]
epic: audit
---

# RF-133: Editar Feature

Este requisito estabelece que usuários autorizados devem poder editar tanto geometria quanto atributos de features existentes permitindo correção e atualização de dados espaciais e descritivos, onde interface oferece modos separados para edição geométrica e alfanumérica. Para edição de geometria, o sistema deve fornecer modo de edição de vértices permitindo que usuário selecione feature e manipule seus pontos de controle, onde vértices são apresentados como handles arrastáveis e usuário pode mover vértices existentes adicionar novos através de clique no meio de segmentos ou remover através de interação apropriada. Para edição de atributos, o sistema deve apresentar formulário populado com valores atuais das propriedades da feature permitindo modificação de campos individuais conforme schema da camada, onde validações de tipo e obrigatoriedade são aplicadas antes de aceitar mudanças. Todas as alterações realizadas devem gerar entradas no log de auditoria registrando usuário responsável timestamp campos modificados e valores anteriores versus novos, garantindo rastreabilidade completa de evolução dos dados e permitindo investigação de mudanças ou reversões se necessário. O sistema deve implementar validação de geometria após edição garantindo que feature modificada continua válida conforme regras GIS antes de persistir. A funcionalidade deve estar disponível nos módulos GEOWEB através de ferramentas de edição interativas e GEOAPI via endpoint PATCH.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
