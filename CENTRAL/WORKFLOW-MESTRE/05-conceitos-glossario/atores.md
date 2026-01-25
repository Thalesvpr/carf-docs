---
type: glossary
status: approved
updated: 2026-01-25
category: atores
---

# Atores

Definicoes dos perfis de usuario do sistema CARF.

## Analista de Drone

Profissional responsavel por gerar e entregar ortofotos prontas para o sistema.

**Responsabilidades:**
- Realizar voos de drone
- Processar mosaicos
- Entregar ortofotos via portal de upload

**Autenticacao:**
- Keycloak (login/senha)

**Acesso:**
- Portal de upload de ortofotos
- Restrito ao TENANT designado

## Analista (QGIS Plugin)

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

## Agente de Campo

Profissional que atua no territorio realizando cadastros e atualizacoes.

**Responsabilidades:**
- Baixar pacote temporario
- Visitar comunidades designadas
- Realizar cadastros (criar/editar/excluir)
- Coletar assinaturas e documentos
- Sincronizar dados com o central

**Autenticacao:**
- Keycloak (login/senha via app)

**Acesso:**
- App REURBCAD
- Pacote de dados do TENANT (apos publicacao)
- Operacao online e offline
