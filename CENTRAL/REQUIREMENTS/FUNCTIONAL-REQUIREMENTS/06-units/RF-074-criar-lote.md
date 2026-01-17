---
modules: [GEOWEB]
epic: units
---

# RF-074: Criar Lote

O sistema deve permitir que usuários criem lotes representando subdivisões dentro de quadras, onde lote é uma unidade territorial intermediária entre quadra e unidade habitacional utilizada em contextos de parcelamento formal ou planejado. O formulário de criação captura código identificador único do lote, área em metros quadrados e geometria espacial representando o polígono delimitador da parcela, além de vinculação obrigatória a uma quadra existente estabelecendo hierarquia comunidade-quadra-lote-unidade. A geometria do lote deve estar contida dentro da geometria da quadra associada quando ambas estiverem definidas, garantindo consistência espacial hierárquica através de validação automática que alerta sobre lotes que extrapolam limites da quadra parente. Este recurso é implementado nos módulos GEOWEB e GEOAPI com prioridade Could-have indicando uso opcional dependente de contexto específico de projeto, sendo essencial em regularizações fundiárias com parcelamento formal mas dispensável em cadastros de ocupações informais onde conceito de lote pode não se aplicar, oferecendo flexibilidade para adaptar modelo de dados à realidade territorial de cada implementação.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
