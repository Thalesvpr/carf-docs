---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-121: Anexar Descricao a Foto

## Descricao

Sistema deve permitir adicionar descricoes textuais a fotos para contexto e documentacao. Campo description opcional pode ser preenchido no upload ou editado posteriormente. Edicao inline direto na galeria ou detalhes sem formulario separado, salvando apos blur ou botao explicito. Descricao exibida consistentemente em galeria, popup no mapa e detalhes. Limite de 500-2000 caracteres para observacoes detalhadas mas nao excessivas. Descricoes indexadas para busca full-text por palavras-chave.

## Criterios de Aceitacao

1. Campo description opcional
2. Edicao inline na galeria
3. Exibicao em todas interfaces
4. Limite de caracteres adequado
5. Busca full-text por descricao

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-108, RF-111
