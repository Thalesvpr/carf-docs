---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-028: Protecao de API Keys

## Descricao

API keys para integracoes server-to-server devem ser gerenciadas com rigor equivalente a senhas. Hashing forte, escopo limitado e revogacao imediata minimizam riscos.

## Metricas

- Armazenamento: hash bcrypt com custo >= 12
- Geracao: CSPRNG com minimo 32 caracteres
- Expiracao: configuravel por policy (90 dias a 1 ano)

## Criterios de Aceitacao

1. Key exibida apenas uma vez na geracao, armazenada como hash
2. Escopo de permissoes definido por key (privilegio minimo)
3. Interface para revogacao imediata disponivel
