---
type: leaf
status: review
updated: 2026-02-08
---

# Holder Management Feature

A feature de gerenciamento de titulares permite cadastrar, consultar, editar e excluir pessoas fisicas e juridicas que ocupam ou possuem unidades habitacionais no processo de regularizacao fundiaria. Abrange validacao de CPF via algoritmo Mod-11, busca por CPF, importacao em lote via planilha XLSX ou CSV e vinculacao com unidades.

## User Stories

US-010 Cadastrar Titular: o cadastrista informa CPF, nome completo, data de nascimento, genero, estado civil e dados de documentacao. O sistema valida o CPF via Mod-11, verifica unicidade por tenant e persiste o registro retornando HolderDto com id gerado.

US-011 Buscar por CPF: o cadastrista informa um CPF de 11 digitos e o sistema retorna o titular correspondente no tenant atual ou 404 se nao encontrado, permitindo reutilizar cadastros existentes ao vincular titulares a novas unidades.

US-012 Importar Titulares em Lote: o analista faz upload de arquivo XLSX ou CSV com dados de multiplos titulares. O servidor processa linha a linha, valida CPF e campos obrigatorios de cada registro e retorna relatorio com total processado, importados com sucesso e erros detalhados por linha.

US-013 Excluir Titular: o cadastrista solicita exclusao de um titular. O sistema verifica se existem vinculos ativos em unit_holders e recusa a exclusao com erro HAS_UNITS quando o titular possui unidades vinculadas.

## Endpoints

| Metodo | Rota | Descricao |
|--------|------|-----------|
| POST | /api/holders | Criar titular |
| GET | /api/holders/{id} | Obter titular |
| GET | /api/holders | Listar com paginacao |
| PATCH | /api/holders/{id} | Atualizar titular |
| DELETE | /api/holders/{id} | Excluir titular |
| GET | /api/holders/search?cpf= | Buscar por CPF |
| POST | /api/holders/import | Importar planilha |

## Regras de Negocio

RN-010: CPF deve ser valido conforme algoritmo Mod-11 com verificacao dos dois digitos verificadores. RN-011: CPF deve ser unico por tenant, constraint UNIQUE em (tenant_id, cpf). RN-012: nome completo deve conter no minimo 2 palavras. RN-013: dados do conjuge (spouse_name e spouse_cpf) sao obrigatorios quando marital_status e CASADO ou stable_union diferente de NAO. RN-014: titular com vinculos ativos em unit_holders nao pode ser excluido, retornando erro HAS_UNITS. RN-015: importacao em lote processa todas as linhas mesmo com erros individuais, retornando relatorio completo ao final.

## Permissoes

| Acao | field-cadastrator | field-coordinator | analyst | manager | admin | super-admin |
|------|-------------------|-------------------|---------|---------|-------|-------------|
| Criar | sim | sim | sim | sim | sim | sim |
| Editar | sim | sim | sim | sim | sim | sim |
| Visualizar | sim | sim | sim | sim | sim | sim |
| Excluir | sim | sim | sim | sim | sim | sim |
| Buscar CPF | sim | sim | sim | sim | sim | sim |
| Importar | nao | nao | sim | sim | sim | sim |
