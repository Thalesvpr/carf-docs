---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: security
---

# UC-003: Vincular Titular a Unidade

Caso de uso permitindo usuários autorizados (ANALYST ADMIN FIELD_AGENT) associarem titular pessoa física ou jurídica a unidade habitacional existente após autenticação e verificação de permissão units.update ou holders.create, onde fluxo principal inicia com acesso à tela de detalhes da unidade exibindo seção Titulares mostrando lista de titulares já vinculados com cards exibindo nome CPF/CNPJ tipo de relacionamento percentual de propriedade e badge destacando titular principal se houver, usuário clica em botão Adicionar Titular abrindo modal com duas opções excludentes apresentadas como tabs ou botões radio (Buscar Titular Existente ou Criar Novo Titular). Opção A buscar existente permite usuário digitar CPF parcial nome ou parte do nome em campo de busca com autocomplete ativando após 3 caracteres digitados disparando GET /api/holders?search=$query que retorna lista de titulares matching filtrados por tenant atual exibindo até 10 resultados com nome CPF formatado endereço resumido e número de unidades já vinculadas, usuário seleciona titular da lista clicando na linha que fecha dropdown de autocomplete e pré-preenche informações do titular selecionado permitindo prosseguir para campos de relacionamento. Opção B criar novo exibe formulário inline dentro do mesmo modal contendo campos obrigatórios nome completo (mínimo 3 palavras validando nome sobrenome), CPF ou CNPJ (radio button selecionando tipo com validação específica de dígitos verificadores), data de nascimento (para pessoa física), telefone com máscara (DDD) XXXXX-XXXX, email opcional validado via regex RFC5322, endereço completo estruturado (logradouro número complemento bairro cidade estado CEP com integração opcional de busca via ViaCEP ao preencher CEP), usuário preenche dados e sistema valida CPF/CNPJ em tempo real exibindo ícone verde de validado ou vermelho de inválido ao lado do campo, executa verificação de duplicação consultando SELECT COUNT WHERE cpf = $1 AND tenant_id = $2 alertando se CPF já cadastrado oferecendo vincular existente ao invés de duplicar, cria novo registro na tabela holders após validações bem-sucedidas retornando holder_id que será usado no vínculo. Independente de opção A ou B sistema exibe campos de relacionamento incluindo dropdown tipo de relacionamento com opções pré-definidas (Proprietário Possuidor Cônjuge Herdeiro Locatário Ocupante Outro) permitindo customização por tenant, input numérico percentual de propriedade validando range 0-100 com incremento de 0.01 para permitir frações precisas, checkbox titular principal indicando se este é o beneficiário principal para fins de documentação oficial e relatórios, e textarea opcional observações sobre o vínculo para casos especiais. Usuário preenche tipo de relacionamento selecionando da lista, informa percentual de propriedade considerando que soma com outros titulares não pode ultrapassar 100%, marca checkbox titular principal se aplicável compreendendo que apenas um pode ser principal por unidade, clica em botão Vincular disparando validações de negócio verificando titular não está duplicado na mesma unidade consultando unit_holders WHERE unit_id = $1 AND holder_id = $2 retornando erro se já existe, soma de percentuais de todos titulares da unidade incluindo novo não ultrapassa 100% calculando SUM(ownership_percentage) WHERE unit_id = $1 mais percentual novo sendo menor ou igual a 100 exibindo warning com soma atual se ultrapassar permitindo ajuste, e apenas um titular principal existe verificando se checkbox está marcado e já existe outro principal oferecendo desmarcar atual automaticamente ou cancelar operação. Sistema após validações bem-sucedidas cria registro na tabela unit_holders associando unit_id holder_id relationship_type ownership_percentage is_primary timestamps criado_em e criador, adiciona entrada na timeline da unidade registrando evento HOLDER_LINKED com nome do titular tipo de relacionamento e percentual para auditoria visível, dispara domain event HolderLinkedEvent para processamento assíncrono de side effects como recalcular estatísticas de completude de dados da unidade ou notificar gestor se unidade atingiu todos titulares necessários para aprovação, e atualiza lista de titulares na tela adicionando card do novo titular com animação de fade-in exibindo toast de sucesso "Titular Nome vinculado com sucesso como Proprietário (50%)".

**Fluxos Alternativos:**
- UC-003-FA-001: Importar titulares de planilha

**Fluxos de Exceção:**
- UC-003-FE-001: CPF/CNPJ inválido
- UC-003-FE-002: Titular já vinculado
- UC-003-FE-003: Soma de percentuais > 100%
- UC-003-FE-004: Múltiplos titulares principais

**Regras de Negócio:**
- RN-001: Unidade pode ter múltiplos titulares (N:N via unit_holders)
- RN-002: Soma de ownership_percentage de todos titulares da unidade deve ser ≤100%
- RN-003: Apenas um titular pode ter is_primary=true por unidade
- RN-004: Tipo de relacionamento (relationship_type) é obrigatório
- RN-005: CPF/CNPJ deve ser válido (dígitos verificadores) e único dentro do tenant

**Rastreabilidade:**
- RF-061, RF-062, RF-084, RF-089, RF-090, RF-091, RF-092, RF-093
- US-029, US-044

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
