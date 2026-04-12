---
type: leaf
status: approved
updated: 2026-02-07
---

# Workflows Diagram

Descricao das state machines para os workflows principais do sistema: status de Unit, processo de Legitimacao e sincronizacao offline.

## Workflow de Status da Unidade

A unidade inicia no estado Rascunho quando criada offline pela equipe de campo. Ao sincronizar e submeter, transiciona para Pendente. O Analista inicia revisao, movendo para EmAnalise. A partir de EmAnalise, tres destinos sao possiveis: Aprovado (analista aprova), Rejeitado (analista rejeita com comentarios) ou RequerAlteracoes (analista solicita correcoes). De RequerAlteracoes, retorna a EmAnalise quando o usuario corrige e reenvia. De Rejeitado, retorna a Rascunho para reedicao. Aprovado e o estado terminal.

| De | Para | Gatilho | Role |
|----|------|---------|------|
| Rascunho | Pendente | Sincronizacao e submissao | Campo |
| Pendente | EmAnalise | Inicio de revisao | Analista |
| EmAnalise | Aprovado | Aprovacao | Analista |
| EmAnalise | Rejeitado | Rejeicao com comentarios | Analista |
| EmAnalise | RequerAlteracoes | Solicitacao de correcoes | Analista |
| RequerAlteracoes | EmAnalise | Correcao e reenvio | Campo |
| Rejeitado | Rascunho | Edicao e reenvio | Campo |

Ao aprovar, o evento UnidadeAprovadaEvent e disparado, acionando NotificacaoEmailHandler, AuditLogHandler e CacheInvalidationHandler.

## Workflow do Processo de Legitimacao

O processo inicia no estado Iniciado quando o Gestor cria o processo. O Analista analisa documentacao, movendo para SobAnalise. De SobAnalise, tres destinos: LegitimacaoAprovada, LegitimacaoRejeitada (com base legal) ou AguardandoDocumentacao. De AguardandoDocumentacao, retorna a SobAnalise quando titular submete documentos. De LegitimacaoAprovada, transiciona para CertidaoEmitida quando a certidao e gerada e assinada digitalmente. CertidaoEmitida e o estado terminal.

| De | Para | Gatilho |
|----|------|---------|
| Iniciado | SobAnalise | Analista analisa documentos |
| SobAnalise | LegitimacaoAprovada | Aprovacao |
| SobAnalise | LegitimacaoRejeitada | Rejeicao com base legal |
| SobAnalise | AguardandoDocumentacao | Solicitacao de documentos adicionais |
| AguardandoDocumentacao | SobAnalise | Titular submete documentos |
| LegitimacaoAprovada | CertidaoEmitida | Certidao gerada e assinada |

Ao concluir, o evento LegitimacaoConcluidaEvent aciona geracao de PDF, registro de titulo, notificacao ao municipio e arquivamento de documentos. O Analista valida documentacao legal, provas de propriedade, aprovacao municipal e conformidade com Lei 13.465.

## Workflow de Sincronizacao Offline

Registro inicia como RascunhoLocal quando criado offline. Ao marcar para sync, transiciona para AguardandoUpload. Com rede disponivel, move para Enviando. Se a versao do servidor difere, entra em Conflito; caso contrario, vai para Sincronizado. De Conflito, o usuario escolhe resolucao (servidor vence, local vence ou merge manual) e transiciona para Sincronizado.

| De | Para | Gatilho |
|----|------|---------|
| RascunhoLocal | AguardandoUpload | Marcado para sync |
| AguardandoUpload | Enviando | Rede disponivel |
| Enviando | Sincronizado | Sucesso |
| Enviando | Conflito | Versao do servidor difere |
| Conflito | Sincronizado | Usuario resolve conflito |

Os workflows seguem o WORKFLOW-MESTRE do CARF. A equipe de campo (Coordenador e Cadastrador) cria unidades offline que sincronizam com o backend. O Analista (via Plugin QGIS ou REURBWEB) revisa e aprova. O processo de Legitimacao segue rito legal da Lei 13.465/2017 com etapas obrigatorias.
