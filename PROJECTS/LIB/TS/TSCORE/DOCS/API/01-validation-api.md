---
type: leaf
status: review
updated: 2026-01-24
---

# API de Validacoes

API completa dos value objects de validacao fornecidos pelo modulo @carf/tscore/validations. Todos os validadores seguem o pattern de value object imutavel com validacao no construtor.

## CPF

Classe para validacao e manipulacao de CPF brasileiro. O construtor recebe string com ou sem mascara e lanca ValidationError se invalido. A propriedade value retorna os 11 digitos sem formatacao. O metodo format retorna com mascara padrao. O metodo estatico isValid permite validar sem instanciar. Os metodos clean e format estaticos manipulam strings diretamente. O metodo equals compara duas instancias por valor. A validacao aplica algoritmo mod-11 com dois digitos verificadores e rejeita sequencias conhecidas como onze digitos iguais.

## CNPJ

Classe para validacao de CNPJ brasileiro. Funciona de forma analoga ao CPF com construtor validador, propriedade value com 14 digitos, metodo format com mascara padrao e metodos estaticos isValid, clean e format. A validacao usa algoritmo mod-11 adaptado para 14 digitos com pesos especificos para cada posicao.

## Email

Classe para validacao de email conforme RFC 5322 simplificada. O construtor normaliza para lowercase. Propriedades local e domain expoe partes do endereco. A validacao requer arroba, parte local nao vazia e dominio com pelo menos um ponto para TLD.

## Phone

Classe para telefones brasileiros com DDD. Aceita 10 ou 11 digitos representando fixo ou celular. Propriedades ddd e number separam componentes. Metodos isMobile e isLandline identificam tipo. Validacao requer DDD entre 11 e 99, celular comecando com 9 e fixo comecando com 2 a 5.

## ValidationError

Excecao lancada por todos os value objects quando validacao falha. Extende Error padrao com name definido como ValidationError para identificacao em catch blocks.
