---
modules: [GEOWEB]
epic: units
---

# RF-035: Editar Comunidade

Usuários com role ADMIN podem editar dados de comunidades existentes onde atualização inclui modificação de nome tipo área população estimada e outros atributos alfanuméricos com validações garantindo integridade de dados obrigatórios, edição de geometria no mapa implementada através de ferramentas interativas permitindo adicionar/remover vértices mover polígono redimensionar ou redesenhar completamente boundary da comunidade com validações topológicas em tempo real alertando sobre polígonos inválidos (auto-intersecção buracos não permitidos), log automático de alterações registrando timestamp usuário responsável campos modificados valores anteriores e novos valores incluindo snapshot de geometria anterior se boundary foi alterado permitindo auditoria completa e rollback se necessário, implementação em módulos GEOWEB e GEOAPI com formulário de edição pré-carregado ferramentas de mapa integradas com bibliotecas como Leaflet ou OpenLayers validações síncronas e assíncronas confirmação de salvamento e opção de visualizar histórico de alterações.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
