---
modules: [GEOWEB, REURBCAD]
epic: units
---

# UC-004-FA-003: Copiar Unidade Anterior

Fluxo alternativo do UC-004 Coletar Dados Campo Mobile desviando no passo 6 (captura GPS e início de preenchimento) quando FIELD_AGENT está cadastrando múltiplas unidades adjacentes ou similares em mesma rua/comunidade com características repetidas economizando tempo de digitação, onde ao abrir formulário de nova unidade app exibe botão Copiar da Última no topo, FIELD_AGENT clica disparando busca em SQLite local da última unidade cadastrada ordenando por created_at DESC LIMIT 1, app pré-preenche formulário atual com dados copiados incluindo endereço (rua bairro cidade CEP mantendo logradouro mas limpando número), tipo de unidade, observações genéricas, mantendo campos específicos vazios como número do endereço geometria fotos titulares que são únicos por unidade. FIELD_AGENT ajusta apenas dados específicos da unidade atual editando número incrementando para próximo (ex: 51 → 53), redesenha geometria nova adjacente, tira fotos diferentes, cadastra titulares específicos, e salva economizando ~60% do tempo de preenchimento em levantamentos de áreas homogêneas.

**Ponto de Desvio:** Passo 6 do UC-004 (início do formulário, antes de preencher)

**Dados Copiados:**
- ✅ Endereço (logradouro, bairro, cidade, estado, CEP)
- ✅ Tipo de unidade
- ✅ Observações genéricas
- ❌ Número (limpo, requer novo)
- ❌ Geometria (vazio, cada unidade única)
- ❌ Fotos (vazio)
- ❌ Titulares (vazio)
- ❌ GPS location (captura novo)

**Query SQLite:**

App executa SELECT asterisco FROM units_local WHERE deleted_at IS NULL ORDER BY created_at DESC LIMIT um retornando última unidade cadastrada com todos campos incluindo endereço tipo observações para pré-preencher formulário novo permitindo FIELD_AGENT economizar tempo digitação em áreas homogêneas com características repetidas.

**Retorno:** Formulário pré-preenchido, FIELD_AGENT ajusta detalhes específicos

---

**Última atualização:** 2025-12-30
