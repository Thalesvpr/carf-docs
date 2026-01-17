---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: approval
---

# RF-056: Status de Unidade

O sistema deve implementar um fluxo de aprovação de unidades baseado em estados (DRAFT PENDING_APPROVAL APPROVED REJECTED CHANGES_REQUESTED), onde cada status representa uma etapa no processo de validação e cadastramento de unidades habitacionais. As transições entre status seguem regras específicas garantindo que apenas caminhos válidos sejam permitidos, incluindo restrição de que somente usuários com perfil MANAGER possam executar ações de aprovar ou rejeitar unidades pendentes. O sistema deve registrar automaticamente todas as mudanças de status em log de auditoria, capturando timestamp, usuário responsável, status anterior e novo, além de comentários ou justificativas fornecidos durante a transição. Este workflow é implementado no módulo GEOAPI através de máquina de estados e validadores de transição, garantindo rastreabilidade completa do ciclo de vida das unidades desde o rascunho inicial até a aprovação final, permitindo que gestores acompanhem o progresso do cadastramento e identifiquem gargalos no processo de validação.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
