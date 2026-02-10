---
type: leaf
status: review
updated: 2026-02-08
---

# ApiKeyValue

Value object imutavel representando uma chave de API para integracao sistema-a-sistema. Gerada automaticamente pelo servidor como token opaco de 64 caracteres hexadecimais, armazenada como hash SHA-256 no banco para seguranca.

## Regras de Validacao

| Regra | Descricao |
|-------|-----------|
| Formato | 64 caracteres hexadecimais (256 bits). |
| Unicidade | Deve ser unica globalmente. Verificada contra hash no banco. |
| Imutabilidade | Uma vez gerada, nao pode ser alterada. Rotacao exige gerar nova chave. |
| Armazenamento seguro | Apenas hash SHA-256 persiste no banco. Valor original exibido uma unica vez ao gerar. |

## Uso no Dominio

ApiKeyValue autentica integracoes externas como QGIS plugin (GEOGIS) que acessa ortofotos e layers via GEOAPI sem JWT de usuario. A chave e enviada no header X-API-Key e validada comparando hash. Criacao requer role ADMIN.
