# Commit Conventions

Conventional Commits do CARF para changelogs automáticos. Formato: type(scope): description. Types: feat (new feature), fix (bug fix), docs (documentation), style (formatting), refactor (code restructure), test (tests), chore (maintenance). Scopes: auth, units, holders, communities, api, db, ui. Exemplos: feat(auth): add Keycloak SSO integration, fix(units): validate polygon self-intersection, docs(api): update authentication endpoints. Breaking changes: feat\!: ou BREAKING CHANGE: no body. Tools: commitlint validando formato pre-commit hook, standard-version gerando CHANGELOG.md e bumping version automaticamente. Benefits: changelog legível, semantic versioning automático, filtrar commits por type/scope.

---

**Última atualização:** 2025-12-29
