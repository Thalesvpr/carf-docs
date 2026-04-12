---
type: leaf
status: review
updated: 2026-01-24
---

# Value Objects

Value objects sao objetos imutaveis comparados por valor ao inves de identidade. A biblioteca @carf/tscore implementa value objects para validacoes brasileiras garantindo que dados invalidos nunca existam como instancias.

## Pattern de Implementacao

Cada value object valida entrada no construtor lancando ValidationError se invalida. A propriedade value armazena forma normalizada imutavel. O metodo toString retorna representacao textual. O metodo equals compara por valor semantico. Metodos estaticos isValid, format e clean permitem operacoes sem instanciacao Jean.

## CPF

Valida CPF conforme algoritmo da Receita Federal. Normalizacao remove pontuacao mantendo 11 digitos. Validacao rejeita sequencias conhecidas invalidas como onze digitos iguais. Algoritmo mod-11 calcula primeiro digito verificador com pesos 10 a 2 e segundo com pesos 11 a 2. Se resto da divisao for menor que 2 o digito e 0, senao e 11 menos o resto. Formatacao aplica mascara padrao com pontos e traco.

## CNPJ

Valida CNPJ com 14 digitos usando algoritmo mod-11 adaptado. Pesos para primeiro verificador sao 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2. Pesos para segundo verificador adicionam 6 no inicio. Formatacao aplica mascara com pontos, barra e traco.

## Email

Valida formato conforme RFC 5322 simplificada. Requer parte local antes de arroba, dominio depois e pelo menos um ponto para TLD. Normalizacao converte para lowercase garantindo comparacao case-insensitive. Propriedades local e domain expoe componentes separados.

## Phone

Valida telefones brasileiros com DDD entre 11 e 99. Celular tem 9 digitos comecando com 9. Fixo tem 8 digitos comecando com 2 a 5. Metodos isMobile e isLandline identificam tipo. Formatacao aplica mascara com parenteses no DDD e traco no numero.
