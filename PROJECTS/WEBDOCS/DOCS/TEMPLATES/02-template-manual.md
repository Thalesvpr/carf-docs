---
type: leaf
status: review
updated: 2026-01-21
---

# Template de Manual

Template para páginas da seção /manuais/ que documentam uso das aplicações GEOWEB, REURBCAD e ADMIN.

Frontmatter obrigatório define title com nome da funcionalidade ou fluxo documentado, description com resumo de 1-2 linhas, section com valor manuais, subsection identificando aplicação (geoweb, reurbcad, admin), e audience com valor user. Campo sidebar define posição na navegação.

Introdução explica o que funcionalidade faz e quando usar. Incluir pré-requisitos se necessário (permissões, dados anteriores). Máximo de 3-4 linhas preparando leitor para instruções.

Corpo apresenta instruções passo-a-passo numeradas. Cada passo descreve uma ação com resultado esperado. Screenshots ilustram passos importantes mostrando exatamente onde clicar ou o que preencher. Callouts tipo warning alertam para ações irreversíveis.

Seção de troubleshooting opcional lista problemas comuns com soluções. Formato de pergunta-resposta facilita escaneamento. Linkar para suporte se problema persistir.

Seção "Ver também" lista funcionalidades relacionadas com links. Ajuda usuário a descobrir recursos complementares.

Exemplo de frontmatter para manual de cadastro de unidade: title como Cadastrar Nova Unidade, description como Passo a passo para registrar unidade habitacional no GEOWEB, section como manuais, subsection como geoweb, audience como user.

## Template Copy-Paste

```mdx
---
title: "Nome da Funcionalidade"
source: "PROJECTS/APLICACAO/DOCS/FEATURES/nome-feature.md"
sidebar:
  order: 1
  label: "Label Curto"
draft: false
---

import { Aside, Steps, Card, CardGrid, Tabs, TabItem } from '@astrojs/starlight/components';

# Nome da Funcionalidade

Breve descrição do que esta funcionalidade faz e quando o usuário deve usá-la.

## Pré-requisitos

Antes de começar, certifique-se de que:

- Você tem permissão de **Agente de Campo** ou superior
- A comunidade já está cadastrada no sistema
- (Outros pré-requisitos específicos)

<Aside type="note">
  Se você não tem as permissões necessárias, solicite ao administrador.
</Aside>

## Passo a Passo

<Steps>
1. **Acesse a tela**

   Navegue para Menu > Seção > Funcionalidade

   ![Captura de tela mostrando o menu](/images/manuais/app/feature-menu.png)

2. **Preencha os campos**

   - Campo 1: descrição do que preencher
   - Campo 2: descrição do que preencher
   - Campo 3: descrição do que preencher

   ![Formulário de cadastro](/images/manuais/app/feature-form.png)

3. **Confirme a ação**

   Clique no botão "Salvar" para confirmar.

   <Aside type="tip">
     Você pode usar o atalho Ctrl+S para salvar rapidamente.
   </Aside>

4. **Verifique o resultado**

   Uma mensagem de sucesso será exibida e o registro aparecerá na lista.
</Steps>

<Aside type="caution">
  Esta ação não pode ser desfeita. Verifique os dados antes de confirmar.
</Aside>

## Opções Avançadas

<Tabs>
  <TabItem label="Opção A">
    Descrição e instruções para a opção A.
  </TabItem>
  <TabItem label="Opção B">
    Descrição e instruções para a opção B.
  </TabItem>
</Tabs>

## Solução de Problemas

### O botão Salvar está desabilitado

**Causa**: Campos obrigatórios não preenchidos.

**Solução**: Verifique se todos os campos marcados com * estão preenchidos.

### Erro "Registro duplicado"

**Causa**: Já existe um registro com os mesmos dados.

**Solução**: Verifique na lista se o registro já existe. Se precisar atualizar, use a opção Editar.

### A tela não carrega

**Causa**: Problema de conexão ou servidor.

**Solução**:
1. Verifique sua conexão com a internet
2. Tente recarregar a página (F5)
3. Se persistir, verifique a [página de status](/status/)

## Ver Também

<CardGrid>
  <Card title="Funcionalidade Relacionada" icon="right-arrow">
    Próximo passo comum após esta ação.
    [Ver manual](/manuais/app/proxima/)
  </Card>
  <Card title="Guia Conceitual" icon="open-book">
    Entenda melhor o contexto desta funcionalidade.
    [Ver guia](/guia/conceito/)
  </Card>
</CardGrid>
```

