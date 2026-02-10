---
type: leaf
status: review
updated: 2026-02-08
---

# CREA

Value object imutavel representando registro profissional no Conselho Regional de Engenharia e Agronomia. Utilizado para validar credenciais de Surveyor responsavel por memoriais descritivos e plantas de legitimacao.

## Regras de Validacao

| Regra | Descricao |
|-------|-----------|
| Formato | Alfanumerico. Formato tipico: 123456-D/UF. |
| UF valida | Sigla do estado deve ser UF brasileira valida (2 letras). |
| Nao vazio | Registro nao pode ser string vazia ou nula ao criar. |

## Uso no Dominio

CREA valida que o responsavel tecnico por DescriptiveMemorial e LegitimationPlan possui habilitacao profissional adequada. O campo ArtNumber (Anotacao de Responsabilidade Tecnica) e obrigatorio para memoriais oficiais de processos de legitimacao.
