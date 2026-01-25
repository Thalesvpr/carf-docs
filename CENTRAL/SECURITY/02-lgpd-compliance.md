---
type: leaf
status: approved
updated: 2026-01-25
---

# LGPD Overview

Visao geral dos controles implementados no CARF para conformidade com a Lei Geral de Protecao de Dados (Lei 13.709/2018).

O sistema trata dados pessoais de cidadaos em processos de regularizacao fundiaria conforme Lei 13.465/2017. Os principais controles implementados sao consentimento explicito via checkbox nao pre-marcado antes de qualquer tratamento, finalidade especifica documentada para cada coleta, e revogacao de consentimento disponivel a qualquer momento via interface do usuario.

Os direitos dos titulares sao implementados atraves de endpoints dedicados. GET /api/lgpd/my-data fornece confirmacao e acesso aos dados pessoais. Formulario de edicao permite correcao de informacoes incorretas. Anonimizacao via delete logico preserva historico para auditoria enquanto remove identificadores pessoais. Exportacao em JSON e CSV atende o direito de portabilidade. O DPO designado recebe requisicoes via email institucional com prazo de resposta de 15 dias uteis.

A retencao de dados segue o principio da minimizacao com periodo de 5 anos pos-conclusao do processo de legitimacao para fins de auditoria fiscal. Apos expiracao, dados sao anonimizados automaticamente. Incidentes de vazamento sao reportados a ANPD dentro de 72 horas conforme exigido pela legislacao.
