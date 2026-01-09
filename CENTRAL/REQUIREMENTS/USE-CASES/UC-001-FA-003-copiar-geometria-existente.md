---
modules: [GEOWEB, REURBCAD]
epic: usability
---

# UC-001-FA-003: Copiar Geometria de Unidade Existente

Fluxo alternativo do UC-001 Cadastrar Unidade Habitacional desviando no passo 5 (desenho de geometria) quando usuário deseja criar unidade adjacente ou similar a unidade já cadastrada aproveitando geometria existente como base, onde ao invés de desenhar polígono do zero usuário clica em botão Copiar de Unidade Existente abrindo modal exibindo lista de unidades próximas dentro de raio de 500m da localização aproximada selecionada ou de comunidade escolhida no passo 3, lista mostra até 20 unidades ordenadas por proximidade exibindo para cada uma código identificador, endereço resumido, área em m², thumbnail miniatura da geometria renderizada, e distância aproximada em metros do ponto de referência, usuário pode filtrar lista por código endereço ou status e seleciona unidade desejada clicando na linha que destaca geometria selecionada no mapa de fundo em cor diferenciada (amarelo semitransparente) permitindo preview visual, usuário confirma seleção clicando Copiar Geometria e sistema duplica coordenadas do polígono aplicando transformação geométrica de offset automático de 5 metros na direção nordeste (ou direção configurável via dropdown N S L O NE NO SE SO) para evitar sobreposição exata com unidade original gerando conflito espacial, geometria copiada com offset é renderizada no mapa em cor padrão (azul) enquanto original permanece visível em amarelo translúcido permitindo comparação visual, usuário pode ajustar manualmente vértices arrastando para corrigir posição exata ou rotacionar polígono mantendo proporções, e ao aceitar cópia sistema preenche campo geometry do formulário com coordenadas transformadas fechando modal e retornando para fluxo principal. Validações aplicadas incluem unidade origem deve ter geometria válida não-nula, geometria copiada após offset ainda deve estar dentro de bounds da comunidade ou município, offset aplicado não deve resultar em auto-interseção se geometria for côncava complexa (detecta e ajusta automaticamente reduzindo offset se necessário), e área da geometria copiada deve permanecer ≥10m² após transformações.

**Ponto de Desvio:** Passo 5 do UC-001 (desenho de geometria)

**Critérios de Listagem:**
- Unidades dentro de raio 500m da localização de referência
- Unidades da mesma comunidade selecionada no passo 3
- Máximo 20 unidades ordenadas por proximidade
- Filtro por código, endereço, status

**Transformação de Offset:**
- Offset padrão: 5m direção nordeste
- Direções configuráveis: N S L O NE NO SE SO
- Detecção de auto-interseção após offset
- Ajuste automático de offset se necessário
- Validação de bounds (geometria dentro da comunidade)

**Retorno:** Volta ao passo 6 do UC-001 (cálculo de área) com geometria copiada e ajustada

---

**Última atualização:** 2025-12-30
