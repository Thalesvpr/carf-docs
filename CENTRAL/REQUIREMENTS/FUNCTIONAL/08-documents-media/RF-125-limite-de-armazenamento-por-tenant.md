---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-125: Limite de Armazenamento por Tenant

## Descricao

Sistema deve implementar quota configuravel de armazenamento por tenant para controle de recursos e governanca, conforme WORKFLOW-MESTRE onde bucket S3/MinIO e segregado por tenant. Modelo de dados de tenants inclui campo storage_quota armazenando limite em bytes configuravel individualmente conforme plano ou politica interna. Sistema calcula uso atual de storage por tenant somando tamanho de todos arquivos, documentos e fotos associados, via calculo em tempo real durante uploads ou job batch periodico. Quando tenant atinge ou excede limite, sistema bloqueia novos uploads retornando erro claro informando quota excedida, orientando usuario a contatar administrador ou liberar espaco. Sistema expoe metrica de uso atual versus quota via endpoint da API e painel administrativo.

## Criterios de Aceitacao

1. Campo storage_quota configuravel por tenant
2. Calculo de uso atual de storage
3. Bloqueio de uploads ao atingir limite
4. Mensagem clara sobre quota excedida
5. Metrica de uso via API e painel

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-017, RF-102, RF-108, RF-116
