---
type: leaf
status: approved
updated: 2026-02-07
---

# Authentication Key

Chave de API de longa duracao projetada para autenticar o plugin QGIS (GEOGIS) na GEOAPI sem exigir que o analista mantenha uma sessao interativa OAuth2 aberta durante todo o trabalho de georreferenciamento. A chave e um UUID v4 gerado pelo servidor, vinculado a sessao Keycloak do analista no momento da criacao, e transmitido no header X-Auth-Key em cada requisicao do plugin.

## Ciclo de Vida

O analista primeiro autentica-se normalmente via Keycloak no REURBWEB ou ADMIN. Com o Bearer token JWT valido, faz POST para /api/auth-keys informando um nome descritivo para a chave (por exemplo "QGIS Desktop - Notebook Joao"). O servidor gera um UUID v4 aleatorio, calcula o hash SHA-256 desse UUID e armazena apenas o hash na tabela api_keys junto com o account_id, tenant_id, nome descritivo e data de expiracao de 30 dias a partir da criacao. O UUID original e retornado na response uma unica vez. O servidor nunca armazena nem consegue recuperar a chave original apos essa resposta.

O analista copia a chave para a configuracao do plugin QGIS. A partir desse momento, toda requisicao do plugin envia a chave no header X-Auth-Key. O middleware de autenticacao da GEOAPI calcula o SHA-256 do valor recebido e busca o hash correspondente na tabela api_keys. Se encontrar um registro ativo (nao revogado, nao expirado), extrai o account_id e tenant_id para montar o contexto de seguranca da requisicao. A chave herda todas as permissoes do account vinculado, incluindo as restricoes de tenant e community_authorization.

## Renovacao e Revogacao

A chave expira automaticamente apos 30 dias. O analista pode gerar uma nova chave a qualquer momento sem revogar a anterior, permitindo transicao suave entre chaves. Revogacao explicita via DELETE /api/auth-keys/{id} marca o campo revoked_at com o timestamp atual, invalidando a chave imediatamente. Troca de senha no Keycloak tambem revoga automaticamente todas as chaves ativas do account, forcando o analista a gerar novas chaves.

## Rate Limiting

Cada chave tem limite de 100 requisicoes por minuto, rastreado via Redis com janela deslizante. Requisicoes excedentes recebem HTTP 429 com header Retry-After indicando segundos ate a proxima janela. O campo last_used_at e atualizado a cada requisicao bem-sucedida para monitoramento de uso.

## Dados Armazenados

A tabela api_keys contem: id como uuid chave primaria, account_id como uuid referenciando o usuario Keycloak que criou a chave, tenant_id como uuid do municipio vinculado, key_hash como varchar 64 contendo o SHA-256 hexadecimal da chave original, name como varchar 200 com descricao fornecida pelo usuario, expires_at como timestamp com timezone, last_used_at como timestamp nullable atualizado a cada uso, created_at como timestamp de criacao e revoked_at como timestamp nullable preenchido na revogacao. Indice unico em key_hash para busca rapida durante autenticacao. Indice em account_id para listar chaves do usuario.

## Seguranca

A chave nunca trafega em logs do servidor pois o middleware registra apenas o prefixo dos primeiros 8 caracteres para identificacao em auditoria. O hash SHA-256 e irreversivel, portanto mesmo com acesso ao banco de dados nao e possivel recuperar a chave original. A listagem de chaves via GET /api/auth-keys retorna apenas id, name, created_at, expires_at e last_used_at, nunca o hash ou a chave.
