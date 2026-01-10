# Atualizar Versão do Keycloak

**Nível**: Avançado | **Tempo**: 2-4 horas

## 1. Review Changelog

```bash
# Check release notes
https://www.keycloak.org/docs/latest/release_notes/

# Breaking changes
grep -i "break\|deprecat\|remov" CHANGELOG.md
```

## 2. Test em Ambiente Isolado

```bash
# Dockerfile.test
FROM quay.io/keycloak/keycloak:25.0.0

# Build e test
docker build -f Dockerfile.test -t carf/keycloak:25.0.0-test .
docker run -p 9090:8080 carf/keycloak:25.0.0-test start-dev

# Test temas
open http://localhost:9090/realms/carf/account
```

## 3. Ajustar Temas (se necessário)

```bash
# Check deprecated FreeMarker vars
grep -r "deprecated" themes/carf/

# Update templates
vim themes/carf/login/login.ftl

# Test rendering
curl http://localhost:9090/realms/carf/protocol/openid-connect/auth?...
```

## 4. Recompilar SPIs

```bash
cd extensions

# Update Keycloak version
vim pom.xml
# <keycloak.version>25.0.0</keycloak.version>

# Rebuild
mvn clean package

# Test interfaces compatibility
mvn test
```

## 5. Database Migrations

Keycloak gerencia migrations automaticamente, mas verifique:

```bash
# Backup antes de migrar
make backup

# Check migration logs
docker logs keycloak | grep liquibase
```

## 6. Staged Rollout

```bash
# 1. Dev
docker-compose -f docker-compose.dev.yml up -d
# Test

# 2. Staging
kubectl set image deployment/keycloak keycloak=carf/keycloak:25.0.0 -n staging
# Test

# 3. Production (canary)
kubectl set image deployment/keycloak keycloak=carf/keycloak:25.0.0 -n production --replicas=1
# Monitor 24h

# 4. Production (full)
kubectl scale deployment/keycloak --replicas=3 -n production
```

## 7. Rollback Plan

```bash
# Quick rollback
kubectl rollout undo deployment/keycloak -n production

# Database rollback (if migrations failed)
make restore FILE=backups/pre-upgrade-backup.tar.gz
```

## Checklist

- [ ] Changelog reviewed
- [ ] Backup criado
- [ ] Testado em ambiente isolado
- [ ] Temas ajustados e testados
- [ ] SPIs recompilados
- [ ] Database migrations validadas
- [ ] Deployed em dev → staging → production
- [ ] Monitoring 24h pós-deploy
- [ ] Rollback plan documentado
