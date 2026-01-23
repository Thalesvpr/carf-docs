---
type: leaf
status: review
updated: 2026-01-22
---

# Log de Auditoria

Registro imutavel de todas as operacoes realizadas no sistema. Documenta quem modificou o que, quando, e de onde, garantindo rastreabilidade completa.

Todo cadastro, edicao ou exclusao gera um registro de auditoria. Isso permite reconstruir historico de qualquer dado, investigar incidentes, e atender requisitos legais de compliance.

## Conteudo

Cada registro inclui usuario responsavel, tipo de operacao, entidade afetada, valores antes e depois da modificacao, endereco IP de origem, e timestamp preciso.

## Imutabilidade

Registros de auditoria nunca sao editados ou excluidos. Essa imutabilidade garante integridade da trilha - ninguem pode apagar rastros de suas acoes.

## Consulta

Timeline cronologica mostra todas as modificacoes de um registro. Diff visual destaca o que mudou entre versoes. Filtros permitem buscar acoes de usuario especifico ou periodo.

## Compliance

LGPD exige rastreabilidade de acesso a dados pessoais. Logs de auditoria atendem esse requisito documentando quem acessou dados de cada titular e quando.
