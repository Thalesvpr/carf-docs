# NON-FUNCTIONAL-REQUIREMENTS

Requisitos não-funcionais do CARF especificando atributos de qualidade e restrições técnicas do sistema incluindo performance (tempo resposta, throughput, latência), escalabilidade (concurrent users, data volume), disponibilidade (uptime, SLA), segurança (autenticação, autorização, criptografia, LGPD), usabilidade (acessibilidade WCAG, responsividade), compatibilidade (browsers, devices, OS), e manutenibilidade (code coverage, technical debt). Cada RNF segue nomenclatura RNF-NNN-titulo-descritivo.md, possui metadados YAML (categoria, prioridade, impacto), descrição detalhada da restrição ou atributo de qualidade, métricas quantificáveis para verificação (ex: tempo resposta < 200ms p95, uptime > 99.5%), e rastreabilidade para UCs e RFs afetados. Organizados por categoria: performance (RNF-001 a RNF-030), security (RNF-031 a RNF-045), scalability (RNF-046 a RNF-060), compatibility (RNF-061 a RNF-075), e usability (RNF-076 a RNF-085).

## Navegação

**[index-by-epic.md](./index-by-epic.md)** - Índice de todos os 85 Requisitos Não-Funcionais organizados por épica (performance, security, scalability, compatibility, usability)

Documentação complementar de requirements inclui [overview completo](../README.md) apresentando estrutura hierárquica de 11 UCs 221 RFs 140 USs e 85 RNFs com estatísticas de cobertura por módulo e épica, [índice por módulo](../index-by-module.md) organizando requirements conforme projetos implementadores GEOWEB REURBCAD GEOAPI GEOGIS facilitando descoberta de atributos de qualidade por equipe de desenvolvimento, e [matriz de rastreabilidade](../traceability-matrix.md) mapeando relacionamentos bidirecionais UC→RF→US→RNF estabelecendo conexões explícitas entre casos de uso requisitos funcionais user stories e requisitos não-funcionais.

---

**Última atualização:** 2026-01-10
