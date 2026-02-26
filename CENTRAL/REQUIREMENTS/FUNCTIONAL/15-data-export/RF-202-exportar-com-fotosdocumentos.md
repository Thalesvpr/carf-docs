---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-202: Exportar com Fotos e Documentos

## Descricao

Sistema deve disponibilizar exportacao avancada que inclui dados tabulares ou geoespaciais das unidades e todos os arquivos de fotos e documentos vinculados, produzindo pacote completo em formato ZIP com estrutura de pastas organizada hierarquicamente. Estrutura de diretorios cria pasta para cada unidade identificada por codigo cadastral, com subpastas separadas para fotos e documentos, arquivos nomeados com timestamps e tipos. Arquivo CSV de metadados incluido no ZIP descreve mapeamento entre unidades e arquivos com caminhos relativos, tipos, datas de upload e autores. Para volumes grandes, geracao assincrona em background processa exportacao sem bloquear interface, enviando notificacao quando arquivo estiver pronto. Dados filtrados por tenant_id.

## Criterios de Aceitacao

1. ZIP com estrutura hierarquica de pastas
2. Fotos e documentos organizados por unidade
3. CSV de metadados com mapeamento
4. Geracao assincrona para volumes grandes
5. Segregacao por tenant_id

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-102, RF-044
