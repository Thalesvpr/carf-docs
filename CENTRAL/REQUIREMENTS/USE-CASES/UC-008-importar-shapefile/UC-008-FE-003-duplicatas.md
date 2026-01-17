---
modules: [GEOWEB, REURBCAD, GEOGIS]
epic: scalability
---

# UC-008-FE-003: Duplicatas Detectadas

Fluxo de exceção do UC-008 Importar Shapefile ocorrendo no passo 10.6 durante criação de unidade quando worker tenta executar INSERT INTO units mas antes valida unicidade de código verificando se já existe registro com mesmo valor no campo code considerado chave natural única do negócio identificando univocamente cada unidade habitacional dentro do tenant, executa query SELECT id FROM units WHERE tenant_id = $tenant AND code = $new_code LIMIT 1 antes do INSERT detectando existência prévia retornando id não null indicando duplicata, tipicamente causado por reimportação de Shapefile parcialmente sobreposto com dataset anterior onde algumas unidades já foram cadastradas manualmente ou em importação prévia e usuário tenta importar novamente arquivo completo sem filtrar registros já existentes, ou múltiplas equipes de campo cadastrando mesma área simultaneamente gerando códigos conflitantes se esquema de numeração não coordenado centralmente, sistema ao detectar duplicata não sobrescreve registro existente preservando dados originais que podem ter informações adicionais como fotos aprovações titulares vinculados não presentes no Shapefile de reimportação evitando perda de trabalho, pula criação do registro duplicado incrementando contador skipped_count, adiciona entrada em import_errors table com feature_index code error_code="DUPLICATE_CODE" error_message="Unidade com código 'UH-001' já existe no sistema" permitindo rastreabilidade de quais features foram ignoradas, worker continua processando próximos registros normalmente sem abortar job permitindo importar unidades novas válidas ao invés de falhar tudo por alguns duplicados, ao concluir importação relatório exibe estatísticas separando Importadas com Sucesso 245, Duplicatas Ignoradas 5 com cor amarela warning, log de erros CSV downloadável inclui coluna tipo_erro=DUPLICATA e coluna codigo_conflitante permitindo ANALYST identificar exatamente quais registros foram pulados, ANALYST pode então decidir manter apenas registros existentes descartando Shapefile duplicado, ou se Shapefile tem dados mais atualizados pode deletar manualmente unidades existentes conflitantes via interface web (buscar por código listar resultados selecionar deletar) e reimportar Shapefile novamente agora sem conflito criando versões atualizadas, ou ajustar esquema de códigos no Shapefile antes de importar renumerando features duplicadas com sufixos (UH-001 → UH-001-B) garantindo unicidade preservando ambos registros para reconciliação posterior manual decidindo qual manter, regra de negócio RN-005 formaliza comportamento sempre priorizando dados existentes evitando sobrescrita acidental que é operação destrutiva irreversível sem backup.

**Ponto de Desvio:** Passo 10.6 do UC-008 (validação antes de INSERT)

**Retorno:** Registro duplicado ignorado, importação continua, duplicata registrada no log

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
