---
type: leaf
status: review
description: "Runbook para deploy de extensões Java SPIs no Keycloak CARF"
updated: 2026-02-08
---

# Deploy de Extensoes Java (SPIs)

O deploy de extensoes Java SPIs no Keycloak CARF e um procedimento de nivel intermediario que requer Maven 3.9+, Java 17+, Docker e acesso ao registry de imagens. Este guia cobre desde o build local ate o deploy em producao com rollback plan.

## Build da Extensao

O processo de build comeca navegando para o diretorio da extensao em `extensions/cpf-validator` e executando `mvn clean package`. Apos a compilacao, o JAR gerado estara disponivel em `target/cpf-validator-1.0.0.jar`. Verificar o artefato com `ls -lh` deve mostrar aproximadamente 45K de tamanho.

## Teste Local via Docker

Para testar localmente, copiar o JAR para o container em execucao com `docker cp target/cpf-validator-1.0.0.jar carf-keycloak-dev:/opt/keycloak/providers/`. Em seguida, reiniciar o Keycloak com `docker restart carf-keycloak-dev`. Verificar os logs com `docker logs -f carf-keycloak-dev | grep cpf-validator` deve mostrar a mensagem `INFO Deploying provider cpf-validator deployed successfully`.

## Ativacao no Admin Console

A ativacao depende do tipo de extensao. Para extensoes do tipo Authenticator, acessar Authentication > Flows no Admin Console, copiar o flow Browser para um novo flow chamado "Browser CARF", adicionar a execution "CARF CPF Validator", definir como Required, e vincular ao realm em Browser Flow selecionando "Browser CARF". Para extensoes do tipo Event Listener, acessar Events > Config, adicionar "tenant-audit" em Event Listeners e salvar.

## Build da Docker Image com Extensao

O Dockerfile utiliza multi-stage build. O primeiro stage parte de `quay.io/keycloak/keycloak:24.0.0 AS builder`, copiando themes e o JAR da extensao para `/opt/keycloak/providers/`, e executando `kc.sh build`. O segundo stage copia os artefatos do builder para a imagem final com `ENTRYPOINT ["kc.sh"]`. O build e feito com `docker build -t carf/keycloak:1.1.0 .`. Para testar, executar `docker run -p 8080:8080` com as variaveis KEYCLOAK_ADMIN e modo `start-dev`, verificando que o provider foi carregado via `curl` no endpoint admin realms carf consultando `authenticatorConfig` com `jq`.

## Deploy em Staging

O deploy em staging comeca com o tagging da imagem para o registry via `docker tag carf/keycloak:1.1.0 registry.example.com/carf/keycloak:1.1.0-staging` seguido de `docker push`. O deploy no Kubernetes e feito com `kubectl set image deployment/keycloak -n staging` e o aguardo do rollout com `kubectl rollout status deployment/keycloak -n staging`. O smoke test consiste em acessar `curl https://keycloak-staging.carf.gov.br/health`.

## Testes em Staging e Deploy em Producao

Os testes em staging devem validar o authentication flow via `curl POST` no token endpoint com `client_id`, `grant_type=password`, `username` (CPF) e `password`. Verificar tambem os logs com `kubectl logs -l app=keycloak -n staging | grep cpf-validator`.

Para o deploy em producao, taguear a imagem com `docker tag carf/keycloak:1.1.0 registry.example.com/carf/keycloak:1.1.0`, fazer push, e executar o deploy com rolling update via `kubectl set image deployment/keycloak -n production`. Monitorar o rollout status com timeout de 5 minutos.

## Rollback

Em caso de problemas, executar `kubectl rollout undo deployment/keycloak -n production` para rollback imediato. Para rollback para uma revisao especifica, consultar o historico com `kubectl rollout history` e executar `kubectl rollout undo --to-revision=2`.

## Troubleshooting

Quando uma extensao nao carrega, verificar se o JAR esta presente no container com `kubectl exec -- ls -la /opt/keycloak/providers/` e se o arquivo `META-INF/services` esta correto inspecionando via `jar -tf`. Se ocorrer ClassNotFoundException, o problema geralmente e de dependencias ausentes no JAR; a extensao deve ser empacotada como uber JAR, reconstruindo com `maven-shade-plugin -P uber-jar`. Se a extensao nao aparece no Admin Console, limpar o cache com `kubectl exec -- rm -rf standalone/data/cache` e deletar o pod para forca-lo a reiniciar.

## Verificacao Pos-Deploy

O procedimento completo deve garantir que a extensao foi buildada com `mvn clean package`, testada localmente via `docker cp` e restart, ativada no Admin Console, que o Dockerfile foi atualizado com o novo JAR, que a imagem foi buildada e taggeada, que o deploy em staging foi realizado com testes de integracao passando, que o deploy em producao foi feito com rolling update, que os smoke tests passaram em producao, e que o rollback plan esta documentado e validado.
