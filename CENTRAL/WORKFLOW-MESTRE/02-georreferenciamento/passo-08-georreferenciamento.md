---
type: workflow
status: approved
updated: 2026-01-25
part: 2
step: 8
---

# Passo 8: Georreferenciamento

Analista desenha poligonos de comunidades, quadras e lotes sobre a ortofoto.

## Fluxo

1. Analista usa ferramentas do QGIS para desenhar/produzir:
   - Poligonos de comunidades (limites da area)
   - Poligonos de quadras (divisoes internas)
   - Poligonos de lotes (unidades individuais)
   - Atributos e metadados associados a cada poligono
2. Analista utiliza ortofoto como referencia visual
3. Analista pode usar snapping para precisao
4. Analista valida topologia (sem sobreposicoes, sem gaps)
5. Trabalho salvo localmente durante edicao

## Hierarquia de Poligonos

```
Comunidade
    └── Quadra
           └── Lote
```

## Tipos de Poligonos

| Tipo | Descricao | Exemplo |
|------|-----------|---------|
| Comunidade | Limite externo da area | Favela X, Assentamento Y |
| Quadra | Divisao interna | Quadra A, Quadra B |
| Lote | Unidade individual | Lote 001, Lote 002 |

## Ferramentas QGIS

- **Sketching**: Desenho de poligonos
- **Snapping**: Precisao nos vertices
- **Topology Checker**: Validacao de topologia
- **Attribute Table**: Edicao de atributos

## Validacao Topologica

Antes de publicar, a topologia deve estar consistente:
- Sem sobreposicoes entre poligonos do mesmo nivel
- Sem gaps (buracos) entre poligonos adjacentes
- Lotes contidos dentro de quadras
- Quadras contidas dentro de comunidades

## Resultado

- Poligonos de comunidades/quadras/lotes desenhados
- Atributos preenchidos
- Topologia validada
- Trabalho salvo localmente

## Proximo Passo

Passo 9: Publicacao no Backend
