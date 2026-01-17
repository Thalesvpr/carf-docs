---
modules: [GEOWEB, REURBCAD]
epic: scalability
---

# UC-006-FE-002: Dados Insuficientes

Fluxo de exceção do UC-006 Gerar Relatório de Comunidade ocorrendo no passo 11.1 durante busca de dados quando worker executa query SELECT * FROM units WHERE community_id = $id AND created_at BETWEEN $start AND $end e retorna resultado vazio com rowCount = 0 indicando comunidade sem nenhuma unidade habitacional cadastrada no período selecionado, tipicamente acontecendo em comunidades recém-criadas ainda aguardando levantamento de campo ou quando período filtrado muito restrito (ex: última semana mas cadastros ocorreram mês anterior), sistema detecta ausência de dados verificando units.length === 0 antes de prosseguir para cálculos estatísticos que falhariam com divisão por zero ou agregações vazias, cancela job imediatamente marcando status failed com failedReason "NO_DATA" sem consumir recursos processando seções inúteis, envia notificação ao usuário via push ou email com ícone amarelo warning título "Relatório Não Gerado" mensagem específica "A comunidade 'Vila Nova' não possui unidades cadastradas no período selecionado (01/01/2025 a 31/01/2025). Verifique: (1) Se comunidade já teve levantamento de campo realizado, (2) Se período selecionado está correto, (3) Se unidades foram cadastradas em outra comunidade por engano" oferecendo ações Ajustar Período abrindo formulário com date_range expandido sugestão últimos 6 meses, Ver Todas as Comunidades listando communities do tenant ordenadas por total de unidades descendente permitindo identificar onde dados realmente estão, ou Cadastrar Primeira Unidade redirecionando para UC-001 iniciando processo de cadastro manual ou importação, exibe também estatística auxiliar na notificação mostrando "Comunidade possui 0 unidades no total (não apenas no período)" diferenciando caso de comunidade completamente vazia vs apenas filtro temporal inadequado orientando usuário sobre próxima ação correta, evitando confusão com relatórios vazios ou mensagens genéricas de erro que não explicam causa raiz.

**Ponto de Desvio:** Passo 11.1 do UC-006 (busca de dados retorna vazio)

**Retorno:** Job cancelado, usuário notificado com diagnóstico e sugestões de ação

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
