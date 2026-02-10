---
type: readme
status: approved
updated: 2026-02-07
---

# WORKFLOW-MESTRE

Fonte unica de verdade do sistema CARF. Este workflow define o fluxo completo end-to-end desde a entrega de ortofotos ate a operacao em campo.

## Objetivo

Garantir que ortofotos (drone) sejam recebidas, processadas (reducao/tamanhos), armazenadas em bucket, distribuidas por regiao (TENANT) e usadas por analistas (via plugin autenticado) para georreferenciar e produzir poligonos (comunidades, lotes etc.). Somente apos o analista "publicar" seu trabalho no backend, a equipe de campo (Coordenador e Cadastrador, designados ao mesmo tenant) pode baixar temporariamente (download unico) a ortofoto + poligonos e executar o fluxo completo de campo (online/offline), com GPS, acoes no mapa e cadastros, assinaturas e sincronizacao.

## Atores

| Ator | Responsabilidade | Sistema |
|------|------------------|---------|
| Analista de Drone | Publicar/entregar ortofotos prontas via link de upload | Portal Upload |
| Backend | Receber ortofotos, reduzir tamanho, armazenar em bucket, controlar permissoes | GEOAPI |
| Keycloak | Autenticacao e autorizacao (login, emissao/validacao de tokens) | Keycloak |
| Analista (QGIS Plugin) | Acessar ortofotos do tenant, georreferenciar lotes/comunidades, enviar poligonos | GEOGIS |
| Coordenador de Campo | Liderar equipe, selecionar regiao, acompanhar metricas | REURBCAD |
| Cadastrador de Campo | Executar cadastros e atualizacoes no mapa, sincronizar | REURBCAD |
| Bucket de Objetos | Armazenamento das ortofotos (originais e versoes reduzidas) | S3/MinIO |

## Partes do Workflow

| Parte | Nome | Passos | Documento |
|-------|------|--------|-----------|
| 1 | Entrega e Processamento de Ortofotos | 1-4 | [01-entrega-ortofotos/](./01-entrega-ortofotos/README.md) |
| 2 | Georreferenciamento e Publicacao | 5-10 | [02-georreferenciamento/](./02-georreferenciamento/README.md) |
| 3 | Operacao em Campo | 11-18 | [03-operacao-campo/](./03-operacao-campo/README.md) |

## Documentos Complementares

| Documento | Descricao |
|-----------|-----------|
| 04-regras-inegociaveis/ | Regras que nao podem ser alteradas |
| 05-conceitos-glossario/ | Definicoes e termos padronizados |

## Resumo das Partes

Na Parte 1, o Analista de Drone autentica via Keycloak (passo 1), envia a ortofoto (passo 2), o backend processa e reduz tamanho (passo 3) e salva em bucket por tenant (passo 4). Na Parte 2, o Analista e designado ao tenant (passo 5), autentica via Keycloak e AUTHENTICATION KEY (passo 6), acessa ortofotos (passo 7), georreferencia poligonos (passo 8), publica no backend (passo 9) e dados ficam liberados (passo 10). Na Parte 3, somente apos publicacao, a equipe e designada ao tenant (passo 11), baixa pacote temporario (passo 12), Coordenador seleciona comunidade (passo 13), mapa carrega (passo 14) e o fluxo operacional inclui GPS, acoes, formulario, assinatura, QR e sincronizacao (passos 15-18).

## Conceito Central: TENANT

TENANT = uma regiao/area de atuacao. Tudo (ortofotos, poligonos, tarefas, usuarios) e segregado por tenant. Um usuario so enxerga e opera dados do(s) tenant(s) ao qual foi designado.

## Regra Critica

A equipe de campo so tem acesso aos dados DEPOIS que o analista publicou o trabalho do tenant no backend. O download e unico e temporario.

## Roles de Campo

| Role | Keycloak Name | Diferencial |
|------|---------------|-------------|
| Coordenador | field-coordinator | Bottom Navigation, seleciona regiao, ve metricas |
| Cadastrador | field-cadastrator | Interface simplificada, vai direto pro mapa |

Ver detalhes em: `CENTRAL/DESIGN-SYSTEM/PATTERNS/bottom-navigation.md`

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Subpastas (5)

| Pasta | Descrição |
|-------|-----------|
| [01-entrega-ortofotos](./01-entrega-ortofotos/README.md) | ... |
| [02-georreferenciamento](./02-georreferenciamento/README.md) | ... |
| [03-operacao-campo](./03-operacao-campo/README.md) | ... |
| [04-regras-inegociaveis](./04-regras-inegociaveis/README.md) | ... |
| [05-conceitos-glossario](./05-conceitos-glossario/README.md) | ... |

<!-- CARF-INDEX-END -->
