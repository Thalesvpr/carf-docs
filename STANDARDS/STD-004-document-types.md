---
type: standard
status: current
updated: 2026-01-23
---

# STD-004: Tipos de Documento

## Regra

Todo documento possui tipo declarado no campo type do frontmatter ou inferido pelo nome. Tipos disponiveis: template, standard, adr, rf, rnf, uc, us, readme, leaf, doc. Templates definem regras de validacao para documentos do mesmo tipo via campo validation no frontmatter. O validador busca templates na pasta do documento e ancestrais.

## Justificativa

Tipagem permite aplicar regras de validacao especificas por categoria de documento, garantindo estrutura consistente em cada tipo.

## Aplicacao

Aplica-se a todos os arquivos markdown. Tipo e inferido automaticamente se nao declarado: STD- infere standard, ADR- infere adr, RF- infere rf, README.md infere readme. Demais arquivos assumem tipo doc.
