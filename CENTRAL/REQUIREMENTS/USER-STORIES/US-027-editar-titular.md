---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: compatibility
---

# US-027: Editar Titular

Como analista, quero editar dados de titular para que correções sejam aplicadas, onde o sistema permite modificar informações de titulares previamente cadastrados garantindo que erros possam ser corrigidos e dados mantidos atualizados ao longo do tempo, preservando integridade referencial com unidades vinculadas e rastreabilidade de mudanças. O cenário principal de uso ocorre quando um analista identifica necessidade de atualizar informações de um titular e acessa formulário de edição preenchido com dados atuais, permitindo modificar qualquer campo como nome, documentos ou endereço e submeter as alterações que serão validadas e persistidas mantendo vínculos existentes com unidades. Os critérios de aceitação incluem editabilidade de todos os campos do titular permitindo correção de qualquer informação previamente cadastrada incluindo dados pessoais e documentos, revalidação completa de CPF/CNPJ quando estes campos são modificados aplicando mesmas regras de validação de formato e dígitos verificadores usadas na criação, e atualização automática do audit log registrando quem fez a edição, quando foi realizada, e quais campos foram alterados com valores antes e depois para rastreabilidade completa. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint PUT /api/holders/{id} com validações e registro de auditoria) e GEOWEB (formulário de edição de titular com pré-carga de dados existentes), garantindo rastreabilidade com RF-085 (Edição de Titulares) e UC-003 (Caso de Uso de Gestão de Titulares), onde edições não afetam vínculos existentes com unidades mas são refletidas imediatamente em todas as visualizações, incluindo validações de unicidade de CPF/CNPJ excluindo o próprio registro sendo editado e notificações de mudança para administradores quando documentos identificadores são alterados.

---

**Última atualização:** 2025-12-30