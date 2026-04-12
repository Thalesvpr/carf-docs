---
type: standard
status: current
updated: 2026-01-23
---

# STD-006: Convencoes de Links

## Regra

Links internos usam paths relativos iniciando com ponto e barra. Links para diretorios apontam para README interno. CENTRAL nao pode linkar para PROJECTS. PROJECTS deve referenciar CENTRAL para requisitos e definicoes centrais. Links quebrados sao erros criticos. Paths absolutos Windows ou Unix nao sao permitidos.

## Justificativa

Paths relativos garantem portabilidade. Isolamento CENTRAL/PROJECTS mantem fonte unica de verdade em CENTRAL evitando dependencias circulares.

## Aplicacao

Aplica-se a todos os links markdown. Validador detecta links quebrados e violacoes de isolamento. Documentos em PROJECTS devem ter rastreabilidade para requisitos em CENTRAL.
