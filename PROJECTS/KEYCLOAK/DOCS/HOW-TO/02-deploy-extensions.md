# Deploy de Extensões Java (SPIs)

Deploy de extensões Java SPIs Keycloak nível intermediário requer Maven 3.9+ Java 17+ Docker e acesso ao registry. Build da extensão navegando para extensions/cpf-validator executando mvn clean package, verificar JAR gerado em target/cpf-validator-1.0.0.jar com ls -lh mostrando aproximadamente 45K.

Testar localmente copiando JAR para container rodando docker cp target/cpf-validator-1.0.0.jar carf-keycloak-dev:/opt/keycloak/providers/, restart Keycloak docker restart carf-keycloak-dev, verificar logs docker logs -f carf-keycloak-dev grep cpf-validator mostrando INFO Deploying provider cpf-validator deployed successfully.

Ativar extension tipo Authenticator via Admin Console Authentication Flows, copiar Browser flow para Browser CARF, Add execution CARF CPF Validator, Set Required, Bind to realm Browser Flow Browser CARF. Para Event Listener via Events Config, Event Listeners Add tenant-audit, Save.

Build Docker Image com extension via Dockerfile multi-stage FROM quay.io/keycloak/keycloak:24.0.0 AS builder copiando themes e extensions JAR para /opt/keycloak/providers/, executando kc.sh build, segundo stage copiando do builder para imagem final com ENTRYPOINT kc.sh. Build docker build -t carf/keycloak:1.1.0 ., test docker run -p 8080:8080 com KEYCLOAK_ADMIN vars start-dev, verificar provider loaded via curl admin realms carf jq authenticatorConfig.

Deploy em staging via docker tag para registry.example.com/carf/keycloak:1.1.0-staging, docker push, deploy Kubernetes kubectl set image deployment/keycloak -n staging, wait rollout kubectl rollout status deployment/keycloak -n staging, smoke test curl https://keycloak-staging.carf.gov.br/health.

Testing em staging testando authentication flow via curl POST token endpoint com client_id grant_type password username CPF password, verificar logs kubectl logs -l app=keycloak -n staging grep cpf-validator. Deploy em produção tag production docker tag carf/keycloak:1.1.0 registry.example.com/carf/keycloak:1.1.0, push, deploy com rolling update kubectl set image deployment/keycloak -n production, monitor rollout status timeout=5m.

Rollback se necessário via kubectl rollout undo deployment/keycloak -n production, ou specific revision via rollout history e rollout undo --to-revision=2. Troubleshooting extension não carrega verificando JAR no container kubectl exec ls -la /opt/keycloak/providers/, verificar META-INF/services via jar -tf. ClassNotFoundException verificar dependencies no JAR deve ser uber JAR, rebuild com maven-shade-plugin P uber-jar. Extension não aparece no Admin Console limpar cache kubectl exec rm -rf standalone/data/cache, delete pod.

Checklist inclui extension buildada mvn clean package, testada localmente via docker cp restart, ativada no Admin Console, Dockerfile atualizado com novo JAR, image buildada e taggeada, deployed em staging, testes integração passaram staging, deployed produção rolling update, smoke tests passaram produção, rollback plan documentado.

---

**Última atualização:** 2026-01-12
