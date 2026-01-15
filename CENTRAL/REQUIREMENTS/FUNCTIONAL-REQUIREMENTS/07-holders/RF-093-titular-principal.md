---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: usability
---

# RF-093: Titular Principal

O sistema deve permitir marcação de um dos titulares vinculados a cada unidade como principal através de flag booleano is_primary na tabela associativa unit_holders, onde titular principal representa responsável prioritário para comunicações, notificações e apresentação em listagens que requeiram simplificação mostrando apenas um titular por unidade. A validação garante que apenas um titular pode ser marcado como principal por unidade (constraint de unicidade ou validação de aplicação), apresentando erro quando usuário tenta marcar segundo titular como principal sem desmarcar o atual, ou automaticamente removendo flag do anterior quando novo principal é selecionado conforme estratégia de UX adotada. A exibição de unidades em listagens, mapas e relatórios destaca titular principal através de posicionamento prioritário (primeiro da lista), formatação visual diferenciada (negrito ou ícone de estrela), ou apresentação exclusiva quando contexto requer simplificação e não comporta exibição de todos os titulares. Implementado no módulo GEOAPI com prioridade Should-have, este recurso facilita identificação rápida do responsável primário especialmente em unidades com múltiplos titulares onde listar todos pode sobrecarregar interfaces e dificultar localização de interlocutor principal para questões administrativas, notificações de aprovação ou comunicações sobre processos de regularização que requeiram contato com representante da unidade.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
