# Deploy de Extensões Java (SPIs)

**Nível**: Intermediário | **Tempo**: 30-45 minutos

## Pré-requisitos

- Maven 3.9+
- Java 17+
- Docker
- Acesso ao registry (ECR/ACR/Docker Hub)

## 1. Build da Extensão

```bash
cd extensions/cpf-validator

# Build
mvn clean package

# Verificar JAR gerado
ls -lh target/cpf-validator-1.0.0.jar
```

**Output esperado**:
```
-rw-r--r-- 1 user user 45K cpf-validator-1.0.0.jar
```

## 2. Testar Localmente

```bash
# Copiar para container rodando
docker cp target/cpf-validator-1.0.0.jar carf-keycloak-dev:/opt/keycloak/providers/

# Restart Keycloak
docker restart carf-keycloak-dev

# Verificar logs
docker logs -f carf-keycloak-dev | grep "cpf-validator"
```

**Output esperado**:
```
INFO [org.keycloak.services] Deploying provider cpf-validator
INFO [org.keycloak.services] Provider cpf-validator deployed successfully
```

## 3. Ativar Extension

### Authenticator
```bash
# Via Admin Console
1. Authentication → Flows
2. Copy "Browser" flow → "Browser CARF"
3. Add execution → "CARF CPF Validator"
4. Set Required
5. Bind to realm → Browser Flow: "Browser CARF"
```

### Event Listener
```bash
# Via Admin Console
1. Events → Config
2. Event Listeners → Add "tenant-audit"
3. Save
```

## 4. Build Docker Image com Extension

```bash
# Dockerfile
FROM quay.io/keycloak/keycloak:24.0.0 AS builder
COPY themes/carf /opt/keycloak/themes/carf
COPY extensions/cpf-validator/target/cpf-validator-1.0.0.jar /opt/keycloak/providers/
RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:24.0.0
COPY --from=builder /opt/keycloak/ /opt/keycloak/
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
```

```bash
# Build
docker build -t carf/keycloak:1.1.0 .

# Test
docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin carf/keycloak:1.1.0 start-dev

# Verify provider loaded
curl http://localhost:8080/admin/realms/carf | jq '.authenticatorConfig'
```

## 5. Deploy em Staging

```bash
# Tag
docker tag carf/keycloak:1.1.0 registry.example.com/carf/keycloak:1.1.0-staging

# Push
docker push registry.example.com/carf/keycloak:1.1.0-staging

# Deploy (Kubernetes)
kubectl set image deployment/keycloak keycloak=registry.example.com/carf/keycloak:1.1.0-staging -n staging

# Wait rollout
kubectl rollout status deployment/keycloak -n staging

# Smoke test
curl https://keycloak-staging.carf.gov.br/health
```

## 6. Testing em Staging

```bash
# Test authentication flow
curl -X POST https://keycloak-staging.carf.gov.br/realms/carf/protocol/openid-connect/token \
  -d "client_id=geoweb" \
  -d "grant_type=password" \
  -d "username=123.456.789-00" \
  -d "password=test123"

# Check logs
kubectl logs -l app=keycloak -n staging | grep cpf-validator
```

## 7. Deploy em Produção

```bash
# Tag production
docker tag carf/keycloak:1.1.0 registry.example.com/carf/keycloak:1.1.0

# Push
docker push registry.example.com/carf/keycloak:1.1.0

# Deploy com rolling update
kubectl set image deployment/keycloak keycloak=registry.example.com/carf/keycloak:1.1.0 -n production

# Monitor rollout
kubectl rollout status deployment/keycloak -n production --timeout=5m
```

## 8. Rollback (se necessário)

```bash
# Rollback to previous version
kubectl rollout undo deployment/keycloak -n production

# Or specific revision
kubectl rollout history deployment/keycloak -n production
kubectl rollout undo deployment/keycloak --to-revision=2 -n production
```

## Troubleshooting

### Extension não carrega
```bash
# Verificar JAR no container
kubectl exec -it keycloak-pod -n production -- ls -la /opt/keycloak/providers/

# Verificar META-INF/services
jar -tf cpf-validator-1.0.0.jar | grep META-INF/services
```

### ClassNotFoundException
```bash
# Verificar dependencies no JAR (deve ser uber JAR)
jar -tf cpf-validator-1.0.0.jar | grep "org/apache"

# Rebuild com maven-shade-plugin
mvn clean package -P uber-jar
```

### Extension não aparece no Admin Console
```bash
# Clear cache
kubectl exec -it keycloak-pod -- rm -rf /opt/keycloak/standalone/data/cache/*
kubectl delete pod keycloak-pod
```

## Checklist

- [ ] Extension buildada com `mvn clean package`
- [ ] Testada localmente via docker cp + restart
- [ ] Ativada no Admin Console
- [ ] Dockerfile atualizado com novo JAR
- [ ] Image buildada e taggeada
- [ ] Deployed em staging
- [ ] Testes de integração passaram em staging
- [ ] Deployed em produção com rolling update
- [ ] Smoke tests passaram em produção
- [ ] Rollback plan documentado
