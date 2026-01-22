---
type: leaf
status: review
updated: 2026-01-21
---

# Seção API

Seção /api/ documenta API GEOAPI de forma conceitual complementando Swagger interativo disponível em /dev/swagger/. Foco em entendimento de negócio, não detalhes técnicos de request/response.

Estrutura de pastas em src/content/docs/api/ organiza por recurso principal: unidades, titulares, comunidades, processos, documentos, e autenticação. Uma página por recurso explicando conceito e operações disponíveis.

Conteúdo esperado por página inclui explicação do que recurso representa no contexto de REURB-S/REURB-E, relacionamentos com outros recursos em termos de negócio, operações disponíveis (criar, listar, atualizar, etc) com casos de uso, permissões necessárias por operação mapeando para roles, e exemplos de cenários de uso em linguagem de negócio.

Tom de escrita é técnico mas acessível. Diferente de /dev/ que assume conhecimento de programação, /api/ deve ser compreensível por analistas técnicos que não programam mas precisam entender capacidades da API.

Sem código de exemplo ou detalhes de payload nesta seção. Desenvolvedores que precisam de detalhes técnicos devem acessar Swagger em /dev/swagger/ que requer role dev. Esta separação protege informações técnicas sensíveis.

Frontmatter define section como api, audience como user. Páginas são públicas diferente de Swagger que requer autenticação.

Manutenção deve acompanhar mudanças na API atualizando descrições de recursos e operações. Validar alinhamento com especificação OpenAPI gerada automaticamente pela GEOAPI.
