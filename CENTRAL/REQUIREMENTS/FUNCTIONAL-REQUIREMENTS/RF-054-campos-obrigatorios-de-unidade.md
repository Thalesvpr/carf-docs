---
modules: [GEOAPI, REURBCAD]
epic: units
---

# RF-054: Campos Obrigatórios de Unidade

O sistema deve validar obrigatoriamente os campos essenciais ao cadastrar ou editar uma unidade habitacional, incluindo código único de identificação, endereço completo, comunidade à qual pertence, geometria espacial (coordenadas geográficas) e tipo de uso da unidade, onde cada campo possui validação específica no backend garantindo integridade dos dados. A validação ocorre tanto no momento do preenchimento quanto antes do salvamento, apresentando mensagens de erro claras e específicas para cada campo inválido ou ausente, permitindo que o usuário corrija os problemas identificados antes de prosseguir. Caso algum campo obrigatório não seja preenchido ou contenha dados inválidos, o sistema deve bloquear o salvamento do registro e destacar visualmente os campos problemáticos, garantindo que nenhuma unidade seja cadastrada com informações incompletas ou inconsistentes. Este requisito é implementado no módulo GEOAPI através de validadores de modelo e middleware de validação de requisições, onde as regras de negócio são centralizadas e aplicadas uniformemente em todas as operações de criação e atualização de unidades.

---

**Última atualização:** 2025-12-30
