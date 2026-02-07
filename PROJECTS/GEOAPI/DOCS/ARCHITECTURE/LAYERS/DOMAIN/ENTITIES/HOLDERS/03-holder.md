---
type: leaf
status: approved
updated: 2026-02-07
---

# Holder

Entidade representando titular ou posseiro pessoa fisica vinculado a uma ou mais unidades habitacionais. Armazena dados pessoais, documentais e socioeconomicos completos necessarios para o processo de regularizacao fundiaria conforme Lei 13.465/2017. Herda de BaseEntity fornecendo auditoria e soft delete.

## Papel no Dominio

O titular e a pessoa que reivindica direito sobre uma unidade habitacional. Seus dados pessoais e socioeconomicos determinam a modalidade de REURB aplicavel (REURB-S para interesse social ou REURB-E para interesse especifico, conforme faixa de renda) e sao obrigatorios para emissao de certidoes de legitimacao fundiaria. O CPF e o identificador natural do titular dentro de cada tenant, aplicando a regra CPF-primeiro: no app mobile, o CPF e o primeiro campo do formulario e bloqueia o preenchimento dos demais ate ser validado.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| TenantId | Guid | nao | Municipio. FK para Tenant. |
| Cpf | string | nao | CPF com 11 digitos sem formatacao. Validado via algoritmo Mod11. |
| Cnpj | string | sim | CNPJ com 14 digitos para pessoa juridica. |
| FullName | string | nao | Nome completo com minimo de 2 palavras. |
| SocialName | string | sim | Nome social quando diferente do registro civil. |
| BirthDate | DateOnly | nao | Data de nascimento. |
| Gender | string | nao | MASCULINO, FEMININO, NAO_DECLARAR, OUTROS. |
| Filiation | string | sim | Campo unico opcional contendo 1 ou 2 nomes de filiacao. |
| MaritalStatus | string | nao | SOLTEIRO, CASADO, DIVORCIADO, VIUVO, SEPARADO. |
| StableUnion | string | sim | NAO, RECONHECIDA_CARTORIO, NAO_RECONHECIDA. |
| SpouseName | string | sim | Nome do conjuge. Obrigatorio se casado ou uniao estavel. |
| SpouseCpf | string | sim | CPF do conjuge. Obrigatorio se casado ou uniao estavel. |
| Email | string | sim | Email de contato. |
| Phone | string | sim | Telefone com DDD. |
| Occupation | string | nao | Situacao profissional: empregado formal, autonomo, aposentado, etc. |
| Profession | string | nao | Profissao conforme CBO simplificada. |
| EducationLevel | string | sim | Nivel de escolaridade. |
| MonthlyIncome | decimal | sim | Renda mensal declarada em reais. |
| DependentsCount | int | sim | Numero de dependentes. |
| Nationality | string | nao | Nacionalidade. Default BRASILEIRA. |
| DocumentType | string | nao | RG, CNH, CIN, PASSAPORTE, CTPS. |
| DocumentNumber | string | nao | Numero do documento de identificacao. |
| SignaturePath | string | sim | Caminho S3 do PNG da assinatura criptografado AES-256. |
| SignatureTimestamp | DateTime | sim | Momento exato da captura da assinatura. |
| SignatureDeviceId | string | sim | Identificador do dispositivo usado. |
| CreatedAt | DateTime | nao | Data de criacao. |
| UpdatedAt | DateTime | nao | Ultima atualizacao. |
| CreatedBy | Guid | nao | Quem cadastrou. |
| UpdatedBy | Guid | nao | Quem atualizou por ultimo. |
| DeletedAt | DateTime | sim | Soft delete. |

## Relacionamentos

Relacionamento N:N com Unit via UnitHolder, permitindo que um titular esteja vinculado a multiplas unidades e que uma unidade tenha multiplos titulares. O tipo de vinculo e o percentual de propriedade sao definidos na entidade de juncao UnitHolder.

Colecao de Documents vinculados via entity_type HOLDER contendo copias digitais de RG, CPF, CNH, comprovante de residencia e outros documentos.

## Invariantes de Negocio

CPF deve ser unico por tenant. Tentativa de criar titular com CPF ja existente retorna erro CPF_EXISTS com HTTP 409.

CPF deve ser valido conforme algoritmo Mod11 de verificacao dos dois digitos verificadores. CPF invalido retorna erro CPF_INVALID com HTTP 400.

Quando marital_status e CASADO ou stable_union e diferente de NAO, os campos spouse_name e spouse_cpf tornam-se obrigatorios. Submissao sem esses campos gera erro VALIDATION_ERROR.

Full_name deve conter ao menos 2 palavras separadas por espaco.

Titular so pode ser excluido se nao estiver vinculado a nenhuma unidade ativa (nao soft-deleted). Tentativa de excluir titular com unidades vinculadas retorna erro HAS_UNITS.

## Domain Events

HolderCreatedEvent emitido ao criar titular. HolderUpdatedEvent emitido ao atualizar dados. Nao emite eventos proprios de vinculacao pois esses sao responsabilidade da entidade Unit (HolderLinkedEvent, HolderUnlinkedEvent).
