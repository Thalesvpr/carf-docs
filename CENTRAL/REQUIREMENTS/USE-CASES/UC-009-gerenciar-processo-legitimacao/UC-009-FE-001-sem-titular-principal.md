---
modules: [GEOWEB]
epic: holders
---

# UC-009-FE-001: Unidade sem Titular Principal

Fluxo de exceção do UC-009 Gerenciar Processo de Legitimação ocorrendo no passo 3 quando usuário clica botão Iniciar Processo de Legitimação mas sistema detecta que unidade não possui titular principal validando query SELECT COUNT(*) FROM unit_holders JOIN holders WHERE unit_id = $id AND is_primary = true retornando count = 0 indicando ausência de beneficiário designado como responsável principal pela unidade, tipicamente causado por cadastro incompleto onde FIELD_AGENT registrou unidade mas ainda não vinculou titulares aguardando coleta de documentos CPF RG em visita posterior, ou múltiplos titulares vinculados mas nenhum marcado como principal gerando ambiguidade sobre quem receberá título de legitimação, sistema bloqueia criação de processo exibindo modal vermelho erro com ícone de alerta título "Titular Principal Obrigatório" mensagem explicativa "Para iniciar processo de legitimação é necessário vincular um titular principal à unidade. O titular principal é quem receberá o título de legitimação fundiária" orientando sobre requisito legal e oferecendo botões Vincular Titular Agora redirecionando para UC-003 Vincular Titular a Unidade abrindo formulário pré-preenchido com unit_id permitindo buscar titular existente ou cadastrar novo e marcar checkbox É Titular Principal garantindo is_primary=true, ou Cancelar fechando modal e mantendo usuário na página de detalhes da unidade, se usuário opta por vincular completa fluxo UC-003 selecionando ou criando holder definindo relationship type ownership_percentage e marcando is_primary salvando registro em unit_holders, retorna automaticamente para detalhes da unidade agora exibindo titular principal na seção de titulares e botão Iniciar Processo de Legitimação habilitado permitindo prosseguir normalmente sem erro garantindo integridade de dados e conformidade com Lei 13.465 que exige identificação clara de beneficiário da regularização evitando processos inválidos que seriam indeferidos posteriormente por falta de qualificação adequada do interessado.

**Ponto de Desvio:** Passo 3 do UC-009 (validação ao clicar iniciar)

**Retorno:** Processo bloqueado, usuário vincula titular principal via UC-003

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
