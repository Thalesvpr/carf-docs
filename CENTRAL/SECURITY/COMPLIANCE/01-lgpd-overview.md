---
type: leaf
status: draft
updated: 2026-01-22
---

# LGPD Overview

Visao geral dos controles implementados no CARF para conformidade com a Lei Geral de Protecao de Dados (Lei 13.709/2018).

O sistema trata dados pessoais de cidadaos em processos de regularizacao fundiaria conforme Lei 13.465/2017. Os principais controles implementados sao: consentimento explicito via checkbox nao pre-marcado antes de qualquer tratamento, finalidade especifica documentada para cada coleta, e revogacao de consentimento disponivel a qualquer momento via interface do usuario.

Os direitos dos titulares sao implementados atraves de endpoints dedicados: GET /api/lgpd/my-data para confirmacao e acesso aos dados, formulario de edicao para correcao, anonimizacao via delete logico preservando historico para auditoria, exportacao JSON/CSV para portabilidade, e contestacao de decisoes automatizadas. O DPO designado recebe requisicoes via dpo@carf.gov.br com prazo de resposta de 15 dias uteis.

A retencao de dados segue o principio da minimizacao com periodo de 5 anos pos-conclusao do processo de legitimacao para fins de auditoria fiscal. Apos expiracao, dados sao anonimizados automaticamente. Incidentes de vazamento sao reportados a ANPD dentro de 72 horas conforme procedimento em [INCIDENTS/03-breach-notification](../INCIDENTS/03-breach-notification.md).
