---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-138: Simbologia por Atributo

## Descricao

Sistema deve suportar aplicacao de estilos visuais diferentes a features da mesma camada baseado em valores de atributos, permitindo visualizacao tematica e categorizacao visual de dados geoespaciais. Regras de estilo condicionais determinam aparencia de cada feature conforme suas propriedades via sintaxe tipo "if attribute equals X then color equals Y". Categorizacao suportada tanto para valores discretos (tipos ou categorias mapeiam para cores distintas via correspondencia exata) quanto continuos (valores numericos divididos em ranges com estilos graduados criando representacao de intensidade). Sistema gera legendas automaticas baseadas nas regras de estilo mostrando mapeamento visual entre categorias ou ranges e suas cores ou simbolos correspondentes, exibida no painel do mapa. Configuracao de simbologia armazenada como parte da definicao da camada e aplicada dinamicamente durante renderizacao.

## Criterios de Aceitacao

1. Regras de estilo condicionais
2. Categorizacao para valores discretos
3. Graduacao para valores continuos
4. Geracao automatica de legendas
5. Aplicacao dinamica durante renderizacao

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-136, RF-137
