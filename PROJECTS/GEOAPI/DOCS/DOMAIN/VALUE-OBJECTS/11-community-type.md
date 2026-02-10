---
type: leaf
status: review
updated: 2026-02-08
---

# CommunityType

Value object enum imutavel representando a classificacao do tipo de comunidade ou assentamento. Persiste na coluna community_type varchar(30) da tabela communities com CHECK constraint nos valores permitidos. Influencia regras de negocio como obrigatoriedade de subdivisao em quadras e limites de area.

## Valores Permitidos

| Valor | Descricao |
|-------|-----------|
| URBANA | Area urbana formal ou informal. Tipicamente subdividida em quadras e lotes. |
| RURAL | Area rural sem organizacao em quadras. Lotes maiores, ocupacao dispersa. |
| QUILOMBOLA | Comunidade remanescente de quilombo com protecao constitucional especial (Art. 68 ADCT). |
| RIBEIRINHA | Comunidade ribeirinha com ocupacao ao longo de rios e igarapes. Regras especificas de APP. |

## Impacto nas Regras

Communities do tipo URBANA tipicamente possuem Blocks e Plots. RURAL, QUILOMBOLA e RIBEIRINHA podem nao ter subdivisao em quadras, com Units vinculadas diretamente a Community sem intermediacao de Block.
