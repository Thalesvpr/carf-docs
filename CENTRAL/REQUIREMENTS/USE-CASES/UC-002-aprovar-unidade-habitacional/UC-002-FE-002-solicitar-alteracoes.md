---
modules: [GEOWEB, REURBCAD]
epic: scalability
---

# UC-002-FE-002: Solicitar Alterações

Fluxo de exceção do UC-002 Aprovar Unidade Habitacional desviando no passo 5 (revisão de informações) quando MANAGER durante inspeção de dados cadastrais geometria fotos e titulares identifica dados faltantes incorretos ou que requerem correção antes de aprovar, como endereço incompleto sem número ou complemento necessário, geometria desenhada grosseiramente com vértices visivelmente imprecisos não seguindo divisa real da propriedade, foto de baixa qualidade ou documento ilegível, titular principal sem CPF validado ou percentual de propriedade somando diferente de 100%, ou observações insuficientes em caso especial que requer documentação adicional, onde ao invés de aprovar diretamente MANAGER identifica necessidade de correção e clica em botão Solicitar Alterações abrindo modal com formulário estruturado para descrever alterações necessárias. Modal exibe textarea obrigatória rotulada "Descreva as alterações necessárias" com placeholder sugerindo formato claro "Por favor corrija: 1) Endereço está sem número, 2) Geometria precisa ser redesenhada seguindo divisa norte com mais precisão, 3) Anexar foto da fachada frontal" incentivando feedback específico acionável ao invés de comentário genérico "dados incorretos", opcionalmente exibe checklist pré-definida de problemas comuns (Endereço incompleto, Geometria imprecisa, Fotos faltando, Titulares incorretos, Documentação insuficiente) permitindo MANAGER marcar checkboxes relevantes que auto-populam textarea com template estruturado facilitando padronização, e campo select de prioridade (Normal Alta Urgente) indicando criticidade das correções solicitadas influenciando ordem na fila de revisões do criador. MANAGER preenche descrição detalhada das correções marca checkboxes aplicáveis se desejar usar template, seleciona prioridade conforme criticidade, e confirma clicando Enviar Solicitação disparando transação que atualiza status da unidade de Pending Approval para Requires Changes (ou Revision Required dependendo de nomenclatura do sistema), cria registro em tabela change_requests associado à unidade contendo requested_by (MANAGER AccountId), requested_at timestamp, description texto das alterações, priority prioridade selecionada, e status OPEN indicando pendente de resolução, adiciona entrada na timeline da unidade marcando evento CHANGES_REQUESTED visível para todos atores autorizados mostrando quem solicitou quando e descrição, dispara notificação ao criador original da unidade (AccountId que criou) enviando email com assunto "Alterações solicitadas para Unidade UH-123" corpo contendo descrição das correções link direto para editar unidade e prazo sugerido (configurável por tenant tipicamente 7 dias), e exibe toast de sucesso ao MANAGER "Solicitação enviada. Criador foi notificado" removendo unidade da lista de Pending Approval pois agora está em Requires Changes. Criador ao receber notificação acessa link que carrega tela de edição da unidade com banner destacado no topo exibindo descrição das alterações solicitadas e nome do MANAGER que solicitou, realiza correções nos campos indicados (edita endereço redesenha geometria anexa fotos adicionais corrige titulares), e ao salvar sistema automaticamente move status de Requires Changes de volta para Pending Approval re-inserindo unidade na fila de aprovação para novo review do MANAGER ou de outro MANAGER disponível, com timeline registrando que correções foram aplicadas permitindo MANAGER comparar estado anterior e posterior ao decidir aprovar finalmente.

**Ponto de Desvio:** Passo 5 do UC-002 (MANAGER revisa informações e identifica problema)

**Formulário de Solicitação:**

Modal exibe seção "Descreva as alterações necessárias" com asterisco indicando obrigatória contendo textarea com validação mínimo dez caracteres, seção opcional "Checklist de problemas comuns" com checkboxes marcáveis incluindo "Endereço incompleto (sem número, complemento, ou CEP)", "Geometria imprecisa (vértices fora da divisa real)", "Fotos faltando ou de baixa qualidade", "Titulares incorretos (CPF inválido, percentual errado)", "Documentação insuficiente (observações necessárias)" permitindo MANAGER marcar relevantes auto-populando textarea com template estruturado, e seção "Prioridade" com radio buttons Normal Alta Urgente sendo Alta pré-selecionada como padrão facilitando feedback padronizado acionável ao criador.

**Atualização de Status:**

Transação SQL inicia BEGIN TRANSACTION executando três operações atômicas sendo UPDATE units SET status igual Requires Changes updated_at igual NOW() WHERE id igual parâmetro um atualizando estado unidade impedindo aprovação até correção, INSERT INTO change_requests com colunas unit_id requested_by requested_at description priority status VALUES parâmetro um unit_id parâmetro dois manager_id NOW() timestamp parâmetro três description parâmetro quatro priority literal OPEN criando registro rastreável solicitação, INSERT INTO unit_timeline com event_type CHANGES_REQUESTED actor_id manager_id description texto alterações created_at NOW() adicionando evento visível timeline auditável, finalmente COMMIT confirmando transação garantindo atomicidade todas mudanças sucesso ou rollback completo se falha.

**Notificação ao Criador:**

Email enviado com assunto "Alterações solicitadas para Unidade UH-123" contendo saudação "Olá [Nome do Criador]" seguido por corpo "O gestor [Nome do MANAGER] solicitou alterações na unidade UH-123 antes de aprovar:" incluindo descrição interpolada das alterações específicas solicitadas, texto "Por favor, acesse o link abaixo para realizar as correções:" com link direto para edição da unidade pré-carregando formulário com dados atuais e banner destacado exibindo solicitação, informação "Prazo sugerido: 7 dias" orientando tempo esperado correção conforme policy tenant, assinatura "Equipe CARF" garantindo comunicação profissional padronizada contexto específico urgência apropriada.

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
**Status do arquivo**: Pronto
