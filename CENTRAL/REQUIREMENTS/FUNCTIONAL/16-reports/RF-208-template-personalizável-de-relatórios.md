---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-208: Template Personalizavel de Relatorios

## Descricao

Sistema deve oferecer a usuarios com perfil ADMIN capacidade de customizar templates de relatorios PDF atraves de editor visual para modificacao de estrutura HTML e estilos CSS, possibilitando adaptacao de layout conforme identidade visual institucional. Editor implementa sistema de variaveis dinamicas inseridas via sintaxe especial como {{unidade.codigo}}, {{titular.nome}}, substituidas automaticamente por valores reais durante geracao. Preview em tempo real renderiza template com dados de exemplo permitindo visualizacao antes de salvar. Templates podem incluir tabelas dinamicas iterando sobre colecoes, graficos JavaScript, codigos QR com URLs de acesso e imagens de mapas estaticos, proporcionando flexibilidade para documentacao tecnica sofisticada.

## Criterios de Aceitacao

1. Editor visual HTML/CSS para ADMIN
2. Variaveis dinamicas com sintaxe {{}}
3. Preview em tempo real
4. Tabelas dinamicas e graficos
5. Codigos QR e mapas estaticos

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-209, RF-210
