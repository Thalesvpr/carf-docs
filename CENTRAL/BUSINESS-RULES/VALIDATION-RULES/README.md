# VALIDATION-RULES

Regras de validação do CARF organizadas por categoria. DOCUMENTS contém validações de documentos (CPF dígito verificador algoritmo mod 11, CNPJ validação, RG formato por estado). GEOGRAPHIC contém validações geográficas (coordenadas dentro bounds Brasil -33.75/-73.98 a 5.27/-34.79, polígono sem auto-interseção via validação topológica, área mínima 20m² máxima 250m² para REURB-S, detecção de sobreposição espacial entre unidades). BUSINESS contém validações de negócio (titular maior 18 anos, email formato RFC 5322, telefone formato brasileiro DDD + número). Validações implementadas em múltiplas camadas: value objects (formato), domain entities (regras de negócio), validadores estruturais na camada de aplicação (composição), restrições de banco de dados (última linha de defesa).

## Regras Documentadas

### Validações de Documentos
- **[cpf-validation.md](./cpf-validation.md)** - Validação de CPF (dígitos verificadores, algoritmo mod 11)
- **[cnpj-validation.md](./cnpj-validation.md)** - Validação de CNPJ (formato, dígitos verificadores)
- **[documents-validation.md](./documents-validation.md)** - Validações gerais de documentos (RG por estado)

### Validações Geográficas
- **[coordinates-validation.md](./coordinates-validation.md)** - Validação de coordenadas (bounds Brasil -33.75/-73.98 a 5.27/-34.79)
- **[geometry-validation.md](./geometry-validation.md)** - Validação de geometrias (polígonos sem auto-interseção, topologia)
- **[geographic-validation.md](./geographic-validation.md)** - Validação geográfica geral (área mínima/máxima, sobreposição espacial)

### Validações de Negócio
- **[email-validation.md](./email-validation.md)** - Validação de email (formato RFC 5322)
- **[phone-validation.md](./phone-validation.md)** - Validação de telefone (formato brasileiro DDD + número)
- **[business-validation.md](./business-validation.md)** - Validações de regras de negócio (idade titular, etc.)

### Validações de Entidades
- **[holder-validation.md](./holder-validation.md)** - Validação de Holder (CPF/CNPJ unicidade, LGPD, UnitHolder relationships)
- **[unit-validation.md](./unit-validation.md)** - Validação de Unit (code unicidade, geometria, área, spatial overlap)

---

**Última atualização:** 2025-01-05
