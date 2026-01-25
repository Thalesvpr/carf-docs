---
type: workflow
status: approved
updated: 2026-01-25
part: 2
---

# PARTE 2: Georreferenciamento e Publicacao

Fluxo onde o Analista usa o Plugin QGIS para acessar ortofotos, georreferenciar poligonos e publicar o trabalho no backend.

## Atores

| Ator | Papel |
|------|-------|
| Analista (Plugin QGIS) | Acessa ortofotos, georreferencia e publica trabalho |
| Backend (GEOAPI) | Fornece ortofotos e recebe poligonos publicados |
| Keycloak | Autentica o Analista |
| Plugin GEOGIS | Ferramenta de georreferenciamento no QGIS |

## Pre-condicoes

- Analista possui credenciais validas no Keycloak
- Analista esta designado a um TENANT
- Plugin GEOGIS instalado no QGIS
- Ortofotos do TENANT disponiveis no bucket (PARTE 1 concluida)
- Analista possui AUTHENTICATION KEY valida

## Passos

| Passo | Descricao | Documento |
|-------|-----------|-----------|
| 5 | Designacao ao TENANT | [passo-05-designacao.md](./passo-05-designacao.md) |
| 6 | Autenticacao no Plugin | [passo-06-autenticacao-plugin.md](./passo-06-autenticacao-plugin.md) |
| 7 | Acesso as Ortofotos | [passo-07-acesso-ortofotos.md](./passo-07-acesso-ortofotos.md) |
| 8 | Georreferenciamento | [passo-08-georreferenciamento.md](./passo-08-georreferenciamento.md) |
| 9 | Publicacao no Backend | [passo-09-publicacao.md](./passo-09-publicacao.md) |
| 10 | Dados Liberados para Campo | [passo-10-dados-liberados.md](./passo-10-dados-liberados.md) |

## Pos-condicoes

- Poligonos (comunidades, quadras, lotes) armazenados no backend
- Poligonos associados ao TENANT correto
- Dados marcados como "liberados" para uso em campo
- Agentes de Campo podem baixar pacote temporario (PARTE 3)

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| RN-06 | Plugin exige Keycloak + AUTHENTICATION KEY |
| RN-07 | Analista so acessa ortofotos do TENANT designado |
| RN-08 | Publicacao e pre-requisito para acesso em campo |
| RN-09 | Dados so ficam disponiveis APOS publicacao |
| RN-10 | Topologia deve ser validada antes de publicar |

## AUTHENTICATION KEY

A AUTHENTICATION KEY e uma chave adicional (estilo "Claude API Key") que:
- Habilita/autoriza o uso do plugin
- Vincula a sessao/ambiente ao backend
- E diferente do login Keycloak (camada extra de seguranca)
- Pode ser revogada independentemente do usuario

## Integracao com Sistemas

| Sistema | Responsabilidade |
|---------|------------------|
| Plugin GEOGIS | Interface de georreferenciamento |
| QGIS | Ambiente de SIG desktop |
| Keycloak | Autenticacao OAuth2/OIDC |
| GEOAPI | Fornece ortofotos, recebe poligonos |

## Proxima Parte

Apos a publicacao, os dados ficam disponiveis para o Agente de Campo na PARTE 3: Operacao em Campo.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (6)

| Documento | Status |
|-----------|--------|
| [Passo 5: Designacao ao TENANT](./passo-05-designacao.md) | ⚠ |
| [Passo 6: Autenticacao no Plugin](./passo-06-autenticacao-plugin.md) | ⚠ |
| [Passo 7: Acesso as Ortofotos do TENANT](./passo-07-acesso-ortofotos.md) | ⚠ |
| [Passo 8: Georreferenciamento](./passo-08-georreferenciamento.md) | ⚠ |
| [Passo 9: Publicacao no Backend](./passo-09-publicacao.md) | ⚠ |
| [Passo 10: Dados Liberados para Campo](./passo-10-dados-liberados.md) | ⚠ |

<!-- CARF-INDEX-END -->
