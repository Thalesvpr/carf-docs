---
type: leaf
status: approved
updated: 2026-01-24
---

# Documento

Arquivo anexado a qualquer registro do sistema. Pode ser foto da unidade, copia do CPF do titular, planta topografica, ou certidao emitida.

Documentos sao essenciais para comprovar situacao de posse, identidade de titulares, e caracteristicas dos imoveis. O processo de legitimacao exige documentacao minima que varia conforme modalidade.

## Tipos Comuns

Fotos documentam estado fisico do imovel - fachada, interior, quintal. Documentos pessoais comprovam identidade - CPF, RG, certidao de casamento. Plantas tecnicas delimitam perimetro e area. Certidoes sao geradas ao final do processo.

## Armazenamento

Arquivos sao guardados em storage seguro separado do banco de dados. O registro do documento contem apenas metadados - nome, tamanho, tipo. O conteudo binario fica no storage com acesso controlado.

## Integridade

Hash criptografico e calculado no upload para garantir que arquivo nao foi alterado. Downloads usam URLs temporarias que expiram apos poucos minutos, impedindo compartilhamento indevido de links.

## Quota

Cada tenant tem limite de armazenamento. Sistema monitora uso e bloqueia novos uploads quando quota e atingida.
