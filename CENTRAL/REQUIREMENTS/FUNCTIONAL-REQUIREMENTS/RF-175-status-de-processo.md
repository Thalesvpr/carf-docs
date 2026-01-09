---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: maintainability
---

# RF-175: Status de Processo

O sistema implementa workflow estruturado de tramitação de processos de legitimação através de enum de status que define estados possíveis incluindo Em Análise para processos recém-criados sob avaliação técnica inicial, Documentação Pendente quando identificadas lacunas documentais que impedem prosseguimento, Aprovado para processos que atenderam todos os requisitos técnicos e jurídicos, Concluído quando título foi emitido e entregue ao beneficiário, e Indeferido para processos que não atenderam critérios de elegibilidade ou apresentaram impedimentos legais. O sistema define matriz de transições válidas que estabelece quais mudanças de status são permitidas conforme lógica de negócio, prevenindo transições inconsistentes como mudança direta de Indeferido para Concluído sem passar por estados intermediários apropriados, garantindo coerência lógica no ciclo de vida processual. Todas as mudanças de status são registradas em log histórico que captura data/hora da transição, usuário responsável, status de origem e destino, além de justificativa textual obrigatória que documenta motivação da mudança, criando trilha auditável completa da tramitação processual que pode ser consultada posteriormente para análises de eficiência, identificação de gargalos e prestação de contas sobre gestão dos processos de regularização fundiária.

---

**Última atualização:** 2025-12-30
