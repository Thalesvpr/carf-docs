# Versionamento Numérico - Semantic Versioning

Sistema CARF adota Semantic Versioning SemVer especificação versionamento MAJOR.MINOR.PATCH comunicando significado mudanças releases garantindo compatibilidade previsibilidade gestão dependências coordenação polyrepo cinco projetos GEOAPI GEOWEB REURBCAD GEOGIS WEBDOCS cada um versionado independentemente releases sincronizadas documentadas release notes especificando versões compatíveis cross-project dependencies API contracts database schemas message broker events domain events integration contracts garantindo funcionamento correto sistema completo evitando breaking changes runtime failures deployment issues production incidents impactando usuários final.

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

## Coordenação Polyrepo

Releases cinco projetos coordenadas reuniões sprint planning review retrospectives definindo scope features bugfixes priorities dependencies sequencing ordering releases ensuring compatibility integration testing end-to-end scenarios user journeys workflows complete validating functionality correctness quality assurance QA manual exploratory testing automated regression suites preventing regressions defects escaping production customer-facing issues reputation damage support tickets escalations incident response firefighting postmortems root cause analysis prevention measures process improvements continuous learning growth culture blameless accountability transparency honesty.

---

**Última atualização:** 2025-01-08
