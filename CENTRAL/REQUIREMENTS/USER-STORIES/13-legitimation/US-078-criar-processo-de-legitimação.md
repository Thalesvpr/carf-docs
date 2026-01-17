---
modules: [GEOAPI, GEOWEB]
epic: compatibility
---

# US-078: Criar Processo de Legitimação

Como gestor, quero criar processo formal de legitimação fundiária vinculado a uma unidade previamente aprovada para que titulação legal seja iniciada conforme marcos regulatórios REURB, onde a funcionalidade deve permitir seleção de unidade com status APPROVED como base para processo, garantindo definição de tipo de processo sendo REURB-S (regularização de interesse social) ou REURB-E (regularização de interesse específico), permitindo que processo seja criado em status inicial DRAFT com checklist de documentos necessários para posterior submissão e aprovação. Esta funcionalidade é implementada pelo módulo GEOWEB com formulário de criação de processo consumindo GEOAPI através do endpoint POST /api/legitimation/processes que valida elegibilidade e cria registro, integrada ao RF-172 (Criação de Processo de Legitimação) e UC-009 (Gestão de Processos de Legitimação). Os critérios de aceitação incluem interface de criação de processo acessível apenas para unidades com status APPROVED, seleção de unidade elegível através de busca ou lista filtrada mostrando apenas unidades aprovadas sem processo ativo, seleção obrigatória de tipo de processo (REURB-S para baixa renda ou REURB-E para demais casos), criação de processo em status inicial DRAFT permitindo preparação antes de submeter formalmente, geração automática de número único de protocolo ou identificador do processo, associação bidirecional entre processo e unidade vinculada, exibição de checklist de documentos necessários conforme tipo de processo selecionado (RG CPF comprovante_residência etc), interface de upload permitindo anexar documentos obrigatórios ao processo, validação impedindo criação de processo duplicado para mesma unidade se já existir processo ativo, e atribuição automática de responsável pelo processo (usuário criador) com possibilidade de reatribuição posterior. A rastreabilidade conecta esta user story ao RF-172 (Abertura de Processo) UC-009 (Gestão de Legitimação) e endpoint POST /api/legitimation/processes, garantindo formalização adequada de processos de titulação conforme legislação vigente.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
