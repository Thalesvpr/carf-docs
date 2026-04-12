---
type: leaf
status: review
updated: 2026-02-08
---

# Health Controller

O Health Controller expoe endpoints de verificacao de saude da aplicacao utilizados pelo Kubernetes para liveness e readiness probes, alem de monitoramento externo. Nao requer autenticacao pois e acessado por infraestrutura de orquestracao.

## Endpoints

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| GET | /health | Health check basico | 200 | 503 | anonimo |
| GET | /health/ready | Readiness check completo | 200 | 503 | anonimo |

## Comportamento

O endpoint /health retorna status Healthy quando a aplicacao esta respondendo, utilizado como liveness probe do Kubernetes com initial delay de 10 segundos e period de 30 segundos. Se a aplicacao nao responde, o Kubernetes reinicia o pod. O endpoint /health/ready executa verificacoes detalhadas de conectividade com dependencias: conexao com PostgreSQL via query SELECT 1, conexao com Redis via ping e acessibilidade do Keycloak via endpoint OIDC discovery. O response retorna objeto com status geral (Healthy ou Unhealthy) e status individual de cada dependencia. O Kubernetes utiliza este endpoint como readiness probe, removendo o pod do balanceamento de carga quando Unhealthy e reintroduzindo quando volta a Healthy.

## Autorizacao

Ambos os endpoints sao anonimos (sem atributo Authorize) pois precisam ser acessiveis por probes do Kubernetes e sistemas de monitoramento que nao possuem tokens JWT. O endpoint /health/ready nao expoe detalhes de conexao (hostnames, portas) nas respostas, retornando apenas status booleano por dependencia.
