---
type: workflow
status: approved
updated: 2026-01-25
part: 2
step: 10
---

# Passo 10: Dados Liberados para Campo

Apos publicacao bem-sucedida, dados ficam disponiveis para Agentes de Campo.

## Fluxo

1. **REGRA CRITICA:** SOMENTE apos publicacao bem-sucedida
2. Backend marca dados como "liberados" para o TENANT
3. Agentes de Campo do mesmo TENANT podem acessar
4. Ortofoto + poligonos disponiveis para download temporario

## Diagrama

```
Publicacao (Passo 9)
        │
        v
  Backend marca como
    "liberados"
        │
        v
┌───────────────────┐
│  PARTE 3 HABILITADA │
│   Agentes de Campo  │
│  podem baixar pacote│
└───────────────────┘
```

## Status dos Dados

| Status | Descricao | Acesso Campo |
|--------|-----------|--------------|
| rascunho | Em edicao pelo Analista | NAO |
| publicado | Publicacao concluida | SIM |

## Conteudo Disponivel

Apos publicacao, o pacote para campo inclui:
- Ortofoto (versao para uso offline)
- Poligonos de comunidades
- Poligonos de quadras
- Poligonos de lotes
- Metadados associados

## Regra Critica

**PUB-02:** Agente de Campo SO consegue baixar dados QUANDO Analista JA PUBLICOU.

Dados NAO ficam disponiveis para campo ANTES da publicacao (PUB-04).

## Resultado

- Dados marcados como "liberados"
- Pacote disponivel para download
- **PARTE 2 CONCLUIDA**

## Proxima Parte

PARTE 3: Operacao em Campo
