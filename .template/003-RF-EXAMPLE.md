---
type: rf
status: review
updated: 2026-01-22
modules:
  - GEOAPI
  - GEOWEB
---

# RF-049: Criar Unidade Habitacional

## Descricao

O sistema deve permitir a criacao de unidades habitacionais vinculadas a uma comunidade, registrando informacoes cadastrais e geometria do lote. A unidade representa o nucleo do cadastro de regularizacao fundiaria, contendo dados do imovel que serao utilizados no processo de legitimacao. O cadastro inicial deve exigir apenas campos minimos obrigatorios, permitindo complementacao posterior durante visitas de campo. A geometria pode ser desenhada manualmente no mapa, importada de GPS ou copiada de unidade adjacente.

## Criterios de Aceitacao

1. Usuario com role ANALYST ou FIELD_AGENT pode criar unidade
2. Campos obrigatorios: comunidade, tipo de uso, numero ou identificador
3. Geometria pode ser adicionada posteriormente
4. Unidade criada inicia com status DRAFT
5. Sistema calcula area automaticamente quando geometria informada
6. Validacao impede sobreposicao maior que 5% com unidades existentes

## Rastreabilidade

- Modulos: GEOAPI, GEOWEB, REURBCAD
- User Stories: US-014, US-040
- Requisitos dependentes: RF-034 (comunidade deve existir)
