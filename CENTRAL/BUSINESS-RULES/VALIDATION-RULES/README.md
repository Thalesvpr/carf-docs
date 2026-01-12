# VALIDATION-RULES

Regras validação CARF organizadas categorias incluindo documentos CPF dígito verificador algoritmo mod 11 calculando dois dígitos verificadores rejeitando sequências conhecidas inválidas 00000000000 11111111111 22222222222 CNPJ validação similar mod 11 com quatorze dígitos formato XX.XXX.XXX/XXXX-XX RG formato variando estado São Paulo nove dígitos Rio Janeiro oito verificando padrões específicos UF geográficas coordenadas dentro bounds Brasil latitude menos trinta e quatro a seis longitude menos setenta e cinco a menos vinte e oito rejeitando coordenadas fora território nacional oceano polígonos sem self-intersections via PostGIS ST_IsValid topologia correta exterior ring counter-clockwise interior rings clockwise área mínima vinte metros quadrados máxima duzentos cinquenta metros quadrados REURB-S quinhentos metros quadrados REURB-E conforme Lei 13465 detecção sobreposição espacial ST_Overlaps impedindo units conflitantes mesmo terreno negócio email formato RFC 5322 regex pattern verificando local-part@domain TLD válido length limits telefone formato brasileiro DDD dois dígitos 11998765432 ou 1033334444 mobile landline respectivamente rejeitando sequences inválidas 11111111111 titular maior dezoito anos data nascimento comparada hoje impedindo menores titular principal property ownership legal capacity brasileira validações entidades complexas holder-validation verificando CPF CNPJ unicidade por tenant permitindo múltiplas units mesmo titular justificativa validando UnitHolder relationships CASCADE deletes orphan checks LGPD consent recorded unit-validation garantindo code unicidade comunidade geometria válida topologicamente área within bounds spatial overlap detection status transitions state machine DRAFT PENDING APPROVED REJECTED allowed flows apenas impedindo voltar approved para draft protegendo integridade processo legitimation implementadas múltiplas camadas value objects formato domain entities regras negócio validadores estruturais camada aplicação composição restrições banco dados última linha defesa.

## Regras

- **[business-validation.md](./business-validation.md)** - Validações regras negócio entidades complexas workflows
- **[cnpj-validation.md](./cnpj-validation.md)** - Validação CNPJ brasileiro algoritmo mod 11 quatorze dígitos
- **[coordinates-validation.md](./coordinates-validation.md)** - Validação coordenadas geográficas bounds território Brasil
- **[cpf-validation.md](./cpf-validation.md)** - Validação CPF brasileiro algoritmo mod 11 dígitos verificadores
- **[documents-validation.md](./documents-validation.md)** - Validação documentos RG formatos específicos UF
- **[email-validation.md](./email-validation.md)** - Validação email formato RFC 5322 regex pattern
- **[geographic-validation.md](./geographic-validation.md)** - Validação dados geográficos coordenadas limites espaciais
- **[geometry-validation.md](./geometry-validation.md)** - Validação geometrias polígonos topologia PostGIS ST_IsValid
- **[holder-validation.md](./holder-validation.md)** - Validação titular CPF unicidade tenant relationships
- **[phone-validation.md](./phone-validation.md)** - Validação telefone brasileiro DDD mobile landline
- **[unit-validation.md](./unit-validation.md)** - Validação unidade code unicidade geometria área bounds

---

**Última atualização:** 2026-01-11
