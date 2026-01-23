---
id: RNF-047
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-047: Internacionalizacao

## Descricao

Sistema deve suportar PT-BR como idioma obrigatorio com infraestrutura i18n para futura adicao de outros idiomas sem refatoracao significativa.

## Metricas

- Idioma obrigatorio: Portugues Brasileiro (PT-BR)
- Biblioteca: i18next ou similar
- Formatos: datas DD/MM/YYYY, moeda R$ X.XXX,XX

## Criterios de Aceitacao

1. Textos externalizados em arquivos JSON por namespace
2. Datas e horas formatadas no padrao brasileiro
3. Estrutura de pastas preparada para multiplos locales
