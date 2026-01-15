---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: scalability
---

# UC-002-FE-001: Concurrent Modification (Unidade Já Foi Aprovada)

Fluxo de exceção do UC-002 Aprovar Unidade Habitacional ocorrendo no passo 9 (execução de aprovação) quando sistema detecta que status da unidade mudou entre momento em que MANAGER carregou tela de detalhes e momento em que clicou Aprovar, cenário típico de concorrência onde dois ou mais MANAGERS acessaram mesma unidade pendente simultaneamente e um deles aprovou enquanto outro ainda estava revisando, onde detecção utiliza optimistic locking comparando RowVersion timestamp ou versão numérica da entidade Unit verificando que valor atual no banco difere do valor carregado inicialmente pelo frontend (enviado no payload de aprovação como expected_version campo), ao executar UPDATE units SET status = 'Approved' WHERE id = X AND row_version = Y sistema retorna affected_rows = 0 indicando que condição de versão falhou pois registro foi modificado por outra transação, backend intercepta affected_rows zero lançando ConcurrentModificationException customizada com mensagem contextual e código de erro específico, retorna HTTP 409 Conflict com body JSON `{"error": "Unit was already approved", "code": "CONCURRENT_MODIFICATION", "current_status": "Approved", "approved_by": "João Silva", "approved_at": "2025-12-30T14:23:15Z"}` incluindo informações atuais da unidade para exibição ao usuário. Frontend interceptor HTTP captura 409 Conflict verificando código CONCURRENT_MODIFICATION diferenciando de outros conflitos (geometria sobreposta código duplicado), exibe toast de erro com ícone de alerta laranja e mensagem "Esta unidade já foi aprovada por João Silva em 30/12/2025 às 14:23" incluindo nome do aprovador e timestamp formatado para contexto humano, automaticamente atualiza tela de detalhes recarregando dados frescos do servidor via GET /api/units/:id mostrando status atual Approved e informações de aprovação na timeline, e desabilita botão Aprovar substituindo por badge verde "Aprovada" com tooltip mostrando quem aprovou e quando. MANAGER lê mensagem de erro compreendendo que outro usuário foi mais rápido, visualiza dados atualizados confirmando que aprovação já foi registrada corretamente, e retorna para lista de pendentes clicando botão Voltar onde unidade aprovada já não aparece mais pois filtro é por status Pending Approval, permitindo continuar revisando outras unidades sem frustração pois sistema comunicou claramente o que aconteceu e atualizou estado automaticamente.

**Ponto de Desvio:** Passo 9 do UC-002 (execução de UPDATE no banco)

**Detecção de Concorrência:**

Backend executa UPDATE units SET status igual Approved approved_at igual NOW() approved_by igual parâmetro um row_version igual row_version mais um WHERE id igual parâmetro dois AND row_version igual parâmetro três verificando expected version enviada pelo frontend, se affected_rows retorna zero indica concurrent modification pois condição row_version falhou significando registro foi modificado por outra transação entre momento leitura inicial e tentativa update, backend lança ConcurrentModificationException retornando HTTP 409 Conflict.

**Resposta de Erro:**

Response HTTP 409 retorna objeto JSON contendo error com mensagem Unit was already approved by another user, code igual CONCURRENT_MODIFICATION identificando tipo conflito específico, details objeto contendo current_status igual Approved, approved_by objeto com id uuid-123 name João Silva, approved_at timestamp 2025-12-30T14:23:15Z, expected_version cinco valor enviado pelo frontend, current_version seis valor atual banco indicando incremento ocorreu por outra transação permitindo frontend processar informações contextuais exibir mensagem específica usuário.

**Tratamento Frontend:**

Frontend executa try-catch chamando await approveUnit passando unitId expectedVersion, catch verifica se error.response.status igual quatrocentos e nove AND error.response.data.code igual CONCURRENT_MODIFICATION identificando conflito concorrência, extrai approved_by approved_at de error.response.data.details via destructuring, chama showToast interpolando mensagem "Unidade já foi aprovada por ${approved_by.name} em ${formatDate(approved_at)}" com tipo warning exibindo toast laranja contexto específico, executa await refreshUnitDetails com unitId recarregando dados frescos servidor atualizando UI automaticamente, e chama setCanApprove false desabilitando botão Aprovar prevenindo retry impossível operação.

**Retorno:** MANAGER retorna para lista de pendentes, unidade não aparece mais (já aprovada)

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
