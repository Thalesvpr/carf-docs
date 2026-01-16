# Tipos de Documento

Cada tipo de documento no repositório CARF possui estrutura específica com seções obrigatórias que garantem completude e consistência da informação.

## Caso de Uso (UC)

Casos de uso documentam fluxos completos de interação entre usuário e sistema. Devem conter seção Regras de Negócio listando as regras aplicáveis ao fluxo. Devem conter seção Rastreabilidade com links para requisitos funcionais e user stories relacionados. O frontmatter deve incluir campo modules listando os módulos implementadores como GEOWEB, GEOAPI ou REURBCAD.

## Requisito Funcional (RF)

Requisitos funcionais especificam capacidades atômicas do sistema. Devem conter seção Critérios de Aceitação em formato verificável, seja como lista de condições testáveis ou como cenários Given-When-Then. O frontmatter deve incluir campo modules listando os módulos onde o requisito é implementado.

## User Story (US)

User stories capturam requisitos na perspectiva do usuário. O corpo do documento deve conter as três frases obrigatórias do formato BDD: Como seguido do papel do usuário, quero seguido da funcionalidade desejada, e para que seguido do benefício esperado. O frontmatter deve incluir campo epic indicando a épica relacionada.

## Requisito Não Funcional (RNF)

Requisitos não funcionais especificam critérios de qualidade como performance, segurança e usabilidade. Devem conter métricas mensuráveis e condições de teste quando aplicável.

## Architecture Decision Record (ADR)

ADRs documentam decisões arquiteturais significativas. Devem conter campos de metadados específicos: Data da decisão, Status indicando se está Proposto, Aprovado ou Implementado, e Decisor identificando responsável pela decisão.

## Feature

Documentos de feature em PROJECTS descrevem funcionalidades implementadas. Devem conter pelo menos uma das seções: Validações ou Validation descrevendo regras de validação, API Integration ou Integração API descrevendo endpoints utilizados, ou Relacionamentos ou Domain Model descrevendo entidades envolvidas.

## How-To

Guias práticos que ensinam como realizar tarefas específicas. Devem conter seção Pré-requisitos listando dependências e configurações necessárias. Devem conter seção Passos com instruções sequenciais para completar a tarefa.

## Entity

Documentos de entidade do modelo de domínio. Devem descrever atributos, relacionamentos e regras de negócio da entidade de forma completa.

## Validação

Os scripts em .scripts/carf_validator validam estrutura de documentos com códigos STRUCT001 e STRUCT002 para seções ausentes, e FRONT001 a FRONT003 para campos de frontmatter ausentes.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
