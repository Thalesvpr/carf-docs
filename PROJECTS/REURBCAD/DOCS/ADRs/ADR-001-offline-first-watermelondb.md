---
type: adr
status: review
updated: 2026-02-08
---

# ADR-001: Escolha de Arquitetura Offline-First com WatermelonDB

## Status

Aprovado e implementado desde inicio do projeto (2024-Q3). Revisao prevista apenas se WatermelonDB demonstrar limitacoes criticas de performance ou sync (improvavel dado adocao por apps enterprise como TrailGuide e ProductHunt) ou se surgir solucao offline-first fundamentalmente superior.

## Contexto

O aplicativo mobile REURBCAD tem requisito critico de coleta de dados em campo em areas rurais e comunidades perifericas sem cobertura celular confiavel. O trabalho de tecnicos nao pode depender de conectividade intermitente, sob risco de perda de produtividade e dados coletados.

Justificativas para arquitetura offline-first:

- **Coleta em campo sem conectividade**: Areas rurais e comunidades perifericas sem cobertura celular confiavel
- **Experiencia de usuario superior**: Responsividade instantanea em todas operacoes (listagens, buscas, formularios) eliminando latencia de rede e loading spinners frustrantes, aumentando satisfacao e adocao do app
- **Resiliencia a falhas de rede**: Problemas de conectividade nao bloqueiam trabalho, permitindo tecnicos continuarem cadastros mesmo durante interrupcoes temporarias ou degradacao de sinal
- **Economia de dados moveis**: Reducao de consumo de plano celular corporativo atraves de sincronizacao inteligente apenas de deltas e compressao de payloads - importante para prefeituras com orcamento limitado
- **Escalabilidade melhorada**: Desacoplamento de carga de leitura do backend onde milhares de consultas locais nao geram trafego no servidor, reduzindo custos de infraestrutura e melhorando performance global do sistema

## Decisao

Escolhemos **WatermelonDB** como database local para implementar a arquitetura offline-first. Recursos que justificam a escolha:

- **Database relacional completo baseado em SQLite**: Performance nativa executando queries complexas com joins e indices em milissegundos, comparavel a acesso direto ao PostgreSQL mas totalmente local
- **Lazy loading automatico**: Carrega apenas dados visiveis em tela, otimizando memoria ao evitar overhead de carregar grafos completos de objetos
- **Observables reativos**: Integra nativamente com React atraves de hooks, garantindo que UI atualiza automaticamente quando dados locais mudam sem codigo boilerplate de listeners
- **Sync engine bidirecional robusto**: Suporta conflict resolution automatico para edicoes concorrentes do mesmo registro usando estrategias configuraveis (last-write-wins, server-wins, custom merge)
- **Migrations automaticas de schema**: Permite evolucao de modelo de dados em novas versoes do app sem quebrar dados existentes em dispositivos antigos - critico para manutencao de longo prazo
- **Performance otimizada para mobile**: Batch operations reduzindo overhead de I/O do SQLite e indexacao inteligente mantendo queries sub-100ms mesmo com dezenas de milhares de registros locais
- **Integracao nativa com React Native via JSI**: Elimina necessidade de bridges lentos entre JavaScript e SQLite usando JavaScript Interface para acesso sincrono ao database

## Arquitetura Implementada

### Padrao Pull-Push

App funciona 100% localmente em modo default, lendo e escrevendo apenas no WatermelonDB local. Sincronizacao ocorre em background automaticamente quando conectividade esta disponivel.

Algoritmo pull-push:

1. **Pull**: Baixa mudancas do servidor aplicando localmente
2. **Push**: Envia mudancas locais pendentes
3. **Conflict Resolution**: Resolve conflitos entre versoes

### Sincronizacao Incremental

Timestamps de ultima modificacao em cada registro permitem sincronizacao incremental, evitando transfer de dataset completo e reduzindo payload em 95-99%.

### Conflict Resolution

