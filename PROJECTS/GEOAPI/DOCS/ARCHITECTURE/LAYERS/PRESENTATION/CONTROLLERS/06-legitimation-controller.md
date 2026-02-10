---
type: leaf
status: review
updated: 2026-02-08
---

# Legitimation Controller

O LegitimationController gerencia o workflow de legitimacao fundiaria conforme Lei 13.465/2017. A rota base e /api/legitimation. Todos os endpoints requerem role analyst ou superior. Aprovacao e rejeicao requerem role manager ou superior.

## Endpoints

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| POST | /api/legitimation | Iniciar processo | 201 | 400 VALIDATION_ERROR | analyst+ |
| GET | /api/legitimation/{id} | Obter processo | 200 | 404 | analyst+ |
| GET | /api/legitimation | Listar com paginacao | 200 | - | analyst+ |
| POST | /api/legitimation/{id}/approve | Aprovar processo | 200 | 403 NOT_AUTHORIZED | manager+ |
| POST | /api/legitimation/{id}/reject | Rejeitar processo | 200 | 403 NOT_AUTHORIZED | manager+ |
| GET | /api/legitimation/{id}/certificate | Download PDF certidao | 200 | 404 | analyst+ |

## Comportamento

O endpoint de criacao recebe body com unitId (UUID obrigatorio), valida pre-condicoes (unidade APPROVED, titular PROPRIETARIO vinculado) e despacha CreateLegitimationRequestCommand. O handler verifica que nao existe outro processo ativo para a mesma unidade e cria o registro com status DRAFT. O endpoint de aprovacao recebe justification (string obrigatoria) e despacha ApproveLegitimationRequestCommand que transiciona o status para APPROVED, registra o manager_id e a justificativa. O endpoint de rejeicao recebe reason (string obrigatoria, minimo 100 caracteres) e despacha RejectLegitimationRequestCommand que transiciona para REJECTED. O endpoint de certidao retorna arquivo PDF com Content-Type application/pdf e Content-Disposition attachment, disponivel apenas para processos com status TITLE_ISSUED ou REGISTERED.

## Autorizacao

Criacao, consulta e listagem requerem role analyst, manager, admin ou super-admin. Aprovacao e rejeicao requerem role manager, admin ou super-admin, retornando 403 NOT_AUTHORIZED para roles insuficientes. Download de certidao requer analyst ou superior.
