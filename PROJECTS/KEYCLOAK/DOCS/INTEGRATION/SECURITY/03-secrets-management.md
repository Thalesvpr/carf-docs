---
type: leaf
status: review
updated: 2026-01-19
---

# Gerenciamento de Secrets

Client secrets para clients confidenciais nunca commitados em repositório. Valores gerados pelo Keycloak durante criação do client e armazenados em Kubernetes Secrets ou vault corporativo. Referência via variável de ambiente em configuração da aplicação.

Kubernetes Secrets criados via kubectl create secret ou gerenciados por External Secrets Operator sincronizando com AWS Secrets Manager ou HashiCorp Vault. Secrets montados como variáveis de ambiente nos pods, não como arquivos para evitar exposição em logs de debug.

Rotação de client secrets segue processo documentado: gerar novo secret no Keycloak Admin Console, atualizar Secret no Kubernetes, aguardar propagação para pods via rolling restart, invalidar secret antigo. Janela de transição permite ambos secrets válidos temporariamente.

Credenciais de banco de dados (PostgreSQL do Keycloak) armazenadas separadamente das credenciais de aplicação. Usuário dedicado keycloak_app com permissões mínimas necessárias: CONNECT, SELECT, INSERT, UPDATE, DELETE nas tabelas do schema keycloak.

Service account credentials para GEOGIS rotacionadas mensalmente via automation. Script em keycloak/scripts/rotate-service-account.sh gera novo secret, atualiza Kubernetes Secret, e registra rotação em audit log. Alertas disparam se rotação não executada em 45 dias.

Backup de secrets críticos em vault geograficamente distribuído com acesso restrito a equipe de infraestrutura. Recovery procedure documentado e testado trimestralmente em simulação de disaster recovery.
