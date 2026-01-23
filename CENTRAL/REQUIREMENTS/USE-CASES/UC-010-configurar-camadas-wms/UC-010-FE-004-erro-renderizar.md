---
id: UC-010-FE-004
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-010-FE-004: Erro ao Renderizar

Fluxo de excecao do UC-010 quando frontend falha ao renderizar camada no mapa.

## Condicao

No passo 17 do UC-010, biblioteca de mapas falha ao adicionar ou renderizar camada.

## Fluxo

1. Frontend tenta adicionar camada ao mapa
2. Biblioteca detecta erro durante operacao
3. Frontend captura excecao e loga detalhes
4. Frontend exibe toast de warning ao usuario
5. Frontend marca camada com badge de erro
6. Frontend desabilita camada ate correcao
7. ADMIN acessa configuracoes para editar ou remover

## Causas Comuns

- Bloqueio CORS (proxy nao habilitado)
- Formato de imagem incompativel
- Sistema de coordenadas nao suportado
- Servidor retornando erros nos tiles

## Retorno

Camada marcada com erro. ADMIN pode editar configuracao, habilitar proxy ou remover camada.
