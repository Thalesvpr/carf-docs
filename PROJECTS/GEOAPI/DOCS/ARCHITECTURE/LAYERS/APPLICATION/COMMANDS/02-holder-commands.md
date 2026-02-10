---
type: leaf
status: review
updated: 2026-02-08
---

# Holder Commands

Os commands de titulares representam operacoes de escrita sobre a entidade Holder. Cada command e um record imutavel implementando IRequest do MediatR. Os handlers coordenam validacao de CPF, unicidade por tenant e persistencia via repositorio.

---

## CreateHolderCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| Cpf | string | sim | CPF de 11 digitos sem formatacao |
| FullName | string | sim | Nome completo com minimo 2 palavras |
| SocialName | string | nao | Nome social quando diferente |
| BirthDate | DateTime | sim | Data de nascimento ISO 8601 |
| Gender | string | sim | MASCULINO, FEMININO, NAO_DECLARAR, OUTROS |
| Filiation | string | nao | Nomes de filiacao |
| MaritalStatus | string | sim | SOLTEIRO, CASADO, DIVORCIADO, VIUVO, SEPARADO |
| StableUnion | string | nao | NAO, RECONHECIDA_CARTORIO, NAO_RECONHECIDA |
| SpouseName | string | condicional | Obrigatorio se casado ou uniao estavel |
| SpouseCpf | string | condicional | Obrigatorio se casado ou uniao estavel |
| Email | string | nao | Email de contato |
| Phone | string | nao | Telefone com DDD |
| Occupation | string | sim | Situacao profissional |
| Profession | string | sim | Profissao conforme CBO |
| DocumentType | string | sim | RG, CNH, CIN, PASSAPORTE, CTPS |
| DocumentNumber | string | sim | Numero do documento |

O handler primeiro valida o CPF via algoritmo Mod-11 verificando os dois digitos verificadores. Segundo, consulta o repositorio para verificar unicidade do CPF no tenant atual usando constraint UNIQUE em (tenant_id, cpf). Terceiro, cria a entidade Holder via construtor validando invariantes de dominio. Quarto, persiste via repositorio e retorna HolderDto.

Emite HolderCreatedEvent com Id e TenantId. Erros possiveis: CPF_INVALID para digitos invalidos, CPF_EXISTS para CPF ja cadastrado no tenant.

---

## UpdateHolderCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| Id | Guid | sim | Identificador do titular |
| FullName | string | nao | Nome completo atualizado |
| SocialName | string | nao | Nome social |
| Email | string | nao | Email atualizado |
| Phone | string | nao | Telefone atualizado |

O handler carrega o titular pelo Id, aplica atualizacoes parciais nos campos fornecidos e incrementa version para controle de concorrencia otimista. O CPF nao pode ser alterado apos criacao.

---

## DeleteHolderCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| HolderId | Guid | sim | Identificador do titular |

O handler verifica se existem registros em unit_holders vinculados ao titular. Se existirem vinculos ativos, retorna erro HAS_UNITS impedindo a exclusao. Caso contrario, executa soft delete preenchendo deleted_at.

---

## ImportHoldersCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| File | IFormFile | sim | Arquivo XLSX ou CSV |

O handler processa o arquivo linha a linha, validando CPF e campos obrigatorios de cada registro. Linhas validas sao persistidas, linhas invalidas sao registradas com detalhes do erro. O response retorna total processado, total importado, total com erro e array de erros detalhados com numero da linha, campo e mensagem.
