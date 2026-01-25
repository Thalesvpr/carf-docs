---
type: workflow
status: approved
updated: 2026-01-25
category: regras
---

# Regras de Publicacao e Acesso

Regras que controlam a publicacao de dados e acesso pelo campo.

## Regras

| Regra | Descricao |
|-------|-----------|
| PUB-01 | Analista do Plugin SO acessa ortofotos do TENANT designado |
| PUB-02 | Agente de Campo SO consegue baixar dados QUANDO Analista JA PUBLICOU |
| PUB-03 | Download do agente e UNICO e TEMPORARIO |
| PUB-04 | Dados NAO ficam disponiveis para campo ANTES da publicacao |

## Detalhamento

### PUB-01: Acesso Restrito ao TENANT

O Analista do Plugin so visualiza e trabalha com:
- Ortofotos do TENANT ao qual foi designado
- Poligonos do TENANT
- Nao ha visibilidade cruzada entre TENANTs

### PUB-02: Dependencia de Publicacao

Esta e uma regra critica:
- O Agente de Campo depende do Analista
- Sem publicacao, nao ha download
- Backend valida se existe publicacao antes de liberar pacote

### PUB-03: Download Unico e Temporario

O pacote para campo tem restricoes:
- Link expira apos uso ou tempo limite
- Um download por link
- Evita compartilhamento indevido

### PUB-04: Controle de Liberacao

Dados so ficam disponiveis apos publicacao explicita:
- Analista deve clicar em "Publicar"
- Backend marca como "liberado"
- Antes disso, campo nao tem acesso
