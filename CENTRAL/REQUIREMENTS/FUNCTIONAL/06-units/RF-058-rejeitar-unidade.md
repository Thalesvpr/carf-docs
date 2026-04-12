---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-058: Rejeitar Unidade

## Descricao

Sistema deve permitir que usuarios com perfil MANAGER rejeitem unidades inadequadas ou com problemas de cadastro. Rejeicao exige obrigatoriamente preenchimento de campo de justificativa explicando os motivos da nao aprovacao. Justificativa deve orientar o analista sobre quais aspectos precisam ser corrigidos. Status alterado para REJECTED com notificacao automatica ao usuario criador incluindo a justificativa e link para edicao.

## Criterios de Aceitacao

1. Botao de rejeicao visivel para MANAGER
2. Justificativa obrigatoria na rejeicao
3. Status alterado para REJECTED
4. Notificacao automatica com justificativa
5. Link para edicao na notificacao

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-056, RF-033
