---
id: UC-001
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-001: Cadastrar Unidade Habitacional

## Atores

- Primario: ANALYST, FIELD_AGENT, ADMIN
- Secundario: Sistema de validacao

## Pre-condicoes

- Usuario autenticado com permissao units.create
- Comunidade previamente cadastrada

## Fluxo Principal

1. Usuario acessa tela de cadastro de unidade
2. Sistema exibe formulario com campos obrigatorios e opcionais
3. Usuario seleciona comunidade no dropdown
4. Usuario preenche dados basicos (codigo, endereco, tipo)
5. Usuario desenha geometria no mapa clicando pontos do poligono
6. Sistema calcula area automaticamente apos fechamento
7. Usuario preenche dados opcionais (comodos, material, observacoes)
8. Usuario clica em Salvar
9. Sistema valida dados e geometria
10. Sistema salva unidade com status Draft (ou Pending Approval se FIELD_AGENT)
11. Sistema exibe mensagem de sucesso e redireciona para detalhes

## Fluxos Alternativos

- FA-001: Desenhar geometria offline no mobile
- FA-002: Importar geometria de GPS
- FA-003: Copiar geometria existente

## Fluxos de Excecao

- FE-001: Validacao falha
- FE-002: Geometria sobreposta

## Pos-condicoes

- Unidade criada com status Draft ou Pending Approval
- Registro de auditoria criado
- Unidade visivel no mapa e listagens
