---
id: UC-P1-002
type: UC
modules: []
status: review
created: 2026-01-24
updated: 2026-01-24
workflow: PARTE-1
---

# UC-P1-002: Processar Ortofoto

Backend recebe e processa ortofoto, gerando versoes otimizadas.

## Referencia

Este UC implementa passo 3 do [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/01-entrega-ortofotos.md).

## Atores

- Primario: Backend GEOAPI (automatico)
- Secundario: Bucket S3/MinIO

## Pre-condicoes

- Ortofoto recebida (UC-P1-001 concluido)
- Servico de processamento operacional
- Bucket com espaco disponivel

## Fluxo Principal

1. Backend recebe notificacao de nova ortofoto
2. Backend extrai metadados (EXIF, coordenadas, data captura)
3. Backend valida georreferenciamento
4. Backend gera versao otimizada para web (JPEG/WebP comprimido)
5. Backend gera tiles para consumo eficiente (piramide de resolucoes)
6. Backend mantem versao original para analise detalhada
7. Backend registra metadados no banco de dados
8. Backend notifica conclusao do processamento
9. Sistema aciona armazenamento (UC-P1-003)

## Fluxos de Excecao

- FE-001: Ortofoto sem georreferenciamento valido
- FE-002: Falha na geracao de tiles
- FE-003: Espaco insuficiente no bucket
- FE-004: Timeout no processamento

## Pos-condicoes

- Versao original preservada
- Versao otimizada gerada
- Tiles gerados
- Metadados registrados no banco

## Regras de Negocio

| Regra | Descricao |
|-------|-----------|
| RN-01 | Backend SEMPRE reduz tamanho da ortofoto |
| RN-02 | Versao original DEVE ser preservada |
| RN-03 | Tiles DEVEM seguir padrao de piramide |
