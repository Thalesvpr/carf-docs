# Template de API

Template para páginas da seção /api/ que documentam conceitos e uso da API GEOAPI de forma não-técnica complementando Swagger.

Frontmatter obrigatório define title com nome do recurso ou conceito, description com resumo de 1-2 linhas, section com valor api, e audience com valor user. Esta seção é pública diferente de Swagger interativo que requer role dev.

Introdução explica o que recurso representa no contexto de negócio, não apenas tecnicamente. Exemplo: "Unidades representam imóveis cadastrados no processo de regularização fundiária" ao invés de "endpoint /units retorna lista de unidades".

Seção de conceitos explica modelo de dados de forma simplificada. Campos principais com descrição do significado, não do tipo técnico. Relacionamentos com outros recursos explicados em termos de negócio.

Seção de operações lista ações possíveis (criar, listar, atualizar, etc) com explicação de quando usar cada uma. Não incluir detalhes técnicos de request/response que estão no Swagger. Focar em casos de uso.

Seção de permissões indica quais roles podem executar cada operação. Tabela simples com operação e roles necessárias. Link para documentação de roles para entender hierarquia.

Seção de exemplos de uso descreve cenários comuns em linguagem de negócio. Exemplo: "Para cadastrar unidade coletada em campo, primeiro valide os dados do titular, depois..."

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
