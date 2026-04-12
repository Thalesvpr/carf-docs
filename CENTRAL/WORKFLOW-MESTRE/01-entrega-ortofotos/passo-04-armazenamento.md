---
type: workflow
status: approved
updated: 2026-02-21
part: 1
step: 4
---

# Passo 4: Armazenamento em Bucket por TENANT

Armazenamento das ortofotos processadas no bucket, segregadas por TENANT.

## Fluxo

1. Backend determina TENANT do Operador de Drone (via token JWT)
2. Backend cria estrutura de pastas no bucket no caminho /{tenant_id}/ortofotos/{ano}/{mes}/
3. Backend salva arquivos nas subpastas original (ortofoto original) e otimizada (versao reduzida)
4. Backend registra URLs no banco de dados
5. Backend associa ortofoto ao TENANT correspondente

## Estrutura no Bucket

| Nivel | Caminho | Conteudo |
|-------|---------|----------|
| Raiz | /{tenant_id}/ | Namespace do tenant |
| Ortofotos | /ortofotos/{ano}/{mes}/ | Organizacao temporal |
| Original | /original/ortofoto_{id}.tif | Arquivo original GeoTIFF |
| Otimizada | /otimizada/ortofoto_{id}.webp | Versao reduzida WebP |

## Segregacao por TENANT

- Cada TENANT possui seu proprio namespace no bucket
- Nao ha acesso cruzado entre TENANTs
- URLs sao geradas com presigned tokens para seguranca

## Resultado

- Ortofoto armazenada no bucket
- Estrutura de pastas criada
- URLs registradas no banco
- **Ortofoto disponivel para PARTE 2** (Analista Plugin QGIS)

## Proxima Parte

PARTE 2: Georreferenciamento e Publicacao
