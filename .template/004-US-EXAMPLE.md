---
type: us
status: review
updated: 2026-01-22
epic: units
---

# US-014: Criar Unidade Habitacional

## Historia

Como analista de regularizacao fundiaria, quero cadastrar unidades habitacionais no sistema para que o levantamento de campo seja registrado digitalmente e possa seguir para validacao e aprovacao.

O cadastro de unidades e a atividade central do trabalho de campo. Preciso conseguir registrar rapidamente os dados basicos do imovel visitado, mesmo sem conexao com internet, e complementar informacoes posteriormente quando tiver acesso a documentos ou precisar corrigir dados.

## Criterios de Aceitacao

1. Formulario exibe campos obrigatorios destacados visualmente
2. Posso salvar unidade apenas com campos minimos preenchidos
3. Sistema sugere numero sequencial baseado na quadra
4. Mapa permite desenhar geometria do lote com ferramentas de edicao
5. Posso anexar fotos da fachada e documentos digitalizados
6. Unidade salva fica disponivel para sincronizacao quando online

## Rastreabilidade

- Epic: units
- Requisitos funcionais: RF-049, RF-054, RF-066
- Endpoints: POST /api/units, GET /api/units/{id}
