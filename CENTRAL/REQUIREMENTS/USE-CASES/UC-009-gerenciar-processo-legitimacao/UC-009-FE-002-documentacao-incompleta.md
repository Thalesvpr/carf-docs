---
modules: [GEOWEB]
epic: reliability
---

# UC-009-FE-002: Documentação Incompleta

Fluxo de exceção do UC-009 Gerenciar Processo de Legitimação ocorrendo no passo 12 quando usuário tenta submeter processo para aprovação clicando botão Submeter mas sistema detecta que checklist de documentos obrigatórios está incompleta verificando count de process_documents WHERE process_id = $id comparando com expected_documents baseado em tipo de legitimação retornando mismatch indicando documentos faltantes, sistema identifica especificamente quais itens estão pendentes iterando checklist e verificando cada document_type possui uploaded=true marcado, bloqueia submissão exibindo modal amarelo warning com ícone de exclamação título "Documentos Obrigatórios Pendentes" mensagem listando items faltantes com bullets destacados em vermelho como "• Comprovante de Residência (obrigatório), • Memorial Descritivo (obrigatório)" orientando claramente o que precisa ser anexado, exibe botão Completar Checklist fechando modal e mantendo foco na seção de documentos com scroll automático para primeiro item pendente destacado com borda vermelha pulsante chamando atenção visual, usuário clica em item faltante faz upload de arquivo PDF ou imagem sistema valida salva marca como concluído exibindo checkmark verde, repete para todos items pendentes até checklist 100% completa verificando visualmente todos checkmarks verdes, botão Submeter para Aprovação agora habilitado com cor destacada permitindo clicar, ao clicar com checklist completo validação passa atualizando status sem erro prosseguindo fluxo normal enviando notificação ao MANAGER, prevenindo situação de MANAGER receber processo para revisão mas não conseguir analisar por falta de documentação essencial que resultaria em devolução imediata para correções desperdiçando tempo e atrasando workflow, força ANALYST verificar completude antes de submeter garantindo qualidade mínima e eficiência do processo de aprovação mantendo SLA de análise dentro de prazo razoável.

**Ponto de Desvio:** Passo 12 do UC-009 (tentativa de submeter com docs faltando)

**Retorno:** Submissão bloqueada, usuário completa checklist e retenta

---

**Última atualização:** 2025-12-30
