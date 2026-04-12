---
type: glossary
status: approved
updated: 2026-01-25
category: termos
---

# Termos Tecnicos

Glossario de termos tecnicos utilizados no sistema CARF.

## Termos

| Termo | Definicao |
|-------|-----------|
| Poligono | Geometria fechada representando area (comunidade/quadra/lote) |
| Georreferenciamento | Processo de atribuir coordenadas geograficas a dados |
| Topologia | Relacoes espaciais entre geometrias (sem sobreposicao, sem gaps) |
| Sincronizacao | Troca de dados entre app local e servidor central |
| PUSH | Envio de dados locais para o servidor |
| PULL | Recebimento de dados do servidor para local |
| Offline-first | Arquitetura onde app funciona sem conexao |
| WatermelonDB | Banco de dados local para React Native |
| RLS | Row-Level Security - isolamento no banco de dados |
| OAuth2 PKCE | Protocolo de autenticacao para apps desktop/mobile |

## Detalhamento

### Poligono

Representacao geometrica de uma area:
- **Comunidade**: Limite externo da area de interesse
- **Quadra**: Divisao interna da comunidade
- **Lote**: Unidade individual dentro da quadra

### Georreferenciamento

Atribuicao de coordenadas geograficas:
- Vincula dados a posicao no mundo real
- Permite visualizacao em mapas
- Base para operacoes espaciais

### Topologia

Regras de relacionamento espacial:
- Sem sobreposicao entre poligonos
- Sem gaps (buracos) entre adjacentes
- Hierarquia: Lote dentro de Quadra dentro de Comunidade

### Sincronizacao

Mecanismo de troca de dados:
- **PUSH**: App envia dados locais para o servidor
- **PULL**: App recebe atualizacoes do servidor
- **Conflitos**: Resolvidos por last-write-wins

### Offline-first

Arquitetura de aplicativo:
- Funciona completamente sem conexao
- Dados armazenados localmente
- Sincroniza quando ha conectividade

### RLS (Row-Level Security)

Isolamento no banco de dados:
- Cada linha pertence a um TENANT
- Queries automaticamente filtradas
- Usuario so ve dados do seu TENANT

### OAuth2 PKCE

Protocolo de autenticacao seguro:
- PKCE (Proof Key for Code Exchange)
- Usado para apps desktop e mobile
- Nao requer client secret no app
