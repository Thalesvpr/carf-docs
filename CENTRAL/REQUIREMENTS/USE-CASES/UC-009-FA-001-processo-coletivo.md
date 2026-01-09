---
modules: [GEOWEB, REURBCAD]
epic: maintainability
---

# UC-009-FA-001: Processo Coletivo (Múltiplas Unidades)

Fluxo alternativo do UC-009 Gerenciar Processo de Legitimação desviando no passo 4 onde ao invés de criar processo individual para 1 unidade, usuário seleciona radio button Modalidade Coletiva expandindo formulário revelando seção adicional Adicionar Unidades ao Processo com campo de busca permitindo localizar unidades por código endereço ou comunidade, usuário digita termo de busca sistema executa query SELECT * FROM units WHERE tenant_id = $tenant AND status = 'APPROVED' AND (code LIKE '%term%' OR address LIKE '%term%') filtrando apenas unidades aprovadas elegíveis, exibe resultados em lista com checkboxes mostrando código endereço e titular principal permitindo seleção múltipla, usuário marca 15-20 unidades adjacentes de mesma comunidade clica Adicionar criando vínculos em tabela process_units armazenando relacionamento N:N entre process e units, checklist de documentos exibido multiplica-se mostrando seção por unidade mas documentos gerais (Memorial Descritivo da Área Planta de Situação Geral) compartilhados entre todas reduzindo burocracia, termo gerado lista todas unidades em anexo com tabela contendo código endereço área beneficiário de cada uma consolidado em único documento oficial economizando custos de cartório e acelerando regularização em assentamentos homogêneos onde legitimação coletiva é mais eficiente que individual segundo diretrizes MCIDADES para REURB urbana.

**Ponto de Desvio:** Passo 4 do UC-009 (seleção de modalidade)

**Retorno:** Múltiplas unidades vinculadas ao mesmo processo, documentação compartilhada

---

**Última atualização:** 2025-12-30
