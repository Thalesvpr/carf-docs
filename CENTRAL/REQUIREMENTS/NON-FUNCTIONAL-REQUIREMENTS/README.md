# NON-FUNCTIONAL-REQUIREMENTS

Requisitos não-funcionais do CARF especificando atributos de qualidade e restrições técnicas do sistema incluindo performance (tempo resposta, throughput, latência), escalabilidade (concurrent users, data volume), disponibilidade (uptime, SLA), segurança (autenticação, autorização, criptografia, LGPD), usabilidade (acessibilidade WCAG, responsividade), compatibilidade (browsers, devices, OS), e manutenibilidade (code coverage, technical debt). Cada RNF segue nomenclatura RNF-NNN-titulo-descritivo.md, possui metadados YAML (categoria, prioridade, impacto), descrição detalhada da restrição ou atributo de qualidade, métricas quantificáveis para verificação (ex: tempo resposta < 200ms p95, uptime > 99.5%), e rastreabilidade para UCs e RFs afetados. Organizados por categoria: performance (RNF-001 a RNF-030), security (RNF-031 a RNF-045), scalability (RNF-046 a RNF-060), compatibility (RNF-061 a RNF-075), e usability (RNF-076 a RNF-085).

## Navegação

**[index-by-epic.md](./index-by-epic.md)** - Índice de todos os 85 Requisitos Não-Funcionais organizados por épica (performance, security, scalability, compatibility, usability)

Ver também:
- **[../README.md](../README.md)** - Overview completo de Requirements com índices adicionais
- **[../index-by-module.md](../index-by-module.md)** - Requirements organizados por módulo implementador
- **[../traceability-matrix.md](../traceability-matrix.md)** - Matriz de rastreabilidade UC→RF→US→RNF

---

**Última atualização:** 2026-01-10
