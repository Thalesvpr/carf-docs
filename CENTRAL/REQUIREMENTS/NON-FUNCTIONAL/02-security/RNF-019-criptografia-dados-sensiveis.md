---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-019: Criptografia de Dados Sensiveis

## Descricao

Dados sensiveis em repouso devem ser criptografados para protecao contra acesso nao autorizado ao banco de dados. Aplica-se a dados pessoais (CPF, CNPJ) e backups.

## Metricas

- Algoritmo: AES-256 para dados em repouso
- Hashing: bcrypt com salt para API keys
- Gerenciamento de chaves: Vault ou AWS KMS

## Criterios de Aceitacao

1. CPF e CNPJ criptografados no PostgreSQL com AES-256
2. API keys armazenadas com bcrypt e salt automatico
3. Backups criptografados antes de armazenamento externo
