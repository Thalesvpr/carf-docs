---
modules: [GEOWEB, REURBCAD]
epic: compatibility
---

# UC-003-FA-001: Importar Titulares de Planilha

Fluxo alternativo do UC-003 Vincular Titular a Unidade desviando no passo 3 (adicionar titular individual) quando usuário possui lista extensa de titulares a vincular proveniente de levantamento externo ou sistema legado exportado em planilha Excel ou CSV economizando tempo de digitação manual repetitiva, onde ao invés de clicar Adicionar Titular para processo individual usuário clica em botão dropdown Ações em Lote selecionando opção Importar Planilha abrindo modal de upload com instruções claras sobre formato esperado, link para download de template Excel pré-formatado contendo headers de colunas obrigatórias (cpf_cnpj nome data_nascimento telefone email relationship_type ownership_percentage is_primary) e opcionais (endereço cep observações), e área de drag-and-drop ou botão Selecionar Arquivo aceitando formatos .xlsx .xls .csv com limite de 1000 linhas por upload para evitar timeout de processamento. Usuário baixa template se necessário entendendo estrutura de colunas, preenche planilha localmente usando Excel Google Sheets ou LibreOffice com dados dos titulares respeitando formatos especificados (CPF sem formatação 11 dígitos, telefone com DDD sem parênteses, relationship_type usando códigos exatos PROPRIETARIO POSSUIDOR CONJUGE HERDEIRO LOCATARIO OCUPANTE, ownership_percentage decimal entre 0-100, is_primary boolean SIM/NAO ou TRUE/FALSE ou 1/0), salva arquivo e faz upload arrastando para área de drop ou selecionando via file picker. Sistema recebe arquivo valida extensão e tamanho máximo 5MB, parsing conteúdo usando biblioteca SheetJS ou similar convertendo para array de objetos JavaScript, valida estrutura verificando presença de colunas obrigatórias (cpf_cnpj nome relationship_type ownership_percentage) exibindo erro específico se alguma coluna crítica faltando listando quais estão ausentes, executa validações de dados linha por linha acumulando erros sem interromper processamento completo verificando CPF/CNPJ válido usando algoritmo de dígitos verificadores, nome com mínimo 3 palavras, telefone com 10-11 dígitos, email formato válido se preenchido, relationship_type pertence a enum permitido, ownership_percentage entre 0-100, is_primary boolean válido, e verificação de duplicação de CPF tanto dentro da planilha (detecta linhas duplicadas) quanto contra banco de dados (titular já existe no tenant). Sistema após parsing e validação exibe tela de preview apresentando tabela interativa com linhas da planilha mostrando ícone de status por linha (verde checkmark se válido, vermelho X se erro, laranja warning se duplicado mas pode prosseguir), colunas principais visíveis (nome CPF tipo relacionamento percentual principal), coluna Ação permitindo editar inline campos com erro ou remover linha clicando ícone lixeira, e resumo estatístico no topo mostrando "X de Y linhas válidas, Z erros, W duplicados" com opções filtrar apenas erros ou apenas válidos facilitando correção em massa. Usuário revisa preview corrigindo erros inline editando células diretamente que re-valida em tempo real atualizando ícone de status, remove linhas problemáticas que não consegue corrigir imediatamente decidindo processar depois, ou cancela upload completo para corrigir planilha original e re-submeter se preferir manter rastreabilidade de arquivo fonte. Após revisão e satisfeito com dados válidos usuário clica Confirmar Importação e sistema processa em batch transaction criando registros na tabela holders para CPFs novos (pulando duplicados ou atualizando se configurado modo upsert), criando vínculos na tabela unit_holders associando todos titulares importados à unidade atual com tipos percentuais e flags principais conforme planilha, validando regras de negócio globais como soma de percentuais ≤100% e apenas um principal existente exibindo erro se violar impedindo commit da transação inteira ou modo permissivo permitindo ajuste automático normalizando percentuais proporcionalmente se soma ultrapassar, adiciona entradas na timeline registrando "X titulares importados via planilha por Nome do Usuário em timestamp" com link para baixar cópia da planilha processada para auditoria, e exibe modal de resumo final mostrando "Importação concluída: X titulares criados, Y vínculos estabelecidos, Z erros (detalhes em log)" com opção baixar relatório de erros em CSV para correção offline.

**Ponto de Desvio:** Passo 3 do UC-003 (ao invés de adicionar individual, importa em lote)

**Template de Planilha:**
```
| cpf_cnpj      | nome              | data_nascimento | telefone      | email           | relationship_type | ownership_percentage | is_primary | observacoes |
|---------------|-------------------|-----------------|---------------|-----------------|-------------------|----------------------|------------|-------------|
| 12345678900   | João Silva Santos | 1980-05-15      | 11987654321   | joao@email.com  | PROPRIETARIO      | 50.00                | SIM        |             |
| 98765432100   | Maria Souza Lima  | 1985-10-20      | 11912345678   | maria@email.com | CONJUGE           | 50.00                | NAO        | Cônjuge     |
```

**Validações Executadas:**
```typescript
const validations = [
  { field: 'cpf_cnpj', rule: 'required, valid CPF/CNPJ digits', error: 'CPF/CNPJ inválido' },
  { field: 'nome', rule: 'required, min 3 words', error: 'Nome deve ter nome e sobrenome' },
  { field: 'relationship_type', rule: 'required, enum [PROPRIETARIO, POSSUIDOR, ...]', error: 'Tipo inválido' },
  { field: 'ownership_percentage', rule: 'required, 0-100', error: 'Percentual entre 0-100' },
  { field: 'is_primary', rule: 'boolean (SIM/NAO, TRUE/FALSE, 1/0)', error: 'Usar SIM ou NAO' },
  { field: 'telefone', rule: 'optional, 10-11 digits', error: 'Telefone inválido' },
  { field: 'email', rule: 'optional, valid email', error: 'Email inválido' }
];
```

**Preview com Correção:**
```
✅ João Silva Santos (CPF válido, 50%, Principal)
❌ Maria Souza (CPF inválido: 123456789) [Editar] [Remover]
⚠️  José Oliveira (CPF já cadastrado: vincular existente?) [Vincular] [Pular]

Resumo: 1 de 3 linhas válidas, 1 erro, 1 duplicado
[Filtrar: Apenas Erros] [Filtrar: Apenas Válidos] [Mostrar Todos]
```

**Processamento em Batch:**
```typescript
const results = { created: 0, linked: 0, errors: [] };

await db.transaction(async (trx) => {
  for (const row of validRows) {
    // Criar ou buscar holder
    let holderId = await findHolderByCpf(row.cpf_cnpj);
    if (!holderId) {
      holderId = await trx('holders').insert({
        cpf: row.cpf_cnpj,
        name: row.nome,
        phone: row.telefone,
        email: row.email,
        tenant_id: currentTenantId
      }).returning('id');
      results.created++;
    }

    // Criar vínculo
    await trx('unit_holders').insert({
      unit_id: currentUnitId,
      holder_id: holderId,
      relationship_type: row.relationship_type,
      ownership_percentage: row.ownership_percentage,
      is_primary: row.is_primary === 'SIM' || row.is_primary === 'TRUE'
    });
    results.linked++;
  }

  // Validar regras de negócio globais
  const sum = await trx('unit_holders')
    .where('unit_id', currentUnitId)
    .sum('ownership_percentage');

  if (sum > 100) throw new Error('Soma de percentuais ultrapassa 100%');
});

return results;
```

**Retorno:** Lista de titulares atualizada com todos importados, timeline registra operação batch

---

**Última atualização:** 2025-12-30
