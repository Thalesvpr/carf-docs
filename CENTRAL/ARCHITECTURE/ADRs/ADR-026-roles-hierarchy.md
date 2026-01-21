---
status: rejected
updated: 2026-01-21
description: "Sobreposicao com ADR-022 (RBAC). Formato incorreto com tabelas de permissoes, diagramas ASCII. Consolidar e simplificar. Contem blocos de codigo."
---

# ADR-026: Hierarquia de Roles CARF

## Contexto

O sistema CARF atende diferentes perfis de usuarios com niveis de acesso distintos: desde cidadaos consultando documentacao ate super-administradores gerenciando multiplos municipios. O modelo de autorizacao precisa suportar hierarquia de permissoes onde roles superiores herdam capacidades das inferiores, alem de roles transversais para casos especiais como desenvolvedores.

Keycloak oferece composite roles para implementar heranca, realm roles para permissoes globais e client roles para permissoes especificas por aplicacao.

## Decisao

Implementar **hierarquia de 5 niveis operacionais** com heranca automatica via composite roles, mais **1 role transversal** sem relacao hierarquica.

### Roles Operacionais (Hierarquicas)

| Role | Nivel | Herda de | Acesso Principal |
|:-----|:------|:---------|:-----------------|
| `user` | 1 | - | Funcionalidades basicas, docs publicas |
| `field-agent` | 2 | user | REURBCAD, coleta offline, upload fotos |
| `analyst` | 3 | field-agent | Gestao de unidades, aprovacoes, relatorios |
| `admin` | 4 | analyst | Gestao de usuarios, configuracao tenant |
| `super-admin` | 5 | admin | Acesso total, multi-tenant, gestao realm |

### Role Transversal

| Role | Tipo | Combinavel com | Acesso |
|:-----|:-----|:---------------|:-------|
| `dev` | transversal | qualquer role | Secao /dev/ WebDocs, Swagger, logs debug |

### Diagrama de Heranca

```
user (base - todos usuarios autenticados)
  |
  +-- field-agent (coleta de dados em campo)
        |
        +-- analyst (analise e aprovacao)
              |
              +-- admin (gestao do tenant)
                    |
                    +-- super-admin (gestao global)

dev (transversal - pode ser atribuida junto com qualquer role acima)
```

### Detalhamento das Permissoes

**user**: Nivel base automaticamente atribuido a todo usuario autenticado. Acessa documentacao publica no WebDocs, visualiza informacoes do proprio perfil, usa funcionalidades publicas. Nao acessa dados operacionais do CARF.

**field-agent**: Agentes de campo usando REURBCAD mobile. Cria e edita unidades proprias, faz upload de fotos/documentos, visualiza mapas do tenant. Nao pode deletar registros, aprovar unidades ou ver dados de outros coletores.

**analyst**: Analistas de regularizacao fundiaria. Aprova/rejeita/solicita correcoes em unidades, edita qualquer unidade do tenant, gera relatorios consolidados, exporta CSV/PDF.

**admin**: Administradores municipais. Gerencia usuarios do tenant (criar, editar roles, desativar), configura preferencias do tenant, visualiza audit logs, gerencia equipes.

**super-admin**: Administradores da plataforma. Cria/deleta tenants, transfere usuarios entre tenants, acessa qualquer tenant via switcher especial, gerencia realm Keycloak.

**dev**: Role transversal para desenvolvedores. Acessa secao /dev/ do WebDocs com Swagger interativo, documentacao tecnica interna, metricas debug. Requer atribuicao explicita, nao herdada.

## Consequencias

### Positivas

**Principio do menor privilegio**: Usuarios recebem apenas permissoes necessarias para sua funcao, reduzindo superficie de ataque.

**Heranca automatica**: Promover usuario de analyst para admin automaticamente concede todas permissoes anteriores sem configuracao manual.

**Separacao dev/ops**: Role dev isolada permite desenvolvedores acessarem ferramentas de debug sem permissoes operacionais, e vice-versa.

**Auditoria clara**: Cada acao no sistema pode ser rastreada ate uma role especifica, facilitando compliance.

### Negativas

**Rigidez hierarquica**: Casos de uso que exigem permissoes de niveis diferentes (ex: field-agent com acesso a relatorios) requerem roles customizadas ou ajustes.

**Composite role overhead**: Keycloak avalia todas roles compostas em cada emissao de token, marginalmente impactando performance com hierarquias profundas.

### Neutras

**Migracao de nomenclatura**: Role anterior `field-collector` renomeada para `field-agent` para consistencia terminologica.

## Alternativas Rejeitadas

### Flat Roles (sem heranca)

Definir cada role independentemente sem composite roles.

**Motivo da rejeicao**: Administradores precisariam atribuir multiplas roles manualmente (user + field-agent + analyst) para um analista, aumentando erro humano e inconsistencia.

### ABAC (Attribute-Based Access Control)

Usar atributos de usuario em vez de roles para controle de acesso.

**Motivo da rejeicao**: Keycloak tem suporte limitado a ABAC nativo, e RBAC com heranca atende os requisitos atuais com menor complexidade. ABAC pode ser adicionado futuramente para permissoes granulares especificas.

### Client Roles Exclusivas

Definir roles apenas no nivel de client (geoweb, reurbcad, etc).

**Motivo da rejeicao**: Permissoes sao transversais entre aplicacoes (analyst acessa tanto GEOWEB quanto REURBCAD). Realm roles permitem definir uma vez e aplicar em todos clients.

## Implementacao Keycloak

```json
// Configuracao de composite role (admin herda de analyst)
{
  "name": "admin",
  "composite": true,
  "composites": {
    "realm": ["analyst"]
  }
}
```

## Metricas de Sucesso

- [ ] 100% dos endpoints protegidos com verificacao de role apropriada
- [ ] Zero usuarios com roles excessivas para sua funcao
- [ ] Tempo de avaliacao de roles < 10ms por request
- [ ] Audit log captura role do usuario em cada acao

## Referencias

- [Keycloak Composite Roles](https://www.keycloak.org/docs/latest/server_admin/#_composite_roles)
- [ADR-022: Role-Based Access Control](./ADR-022-role-based-access-control.md)
- [Roles Implementation](../../PROJECTS/KEYCLOAK/DOCS/INTEGRATION/RBAC/01-roles-hierarchy.md)
