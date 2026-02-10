---
type: leaf
status: review
updated: 2026-02-07
---

# Topologia de Deployment

Mostra a arquitetura de implantacao em producao com containers Kubernetes, load balancer, clusters de banco de dados e servicos de observabilidade.

## Camada de Entrada

Usuarios acessam o sistema pela internet. Assets estaticos sao servidos via CDN. Todo trafego passa por um load balancer (Nginx ou Traefik) com SSL termination antes de chegar ao cluster Kubernetes.

## Cluster Kubernetes

| Grupo de Pods | Replicas | Servico |
|---------------|----------|---------|
| Web Pods | 2 | GEOWEB (React SPA) |
| API Pods | 3 | GEOAPI (.NET 9 REST API) |
| Auth Pods | 2 | Keycloak (OAuth2/OIDC) |
| Docs Pods | 1 | WEBDOCS (Astro/Starlight) |

O load balancer distribui trafego entre os pods conforme o tipo de requisicao. API Pods e Auth Pods possuem replicas para alta disponibilidade.

## Database Cluster

PostgreSQL opera com replicacao primary-replica. O primary recebe escritas dos API Pods e Auth Pods. O replica atende leituras para balanceamento de carga.

## Object Storage

Bucket S3/MinIO armazena documentos, ortofotos e fotos. Acessado exclusivamente pelos API Pods via URLs presigned.

## Observabilidade

| Servico | Funcao |
|---------|--------|
| Prometheus | Coleta de metricas dos API Pods e Auth Pods |
| Grafana | Dashboards de visualizacao das metricas |
| Loki | Agregacao de logs dos API Pods |

API Pods e Auth Pods exportam metricas para Prometheus e enviam logs para Loki. Grafana consome dados do Prometheus para dashboards operacionais.
