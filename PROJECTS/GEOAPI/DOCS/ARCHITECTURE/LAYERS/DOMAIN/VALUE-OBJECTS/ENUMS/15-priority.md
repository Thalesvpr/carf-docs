# Priority

Value object enum representando nível de prioridade aplicável a diversos contextos do sistema como solicitações de legitimação, anotações e tickets de suporte. Valores possíveis são LOW (baixa prioridade para tarefas que podem aguardar sem impacto em prazos), NORMAL (prioridade padrão para fluxo regular de trabalho), HIGH (alta prioridade para situações que exigem atenção breve mas não impedem operação), e URGENT (urgência máxima para casos críticos que bloqueiam processos ou afetam prazos legais).

Métodos incluem GetSLA() retornando tempo esperado de resposta em horas (URGENT: 4h, HIGH: 24h, NORMAL: 72h, LOW: 168h), GetColor() retornando código de cor para UI (URGENT: vermelho, HIGH: laranja, NORMAL: azul, LOW: cinza), CanEscalate() verificando se permite escalação automática após timeout, CompareTo(Priority other) implementando IComparable para ordenação, e ToDisplayString() retornando nome amigável.

Usado em LegitimationRequest.Priority influenciando ordem de análise na fila de trabalho, Annotation.Priority para anotações tipo ISSUE definindo criticidade e REMINDER estabelecendo urgência, integra com sistema de notificações onde URGENT dispara alertas imediatos via email e push enquanto LOW apenas registra in-app, e alimenta relatórios gerenciais mostrando distribuição e SLA compliance.

---

**Última atualização:** 2026-01-12
