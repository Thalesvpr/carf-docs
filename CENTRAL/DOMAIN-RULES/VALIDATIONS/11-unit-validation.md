---
type: leaf
status: approved
updated: 2026-01-25
---

# Unit Validation

Regras de validacao aplicadas a entidade Unit garantindo integridade de dados espaciais, completude cadastral e compliance com requisitos de regularizacao fundiaria. Codigo deve ser unico dentro da comunidade, gerado automaticamente se nao fornecido. Comunidade e tenant sao obrigatorios.

Geometria deve ser poligono valido com minimo 3 vertices, sem auto-intersecao, contido dentro dos limites da comunidade. Area deve ser positiva e menor que limite maximo configuravel. Area calculada deve ser consistente com area declarada dentro de tolerancia de 10%. Deteccao de sobreposicao alerta analista sobre conflitos espaciais.

## Transicoes e Documentacao

Ao menos um titular deve estar vinculado antes de transicionar para status de revisao ou aprovacao. Foto frontal obrigatoria exceto para terrenos vazios. Limites de area variam conforme modalidade REURB sendo 250 metros quadrados para interesse social e 500 para interesse especifico. Validacao offline executa subset de regras com flag indicando validacao completa pendente durante sincronizacao.
