---
modules: [GEOWEB]
epic: communities
---

# RF-042: Timeline de Comunidade

Interface deve exibir histórico cronológico de alterações da comunidade onde linha do tempo visual apresenta eventos em ordem cronológica reversa (mais recentes primeiro) com representação gráfica intuitiva usando ícones marcadores e conexões visuais, eventos registrados incluem criação inicial da comunidade edições de dados alfanuméricos modificações de geometria (boundary) aprovações de unidades vinculadas desativação/reativação anexação de documentos e outras operações relevantes capturando evolução completa, cada evento exibe usuário responsável pela ação com avatar ou iniciais timestamp preciso com data e hora descrição textual da modificação e opcionalmente link para visualizar detalhes completos ou comparação de valores antes/depois, implementação em módulo GEOWEB consumindo dados de tabela de auditoria ou event sourcing store do GEOAPI com componente de timeline responsivo suportando filtros por tipo de evento período temporal usuário responsável e expansão de detalhes inline.

---

**Última atualização:** 2025-12-30
