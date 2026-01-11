# PostgreSQL + PostGIS Configuration

Configuração do banco de dados PostgreSQL com extensão PostGIS para o CARF.

## Visão Geral

- **PostgreSQL 16** - Banco de dados relacional
- **PostGIS 3.4** - Extensão geoespacial
- **Row-Level Security (RLS)** - Isolamento multi-tenant
- **Docker Compose** - Setup local

## Docker Compose

Arquivo docker-compose.yml configurado com version três ponto oito definindo service postgres usando image postgis/postgis dezesseis traço três ponto quatro com container_name carf-postgres configurando environment variables POSTGRES_DB igual carf POSTGRES_USER igual postgres POSTGRES_PASSWORD igual postgres expondo ports cinco quatro três dois mapeado para cinco quatro três dois do host montando volumes postgres_data em /var/lib/postgresql/data e ./init-scripts em /docker-entrypoint-initdb.d para scripts inicialização automática configurando healthcheck executando pg_isready menos U postgres com interval dez segundos timeout cinco segundos retries cinco garantindo disponibilidade antes considerar container healthy pronto receber conexões.

## Init Scripts

### 01-enable-postgis.sql

Script SQL habilitando PostGIS extension executando CREATE EXTENSION IF NOT EXISTS postgis seguido por CREATE EXTENSION IF NOT EXISTS postgis_topology verificando PostGIS version com SELECT PostGIS_Version() confirmando instalação correta funcionalidade geoespacial disponível para uso.

### 02-enable-rls.sql

Script SQL habilitando Row-Level Security para multi-tenancy executando ALTER TABLE units ENABLE ROW LEVEL SECURITY ALTER TABLE holders ENABLE ROW LEVEL SECURITY e ALTER TABLE communities ENABLE ROW LEVEL SECURITY criando RLS policy tenant_isolation_policy em units usando USING tenant_id igual current_setting app ponto tenant_id cast uuid repetindo mesma policy para holders e communities garantindo isolamento completo dados entre tenants baseado em tenant_id session variable configurada application layer impedindo acesso cross-tenant queries automaticamente filtrados PostgreSQL engine nível row transparente para aplicação.

## Connection String

Connection string para ambiente desenvolvimento configurada com Host igual localhost Port cinco quatro três dois Database igual carf Username igual postgres Password igual postgres enquanto connection string para ambiente produção configurada com Host igual Azure PostgreSQL FQDN ponto postgres ponto database ponto azure ponto com Port cinco quatro três dois Database igual carf Username e Password substituídos por credenciais seguras gerenciadas Azure Key Vault ou secrets manager.

## Configuração GEOAPI

Arquivo appsettings.json contendo seção ConnectionStrings com propriedade DefaultConnection definida como string conexão PostgreSQL Host localhost Port cinco quatro três dois Database carf Username postgres Password postgres para desenvolvimento local. Arquivo Program.cs registrando DbContext executando builder ponto Services ponto AddDbContext parâmetro generic AppDbContext configurando options ponto UseNpgsql passando connection string obtida via builder ponto Configuration ponto GetConnectionString com parâmetro DefaultConnection e configurando extensão x ponto UseNetTopologySuite habilitando suporte PostGIS permitindo uso tipos geoespaciais NetTopologySuite mapeamento automático geometries PostgreSQL PostGIS columns para objetos .NET strongly-typed.

## Migrations

Adicionar migration executando dotnet ef migrations add MigrationName especificando menos menos project src/Infrastructure menos menos startup-project src/Gateway e aplicar migrations executando dotnet ef database update com mesmos parâmetros project e startup-project garantindo schema database sincronizado com domain model entities atualizações aplicadas ambiente desenvolvimento ou produção conforme necessário.

## Comandos Úteis

Iniciar PostgreSQL executando docker-compose up menos d rodando container background detached mode, parar PostgreSQL executando docker-compose down removendo containers mantendo volumes data persistentes, visualizar logs executando docker logs menos f carf-postgres seguindo output real-time, conectar database executando docker exec menos it carf-postgres psql menos U postgres menos d carf abrindo shell interativo PostgreSQL, criar backup executando docker exec carf-postgres pg_dump menos U postgres carf redirecionando output para arquivo backup.sql, e restaurar backup executando docker exec menos i carf-postgres psql menos U postgres menos d carf lendo input de arquivo backup.sql recriando schema e dados completos.

## Ver Também

- [GEOAPI Setup Dev Environment](../../../PROJECTS/GEOAPI/DOCS/HOW-TO/01-setup-dev-environment.md)
- [PostGIS Documentation](https://postgis.net/documentation/)
- [Row-Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
