---
type: leaf
status: review
updated: 2026-02-08
---

# Legitimation Workflow Feature

A feature de workflow de legitimacao fundiaria implementa o processo completo conforme Lei 13.465/2017, desde a abertura do requerimento ate a emissao do titulo e registro em cartorio. O processo segue uma maquina de estados com 11 status possiveis, prazos legais de 30 dias para contestacao e 120 dias para decisao, e gera certidao em PDF com numero sequencial no formato CERT-AAAA-NNNNN.

## User Stories

US-050 Iniciar Processo: o analista cria um requerimento de legitimacao para uma unidade. Pre-condicoes: unidade com status APPROVED e ao menos um titular PROPRIETARIO vinculado. O processo e criado com status DRAFT.

US-051 Aprovar Processo: o gestor aprova o requerimento fornecendo justificativa obrigatoria. O status transiciona para APPROVED e o sistema fica habilitado para emissao de certidao.

US-052 Rejeitar Processo: o gestor rejeita o requerimento informando motivo com no minimo 100 caracteres citando fundamento legal. O status transiciona para REJECTED.

US-053 Download Certidao: o analista faz download do PDF da certidao de legitimacao fundiaria. Disponivel apenas para processos com status TITLE_ISSUED ou REGISTERED.

## Maquina de Estados

O ciclo de vida do processo segue a sequencia DRAFT, SUBMITTED, UNDER_ANALYSIS, NOTIFICATION_PUBLISHED, CONTESTATION_PERIOD, CONTESTATION_RECEIVED (opcional), DECISION_PENDING, APPROVED ou REJECTED, TITLE_ISSUED (apos aprovacao) e REGISTERED (apos cartorio). A transicao de NOTIFICATION_PUBLISHED para CONTESTATION_PERIOD inicia prazo de 30 dias. A transicao para DECISION_PENDING inicia prazo de 120 dias para decisao.

## Endpoints

| Metodo | Rota | Descricao |
|--------|------|-----------|
| POST | /api/legitimation | Iniciar processo |
| GET | /api/legitimation/{id} | Obter processo |
| GET | /api/legitimation | Listar com paginacao |
| POST | /api/legitimation/{id}/approve | Aprovar processo |
| POST | /api/legitimation/{id}/reject | Rejeitar processo |
| GET | /api/legitimation/{id}/certificate | Download PDF certidao |

## Regras de Negocio

RN-050: processo so pode ser criado para unidade com status APPROVED. RN-051: unidade deve ter ao menos um titular com relationship_type PROPRIETARIO. RN-052: nao pode existir dois processos ativos para a mesma unidade (constraint parcial onde deleted_at IS NULL e status NOT IN REJECTED). RN-053: rejeicao requer reason com no minimo 100 caracteres citando fundamento legal. RN-054: prazo de contestacao e de 30 dias apos publicacao do edital. RN-055: prazo de decisao e de 120 dias apos encerramento do periodo de contestacao. RN-056: certidao PDF recebe numero sequencial unico no formato CERT-AAAA-NNNNN, constraint UNIQUE global em certificate_number. RN-057: certidao so pode ser baixada para processos com status TITLE_ISSUED ou REGISTERED.

## Permissoes

| Acao | field-cadastrator | field-coordinator | analyst | manager | admin | super-admin |
|------|-------------------|-------------------|---------|---------|-------|-------------|
| Iniciar processo | nao | nao | sim | sim | sim | sim |
| Visualizar | nao | nao | sim | sim | sim | sim |
| Aprovar | nao | nao | nao | sim | sim | sim |
| Rejeitar | nao | nao | nao | sim | sim | sim |
| Download certidao | nao | nao | sim | sim | sim | sim |
