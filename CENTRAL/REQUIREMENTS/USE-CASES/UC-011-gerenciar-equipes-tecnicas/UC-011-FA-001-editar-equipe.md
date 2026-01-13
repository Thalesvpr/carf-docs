---
modules: [GEOAPI, GEOWEB]
epic: compatibility
---

# UC-011-FA-001: Editar Equipe Existente

Fluxo alternativo do UC-011 Gerenciar Equipes Técnicas desviando no passo 3 onde ao invés de clicar + Nova Equipe, usuário clica ícone editar (lápis) em equipe existente na listagem disparando abertura de formulário modal pré-preenchido com dados atuais carregados via GET /api/teams/{id} incluindo name description leader_id status permitindo modificação, usuário altera nome corrigindo typo ou refletindo mudança organizacional, atualiza descrição adicionando detalhes sobre escopo ampliado, troca líder selecionando outro usuário do dropdown devido transferência de responsabilidade promoção ou saída do líder anterior, ou altera status de Ativa para Inativa arquivando equipe não mais operacional, clica Salvar Alterações executando validação nome único excluindo própria equipe da verificação WHERE name = $name AND id != $current_id evitando falso positivo, líder selecionado válido e ativo, se validação passa executa UPDATE teams SET name=$name description=$description leader_id=$leader status=$status updated_by=$user_id updated_at=NOW() WHERE id=$id, registra auditoria em audit_log com action=TEAM_UPDATED details JSON contendo changed_fields comparando valores antigos vs novos, envia notificação ao novo líder se alterado informando designação, exibe toast verde "Equipe atualizada com sucesso" fecha modal e atualiza listagem refletindo mudanças imediatamente.

**Ponto de Desvio:** Passo 3 do UC-011 (clicar editar ao invés de novo)

**Retorno:** Equipe atualizada, listagem refreshed

---

**Última atualização:** 2025-12-30
