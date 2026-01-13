---
modules: [GEOWEB]
epic: security
---

# UC-009-FE-003: Processo Indeferido

Fluxo de exceção do UC-009 Gerenciar Processo de Legitimação desviando no passo 13.4 quando MANAGER ao revisar processo detecta impedimento legal ou documentação insuficiente não corrigível impossibilitando aprovação conforme Lei 13.465 e decide indeferir clicando botão Indeferir, sistema exibe modal vermelho crítico com título "Indeferir Processo" e textarea obrigatória para Justificativa Legal exigindo mínimo 50 caracteres descrevendo motivo específico de indeferimento como "Beneficiário não comprovou tempo mínimo de posse conforme Art. 23 Lei 13.465 (requer 5 anos ininterruptos, documentação apresentada comprova apenas 2 anos)" ou "Área da unidade excede limite de 250m² estabelecido para REURB-S conforme Art. 13 §1º impossibilitando enquadramento como interesse social", validação impede submissão se justificativa vazia ou genérica exigindo fundamentação adequada para auditoria e transparência, MANAGER preenche justificativa detalhada clica Confirmar Indeferimento executando transação UPDATE legitimation_processes SET status='INDEFERIDO' deferred_by=$manager_id deferred_at=NOW() deferred_reason=$justificativa archived=true impedindo edições futuras via constraint ou trigger verificando archived=true rejeitando UPDATEs preservando integridade histórica, sistema registra entrada em process_timeline table com action=INDEFERIDO actor=MANAGER timestamp e reason para auditoria completa rastreando decisões administrativas, envia notificação automática ao ANALYST criador do processo via email e push mostrando "Processo LEGITIM-2025-00123 foi indeferido" com justificativa completa transcrita permitindo entender motivo, processo movido para aba Arquivados na listagem com badge vermelho INDEFERIDO visualmente destacado, interface bloqueia totalmente edição desabilitando todos botões e campos marcando formulário como readonly evitando tentativas de reabertura ou modificação que violariam decisão administrativa documentada, se beneficiário desejar nova tentativa após corrigir impedimentos (ex: aguardar completar 5 anos de posse, subdividir lote reduzindo área) ANALYST deve criar novo processo separado iniciando UC-009 novamente do zero com número diferente mantendo processo original indeferido como histórico comprovando tentativa anterior e evolução temporal da situação fundiária, decisão de indeferimento possui efeito permanente conforme RN-003 garantindo segurança jurídica e impedindo manipulação retroativa de registros administrativos que poderia gerar responsabilização de gestor por irregularidades em processos de legitimação fundiária que envolvem transferência de patrimônio público para particulares exigindo controle rigoroso e transparência total.

**Ponto de Desvio:** Passo 13.4 do UC-009 (MANAGER escolhe indeferir)

**Retorno:** Processo arquivado definitivamente, notificação enviada, novo processo requerido se necessário

---

**Última atualização:** 2025-12-30
