---
id: UC-004-FA-003
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-004-FA-003: Copiar Unidade Anterior

Fluxo alternativo do UC-004 para copiar dados de unidade anterior em areas homogeneas.

## Condicao

No passo 4 do UC-004, FIELD_AGENT esta cadastrando unidades adjacentes com caracteristicas similares.

## Fluxo

1. FIELD_AGENT clica em Copiar da Ultima
2. Sistema busca ultima unidade cadastrada localmente
3. Sistema pre-preenche formulario com dados copiados
4. Sistema mantem vazios campos unicos (numero, geometria, fotos, titulares)
5. FIELD_AGENT ajusta numero do endereco
6. FIELD_AGENT desenha nova geometria
7. FIELD_AGENT tira fotos especificas
8. FIELD_AGENT cadastra titulares da unidade atual

## Dados Copiados

- Endereco (logradouro, bairro, cidade, CEP)
- Tipo de unidade
- Observacoes genericas

## Dados Nao Copiados

- Numero do endereco
- Geometria
- Fotos
- Titulares
- Localizacao GPS

## Retorno

Formulario pre-preenchido. FIELD_AGENT ajusta detalhes especificos da unidade atual.
