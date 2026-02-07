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

## Diagrama Visual

```
PARTE 1                          PARTE 2                          PARTE 3
Drone → Backend → Bucket         Analista → Plugin → Backend      Equipe → Download → Campo

┌─────────────────┐              ┌─────────────────┐              ┌─────────────────┐
│ Analista Drone  │              │ Analista QGIS   │              │ Equipe Campo    │
│                 │              │                 │              │ (Coord + Cad)   │
│ 1. Autentica    │              │ 5. Designado    │              │ 11. Designado   │
│    Keycloak     │              │    ao TENANT    │              │     ao TENANT   │
│                 │              │                 │              │                 │
│ 2. Envia        │              │ 6. Autentica    │              │ 12. Download    │
│    ortofoto     │              │    Keycloak +   │              │     temporario  │
│                 │              │    AUTH KEY     │              │                 │
└────────┬────────┘              │                 │              │ 13. Seleciona   │
         │                       │ 7. Acessa       │              │     comunidade  │
         ▼                       │    ortofotos    │              │     (Coord)     │
┌─────────────────┐              │                 │              │                 │
│ Backend         │              │ 8. Georrefe-    │              │ 14. Mapa        │
│                 │              │    rencia       │              │     carrega     │
│ 3. Processa     │              │                 │              │                 │
│    reduz        │              │ 9. Publica      │──────────────│ 15. Fluxo       │
│    tamanho      │              │    backend      │  SOMENTE     │     operacional │
│                 │              │                 │  APOS        │     GPS, acoes  │
│ 4. Salva em     │              │ 10. Dados       │  PUBLICACAO  │     formulario  │
│    bucket por   │              │     liberados   │              │     assinatura  │
│    TENANT       │              │                 │              │     QR, sync    │
└─────────────────┘              └─────────────────┘              └─────────────────┘
```

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
