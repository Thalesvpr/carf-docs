---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-032: Redefinir Senha

## Descricao

Usuario que esqueceu senha pode solicitar redefinicao via email. Fluxo inicia na tela de login com link "Esqueci minha senha" levando a formulario de recuperacao solicitando email cadastrado. Link de recuperacao enviado automaticamente contendo URL unica com token criptografado. Token possui expiracao de 1 hora apos geracao, invalidando automaticamente apos uso bem-sucedido. Validacao de senha forte aplicada durante definicao de nova senha com feedback visual em tempo real.

## Criterios de Aceitacao

1. Link de recuperacao na tela de login
2. Email com token criptografado enviado automaticamente
3. Token expira em 1 hora ou apos uso
4. Validacao de senha forte com feedback visual
5. Sincronizacao de nova senha com Keycloak

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-001, RF-021
