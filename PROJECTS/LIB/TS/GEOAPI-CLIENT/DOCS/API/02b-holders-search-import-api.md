---
type: leaf
status: review
updated: 2026-02-08
---

# Holders API - Campos, Busca e Importacao

Detalhamento dos campos do CreateHolderDTO conforme [API Reference](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/00-api-reference.md), metodos search e import do modulo api.holders. Campos mapeados 1:1 com a tabela holders do [schema PostgreSQL](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/INFRA/PERSISTENCE/02-database-schema.md).

## Campos do CreateHolderDTO

| Campo | Tipo TS | Obrigatorio | Descricao |
|:------|:--------|:------------|:----------|
| cpf | string | sim | 11 digitos sem formatacao, validado Mod11 |
| fullName | string | sim | Nome completo com minimo 2 palavras |
| socialName | string | nao | Nome social quando diferente do registro |
| birthDate | string | sim | Data ISO 8601 AAAA-MM-DD |
| gender | string | sim | MASCULINO, FEMININO, NAO_DECLARAR ou OUTROS |
| filiation | string | nao | Nomes de filiacao |
| maritalStatus | string | sim | SOLTEIRO, CASADO, DIVORCIADO, VIUVO ou SEPARADO |
| stableUnion | string | nao | NAO, RECONHECIDA_CARTORIO ou NAO_RECONHECIDA |
| spouseName | string | condicional | Obrigatorio se CASADO ou stableUnion diferente de NAO |
| spouseCpf | string | condicional | Obrigatorio se CASADO ou stableUnion diferente de NAO |
| email | string | nao | Email de contato |
| phone | string | nao | Telefone com DDD |
| occupation | string | sim | Situacao profissional |
| profession | string | sim | Profissao conforme CBO simplificada |
| educationLevel | string | nao | Nivel de escolaridade |
| monthlyIncome | number | nao | Renda mensal em reais, relevante para REURB-S vs REURB-E |
| dependentsCount | number | nao | Numero de dependentes |
| nationality | string | nao | Padrao BRASILEIRA |
| documentType | string | sim | RG, CNH, CIN, PASSAPORTE ou CTPS |
| documentNumber | string | sim | Numero do documento de identificacao |

A response retorna HolderDto com todos os campos incluindo id gerado pelo servidor e timestamps.

## search (GET /api/holders/search)

O metodo search aceita query param cpf como string de 11 digitos e retorna Promise de Holder. Busca exata pelo CPF dentro do tenant. Retorna HolderDto completo se encontrado ou NotFoundError 404 se nao existe no tenant. Acessivel por todos os usuarios autenticados. Util para verificar se titular ja existe antes de criar novo registro, evitando erro 409 CPF_EXISTS na criacao.

## import (POST /api/holders/import)

O metodo import aceita arquivo via multipart/form-data com arquivo XLSX ou CSV. Restrito a roles analyst ou superior. O servidor processa linha a linha, validando CPF e campos obrigatorios de cada registro.

Response retorna ImportResult com os seguintes campos:

| Campo | Tipo TS | Descricao |
|:------|:--------|:----------|
| totalProcessed | number | Total de linhas processadas no arquivo |
| totalImported | number | Total importadas com sucesso |
| totalErrors | number | Total com erro de validacao |
| errors | array de ImportError | Detalhes por linha com erro |

Cada ImportError contem row (numero da linha), field (nome do campo com problema) e message (descricao do erro). Erros comuns incluem CPF invalido (falha na validacao Mod11), CPF duplicado (ja existe no tenant), campo obrigatorio faltando e formato de data invalido.
