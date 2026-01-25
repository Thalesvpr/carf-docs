---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
---

# RF-031: Perfil de Usuario

## Descricao

Usuario autenticado pode visualizar e editar seu proprio perfil. Exibicao inclui informacoes basicas como nome completo, email, role atribuida, tenant vinculado e data de criacao da conta. Edicao de foto de perfil implementada com upload de imagem validando formato (JPEG, PNG) e tamanho maximo, aplicando redimensionamento automatico para dimensoes padronizadas. Alteracao de senha propria disponivel atraves de formulario seguro validando senha atual antes de permitir definicao de nova senha com sincronizacao em Keycloak.

## Criterios de Aceitacao

1. Visualizacao de dados basicos do perfil
2. Upload de foto com validacao de formato e tamanho
3. Redimensionamento automatico da foto
4. Alteracao de senha validando senha atual
5. Sincronizacao de senha com Keycloak

## Rastreabilidade

- Modulos: GEOWEB
- Requisitos dependentes: RF-001, RF-021
