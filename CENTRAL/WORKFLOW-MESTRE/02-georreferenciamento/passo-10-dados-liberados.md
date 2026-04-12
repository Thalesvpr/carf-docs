---
type: workflow
status: approved
updated: 2026-02-07
part: 2
step: 10
---

# Passo 10: Dados Liberados para Campo

Apos publicacao bem-sucedida, dados ficam disponiveis para a equipe de campo.

## Fluxo

1. **REGRA CRITICA:** SOMENTE apos publicacao bem-sucedida
2. Backend marca dados como "liberados" para o TENANT
3. Equipe de campo (Coordenador e Cadastrador) do mesmo TENANT podem acessar
4. Ortofoto + poligonos disponiveis para download temporario

## Transicao

Apos a publicacao no Passo 9, o backend marca os dados como liberados. A Parte 3 torna-se habilitada e a equipe de campo pode baixar o pacote temporario.

## Status dos Dados

| Status | Descricao | Acesso Campo |
|--------|-----------|--------------|
| rascunho | Em edicao pelo Analista | NAO |
| publicado | Publicacao concluida | SIM |

## Conteudo Disponivel

Apos publicacao, o pacote para campo inclui:
- Ortofoto (versao para uso offline)
- Poligonos de comunidades
- Poligonos de quadras
- Poligonos de lotes
- Metadados associados

## Regra Critica

**PUB-02:** Equipe de campo SO consegue baixar dados QUANDO Analista JA PUBLICOU.

Dados NAO ficam disponiveis para campo ANTES da publicacao (PUB-04).

## Resultado

- Dados marcados como "liberados"
- Pacote disponivel para download
- **PARTE 2 CONCLUIDA**

## Proxima Parte

PARTE 3: Operacao em Campo
