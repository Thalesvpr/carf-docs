---
type: standard
status: current
updated: 2026-01-23
---

# STD-002: Estrutura de README

## Regra

Todo diretorio deve conter README.md com titulo H1 igual ao nome da pasta, seguido de paragrafo denso descrevendo conteudo com links inline para arquivos filhos. Usar prosa continua sem bullets no corpo principal. Indice de arquivos e gerado automaticamente entre comentarios CARF-INDEX-START e CARF-INDEX-END. Arquivos index.md nao sao permitidos.

## Justificativa

Estrutura padronizada facilita navegacao hierarquica e permite geracao automatica de indices, eliminando manutencao manual de listas de arquivos.

## Aplicacao

Aplica-se a todos os diretorios em CENTRAL e PROJECTS. READMEs devem linkar apenas filhos diretos, nunca netos ou arquivos de outras pastas. Referencias a outras areas usam mencao textual sem hyperlink.
