---
type: workflow
status: approved
updated: 2026-02-07
part: 3
---

# PARTE 3: Operacao em Campo

Fluxo onde a equipe de campo (Coordenador e Cadastrador) consome o pacote publicado e executa operacoes no territorio.

## Atores

| Ator | Papel |
|------|-------|
| Coordenador de Campo | Lidera equipe, seleciona regiao, ve metricas |
| Cadastrador de Campo | Executa cadastros na regiao atribuida |
| Backend (GEOAPI) | Fornece pacote temporario e recebe sincronizacao |
| Keycloak | Autentica os usuarios de campo |
| App REURBCAD | Aplicativo mobile para operacao em campo |

## Diferenca entre Coordenador e Cadastrador

| Aspecto | Coordenador | Cadastrador |
|---------|-------------|-------------|
| Bottom Navigation | SIM | NAO |
| Seleciona regiao | SIM | NAO |
| Ve metricas equipe | SIM | NAO |
| Preenche formularios | SIM | SIM |

Ver detalhes em: `CENTRAL/DESIGN-SYSTEM/PATTERNS/bottom-navigation.md`

## Pre-condicoes

- Usuario de campo possui credenciais validas no Keycloak
- Usuario de campo esta designado a um TENANT
- Analista JA PUBLICOU o trabalho do TENANT (PARTE 2 concluida)
- App REURBCAD instalado no dispositivo mobile

## Passos

| Passo | Descricao | Documento |
|-------|-----------|-----------|
| 11 | Designacao ao TENANT | [passo-11-designacao.md](./passo-11-designacao.md) |
| 12 | Download do Pacote Temporario | [passo-12-download.md](./passo-12-download.md) |
| 13 | Selecao de Comunidade | [passo-13-selecao.md](./passo-13-selecao.md) |
| 14 | Carregamento do Mapa | [passo-14-mapa.md](./passo-14-mapa.md) |
| 15 | Fluxo Operacional em Campo | [passo-15-fluxo-operacional.md](./passo-15-fluxo-operacional.md) |
| 16 | Pre-Formulario | [passo-16-pre-formulario.md](./passo-16-pre-formulario.md) |
| 17 | Formulario Completo | [passo-17-formulario.md](./passo-17-formulario.md) |
| 18 | Finalizacao e Sincronizacao | [passo-18-finalizacao.md](./passo-18-finalizacao.md) |

## Pos-condicoes

- Cadastros realizados em campo
- Dados armazenados localmente (offline)
- Dados sincronizados com backend (quando online)
- Status dos lotes atualizados
- Metricas de produtividade registradas

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| RN-11 | Equipe de campo so acessa dados APOS publicacao do Analista |
| RN-12 | Download do pacote e UNICO e TEMPORARIO |
| RN-13 | App funciona completamente OFFLINE |
| RN-14 | Sincronizacao ocorre quando ha conectividade |
| RN-15 | Dados do titular sao OBRIGATORIOS |
| RN-16 | Assinatura digital e OBRIGATORIA |

## Integracao com Sistemas

| Sistema | Responsabilidade |
|---------|------------------|
| App REURBCAD | Interface mobile para campo |
| Keycloak | Autenticacao OAuth2/OIDC |
| GEOAPI | Fornece pacote, recebe sincronizacao |
| WatermelonDB | Armazenamento local offline |

## Fluxo Completo Concluido

Apos a PARTE 3, o ciclo completo esta finalizado:
- Ortofoto entregue e processada (PARTE 1)
- Poligonos georreferenciados e publicados (PARTE 2)
- Cadastros realizados em campo e sincronizados (PARTE 3)

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (8)

| Documento | Status |
|-----------|--------|
| [Passo 11: Designacao ao TENANT](./passo-11-designacao.md) | ⚠ |
| [Passo 12: Download do Pacote Temporario](./passo-12-download.md) | ⚠ |
| [Passo 13: Selecao de Comunidade](./passo-13-selecao.md) | ⚠ |
| [Passo 14: Carregamento do Mapa](./passo-14-mapa.md) | ⚠ |
| [Passo 15: Fluxo Operacional em Campo](./passo-15-fluxo-operacional.md) | ⚠ |
| [Passo 16: Pre-Formulario](./passo-16-pre-formulario.md) | ⚠ |
| [Passo 17: Formulario Completo de Cadastro](./passo-17-formulario.md) | ⚠ |
| [Passo 18: Finalizacao e Sincronizacao](./passo-18-finalizacao.md) | ⚠ |

<!-- CARF-INDEX-END -->
