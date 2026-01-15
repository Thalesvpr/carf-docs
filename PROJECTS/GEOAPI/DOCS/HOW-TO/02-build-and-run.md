# Build and Run

Build do GEOAPI usa dotnet build na raiz do projeto compilando solução completa Domain Application Infrastructure Gateway layers gerando assemblies em bin/Debug/net9.0/, build específico por projeto com dotnet build src/Carf.GEOAPI.Domain ou Application ou Infrastructure ou Gateway, build Release com dotnet build --configuration Release para produção, clean com dotnet clean removendo artefatos e dotnet clean && dotnet build para rebuildar do zero, restore com dotnet restore restaurando dependências NuGet ou dotnet restore --force para forçar redownload de packages.

Rodar API em development mode com dotnet watch run --project src/Carf.GEOAPI.Gateway para hot reload automático ou dotnet run sem hot reload, porta específica via --urls https://localhost:8001, variáveis de ambiente definidas export ASPNETCORE_ENVIRONMENT=Development Linux macOS ou set no Windows, rodar inline ASPNETCORE_ENVIRONMENT=Staging dotnet run para ambientes específicos. Production mode requer build Release primeiro depois dotnet run --project src/Carf.GEOAPI.Gateway --configuration Release --no-build ou executar DLL diretamente dotnet bin/Release/net9.0/Carf.GEOAPI.Gateway.dll, Swagger UI disponível em https://localhost:7001/swagger.

Migrations via EF Core CLI navegando para src/Carf.GEOAPI.Infrastructure executando dotnet ef migrations add NomeMigration --startup-project ../Carf.GEOAPI.Gateway --context AppDbContext criando nova migration, aplicar com dotnet ef database update mesmos flags, aplicar até migration específica passando nome, reverter todas com database update 0 CUIDADO, gerar SQL script com dotnet ef migrations script --output migrations.sql ou --idempotent para script executável múltiplas vezes, remover última migration com dotnet ef migrations remove antes de aplicar ou --force depois de aplicada.

Testes com dotnet test na raiz executando todos unit tests Domain Application e integration tests Infrastructure Gateway, logger verboso --logger console;verbosity=detailed, filtro por categoria --filter Category=Unit ou Category=Integration, testes por projeto dotnet test tests/Carf.GEOAPI.Domain.Tests, coverage via dotnet tool install --global dotnet-coverage depois dotnet test --collect:XPlat Code Coverage gerando coverage.cobertura.xml, reportgenerator para HTML em coverage-report/, filtros por nome classe FullyQualifiedName~UnitTests ou método Name=CreateUnit_ShouldSucceed ou múltiplos Category=Unit&Priority=High.

Docker build com docker build -t carf-geoapi:latest . ou com argumentos --build-arg ASPNETCORE_ENVIRONMENT=Production -t carf-geoapi:v1.0.0, rodar container docker run -d --name geoapi -p 8080:8080 -e ASPNETCORE_ENVIRONMENT=Production -e ConnectionStrings__DefaultConnection=Host=postgres passando connection string, ver logs docker logs -f geoapi, parar docker stop geoapi, remover docker rm geoapi. Docker Compose em docker-compose.yml definindo services api build context ports 8080:8080 environment ASPNETCORE_ENVIRONMENT Production ConnectionStrings depends_on postgres condition service_healthy, service postgres image postgis/postgis:16-3.4 environment POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD healthcheck pg_isready, subir stack docker-compose up -d ver logs docker-compose logs -f parar docker-compose down.

Publish local com dotnet publish src/Carf.GEOAPI.Gateway --configuration Release --output ./publish gerando DLL executável, publish self-contained incluindo runtime .NET com --runtime linux-x64 --self-contained true --output ./publish-linux gerando executável nativo ./publish-linux/Carf.GEOAPI.Gateway, publish Azure via az webapp up --name carf-geoapi --resource-group carf-rg --runtime DOTNETCORE:9.0 após az login.

Performance benchmarks com BenchmarkDotNet package rodando dotnet run --project tests/Carf.GEOAPI.Benchmarks --configuration Release, profiling com dotnet-trace tool collect --process-id PID capturando trace para análise com PerfView Windows.

Checklist pré-deploy verifica build sem erros dotnet build --configuration Release, testes passando dotnet test, coverage maior que 80% via collect, migrations aplicadas dotnet ef database update, Swagger documentado em /swagger, health checks funcionando curl /health, logs estruturados em JSON, variáveis ambiente configuradas em appsettings.Production.json.

## Referências

Documentação .NET CLI comandos build run test publish disponível Microsoft Learn, Entity Framework Core Tools migrations scaffold database update, Docker Build containerização imagens layers, ASP.NET Core Deployment hosting produção IIS Kestrel Nginx encontram-se documentados nos sites oficiais Microsoft Docker.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
