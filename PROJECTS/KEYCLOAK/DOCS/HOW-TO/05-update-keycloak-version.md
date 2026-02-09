---
type: leaf
status: review
description: "Runbook para atualizacao de versao do Keycloak CARF"
updated: 2026-02-08
---

# Atualizar Versao do Keycloak

A atualizacao de versao do Keycloak e um procedimento de nivel avancado que requer entre 2 e 4 horas e planejamento cuidadoso. O processo comeca pela revisao do changelog em `keycloak.org/docs/latest/release_notes`, procurando breaking changes, deprecations e removals. O `CHANGELOG.md` do repositorio upstream tambem deve ser consultado.

## Teste em Ambiente Isolado

Antes de qualquer alteracao no ambiente principal, criar um `Dockerfile.test` apontando para a nova versao (por exemplo `FROM quay.io/keycloak/keycloak:25.0.0`). Fazer o build com `docker build -f Dockerfile.test -t carf/keycloak:25.0.0-test .` e executar em uma porta diferente com `docker run -p 9090:8080 carf/keycloak:25.0.0-test start-dev`. Testar os temas acessando `http://localhost:9090/realms/carf/account` para verificar a renderizacao correta.

## Ajuste de Temas

Se a nova versao introduzir mudancas nos templates FreeMarker, verificar variaveis deprecadas com `grep -r "deprecated" themes/carf/`. Editar os templates afetados (por exemplo `vim themes/carf/login/login.ftl`) e testar a renderizacao via `curl` no endpoint de autenticacao. Esse passo e especialmente importante em atualizacoes de versao major, onde a estrutura dos templates pode mudar significativamente.

## Recompilacao de SPIs Java

Navegar para o diretorio `extensions` e editar o `pom.xml` atualizando a propriedade `keycloak.version` para a nova versao. Reconstruir com `mvn clean package` e verificar a compatibilidade de interfaces executando `mvn test`. Se houver quebra de API nas SPIs do Keycloak, os testes unitarios apontarao as interfaces que precisam de ajuste.

## Migracao de Banco de Dados

As migrations de banco sao gerenciadas automaticamente pelo Keycloak via Liquibase. Antes de iniciar o processo, criar um backup com `make backup`. Durante a inicializacao com a nova versao, monitorar os logs com `docker logs keycloak | grep liquibase` para garantir que todas as migrations foram aplicadas com sucesso.

## Rollout Escalonado

O deploy da nova versao segue um rollout escalonado em quatro etapas. O ambiente de desenvolvimento e atualizado primeiro com `docker-compose up -d` seguido de testes funcionais. Em seguida, o staging recebe a atualizacao via `kubectl set image deployment/keycloak`. O proximo passo e o deploy canary em producao com `replicas=1`, monitorando por 24 horas. Finalmente, o deploy completo em producao com `kubectl scale --replicas=3` e liberado apos validacao do canary.

## Rollback

Para rollback rapido em producao, executar `kubectl rollout undo deployment/keycloak -n production`. Para reverter para uma revisao especifica, consultar o historico com `kubectl rollout history` e executar `kubectl rollout undo --to-revision=2`. Se as migrations de banco falharam, o restore do backup e necessario via `make restore FILE=backups/pre-upgrade-backup.tar.gz`.

## Verificacao Pos-Atualizacao

O procedimento completo deve garantir que o changelog foi revisado, que um backup foi criado antes da atualizacao, que a nova versao foi testada em ambiente isolado, que os temas foram ajustados e testados, que as SPIs foram recompiladas com sucesso, que as database migrations foram validadas nos logs, que o deploy passou por dev, staging e producao, que o monitoramento 24 horas pos-deploy esta ativo, e que o rollback plan esta documentado e acessivel a equipe.
