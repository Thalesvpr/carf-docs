# VALIDATION-RULES

Regras de validação do CARF garantindo integridade e consistência dos dados antes da persistência. As validações são implementadas em múltiplas camadas: value objects para formato, domain entities para regras de negócio, e banco de dados como última linha de defesa.

As validações de documentos incluem CPF e CNPJ com algoritmo mod 11, RG com formatos específicos por UF, email conforme RFC 5322, e telefone brasileiro com DDD.

As validações geográficas verificam coordenadas dentro dos limites do território brasileiro, polígonos sem auto-interseções via PostGIS ST_IsValid, área dentro dos limites da modalidade REURB, e detecção de sobreposição espacial entre unidades.

As validações de entidades complexas verificam unicidade de CPF por tenant, relacionamentos válidos entre Unit e Holder, transições de status conforme state machine, e consentimento LGPD registrado.

## Regras

- **[cpf-validation.md](./04-cpf-validation.md)** - CPF com dígitos verificadores mod 11
- **[cnpj-validation.md](./02-cnpj-validation.md)** - CNPJ com quatorze dígitos
- **[documents-validation.md](./05-documents-validation.md)** - RG e formatos por UF
- **[email-validation.md](./06-email-validation.md)** - Email conforme RFC 5322
- **[phone-validation.md](./10-phone-validation.md)** - Telefone brasileiro com DDD
- **[coordinates-validation.md](./03-coordinates-validation.md)** - Coordenadas dentro do Brasil
- **[geographic-validation.md](./07-geographic-validation.md)** - Limites espaciais
- **[geometry-validation.md](./08-geometry-validation.md)** - Polígonos e topologia PostGIS
- **[holder-validation.md](./09-holder-validation.md)** - Titular e relacionamentos
- **[unit-validation.md](./11-unit-validation.md)** - Unidade, código e geometria
- **[business-validation.md](./01-business-validation.md)** - Regras de negócio complexas

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição:  O ramo completo ta sem numeração.

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (11 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-business-validation](./01-business-validation.md) | BUSINESS |
| [02-cnpj-validation](./02-cnpj-validation.md) | CNPJ Validation |
| [03-coordinates-validation](./03-coordinates-validation.md) | Coordinates Validation |
| [04-cpf-validation](./04-cpf-validation.md) | CPF Validation |
| [05-documents-validation](./05-documents-validation.md) | DOCUMENTS |
| [06-email-validation](./06-email-validation.md) | Email Validation |
| [07-geographic-validation](./07-geographic-validation.md) | GEOGRAPHIC |
| [08-geometry-validation](./08-geometry-validation.md) | Geometry Validation |
| [09-holder-validation](./09-holder-validation.md) | Holder Validation Rules |
| [10-phone-validation](./10-phone-validation.md) | Phone Validation |
| [11-unit-validation](./11-unit-validation.md) | Unit Validation Rules |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
