---
modules: [GEOWEB, REURBCAD]
epic: units
---

# UC-001-FE-002: Geometria Sobreposta

Fluxo de exceção do UC-001 Cadastrar Unidade Habitacional ocorrendo no passo 9 (validação de dados) quando sistema detecta sobreposição espacial da geometria desenhada com uma ou mais unidades já cadastradas na mesma comunidade, onde detecção de sobreposição utiliza função espacial PostGIS ST_Overlaps ou ST_Intersects executando query `SELECT id, code FROM units WHERE community_id = X AND ST_Intersects(geometry, ST_GeomFromGeoJSON($1)) AND deleted_at IS NULL` retornando lista de unidades conflitantes com seus identificadores códigos e percentual de área sobreposta calculado via `ST_Area(ST_Intersection(geometry, $new_geometry)) / ST_Area($new_geometry) * 100`. Sistema classifica severidade da sobreposição como WARNING se percentual <10% (possível imprecisão de GPS ou ajuste de divisa aceitável) ou ERROR se ≥10% (provável duplicação ou erro grosseiro de desenho), e exibe modal de alerta com título "Geometria Sobreposta Detectada" apresentando tabela com colunas Código da Unidade, Endereço, Área Sobreposta (m²), Percentual (%), e Ação com link Ver no Mapa que destaca ambas geometrias (nova em azul semitransparente existente em vermelho semitransparente área de interseção em roxo sólido) permitindo análise visual. Usuário analisa sobreposição verificando se é erro legítimo (desenhou polígono errado) ou imprecisão aceitável (divisa compartilhada entre unidades geminadas), e decide entre três ações: Ajustar Geometria fechando modal e retornando ao passo 5 do fluxo principal (desenho de geometria) com polígono atual pré-carregado para edição manual dos vértices conflitantes guiado por highlight visual da área de interseção, Ignorar e Salvar Mesmo Assim prosseguindo com salvamento apesar de sobreposição (disponível apenas se WARNING <10% e usuário tem permissão units.override_warnings) registrando flag overlap_acknowledged=true no banco e adicionando observação automática "Sobreposição de X% com unidade Y foi reconhecida e aceita pelo usuário Z em data/hora" para auditoria futura, ou Cancelar Operação descartando unidade inteira retornando para tela de listagem. Após ajuste manual e nova tentativa de salvamento sistema re-executa validação espacial verificando se sobreposição foi corrigida, e se persistir com percentual ainda alto (≥10%) exibe novamente modal de alerta impedindo salvamento até correção efetiva ou usuário com permissão especial forçar override.

**Ponto de Desvio:** Passo 9 do UC-001 (validação de dados antes de salvar)

**Detecção de Sobreposição:**

Query PostGIS executando SELECT nos campos id code address da tabela units calculando overlap_area_m2 usando ST_Area de ST_Intersection entre geometry existente e nova geometria convertida de GeoJSON via ST_GeomFromGeoJSON, calculando overlap_percent como área de interseção dividida por área total da nova geometria multiplicado por cem, filtrando WHERE community_id igual ao tenant atual AND ST_Intersects detectando qualquer sobreposição espacial AND deleted_at IS NULL excluindo unidades soft-deleted, ordenando ORDER BY overlap_percent DESC priorizando conflitos com maior percentual de sobreposição retornando lista de unidades conflitantes com métricas precisas para análise usuário.

**Classificação de Severidade:**
- WARNING: overlap_percent < 10% (permite override com permissão)
- ERROR: overlap_percent ≥ 10% (bloqueia salvamento até ajuste)

**Ações Disponíveis:**
1. **Ajustar Geometria:** Retorna ao passo 5 do UC-001 com polígono pré-carregado
2. **Ignorar e Salvar:** Salva com flag overlap_acknowledged=true (só WARNING <10%)
3. **Cancelar:** Descarta operação completa retornando para listagem

**Retorno:**
- Se Ajustar: Volta ao passo 5 do UC-001 (desenho de geometria)
- Se Ignorar: Prossegue para passo 10 do UC-001 (salvamento com flag)
- Se Cancelar: Operação abortada

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
