---
type: standard
status: current
updated: 2026-01-23
---

# STD-001: Status de Arquivo

## Regra

Todo arquivo markdown deve ter frontmatter YAML com campos type, status e updated. O campo status aceita valores review, approved ou rejected. O campo updated usa formato YYYY-MM-DD. Arquivos rejeitados devem incluir campo description explicando o motivo. Arquivos sem status definido assumem review como padrao.

## Justificativa

Metadados padronizados permitem rastrear estado de completude da documentacao, identificar arquivos pendentes de revisao e automatizar validacoes via scripts.

## Aplicacao

Aplica-se a todos os arquivos .md em CENTRAL e PROJECTS, incluindo READMEs. Scripts em .scripts/ normalizam frontmatter automaticamente. O plugin Obsidian valida presenca dos campos obrigatorios.
