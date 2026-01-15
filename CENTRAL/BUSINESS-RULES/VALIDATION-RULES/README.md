# VALIDATION-RULES

Regras de validação do CARF garantindo integridade e consistência dos dados antes da persistência. As validações são implementadas em múltiplas camadas: value objects para formato, domain entities para regras de negócio, e banco de dados como última linha de defesa.

As validações de documentos incluem CPF e CNPJ com algoritmo mod 11, RG com formatos específicos por UF, email conforme RFC 5322, e telefone brasileiro com DDD.

As validações geográficas verificam coordenadas dentro dos limites do território brasileiro, polígonos sem auto-interseções via PostGIS ST_IsValid, área dentro dos limites da modalidade REURB, e detecção de sobreposição espacial entre unidades.

As validações de entidades complexas verificam unicidade de CPF por tenant, relacionamentos válidos entre Unit e Holder, transições de status conforme state machine, e consentimento LGPD registrado.

## Regras

- **[cpf-validation.md](./cpf-validation.md)** - CPF com dígitos verificadores mod 11
- **[cnpj-validation.md](./cnpj-validation.md)** - CNPJ com quatorze dígitos
- **[documents-validation.md](./documents-validation.md)** - RG e formatos por UF
- **[email-validation.md](./email-validation.md)** - Email conforme RFC 5322
- **[phone-validation.md](./phone-validation.md)** - Telefone brasileiro com DDD
- **[coordinates-validation.md](./coordinates-validation.md)** - Coordenadas dentro do Brasil
- **[geographic-validation.md](./geographic-validation.md)** - Limites espaciais
- **[geometry-validation.md](./geometry-validation.md)** - Polígonos e topologia PostGIS
- **[holder-validation.md](./holder-validation.md)** - Titular e relacionamentos
- **[unit-validation.md](./unit-validation.md)** - Unidade, código e geometria
- **[business-validation.md](./business-validation.md)** - Regras de negócio complexas

---

**Última atualização:** 2026-01-14
