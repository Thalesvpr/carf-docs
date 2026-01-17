# Atualizar Versão do Keycloak

Atualização de versão Keycloak nível avançado requer 2-4 horas e planejamento cuidadoso. Review changelog em keycloak.org/docs/latest/release_notes procurando breaking changes deprecations removals com grep no CHANGELOG.md.

Testar em ambiente isolado criando Dockerfile.test com nova versão FROM quay.io/keycloak/keycloak:25.0.0, build e test docker build -f Dockerfile.test -t carf/keycloak:25.0.0-test ., rodar em porta diferente docker run -p 9090:8080 carf/keycloak:25.0.0-test start-dev, testar temas acessando http://localhost:9090/realms/carf/account.

Ajustar temas se necessário verificando deprecated FreeMarker vars com grep -r deprecated themes/carf/, editar templates vim themes/carf/login/login.ftl, testar rendering via curl ao endpoint auth. Recompilar SPIs Java navegando para extensions, editando pom.xml com nova keycloak.version, rebuild mvn clean package, verificar compatibilidade de interfaces mvn test.

Database migrations gerenciadas automaticamente pelo Keycloak via Liquibase mas verificar backup antes make backup, monitorar logs durante migração docker logs keycloak grep liquibase. Staged rollout começando em dev com docker-compose up -d e testes, depois staging via kubectl set image deployment/keycloak, depois production canary com replicas=1 monitorando 24h, depois production full com scale replicas=3.

Rollback plan via kubectl rollout undo deployment/keycloak -n production para quick rollback, ou specific revision via rollout history e rollout undo --to-revision=2, database rollback se migrations falharam via make restore FILE=backups/pre-upgrade-backup.tar.gz. Checklist inclui changelog reviewed, backup criado, testado em ambiente isolado, temas ajustados e testados, SPIs recompilados, database migrations validadas, deployed em dev staging production, monitoring 24h pós-deploy, rollback plan documentado.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
