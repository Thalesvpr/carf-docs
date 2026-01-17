---
modules: [GEOWEB]
epic: units
---

# RF-050: Editar Unidade

Usuários com roles ANALYST e MANAGER podem editar dados de unidades existentes onde edição de campos cadastrais permite atualização de endereço tipo área nomes de titulares documentos anexados e outros atributos alfanuméricos com validações garantindo integridade e conformidade com regras de negócio, edição de geometria no mapa utilizando ferramentas interativas permitindo mover redimensionar ou redesenhar completamente polígono da unidade com snap para features adjacentes validações topológicas em tempo real e recalculo automático de área após modificações geométricas, validação de permissões garante que usuários só editem unidades permitidas onde ANALYST pode editar apenas unidades em status DRAFT ou CHANGES_REQUESTED MANAGER pode editar unidades em qualquer status (exceto APPROVED final sem workflow de alteração) e verificação de tenant_id garante isolamento de dados, log automático de alterações registra todas modificações incluindo campos alterados valores anteriores/novos timestamp e usuário responsável preservando trilha de auditoria completa, implementação em módulos GEOWEB e GEOAPI com formulário de edição pré-carregado ferramentas de mapa integradas validações em tempo real e confirmação de salvamento com opção de visualizar histórico de alterações.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
