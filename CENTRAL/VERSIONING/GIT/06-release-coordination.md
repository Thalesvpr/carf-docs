# Release Coordination

Coordenação releases polyrepo do CARF. compatibility-matrix.md documenta versões compatíveis (GEOAPI v1.2.0 compatível GEOWEB v2.1.0 REURBCAD v1.5.0). Release process: preparar release branch cada repo, atualizar changelogs, bump versions package.json/csproj, tag releases (v1.2.0), deploy staging todos repos, smoke tests integração, deploy prod coordenado (backend primeiro, depois frontends), release notes agregadas referenciando todos repos. Breaking changes comunicar com antecedência, deprecation warnings 1 release antes removal. Rollback: reverter tags, deploy versões anteriores, investigar root cause.

---

**Última atualização:** 2025-12-29
**Status do arquivo**: Pronto
