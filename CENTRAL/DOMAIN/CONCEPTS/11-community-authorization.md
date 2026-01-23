---
type: leaf
status: review
updated: 2026-01-22
---

# Autorizacao de Comunidade

Permissao que define quem pode acessar dados de uma comunidade especifica e quais operacoes pode realizar. Controla acesso granular por equipe ou usuario individual.

Autorizacoes sao o mecanismo de seguranca que impede acesso nao autorizado. Usuario so ve comunidades para as quais tem autorizacao explicita, seja via equipe ou individual.

## Niveis de Permissao

Permissoes sao independentes para cada operacao. Usuario pode ter permissao de leitura sem poder editar. Pode criar novos registros sem poder deletar. Cada combinacao atende necessidades diferentes.

## Via Equipe

Quando autorizacao e concedida a uma equipe, todos os membros herdam automaticamente. E a forma mais comum - equipes recebem acesso as comunidades que trabalham.

## Individual

Autorizacoes individuais atendem casos especificos. Consultor externo precisa acesso temporario. Analista precisa ver comunidade fora de sua equipe para validacao. Gestor precisa supervisionar comunidades de outras equipes.

## Sincronizacao Mobile

Autorizacoes definem o escopo de download offline. Aplicativo mobile so sincroniza comunidades autorizadas, economizando espaco e evitando exposicao de dados desnecessarios.
