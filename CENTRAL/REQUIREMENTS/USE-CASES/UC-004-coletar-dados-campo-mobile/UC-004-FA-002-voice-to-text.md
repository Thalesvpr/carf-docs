---
id: UC-004-FA-002
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-004-FA-002: Voice-to-Text

Fluxo alternativo do UC-004 para preenchimento de campos por ditado de voz.

## Condicao

No passo 6 do UC-004, FIELD_AGENT prefere ditar informacoes ao inves de digitar.

## Fluxo

1. FIELD_AGENT clica no icone de microfone ao lado do campo
2. Sistema ativa reconhecimento de voz
3. Sistema exibe indicador visual de escuta ativa
4. FIELD_AGENT fala as informacoes
5. Sistema transcreve audio para texto em tempo real
6. Sistema aplica formatacao basica ao texto
7. Sistema preenche campo com texto transcrito
8. FIELD_AGENT revisa e edita se necessario

## Retorno

Campo preenchido via voz. FIELD_AGENT continua para proximo campo.

## Pos-condicoes

- Texto transcrito inserido no campo
- FIELD_AGENT pode editar antes de prosseguir
