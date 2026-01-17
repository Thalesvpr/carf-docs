# Fluxo de Cadastro E2E

Testes end-to-end do fluxo completo de cadastro de unidade e titulares.

## TC-E2E-001: Fluxo Completo de Cadastro

```gherkin
Feature: Cadastro completo de unidade habitacional
  Como cadastrista do CARF
  Quero cadastrar uma unidade com titulares
  Para que o processo de legitimação possa ser iniciado

Background:
  Dado que estou logado como "cadastrista"
  E tenho acesso ao tenant "municipio-teste"

Cenário: Cadastro completo de unidade com titular
  # Etapa 1: Criar unidade
  Quando acesso a página de cadastro de unidades
  E preencho o endereço:
    | Rua       | Rua das Flores |
    | Número    | 123            |
    | Bairro    | Centro         |
    | CEP       | 01310-100      |
  E desenho o polígono da unidade no mapa
  E clico em "Salvar Unidade"
  Então vejo a mensagem "Unidade criada com sucesso"
  E a unidade aparece com status "Rascunho"

  # Etapa 2: Adicionar fotos
  Quando clico em "Adicionar Fotos"
  E faço upload de 3 fotos da unidade
  Então vejo as 3 fotos na galeria da unidade

  # Etapa 3: Cadastrar titular
  Quando clico em "Adicionar Titular"
  E preencho os dados do titular:
    | Nome           | Maria da Silva Santos |
    | CPF            | 123.456.789-00        |
    | Data Nascimento| 15/03/1985            |
    | Telefone       | 11999998888           |
  E clico em "Salvar Titular"
  Então vejo "Maria da Silva Santos" na lista de titulares

  # Etapa 4: Vincular titular à unidade
  Quando seleciono "Proprietário" como tipo de vínculo
  E defino "100%" de participação
  E clico em "Confirmar Vínculo"
  Então vejo o titular vinculado à unidade

  # Etapa 5: Submeter para análise
  Quando clico em "Submeter para Análise"
  Então vejo confirmação "Unidade submetida para análise"
  E o status muda para "Pendente"
```

## TC-E2E-002: Validação de Dados no Fluxo

```gherkin
Cenário: Validações impedem cadastro incompleto
  Quando tento salvar unidade sem endereço
  Então vejo erro "Endereço é obrigatório"

  Quando tento salvar unidade sem polígono
  Então vejo erro "Geometria é obrigatória"

  Quando tento submeter unidade sem titular
  Então vejo erro "Adicione pelo menos um titular"
```

## TC-E2E-003: Fluxo com Múltiplos Titulares

```gherkin
Cenário: Cadastro de unidade com coproprietários
  Dado que criei uma unidade com geometria válida

  Quando adiciono titular "João Silva" com 50% de participação
  E adiciono titular "Maria Silva" com 50% de participação
  Então a soma de participações é 100%
  E posso submeter para análise

  Quando tento adicionar terceiro titular com 10%
  Então vejo erro "Soma de participações excede 100%"
```

## TC-E2E-004: Edição de Unidade em Rascunho

```gherkin
Cenário: Editar unidade antes de submeter
  Dado que existe uma unidade em "Rascunho"

  Quando altero o número do endereço para "456"
  E redesenho o polígono no mapa
  E clico em "Salvar Alterações"

  Então vejo "Alterações salvas com sucesso"
  E o histórico mostra as alterações
```

## Dados de Teste

```typescript
// fixtures/cadastro.ts
export const unitFixture = {
  address: {
    street: 'Rua das Flores',
    number: '123',
    neighborhood: 'Centro',
    city: 'São Paulo',
    state: 'SP',
    zip_code: '01310-100'
  },
  geometry: {
    type: 'Polygon',
    coordinates: [[
      [-46.6388, -23.5489],
      [-46.6385, -23.5489],
      [-46.6385, -23.5492],
      [-46.6388, -23.5492],
      [-46.6388, -23.5489]
    ]]
  }
};

export const holderFixture = {
  name: 'Maria da Silva Santos',
  cpf: '123.456.789-00',
  birth_date: '1985-03-15',
  contact: { phone: '11999998888' }
};
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
