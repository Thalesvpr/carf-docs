---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: compatibility
---

# US-015: Editar Unidade

Como analista cadastral, quero editar dados de unidade existente para que correções sejam aplicadas, onde o sistema permite modificar informações de unidades previamente cadastradas incluindo dados descritivos e geometria espacial, garantindo que erros possam ser corrigidos e informações possam ser atualizadas ao longo do ciclo de vida da unidade. O cenário principal de uso ocorre quando um analista identifica necessidade de correção ou atualização em uma unidade e acessa o formulário de edição onde todos os campos são preenchidos com valores atuais e podem ser modificados, permitindo alterações em qualquer campo exceto tenant_id que é imutável para garantir isolamento de dados entre tenants. Os critérios de aceitação incluem editabilidade de todos os campos da unidade com exceção explícita de tenant_id que permanece fixo como definido na criação, revalidação completa de geometria quando modificada incluindo verificação de sobreposições com outras unidades e validação de SRID, registro automático no histórico de alterações através do audit log capturando quem fez a mudança, quando foi feita, e valores antes e depois para cada campo alterado, e atualização automática do campo updated_at com timestamp da última modificação. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoints PUT /api/units/{id} para substituição completa e PATCH /api/units/{id} para atualização parcial) e GEOWEB (formulário de edição com pré-carga de dados existentes e mapa para edição de geometria), garantindo rastreabilidade com RF-054 (Edição de Unidades) e UC-001 (Caso de Uso de Gestão de Unidades), onde edições mantêm integridade referencial com holders e documentos vinculados, incluindo validações que previnem edições conflitantes quando múltiplos usuários trabalham na mesma unidade e notificações de mudanças para stakeholders relevantes.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Pronto
