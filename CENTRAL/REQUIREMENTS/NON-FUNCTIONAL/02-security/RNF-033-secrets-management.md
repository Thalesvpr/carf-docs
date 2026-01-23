---
id: RNF-033
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-033: Secrets Management

## Descricao

Secrets (senhas de banco, API keys, certificados) devem ser gerenciados de forma segura sem exposicao em codigo fonte ou logs. Variaveis de ambiente ou Vault em producao.

## Metricas

- Desenvolvimento: arquivos .env nao versionados
- Producao: Kubernetes Secrets ou HashiCorp Vault
- Rotacao: trimestral para banco, semestral para API keys

## Criterios de Aceitacao

1. Nenhum secret hardcoded no codigo ou versionado no Git
2. Secrets injetados via variaveis de ambiente ou volumes em K8s
3. Scanning de codigo (git-secrets/truffleHog) no CI/CD
