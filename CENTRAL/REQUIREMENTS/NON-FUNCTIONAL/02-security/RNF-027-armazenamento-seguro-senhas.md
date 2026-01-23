---
id: RNF-027
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-027: Armazenamento Seguro de Senhas

## Descricao

Keycloak deve armazenar senhas com hashing forte resistente a forca bruta. Mesmo com banco comprometido, senhas originais nao podem ser recuperadas.

## Metricas

- Algoritmo: bcrypt com work factor minimo 12
- Salting: automatico por senha
- Politica: minimo 8 caracteres, maiusculas, numeros e simbolos

## Criterios de Aceitacao

1. Senhas armazenadas como hash bcrypt com custo >= 12
2. Politica de senha forte configurada no Keycloak
3. Bloqueio temporario apos multiplas tentativas falhadas
