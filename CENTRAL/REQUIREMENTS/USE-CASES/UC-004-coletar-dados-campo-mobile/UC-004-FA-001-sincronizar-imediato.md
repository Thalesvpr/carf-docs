---
id: UC-004-FA-001
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-004-FA-001: Sincronizar Imediatamente

Fluxo alternativo do UC-004 para sincronizar dados quando conexao esta disponivel.

## Condicao

No passo 13 do UC-004, app detecta conexao de rede disponivel apos salvar unidade localmente.

## Fluxo

1. App detecta conexao WiFi ou dados moveis
2. App exibe botao Sincronizar Agora com badge de pendencias
3. FIELD_AGENT clica em Sincronizar Agora
4. Sistema inicia processo de sincronizacao (UC-005)
5. Sistema exibe progresso da sincronizacao
6. Sistema atualiza registros locais apos sucesso
7. Sistema remove badges de pendencia
8. Sistema exibe confirmacao

## Retorno

Dados sincronizados com servidor. FIELD_AGENT continua coleta com storage local liberado.

## Pos-condicoes

- Unidades enviadas para servidor
- Registros locais marcados como sincronizados
- Espaco de armazenamento liberado
