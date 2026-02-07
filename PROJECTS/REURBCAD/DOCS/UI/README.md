---
type: readme
status: draft
updated: 2026-02-06
---

# UI - Especificacoes de Interface

Documentacao de telas, componentes e design system do REURBCAD.

## Documentos

| Documento | Descricao |
|-----------|-----------|
| [01-screen-specs.md](01-screen-specs.md) | Especificacao de telas com correcoes aplicadas |

## Fonte de Verdade

As regras de negocio estao em `CENTRAL/DOMAIN-RULES/VALIDATIONS/`:
- `12-field-registration-rules.md` - Regras de campos e formularios
- `09-holder-validation.md` - Validacao de titular
- `11-unit-validation.md` - Validacao de unidade

## Figma

TODO: Adicionar link do projeto Figma

## Correcoes Importantes (2026-02-06)

1. **Autenticacao**: Keycloak proprio (NAO Gov.br)
2. **Filiacao**: Campo unico opcional (nao 2 campos obrigatorios)
3. **Tempo de moradia**: Declaratorio ("5 anos"), nao data MM/AAAA
4. **Status**: 3 categorias separadas (Atendimento, Ocupante, Utilizacao)
5. **Assinatura**: Vinculada via `signature_path` ao cadastro