## Exemplo Real: Cadastrar Unidade no GeoWeb

```mdx
---
title: "Cadastrar Unidade Habitacional"
description: "Passo a passo completo para cadastrar uma nova unidade habitacional no GeoWeb, com desenho de geometria e preenchimento de dados."
source: "PROJECTS/GEOWEB/DOCS/FEATURES/02-unit-crud.md"
sidebar:
  order: 3
  label: "Cadastrar Unidade"
draft: false
---

import { Aside, Steps, Tabs, TabItem } from '@astrojs/starlight/components';

# Cadastrar Unidade Habitacional

O cadastro de unidades é o processo principal de registro de moradias para regularização fundiária.
Esta funcionalidade permite desenhar a geometria da unidade no mapa e preencher os dados cadastrais.

## Pré-requisitos

- Permissão de **Agente de Campo** ou superior
- Comunidade já cadastrada e selecionada
- Imagem de satélite ou ortofoto disponível na região

<Aside type="note">
  Para cadastro em campo, recomendamos usar o app **REURBCAD** que funciona offline.
</Aside>

## Passo a Passo

<Steps>
1. **Selecione a comunidade**

   No painel lateral, clique na comunidade onde a unidade será cadastrada.
   O mapa será centralizado na área da comunidade.

2. **Inicie o cadastro**

   Clique no botão **+ Nova Unidade** na barra de ferramentas superior.
   O cursor mudará para modo de desenho.

3. **Desenhe a geometria**

   - Clique nos vértices do lote para desenhar o polígono
   - Use **duplo clique** para finalizar o desenho
   - Use **Esc** para cancelar

   <Aside type="tip">
     Ative a camada de imagem de satélite para visualizar melhor os limites.
   </Aside>

4. **Preencha os dados**

   O formulário abrirá automaticamente. Preencha:

   | Campo | Obrigatório | Descrição |
   |-------|-------------|-----------|
   | Identificador | Sim | Código único da unidade |
   | Tipo de Uso | Sim | Residencial, Comercial, Misto |
   | Área (m²) | Automático | Calculado da geometria |
   | Endereço | Não | Logradouro e número |

5. **Salve a unidade**

   Clique em **Salvar** para registrar a unidade.
   Status inicial será "Em Rascunho".

6. **Envie para aprovação**

   Quando todos os dados estiverem completos, clique em **Enviar para Aprovação**.
</Steps>

<Aside type="caution">
  A geometria não pode sobrepor mais de 5% com unidades existentes.
  Verifique possíveis conflitos antes de salvar.
</Aside>

## Editar Geometria

<Tabs>
  <TabItem label="Mover Vértices">
    1. Selecione a unidade no mapa
    2. Clique em **Editar Geometria**
    3. Arraste os vértices para nova posição
    4. Clique em **Confirmar**
  </TabItem>
  <TabItem label="Adicionar Vértices">
    1. Selecione a unidade no mapa
    2. Clique em **Editar Geometria**
    3. Clique no ponto médio de uma aresta
    4. Arraste o novo vértice
  </TabItem>
</Tabs>

## Solução de Problemas

### "Geometria inválida"

**Causa**: Polígono com auto-interseção ou área zero.

**Solução**: Redesenhe o polígono certificando-se de que as linhas não se cruzam.

### "Sobreposição detectada"

**Causa**: A unidade sobrepõe outra já cadastrada.

**Solução**: Ajuste a geometria para eliminar a sobreposição ou verifique se é a mesma unidade.

## Ver Também

- [Vincular Titular à Unidade](/manuais/geoweb/titulares/)
- [Fluxo de Aprovação](/guia/aprovacao/)
- [Editar Unidade](/manuais/geoweb/editar-unidade/)
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
