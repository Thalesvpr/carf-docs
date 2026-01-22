---
type: leaf
status: review
updated: 2026-01-21
---

# Seção Changelog

Seção /changelog/ documenta release notes das versões do ecossistema CARF permitindo usuários acompanharem novidades, correções e mudanças.

Estrutura de pastas em src/content/docs/changelog/ contém um arquivo por release nomeado com versão (v1.0.0.md, v1.1.0.md, etc). Ordem de navegação por data decrescente mostrando versões mais recentes primeiro.

Frontmatter define campos específicos: version como string semver, releaseDate como data ISO, applications como array de aplicações afetadas (GEOWEB, REURBCAD, GEOAPI, etc), e highlights como array de strings com principais mudanças para preview.

Estrutura de conteúdo por release inclui seção de highlights com principais novidades em destaque, seção de novas funcionalidades detalhando features adicionadas, seção de melhorias listando aperfeiçoamentos de funcionalidades existentes, seção de correções documentando bugs resolvidos, e seção de breaking changes alertando sobre mudanças que requerem ação dos usuários.

Tom de escrita é informativo focado no impacto para usuários. Evitar detalhes técnicos de implementação. Para cada item, explicar o que mudou e como afeta o uso. Links para documentação detalhada quando aplicável.

Página index da seção lista todas releases com versão, data, e highlights. Filtro opcional por aplicação permite ver apenas releases relevantes.

Integração com banner de notificações pode destacar novas releases por período configurável alertando usuários sobre atualizações importantes.
