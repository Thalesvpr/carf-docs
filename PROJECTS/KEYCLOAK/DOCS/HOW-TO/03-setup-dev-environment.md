# Setup Ambiente de Desenvolvimento

Setup do ambiente de desenvolvimento Keycloak CARF para iniciantes requer Docker Desktop instalado, Git e editor VS Code ou IntelliJ IDEA. Clonar repositório e navegar para PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak, gerar secrets executando script scripts/generate-secrets.sh com chmod +x, iniciar ambiente com make dev ou docker-compose -f docker-compose.dev.yml up -d.

Verificar stack com docker ps grep keycloak listando containers, health check via curl http://localhost:8080/health, logs via docker logs -f carf-keycloak-dev. Acessar Admin Console em http://localhost:8080 com user admin e password admin.

Hot reload para temas funciona via volume mount em docker-compose.dev.yml mapeando ./themes para /opt/keycloak/themes:ro, editar tema e recarregar browser com Ctrl+Shift+R. IDE setup para VS Code requer extensões vscode-freemarker e esbenp.prettier-vscode configuradas em .vscode/extensions.json, IntelliJ IDEA para desenvolvimento SPIs Java abrindo extensions/pom.xml, Maven Reload, configurar Run Edit Configurations Remote JVM Debug com Host localhost Port 8787.

Debug remoto para SPIs Java rodando docker run -p 8080:8080 -p 8787:8787 com JAVA_OPTS incluindo agentlib:jdwp transport=dt_socket server=y suspend=n address=*:8787, depois attach debugger no IntelliJ e setar breakpoints. Quick iteration loop consiste em editar tema vim themes/carf/login/login.ftl, recarregar browser Ctrl+Shift+R, para SPIs editar código Java vim extensions/cpf-validator/src/main/java, rebuild mvn clean package, docker cp target/*.jar container:/opt/keycloak/providers/, docker restart container.

Troubleshooting comum inclui tema não recarrega resolvido limpando cache browser e cache Keycloak, Port 8080 em uso verificando docker ps -a e parando containers conflitantes, PostgreSQL não inicia resolvido com docker volume rm carf-keycloak-postgres-data e recriando. Atalhos úteis via Makefile incluem make dev para start environment, make logs para tail logs, make health para health check, make clean para stop e remove tudo, make psql para connect PostgreSQL diretamente.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
