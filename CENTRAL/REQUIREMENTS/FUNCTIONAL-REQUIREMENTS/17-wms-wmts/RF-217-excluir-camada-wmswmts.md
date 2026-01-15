---
modules: [GEOWEB]
epic: usability
---

# RF-217: Excluir Camada WMS/WMTS

O sistema permite remoção de serviços WMS/WMTS configurados através de operação de soft delete que marca registro como excluído sem remover fisicamente dados do banco, preservando histórico de configurações e permitindo restauração futura se necessário, além de manter integridade referencial com logs de auditoria e registros de uso que referenciam camada removida. Antes de executar exclusão, o sistema apresenta diálogo de confirmação obrigatória que alerta administrador sobre ação e lista potenciais impactos como número de usuários que atualmente visualizam a camada, dependências em dashboards ou relatórios customizados, e impossibilidade de desfazer operação sem intervenção de suporte técnico, prevenindo remoções acidentais de serviços críticos que causariam interrupção de trabalho para múltiplos usuários. Ao confirmar exclusão, a camada é imediatamente removida do seletor de camadas disponível aos usuários finais em todas as instâncias ativas do aplicativo através de atualização em tempo real via WebSocket ou polling periódico, garantindo que tentativas de visualizar camada inexistente não ocorram e proporcionando consistência imediata entre configuração administrativa e experiência do usuário. Administradores podem consultar lista de camadas excluídas através de filtro específico na interface de listagem, permitindo revisão de histórico de remoções, identificação de exclusões incorretas e eventualmente restauração de configurações através de operação de undelete acessível apenas a perfis super_admin com privilégios elevados de administração de sistema.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
