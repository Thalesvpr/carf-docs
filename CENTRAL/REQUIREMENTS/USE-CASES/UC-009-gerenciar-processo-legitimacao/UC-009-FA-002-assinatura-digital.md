---
id: UC-009-FA-002
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-009-FA-002: Assinatura Digital do Termo

Fluxo alternativo do UC-009 para assinar termo digitalmente ao inves de fisicamente.

## Condicao

No passo 19 do UC-009, apos gerar PDF do termo, usuario opta por assinatura digital.

## Fluxo

1. Usuario clica em Assinar Digitalmente
2. Sistema envia documento para plataforma de assinatura
3. Sistema gera links individuais para cada signatario
4. Sistema envia emails com instrucoes aos signatarios
5. Signatarios acessam links e assinam com certificado digital
6. Plataforma notifica sistema apos todas assinaturas
7. Sistema baixa PDF assinado e atualiza processo
8. Sistema exibe badge de documento assinado digitalmente

## Signatarios

- Beneficiario principal
- Gestor municipal
- Tecnico responsavel (se REURB-E)

## Retorno

Termo assinado digitalmente com validade juridica. Processo atualizado com documento final.
