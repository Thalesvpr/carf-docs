---
type: leaf
status: review
updated: 2026-02-08
---

# Setup Ambiente de Desenvolvimento

O setup do ambiente de desenvolvimento Keycloak CARF e direcionado a iniciantes e requer Docker Desktop instalado, Git e um editor como VS Code ou IntelliJ IDEA.

## Clone e Inicializacao

O primeiro passo e clonar o repositorio e navegar para `PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak`. Em seguida, gerar os secrets executando o script `scripts/generate-secrets.sh` (garantindo permissao de execucao com `chmod +x`). Para iniciar o ambiente, executar `make dev` ou diretamente `docker-compose -f docker-compose.dev.yml up -d`.

## Verificacao da Stack

Apos a inicializacao, verificar os containers em execucao com `docker ps | grep keycloak`. O health check pode ser confirmado via `curl http://localhost:8080/health` e os logs acompanhados com `docker logs -f carf-keycloak-dev`. O Admin Console estara disponivel em `http://localhost:8080` com usuario `admin` e senha `admin`.

## Hot Reload de Temas

O hot reload para temas funciona atraves de volume mount configurado no `docker-compose.dev.yml`, mapeando `./themes` para `/opt/keycloak/themes:ro`. Apos editar qualquer arquivo do tema, basta recarregar o browser com Ctrl+Shift+R para ver as alteracoes sem reiniciar o container.

## Configuracao de IDE

Para VS Code, as extensoes necessarias sao `vscode-freemarker` e `esbenp.prettier-vscode`, ja configuradas em `.vscode/extensions.json`. Para IntelliJ IDEA, o desenvolvimento de SPIs Java e feito abrindo `extensions/pom.xml`, executando Maven Reload, e configurando um perfil de debug remoto em Run > Edit Configurations > Remote JVM Debug com Host `localhost` e Port `8787`.

## Debug Remoto para SPIs Java

O debug remoto exige que o Keycloak seja iniciado com portas adicionais: `docker run -p 8080:8080 -p 8787:8787` incluindo nas JAVA_OPTS o parametro `agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8787`. Com o container rodando, fazer attach do debugger no IntelliJ e setar breakpoints no codigo das SPIs.

## Ciclo Rapido de Iteracao

Para temas, o ciclo consiste em editar o template (por exemplo `vim themes/carf/login/login.ftl`) e recarregar o browser com Ctrl+Shift+R. Para SPIs Java, o ciclo e mais longo: editar o codigo fonte em `extensions/cpf-validator/src/main/java`, reconstruir com `mvn clean package`, copiar o JAR atualizado para o container com `docker cp target/*.jar container:/opt/keycloak/providers/`, e reiniciar o container com `docker restart`.

## Troubleshooting Comum

Quando o tema nao recarrega, a solucao e limpar o cache do browser e tambem o cache interno do Keycloak. Se a porta 8080 estiver em uso, verificar com `docker ps -a` quais containers estao ativos e parar os conflitantes. Quando o PostgreSQL nao inicia, remover o volume com `docker volume rm carf-keycloak-postgres-data` e recriar o ambiente.

## Atalhos via Makefile

O Makefile do projeto disponibiliza comandos uteis para o dia a dia do desenvolvimento.

| Comando      | Descricao                          |
|--------------|------------------------------------|
| `make dev`   | Inicia o ambiente de desenvolvimento |
| `make logs`  | Acompanha os logs em tempo real    |
| `make health`| Executa health check               |
| `make clean` | Para e remove todos os containers  |
| `make psql`  | Conecta ao PostgreSQL diretamente  |
