---
type: leaf
status: review
description: "Usa tabela e diagrama ao inves de prosa densa - reescrever em paragrafos corridos"
updated: 2026-01-22
---

# Hierarquia de Roles

Sistema CARF implementa seis níveis de roles sendo cinco operacionais hierárquicos onde roles superiores herdam automaticamente permissões das inferiores através de composite roles no Keycloak, mais uma role transversal para desenvolvedores.

## Tabela de Roles

| Role | Descrição | Acesso Principal |
|------|-----------|------------------|
| `user` | Usuário padrão | Funcionalidades básicas, docs públicas |
| `field-cadastrator` | Cadastrador de campo | REURBCAD apenas mapa e formularios, sem menu |
| `field-coordinator` | Coordenador de campo | REURBCAD, coleta offline, upload fotos, menu completo, supervisao |
| `analyst` | Analista REURB | Gestão de unidades, titulares, aprovações |
| `admin` | Administrador | Gestão de tenants, usuários, permissões |
| `super-admin` | Super administrador | Acesso total, multi-tenant |
| `dev` | Desenvolvedor (transversal) | Seção /dev/ no WebDocs, Swagger, logs |

## Detalhamento das Roles

Role user é o nível mais básico concedido automaticamente a todos usuários autenticados. Permite acessar documentação pública no WEBDOCS, visualizar informações básicas do próprio perfil, e usar funcionalidades públicas das aplicações. Não concede acesso a dados operacionais do sistema CARF.

Role field-cadastrator é destinada a cadastradores de campo que utilizam REURBCAD para coleta de dados com acesso restrito apenas ao mapa e formularios, sem menu completo. Herda permissões de user e adiciona: criar e editar unidades próprias, fazer upload de fotos e documentos. Não pode deletar registros, aprovar unidades ou acessar dados de outros coletores.

Role field-coordinator é destinada a coordenadores de campo que supervisionam equipes de cadastradores. Herda permissões de field-cadastrator e adiciona: menu mobile completo, visualização de dados da equipe, coordenação de trabalho em campo.

Role analyst herda de field-coordinator e adiciona capacidade de aprovar, rejeitar ou solicitar correções em unidades cadastradas, criar e editar qualquer unidade do tenant independente do criador original, gerar relatórios consolidados e exportar dados em formatos CSV e PDF.

Role admin herda de analyst e adiciona gerenciamento de usuários do tenant incluindo criar contas, editar perfis, atribuir roles e desativar acessos. Também permite configurar preferências do tenant como nome e CNPJ, visualizar audit logs de ações no tenant, e gerenciar equipes de trabalho.

Role super-admin herda de admin e adiciona capacidade de criar novos tenants/prefeituras, transferir usuários entre tenants mantendo histórico, deletar tenants inativos, acessar qualquer tenant via switcher especial sem validação de allowed_tenants, e gerenciar realm Keycloak via Admin API.

## Role Transversal

Role dev é transversal e não participa da hierarquia operacional podendo ser combinada com qualquer outra role sem relação de herança. Destina-se a desenvolvedores que precisam acessar seção /dev/ do WEBDOCS contendo Swagger interativo, documentação técnica interna, métricas de debug e guias de contribuição. Não concede permissões operacionais no sistema CARF sendo necessária atribuição explícita mesmo para usuários admin ou super-admin. Ver [02-role-dev.md](./02-role-dev.md) para detalhes.

## Diagrama de Herança

```
user (base)
  └── field-cadastrator
        └── field-coordinator
              └── analyst
                    └── admin
                          └── super-admin

dev (transversal - pode ser combinada com qualquer role acima)
```
