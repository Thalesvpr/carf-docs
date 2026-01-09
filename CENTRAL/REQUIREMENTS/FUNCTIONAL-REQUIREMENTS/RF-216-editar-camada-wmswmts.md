---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# RF-216: Editar Camada WMS/WMTS

O sistema possibilita edição de configurações de serviços WMS/WMTS previamente cadastrados através de formulário dedicado que permite atualização de URL do servidor quando endpoint sofre mudanças, modificação de layers consumidos para adicionar ou remover camadas específicas oferecidas pelo serviço, ajuste de estilos aplicados quando servidor suporta múltiplos estilos de renderização, e alteração de parâmetros de exibição como opacidade, ordem de renderização e nome de apresentação. Todas as modificações submetidas passam por validação automática que testa conectividade com nova URL fornecida, verifica disponibilidade dos layers especificados através de requisição GetCapabilities atualizada, e confirma compatibilidade de sistemas de coordenadas, garantindo que alterações não resultem em camadas inoperantes que frustrariam usuários finais. O sistema mantém log detalhado de alterações incluindo timestamp de cada modificação, identificação do administrador responsável, campos alterados com valores antes e depois da mudança, e justificativa textual opcional que documenta motivação da alteração, proporcionando trilha de auditoria completa útil para troubleshooting quando camadas param de funcionar, atendimento a auditorias de conformidade e compreensão de evolução histórica das configurações do sistema ao longo do ciclo de vida do projeto.

---

**Última atualização:** 2025-12-30
