---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-116: Armazenamento em S3/MinIO

## Descricao

Sistema deve armazenar arquivos em object storage compativel S3 (Amazon S3, MinIO ou equivalente) ao inves de filesystem local, garantindo escalabilidade e durabilidade. Integracao via SDK com credenciais e endpoint configuraveis. Downloads seguros via URLs presigned temporarias com expiracao configuravel. Arquivos organizados hierarquicamente por tenant e entidade usando prefixos (tenant-id/entity-type/entity-id/filename). Camada de abstracao permite trocar provider sem alterar logica. Conforme WORKFLOW-MESTRE, bucket segregado por tenant.

## Criterios de Aceitacao

1. Integracao com S3-compatible storage
2. URLs presigned temporarias para download
3. Organizacao por tenant e entidade
4. Configuracao de credenciais e endpoint
5. Camada de abstracao de storage

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-102, RF-108, RF-017
