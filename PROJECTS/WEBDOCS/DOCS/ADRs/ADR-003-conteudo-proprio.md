# ADR-003: Conteúdo Próprio sem Sync de CENTRAL

Decisão mantendo conteúdo do WEBDOCS escrito diretamente no repositório ao invés de sincronizar de CENTRAL justificada por diferenças fundamentais de propósito onde CENTRAL contém documentação técnica granular para máquinas (especificações, requisitos, ADRs) enquanto WEBDOCS contém documentação orientada a humanos (guias, tutoriais, manuais) com estrutura de navegação e tom de voz distintos, complexidade proibitiva de manter sync bidirecional com transformação de formato exigindo mapeamentos frágeis propensos a quebrar em mudanças de estrutura, e independência operacional permitindo equipe de documentação trabalhar no WEBDOCS via CMS visual sem conhecimento da estrutura de CENTRAL.

Conteúdo do WEBDOCS pode referenciar conceitos definidos em CENTRAL quando necessário mas não existe dependência de build ou runtime. Equipe de documentação é responsável por manter consistência conceitual revisando CENTRAL periodicamente para atualizações relevantes.

Alternativas rejeitadas: sync automático unidirecional (perde customizações de navegação), sync com transformação (complexidade de manutenção), conteúdo duplicado manual (divergência inevitável).

Consequências: maior autonomia da equipe de documentação, risco de divergência conceitual mitigado por revisão periódica, necessidade de manter conteúdo em dois lugares para tópicos que existem em ambos.

---

**Data:** 2026-01-17
**Status:** Aprovado
**Decisor:** Equipe de Arquitetura + Documentação
**Última atualização:** 2026-01-17
**Status do arquivo**: Review
