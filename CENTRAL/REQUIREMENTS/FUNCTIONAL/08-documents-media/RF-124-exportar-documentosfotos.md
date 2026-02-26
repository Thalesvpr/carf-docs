---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-124: Exportar Documentos e Fotos

## Descricao

Sistema deve permitir exportacao de todos os documentos e fotos associados a uma entidade em arquivo ZIP consolidado para backup, compartilhamento ou arquivamento externo. Arquivo ZIP gerado contem estrutura de pastas organizada hierarquicamente separando documentos e fotos em diretorios distintos (raiz/documentos/, raiz/fotos/) com possivel subdivisao por tipo ou data. Sistema inclui arquivo CSV de metadados dentro do ZIP com informacoes sobre cada arquivo: nome original, tipo, tamanho, data de upload, usuario responsavel e descricao. Geracao do ZIP ocorre de forma assincrona para exportacoes grandes, com processo em background, feedback de progresso e notificacao quando arquivo pronto para download. ZIP disponibilizado via URL temporaria com expiracao configurada.

## Criterios de Aceitacao

1. Exportacao em arquivo ZIP consolidado
2. Estrutura hierarquica de pastas
3. CSV de metadados incluido no ZIP
4. Geracao assincrona para arquivos grandes
5. URL temporaria para download

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-105, RF-111, RF-116
