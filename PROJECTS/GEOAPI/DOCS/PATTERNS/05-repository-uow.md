---
type: leaf
status: approved
updated: 2026-02-07
---

# Repository and Unit of Work

Repositorios abstraem o acesso a dados atras de interfaces definidas no Domain, enquanto o Unit of Work agrupa multiplas operacoes em uma unica transacao atomica. Na GEOAPI, o EF Core fornece ambos os patterns nativamente: DbContext funciona como Unit of Work e cada DbSet como base para repositorios.

## Repository

Cada aggregate root tem seu proprio repositorio com interface definida no Domain e implementacao concreta no Infrastructure. IUnitRepository declara metodos especificos para o dominio de unidades: GetByIdAsync, GetByCommunityAsync, GetByStatusAsync, ExistsWithCodeAsync. IHolderRepository declara GetByIdAsync, GetByCpfAsync, SearchByNameAsync. Nao existe repositorio generico compartilhado pois cada aggregate tem necessidades de consulta distintas.

A implementacao concreta (UnitRepository) usa o DbSet do EF Core como base e encapsula queries complexas em metodos nomeados. GetByCommunityAsync aplica filtros de tenant_id e community_id, inclui relacionamentos necessarios via Include (UnitHolders, Documents) e retorna entidades de dominio completas. Queries que retornam entidades para modificacao usam tracking do EF Core. Queries somente para leitura desabilitam tracking via AsNoTracking, economizando memoria e CPU.

Repositorios nunca expõem IQueryable para fora da camada de Infrastructure. Toda query e construida internamente e retorna colecoes materializadas ou entidades. Isso evita que queries incompletas vazem para camadas superiores e sejam executadas em contextos inesperados.

Specification Pattern e usado para encapsular regras de filtro reutilizaveis. ActiveUnitsSpec filtra unidades com deleted_at nulo e status diferente de REJECTED. WithinBoundingBoxSpec filtra unidades cujo centroide esta dentro de um retangulo geografico. CreatedAfterSpec filtra por data de criacao. Specifications sao combinaveis via And e Or, permitindo construir filtros complexos sem duplicar logica de query.

## Unit of Work

O GeoApiDbContext do EF Core funciona como Unit of Work natural. O ChangeTracker monitora todas as alteracoes feitas em entidades rastreadas (insercoes, atualizacoes, exclusoes) durante o escopo de uma operacao. SaveChangesAsync persiste atomicamente todas as mudancas pendentes em uma unica transacao PostgreSQL.

Quando um command handler cria uma unidade, vincula um titular e registra um documento, essas tres operacoes acontecem como transacao atomica via SaveChanges. Se qualquer operacao falhar, todas sofrem rollback automaticamente. O TransactionBehavior do MediatR garante que o escopo da transacao abrange toda a execucao do handler, incluindo domain events despachados apos SaveChanges.

Domain events sao coletados pelas entidades durante a execucao do handler e despachados apos SaveChanges bem-sucedido. Isso garante que eventos so sao publicados se a persistencia funcionou. Se o despacho de um evento falhar, a transacao de persistencia ja foi commitada (os dados estao seguros) e o evento entra em retry.

Queries complexas que nao se encaixam nos metodos de repositorio sao implementadas diretamente como query handlers na camada Application usando o DbContext injetado. Essas queries usam projecoes Select para criar DTOs diretamente da query SQL, sem materializar entidades intermediarias, otimizando performance para listagens e dashboards.
