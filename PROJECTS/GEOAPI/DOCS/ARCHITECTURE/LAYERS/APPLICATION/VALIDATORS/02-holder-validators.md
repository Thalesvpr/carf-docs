---
type: leaf
status: review
updated: 2026-02-08
---

# Holder Validators

Os validators de titulares utilizam FluentValidation para validar requests de criacao e atualizacao de titulares.

## CreateHolderRequestValidator

Valida o request de criacao de titular com as seguintes regras:

| Campo | Regras | Mensagem de Erro |
|-------|--------|-----------------|
| Cpf | Obrigatorio, exatamente 11 digitos, valido via Mod-11 | CPF invalido |
| FullName | Obrigatorio, minimo 2 palavras, maximo 200 caracteres | Nome deve conter ao menos 2 palavras |
| BirthDate | Obrigatorio, data no passado, idade minima 16 anos | Data de nascimento invalida |
| Gender | Obrigatorio, enum MASCULINO, FEMININO, NAO_DECLARAR, OUTROS | Genero invalido |
| MaritalStatus | Obrigatorio, enum SOLTEIRO, CASADO, DIVORCIADO, VIUVO, SEPARADO | Estado civil invalido |
| SpouseName | Obrigatorio quando MaritalStatus CASADO ou StableUnion diferente de NAO | Nome do conjuge obrigatorio |
| SpouseCpf | Obrigatorio quando MaritalStatus CASADO ou StableUnion diferente de NAO, valido via Mod-11 | CPF do conjuge invalido |
| Occupation | Obrigatorio, maximo 100 caracteres | Ocupacao obrigatoria |
| Profession | Obrigatorio, maximo 100 caracteres | Profissao obrigatoria |
| DocumentType | Obrigatorio, enum RG, CNH, CIN, PASSAPORTE, CTPS | Tipo de documento invalido |
| DocumentNumber | Obrigatorio, maximo 30 caracteres | Numero do documento obrigatorio |
| Email | Opcional, formato email valido quando presente | Email invalido |
| Phone | Opcional, maximo 20 caracteres quando presente | Telefone invalido |

## CpfValidator

Validator customizado reutilizavel que implementa o algoritmo Mod-11 para validacao dos dois digitos verificadores do CPF. Rejeita sequencias repetidas (111.111.111-11) e valida calculo dos digitos conforme formula oficial da Receita Federal.

## UpdateHolderRequestValidator

Valida o request de atualizacao parcial. Todos os campos sao opcionais. Quando presentes, delegam validacao aos respectivos validators. FullName quando presente deve ter minimo 2 palavras. Email quando presente deve ter formato valido.
