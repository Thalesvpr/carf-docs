---
type: workflow
status: approved
updated: 2026-01-25
part: 1
step: 2
---

# Passo 2: Upload da Ortofoto

Envio do arquivo de ortofoto para o backend.

## Fluxo

1. Analista de Drone seleciona arquivo de ortofoto
2. Sistema valida formato (GeoTIFF, JPEG2000, etc.)
3. Sistema valida tamanho maximo permitido
4. Sistema inicia upload multipart (para arquivos grandes)
5. Progresso e exibido ao usuario
6. Upload concluido com sucesso

## Formatos Aceitos

| Formato | Extensao | Descricao |
|---------|----------|-----------|
| GeoTIFF | .tif, .tiff | Formato padrao para ortofotos |
| JPEG2000 | .jp2 | Compressao eficiente |

## Upload Multipart

Para arquivos grandes (> 100MB), o sistema utiliza upload multipart:
- Arquivo dividido em partes menores
- Cada parte enviada separadamente
- Resumo automatico em caso de falha
- Progresso exibido em tempo real

## Resultado

- Arquivo de ortofoto recebido pelo backend
- Validacoes basicas concluidas
- Pronto para processamento

## Proximo Passo

Passo 3: Processamento pelo Backend
