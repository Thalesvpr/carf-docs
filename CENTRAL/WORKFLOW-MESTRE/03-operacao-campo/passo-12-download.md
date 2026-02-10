---
type: workflow
status: approved
updated: 2026-02-07
part: 3
step: 12
---

# Passo 12: Download do Pacote Temporario

Coordenador de Campo ou Cadastrador de Campo baixa o pacote de dados para operacao em campo.

## Atores

- **Coordenador de Campo**: baixa pacote e seleciona regiao
- **Cadastrador de Campo**: baixa pacote da regiao atribuida

## Fluxo

1. Usuario de campo abre o app REURBCAD
2. App autentica via Keycloak
3. App consulta backend via requisicao GET para /api/pacotes/campo com parametro tenant_id, autenticado com Bearer token
4. Backend verifica que o usuario pertence ao TENANT e que o Analista ja publicou o trabalho
5. Somente se publicado, o backend disponibiliza pacote contendo ortofoto (versao offline), poligonos georreferenciados (comunidades, quadras, lotes) e metadados
6. Download e unico e temporario (link expira)
7. App armazena pacote localmente (WatermelonDB)

## Dados da Resposta

| Campo | Descricao |
|-------|-----------|
| pacote_id | UUID do pacote |
| tenant_id | UUID do tenant |
| download_url | URL presigned para download |
| expires_at | Data e hora de expiracao |
| conteudo.ortofoto | URL e bounding box da ortofoto |
| conteudo.comunidades | Lista de comunidades |
| conteudo.quadras | Lista de quadras |
| conteudo.lotes | Lista de lotes |

## Regra Critica

**PUB-02:** Usuario de campo SO consegue baixar dados QUANDO Analista JA PUBLICOU.

Se o Analista ainda nao publicou, o backend retorna erro 404.

## Caracteristicas do Pacote

| Caracteristica | Descricao |
|----------------|-----------|
| Link expiravel | URL presigned com tempo limite |
| Download unico | Apenas um download por link |
| Armazenamento local | Salvo em WatermelonDB |
| Operacao offline | Permite trabalho sem conexao |

## Comportamento por Role

| Role | Apos Download |
|------|---------------|
| Coordenador | Ve Bottom Navigation, seleciona comunidade |
| Cadastrador | Vai direto pro mapa da regiao atribuida |

## Resultado

- Pacote baixado para o dispositivo
- Dados armazenados localmente
- App pronto para operacao offline

## Proximo Passo

Passo 13: Selecao de Comunidade
