---
type: workflow
status: approved
updated: 2026-01-25
category: regras
---

# Regras de Ordem do Workflow

Regras que definem a sequencia obrigatoria das etapas.

## Regras

| Regra | Descricao |
|-------|-----------|
| ORDEM-01 | PARTE 1 (Drone) DEVE ser concluida ANTES de PARTE 2 |
| ORDEM-02 | PARTE 2 (Analista) DEVE ser concluida ANTES de PARTE 3 |
| ORDEM-03 | Publicacao (PARTE 2, passo 9) e PRE-REQUISITO para PARTE 3 |
| ORDEM-04 | NAO e possivel pular etapas |

## Detalhamento

### ORDEM-01: PARTE 1 antes de PARTE 2

Sequencia obrigatoria:
1. Analista de Drone entrega ortofoto
2. Backend processa e armazena
3. Somente entao Analista do Plugin pode acessar

Sem ortofoto no bucket, nao ha o que georreferenciar.

### ORDEM-02: PARTE 2 antes de PARTE 3

Sequencia obrigatoria:
1. Analista do Plugin georreferencia poligonos
2. Analista publica trabalho
3. Somente entao Agente de Campo pode baixar

Sem poligonos publicados, nao ha o que visitar em campo.

### ORDEM-03: Publicacao como Pre-requisito

A publicacao (Passo 9 da PARTE 2) e o marco critico:
- Antes: Dados em rascunho
- Depois: Dados liberados para campo

### ORDEM-04: Sem Pular Etapas

Nao e possivel:
- Ir direto para campo sem ortofoto
- Ir direto para campo sem publicacao
- Publicar sem ortofoto processada

## Diagrama de Dependencia

```
PARTE 1 ──> PARTE 2 ──> PARTE 3
(Drone)    (Analista)  (Campo)
   │           │          │
   └──────┬────┘          │
          │               │
     Publicacao ──────────┘
     (Pre-requisito)
```
