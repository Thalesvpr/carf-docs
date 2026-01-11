# CNPJ Validation

Regra de validação de Cadastro Nacional de Pessoa Jurídica brasileiro garantindo que apenas números válidos de empresas são aceitos onde validação inclui verificação de formato (14 dígitos numéricos), rejeição de sequências conhecidas como inválidas (00000000000000 até 99999999999999 todos iguais), cálculo de dígitos verificadores usando algoritmo oficial da Receita Federal, e identificação de matriz versus filial analisando últimos 4 dígitos antes dos verificadores. CNPJ pode ser fornecido formatado com pontos barra e hífen (##.###.###/####-##) ou apenas dígitos sendo normalizado para comparação e armazenamento removendo caracteres não numéricos antes de validação. Algoritmo de validação calcula primeiro dígito verificador multiplicando primeiros 12 dígitos por sequência cíclica 5 4 3 2 9 8 7 6 5 4 3 2 somando resultados calculando resto da divisão por 11 considerando 0 se resto for menor que 2 caso contrário 11 menos resto, depois calcula segundo dígito verificador multiplicando primeiros 12 dígitos mais primeiro verificador por sequência 6 5 4 3 2 9 8 7 6 5 4 3 2 aplicando mesma lógica de resto. Estrutura do CNPJ identifica raiz cadastral (primeiros 8 dígitos), filial (4 dígitos seguintes onde 0001 indica matriz e valores maiores indicam filiais), e dígitos verificadores (2 últimos) permitindo agrupar todas filiais de mesma empresa raiz para relatórios e análises.

**Formato aceito:** 14 dígitos numéricos ou ##.###.###/####-## (normalizado automaticamente)

**CNPJs inválidos conhecidos:** 00000000000000, 11111111111111, 22222222222222, ..., 99999999999999 (sequências repetidas)

**Estrutura:** RR.RRR.RRR/FFFF-DD onde RR.RRR.RRR = raiz (8 dígitos), FFFF = filial (0001 matriz, outros filiais), DD = dígitos verificadores

**Algoritmo dígito verificador:**

Primeiro dígito (posição 13):
1. Multiplicar dígitos 1-12 por: 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2
2. Somar resultados: soma = d1×5 + d2×4 + d3×3 + d4×2 + d5×9 + d6×8 + d7×7 + d8×6 + d9×5 + d10×4 + d11×3 + d12×2
3. Calcular resto: resto = soma mod 11
4. Dígito verificador: dv1 = (resto < 2) ? 0 : (11 - resto)

Segundo dígito (posição 14):
1. Multiplicar dígitos 1-12 + dv1 por: 6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2
2. Somar resultados: soma = d1×6 + d2×5 + d3×4 + d4×3 + d5×2 + d6×9 + d7×8 + d8×7 + d9×6 + d10×5 + d11×4 + d12×3 + dv1×2
3. Calcular resto: resto = soma mod 11
4. Dígito verificador: dv2 = (resto < 2) ? 0 : (11 - resto)

**Exemplo:** CNPJ 11.222.333/0001-81

Validação primeiro dígito:
- 1×5 + 1×4 + 2×3 + 2×2 + 2×9 + 3×8 + 3×7 + 3×6 + 0×5 + 0×4 + 0×3 + 1×2 = 140
- 140 mod 11 = 8
- dv1 = 11 - 8 = 3

(Nota: Exemplo ilustrativo, CNPJ real pode ter verificadores diferentes)

**Identificação matriz/filial:**
- Dígitos 9-12 (FFFF): 0001 = matriz, 0002+ = filial
- Mesmo CNPJ raiz com filiais diferentes são CNPJs distintos válidos
- Agrupar por raiz (primeiros 8 dígitos) para relatórios de grupo empresarial

**Normalização:** Remover caracteres não numéricos antes de validar (aceitar "11.222.333/0001-81" ou "11222333000181")

**Armazenamento:** Apenas dígitos numéricos sem formatação facilitando queries e comparações

**Exibição:** Formatado com pontos barra e hífen para legibilidade (##.###.###/####-##)

**Validações adicionais:**
- CNPJ matriz: filial = 0001
- CNPJ filial: filial > 0001
- Mesmo CNPJ raiz pode ter múltiplas filiais válidas

**Mensagens de erro:**
- "CNPJ inválido: deve conter 14 dígitos"
- "CNPJ inválido: sequência repetida não permitida"
- "CNPJ inválido: dígitos verificadores incorretos"
- "CNPJ já cadastrado no sistema" (validação de unicidade)

**Casos especiais:**
- Empresas individuais (MEI) possuem CNPJ válido
- Órgãos públicos possuem CNPJ válido
- Filiais encerradas podem ter CNPJ válido mas inativo (verificar situação cadastral via API Receita)

---

## 🔗 Relacionado

**Domain Model:**
- `../DOMAIN-MODEL/VALUE-OBJECTS/02-cnpj.md` - Value Object implementando validação
- `../DOMAIN-MODEL/ENTITIES/02-holder.md` - Entity usando CNPJ quando PJ

**Implementações:**
- (caminho de implementação) - Backend .NET
- (caminho de implementação) - Frontend React
- (caminho de implementação) - Mobile React Native

**Referências externas:**
- Receita Federal do Brasil - Algoritmo oficial
- ABNT NBR 9524 - Cadastro nacional de pessoa jurídica

---

**Última atualização:** 2025-01-06
