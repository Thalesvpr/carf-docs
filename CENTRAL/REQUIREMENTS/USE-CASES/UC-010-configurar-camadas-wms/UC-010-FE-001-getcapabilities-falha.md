---
id: UC-010-FE-001
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-010-FE-001: GetCapabilities Falha

Fluxo de excecao do UC-010 quando request GetCapabilities falha.

## Condicao

No passo 7 do UC-010, sistema nao consegue obter resposta do servidor externo.

## Fluxo

1. Sistema executa request GetCapabilities
2. Sistema detecta falha na conexao
3. Sistema captura erro e loga detalhes
4. Sistema exibe modal com mensagem de erro
5. Sistema sugere acoes corretivas
6. ADMIN verifica URL e tenta novamente

## Causas Comuns

- Timeout (servidor lento ou fora do ar)
- URL incorreta ou endpoint alterado
- Erro de certificado SSL
- Firewall bloqueando conexao
- DNS nao resolve dominio

## Retorno

Erro exibido com detalhes. ADMIN corrige URL ou aguarda servidor e retenta.
