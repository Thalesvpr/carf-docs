---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-047: Clonar Comunidade

## Descricao

Usuarios com role ADMIN podem clonar comunidade existente criando copia completa util para gerenciar fases sequenciais de projeto. Copia inclui geometria de boundary identica, configuracoes de camadas WMS, documentos anexados (opcionalmente) e metadados relevantes. Unidades vinculadas explicitamente nao copiadas garantindo que clone inicia vazio de cadastros. Novo nome gerado automaticamente com possibilidade de edicao imediata.

## Criterios de Aceitacao

1. Clonagem de geometria e metadados
2. Opcao de copiar documentos anexados
3. Unidades nao copiadas (clone vazio)
4. Nome automatico com edicao permitida
5. Redirecionamento para edicao apos clonagem

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-034, RF-008
