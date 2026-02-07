---
type: workflow
status: approved
updated: 2026-02-07
part: 3
step: 12
---

# Passo 12: Download do Pacote Temporario

Coordenador de Campo ou Cadastrador de Campo baixa o pacote de dados para operacao em campo.

## Atores

- **Coordenador de Campo**: baixa pacote e seleciona regiao
- **Cadastrador de Campo**: baixa pacote da regiao atribuida

## Fluxo

1. Usuario de campo abre o app REURBCAD
2. App autentica via Keycloak
3. App consulta backend: `GET /api/pacotes/campo?tenant_id={tenant}`
4. Backend verifica:
   - Usuario pertence ao TENANT
   - Analista JA PUBLICOU trabalho do TENANT
5. **SOMENTE SE PUBLICADO:** Backend disponibiliza pacote contendo:
   - Ortofoto (versao para uso offline)
   - Poligonos georreferenciados (comunidades/quadras/lotes)
   - Metadados necessarios
6. Download e UNICO e TEMPORARIO (link expira)
7. App armazena pacote localmente (WatermelonDB)

## API Request

```http
GET /api/pacotes/campo?tenant_id={tenant}
Authorization: Bearer {jwt_token}
```

## Response

```json
{
  "pacote_id": "uuid",
  "tenant_id": "uuid",
  "download_url": "https://presigned-url...",
  "expires_at": "2026-01-25T23:59:59Z",
  "conteudo": {
    "ortofoto": { "url": "...", "bbox": [...] },
    "comunidades": [...],
    "quadras": [...],
    "lotes": [...]
  }
}
```

## Regra Critica

**PUB-02:** Usuario de campo SO consegue baixar dados QUANDO Analista JA PUBLICOU.

Se o Analista ainda nao publicou, o backend retorna erro 404.

## Caracteristicas do Pacote

| Caracteristica | Descricao |
|----------------|-----------|
| Link expiravel | URL presigned com tempo limite |
| Download unico | Apenas um download por link |
| Armazenamento local | Salvo em WatermelonDB |
| Operacao offline | Permite trabalho sem conexao |

## Comportamento por Role

| Role | Apos Download |
|------|---------------|
| Coordenador | Ve Bottom Navigation, seleciona comunidade |
| Cadastrador | Vai direto pro mapa da regiao atribuida |

## Resultado

- Pacote baixado para o dispositivo
- Dados armazenados localmente
- App pronto para operacao offline

## Proximo Passo

Passo 13: Selecao de Comunidade
