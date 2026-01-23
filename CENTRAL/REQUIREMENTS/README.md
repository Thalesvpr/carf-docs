---
type: readme
status: review
updated: 2026-01-22
---

# REQUIREMENTS

O QUE o sistema faz. Funcionalidades e casos de uso organizados por dominio.

## Estrutura

| Pasta | Proposito |
|-------|-----------|
| [FUNCTIONAL](./FUNCTIONAL/README.md) | Requisitos funcionais atomicos por dominio |
| [NON-FUNCTIONAL](./NON-FUNCTIONAL/README.md) | Requisitos de qualidade (performance, seguranca) |
| [USE-CASES](./USE-CASES/README.md) | Fluxos completos de interacao usuario-sistema |

## Principio

- **RF**: Funcionalidade atomica - "Sistema permite criar unidade"
- **UC**: Fluxo completo - "Usuario seleciona comunidade, preenche form, salva"
- **RNF**: Metrica de qualidade - "Resposta em menos de 2 segundos"

## Hierarquia

Requisitos funcionais definem capacidades. Casos de uso documentam jornadas completas referenciando RFs. Requisitos nao-funcionais estabelecem metricas de qualidade transversais.

<!-- CARF-INDEX-START -->
## Subpastas

- [[CENTRAL/REQUIREMENTS/FUNCTIONAL/README|FUNCTIONAL]]
- [[CENTRAL/REQUIREMENTS/NON-FUNCTIONAL/README|NON-FUNCTIONAL]]
- [[CENTRAL/REQUIREMENTS/USE-CASES/README|USE-CASES]]

<!-- CARF-INDEX-END -->
