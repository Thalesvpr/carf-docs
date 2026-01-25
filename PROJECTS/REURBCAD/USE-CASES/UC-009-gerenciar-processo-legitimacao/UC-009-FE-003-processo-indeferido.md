---
id: UC-009-FE-003
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-009-FE-003: Processo Indeferido

Fluxo de excecao do UC-009 quando MANAGER decide indeferir processo por impedimento legal.

## Condicao

No passo 17 do UC-009, MANAGER identifica impedimento que impossibilita aprovacao.

## Fluxo

1. MANAGER revisa processo e documentacao
2. MANAGER identifica impedimento legal ou documental
3. MANAGER clica em Indeferir
4. Sistema exibe modal solicitando justificativa obrigatoria
5. MANAGER descreve motivo detalhado do indeferimento
6. MANAGER confirma indeferimento
7. Sistema atualiza status para Indeferido
8. Sistema arquiva processo impedindo edicoes futuras
9. Sistema notifica ANALYST criador com justificativa
10. Processo movido para aba Arquivados

## Motivos Comuns

- Beneficiario nao comprova tempo minimo de posse
- Area excede limite para modalidade solicitada
- Documentacao insuficiente e nao corrigivel
- Impedimento legal especifico

## Retorno

Processo arquivado definitivamente. Novo processo necessario se beneficiario corrigir impedimentos.
