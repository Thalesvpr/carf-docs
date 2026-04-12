---
type: leaf
status: review
updated: 2026-02-08
---

# Holder DTOs

Os Data Transfer Objects de titulares definem os contratos de entrada e saida da API para operacoes sobre a entidade Holder. Todos sao implementados como records imutaveis.

## DTOs de Resposta

HolderDto e o DTO completo retornado em operacoes de leitura individual.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Id | Guid | Identificador unico |
| Cpf | string | CPF mascarado (***.XXX.XXX-**) |
| FullName | string | Nome completo |
| SocialName | string | Nome social (nullable) |
| BirthDate | DateTime | Data de nascimento |
| Age | int | Idade calculada |
| Gender | string | Genero |
| MaritalStatus | string | Estado civil |
| StableUnion | string | Uniao estavel (nullable) |
| SpouseName | string | Nome do conjuge (nullable) |
| Email | string | Email (nullable) |
| Phone | string | Telefone (nullable) |
| Occupation | string | Ocupacao |
| Profession | string | Profissao |
| DocumentType | string | Tipo do documento |
| DocumentNumber | string | Numero do documento |
| UnitsCount | int | Quantidade de unidades vinculadas |
| CreatedAt | DateTime | Data de criacao |
| UpdatedAt | DateTime | Ultima atualizacao |

HolderListItemDto e o DTO reduzido para listagens contendo Id, Cpf mascarado, FullName, BirthDate, Gender e UnitsCount.

HolderSummaryDto e o DTO minimo usado em contextos de vinculacao com unidades, contendo Id, Cpf mascarado e FullName.

## DTOs de Request

CreateHolderRequest contem cpf (string 11 digitos obrigatorio), fullName (obrigatorio), socialName (opcional), birthDate (obrigatorio), gender (obrigatorio), filiation (opcional), maritalStatus (obrigatorio), stableUnion (opcional), spouseName (condicional), spouseCpf (condicional), email (opcional), phone (opcional), occupation (obrigatorio), profession (obrigatorio), documentType (obrigatorio) e documentNumber (obrigatorio).

UpdateHolderRequest contem fullName, socialName, email, phone, occupation e profession, todos opcionais para atualizacao parcial. CPF nao pode ser alterado.

ImportHoldersRequest contem file (IFormFile obrigatorio, XLSX ou CSV).
