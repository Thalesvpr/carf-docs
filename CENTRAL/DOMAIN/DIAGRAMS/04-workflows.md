---
type: leaf
status: approved
updated: 2026-01-24
---

# Workflows Diagram

Diagramas de state machine para os workflows principais do sistema: status de Unit, processo de Legitimacao e sincronizacao offline.

## Diagrama Mermaid

```mermaid
stateDiagram-v2
    [*] --> Rascunho: Equipe de campo cria unidade offline

    state "Workflow de Status da Unidade" as UnitWorkflow {
        Rascunho --> Pendente: Usuario de campo sincroniza e submete
        Pendente --> EmAnalise: Analista inicia revisao
        EmAnalise --> Aprovado: Analista aprova
        EmAnalise --> Rejeitado: Analista rejeita com comentarios
        EmAnalise --> RequerAlteracoes: Analista solicita correcoes

        RequerAlteracoes --> EmAnalise: Usuario de campo corrige e reenvia
        Rejeitado --> Rascunho: Usuario de campo pode editar e reenviar
        Aprovado --> [*]: Unidade ativa

        note right of Aprovado
            UnidadeAprovadaEvent disparado
            - NotificacaoEmailHandler
            - AuditLogHandler
            - CacheInvalidationHandler
        end note

        note right of EmAnalise
            Role: ANALISTA
            Valida conformidade com
            regulamentos municipais
        end note
    }

    state "Workflow do Processo de Legitimacao" as LegitimationWorkflow {
        [*] --> Iniciado: Gestor cria processo

        Iniciado --> SobAnalise: Analista analisa docs
        SobAnalise --> LegitimacaoAprovada: Analista aprova
        SobAnalise --> LegitimacaoRejeitada: Analista rejeita com base legal
        SobAnalise --> AguardandoDocumentacao: Analista solicita docs adicionais

        AguardandoDocumentacao --> SobAnalise: Titular submete docs
        LegitimacaoAprovada --> CertidaoEmitida: Certidao gerada e assinada digitalmente
        CertidaoEmitida --> [*]: Processo completo

        note right of CertidaoEmitida
            LegitimacaoConcluidaEvent
            - Gerar PDF da certidao
            - Registrar titulo de propriedade
            - Notificar municipio
            - Arquivar documentos
        end note

        note right of SobAnalise
            Role: ANALISTA
            Valida:
            - Documentacao legal
            - Provas de propriedade
            - Aprovacao municipal
            - Conformidade Lei 13.465
        end note
    }

    state "Workflow de Sincronizacao Offline" as SyncWorkflow {
        [*] --> RascunhoLocal: Criado offline
        RascunhoLocal --> AguardandoUpload: Marcado para sync
        AguardandoUpload --> Enviando: Rede disponivel
        Enviando --> Conflito: Versao do servidor difere
        Enviando --> Sincronizado: Sucesso
        Conflito --> Resolvendo: Usuario escolhe resolucao
        Resolvendo --> Sincronizado: Conflito resolvido
        Sincronizado --> [*]: Concluido

        note right of Conflito
            Merge three-way:
            - Baseline (ultima sync)
            - Alteracoes locais
            - Alteracoes servidor
            Usuario escolhe:
            - Servidor vence
            - Local vence
            - Merge manual
        end note
    }
```

Os workflows seguem o WORKFLOW-MESTRE do CARF. A equipe de campo (Coordenador e Cadastrador) cria unidades offline que sincronizam com o backend. O Analista (via Plugin QGIS ou GEOWEB) revisa e aprova. O processo de Legitimacao segue rito legal da Lei 13.465/2017 com etapas obrigatorias.
