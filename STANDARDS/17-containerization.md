---
type: standard
status: approved
updated: 2026-01-22
---

# STD-017: Docker e Kubernetes

## Regra

Todo servico deve ter Dockerfile multi-stage para build otimizado. Producao usa Kubernetes com Helm charts. Desenvolvimento usa Docker Compose.

## Justificativa

Containers garantem paridade dev/prod. K8s permite scaling horizontal, self-healing, rolling updates. Helm padroniza deploys.

## Aplicacao

Todos os servicos: GEOAPI, Keycloak, PostgreSQL, Redis. Configs em CENTRAL/DEPLOYMENTS. Imagens em registry privado.
