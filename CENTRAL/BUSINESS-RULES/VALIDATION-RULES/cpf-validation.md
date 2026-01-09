# CPF Validation

Regra de validação de Cadastro de Pessoa Física brasileiro garantindo que apenas números válidos são aceitos no sistema onde validação inclui verificação de formato (11 dígitos numéricos), rejeição de sequências conhecidas como inválidas (00000000000 até 99999999999 todos iguais), e cálculo de dígitos verificadores usando algoritmo oficial da Receita Federal do Brasil. CPF pode ser fornecido formatado com pontos e hífen (###.###.###-##) ou apenas dígitos sendo normalizado para comparação e armazenamento removendo caracteres não numéricos antes de validação. Algoritmo de validação calcula primeiro dígito verificador multiplicando primeiros 9 dígitos por sequência decrescente 10 9 8 7 6 5 4 3 2 somando resultados calculando resto da divisão por 11 e invertendo (11 menos resto) considerando 0 se resultado for 10 ou 11, depois calcula segundo dígito verificador multiplicando primeiros 9 dígitos mais primeiro verificador por sequência 11 10 9 8 7 6 5 4 3 2 aplicando mesma lógica de resto e inversão. Validação de unicidade por tenant é responsabilidade de camada de application consultando repository para verificar se CPF já está vinculado a outro Holder evitando duplicação de titulares mas permitindo mesmo CPF em diferentes tenants isolados.

**Formato aceito:** 11 dígitos numéricos ou ###.###.###-## (normalizado automaticamente)

**CPFs inválidos conhecidos:** 00000000000, 11111111111, 22222222222, ..., 99999999999 (sequências repetidas)

**Algoritmo dígito verificador:**

Primeiro dígito (posição 10):
1. Multiplicar dígitos 1-9 por: 10, 9, 8, 7, 6, 5, 4, 3, 2
2. Somar resultados: soma = d1×10 + d2×9 + d3×8 + d4×7 + d5×6 + d6×5 + d7×4 + d8×3 + d9×2
3. Calcular resto: resto = soma mod 11
4. Dígito verificador: dv1 = (resto < 2) ? 0 : (11 - resto)

Segundo dígito (posição 11):
1. Multiplicar dígitos 1-9 + dv1 por: 11, 10, 9, 8, 7, 6, 5, 4, 3, 2
2. Somar resultados: soma = d1×11 + d2×10 + d3×9 + d4×8 + d5×7 + d6×6 + d7×5 + d8×4 + d9×3 + dv1×2
3. Calcular resto: resto = soma mod 11
4. Dígito verificador: dv2 = (resto < 2) ? 0 : (11 - resto)

**Exemplo:** CPF 123.456.789-09

Validação primeiro dígito:
- 1×10 + 2×9 + 3×8 + 4×7 + 5×6 + 6×5 + 7×4 + 8×3 + 9×2 = 210
- 210 mod 11 = 1
- dv1 = 11 - 1 = 10, mas como resultado ≥ 10 então dv1 = 0

Validação segundo dígito:
- 1×11 + 2×10 + 3×9 + 4×8 + 5×7 + 6×6 + 7×5 + 8×4 + 9×3 + 0×2 = 255
- 255 mod 11 = 2
- dv2 = 11 - 2 = 9

CPF válido: 123.456.789-09 ✅

**Normalização:** Remover caracteres não numéricos antes de validar (aceitar "123.456.789-09" ou "12345678909")

**Armazenamento:** Apenas dígitos numéricos sem formatação facilitando queries e comparações

**Exibição:** Formatado com pontos e hífen para legibilidade humana (###.###.###-##)

**Mensagens de erro:**
- "CPF inválido: deve conter 11 dígitos"
- "CPF inválido: sequência repetida não permitida"
- "CPF inválido: dígitos verificadores incorretos"
- "CPF já cadastrado no sistema" (validação de unicidade)

**Exceções:** CPF 000.000.000-00 é tecnicamente inválido mas pode aparecer em sistemas legados devendo ser rejeitado em novos cadastros

---

## 🔗 Relacionado

**Domain Model:**
- `../DOMAIN-MODEL/VALUE-OBJECTS/01-cpf.md` - Value Object implementando validação
- `../DOMAIN-MODEL/ENTITIES/02-holder.md` - Entity usando CPF validado

**Implementações:**
- `PROJECTS/GEOAPI/LAYERS/DOMAIN/VALUE-OBJECTS/Cpf.cs` - Backend .NET
- `PROJECTS/GEOWEB/UTILS/validators/cpfValidator.ts` - Frontend React
- `PROJECTS/REURBCAD/UTILS/cpfValidator.ts` - Mobile React Native

**Referências externas:**
- Receita Federal do Brasil - Algoritmo oficial
- ABNT NBR 9524 - Cadastro de pessoa física

---

**Última atualização:** 2025-01-06
