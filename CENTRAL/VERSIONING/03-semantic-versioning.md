# Versionamento Numérico - Semantic Versioning

Sistema CARF adota Semantic Versioning SemVer especificação versionamento MAJOR.MINOR.PATCH comunicando significado mudanças releases garantindo compatibilidade previsibilidade gestão dependências coordenação polyrepo oito projetos TSCORE GEOAPI GEOWEB REURBCAD GEOGIS WEBDOCS ADMIN cada um versionado independentemente releases sincronizadas documentadas release notes especificando versões compatíveis cross-project dependencies API contracts database schemas message broker events domain events integration contracts biblioteca compartilhada @carf/tscore consumida por projetos TypeScript GEOWEB REURBCAD ADMIN WEBDOCS garantindo funcionamento correto sistema completo evitando breaking changes runtime failures deployment issues production incidents impactando usuários final.

## Formato Versionamento

**MAJOR.MINOR.PATCH** onde MAJOR incrementado mudanças incompatíveis breaking changes API alterações signature métodos remoção endpoints fields obrigatórios novos alteração comportamento existente backward incompatible requiring client updates migrations data transformations. MINOR incrementado funcionalidades novas backward compatible adição endpoints novos fields opcionais responses features expandindo capabilities mantendo compatibilidade clientes existentes sem necessidade updates imediatos gradual adoption optional. PATCH incrementado bug fixes correções defeitos comportamento incorreto sem alterar funcionalidades existentes mantendo compatibilidade completa backward forward safe updates automatic deployments zero risk regressions breaking changes.

## Estratégia Releases

Releases coordenadas polyrepo incluem release notes markdown documentando mudanças cada projeto versões compatíveis dependencies exemplo GEOAPI v2.5.0 compatível GEOWEB v1.8.0 até v1.10.x REURBCAD v0.9.5+ especificando ranges suportados evitando combinações incompatíveis deployment failures integration issues runtime errors API contracts violated schemas mismatched events malformed unprocessable. Git tags semantic format v1.2.3 trigger CI/CD pipelines GitHub Actions workflows automaticamente building testing deploying staging environments smoke tests validating health readiness promoting production blue-green deployment zero downtime canary releases gradual rollout monitoring error rates latency metrics alerting incidents rollback automatic restoring previous stable version disaster recovery.

## Changelog Manutenção

CHANGELOG.md raiz cada repositório mantido atualizado releases documentando mudanças categorias Added novas funcionalidades Changed alterações funcionalidades existentes Deprecated funcionalidades marcadas remoção futura Removed funcionalidades removidas Fixed bugs corrigidos Security vulnerabilidades corrigidas urgência critical high medium low impacto usuários business operations compliance regulations. Conventional Commits padrão mensagens commits facilitando geração automática changelog parsing commits extração metadata tipo scope breaking changes footers linking issues pull requests traceability rastreabilidade bidirectional requisitos código testes deployment production validation.

## API Versioning

APIs REST versionadas via header HTTP api-version client especifica versão desejada request servidor responde version suportada ou error unsupported version requiring upgrade downgrade compatibility matrix documented public API documentation Swagger OpenAPI specification endpoints schemas examples responses error codes facilitating client implementation testing integration. Versionamento header preferível URL path /api/v1/resource evitando proliferação endpoints duplicação controllers logic maintenance overhead deprecation policy gradual sunsetting old versions notifications clients advance warning migration guides documentation examples code snippets facilitating transition minimizing friction adoption resistance.

## Database Migrations

Migrations database schema versionadas numericamente sequenciais 001_initial_schema.sql 002_add_units_table.sql 003_alter_holders_add_cpf.sql aplicadas ordem incremental up migrations forward progressing down migrations rollback reverting changes disaster recovery development testing environments reset clean state. Migrations additive apenas adicionam colunas tabelas indexes constraints nunca removem immediately deprecate first mark nullable default values populate data backfill transformations after grace period remove definitively preventing breaking changes applications queries depending schema structure field existence data types constraints foreign keys cascade deletes updates.

## Versionamento @carf/tscore

Biblioteca compartilhada TypeScript @carf/tscore publicada GitHub Packages versionada estritamente seguindo SemVer onde MAJOR incrementado breaking changes em value objects (alterar signature CPF.validate(), remover método público, mudar comportamento validação rejeitando inputs anteriormente válidos), types (remover field entity, tornar field nullable em non-nullable, renomear interfaces), enums (remover valor enum, alterar hierarchia Role levels), e auth (mudar return type useAuth(), remover propriedade AuthContext, alterar contract KeycloakClient methods) exigindo updates coordenados projetos consumidores GEOWEB REURBCAD ADMIN WEBDOCS com code changes necessários migration guide detalhado CHANGELOG. MINOR incrementado adicionando novas funcionalidades backward compatible como novos value objects (CREA, GeoPoint, Address), novas entities/types (Survey, Monument, Annotation), novos campos opcionais em interfaces existentes, novos hooks/composables React/Vue, e novas utility functions mantendo APIs existentes inalteradas permitindo adoption gradual opcional sem breaking existing code. PATCH incrementado corrigindo bugs em validations (fix edge case CPF algorithm, corrigir regex Email validation), type definitions (ajustar nullability incorreta, adicionar missing fields), e authentication (fix token refresh timing, corrigir role checking logic) sem alterar public APIs mantendo compatibilidade completa permitindo updates automáticos via dependabot/renovate sem risk regression.

Projetos consumidores especificam dependency @carf/tscore em package.json usando range operators `^0.1.0` permitindo updates MINOR e PATCH automáticos (^0.1.0 aceita 0.1.1, 0.2.0 mas rejeita 1.0.0) ou `~0.1.0` permitindo apenas PATCH (aceita 0.1.1, 0.1.2 mas rejeita 0.2.0) conforme risk tolerance, CI/CD roda testes projetos consumidores contra latest tscore version candidate antes publicar garantindo non-breaking, e updates coordenados via PRs simultâneos quando breaking changes inevitáveis.

## Coordenação Polyrepo

Releases oito projetos coordenadas reuniões sprint planning review retrospectives definindo scope features bugfixes priorities dependencies sequencing ordering releases ensuring compatibility integration testing end-to-end scenarios user journeys workflows complete validating functionality correctness quality assurance QA manual exploratory testing automated regression suites preventing regressions defects escaping production customer-facing issues reputation damage support tickets escalations incident response firefighting postmortems root cause analysis prevention measures process improvements continuous learning growth culture blameless accountability transparency honesty.

---

**Última atualização:** 2025-01-08
**Status do arquivo**: Pronto
