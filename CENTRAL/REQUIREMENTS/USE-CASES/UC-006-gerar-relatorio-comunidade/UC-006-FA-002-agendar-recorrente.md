---
id: UC-006-FA-002
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-006-FA-002: Agendar Geracao Recorrente

Fluxo alternativo do UC-006 para envio automatico de relatorios em periodicidade definida.

## Condicao

No passo 6 do UC-006, usuario deseja receber relatorio automaticamente em vez de gerar sob demanda.

## Fluxo

1. Usuario marca opcao Agendar Envio Recorrente
2. Sistema expande formulario com opcoes de periodicidade
3. Usuario seleciona frequencia (semanal, mensal, trimestral)
4. Usuario informa emails dos destinatarios
5. Sistema valida permissao de agendamento
6. Sistema cria registro de agendamento
7. Sistema configura job recorrente
8. Sistema exibe confirmacao com proxima execucao

## Periodicidades Disponiveis

- Semanal (toda segunda-feira)
- Mensal (dia 1 de cada mes)
- Trimestral (primeiro dia do trimestre)

## Gerenciamento

- Usuario pode editar, desativar ou deletar agendamentos
- Menu Meus Agendamentos lista todos configurados

## Retorno

Agendamento criado. Relatorio gerado e enviado automaticamente na periodicidade definida.

## Pos-condicoes

- Job recorrente configurado no sistema
- Destinatarios receberao email com relatorio anexo
