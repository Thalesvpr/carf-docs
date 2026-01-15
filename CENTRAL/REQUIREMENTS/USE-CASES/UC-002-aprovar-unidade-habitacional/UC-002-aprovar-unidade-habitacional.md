---
modules: [GEOWEB, REURBCAD]
epic: performance
---

# UC-002: Aprovar Unidade Habitacional

Caso de uso permitindo MANAGER gestor com poder de aprovação de unidades revisar e aprovar unidades cadastradas previamente mudando status de Pending Approval para Approved após autenticação e verificação de role MANAGER, onde fluxo principal inicia com acesso à lista de unidades pendentes exibindo filtro automático por status Pending Approval mostrando código endereço resumido data de criação nome do criador e tempo aguardando aprovação em dias ordenadas por antiguidade (mais antigas primeiro) ou prioridade configurável, MANAGER seleciona unidade específica para revisar clicando na linha que carrega tela de detalhes completa exibindo dados cadastrais completos em seções organizadas (código endereço tipo área número de moradores), geometria renderizada no mapa interativo com ferramentas de zoom pan e medição permitindo inspeção visual do perímetro, fotos anexadas em galeria clicável com lightbox, titulares vinculados listando CPF nome tipo de vínculo percentual de propriedade com validação visual de CPF verificado, timeline de alterações mostrando histórico cronológico de mudanças desde criação incluindo quem modificou o que e quando, e indicadores de qualidade automatizados (completude de dados percentual de campos preenchidos alertas de validação warnings de geometria sobreposta). MANAGER revisa informações verificando correção de endereço validade de geometria presença de titulares principais e conformidade com padrões municipais, clica em botão Aprovar disparando modal de confirmação com campo textarea opcional para adicionar comentário justificativo (aprovado conforme critérios técnicos ou observações específicas), confirma aprovação clicando Confirmar no modal e sistema executa transação atômica atualizando status para Approved, registrando approved_at timestamp atual, approved_by AccountId do MANAGER autenticado, adding comentário à timeline se fornecido marcando como APPROVAL_COMMENT, disparando domain event UnitApprovedEvent para notificações assíncronas via message broker (RabbitMQ ou similar) que envia email ao criador da unidade informando aprovação com link direto para visualizar detalhes, e criando registro de auditoria em audit_logs tabela documentando operação. Sistema exibe toast de sucesso "Unidade UH-123 aprovada com sucesso" e atualiza lista de pendentes removendo unidade aprovada automaticamente decrementando contador de badges numéricos. Fluxos alternativos cobertos incluem aprovar em lote selecionando múltiplas unidades via checkboxes (UC-002-FA-001). Fluxos de exceção cobertos incluem detecção de concurrent modification quando unidade já foi aprovada por outro MANAGER entre carregamento e tentativa de aprovação (UC-002-FE-001), e cenário onde MANAGER identifica dados incompletos ou incorretos solicitando alterações ao invés de aprovar (UC-002-FE-002). Pós-condições garantem status Approved irreversível sem workflow reverso (requer novo processo de revisão administrativo se necessário desfazer), timestamp de aprovação registrado permanentemente, aprovador identificado rastreável, notificação enviada garantida com retry em caso de falha temporária de email service, e registro de auditoria criado para compliance.

**Fluxos Alternativos:**
- UC-002-FA-001: Aprovar em lote

**Fluxos de Exceção:**
- UC-002-FE-001: Unidade já foi aprovada
- UC-002-FE-002: Solicitar alterações

**Regras de Negócio:**
- RN-001: Apenas MANAGER pode aprovar unidades verificado via middleware authorization
- RN-002: Unidades com status Draft não podem ser aprovadas diretamente (devem passar por Pending Approval primeiro)
- RN-003: Aprovação é irreversível sem workflow reverso (apenas soft delete ou novo processo administrativo pode desfazer)

**Rastreabilidade:**
- RF-056, RF-057, RF-060
- US-034, US-036

---

**Última atualização:** 2025-12-30
