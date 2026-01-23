---
id: RNF-090
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-090: Charset

## Descricao

UTF-8 obrigatorio em todos os componentes: banco de dados, APIs e exportacoes. Garante suporte a acentuacao portuguesa, caracteres especiais e interoperabilidade.

## Metricas

- Database: PostgreSQL com encoding UTF-8 e collation pt_BR
- APIs: Content-Type application/json; charset=utf-8
- Exportacoes: UTF-8 com BOM opcional para compatibilidade Excel

## Criterios de Aceitacao

1. Textos com acentuacao armazenados e exibidos corretamente
2. Importacoes detectam e convertem encodings legados automaticamente
3. APIs rejeitam payloads com bytes UTF-8 mal-formados
