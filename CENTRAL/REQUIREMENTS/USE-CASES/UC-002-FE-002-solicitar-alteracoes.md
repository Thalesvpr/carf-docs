---
modules: [GEOWEB, REURBCAD]
epic: scalability
---

# UC-002-FE-002: Solicitar Alterações

Fluxo de exceção do UC-002 Aprovar Unidade Habitacional desviando no passo 5 (revisão de informações) quando MANAGER durante inspeção de dados cadastrais geometria fotos e titulares identifica dados faltantes incorretos ou que requerem correção antes de aprovar, como endereço incompleto sem número ou complemento necessário, geometria desenhada grosseiramente com vértices visivelmente imprecisos não seguindo divisa real da propriedade, foto de baixa qualidade ou documento ilegível, titular principal sem CPF validado ou percentual de propriedade somando diferente de 100%, ou observações insuficientes em caso especial que requer documentação adicional, onde ao invés de aprovar diretamente MANAGER identifica necessidade de correção e clica em botão Solicitar Alterações abrindo modal com formulário estruturado para descrever alterações necessárias. Modal exibe textarea obrigatória rotulada "Descreva as alterações necessárias" com placeholder sugerindo formato claro "Por favor corrija: 1) Endereço está sem número, 2) Geometria precisa ser redesenhada seguindo divisa norte com mais precisão, 3) Anexar foto da fachada frontal" incentivando feedback específico acionável ao invés de comentário genérico "dados incorretos", opcionalmente exibe checklist pré-definida de problemas comuns (Endereço incompleto, Geometria imprecisa, Fotos faltando, Titulares incorretos, Documentação insuficiente) permitindo MANAGER marcar checkboxes relevantes que auto-populam textarea com template estruturado facilitando padronização, e campo select de prioridade (Normal Alta Urgente) indicando criticidade das correções solicitadas influenciando ordem na fila de revisões do criador. MANAGER preenche descrição detalhada das correções marca checkboxes aplicáveis se desejar usar template, seleciona prioridade conforme criticidade, e confirma clicando Enviar Solicitação disparando transação que atualiza status da unidade de Pending Approval para Requires Changes (ou Revision Required dependendo de nomenclatura do sistema), cria registro em tabela change_requests associado à unidade contendo requested_by (MANAGER AccountId), requested_at timestamp, description texto das alterações, priority prioridade selecionada, e status OPEN indicando pendente de resolução, adiciona entrada na timeline da unidade marcando evento CHANGES_REQUESTED visível para todos atores autorizados mostrando quem solicitou quando e descrição, dispara notificação ao criador original da unidade (AccountId que criou) enviando email com assunto "Alterações solicitadas para Unidade UH-123" corpo contendo descrição das correções link direto para editar unidade e prazo sugerido (configurável por tenant tipicamente 7 dias), e exibe toast de sucesso ao MANAGER "Solicitação enviada. Criador foi notificado" removendo unidade da lista de Pending Approval pois agora está em Requires Changes. Criador ao receber notificação acessa link que carrega tela de edição da unidade com banner destacado no topo exibindo descrição das alterações solicitadas e nome do MANAGER que solicitou, realiza correções nos campos indicados (edita endereço redesenha geometria anexa fotos adicionais corrige titulares), e ao salvar sistema automaticamente move status de Requires Changes de volta para Pending Approval re-inserindo unidade na fila de aprovação para novo review do MANAGER ou de outro MANAGER disponível, com timeline registrando que correções foram aplicadas permitindo MANAGER comparar estado anterior e posterior ao decidir aprovar finalmente.

**Ponto de Desvio:** Passo 5 do UC-002 (MANAGER revisa informações e identifica problema)

**Formulário de Solicitação:**
```markdown
### Descreva as alterações necessárias *

[Textarea obrigatória com mínimo 10 caracteres]

### Checklist de problemas comuns (opcional)
- [ ] Endereço incompleto (sem número, complemento, ou CEP)
- [ ] Geometria imprecisa (vértices fora da divisa real)
- [ ] Fotos faltando ou de baixa qualidade
- [ ] Titulares incorretos (CPF inválido, percentual errado)
- [ ] Documentação insuficiente (observações necessárias)

### Prioridade
( ) Normal  (•) Alta  ( ) Urgente
```

**Atualização de Status:**
```sql
BEGIN TRANSACTION;

-- Atualizar status da unidade
UPDATE units
SET status = 'Requires Changes',
    updated_at = NOW()
WHERE id = $1;

-- Criar registro de solicitação
INSERT INTO change_requests (
  unit_id,
  requested_by,
  requested_at,
  description,
  priority,
  status
) VALUES (
  $1, -- unit_id
  $2, -- manager_id
  NOW(),
  $3, -- description
  $4, -- priority
  'OPEN'
);

-- Adicionar à timeline
INSERT INTO unit_timeline (
  unit_id,
  event_type,
  actor_id,
  description,
  created_at
) VALUES (
  $1,
  'CHANGES_REQUESTED',
  $2,
  $3,
  NOW()
);

COMMIT;
```

**Notificação ao Criador:**
```
Assunto: Alterações solicitadas para Unidade UH-123

Olá [Nome do Criador],

O gestor [Nome do MANAGER] solicitou alterações na unidade UH-123 antes de aprovar:

[Descrição das alterações]

Por favor, acesse o link abaixo para realizar as correções:
[Link direto para edição]

Prazo sugerido: 7 dias

Equipe CARF
```

**Fluxo de Correção:**
1. Criador recebe email com descrição das alterações
2. Acessa link carregando tela de edição com banner destacando solicitação
3. Realiza correções nos campos indicados
4. Salva alterações
5. Sistema atualiza status Requires Changes → Pending Approval
6. Unidade retorna para fila de aprovação (pode ser outro MANAGER)
7. Timeline registra "Correções aplicadas pelo criador em DD/MM/YYYY"

**Retorno:** Unidade sai da lista Pending Approval, entra em Requires Changes aguardando correção

---

**Última atualização:** 2025-12-30
