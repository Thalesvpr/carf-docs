---
id: UC-011
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-011: Gerenciar Equipes Tecnicas

## Atores

- Primario: ADMIN, MANAGER
- Secundario: Sistema de notificacao

## Pre-condicoes

- Usuario autenticado com permissao de gerenciamento de equipes
- Usuarios disponiveis para adicionar como membros

## Fluxo Principal

1. Usuario acessa menu Administracao > Equipes
2. Sistema exibe lista de equipes existentes
3. Usuario clica em Nova Equipe
4. Sistema exibe formulario de criacao
5. Usuario preenche nome e descricao da equipe
6. Usuario seleciona lider da equipe
7. Usuario define status (Ativa/Inativa)
8. Usuario clica Criar Equipe
9. Sistema valida dados (nome unico, lider valido)
10. Sistema cria equipe e exibe tela de detalhes
11. Usuario acessa tab Membros
12. Usuario clica Adicionar Membro
13. Sistema exibe usuarios disponiveis
14. Usuario seleciona membros e define papeis
15. Sistema adiciona membros a equipe
16. Usuario acessa tab Comunidades
17. Usuario atribui comunidades a equipe
18. Sistema notifica lider e membros sobre inclusao

## Fluxos Alternativos

- FA-001: Editar equipe existente
- FA-002: Alterar lider da equipe

## Fluxos de Excecao

- FE-001: Nome de equipe duplicado
- FE-002: Lider invalido ou inativo

## Pos-condicoes

- Equipe criada com lider definido
- Membros adicionados com papeis atribuidos
- Comunidades vinculadas a equipe
- Notificacoes enviadas aos envolvidos
