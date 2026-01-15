# HOW-TO - GEOGIS

Guias práticos para desenvolver e usar o plugin GEOGIS QGIS.

## Setup e Instalação

- **[01-setup-keycloak.md](./01-setup-keycloak.md)** - Configurar Keycloak realm, client_id, redirect_uri para plugin QGIS
- Instalação do plugin copiando pasta para `~/.qgis3/python/plugins/carf-geogis/` ou via ZIP no QGIS Plugin Manager

## Autenticação

- **[02-login-flow.md](./02-login-flow.md)** - OAuth2 login flow: browser OAuth → authorization code → callback local HTTP server → exchange code + PKCE → store tokens encrypted
- Configuração inicial: abrir Settings dialog, definir GEOAPI base URL e Keycloak realm/client_id

## Uso da API

- **[03-api-requests.md](./03-api-requests.md)** - Load Layers, listar comunidades via GET /api/communities, download geometries GeoJSON, adicionar ao map canvas

## Análises Espaciais

**Processing Toolbox algorithms:**
- Buffer - criar área influência
- Intersect - identificar overlaps
- Validate Geometry - detectar polígonos inválidos

## Exportação

**Export features:**
- Selecionar features desejadas
- Clicar Export button
- Escolher formato (Shapefile ou GeoJSON)
- Definir output path
- Preservar attributes e CRS

## Sincronização de Edições

**Sync workflow:**
1. Modificar geometries no QGIS via editing tools
2. Clicar Sync Changes button
3. Detectar features modified comparando com server version
4. Resolver conflicts via merge strategy
5. Upload changes via PATCH /api/units/:id endpoint
6. Validar server-side

## Troubleshooting

**Erros comuns:**
- "Plugin failed to load" → verificar metadata.txt e `pip install -r requirements.txt` no QGIS Python environment
- "Authentication failed" → verificar Keycloak acessível e client_id/redirect_uri corretos
- "Layer loading failed" → verificar connectivity GEOAPI e WFS endpoint habilitado
- "Export failed" → verificar permissions write em output directory e CRS transformation suportada pelo GDAL

---

**Última atualização:** 2026-01-10

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (3 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-setup-keycloak](./01-setup-keycloak.md) | 01-setup-keycloak |
| [02-login-flow](./02-login-flow.md) | 02-login-flow |
| [03-api-requests](./03-api-requests.md) | 03-api-requests |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Incompleto
Descrição: Falta parágrafo denso introdutório; Muitas listas com bullets (17) antes do rodapé - considerar converter para parágrafo denso.
