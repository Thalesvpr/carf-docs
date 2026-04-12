---
type: leaf
status: approved
updated: 2026-02-21
---

# Bucket por Tenant

Armazenamento de objetos (S3/MinIO) organizado com segregacao completa por tenant. Cada tenant tem estrutura de pastas isolada para seus arquivos pesados.

Arquitetura multi-tenant exige que arquivos de um cliente nunca sejam acessiveis por outro. Bucket usa prefixo de tenant em todos os paths garantindo isolamento logico.

## Estrutura de Pastas

| Caminho | Conteudo |
|---------|----------|
| /{tenant_id}/ortofotos/{ano}/{mes}/original/ | Ortofoto original |
| /{tenant_id}/ortofotos/{ano}/{mes}/otimizada/ | Versao reduzida |
| /{tenant_id}/documentos/ | Documentos anexados |
| /{tenant_id}/fotos/ | Fotos de campo |

## Tipos de Arquivos

Bucket armazena arquivos que nao cabem em banco de dados relacional:
- Ortofotos (GeoTIFF, JPEG2000) - varios gigabytes
- Documentos anexados (PDF, imagens) - megabytes
- Fotos de campo - megabytes

## Acesso

URLs presigned sao geradas pelo backend para acesso temporario. Plugin QGIS e App mobile nunca acessam bucket diretamente - sempre via backend que valida permissoes e tenant.

## Seguranca

- Credenciais de acesso ao bucket nunca expostas a clientes
- Backend valida tenant do usuario antes de gerar URL
- URLs presigned expiram apos periodo curto (minutos/horas)
- Logs de acesso mantidos para auditoria

## Referencia

Ver [WORKFLOW-MESTRE](../../WORKFLOW-MESTRE/README.md) para fluxo de armazenamento e acesso a arquivos.
