# DOCUMENTS

Validações de documentos do CARF. cpf-validation.md especifica algoritmo: remover formatação, verificar 11 dígitos, calcular primeiro dígito verificador (soma ponderada posições 1-9 multiplicadas por 10-2, mod 11, resultado 11 ou 10 vira 0), calcular segundo dígito (posições 1-10 multiplicadas por 11-2), comparar dígitos calculados vs fornecidos, rejeitar sequências repetidas (111.111.111-11). cnpj-validation.md similar com 14 dígitos e pesos diferentes. rg-validation.md validação formato por estado (SP: XX.XXX.XXX-X, RJ: XX.XXX.XXX-X, diferentes patterns). Implementação: value object CPF com validation no constructor, unit tests covering edge cases.

---

**Última atualização:** 2025-01-05
**Status do arquivo**: Review