- **Default**: Last-write-wins
- **Campos criticos** (geometria de unidade, status, titular): Fallback para manual resolution marcando registro como `conflicted` e apresentando UI de merge para usuario

### Queue Persistente

Queue persistente de operacoes pendentes garante que acoes offline (criar unidade, adicionar foto, vincular titular) nao sejam perdidas mesmo se app crashar antes de sincronizar.

## Alternativas Consideradas

| Alternativa | Motivo da Rejeicao |
|---|---|
| **Realm** | Sync engine proprietario exigindo Realm Cloud ou MongoDB Atlas com custos variaveis imprevisiveis. Limitacoes de queries complexas comparado a SQL completo. |
| **PouchDB/CouchDB** | Performance inferior em mobile devido a overhead de JSON e ausencia de indices otimizados para queries espaciais. Tamanho de database crescendo indefinidamente sem compaction. |
| **AsyncStorage** | Key-value store simples sem suporte a queries complexas ou relacionamentos. Exigiria implementacao manual de indices e joins - impossivel de escalar. |
| **SQLite raw** (react-native-sqlite-storage) | Falta de sync engine exigindo implementacao manual de sincronizacao, conflitos e migrations. Ausencia de reactive updates automaticos. |
| **Firebase Realtime Database** | Exige conectividade online para funcionalidade completa. Modelo de dados NoSQL limitado. Custos por operacao tornando inviavel para uso intenso. |

## Consequencias Positivas

- **UX excepcional**: App sempre responsivo independente de conectividade, aumentando satisfacao e produtividade de tecnicos em campo
- **Trabalho offline garantido**: Coleta de dados em areas remotas sem cobertura celular, habilitando uso em 100% do territorio versus ~70% com abordagem online-only
- **Resiliencia a falhas de rede**: Elimina frustracao de erros de timeout e perda de trabalho
- **Economia de dados moveis**: Reduz custo operacional de planos celulares corporativos
- **Escalabilidade melhorada**: Descarrega leitura do backend

## Consequencias Negativas

- **Complexidade de sincronizacao**: Exige logica robusta de conflict resolution e tratamento de edge cases (exemplo: registro deletado no servidor enquanto editado offline)
- **Overhead de armazenamento local**: Database SQLite crescendo ate ~100-500MB apos meses de uso, exigindo estrategia de archival de dados antigos
- **Debugging mais complexo**: Estados divergentes entre cliente e servidor dificultam reproducao de bugs
- **Dados potencialmente stale**: Se usuario ficar offline por dias sem sincronizar, pode causar decisoes baseadas em informacao desatualizada (mitigado com indicadores visuais de ultima sync)
- **Features real-time limitadas**: Impossibilidade de features que exigem dados real-time absolutos (exemplo: notificacoes instantaneas de aprovacao) exigindo push notifications complementares

## Configuracao Especifica

| Parametro | Valor | Justificativa |
|---|---|---|
| WatermelonDB version | 0.27+ | JSI habilitado para performance maxima |
| SQLite backend | WAL mode habilitado | Melhor concorrencia entre leitura e escrita |
| Sync automatico (WiFi) | A cada 15 minutos | Balanco entre atualizacao e uso de recursos |
| Sync manual (celular) | Via pull-to-refresh | Economiza dados moveis |
| Batch size | 500 registros por request | Balanceia payload com numero de requests |
| Conflict resolution (default) | Last-write-wins | Simples e previsivel para maioria dos campos |
| Conflict resolution (critico) | UI de merge manual | Para conflitos em geometria, status, titular |
| Retention policy | 6 meses | Deleta registros locais antigos, mantendo database compacto |

## Referencias

- [Offline Authentication](../CONCEPTS/02-offline-authentication.md)
- [Offline Sync Patterns](../../GEOAPI/DOCS/PATTERNS/01-mobile-offline-first.md)
- [Sync Protocol Detail](../../GEOAPI/DOCS/PATTERNS/04-sync-protocol-detail.md)
