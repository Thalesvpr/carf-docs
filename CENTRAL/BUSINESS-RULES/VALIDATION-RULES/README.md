# VALIDATION-RULES

Regras de validação do CARF organizadas por categoria. DOCUMENTS contém validações de documentos (CPF dígito verificador algoritmo mod 11, CNPJ validação, RG formato por estado). GEOGRAPHIC contém validações geográficas (coordenadas dentro bounds Brasil -33.75/-73.98 a 5.27/-34.79, polígono sem auto-interseção via validação topológica, área mínima 20m² máxima 250m² para REURB-S, detecção de sobreposição espacial entre unidades). BUSINESS contém validações de negócio (titular maior 18 anos, email formato RFC 5322, telefone formato brasileiro DDD + número). Validações implementadas em múltiplas camadas: value objects (formato), domain entities (regras de negócio), validadores estruturais na camada de aplicação (composição), restrições de banco de dados (última linha de defesa).

---

**Última atualização:** 2025-01-05
