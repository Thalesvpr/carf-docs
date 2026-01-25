---
type: leaf
status: approved
updated: 2026-01-25
---

# Holder Validation

Regras de validacao aplicadas a entidade Holder garantindo integridade de dados pessoais, unicidade de identificacao e compliance LGPD. CPF ou CNPJ deve ser valido conforme algoritmo de digitos verificadores da Receita Federal, sendo unico por tenant. Exatamente um dos campos deve estar preenchido identificando pessoa fisica ou juridica.

Nome completo requer minimo duas palavras. Email segue RFC 5322 e telefone formato brasileiro com DDD valido. Data de nascimento deve ser passada com idade minima de 18 anos para titular principal. Vinculos com unidades via UnitHolder exigem soma de percentuais nao excedendo 100% e exatamente um titular primario por unidade.

## Documentacao

Ao menos um documento de identificacao (CPF, RG ou CNH) deve estar anexado antes de aprovacao. Comprovante de residencia requer data recente quando exigido pela modalidade. Para REURB-S, renda declarada nao pode exceder 3 salarios minimos. Sistema detecta duplicatas potenciais comparando CPF, similaridade de nome e proximidade de endereco alertando analista para decisao.
