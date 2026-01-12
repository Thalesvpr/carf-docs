# VALIDATORS

FluentValidation validators do GEOAPI validando commands e DTOs antes de execução garantindo que apenas dados válidos cheguem à camada de domínio. Validators implementam AbstractValidator<T> definindo regras declarativas via métodos RuleFor, validando formato, tamanho, obrigatoriedade e regras simples delegando lógica complexa de negócio para entidades de domínio. Integrados ao pipeline do MediatR via behavior que intercepta commands/queries executando validação automática antes do handler retornando ValidationException com lista de erros quando falha impedindo execução. Validators podem chamar serviços externos para validações assíncronas (verificar CPF duplicado via repository, validar CEP em API externa) e compor validators reutilizáveis para propriedades comuns (AddressValidator, CpfValidator). Mensagens de erro customizadas em português para cada regra facilitando feedback ao usuário final e testes unitários validam comportamento de cada validator isoladamente sem depender de infraestrutura.

## Arquivos Principais (a criar)

**Commands Validators:**
- 01-create-unit-command-validator.md
- 02-update-unit-command-validator.md
- 03-create-holder-command-validator.md
- 04-update-holder-command-validator.md
- 05-create-community-command-validator.md
- 06-create-legitimation-request-command-validator.md

**DTOs Validators:**
- 07-create-unit-dto-validator.md
- 08-address-dto-validator.md
- 09-cpf-validator.md (reutilizável)
- 10-email-validator.md (reutilizável)
- 11-phone-number-validator.md (reutilizável)

---

**Última atualização:** 2026-01-12
