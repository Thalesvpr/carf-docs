---
modules: [GEOWEB]
epic: units
---

# RF-071: Editar Quadra

O sistema deve permitir que usuários editem dados cadastrais de quadras existentes, onde interface oferece atualização de campos alfanuméricos (código nome comunidade) através de formulário padrão e edição de geometria espacial através de ferramentas interativas de mapa. A edição de geometria permite ajuste de vértices do polígono delimitador da quadra garantindo que contorno reflita com precisão a área ocupada pelo agrupamento de unidades, incluindo operações de adicionar, mover ou remover vértices de forma fluida e intuitiva. Todas as alterações realizadas são automaticamente registradas em log de auditoria capturando timestamp, usuário responsável, campos modificados e valores anteriores e novos, garantindo rastreabilidade completa do histórico de mudanças ao longo do ciclo de vida da quadra. A edição respeita regras de validação incluindo unicidade de códigos, consistência de vínculos com comunidade e unidades, e integridade geométrica quando geometria está definida, onde sistema apresenta mensagens claras sobre violações de regras bloqueando salvamento até que dados sejam corrigidos conforme requisitos de negócio.

---

**Última atualização:** 2025-12-30
