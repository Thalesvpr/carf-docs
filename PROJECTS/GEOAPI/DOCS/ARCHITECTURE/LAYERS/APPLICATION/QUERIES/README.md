# QUERIES

Queries CQRS do GEOAPI representando operações apenas-leitura (reads) otimizadas para apresentação de dados, organizadas por feature e seguindo convenção GetXByIdQuery/ListXQuery/SearchXQuery. Queries são records imutáveis contendo filtros, paginação e parâmetros de busca retornando DTOs diretamente sem passar por entidades de domínio quando apropriado para performance. Handlers implementam IRequestHandler<TQuery, TResult> do MediatR podendo acessar DbContext diretamente via IQueryable para projeções eficientes com Select, Include e AsNoTracking evitando carregar agregados completos quando apenas subset de dados é necessário. Queries complexas podem usar views SQL, stored procedures ou índices especializados para performance em listagens, buscas e relatórios sem violar encapsulamento de domínio pois não alteram estado. Suportam paginação via PagedResult<T>, ordenação dinâmica, filtros compostos e projeções customizadas retornando exatamente dados que UI/API precisa minimizando over-fetching.

## Arquivos Principais (a criar)

**Units:**
- 01-get-unit-by-id-query.md
- 02-list-units-query.md
- 03-search-units-by-address-query.md
- 04-get-units-by-community-query.md

**Holders:**
- 05-get-holder-by-id-query.md
- 06-get-holder-by-cpf-query.md
- 07-list-holders-query.md
- 08-get-holders-by-unit-query.md

**Communities:**
- 09-get-community-by-id-query.md
- 10-list-communities-query.md
- 11-get-community-stats-query.md

**Teams:**
- 12-get-team-by-id-query.md
- 13-list-teams-query.md
- 14-get-team-members-query.md

**Legitimation:**
- 15-get-legitimation-request-by-id-query.md
- 16-list-legitimation-requests-query.md
- 17-get-pending-legitimation-requests-query.md

**Reports:**
- 18-get-units-summary-report-query.md
- 19-get-legitimation-progress-report-query.md

---

**Última atualização:** 2026-01-12
