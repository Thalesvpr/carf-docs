# NON-FUNCTIONAL-REQUIREMENTS

Requisitos não-funcionais do CARF especificando atributos de qualidade e restrições técnicas do sistema incluindo performance (tempo resposta, throughput, latência), escalabilidade (concurrent users, data volume), disponibilidade (uptime, SLA), segurança (autenticação, autorização, criptografia, LGPD), usabilidade (acessibilidade WCAG, responsividade), compatibilidade (browsers, devices, OS), e manutenibilidade (code coverage, technical debt). Cada RNF segue nomenclatura RNF-NNN-titulo-descritivo.md, possui metadados YAML (categoria, prioridade, impacto), descrição detalhada da restrição ou atributo de qualidade, métricas quantificáveis para verificação (ex: tempo resposta < 200ms p95, uptime > 99.5%), e rastreabilidade para UCs e RFs afetados. Organizados por categoria: performance (RNF-001 a RNF-030), security (RNF-031 a RNF-045), scalability (RNF-046 a RNF-060), compatibility (RNF-061 a RNF-075), e usability (RNF-076 a RNF-085).

## Navegação

Documentação complementar de requirements inclui [overview completo](../README.md) apresentando estrutura hierárquica de 11 UCs 221 RFs 140 USs e 85 RNFs com estatísticas de cobertura por módulo e épica organizando requirements conforme projetos implementadores GEOWEB REURBCAD GEOAPI GEOGIS facilitando descoberta de atributos de qualidade por equipe de desenvolvimento estabelecendo conexões explícitas entre casos de uso requisitos funcionais user stories e requisitos não-funcionais.

---

**Última atualização:** 2026-01-10

---

<!-- GENERATED:START - Não edite abaixo desta linha -->
## Índice por Domínio (85 requisitos)

| # | Domínio | Arquivos |
|:--|:--------|:--------:|
| 01 | [Performance](./01-performance/README.md) | 8 |
| 02 | [Segurança](./02-security/README.md) | 17 |
| 03 | [Confiabilidade](./03-reliability/README.md) | 12 |
| 04 | [Usabilidade](./04-usability/README.md) | 13 |
| 05 | [Escalabilidade](./05-scalability/README.md) | 19 |
| 06 | [Compatibilidade](./06-compatibility/README.md) | 7 |
| 07 | [Manutenibilidade](./07-maintainability/README.md) | 6 |
| 08 | [Interoperabilidade](./08-interoperability/README.md) | 3 |

*Gerado automaticamente em 2026-01-13 19:11*
<!-- GENERATED:END -->
