---
id: UC-P3-003
type: UC
modules: []
status: review
created: 2026-01-24
updated: 2026-01-24
workflow: PARTE-3
---

# UC-P3-003: Selecionar Comunidade

Agente de Campo seleciona comunidade para o periodo de atuacao e carrega mapa.

## Referencia

Este UC implementa passos 13-14 do [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/03-operacao-campo.md).

## Atores

- Primario: Agente de Campo

## Pre-condicoes

- Pacote baixado (UC-P3-002 concluido)
- Comunidades disponiveis no pacote

## Fluxo Principal

1. App exibe lista de comunidades liberadas
2. Agente visualiza informacoes de cada comunidade:
   - Nome da comunidade
   - Quantidade de lotes
   - Status de progresso
3. Agente seleciona comunidade para o periodo de atuacao
4. App carrega dados especificos da comunidade:
   - Poligonos de quadras
   - Poligonos de lotes
   - Cadastros existentes
5. App carrega mapa georreferenciado da area
6. Agente escolhe modo de visualizacao:
   - Ortofoto ONLINE (se houver conectividade)
   - Ortofoto OFFLINE (pacote baixado)
7. Poligonos de quadras e lotes exibidos sobre a ortofoto
8. Mapa pronto para operacao

## Fluxos Alternativos

- FA-001: Filtrar comunidades por status
- FA-002: Buscar comunidade por nome

## Fluxos de Excecao

- FE-001: Nenhuma comunidade disponivel
- FE-002: Erro ao carregar mapa

## Pos-condicoes

- Comunidade selecionada
- Mapa carregado com ortofoto e poligonos
- Agente pode operar em campo (UC-P3-004)

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| RN-01 | Apenas comunidades publicadas sao exibidas |
| RN-02 | Modo offline disponivel sem conexao |
