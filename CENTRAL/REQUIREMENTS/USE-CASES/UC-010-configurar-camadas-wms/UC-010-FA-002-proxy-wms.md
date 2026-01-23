---
id: UC-010-FA-002
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-010-FA-002: Proxy de WMS

Fluxo alternativo do UC-010 para rotear requests via backend evitando bloqueios CORS.

## Condicao

No passo 13 do UC-010, ADMIN marca opcao Usar Proxy antes de salvar.

## Fluxo

1. ADMIN marca checkbox Usar Proxy
2. Sistema salva configuracao com flag de proxy
3. Frontend detecta flag ao carregar camada
4. Frontend usa endpoint interno ao inves de URL direta
5. Backend recebe request e valida permissoes
6. Backend executa request ao servidor externo
7. Backend aplica cache local nos tiles
8. Backend retorna imagem ao frontend
9. Frontend renderiza tile normalmente

## Casos de Uso

- Servidores sem headers CORS configurados
- Orgaos governamentais com infraestrutura antiga
- Servidores internos sem HTTPS

## Retorno

Camada configurada com proxy. Requests roteados via backend sem bloqueio CORS.
