---
type: glossary
status: approved
updated: 2026-02-21
category: atores
---

# Atores

Definicoes dos perfis de usuario do sistema CARF.

## Atores por Fase do Workflow

### Parte 1: Entrega de Ortofotos

#### Operador de Drone

Profissional responsavel por entregar ortofotos prontas ao sistema via portal de upload.

**Responsabilidades:**
- Entregar ortofotos via portal de upload

**Autenticacao:**
- Keycloak (login/senha)
- Role no Keycloak: `drone-operator`

**Acesso:**
- Portal de upload de ortofotos
- Restrito ao TENANT designado

### Parte 2: Georreferenciamento

#### Analista (QGIS Plugin)

Profissional que usa o Plugin GEOGIS para georreferenciar areas e publicar trabalho.

**Responsabilidades:**
- Acessar ortofotos do TENANT
- Desenhar poligonos de comunidades/quadras/lotes
- Validar topologia
- Publicar trabalho no backend

**Autenticacao:**
- Keycloak (login/senha)
- AUTHENTICATION KEY (camada extra)

**Acesso:**
- Plugin QGIS (GEOGIS)
- Ortofotos do TENANT
- Publicacao de poligonos

### Parte 3: Operacao de Campo

#### Coordenador de Campo (field-coordinator)

Profissional que lidera a equipe de campo, seleciona regioes de trabalho e acompanha metricas.

**Responsabilidades:**
- Baixar pacote temporario
- **Selecionar comunidade/regiao de atuacao no app**
- Visualizar metricas da equipe
- Acessar lista de membros da equipe
- Acompanhar dashboard de produtividade
- Visitar comunidades designadas
- Realizar cadastros (criar/editar/excluir)
- Coletar assinaturas e documentos
- Sincronizar dados com o central

**Interface Mobile:**
- **Menu inferior (Bottom Navigation)** com:
  - Home (metricas)
  - Mapa
  - Equipe
  - Perfil/Configuracoes

**Autenticacao:**
- Keycloak (login/senha via app)

**Acesso:**
- App REURBCAD (interface completa)
- Pacote de dados do TENANT (apos publicacao)
- Operacao online e offline

#### Cadastrador de Campo (field-cadastrator)

Profissional que executa cadastros no territorio, vinculado a uma regiao atribuida pelo administrador.

**Responsabilidades:**
- Baixar pacote temporario
- Visualizar mapa da regiao atribuida
- Realizar cadastros (criar/editar/excluir)
- Coletar assinaturas e documentos
- Criar pings em lotes
- Sincronizar dados com o central

**Interface Mobile:**
- **SEM menu inferior** - abre direto no mapa
- Nao visualiza metricas de colegas
- Nao seleciona regiao (recebe atribuicao do Admin/Manager)

**Autenticacao:**
- Keycloak (login/senha via app)

**Acesso:**
- App REURBCAD (interface simplificada)
- Pacote de dados do TENANT (apos publicacao)
- Operacao online e offline

## Comparativo: Coordenador vs Cadastrador

| Funcionalidade | Coordenador | Cadastrador |
|----------------|:-----------:|:-----------:|
| Bottom Navigation | SIM | NAO |
| Seleciona regiao no app | SIM | NAO |
| Ve metricas da equipe | SIM | NAO |
| Ve lista de membros | SIM | NAO |
| Dashboard produtividade | SIM | NAO |
| Preenche formularios | SIM | SIM |
| Captura fotos/assinatura | SIM | SIM |
| Cria pings em lotes | SIM | SIM |
| Sincroniza dados | SIM | SIM |

## Atores Administrativos

### Analyst (Web)

Profissional que revisa cadastros e recomenda aprovacao via sistema web.

**Responsabilidades:**
- Revisar cadastros submetidos
- Validar documentacao
- Recomendar aprovacao ou rejeicao

**Acesso:**
- REURBWEB (painel de revisao)
- Dados do TENANT designado

### Manager

Profissional que aprova unidades e gerencia processos de legitimacao.

**Responsabilidades:**
- Aprovar ou rejeitar cadastros revisados
- Gerenciar processos de legitimacao fundiaria
- Emitir certidoes (com permissoes adequadas)

**Acesso:**
- REURBWEB (painel de aprovacao)
- Dados do TENANT designado

### Admin

Administrador do tenant que gerencia usuarios, times e configuracoes.

**Responsabilidades:**
- Criar e gerenciar usuarios
- Criar e gerenciar equipes
- Designar usuarios a roles
- Configurar tenant

**Acesso:**
- ADMIN (painel administrativo)
- Dados do TENANT designado

### Super Admin

Acesso irrestrito incluindo todos os tenants. Equipe tecnica de infraestrutura.

**Responsabilidades:**
- Gerenciar todos os tenants
- Configurar sistema global
- Monitorar infraestrutura

**Acesso:**
- Todos os sistemas
- Todos os tenants

## Referencia

- Permissoes por role: `CENTRAL/DOMAIN-RULES/WORKFLOWS/03-role-permissions.md`
- Keycloak realm: `CENTRAL/INTEGRATION/KEYCLOAK/realm-export.json`
- UI Pattern (Bottom Navigation): `CENTRAL/DESIGN-SYSTEM/PATTERNS/bottom-navigation.md`
